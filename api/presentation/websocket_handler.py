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
from api.infrastructure.auth.service import refresh_token
from api.infrastructure.projects.service import get_project
from api.infrastructure.code_generations.service import create_code_generation, update_code_generation
from api.presentation.exceptions import APIException

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.flutter_generator_service = FlutterGeneratorServiceImpl()
        self.supabase_manager = SupabaseManager()  # Eventually this can be removed once all methods are migrated to services
        # Track active generation IDs for cleanup on disconnect
        self.active_generation_ids = {}
    
    async def send_error(self, websocket: WebSocket, message: str) -> None:
        """Send an error message and close the connection."""
        await websocket.send_json({
            "type": "Error",
            "value": message
        })
        await websocket.close()
    
    async def send_token_expired(self, websocket: WebSocket) -> None:
        """Send a token expired message without closing the connection."""
        await websocket.send_json({
            "type": "TokenExpired",
            "value": "Authentication token has expired. Please refresh the token."
        })
    
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
            # Track authentication state
            access_token = token
            user = None
            
            # Initialize session tracking
            websocket_id = str(id(websocket))
            self.active_generation_ids[websocket_id] = set()
            
            # Verify the token and project access
            try:
                # Use the centralized auth validation
                user = await get_current_user(token)
                
                if not user:
                    await self.send_error(websocket, "Invalid authentication token")
                    return
                
                # Extract the access token
                access_token = user.get('access_token')
                if not access_token:
                    await self.send_error(websocket, "Invalid or missing access token")
                    return
                
                # Verify project access
                project = await get_project(project_id, access_token)
                if not project or not project.data:
                    await self.send_error(websocket, "Project not found or you don't have access")
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
                if e.status_code == 401:
                    # Token likely expired, notify client
                    await self.send_token_expired(websocket)
                else:
                    await self.send_error(websocket, e.detail)
                    return
            except Exception as e:
                await self.send_error(websocket, f"Authentication error: {str(e)}")
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
                
                # Handle token refresh
                if message["type"] == "RefreshToken":
                    if "refresh_token" not in message:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Missing 'refresh_token' field in request"
                        })
                        continue
                    
                    try:
                        # Refresh the token
                        refresh_result = await refresh_token(message["refresh_token"])
                        access_token = refresh_result["access_token"]
                        
                        # Update the user
                        user = await get_current_user(access_token)
                        
                        # Notify client of successful refresh
                        await websocket.send_json({
                            "type": "TokenRefreshed",
                            "value": {
                                "access_token": access_token,
                                "refresh_token": refresh_result["refresh_token"]
                            }
                        })
                        
                        # Re-verify project access with new token
                        project = await get_project(project_id, access_token)
                        if not project or not project.data:
                            await self.send_error(websocket, "Project not found or you don't have access")
                            return
                            
                        continue
                    except Exception as e:
                        await self.send_error(websocket, f"Token refresh failed: {str(e)}")
                        return
                
                # Handle cleanup for a specific generation
                if message["type"] == "CleanupGeneration":
                    if "generation_id" not in message:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Missing 'generation_id' field in request"
                        })
                        continue
                    
                    generation_id = message["generation_id"]
                    
                    try:
                        # Clean up resources for this generation
                        success = self.flutter_generator_service.cleanup_generation(generation_id)
                        
                        # Remove from tracking
                        if websocket_id in self.active_generation_ids:
                            self.active_generation_ids[websocket_id].discard(generation_id)
                        
                        # Notify client of result
                        await websocket.send_json({
                            "type": "Success" if success else "Error",
                            "value": f"Generation {generation_id} cleanup {'completed' if success else 'failed'}"
                        })
                        
                        continue
                    except Exception as e:
                        await websocket.send_json({
                            "type": "Error",
                            "value": f"Cleanup failed: {str(e)}"
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
                
                try:
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
                                
                                if not generation_result or not generation_result.data:
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": "Failed to create code generation record"
                                    })
                                    continue
                                
                                # Use the generation ID as part of the generation context
                                generation_id = generation_result.data[0]["id"]
                                output_path = os.path.join(project_output_dir, f"{generation_id}.dart")
                                
                                # Update the message with context
                                message["generation_id"] = generation_id
                                message["output_path"] = output_path
                            except HTTPException as e:
                                if e.status_code == 401:
                                    # Token expired during operation
                                    await self.send_token_expired(websocket)
                                    continue
                                else:
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": e.detail
                                    })
                                    continue
                            except Exception as e:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Failed to create code generation record: {str(e)}"
                                })
                                continue
                    
                    # Handle different message types
                    if message["type"] == "GenerateCode":
                        if "user_query" not in message:
                            await websocket.send_json({
                                "type": "Error",
                                "value": "Missing 'user_query' field in request"
                            })
                            continue
                        
                        # Generate code - pass the database generation_id to ensure we use the same ID
                        result = await self.flutter_generator_service.generate_flutter_code(
                            message["user_query"],
                            on_chunk,
                            session_id,
                            message.get("generation_id")  # Pass the database ID
                        )
                        
                        # Track the generation ID for cleanup on disconnect
                        if result.get("generation_id") and websocket_id in self.active_generation_ids:
                            self.active_generation_ids[websocket_id].add(result["generation_id"])
                        
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
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Failed to update code generation record: {str(e)}"
                                })
                        
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
                        
                        # Generate conversation
                        result = await self.flutter_generator_service.generate_conversation(
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
                                        "conversation": result.get("conversation", [])
                                    },
                                    access_token
                                )
                            except Exception as e:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Failed to update code generation record: {str(e)}"
                                })
                        
                        # Send final result
                        await websocket.send_json({
                            "type": "Result",
                            "value": result
                        })
                    
                    elif message["type"] == "FixCode":
                        if "user_query" not in message or "error_message" not in message:
                            await websocket.send_json({
                                "type": "Error",
                                "value": "Missing required fields in request"
                            })
                            continue
                        
                        # Get generation ID that should already exist in the database
                        existing_generation_id = message.get("generation_id")
                        
                        if not existing_generation_id:
                            await websocket.send_json({
                                "type": "Error",
                                "value": "Missing 'generation_id' field in request, which is required for fixing code"
                            })
                            continue
                        
                        # Fix code
                        result = await self.flutter_generator_service.fix_flutter_code(
                            message["user_query"],
                            message["error_message"],
                            on_chunk,
                            session_id,
                            existing_generation_id
                        )
                        
                        # Track the generation ID for cleanup on disconnect
                        if result.get("generation_id") and websocket_id in self.active_generation_ids:
                            self.active_generation_ids[websocket_id].add(result["generation_id"])
                        
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
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Failed to update code generation record: {str(e)}"
                                })
                        
                        # Send final result
                        await websocket.send_json({
                            "type": "Result",
                            "value": result
                        })
                    
                    else:
                        await websocket.send_json({
                            "type": "Error",
                            "value": f"Unsupported message type: {message['type']}"
                        })
                
                except HTTPException as e:
                    if e.status_code == 401:
                        # Token expired during operation
                        await self.send_token_expired(websocket)
                        continue
                    else:
                        await websocket.send_json({
                            "type": "Error",
                            "value": e.detail
                        })
                except Exception as e:
                    await websocket.send_json({
                        "type": "Error",
                        "value": f"Error processing request: {str(e)}"
                    })
        
        except WebSocketDisconnect:
            # Client disconnected, clean up resources
            if websocket_id in self.active_generation_ids:
                for generation_id in self.active_generation_ids[websocket_id]:
                    try:
                        self.flutter_generator_service.cleanup_generation(generation_id)
                    except Exception as e:
                        print(f"Error cleaning up generation {generation_id} on disconnect: {str(e)}")
                
                # Remove tracking for this websocket
                del self.active_generation_ids[websocket_id]
        except Exception as e:
            # Unexpected error
            await self.send_error(websocket, f"Unexpected error: {str(e)}")
            
            # Clean up resources even on error
            if websocket_id in self.active_generation_ids:
                for generation_id in self.active_generation_ids[websocket_id]:
                    try:
                        self.flutter_generator_service.cleanup_generation(generation_id)
                    except:
                        pass
                
                # Remove tracking for this websocket
                del self.active_generation_ids[websocket_id]
            return 