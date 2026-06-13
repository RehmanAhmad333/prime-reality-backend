from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt, JWTError
import json
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
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
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time chat between buyer and seller."""

    current_user = None
    is_connected = False

    # -------------------- Authenticate User --------------------
    try:
        if not token:
            logger.warning("WebSocket connection rejected: Missing token.")
            await websocket.close(code=1008)
            return

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
            logger.warning(f"WebSocket connection rejected: User not found for email {email}.")
            await websocket.close(code=1008)
            return

    except JWTError as jwt_error:
        logger.error(f"JWT authentication error in WebSocket: {str(jwt_error)}")
        await websocket.close(code=1008)
        return

    except SQLAlchemyError as db_error:
        logger.error(f"Database error during WebSocket authentication: {str(db_error)}")
        await websocket.close(code=1011)
        return

    except Exception as e:
        logger.error(f"Unexpected authentication error: {str(e)}")
        await websocket.close(code=1008)
        return

    # -------------------- Check Property Exists --------------------
    try:
        property = db.query(Property).filter(Property.id == property_id).first()

        if not property:
            logger.warning(f"WebSocket connection rejected: Property {property_id} not found.")
            await websocket.close(code=1004)
            return

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while checking property: {str(db_error)}")
        await websocket.close(code=1011)
        return

    except Exception as e:
        logger.error(f"Unexpected error while checking property: {str(e)}")
        await websocket.close(code=1011)
        return

    # -------------------- Determine User Role --------------------
    try:
        user_role = current_user.role
        is_seller = (property.seller_id == current_user.id) or (user_role == "admin")
        is_buyer = user_role == "buyer"

    except Exception as e:
        logger.error(f"Error determining user role: {str(e)}")
        await websocket.close(code=1011)
        return

    # -------------------- Connect to Room --------------------
    try:
        await manager.connect(websocket, property_id, current_user.id)
        is_connected = True

        await manager.send_personal_message(
            json.dumps({
                "type": "system",
                "message": f"Connected to chat for property: {property.title}",
                "role": user_role
            }),
            websocket
        )

        logger.info(
            f"User {current_user.id} connected to WebSocket chat for property {property_id}"
        )

    except Exception as e:
        logger.error(f"Error while connecting WebSocket: {str(e)}")
        if is_connected:
            manager.disconnect(websocket, property_id, current_user.id)
        await websocket.close(code=1011)
        return

    # -------------------- Receive and Handle Messages --------------------
    try:
        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                logger.warning(
                    f"Invalid JSON received from user {current_user.id}: {data}"
                )
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Invalid message format. Please send valid JSON."
                    }),
                    websocket
                )
                continue

            message_type = message_data.get("type")

            # -------------------- Normal Chat Message --------------------
            if message_type == "message":
                content = message_data.get("content")

                if not content or not str(content).strip():
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "error",
                            "message": "Message content cannot be empty."
                        }),
                        websocket
                    )
                    continue

                await manager.broadcast_to_property(property_id, {
                    "type": "message",
                    "user": current_user.full_name,
                    "role": user_role,
                    "message": content,
                    "timestamp": message_data.get("timestamp")
                })

                # If buyer sends message, also create an inquiry record
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
                        logger.error(
                            f"Database error while saving inquiry: {str(db_error)}"
                        )
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "message": "Message sent, but inquiry could not be saved."
                            }),
                            websocket
                        )

                    except Exception as e:
                        db.rollback()
                        logger.error(
                            f"Unexpected error while saving inquiry: {str(e)}"
                        )
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "message": "Message sent, but inquiry could not be saved."
                            }),
                            websocket
                        )

            # -------------------- Typing Status --------------------
            elif message_type == "typing":
                await manager.broadcast_to_property(property_id, {
                    "type": "typing",
                    "user": current_user.full_name,
                    "is_typing": message_data.get("is_typing")
                })

            # -------------------- Unknown Message Type --------------------
            else:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Unsupported message type."
                    }),
                    websocket
                )

    except WebSocketDisconnect:
        logger.info(
            f"User {current_user.id} disconnected from property chat {property_id}"
        )

        manager.disconnect(websocket, property_id, current_user.id)

        await manager.broadcast_to_property(property_id, {
            "type": "system",
            "message": f"{current_user.full_name} has left the chat"
        })

    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in WebSocket chat: {str(db_error)}")

        if is_connected:
            manager.disconnect(websocket, property_id, current_user.id)

    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {str(e)}")

        if is_connected:
            manager.disconnect(websocket, property_id, current_user.id)

        try:
            await websocket.close(code=1011)
        except Exception:
            pass