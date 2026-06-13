from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging


logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # Store active connections by property_id -> list of WebSockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

        # Store user_id to property_id mapping
        self.user_sessions: Dict[int, int] = {}

    async def connect(self, websocket: WebSocket, property_id: int, user_id: int):
        try:
            await websocket.accept()

            if property_id not in self.active_connections:
                self.active_connections[property_id] = []

            self.active_connections[property_id].append(websocket)
            self.user_sessions[user_id] = property_id

            logger.info(f"User {user_id} connected to property {property_id}")

        except Exception as e:
            logger.error(
                f"Error while connecting user {user_id} to property {property_id}: {str(e)}"
            )

    def disconnect(self, websocket: WebSocket, property_id: int, user_id: int):
        try:
            if property_id in self.active_connections:
                if websocket in self.active_connections[property_id]:
                    self.active_connections[property_id].remove(websocket)

                if not self.active_connections[property_id]:
                    del self.active_connections[property_id]

            if user_id in self.user_sessions:
                del self.user_sessions[user_id]

            logger.info(f"User {user_id} disconnected from property {property_id}")

        except Exception as e:
            logger.error(
                f"Error while disconnecting user {user_id} from property {property_id}: {str(e)}"
            )

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)

        except WebSocketDisconnect:
            logger.warning("WebSocket disconnected while sending personal message.")

        except Exception as e:
            logger.error(f"Error sending personal message: {str(e)}")

    async def broadcast_to_property(self, property_id: int, message: dict):
        """Send message to all users connected to a specific property chat."""

        try:
            if property_id in self.active_connections:
                disconnected_connections = []

                for connection in self.active_connections[property_id]:
                    try:
                        await connection.send_text(json.dumps(message))

                    except WebSocketDisconnect:
                        disconnected_connections.append(connection)
                        logger.warning(
                            f"WebSocket disconnected during broadcast for property {property_id}"
                        )

                    except Exception as e:
                        disconnected_connections.append(connection)
                        logger.error(
                            f"Error broadcasting message to property {property_id}: {str(e)}"
                        )

                # Remove disconnected/broken connections safely
                for connection in disconnected_connections:
                    if connection in self.active_connections.get(property_id, []):
                        self.active_connections[property_id].remove(connection)

                if property_id in self.active_connections and not self.active_connections[property_id]:
                    del self.active_connections[property_id]

        except Exception as e:
            logger.error(
                f"Unexpected error in broadcast_to_property for property {property_id}: {str(e)}"
            )

    async def notify_seller(self, property_id: int, buyer_name: str, message: str):
        """Notify seller about new inquiry via WebSocket."""

        try:
            notification = {
                "type": "inquiry",
                "buyer_name": buyer_name,
                "message": message,
                "property_id": property_id
            }

            await self.broadcast_to_property(property_id, notification)

        except Exception as e:
            logger.error(
                f"Error notifying seller for property {property_id}: {str(e)}"
            )


manager = ConnectionManager()