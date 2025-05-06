"""
Conversational interface for existing GitHub project analysis and conversation.

Response Types:
- Chat: Conversational explanations and analysis of existing projects
- Error: Error messages
"""

import os
from typing import Dict, Optional, Callable, Awaitable, Any, List

from google import genai
from google.genai import types

from flutter_generator.config import Settings
from flutter_generator.utils.ingest import get_ingest_text

class ExistingProjectConversationManager:
    """Manages conversational responses for existing GitHub projects."""

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
            # Load custom prompt for existing projects
            prompt_path = 'existing-project-prompt.txt'
            if os.path.exists(prompt_path):
                with open(prompt_path, 'r', encoding='utf-8') as prompt_file:
                    prompt_content = prompt_file.read()
            
            with open('docs.txt', 'r', encoding='utf-8') as docs_file:
                docs_content = docs_file.read()
            
            return [
                types.Part.from_text(text="""You are a helpful Flutter development assistant that analyzes existing 
                GitHub project and explains the approaches to extend them by integrating the LikeMinds Flutter Chat SDK.
                You have access to the full ingested project source code and documentation.
                Focus on helping users understand the existing codebase and suggesting approaches for new features."""),
                types.Part.from_text(text=prompt_content),
                types.Part.from_text(text="""<flutter-docs>
                \n\nThis is the entire documentation for context:
                """ + docs_content + """</flutter-docs>"""),
            ]
        except FileNotFoundError as e:
            print(f"Error loading system instructions: {str(e)}")
            return []
    
    async def generate_conversation(self, user_prompt: str, project_id: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        """
        Generate conversational response analyzing the existing project.
        
        Args:
            user_prompt (str): User input prompt
            project_id (str): Project ID to analyze
            on_chunk (Callable): Callback function for streaming chunks
            
        Returns:
            str: Complete conversational response
        """
        try:
            # Inform starting project analysis
            await on_chunk({
                "type": "Text",
                "value": "Analyzing existing project structure..."
            })
            
            # Get the ingested project text
            project_text = get_ingest_text(project_id)
            if not project_text:
                error_msg = f"Could not find or generate project ingest for {project_id}"
                await on_chunk({
                    "type": "Error",
                    "value": error_msg
                })
                return ""
            
            # Enhance the prompt to focus on analysis
            enhanced_prompt = f"""
            Based on this request: "{user_prompt}"
            
            Please analyze the project structure and provide:
            1. A brief overview of the key components and architecture
            2. The main Flutter and Dart packages used in the project
            3. A response to the specific query or feature request
            
            Focus on explaining the project structure first, then address the specific request.
            """
            
            # Create content with ingested project data
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=enhanced_prompt),
                        types.Part.from_text(text=f"""<project-code>
                        {project_text}
                        </project-code>""")
                    ],
                ),
            ]
            
            # Generate content with streaming
            response_text = ""
            
            # Get the streaming response
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            )
            
            # Process the stream
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
            error_msg = f"Error analyzing project: {str(e)}"
            await on_chunk({
                "type": "Error",
                "value": error_msg
            })
            return "" 