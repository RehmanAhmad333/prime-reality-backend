from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt, JWTError
import json
import logging
import asyncio

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.models.property import Property
from app.models.inquiry import Inquiry
from app.websocket.connection_manager import manager


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("/ws/{property_id}")
async def websocket_chat(
    websocket: WebSocket,
    property_id: int,
    token: str,  # Pass token as query parameter: ws://.../chat/ws/1?token=xxxx
):
    """
    WebSocket endpoint for real-time chat between buyer and seller.

    Authentication:
    Pass JWT token as query parameter `token`.

    Message Format Send:
    {"type": "message", "content": "Hello!", "timestamp": "2026-06-05T12:00:00Z"}
    {"type": "typing", "is_typing": true}

    Message Format Receive:
    {"type": "message", "user": "John", "role": "buyer", "message": "Hello!", "timestamp": "..."}
    {"type": "system", "message": "User joined"}
    {"type": "typing", "user": "John", "is_typing": true}
    """

    db: Session = SessionLocal()
    current_user = None
    is_connected = False
    ping_task = None

    try:
        # -------------------- Authenticate User --------------------
        if not token:
            logger.warning("WebSocket connection rejected: Missing token.")
            await websocket.close(code=1008)
            return

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            email = payload.get("sub")

            if not email:
                logger.warning("WebSocket connection rejected: Token subject missing.")
                await websocket.close(code=1008)
                return

            current_user = db.query(User).filter(User.email == email).first()

            if not current_user:
                logger.warning(
                    f"WebSocket connection rejected: User not found for email {email}."
                )
                await websocket.close(code=1008)
                return

        except JWTError as jwt_error:
            logger.error(f"JWT authentication error in WebSocket: {str(jwt_error)}")
            await websocket.close(code=1008)
            return

        except SQLAlchemyError as db_error:
            logger.error(
                f"Database error during WebSocket authentication: {str(db_error)}"
            )
            await websocket.close(code=1011)
            return

        # -------------------- Check Property Exists --------------------
        try:
            property_obj = db.query(Property).filter(
                Property.id == property_id
            ).first()

            if not property_obj:
                logger.warning(
                    f"WebSocket connection rejected: Property {property_id} not found."
                )
                await websocket.close(code=1004)
                return

        except SQLAlchemyError as db_error:
            logger.error(f"Database error while checking property: {str(db_error)}")
            await websocket.close(code=1011)
            return

        # -------------------- Determine User Role --------------------
        user_role = current_user.role
        is_seller = (property_obj.seller_id == current_user.id) or (user_role == "admin")
        is_buyer = user_role == "buyer"

        # -------------------- Connect to Room --------------------
        await manager.connect(websocket, property_id, current_user.id)
        is_connected = True

        await manager.send_personal_message(
            json.dumps({
                "type": "system",
                "message": f"Connected to chat for property: {property_obj.title}",
                "role": user_role
            }),
            websocket
        )

        logger.info(
            f"User {current_user.id} connected to WebSocket chat for property {property_id}"
        )

        # -------------------- Heartbeat / Ping Pong --------------------
        async def send_ping():
            while is_connected:
                await asyncio.sleep(30)

                try:
                    await websocket.send_text(json.dumps({"type": "ping"}))
                except Exception as e:
                    logger.warning(f"Ping failed for user {current_user.id}: {str(e)}")
                    break

        ping_task = asyncio.create_task(send_ping())

        # -------------------- Main Message Loop --------------------
        while True:
            data = await websocket.receive_text()

            # Skip ping responses
            if data == "pong":
                continue

            try:
                message_data = json.loads(data)

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from user {current_user.id}: {data}")

                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format."
                    }),
                    websocket
                )
                continue

            message_type = message_data.get("type")

            # -------------------- Chat Message --------------------
            if message_type == "message":
                content = message_data.get("content", "").strip()

                if not content:
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "error",
                            "message": "Message cannot be empty."
                        }),
                        websocket
                    )
                    continue

                # Broadcast to all participants
                await manager.broadcast_to_property(property_id, {
                    "type": "message",
                    "user": current_user.full_name,
                    "role": user_role,
                    "message": content,
                    "timestamp": message_data.get("timestamp")
                })

                # Save inquiry if buyer
                if is_buyer:
                    try:
                        new_inquiry = Inquiry(
                            property_id=property_id,
                            buyer_id=current_user.id,
                            message=content,
                            status="pending"
                        )

                        db.add(new_inquiry)
                        db.commit()

                    except SQLAlchemyError as db_error:
                        db.rollback()

                        logger.error(f"Failed to save inquiry: {str(db_error)}")

                        await manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "message": "Message sent but could not save inquiry."
                            }),
                            websocket
                        )

                    except Exception as e:
                        db.rollback()

                        logger.error(f"Unexpected error while saving inquiry: {str(e)}")

                        await manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "message": "Message sent but could not save inquiry."
                            }),
                            websocket
                        )

            # -------------------- Typing Indicator --------------------
            elif message_type == "typing":
                is_typing = message_data.get("is_typing", False)

                await manager.broadcast_to_property(property_id, {
                    "type": "typing",
                    "user": current_user.full_name,
                    "is_typing": is_typing
                })

            # -------------------- Unknown Message Type --------------------
            else:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    }),
                    websocket
                )

    except WebSocketDisconnect:
        if current_user:
            logger.info(
                f"User {current_user.id} disconnected from property {property_id}."
            )

    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in WebSocket chat: {str(db_error)}")

    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {str(e)}")

        try:
            await websocket.close(code=1011)
        except Exception:
            pass

    finally:
        # -------------------- Cleanup --------------------
        is_connected = False

        if ping_task:
            ping_task.cancel()

            try:
                await ping_task
            except asyncio.CancelledError:
                pass

        if is_connected and current_user:
            manager.disconnect(websocket, property_id, current_user.id)

        elif current_user:
            try:
                manager.disconnect(websocket, property_id, current_user.id)
            except Exception as e:
                logger.error(f"Error during WebSocket disconnect cleanup: {str(e)}")

        if current_user:
            try:
                await manager.broadcast_to_property(property_id, {
                    "type": "system",
                    "message": f"{current_user.full_name} has left the chat"
                })
            except Exception as e:
                logger.error(f"Error broadcasting leave message: {str(e)}")

        db.close()