"""
WebSocket handler for Flutter code generation.

Response Types:
- Text: Status updates and progress messages
- Code: Generated code content
- Chat: Conversational explanations and plans
- Error: Error messages
- Success: Success notifications
- AnalysisError: Flutter code analysis errors
- Result: Final result with URL and file path information
"""

import json
import os
from typing import Dict, Any, Optional
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
import asyncio

from api.infrastructure.services.flutter_generator_service_impl import FlutterGeneratorServiceImpl
from api.infrastructure.database import SupabaseManager
from api.infrastructure.auth import get_current_user
from api.infrastructure.projects.service import get_project
from api.infrastructure.code_generations.service import create_code_generation, update_code_generation

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.flutter_generator_service = FlutterGeneratorServiceImpl()
        self.supabase_manager = SupabaseManager()  # Eventually this can be removed once all methods are migrated to services
    
    async def handle_websocket(self, websocket: WebSocket, token: str, project_id: str):
        """
        Handle WebSocket connection and messages.
        
        Args:
            websocket (WebSocket): The WebSocket connection
            token (str): JWT access token for authentication
            project_id (str): Project ID to associate with this session
        """
        await websocket.accept()
        
        try:
            # Verify the token and project access
            try:
                # Use the centralized auth validation
                user = await get_current_user(token)
                
                if not user:
                    await websocket.send_json({
                        "type": "Error",
                        "value": "Invalid authentication token"
                    })
                    await websocket.close()
                    return
                
                # Extract the access token
                access_token = user.get('access_token')
                if not access_token:
                    await websocket.send_json({
                        "type": "Error",
                        "value": "Invalid or missing access token"
                    })
                    await websocket.close()
                    return
                
                # Verify project access
                project = await get_project(project_id, access_token)
                if not project or not project.data:
                    await websocket.send_json({
                        "type": "Error",
                        "value": "Project not found or you don't have access"
                    })
                    await websocket.close()
                    return

                # Create project output directory if it doesn't exist
                project_output_dir = os.path.join("output", project_id)
                os.makedirs(project_output_dir, exist_ok=True)
                
                # Send confirmation of connection
                await websocket.send_json({
                    "type": "Success",
                    "value": {
                        "message": "Connected successfully",
                        "project": {
                            "id": project_id,
                            "name": project.data.get("name")
                        }
                    }
                })
                
            except HTTPException as e:
                await websocket.send_json({
                    "type": "Error",
                    "value": e.detail
                })
                await websocket.close()
                return
            except Exception as e:
                await websocket.send_json({
                    "type": "Error",
                    "value": f"Authentication error: {str(e)}"
                })
                await websocket.close()
                return
            
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
                    # Add a tiny delay to ensure chunks are processed individually
                    # Small enough not to be noticeable but helps prevent buffering
                    if response.get("type") == "Text":
                        await asyncio.sleep(0.02)  # Slightly longer delay for text chunks
                    elif response.get("type") == "Chat":
                        await asyncio.sleep(0.02)  # Similar delay for chat chunks
                    else:
                        await asyncio.sleep(0.005)  # Minimal delay for other message types
                
                # Extract session ID if available, otherwise use project_id
                session_id = message.get("session_id", project_id)
                
                # Create a code generation record in the database
                if message["type"] in ["GenerateCode", "GenerateConversation", "FixCode"]:
                    if "user_query" in message:
                        try:
                            # Create a code generation record
                            generation_result = await create_code_generation(
                                project_id=project_id,
                                prompt=message["user_query"],
                                jwt=access_token
                            )
                            
                            # Use the generation ID as part of the generation context
                            generation_id = generation_result.data[0]["id"]
                            output_path = os.path.join(project_output_dir, f"{generation_id}.dart")
                            
                            # Update the message with context
                            message["generation_id"] = generation_id
                            message["output_path"] = output_path
                        except Exception as e:
                            # Log the error but continue - this is not critical
                            print(f"Failed to create code generation record: {str(e)}")
                
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
                        on_chunk,
                        session_id
                    )
                    
                    # Update the generation record with the result
                    if "generation_id" in message:
                        try:
                            await update_code_generation(
                                message["generation_id"],
                                {
                                    "status": "completed" if result.get("success", False) else "error",
                                    "code_content": result.get("code", ""),
                                    "output_path": result.get("file_path", ""),
                                    "analysis_results": result.get("analysis", {})
                                },
                                access_token
                            )
                        except Exception as e:
                            # Log the error but continue - this is not critical
                            print(f"Failed to update code generation record: {str(e)}")
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "Result",
                        "value": result
                    })
                
                elif message["type"] == "GenerateConversation":
                    if "user_query" not in message:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Missing 'user_query' field in request"
                        })
                        continue
                    
                    # Generate only conversation/explanation
                    conversation_text = await self.flutter_generator_service.generate_conversation(
                        message["user_query"],
                        on_chunk,
                        session_id
                    )
                    
                    # Update the generation record with the result
                    if "generation_id" in message:
                        try:
                            await update_code_generation(
                                message["generation_id"],
                                {
                                    "status": "completed",
                                    "code_content": conversation_text,
                                },
                                access_token
                            )
                        except Exception as e:
                            # Log the error but continue - this is not critical
                            print(f"Failed to update code generation record: {str(e)}")
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "Result",
                        "value": {
                            "success": True,
                            "conversation": conversation_text
                        }
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
                        on_chunk,
                        session_id
                    )
                    
                    # Update the generation record with the result
                    if "generation_id" in message:
                        try:
                            await update_code_generation(
                                message["generation_id"],
                                {
                                    "status": "completed" if result.get("success", False) else "error",
                                    "code_content": result.get("code", ""),
                                    "output_path": result.get("file_path", ""),
                                    "analysis_results": result.get("analysis", {})
                                },
                                access_token
                            )
                        except Exception as e:
                            # Log the error but continue - this is not critical
                            print(f"Failed to update code generation record: {str(e)}")
                    
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