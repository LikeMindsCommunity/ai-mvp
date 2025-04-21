"""
Implementation of the Flutter code generator service.

Response Types:
- Text: Status updates and progress messages
- Code: Generated code content
- Chat: Conversational explanations and plans
- Error: Error messages
- Success: Success notifications
- AnalysisError: Flutter code analysis errors
- Result: Final result with URL and file path information
"""

import os
import re
import time
import uuid
import subprocess
import threading
from typing import Dict, Optional, Callable, Awaitable, Any, List, Tuple

from api.domain.interfaces.flutter_generator_service import FlutterGeneratorService
from flutter_generator.core.generator import FlutterCodeGenerator
from flutter_generator.core.code_manager import FlutterCodeManager
from flutter_generator.core.integration_manager import FlutterIntegrationManager
from flutter_generator.core.conversation import FlutterConversationManager
from api.infrastructure.code_generations.service import update_code_generation

class FlutterGeneratorServiceImpl(FlutterGeneratorService):
    """Implementation of the Flutter code generator service."""
    
    def __init__(self):
        """Initialize the Flutter generator service."""
        self.code_generator = FlutterCodeGenerator()
        self.root_dir = os.getcwd()
        # Dictionary to store conversation history by session ID
        self.conversation_history = {}
        # Dictionary to store code managers by generation ID
        self.code_managers = {}
        # Dictionary to store integration managers by generation ID
        self.integration_managers = {}
        # Dictionary to store conversation managers by session ID
        self.conversation_managers = {}
    
    def _get_code_manager(self, generation_id: str) -> FlutterCodeManager:
        """
        Get or create a code manager for the given generation ID.
        
        Args:
            generation_id (str): Unique identifier for this generation
            
        Returns:
            FlutterCodeManager: A code manager for this generation
        """
        if generation_id not in self.code_managers:
            self.code_managers[generation_id] = FlutterCodeManager(generation_id=generation_id)
        return self.code_managers[generation_id]
    
    def _get_integration_manager(self, generation_id: str) -> FlutterIntegrationManager:
        """
        Get or create an integration manager for the given generation ID.
        
        Args:
            generation_id (str): Unique identifier for this generation
            
        Returns:
            FlutterIntegrationManager: An integration manager for this generation
        """
        if generation_id not in self.integration_managers:
            code_manager = self._get_code_manager(generation_id)
            self.integration_managers[generation_id] = FlutterIntegrationManager(
                generation_id=generation_id,
                integration_path=code_manager.integration_path
            )
        return self.integration_managers[generation_id]
    
    def _get_conversation_manager(self, session_id: str) -> FlutterConversationManager:
        """
        Get or create a conversation manager for the given session ID.
        
        Args:
            session_id (str): Unique identifier for the user session
            
        Returns:
            FlutterConversationManager: A conversation manager for this session
        """
        if session_id not in self.conversation_managers:
            self.conversation_managers[session_id] = FlutterConversationManager()
        return self.conversation_managers[session_id]
    
    def _update_conversation_history(self, session_id: str, user_query: str) -> str:
        """
        Update conversation history and return the enhanced prompt with history.
        
        Args:
            session_id (str): Unique identifier for the user session
            user_query (str): The current user query
            
        Returns:
            str: Enhanced prompt with conversation history
        """
        # Initialize history for new sessions
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        # Add current query to history
        self.conversation_history[session_id].append(user_query)
        
        # Build enhanced prompt with history context
        if len(self.conversation_history[session_id]) > 1:
            # Format history as conversation context
            history = "\n\n".join(
                [f"Previous request {i+1}: {query}" for i, query in enumerate(self.conversation_history[session_id][:-1])]
            )
            enhanced_prompt = f"Previous requests for context:\n{history}\n\nCurrent request: {user_query}"
            return enhanced_prompt
        
        # If this is the first request, return the original query
        return user_query
    
    async def generate_flutter_code(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Generate Flutter code based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this instead of generating a UUID.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: Response containing the generation result
        """
        try:
            # Use provided database generation ID or generate a new UUID
            generation_id = db_generation_id or str(uuid.uuid4())
            
            # Get managers for this generation
            code_manager = self._get_code_manager(generation_id)
            integration_manager = self._get_integration_manager(generation_id)
            conversation_manager = self._get_conversation_manager(session_id)
            
            # Store the complete AI response
            full_ai_response = ""
            
            # Store the complete code content
            full_code_content = ""
            
            # Modified callback to capture full AI response
            original_on_chunk = on_chunk
            async def capture_response_on_chunk(chunk: Dict[str, Any]) -> None:
                nonlocal full_ai_response
                # Capture Chat and Code chunks for the full AI response
                if chunk.get("type") == "Chat":
                    full_ai_response += chunk.get("value", "")
                
                # Forward to original callback
                await original_on_chunk(chunk)
            
            # First, generate a conversation plan
            conversation_result = await conversation_manager.generate_conversation(user_query, capture_response_on_chunk)
            
            # Update conversation history and get enhanced prompt
            enhanced_prompt = self._update_conversation_history(session_id, user_query)
            
            # Inform starting generation
            await on_chunk({
                "type": "Text",
                "value": "Generating Flutter code based on your request..."
            })
            
            # Generate code with the enhanced prompt
            generated_text = await self.code_generator.generate_code(enhanced_prompt, capture_response_on_chunk)
            if not generated_text:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to generate code. Please try again."
                })
                return {"success": False, "error": "Failed to generate code"}
            
            # Extract and save code
            await on_chunk({
                "type": "Text",
                "value": "Processing generated code..."
            })
            
            dart_codes = code_manager.extract_dart_code(generated_text)
            if not dart_codes:
                await on_chunk({
                    "type": "Error",
                    "value": "No valid Dart code found in the response"
                })
                return {"success": False, "error": "No valid Dart code found"}
            
            # Save the first code block and store the full code content
            full_code_content = dart_codes[0]
            latest_file = code_manager.save_dart_code(full_code_content)
            
            # Copy to integration project
            await on_chunk({
                "type": "Text",
                "value": "Setting up integration environment..."
            })
            
            if not code_manager.copy_to_integration(latest_file):
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to copy code to integration project"
                })
                return {"success": False, "error": "Failed to copy code"}
            
            # Run Flutter pub get
            await on_chunk({
                "type": "Text",
                "value": "Running flutter pub get..."
            })
            
            exit_code, output = integration_manager.run_command_with_timeout(
                'flutter pub get', 
                timeout=300,
                working_dir=code_manager.integration_path
            )
            
            if exit_code != 0:
                await on_chunk({
                    "type": "Error",
                    "value": f"Error running flutter pub get:\n{output}"
                })
                return {"success": False, "error": f"Flutter pub get failed: {output}"}
            
            # Analyze code
            await on_chunk({
                "type": "Text",
                "value": "Analyzing Flutter code..."
            })
            
            success, error_message = code_manager.analyze_flutter_code()
            
            if not success:
                await on_chunk({
                    "type": "AnalysisError",
                    "value": error_message
                })
                
                # Update the generation record with error info and full content
                if db_generation_id and access_token:
                    try:
                        await update_code_generation(
                            db_generation_id,
                            {
                                "status": "error",
                                "code_content": full_code_content,
                                "ai_response": full_ai_response,
                                "analysis_results": error_message,
                                "output_path": latest_file
                            },
                            access_token
                        )
                    except Exception as e:
                        print(f"Failed to update code generation record: {str(e)}")
                
                return {
                    "success": False, 
                    "error": "Flutter code analysis found errors",
                    "analysis_error": error_message,
                    "needs_fix": True,
                    "generation_id": generation_id
                }
            
            # Start Flutter development server
            await on_chunk({
                "type": "Text",
                "value": "Starting Flutter development server..."
            })
            
            # Start the Flutter app with hot reload
            web_url = integration_manager.start_flutter_app()
            
            if not web_url:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to start Flutter development server"
                })
                
                # Update the generation record with error info and full content
                if db_generation_id and access_token:
                    try:
                        await update_code_generation(
                            db_generation_id,
                            {
                                "status": "error",
                                "code_content": full_code_content,
                                "ai_response": full_ai_response,
                                "output_path": latest_file
                            },
                            access_token
                        )
                    except Exception as e:
                        print(f"Failed to update code generation record: {str(e)}")
                
                return {
                    "success": False,
                    "error": "Failed to start Flutter development server",
                    "generation_id": generation_id
                }
            
            # Get the public host for client-facing URLs
            public_host = os.environ.get("PUBLIC_HOST", "0.0.0.0")
            
            # Ensure the returned URL uses the public host
            if "localhost" in web_url:
                # Replace localhost with public host if needed
                web_url = web_url.replace("localhost", public_host)
            
            await on_chunk({
                "type": "Success",
                "value": "Integration completed successfully!"
            })
            
            # Update the generation record with success info and full content
            if db_generation_id and access_token:
                try:
                    await update_code_generation(
                        db_generation_id,
                        {
                            "status": "completed",
                            "code_content": full_code_content,
                            "ai_response": full_ai_response,
                            "output_path": latest_file,
                            "web_url": web_url
                        },
                        access_token
                    )
                except Exception as e:
                    print(f"Failed to update code generation record: {str(e)}")
            
            return {
                "success": True,
                "web_url": web_url,
                "code_path": latest_file,
                "generation_id": generation_id,
                "code": full_code_content
            }
            
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": f"An error occurred: {str(e)}"
            })
            
            # Update the generation record with error info
            if db_generation_id and access_token:
                try:
                    await update_code_generation(
                        db_generation_id,
                        {
                            "status": "error",
                            "ai_response": full_ai_response if 'full_ai_response' in locals() else "",
                            "code_content": full_code_content if 'full_code_content' in locals() else "",
                            "error_message": str(e)
                        },
                        access_token
                    )
                except Exception as update_err:
                    print(f"Failed to update code generation record: {str(update_err)}")
            
            return {"success": False, "error": str(e)}
    
    async def generate_conversation(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Generate conversational explanation and plan for Flutter code implementation.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this to update the record.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: The generated conversation result
        """
        try:
            # Get conversation manager for this session
            conversation_manager = self._get_conversation_manager(session_id)
            
            # Store the complete AI response
            full_ai_response = ""
            
            # Modified callback to capture full AI response
            original_on_chunk = on_chunk
            async def capture_response_on_chunk(chunk: Dict[str, Any]) -> None:
                nonlocal full_ai_response
                # Capture Chat chunks for the full AI response
                if chunk.get("type") == "Chat":
                    full_ai_response += chunk.get("value", "")
                
                # Forward to original callback
                await original_on_chunk(chunk)
            
            # Use the conversation history for context if available
            enhanced_prompt = self._update_conversation_history(session_id, user_query)
            
            # Generate conversation response
            conversation_text = await conversation_manager.generate_conversation(enhanced_prompt, capture_response_on_chunk)
            
            # Update the generation record with the conversation
            if db_generation_id and access_token:
                try:
                    await update_code_generation(
                        db_generation_id,
                        {
                            "status": "completed",
                            "ai_response": full_ai_response,
                            "conversation": [
                                {"role": "user", "content": user_query},
                                {"role": "assistant", "content": full_ai_response}
                            ]
                        },
                        access_token
                    )
                except Exception as e:
                    print(f"Failed to update code generation record: {str(e)}")
            
            return {
                "success": True,
                "conversation": [
                    {"role": "user", "content": user_query},
                    {"role": "assistant", "content": full_ai_response}
                ]
            }
            
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": f"Error generating conversation: {str(e)}"
            })
            
            # Update the generation record with error info
            if db_generation_id and access_token:
                try:
                    await update_code_generation(
                        db_generation_id,
                        {
                            "status": "error",
                            "ai_response": full_ai_response if 'full_ai_response' in locals() else "",
                            "error_message": str(e)
                        },
                        access_token
                    )
                except Exception as update_err:
                    print(f"Failed to update code generation record: {str(update_err)}")
            
            return {"success": False, "error": str(e)}
    
    async def fix_flutter_code(self, user_query: str, error_message: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", generation_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Fix Flutter code based on analysis errors.
        
        Args:
            user_query (str): The user's input query
            error_message (str): The error message from the Flutter analyzer
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            generation_id (str, optional): Unique identifier for the generation to fix. If not provided, a new one will be created.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: Response containing the fixed code result
        """
        try:
            # Use existing generation ID or create a new one
            if not generation_id:
                generation_id = str(uuid.uuid4())
                
            # Get managers for this generation
            code_manager = self._get_code_manager(generation_id)
            integration_manager = self._get_integration_manager(generation_id)
            conversation_manager = self._get_conversation_manager(session_id)
            
            # Store the complete AI response
            full_ai_response = ""
            
            # Store the complete code content
            full_code_content = ""
            
            # Modified callback to capture full AI response
            original_on_chunk = on_chunk
            async def capture_response_on_chunk(chunk: Dict[str, Any]) -> None:
                nonlocal full_ai_response
                # Capture Chat and Code chunks for the full AI response
                if chunk.get("type") == "Chat":
                    full_ai_response += chunk.get("value", "")
                
                # Forward to original callback
                await original_on_chunk(chunk)
                
            # Update conversation history with error context
            error_prompt = f"{user_query}\n\nI'm getting these Flutter errors:\n{error_message}\n\nPlease fix them."
            enhanced_prompt = self._update_conversation_history(session_id, error_prompt)
            
            # Inform the user about the fix attempt
            await on_chunk({
                "type": "Text",
                "value": "Analyzing errors and generating fixes..."
            })
            
            # Generate fixed code with the enhanced prompt
            generated_text = await self.code_generator.generate_code(enhanced_prompt, capture_response_on_chunk)
            if not generated_text:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to generate fixed code. Please try again."
                })
                return {"success": False, "error": "Failed to generate fixed code"}
            
            # Extract and save the fixed code
            await on_chunk({
                "type": "Text",
                "value": "Processing fixed code..."
            })
            
            dart_codes = code_manager.extract_dart_code(generated_text)
            if not dart_codes:
                await on_chunk({
                    "type": "Error",
                    "value": "No valid Dart code found in the response"
                })
                return {"success": False, "error": "No valid Dart code found"}
            
            # Save the fixed code
            full_code_content = dart_codes[0]
            latest_file = code_manager.save_dart_code(full_code_content, index=1)  # Use index 1 to avoid overwriting
            
            # Copy to integration project
            await on_chunk({
                "type": "Text",
                "value": "Updating integration with fixed code..."
            })
            
            if not code_manager.copy_to_integration(latest_file):
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to copy fixed code to integration project"
                })
                return {"success": False, "error": "Failed to copy fixed code"}
            
            # Analyze the fixed code
            await on_chunk({
                "type": "Text",
                "value": "Analyzing fixed Flutter code..."
            })
            
            success, error_message = code_manager.analyze_flutter_code()
            
            if not success:
                await on_chunk({
                    "type": "AnalysisError",
                    "value": error_message
                })
                
                # Update the generation record with error info and full content
                if generation_id and access_token:
                    try:
                        await update_code_generation(
                            generation_id,
                            {
                                "status": "error",
                                "code_content": full_code_content,
                                "ai_response": full_ai_response,
                                "analysis_results": error_message,
                                "output_path": latest_file
                            },
                            access_token
                        )
                    except Exception as e:
                        print(f"Failed to update code generation record: {str(e)}")
                
                return {
                    "success": False,
                    "error": "Flutter code analysis still found errors",
                    "analysis_error": error_message,
                    "needs_fix": True,
                    "generation_id": generation_id
                }
            
            # Hot restart the Flutter app if it's running
            await on_chunk({
                "type": "Text",
                "value": "Applying code changes..."
            })
            
            if integration_manager.is_running:
                if integration_manager.hot_restart():
                    await on_chunk({
                        "type": "Success",
                        "value": "Hot restarted Flutter app with fixed code"
                    })
                    
                    # Update the generation record with success info and full content
                    if generation_id and access_token:
                        try:
                            await update_code_generation(
                                generation_id,
                                {
                                    "status": "completed",
                                    "code_content": full_code_content,
                                    "ai_response": full_ai_response,
                                    "output_path": latest_file
                                },
                                access_token
                            )
                        except Exception as e:
                            print(f"Failed to update code generation record: {str(e)}")
                    
                    return {
                        "success": True,
                        "code_path": latest_file,
                        "generation_id": generation_id,
                        "code": full_code_content
                    }
                else:
                    await on_chunk({
                        "type": "Text",
                        "value": "Hot restart failed, attempting to restart the server..."
                    })
                    
                    # Stop the current app
                    integration_manager.stop_flutter_app()
                    
                    # Start a new Flutter app
                    web_url = integration_manager.start_flutter_app()
                    
                    if not web_url:
                        await on_chunk({
                            "type": "Error",
                            "value": "Failed to restart Flutter development server"
                        })
                        
                        # Update the generation record with error info and full content
                        if generation_id and access_token:
                            try:
                                await update_code_generation(
                                    generation_id,
                                    {
                                        "status": "error",
                                        "code_content": full_code_content,
                                        "ai_response": full_ai_response,
                                        "output_path": latest_file,
                                        "error_message": "Failed to restart Flutter development server"
                                    },
                                    access_token
                                )
                            except Exception as e:
                                print(f"Failed to update code generation record: {str(e)}")
                        
                        return {
                            "success": False,
                            "error": "Failed to restart Flutter development server",
                            "generation_id": generation_id
                        }
                    
                    # Get the public host for client-facing URLs
                    public_host = os.environ.get("PUBLIC_HOST", "0.0.0.0")
                    
                    # Ensure the returned URL uses the public host
                    if "localhost" in web_url:
                        # Replace localhost with public host if needed
                        web_url = web_url.replace("localhost", public_host)
                    
                    await on_chunk({
                        "type": "Success",
                        "value": "Flutter server restarted with fixed code"
                    })
                    
                    # Update the generation record with success info and full content
                    if generation_id and access_token:
                        try:
                            await update_code_generation(
                                generation_id,
                                {
                                    "status": "completed",
                                    "code_content": full_code_content,
                                    "ai_response": full_ai_response,
                                    "output_path": latest_file,
                                    "web_url": web_url
                                },
                                access_token
                            )
                        except Exception as e:
                            print(f"Failed to update code generation record: {str(e)}")
                    
                    return {
                        "success": True,
                        "web_url": web_url,
                        "code_path": latest_file,
                        "generation_id": generation_id,
                        "code": full_code_content
                    }
            else:
                # Start a new Flutter app
                await on_chunk({
                    "type": "Text",
                    "value": "Starting Flutter development server..."
                })
                
                web_url = integration_manager.start_flutter_app()
                
                if not web_url:
                    await on_chunk({
                        "type": "Error",
                        "value": "Failed to start Flutter development server"
                    })
                    
                    # Update the generation record with error info and full content
                    if generation_id and access_token:
                        try:
                            await update_code_generation(
                                generation_id,
                                {
                                    "status": "error",
                                    "code_content": full_code_content,
                                    "ai_response": full_ai_response,
                                    "output_path": latest_file,
                                    "error_message": "Failed to start Flutter development server"
                                },
                                access_token
                            )
                        except Exception as e:
                            print(f"Failed to update code generation record: {str(e)}")
                    
                    return {
                        "success": False,
                        "error": "Failed to start Flutter development server",
                        "generation_id": generation_id
                    }
                
                # Get the public host for client-facing URLs
                public_host = os.environ.get("PUBLIC_HOST", "0.0.0.0")
                
                # Ensure the returned URL uses the public host
                if "localhost" in web_url:
                    # Replace localhost with public host if needed
                    web_url = web_url.replace("localhost", public_host)
                
                await on_chunk({
                    "type": "Success",
                    "value": "Code fixes applied successfully!"
                })
                
                # Update the generation record with success info and full content
                if generation_id and access_token:
                    try:
                        await update_code_generation(
                            generation_id,
                            {
                                "status": "completed",
                                "code_content": full_code_content,
                                "ai_response": full_ai_response,
                                "output_path": latest_file,
                                "web_url": web_url if 'web_url' in locals() else None
                            },
                            access_token
                        )
                    except Exception as e:
                        print(f"Failed to update code generation record: {str(e)}")
                
                return {
                    "success": True,
                    "web_url": web_url if 'web_url' in locals() else None,
                    "code_path": latest_file,
                    "generation_id": generation_id,
                    "code": full_code_content
                }
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": f"An error occurred while fixing code: {str(e)}"
            })
            
            # Update the generation record with error info
            if generation_id and access_token:
                try:
                    await update_code_generation(
                        generation_id,
                        {
                            "status": "error",
                            "ai_response": full_ai_response if 'full_ai_response' in locals() else "",
                            "code_content": full_code_content if 'full_code_content' in locals() else "",
                            "error_message": str(e)
                        },
                        access_token
                    )
                except Exception as update_err:
                    print(f"Failed to update code generation record: {str(update_err)}")
            
            return {"success": False, "error": str(e)}
            
    def cleanup_generation(self, generation_id: str) -> bool:
        """
        Clean up resources for a specific generation.
        
        Args:
            generation_id (str): Unique identifier for the generation to clean up
            
        Returns:
            bool: True if cleanup was successful, False otherwise
        """
        try:
            # Stop the Flutter app if it's running
            if generation_id in self.integration_managers:
                self.integration_managers[generation_id].stop_flutter_app()
        
            # Clean up code manager resources
            if generation_id in self.code_managers:
                self.code_managers[generation_id].cleanup()
                
            # Remove managers from dictionaries
            if generation_id in self.integration_managers:
                del self.integration_managers[generation_id]
                
            if generation_id in self.code_managers:
                del self.code_managers[generation_id]
                
            return True
        except Exception as e:
            print(f"Error cleaning up generation {generation_id}: {str(e)}")
            return False 