"""
Generates Flutter code using the Gemini model based on documentation.

Response Types:
- Text: Status updates and progress messages
- Code: Generated code content
- Error: Error messages
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
        self.system_instructions = None  # Will be loaded on demand
        
        # Configure Google Generative AI client
        self.client = genai.Client(
            api_key=self.settings.google_api_key,
        )
        
        # Setup model
        self.model = self.settings.gemini_model
    
    def _load_system_instructions(self, is_imported_project: bool = False, ingest_text: Optional[str] = None) -> List[types.Part]:
        """
        Load system instructions from files.
        
        Args:
            is_imported_project (bool): Whether the project is imported from GitHub
            ingest_text (str, optional): Ingested text from the GitHub repository
            
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
            
            instructions = [
                types.Part.from_text(text="""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text="""<flutter-docs>
                \n\nThis is the entire documentation for context:
                """ + docs_content + """</flutter-docs>"""),
                types.Part.from_text(text="""<flutter-sdk-code>
                \n\nThis is the code of the entire SDK repository for context:
                """ + code_content + """</flutter-sdk-code>"""),
            ]
            
            # If this is an imported project, add the project code as a context
            if is_imported_project and ingest_text:
                instructions.append(
                    types.Part.from_text(text=f"""<project-code>
                    \n\nThis is the code of the GitHub project that needs modification:
                    {ingest_text}
                    </project-code>""")
                )
                
                # Add specific instruction for imported projects
                instructions.append(
                    types.Part.from_text(text="""
                    For this GitHub project, focus on integrating the LikeMinds SDK into the existing codebase:
                    1. Respect the project's existing architecture, patterns, and naming conventions
                    2. Only modify or add files that are necessary for the integration
                    3. Preserve existing functionality while adding LikeMinds features
                    4. Generate code that works harmoniously with the existing project structure
                    """)
                )
            
            return instructions
        except FileNotFoundError as e:
            print(f"Error loading system instructions: {str(e)}")
            return []
    
    async def generate_code(self, user_prompt: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], 
                          is_imported_project: bool = False, ingest_text: Optional[str] = None) -> str:
        """
        Generate code using the Gemini model.
        
        Args:
            user_prompt (str): User input prompt for code generation
            on_chunk (Callable): Callback function for streaming chunks
            is_imported_project (bool): Whether the project is imported from GitHub
            ingest_text (str, optional): Ingested text from the GitHub repository
            
        Returns:
            str: Generated code response
        """
        try:
            # Load system instructions with potential project context
            self.system_instructions = self._load_system_instructions(is_imported_project, ingest_text)
            
            # Configure content generation with instructions
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=self.system_instructions,
            )
            
            # Create content from user prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)],
                ),
            ]
            
            # Generate content with streaming
            response_text = ""
            
            # Inform about the generation type
            if is_imported_project:
                await on_chunk({
                    "type": "Text",
                    "value": "Generating code based on existing GitHub project structure..."
                })
            else:
                await on_chunk({
                    "type": "Text",
                    "value": "Generating new Flutter code..."
                })
            
            # Get the streaming response
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
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
                
                # Stream chunk to client
                await on_chunk({
                    "type": "Code",
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