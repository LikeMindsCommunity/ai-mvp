"""
Generates Flutter code using the Gemini model based on documentation.
"""

import os
from typing import Dict, Optional, Callable, Awaitable, Any, List

from google import genai
from google.genai import types

from flutter_generator.config import Settings

class FlutterCodeGenerator:
    """Generates Flutter code using the Gemini model based on documentation."""

    def __init__(self, settings: Settings = None):
        """
        Initialize the code generator with settings.
        
        Args:
            settings (Settings, optional): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.system_instructions = self._load_system_instructions()
        
        # Configure Google Generative AI client
        self.client = genai.Client(api_key=self.settings.google_api_key)
        
        # Setup generation configuration
        self.generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=self.system_instructions,
        )
    
    def _load_system_instructions(self) -> List[types.Part]:
        """
        Load system instructions from files.
        
        Returns:
            List[types.Part]: List of system instruction parts
        """
        try:
            with open('prompt.txt', 'r', encoding='utf-8') as prompt_file:
                prompt_content = prompt_file.read()
            
            with open('docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            with open('code.txt', 'r', encoding='utf-8') as code_file:
                code_content = code_file.read()
            
            return [
                types.Part.from_text(text="""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text="""<flutter-docs>
                \n\nThis is the entire documentation for context:
                """ + docs_content + """</flutter-docs>"""),
                types.Part.from_text(text="""<flutter-sdk-code>
                \n\nThis is the code of the entire SDK repository for context:
                """ + code_content + """</flutter-sdk-code>"""),
            ]
        except FileNotFoundError as e:
            print(f"Error loading system instructions: {str(e)}")
            return []
    
    async def generate_code(self, user_prompt: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        """
        Generate code using the Gemini model.
        
        Args:
            user_prompt (str): User input prompt for code generation
            on_chunk (Callable): Callback function for streaming chunks
            
        Returns:
            str: Generated code response
        """
        try:
            # Create the prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)],
                ),
            ]
            
            # Generate content with streaming
            response_text = ""
            async for chunk in self.client.models.generate_content_stream(
                model=self.settings.gemini_model,
                contents=contents,
                config=self.generate_content_config,
            ):
                chunk_text = chunk.text if not chunk.function_calls else str(chunk.function_calls[0])
                
                # Stream chunk to client
                await on_chunk({
                    "type": "GeneratedText",
                    "value": chunk_text
                })
                
                response_text += chunk_text
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error generating code: {str(e)}"
            await on_chunk({
                "type": "Error",
                "value": error_msg
            })
            return "" 