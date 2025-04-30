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
from flutter_generator.core.existing_project_conversation import ExistingProjectConversationManager
from flutter_generator.utils.ingest import get_ingest_text
from flutter_generator.config import Settings
from api.infrastructure.code_generations.service import update_code_generation

class FlutterGeneratorServiceImpl(FlutterGeneratorService):
    """Implementation of the Flutter code generator service."""
    
    def __init__(self):
        """Initialize the Flutter generator service."""
        self.settings = Settings()
        self.code_generator = FlutterCodeGenerator()
        self.root_dir = os.getcwd()
        # Dictionary to store conversation history by session ID
        self.conversation_history = {}
        # Dictionary to store code managers by project ID
        self.code_managers = {}
        # Dictionary to store integration managers by project ID
        self.integration_managers = {}
        # Dictionary to store conversation managers by session ID
        self.conversation_managers = {}
        
        # Initialize both conversation managers (regular and for GitHub projects)
        self.standard_conversation_manager = FlutterConversationManager()
        self.github_conversation_manager = ExistingProjectConversationManager(self.settings)
    
    def _get_code_manager(self, project_id: str, generation_id: str = None) -> FlutterCodeManager:
        """
        Get or create a code manager for the given project ID.
        
        Args:
            project_id (str): Project identifier
            generation_id (str, optional): Unique identifier for this generation
            
        Returns:
            FlutterCodeManager: A code manager for this project
        """
        if project_id not in self.code_managers:
            self.code_managers[project_id] = FlutterCodeManager(
                project_id=project_id,
                generation_id=generation_id
            )
        else:
            # Update generation ID if provided
            if generation_id:
                self.code_managers[project_id].generation_id = generation_id
                
        return self.code_managers[project_id]
    
    def _get_integration_manager(self, project_id: str, generation_id: str = None) -> FlutterIntegrationManager:
        """
        Get or create an integration manager for the given project ID.
        
        Args:
            project_id (str): Project identifier
            generation_id (str, optional): Unique identifier for this generation
            
        Returns:
            FlutterIntegrationManager: An integration manager for this project
        """
        if project_id not in self.integration_managers:
            code_manager = self._get_code_manager(project_id, generation_id)
            self.integration_managers[project_id] = FlutterIntegrationManager(
                project_id=project_id,
                generation_id=generation_id,
                integration_path=code_manager.integration_path
            )
        else:
            # Update generation ID if provided
            if generation_id:
                self.integration_managers[project_id].generation_id = generation_id
                
        return self.integration_managers[project_id]
    
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
    
    def _update_conversation_history(self, session_id: str, user_query: str, project_history: list = None, code_manager = None) -> str:
        """
        Update conversation history and return the enhanced prompt with history.
        
        Args:
            session_id (str): Unique identifier for the user session
            user_query (str): The current user query
            project_history (list, optional): List of previous conversations from the database
            code_manager (FlutterCodeManager, optional): Code manager that might contain project analysis
            
        Returns:
            str: Enhanced prompt with conversation history and project analysis if available
        """
        # Initialize history for new sessions
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
            
            # If we have project history from database, initialize with it
            if project_history:
                # Extract previous prompts from project history
                for item in project_history:
                    if item.get('prompt'):
                        self.conversation_history[session_id].append(item.get('prompt'))
        
        # Add current query to history
        self.conversation_history[session_id].append(user_query)
        
        # Build enhanced prompt with history context
        history_text = ""
        if len(self.conversation_history[session_id]) > 1:
            # Format history as conversation context
            history = "\n\n".join(
                [f"Previous request {i+1}: {query}" for i, query in enumerate(self.conversation_history[session_id][:-1])]
            )
            history_text = f"Previous requests for context:\n{history}\n\n"
        
        # Include project analysis if available
        project_analysis_text = ""
        if code_manager and code_manager.is_existing_project and code_manager.existing_project_analysis:
            project_analysis_text = f"""
            Project analysis for existing Flutter project:
            {code_manager.existing_project_analysis}
            
            Based on this project structure, please adapt your integration to work with the existing code rather than creating a new project from scratch.
            Respect the existing architecture, patterns, and naming conventions.
            
            """
        
        # Combine all elements
        enhanced_prompt = f"{history_text}{project_analysis_text}Current request: {user_query}"
        return enhanced_prompt
    
    async def load_project_history(self, project_history: list, session_id: str = "default") -> None:
        """
        Load project conversation history into the session conversation history.
        
        Args:
            project_history (list): List of previous conversations from the database
            session_id (str, optional): Session ID to load history into. Defaults to "default".
        """
        # Initialize history for this session if it doesn't exist
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
            
        # Clear existing history and load from project history
        self.conversation_history[session_id] = []
        
        # Extract previous prompts from project history
        for item in project_history:
            if item.get('prompt'):
                self.conversation_history[session_id].append(item.get('prompt'))
                
    async def generate_flutter_code(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, project_id: str = None, access_token: str = None, project_history: list = None) -> Dict[str, Any]:
        """
        Generate Flutter code based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this instead of generating a UUID.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            project_history (list, optional): List of previous conversations from the database.
            
        Returns:
            Dict[str, Any]: Response containing the generation result
        """
        try:
            # Load project history if provided
            if project_history:
                await self.load_project_history(project_history, session_id)
                
            # Use provided database generation ID or generate a new UUID
            generation_id = db_generation_id or str(uuid.uuid4())
            
            # Require project_id for organization
            if not project_id:
                await on_chunk({
                    "type": "Error",
                    "value": "Project ID is required for code generation"
                })
                return {"success": False, "error": "Project ID is required"}
            
            # Check if this is a GitHub project (if we have access_token)
            is_github_project = False
            ingest_text = None
            if access_token:
                is_github_project = await self._is_imported_project(project_id, access_token)
                
                # If it's a GitHub project, try to get the ingested text
                if is_github_project:
                    ingest_text = get_ingest_text(project_id)
                    if not ingest_text:
                        # Inform user, but continue without blocking
                        await on_chunk({
                            "type": "Text",
                            "value": "Note: Repository ingestion data not found. Generation may be less context-aware."
                        })
            
            # Get managers for this generation
            code_manager = self._get_code_manager(project_id, generation_id)
            integration_manager = self._get_integration_manager(project_id, generation_id)
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
            if is_github_project:
                # Use GitHub conversation manager for imported projects
                conversation_result = await self.github_conversation_manager.generate_conversation(
                    user_query, 
                    project_id,
                    capture_response_on_chunk
                )
                
                # Set existing project mode flag for use in code generation
                code_manager.set_existing_project_mode(True)
                
                # If we have ingest text, store it in the code manager for reference
                if ingest_text:
                    code_manager.set_existing_project_code(ingest_text)
                
                # Store the conversation analysis for reference in code generation
                code_manager.set_existing_project_analysis(conversation_result)
            else:
                # Use standard conversation manager for regular projects
                conversation_result = await conversation_manager.generate_conversation(
                    user_query, 
                    capture_response_on_chunk
                )
                
                # Reset any existing project settings
                code_manager.set_existing_project_mode(False)
            
            # Update conversation history and get enhanced prompt
            enhanced_prompt = self._update_conversation_history(session_id, user_query, project_history, code_manager)
            
            # Inform starting generation
            await on_chunk({
                "type": "Text",
                "value": "Generating Flutter code..."
            })
            
            # Generate code with the enhanced prompt
            if is_github_project and ingest_text:
                # Use project-aware code generation for GitHub projects
                generated_text = await self.code_generator.generate_code(
                    enhanced_prompt, 
                    capture_response_on_chunk,
                    is_imported_project=True,
                    ingest_text=ingest_text
                )
            else:
                # Use standard code generation for regular projects
                generated_text = await self.code_generator.generate_code(
                    enhanced_prompt, 
                    capture_response_on_chunk
                )
                
            if not generated_text:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to generate code. Please try again."
                })
                return {"success": False, "error": "Failed to generate code"}
            
            # Extract and save code
            await on_chunk({
                "type": "Text",
                "value": "Processing code..."
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
                "value": "Preparing Flutter environment..."
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
                "value": "Starting Flutter application..."
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
                "value": "Flutter application is ready!"
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
    
    async def generate_conversation(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, project_id: str = None, access_token: str = None, project_history: list = None) -> Dict[str, Any]:
        """
        Generate conversational explanation and plan for Flutter code implementation.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this to update the record.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            project_history (list, optional): List of previous conversations from the database.
            
        Returns:
            Dict[str, Any]: The generated conversation result
        """
        try:
            # Load project history if provided
            if project_history:
                await self.load_project_history(project_history, session_id)
            
            # Check if this is a GitHub project (if we have a project_id and access_token)
            is_github_project = False
            if project_id and access_token:
                is_github_project = await self._is_imported_project(project_id, access_token)
            
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
            enhanced_prompt = self._update_conversation_history(session_id, user_query, project_history)
            
            # Generate conversation response using the appropriate manager
            if is_github_project:
                # Inform the user we're analyzing a GitHub project
                await on_chunk({
                    "type": "Text",
                    "value": "Analyzing GitHub project structure..."
                })
                
                # Use the GitHub conversation manager with project context
                conversation_text = await self.github_conversation_manager.generate_conversation(
                    enhanced_prompt, 
                    project_id,
                    capture_response_on_chunk
                )
            else:
                # Use the standard conversation manager for regular projects
                conversation_manager = self._get_conversation_manager(session_id)
                conversation_text = await conversation_manager.generate_conversation(
                    enhanced_prompt, 
                    capture_response_on_chunk
                )
            
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
                ],
                "is_github_project": is_github_project
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
    
    async def fix_flutter_code(self, user_query: str, error_message: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", generation_id: str = None, project_id: str = None, access_token: str = None, project_history: list = None) -> Dict[str, Any]:
        """
        Fix Flutter code based on analysis errors.
        
        Args:
            user_query (str): The user's input query
            error_message (str): The error message from the Flutter analyzer
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            generation_id (str, optional): Generation ID to fix. If not provided, uses the latest generation.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            project_history (list, optional): List of previous conversations from the database.
            
        Returns:
            Dict[str, Any]: Response containing the fixed code result
        """
        try:
            # Load project history if provided
            if project_history:
                await self.load_project_history(project_history, session_id)
                
            # Use existing generation ID or create a new one
            if not generation_id:
                generation_id = str(uuid.uuid4())
            
            # Check if this is a GitHub project (if we have project_id and access_token)
            is_github_project = False
            ingest_text = None
            if project_id and access_token:
                is_github_project = await self._is_imported_project(project_id, access_token)
                
                # If it's a GitHub project, try to get the ingested text
                if is_github_project:
                    ingest_text = get_ingest_text(project_id)
                    if not ingest_text:
                        # Inform user, but continue without blocking
                        await on_chunk({
                            "type": "Text",
                            "value": "Note: Repository ingestion data not found. Fix may be less context-aware."
                        })
                
            # Get managers for this generation
            code_manager = self._get_code_manager(project_id, generation_id)
            integration_manager = self._get_integration_manager(project_id, generation_id)
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
            enhanced_prompt = self._update_conversation_history(session_id, error_prompt, project_history, code_manager)
            
            # Inform the user about the fix attempt
            await on_chunk({
                "type": "Text",
                "value": "Analyzing errors and generating fixes..."
            })
            
            # Generate fixed code with the enhanced prompt
            if is_github_project and ingest_text:
                # Use project-aware code generation for GitHub projects
                generated_text = await self.code_generator.generate_code(
                    enhanced_prompt, 
                    capture_response_on_chunk,
                    is_imported_project=True,
                    ingest_text=ingest_text
                )
            else:
                # Use standard code generation for regular projects
                generated_text = await self.code_generator.generate_code(
                    enhanced_prompt, 
                    capture_response_on_chunk
                )
                
            if not generated_text:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to generate fixed code. Please try again."
                })
                return {"success": False, "error": "Failed to generate fixed code"}
            
            # Extract and save the fixed code
            await on_chunk({
                "type": "Text",
                "value": "Processing code fixes..."
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
                "value": "Updating integration environment..."
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
                "value": "Analyzing fixed code..."
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
                        "value": "Code fixes applied successfully"
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
                        "value": "Restarting Flutter application..."
                    })
                    
                    # Stop the current app
                    integration_manager.stop_flutter_app()
                    
                    # Start a new Flutter app
                    web_url = integration_manager.start_flutter_app()
                    
                    if not web_url:
                        await on_chunk({
                            "type": "Error",
                            "value": "Failed to restart Flutter application"
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
                        "value": "Flutter application restarted with fixed code"
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
                    "value": "Starting Flutter application..."
                })
                
                web_url = integration_manager.start_flutter_app()
                
                if not web_url:
                    await on_chunk({
                        "type": "Error",
                        "value": "Failed to start Flutter application"
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
                    "value": "Flutter application is ready with fixed code"
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
            
    def cleanup_generation(self, project_id: str) -> bool:
        """
        Clean up resources for a project.
        
        Args:
            project_id (str): Project ID to clean up
            
        Returns:
            bool: True if cleanup was successful
        """
        try:
            # Clean up code manager resources
            if project_id in self.code_managers:
                self.code_managers[project_id].cleanup()
                del self.code_managers[project_id]
            
            # Clean up integration manager resources
            if project_id in self.integration_managers:
                # Stop any running processes
                integration_manager = self.integration_managers[project_id]
                integration_manager.stop_flutter_app()
                del self.integration_managers[project_id]
            
            return True
        except Exception as e:
            print(f"Error cleaning up project {project_id}: {str(e)}")
            return False
    
    async def _is_imported_project(self, project_id: str, access_token: str) -> bool:
        """
        Check if the project is an imported GitHub project.
        
        Args:
            project_id (str): The project ID to check
            access_token (str): The access token for API calls
            
        Returns:
            bool: True if the project is imported from GitHub
        """
        try:
            # Import at function level to avoid circular dependencies
            from api.infrastructure.projects.service import get_project
            
            # Get project details
            project_result = await get_project(project_id, access_token)
            
            if project_result and project_result.data:
                # Check if project name starts with "GitHub: "
                project_name = project_result.data.get("name", "")
                return project_name.startswith("GitHub: ")
                
            return False
        except Exception as e:
            # If we can't determine, assume it's not an imported project
            print(f"Error checking if project is imported: {str(e)}")
            return False 