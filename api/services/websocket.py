import json
from typing import Dict, Set
from datetime import datetime
from fastapi import WebSocket
from api.models.schemas import WebSocketMessage

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = set()
        self.active_connections[project_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, project_id: str):
        """Disconnect a WebSocket client"""
        if project_id in self.active_connections and websocket in self.active_connections[project_id]:
            self.active_connections[project_id].remove(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    def _serialize_datetime(self, obj):
        """Helper method to serialize datetime objects in JSON"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    async def broadcast_to_project(self, project_id: str, message_type: str, data: dict):
        """Broadcast a message to all clients connected to a project"""
        if project_id in self.active_connections:
            message = WebSocketMessage(
                type=message_type,
                data=data,
                timestamp=datetime.now()
            )
            
            message_json = json.dumps(message.dict(), default=self._serialize_datetime)
            
            dead_connections = set()
            for connection in self.active_connections[project_id]:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"Error sending message: {str(e)}")
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for dead in dead_connections:
                await self.disconnect(dead, project_id)

    async def send_status(self, project_id: str, status: str, details: dict = None):
        """Send a status update"""
        await self.broadcast_to_project(project_id, "status", {
            "status": status,
            "details": details or {}
        })

    async def send_error(self, project_id: str, error: str):
        """Send an error message"""
        await self.broadcast_to_project(project_id, "error", {
            "error": error
        })

    async def send_preview_update(self, project_id: str, preview_url: str):
        """Send a preview URL update"""
        await self.broadcast_to_project(project_id, "preview", {
            "url": preview_url
        })

    async def send_completion(self, project_id: str, success: bool, details: dict = None):
        """Send a completion message"""
        await self.broadcast_to_project(project_id, "completion", {
            "success": success,
            "details": details or {}
        }) 