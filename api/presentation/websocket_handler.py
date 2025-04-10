import json
from fastapi import WebSocket
from api.infrastructure.services.code_generator_service_impl import CodeGeneratorServiceImpl

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
                
                # Generate project
                result = await self.code_generator_service.generate_project(
                    message["user_query"],
                    websocket
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