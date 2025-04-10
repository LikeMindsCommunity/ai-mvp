"""
WebSocket handler for Flutter code generation.
"""

import json
from typing import Dict, Any
from fastapi import WebSocket, WebSocketDisconnect

from api.infrastructure.services.flutter_generator_service_impl import FlutterGeneratorServiceImpl

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.flutter_generator_service = FlutterGeneratorServiceImpl()
    
    async def handle_websocket(self, websocket: WebSocket):
        """
        Handle WebSocket connection and messages.
        
        Args:
            websocket (WebSocket): The WebSocket connection
        """
        await websocket.accept()
        
        try:
            # Process incoming messages
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Validate message structure
                if "type" not in message:
                    await websocket.send_json({
                        "type": "Error",
                        "value": "Missing 'type' field in request"
                    })
                    continue
                
                # Define callback for streaming responses
                async def on_chunk(response: Dict[str, Any]):
                    await websocket.send_json(response)
                
                # Handle different message types
                if message["type"] == "GenerateCode":
                    if "user_query" not in message:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Missing 'user_query' field in request"
                        })
                        continue
                    
                    # Generate code
                    result = await self.flutter_generator_service.generate_flutter_code(
                        message["user_query"],
                        on_chunk
                    )
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "Result",
                        "value": result
                    })
                
                elif message["type"] == "FixCode":
                    if "user_query" not in message or "error_message" not in message:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Missing 'user_query' or 'error_message' field in request"
                        })
                        continue
                    
                    # Fix code with errors
                    result = await self.flutter_generator_service.fix_flutter_code(
                        message["user_query"],
                        message["error_message"],
                        on_chunk
                    )
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "Result",
                        "value": result
                    })
                
                else:
                    await websocket.send_json({
                        "type": "Error",
                        "value": f"Unknown message type: {message['type']}"
                    })
        
        except WebSocketDisconnect:
            # Client disconnected
            pass
        except Exception as e:
            # Send error message
            try:
                await websocket.send_json({
                    "type": "Error",
                    "value": str(e)
                })
            except:
                # Websocket already closed
                pass
        finally:
            # Ensure websocket is closed
            try:
                await websocket.close()
            except:
                pass 