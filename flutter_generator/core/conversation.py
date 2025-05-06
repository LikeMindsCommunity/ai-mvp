"""
Conversational interface for Flutter code generation planning and explanation.

Response Types:
- Chat: Conversational explanations and generation plans
- Error: Error messages
"""

import os
from typing import Dict, Optional, Callable, Awaitable, Any, List

from google import genai
from google.genai import types

from flutter_generator.config import Settings

class FlutterConversationManager:
    """Manages conversational responses for Flutter code generation."""

    def __init__(self, settings: Settings = None):
        """
        Initialize the conversation manager with settings.
        
        Args:
            settings (Settings, optional): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.system_instructions = self._load_system_instructions()
        
        # Configure Google Generative AI client
        self.client = genai.Client(
            api_key=self.settings.google_api_key,
        )
        
        # Setup model and configuration
        self.model = self.settings.gemini_model
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=self.system_instructions,
        )
    
    def _load_system_instructions(self) -> List[types.Part]:
        """
        Load system instructions for conversation.
        
        Returns:
            List[types.Part]: List of system instruction parts
        """
        try:
            with open('chat-prompt.txt', 'r', encoding='utf-8') as prompt_file:
                prompt_content = prompt_file.read()
            
            with open('docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            return [
                types.Part.from_text(text="""You are a helpful Flutter development assistant that explains the approach to solving user requests. 
                For each request, provide:
                1. A brief summary of what you understand from the request
                2. The key Flutter components and LikeMinds SDK features that will be used
                3. A step-by-step plan for implementing the solution
                
                Keep explanations clear, concise and focused on Flutter development best practices."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text="""<flutter-docs>
                \n\nThis is the entire documentation for context:
                """ + docs_content + """</flutter-docs>"""),
            ]
        except FileNotFoundError as e:
            print(f"Error loading system instructions: {str(e)}")
            return []
    
    async def generate_conversation(self, user_prompt: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        """
        Generate conversational response about Flutter code generation approach.
        
        Args:
            user_prompt (str): User input prompt
            on_chunk (Callable): Callback function for streaming chunks
            
        Returns:
            str: Complete conversational response
        """
        try:
            # Enhance the prompt to focus on explanation and planning
            enhanced_prompt = f"""
            Based on this request: "{user_prompt}"
            
            Please provide:
            1. A brief summary of what you understand from the request
            2. The key Flutter components and LikeMinds SDK features that will be used
            3. A step-by-step plan for implementing the solution
            
            Focus on explaining your approach rather than writing the actual code.
            """
            
            # Create content from enhanced prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=enhanced_prompt)],
                ),
            ]
            
            # Generate content with streaming
            response_text = ""
            
            # Inform starting conversation generation
            await on_chunk({
                "type": "Text",
                "value": "Planning approach of implementation.."
            })
            
            # Get the streaming response
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            )
            
            # Process the stream with a regular for loop
            for chunk in stream:
                # Safely extract text from chunk
                chunk_text = ""
                if hasattr(chunk, 'text') and chunk.text is not None:
                    chunk_text = chunk.text
                elif hasattr(chunk, 'function_calls') and chunk.function_calls:
                    chunk_text = str(chunk.function_calls[0])
                
                # Skip empty chunks
                if not chunk_text:
                    continue
                
                # Stream chunk to client with "Chat" type
                await on_chunk({
                    "type": "Chat",
                    "value": chunk_text
                })
                
                response_text += chunk_text
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error generating conversation: {str(e)}"
            await on_chunk({
                "type": "Error",
                "value": error_msg
            })
            return "" 