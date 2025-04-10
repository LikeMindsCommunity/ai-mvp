import json
from fastapi import WebSocket
from api.infrastructure import CodeGeneratorServiceImpl
from typing import Dict

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.code_generator_service = CodeGeneratorServiceImpl()
    
    async def handle_websocket(self, websocket: WebSocket):
        """
        Handle WebSocket connection and messages.
        
        Args:
            websocket (WebSocket): The WebSocket connection
        """
        await websocket.accept()
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if "user_query" not in message:
                    await websocket.send_json({
                        "type": "Error",
                        "value": "Missing user_query in request"
                    })
                    continue
                
                # Define callback for handling chunks
                async def on_chunk(response: Dict):
                    await websocket.send_json(response)
                
                # Generate project
                result = await self.code_generator_service.generate_project(
                    message["user_query"],
                    on_chunk
                )
                
                # Send final result
                await websocket.send_json({
                    "type": "Result",
                    "value": result
                })
                
        except Exception as e:
            await websocket.send_json({
                "type": "Error",
                "value": str(e)
            })
        finally:
            await websocket.close() 