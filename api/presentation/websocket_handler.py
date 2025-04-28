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
from api.infrastructure.code_generations.service import create_code_generation, update_code_generation, get_project_conversations, get_pending_generation, get_generation_by_id
from api.presentation.exceptions import APIException

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.flutter_generator_service = FlutterGeneratorServiceImpl()
        self.supabase_manager = SupabaseManager()  # Eventually this can be removed once all methods are migrated to services
        # Track active project IDs for cleanup on disconnect
        self.active_projects = {}
    
    async def send_error(self, websocket: WebSocket, message: str) -> None:
        """Send an error message and close the connection."""
        try:
            # Try to send error without checking state first
            await websocket.send_json({
                "type": "Error",
                "value": message
            })
            await websocket.close()
        except Exception as e:
            # Log the error but don't try to send any more messages
            print(f"Error sending error message: {str(e)}")
    
    async def send_token_expired(self, websocket: WebSocket) -> None:
        """Send a token expired message without closing the connection."""
        try:
            # Try to send without checking state first
            await websocket.send_json({
                "type": "TokenExpired",
                "value": "Authentication token has expired. Please refresh the token."
            })
        except Exception as e:
            # Log the error but don't try to send any more messages
            print(f"Error sending token expired message: {str(e)}")
    
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
            self.active_projects[websocket_id] = project_id
            
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
                
                # Send connection confirmation first before doing any potentially time-consuming operations
                try:
                    await websocket.send_json({
                        "type": "Text",
                        "value": {
                            "message": "Connected successfully",
                            "project": {
                                "id": project_id,
                                "name": project.data.get("name")
                            }
                        }
                    })
                except Exception as e:
                    print(f"Error sending connection confirmation: {str(e)}")
                    return
                
                # Fetch conversation history after confirming connection
                try:
                    conversation_history = await get_project_conversations(
                        project_id=project_id,
                        jwt=access_token
                    )
                    
                    # Send conversation history without checking state
                    try:
                        # Send conversation history automatically if available
                        if conversation_history and conversation_history.data:
                            await websocket.send_json({
                                "type": "ConversationHistory",
                                "value": conversation_history.data
                            })
                    except Exception as send_error:
                        print(f"Failed to send conversation history: {str(send_error)}")
                except Exception as e:
                    # Just log the error without trying to send to client in case the connection is closed
                    print(f"Failed to fetch initial project history: {str(e)}")
                
            except HTTPException as e:
                if e.status_code == 401:
                    # Token likely expired, notify client
                    try:
                        await self.send_token_expired(websocket)
                    except Exception:
                        print("Failed to send token expired notification")
                else:
                    try:
                        await self.send_error(websocket, e.detail)
                    except Exception:
                        print("Failed to send error details")
                    return
            except WebSocketDisconnect:
                # Client disconnected during initialization, just clean up
                if websocket_id in self.active_projects:
                    try:
                        project_id = self.active_projects[websocket_id]
                        # self.flutter_generator_service.cleanup_generation(project_id)
                    except Exception as cleanup_error:
                        print(f"Error during disconnect cleanup: {str(cleanup_error)}")
                    
                    # Remove tracking for this websocket
                    del self.active_projects[websocket_id]
                return
            except Exception as e:
                # Unexpected error during initialization
                try:
                    await self.send_error(websocket, f"Authentication error: {str(e)}")
                except Exception:
                    # Connection might be closed now, just log
                    print(f"Cannot send error to client: {str(e)}")
                return
            
            # Process incoming messages
            while True:
                try:
                    # Receive message from client
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Validate message structure
                    if "type" not in message:
                        try:
                            await websocket.send_json({
                                "type": "Error",
                                "value": "Missing 'type' field in request"
                            })
                        except Exception:
                            print("Failed to send message validation error")
                        continue
                    
                    # Handle token refresh
                    if message["type"] == "RefreshToken":
                        if "refresh_token" not in message:
                            try:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": "Missing 'refresh_token' field in request"
                                })
                            except Exception:
                                print("Failed to send missing refresh token error")
                            continue
                        
                        try:
                            # Refresh the token
                            refresh_result = await refresh_token(message["refresh_token"])
                            access_token = refresh_result["access_token"]
                            
                            # Update the user
                            user = await get_current_user(access_token)
                            
                            # Notify client of successful refresh
                            try:
                                await websocket.send_json({
                                    "type": "TokenRefreshed",
                                    "value": {
                                        "access_token": access_token,
                                        "refresh_token": refresh_result["refresh_token"]
                                    }
                                })
                            except Exception:
                                print("Failed to send token refresh confirmation")
                                return
                            
                            # Re-verify project access with new token
                            project = await get_project(project_id, access_token)
                            if not project or not project.data:
                                await self.send_error(websocket, "Project not found or you don't have access")
                                return
                                
                            continue
                        except Exception as e:
                            await self.send_error(websocket, f"Token refresh failed: {str(e)}")
                            return
                    
                    # Handle cleanup for a specific project
                    if message["type"] == "CleanupProject":
                        try:
                            # Clean up resources for this project
                            success = self.flutter_generator_service.cleanup_generation(project_id)
                            
                            # Notify client of result
                            try:
                                await websocket.send_json({
                                    "type": "Success" if success else "Error",
                                    "value": f"Project {project_id} cleanup {'completed' if success else 'failed'}"
                                })
                            except Exception:
                                print("Failed to send cleanup result")
                            
                            continue
                        except Exception as e:
                            try:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Cleanup failed: {str(e)}"
                                })
                            except Exception:
                                print("Failed to send cleanup error")
                            continue
                    
                    # Handle manual refreshing of project conversation history
                    if message["type"] == "GetProjectConversations":
                        try:
                            # Fetch all conversations for this project
                            conversations = await get_project_conversations(
                                project_id=project_id,
                                jwt=access_token
                            )
                            
                            # Send conversation history to the client
                            try:
                                await websocket.send_json({
                                    "type": "ConversationHistory",
                                    "value": conversations.data if conversations else []
                                })
                            except Exception:
                                print("Failed to send conversation history response")
                            
                            continue
                        except Exception as e:
                            try:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": f"Failed to fetch project conversations: {str(e)}"
                                })
                            except Exception:
                                print("Failed to send conversation fetch error")
                            continue
                    
                    # Define callback for streaming responses
                    async def on_chunk(response: Dict[str, Any]):
                        try:
                            await websocket.send_json(response)
                            # Add a tiny delay to ensure chunks are processed individually
                            # Small enough not to be noticeable but helps prevent buffering
                            if response.get("type") == "Text":
                                await asyncio.sleep(0.02)  # Slightly longer delay for text chunks
                            elif response.get("type") == "Chat":
                                await asyncio.sleep(0.02)  # Similar delay for chat chunks
                            else:
                                await asyncio.sleep(0.005)  # Minimal delay for other message types
                        except Exception as e:
                            print(f"Error sending chunk: {str(e)}")
                            raise  # Re-raise to stop generation process
                    
                    # Extract session ID if available, otherwise use project_id
                    session_id = message.get("session_id", project_id)
                    
                    # Fetch project conversation history for context if needed
                    project_history = None
                    if message["type"] in ["GenerateCode", "GenerateConversation", "FixCode"]:
                        try:
                            # Get project history automatically for these operations
                            history_result = await get_project_conversations(
                                project_id=project_id,
                                jwt=access_token
                            )
                            project_history = history_result.data if history_result else []
                        except Exception as e:
                            print(f"Failed to fetch project history: {str(e)}")
                            # Continue even if we can't fetch history
                    
                    try:
                        # Create a code generation record in the database
                        if message["type"] in ["GenerateCode", "GenerateConversation", "FixCode"]:
                            if "user_query" in message:
                                try:
                                    # Check if we should update an existing generation (for GenerateCode)
                                    generation_id = None
                                    if message["type"] == "GenerateCode" and message.get("update_existing", False):
                                        try:
                                            # Try to get a pending generation to update
                                            pending_result = await get_pending_generation(
                                                project_id=project_id,
                                                jwt=access_token
                                            )
                                            
                                            if pending_result and pending_result['data']:
                                                # We found a pending generation - use it
                                                generation_id = pending_result['data']['id']
                                                
                                                # Update the prompt
                                                await update_code_generation(
                                                    generation_id=generation_id,
                                                    update_data={
                                                        'prompt': message["user_query"],
                                                        'status': 'pending'  # Reset status if it was changed
                                                    },
                                                    jwt=access_token
                                                )
                                                
                                                # Log that we're updating an existing generation
                                                try:
                                                    await websocket.send_json({
                                                        "type": "Text",
                                                        "value": f"Updating existing generation (ID: {generation_id})"
                                                    })
                                                except Exception:
                                                    print("Failed to send update notification")
                                        except Exception as e:
                                            print(f"Error finding/updating pending generation: {str(e)}")
                                            # Continue with creating a new generation
                                    
                                    # If no existing generation to update, create a new one
                                    if not generation_id:
                                        # Create a code generation record
                                        generation_result = await create_code_generation(
                                            project_id=project_id,
                                            prompt=message["user_query"],
                                            jwt=access_token
                                        )
                                        
                                        if not generation_result or not generation_result.data:
                                            try:
                                                await websocket.send_json({
                                                    "type": "Error",
                                                    "value": "Failed to create code generation record"
                                                })
                                            except Exception:
                                                print("Failed to send generation record creation error")
                                            continue
                                        
                                        # Use the generation ID as part of the generation context
                                        generation_id = generation_result.data["id"]
                                    
                                    # We only track projects now, not individual generations
                                    # since we're using project-based cleanup
                                    
                                    # Update the message with context
                                    message["generation_id"] = generation_id
                                except HTTPException as e:
                                    if e.status_code == 401:
                                        # Token expired during operation
                                        await self.send_token_expired(websocket)
                                        continue
                                    else:
                                        try:
                                            await websocket.send_json({
                                                "type": "Error",
                                                "value": f"Failed to create generation record: {e.detail}"
                                            })
                                        except Exception:
                                            print("Failed to send HTTP exception error")
                                        continue
                                except Exception as e:
                                    try:
                                        await websocket.send_json({
                                            "type": "Error",
                                            "value": f"Failed to create generation record: {str(e)}"
                                        })
                                    except Exception:
                                        print("Failed to send generation record error")
                                    continue
                                    
                        # Handle different message types
                        if message["type"] == "GenerateCode":
                            if "user_query" not in message:
                                try:
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": "Missing 'user_query' field in GenerateCode request"
                                    })
                                except Exception:
                                    print("Failed to send missing user query error")
                                continue
                            
                            # Generate Flutter code
                            result = await self.flutter_generator_service.generate_flutter_code(
                                user_query=message["user_query"],
                                on_chunk=on_chunk,
                                session_id=session_id,
                                db_generation_id=message.get("generation_id"),
                                project_id=project_id,  # Pass project_id to the service
                                access_token=access_token,
                                project_history=project_history  # Pass the loaded project history
                            )
                            
                            # Send final result to the frontend
                            try:
                                if result.get("success", False):
                                    await websocket.send_json({
                                        "type": "Result",
                                        "value": result
                                    })
                                else:
                                    error_message = result.get("error", "Unknown error")
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": f"Code generation failed: {error_message}"
                                    })
                            except Exception:
                                print("Failed to send generation result")
                        
                        elif message["type"] == "GenerateConversation":
                            if "user_query" not in message:
                                try:
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": "Missing 'user_query' field in GenerateConversation request"
                                    })
                                except Exception:
                                    print("Failed to send missing user query error")
                                continue
                            
                            # Generate conversation
                            result = await self.flutter_generator_service.generate_conversation(
                                user_query=message["user_query"],
                                on_chunk=on_chunk,
                                session_id=session_id,
                                db_generation_id=message.get("generation_id"),
                                project_id=project_id,  # Pass project_id to the service
                                access_token=access_token,
                                project_history=project_history  # Pass the loaded project history
                            )
                            
                            # Send final result to the frontend
                            try:
                                if result.get("success", False):
                                    await websocket.send_json({
                                        "type": "Result",
                                        "value": result
                                    })
                                else:
                                    error_message = result.get("error", "Unknown error")
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": f"Conversation generation failed: {error_message}"
                                    })
                            except Exception:
                                print("Failed to send conversation result")
                        
                        elif message["type"] == "FixCode":
                            if "user_query" not in message or "error_message" not in message:
                                try:
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": "Missing 'user_query' or 'error_message' field in FixCode request"
                                    })
                                except Exception:
                                    print("Failed to send missing fields error")
                                continue
                            
                            # Fix Flutter code
                            result = await self.flutter_generator_service.fix_flutter_code(
                                user_query=message["user_query"],
                                error_message=message["error_message"],
                                on_chunk=on_chunk,
                                session_id=session_id,
                                generation_id=message.get("generation_id"),
                                project_id=project_id,
                                access_token=access_token,
                                project_history=project_history  # Pass the loaded project history
                            )
                            
                            # Send final result to the frontend
                            try:
                                if result.get("success", False):
                                    await websocket.send_json({
                                        "type": "Result",
                                        "value": result
                                    })
                                else:
                                    error_message = result.get("error", "Unknown error")
                                    await websocket.send_json({
                                        "type": "Error",
                                        "value": f"Code fixing failed: {error_message}"
                                    })
                            except Exception:
                                print("Failed to send fix result")
                        
                        # Handle other message types if needed
                    
                    except HTTPException as e:
                        if e.status_code == 401:
                            # Token expired during operation
                            await self.send_token_expired(websocket)
                            continue
                        else:
                            try:
                                await websocket.send_json({
                                    "type": "Error",
                                    "value": e.detail
                                })
                            except Exception:
                                print("Failed to send HTTP exception")
                    except Exception as e:
                        try:
                            await websocket.send_json({
                                "type": "Error",
                                "value": f"Error processing request: {str(e)}"
                            })
                        except Exception:
                            print("Failed to send general error")
                
                except WebSocketDisconnect:
                    print(f"WebSocket disconnect detected during message processing for ID: {websocket_id}")
                    # Client disconnected during message processing, clean up resources
                    if websocket_id in self.active_projects:
                        try:
                            project_id = self.active_projects[websocket_id]
                            # print(f"Cleaning up resources for project: {project_id}")
                            # self.flutter_generator_service.cleanup_generation(project_id)
                            # print(f"Cleanup completed for project: {project_id}")
                        except Exception as cleanup_error:
                            print(f"Error during disconnect cleanup: {str(cleanup_error)}")
                        
                        # Remove tracking for this websocket
                        del self.active_projects[websocket_id]
                        print(f"Removed tracking for websocket: {websocket_id}")
                    # Exit the loop and end the handler
                    break
                except json.JSONDecodeError:
                    # Invalid JSON message
                    try:
                        await websocket.send_json({
                            "type": "Error",
                            "value": "Invalid JSON message"
                        })
                    except Exception as e:
                        print(f"Error sending JSON decode error: {str(e)}")
                        break  # Exit the loop if we can't send messages
                except Exception as e:
                    # Unexpected error
                    print(f"Unexpected error processing message: {str(e)}")
                    try:
                        await websocket.send_json({
                            "type": "Error",
                            "value": f"Error processing request: {str(e)}"
                        })
                    except Exception as send_error:
                        print(f"Failed to send error message: {str(send_error)}")
                        break  # Exit the loop if we can't send messages
        
        except WebSocketDisconnect:
            # Client disconnected, clean up resources
            print(f"WebSocket disconnect detected for ID: {websocket_id}")
            if websocket_id in self.active_projects:
                try:
                    project_id = self.active_projects[websocket_id]
                    print(f"Cleaning up resources for project: {project_id}")
                    self.flutter_generator_service.cleanup_generation(project_id)
                    print(f"Cleanup completed for project: {project_id}")
                except Exception as cleanup_error:
                    print(f"Error during disconnect cleanup: {str(cleanup_error)}")
                
                # Remove tracking for this websocket
                del self.active_projects[websocket_id]
                print(f"Removed tracking for websocket: {websocket_id}")
        except Exception as e:
            # Unexpected error
            print(f"Unexpected error in WebSocket handler: {str(e)}")
            try:
                await self.send_error(websocket, f"Unexpected error: {str(e)}")
            except Exception as send_error:
                print(f"Failed to send error message: {str(send_error)}")
            
            # Clean up resources even on error
            if websocket_id in self.active_projects:
                try:
                    project_id = self.active_projects[websocket_id]
                    # print(f"Cleaning up resources for project on error: {project_id}")
                    # self.flutter_generator_service.cleanup_generation(project_id)
                    # print(f"Cleanup completed for project on error: {project_id}")
                except Exception as cleanup_error:
                    print(f"Error during error cleanup: {str(cleanup_error)}")
                
                # Remove tracking for this websocket
                del self.active_projects[websocket_id]
                print(f"Removed tracking for websocket on error: {websocket_id}")
            return 