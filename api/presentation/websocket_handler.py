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
import logging
from typing import Dict, Any, Optional, Callable, Awaitable
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
import asyncio

from api.infrastructure.services.flutter_generator_service_impl import FlutterGeneratorServiceImpl
from api.infrastructure.database import SupabaseManager
from api.infrastructure.auth import get_current_user
from api.infrastructure.auth.service import refresh_token
from api.infrastructure.projects.service import get_project
from api.infrastructure.code_generations.service import create_code_generation, update_code_generation, get_project_conversations, get_pending_generation, get_generation_by_id
from api.presentation.exceptions import APIException

# Configure logging
logger = logging.getLogger(__name__)

# Message types
MSG_REFRESH_TOKEN = "RefreshToken"
MSG_CLEANUP_PROJECT = "CleanupProject"
MSG_GET_PROJECT_CONVERSATIONS = "GetProjectConversations"
MSG_GENERATE_CODE = "GenerateCode"
MSG_GENERATE_CONVERSATION = "GenerateConversation"
MSG_FIX_CODE = "FixCode"

# Response types
RESP_ERROR = "Error"
RESP_TEXT = "Text"
RESP_TOKEN_EXPIRED = "TokenExpired"
RESP_TOKEN_REFRESHED = "TokenRefreshed"
RESP_SUCCESS = "Success"
RESP_RESULT = "Result"
RESP_CONVERSATION_HISTORY = "ConversationHistory"

class WebSocketHandler:
    """Handler for WebSocket connections."""
    
    def __init__(self):
        """Initialize the WebSocket handler."""
        self.flutter_generator_service = FlutterGeneratorServiceImpl()
        self.supabase_manager = SupabaseManager()  # Eventually this can be removed once all methods are migrated to services
        # Track active project IDs for cleanup on disconnect
        self.active_projects = {}
        # Define message handlers map
        self._message_handlers = {
            MSG_REFRESH_TOKEN: self._handle_token_refresh,
            MSG_CLEANUP_PROJECT: self._handle_cleanup_project,
            MSG_GET_PROJECT_CONVERSATIONS: self._handle_get_project_conversations,
            MSG_GENERATE_CODE: self._handle_generate_code,
            MSG_GENERATE_CONVERSATION: self._handle_generate_conversation,
            MSG_FIX_CODE: self._handle_fix_code
        }
    
    async def send_json_response(self, websocket: WebSocket, response_type: str, value: Any) -> bool:
        """
        Send a JSON response to the client.
        
        Args:
            websocket: The WebSocket connection
            response_type: The type of response
            value: The response value
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        try:
            await websocket.send_json({
                "type": response_type,
                "value": value
            })
            return True
        except Exception as e:
            logger.error(f"Error sending {response_type} message: {str(e)}")
            return False
    
    async def send_error(self, websocket: WebSocket, message: str) -> None:
        """Send an error message and close the connection."""
        try:
            await self.send_json_response(websocket, RESP_ERROR, message)
            await websocket.close()
        except Exception as e:
            logger.error(f"Error sending error message: {str(e)}")
    
    async def send_token_expired(self, websocket: WebSocket) -> None:
        """Send a token expired message without closing the connection."""
        await self.send_json_response(
            websocket, 
            RESP_TOKEN_EXPIRED, 
            "Authentication token has expired. Please refresh the token."
        )
    
    async def create_chunk_callback(self, websocket: WebSocket) -> Callable[[Dict[str, Any]], Awaitable[None]]:
        """
        Create a callback function for streaming responses.
        
        Args:
            websocket: The WebSocket connection
            
        Returns:
            A callback function that sends chunks to the client
        """
        async def on_chunk(response: Dict[str, Any]):
            try:
                await websocket.send_json(response)
                # Add a tiny delay to ensure chunks are processed individually
                # Small enough not to be noticeable but helps prevent buffering
                if response.get("type") == RESP_TEXT:
                    await asyncio.sleep(0.02)  # Slightly longer delay for text chunks
                elif response.get("type") == "Chat":
                    await asyncio.sleep(0.02)  # Similar delay for chat chunks
                else:
                    await asyncio.sleep(0.005)  # Minimal delay for other message types
            except Exception as e:
                logger.error(f"Error sending chunk: {str(e)}")
                raise  # Re-raise to stop generation process
        
        return on_chunk
    
    async def _handle_token_refresh(self, websocket: WebSocket, message: Dict[str, Any], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle token refresh message."""
        if "refresh_token" not in message:
            await self.send_json_response(
                websocket, 
                RESP_ERROR, 
                "Missing 'refresh_token' field in request"
            )
            return context
        
        try:
            # Refresh the token
            refresh_result = await refresh_token(message["refresh_token"])
            access_token = refresh_result["access_token"]
            
            # Update the user in context
            user = await get_current_user(access_token)
            context["access_token"] = access_token
            context["user"] = user
            
            # Notify client of successful refresh
            if not await self.send_json_response(
                websocket,
                RESP_TOKEN_REFRESHED,
                {
                    "access_token": access_token,
                    "refresh_token": refresh_result["refresh_token"]
                }
            ):
                return context
            
            # Re-verify project access with new token
            project = await get_project(context["project_id"], access_token)
            if not project or not project.data:
                await self.send_error(websocket, "Project not found or you don't have access")
            
            return context
        except Exception as e:
            await self.send_error(websocket, f"Token refresh failed: {str(e)}")
            raise
    
    async def _handle_cleanup_project(self, websocket: WebSocket, message: Dict[str, Any], 
                                     context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle project cleanup message."""
        try:
            # Clean up resources for this project
            project_id = context["project_id"]
            success = self.flutter_generator_service.cleanup_generation(project_id)
            
            # Notify client of result
            response_type = RESP_SUCCESS if success else RESP_ERROR
            await self.send_json_response(
                websocket,
                response_type,
                f"Project {project_id} cleanup {'completed' if success else 'failed'}"
            )
            
            return context
        except Exception as e:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                f"Cleanup failed: {str(e)}"
            )
            return context
    
    async def _handle_get_project_conversations(self, websocket: WebSocket, message: Dict[str, Any], 
                                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get project conversations message."""
        try:
            # Fetch all conversations for this project
            conversations = await get_project_conversations(
                project_id=context["project_id"],
                jwt=context["access_token"]
            )
            
            # Send conversation history to the client
            await self.send_json_response(
                websocket,
                RESP_CONVERSATION_HISTORY,
                conversations.data if conversations else []
            )
            
            return context
        except Exception as e:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                f"Failed to fetch project conversations: {str(e)}"
            )
            return context
    
    async def _prepare_generation_record(self, websocket: WebSocket, message: Dict[str, Any], 
                                        context: Dict[str, Any]) -> Optional[str]:
        """Prepare a generation record for code/conversation generation."""
        if "user_query" not in message:
            return None
        
        try:
            # Check if we should update an existing generation (for GenerateCode)
            generation_id = None
            if message["type"] == MSG_GENERATE_CODE and message.get("update_existing", False):
                try:
                    # Try to get a pending generation to update
                    pending_result = await get_pending_generation(
                        project_id=context["project_id"],
                        jwt=context["access_token"]
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
                            jwt=context["access_token"]
                        )
                        
                        # Log that we're updating an existing generation
                        await self.send_json_response(
                            websocket,
                            RESP_TEXT,
                            f"Updating existing generation (ID: {generation_id})"
                        )
                except Exception as e:
                    logger.error(f"Error finding/updating pending generation: {str(e)}")
                    # Continue with creating a new generation
            
            # If no existing generation to update, create a new one
            if not generation_id:
                # Create a code generation record
                generation_result = await create_code_generation(
                    project_id=context["project_id"],
                    prompt=message["user_query"],
                    jwt=context["access_token"]
                )
                
                if not generation_result or not generation_result.data:
                    await self.send_json_response(
                        websocket,
                        RESP_ERROR,
                        "Failed to create code generation record"
                    )
                    return None
                
                # Use the generation ID as part of the generation context
                generation_id = generation_result.data["id"]
            
            return generation_id
        except HTTPException as e:
            if e.status_code == 401:
                # Token expired during operation
                await self.send_token_expired(websocket)
            else:
                await self.send_json_response(
                    websocket,
                    RESP_ERROR,
                    f"Failed to create generation record: {e.detail}"
                )
            return None
        except Exception as e:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                f"Failed to create generation record: {str(e)}"
            )
            return None
    
    async def _handle_generate_code(self, websocket: WebSocket, message: Dict[str, Any], 
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate code message."""
        if "user_query" not in message:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                "Missing 'user_query' field in GenerateCode request"
            )
            return context
        
        # Prepare generation record
        generation_id = await self._prepare_generation_record(websocket, message, context)
        if not generation_id:
            return context
        
        # Generate Flutter code
        on_chunk = await self.create_chunk_callback(websocket)
        try:
            result = await self.flutter_generator_service.generate_flutter_code(
                user_query=message["user_query"],
                on_chunk=on_chunk,
                session_id=message.get("session_id", context["project_id"]),
                db_generation_id=generation_id,
                project_id=context["project_id"],
                access_token=context["access_token"],
                project_history=context.get("project_history")
            )
            
            # Send final result to the frontend
            if result.get("success", False):
                await self.send_json_response(
                    websocket,
                    RESP_RESULT,
                    result
                )
            else:
                error_message = result.get("error", "Unknown error")
                await self.send_json_response(
                    websocket,
                    RESP_ERROR,
                    f"Code generation failed: {error_message}"
                )
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
        
        return context
    
    async def _handle_generate_conversation(self, websocket: WebSocket, message: Dict[str, Any], 
                                           context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate conversation message."""
        if "user_query" not in message:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                "Missing 'user_query' field in GenerateConversation request"
            )
            return context
        
        # Prepare generation record
        generation_id = await self._prepare_generation_record(websocket, message, context)
        if not generation_id:
            return context
        
        # Generate conversation
        on_chunk = await self.create_chunk_callback(websocket)
        try:
            result = await self.flutter_generator_service.generate_conversation(
                user_query=message["user_query"],
                on_chunk=on_chunk,
                session_id=message.get("session_id", context["project_id"]),
                db_generation_id=generation_id,
                project_id=context["project_id"],
                access_token=context["access_token"],
                project_history=context.get("project_history")
            )
            
            # Send final result to the frontend
            if result.get("success", False):
                await self.send_json_response(
                    websocket,
                    RESP_RESULT,
                    result
                )
            else:
                error_message = result.get("error", "Unknown error")
                await self.send_json_response(
                    websocket,
                    RESP_ERROR,
                    f"Conversation generation failed: {error_message}"
                )
        except Exception as e:
            logger.error(f"Error generating conversation: {str(e)}")
        
        return context
    
    async def _handle_fix_code(self, websocket: WebSocket, message: Dict[str, Any], 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle fix code message."""
        if "user_query" not in message or "error_message" not in message:
            await self.send_json_response(
                websocket,
                RESP_ERROR,
                "Missing 'user_query' or 'error_message' field in FixCode request"
            )
            return context
        
        # Prepare generation record
        generation_id = await self._prepare_generation_record(websocket, message, context)
        if not generation_id:
            return context
        
        # Fix Flutter code
        on_chunk = await self.create_chunk_callback(websocket)
        try:
            result = await self.flutter_generator_service.fix_flutter_code(
                user_query=message["user_query"],
                error_message=message["error_message"],
                on_chunk=on_chunk,
                session_id=message.get("session_id", context["project_id"]),
                generation_id=generation_id,
                project_id=context["project_id"],
                access_token=context["access_token"],
                project_history=context.get("project_history")
            )
            
            # Send final result to the frontend
            if result.get("success", False):
                await self.send_json_response(
                    websocket,
                    RESP_RESULT,
                    result
                )
            else:
                error_message = result.get("error", "Unknown error")
                await self.send_json_response(
                    websocket,
                    RESP_ERROR,
                    f"Code fixing failed: {error_message}"
                )
        except Exception as e:
            logger.error(f"Error fixing code: {str(e)}")
        
        return context
    
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
            # Initialize context dictionary to track state
            context = {
                "project_id": project_id,
                "access_token": token,
                "user": None,
                "project": None,
                "project_history": None
            }
            
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
                
                # Extract the access token and update context
                access_token = user.get('access_token')
                if not access_token:
                    await self.send_error(websocket, "Invalid or missing access token")
                    return
                
                context["access_token"] = access_token
                context["user"] = user
                
                # Verify project access
                project = await get_project(project_id, access_token)
                if not project or not project.data:
                    await self.send_error(websocket, "Project not found or you don't have access")
                    return

                context["project"] = project.data
                
                # Create project output directory if it doesn't exist
                project_output_dir = os.path.join("output", project_id)
                os.makedirs(project_output_dir, exist_ok=True)
                
                # Send connection confirmation
                if not await self.send_json_response(
                    websocket,
                    RESP_TEXT,
                    {
                        "message": "Connected successfully",
                        "project": {
                            "id": project_id,
                            "name": project.data.get("name")
                        }
                    }
                ):
                    return
                
                # Fetch conversation history after confirming connection
                try:
                    conversation_history = await get_project_conversations(
                        project_id=project_id,
                        jwt=access_token
                    )
                    
                    context["project_history"] = conversation_history.data if conversation_history else []
                    
                    # Send conversation history
                    if context["project_history"]:
                        await self.send_json_response(
                            websocket,
                            RESP_CONVERSATION_HISTORY,
                            context["project_history"]
                        )
                except Exception as e:
                    logger.error(f"Failed to fetch initial project history: {str(e)}")
                    # Continue even if we can't fetch history
                
            except HTTPException as e:
                if e.status_code == 401:
                    # Token likely expired, notify client
                    await self.send_token_expired(websocket)
                else:
                    await self.send_error(websocket, e.detail)
                return
            except WebSocketDisconnect:
                # Client disconnected during initialization, clean up
                self._handle_disconnect(websocket_id)
                return
            except Exception as e:
                # Unexpected error during initialization
                await self.send_error(websocket, f"Authentication error: {str(e)}")
                return
            
            # Process incoming messages
            while True:
                try:
                    # Receive message from client
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Validate message structure
                    if "type" not in message:
                        await self.send_json_response(
                            websocket,
                            RESP_ERROR,
                            "Missing 'type' field in request"
                        )
                        continue
                    
                    # Get the appropriate handler for this message type
                    message_type = message["type"]
                    handler = self._message_handlers.get(message_type)
                    
                    if handler:
                        try:
                            # Load project history if needed and not already loaded
                            if message_type in [MSG_GENERATE_CODE, MSG_GENERATE_CONVERSATION, MSG_FIX_CODE] and not context.get("project_history"):
                                try:
                                    history_result = await get_project_conversations(
                                        project_id=project_id,
                                        jwt=context["access_token"]
                                    )
                                    context["project_history"] = history_result.data if history_result else []
                                except Exception as e:
                                    logger.error(f"Failed to fetch project history: {str(e)}")
                                    # Continue even if we can't fetch history
                            
                            # Call the handler
                            context = await handler(websocket, message, context)
                        except HTTPException as e:
                            if e.status_code == 401:
                                # Token expired during operation
                                await self.send_token_expired(websocket)
                            else:
                                await self.send_json_response(
                                    websocket,
                                    RESP_ERROR,
                                    e.detail
                                )
                        except Exception as e:
                            await self.send_json_response(
                                websocket,
                                RESP_ERROR,
                                f"Error processing request: {str(e)}"
                            )
                    else:
                        # Unknown message type
                        await self.send_json_response(
                            websocket,
                            RESP_ERROR,
                            f"Unknown message type: {message_type}"
                        )
                
                except WebSocketDisconnect:
                    logger.info(f"WebSocket disconnect detected during message processing for ID: {websocket_id}")
                    self._handle_disconnect(websocket_id)
                    break
                except json.JSONDecodeError:
                    # Invalid JSON message
                    await self.send_json_response(
                        websocket,
                        RESP_ERROR,
                        "Invalid JSON message"
                    )
                except Exception as e:
                    # Unexpected error
                    logger.error(f"Unexpected error processing message: {str(e)}")
                    await self.send_json_response(
                        websocket,
                        RESP_ERROR,
                        f"Error processing request: {str(e)}"
                    )
        
        except WebSocketDisconnect:
            # Client disconnected
            logger.info(f"WebSocket disconnect detected for ID: {websocket_id}")
            self._handle_disconnect(websocket_id)
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error in WebSocket handler: {str(e)}")
            await self.send_error(websocket, f"Unexpected error: {str(e)}")
            self._handle_disconnect(websocket_id)
    
    def _handle_disconnect(self, websocket_id: str) -> None:
        """Handle websocket disconnect and cleanup."""
        if websocket_id in self.active_projects:
            try:
                project_id = self.active_projects[websocket_id]
                logger.info(f"Cleaning up resources for project: {project_id}")
                self.flutter_generator_service.cleanup_generation(project_id)
                logger.info(f"Cleanup completed for project: {project_id}")
            except Exception as cleanup_error:
                logger.error(f"Error during disconnect cleanup: {str(cleanup_error)}")
            
            # Remove tracking for this websocket
            del self.active_projects[websocket_id]
            logger.info(f"Removed tracking for websocket: {websocket_id}") 