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
import subprocess
import threading
from typing import Dict, Optional, Callable, Awaitable, Any, List, Tuple
from google.genai import types

from api.domain.interfaces.flutter_generator_service import FlutterGeneratorService
from flutter_generator.core.generator import FlutterCodeGenerator
from flutter_generator.core.code_manager import FlutterCodeManager
from flutter_generator.core.integration_manager import FlutterIntegrationManager
from flutter_generator.core.conversation import FlutterConversationManager

class FlutterGeneratorServiceImpl(FlutterGeneratorService):
    """Implementation of the Flutter code generator service."""
    
    def __init__(self):
        """Initialize the Flutter generator service."""
        self.code_generator = FlutterCodeGenerator()
        self.code_manager = FlutterCodeManager()
        self.integration_manager = FlutterIntegrationManager()
        self.conversation_manager = FlutterConversationManager()
        self.root_dir = os.getcwd()
        # Dictionary to store conversation history by session ID
        self.conversation_history = {}
    
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
    
    async def generate_flutter_code(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default") -> Dict[str, Any]:
        """
        Generate Flutter code based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            
        Returns:
            Dict[str, Any]: Response containing the generation result
        """
        try:
            # First, generate a conversation plan
            await self.generate_conversation(user_query, on_chunk, session_id)
            
            # Update conversation history and get enhanced prompt
            enhanced_prompt = self._update_conversation_history(session_id, user_query)
            
            # Inform starting generation
            await on_chunk({
                "type": "Text",
                "value": "Generating Flutter code based on your request..."
            })

            # understand user query and existing code from github
            query_understanding_output = await self.code_generator.understand_user_query(user_query)
            
            # Generate code with the enhanced prompt
            generated_text = await self.code_generator.generate_code(enhanced_prompt, on_chunk)
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
            
            dart_codes = self.code_manager.extract_dart_code(generated_text)
            if not dart_codes:
                await on_chunk({
                    "type": "Error",
                    "value": "No valid Dart code found in the response"
                })
                return {"success": False, "error": "No valid Dart code found"}
            
            # Save the first code block
            latest_file = self.code_manager.save_dart_code(dart_codes[0])
            
            # Copy to integration project
            await on_chunk({
                "type": "Text",
                "value": "Setting up integration..."
            })
            
            if not self.code_manager.copy_to_integration(latest_file):
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to copy code to integration project"
                })
                return {"success": False, "error": "Failed to copy code"}
            
            # Change to integration directory
            os.chdir(os.path.join(self.root_dir, "integration"))
            
            # Run Flutter pub get
            await on_chunk({
                "type": "Text",
                "value": "Running flutter pub get..."
            })
            
            exit_code, output = self.integration_manager.run_command_with_timeout('flutter pub get', timeout=300)
            if exit_code != 0:
                await on_chunk({
                    "type": "Error",
                    "value": f"Error running flutter pub get:\n{output}"
                })
                # Return to root directory
                os.chdir(self.root_dir)
                return {"success": False, "error": f"Flutter pub get failed: {output}"}
            
            # Analyze code
            await on_chunk({
                "type": "Text",
                "value": "Analyzing Flutter code..."
            })
            
            success, error_message = self.code_manager.analyze_flutter_code()
            
            if not success:
                await on_chunk({
                    "type": "AnalysisError",
                    "value": error_message
                })
                # Return to root directory
                os.chdir(self.root_dir)
                return {
                    "success": False, 
                    "error": "Flutter code analysis found errors",
                    "analysis_error": error_message,
                    "needs_fix": True
                }
            
            # Start Flutter development server
            await on_chunk({
                "type": "Text",
                "value": "Starting Flutter development server..."
            })
            
            # Start the Flutter app with hot reload
            web_url = self.integration_manager.start_flutter_app()
            
            if not web_url:
                await on_chunk({
                    "type": "Error",
                    "value": "Failed to start Flutter development server"
                })
                # Return to root directory
                os.chdir(self.root_dir)
                return {
                    "success": False,
                    "error": "Failed to start Flutter development server"
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
            
            # Return to root directory
            os.chdir(self.root_dir)
            
            return {
                "success": True,
                "web_url": web_url,
                "code_path": latest_file
            }
            
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": f"An error occurred: {str(e)}"
            })
            # Return to root directory if needed
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return {"success": False, "error": str(e)}
    
    async def generate_conversation(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default") -> str:
        """
        Generate conversational explanation and plan for Flutter code implementation.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            
        Returns:
            str: The generated conversation text
        """
        try:
            # Use the conversation history for context if available
            enhanced_prompt = self._update_conversation_history(session_id, user_query)
            
            # Generate conversation response
            conversation_text = await self.conversation_manager.generate_conversation(enhanced_prompt, on_chunk)
            return conversation_text
            
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": f"Error generating conversation: {str(e)}"
            })
            return ""
    
    async def fix_flutter_code(self, user_query: str, error_message: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default") -> Dict[str, Any]:
        """
        Fix Flutter code based on analysis errors.
        
        Args:
            user_query (str): The original user query
            error_message (str): The Flutter analysis error message
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            
        Returns:
            Dict[str, Any]: Response containing the fixed code generation result
        """
        await on_chunk({
            "type": "Text",
            "value": "Regenerating with error fixes..."
        })
        
        # Generate conversation plan for fixing the code
        await on_chunk({
            "type": "Chat",
            "value": "Analyzing error and planning the fix..."
        })
        
        error_context = f"{user_query}\n\nPlease fix these errors:\n{error_message}"
        await self.generate_conversation(error_context, on_chunk, session_id)
        
        # Create enhanced prompt with error info
        fix_prompt = f"{user_query}\n\nPlease fix these errors:\n{error_message}"
        
        # Add this fix request to conversation history
        if session_id in self.conversation_history:
            self.conversation_history[session_id].append(fix_prompt)
        
        # Call the generate method with the enhanced prompt
        return await self.generate_flutter_code(fix_prompt, on_chunk, session_id) 