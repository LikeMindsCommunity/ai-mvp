"""
Generates code using the Gemini model based on documentation.
"""

import json
import os
import subprocess
import shutil
from typing import Dict, List, Optional, Callable

from fastapi import WebSocket
import google.genai as genai
from google.genai import types
from code_generator.config import Settings
from code_generator.core.project_creator import ProjectCreator
from code_generator.utils import DocumentationManager
from .constants import BUILD_CONFIG_FILES

class CodeGenerator:
    """Generates code using the Gemini model based on documentation."""

    def __init__(self, settings: Settings):
        """Initialize the code generator with settings."""
        self.settings = settings
        self.documentation_manager = DocumentationManager(self.settings.documentation_path)
        self.project_creator = ProjectCreator(settings)
        
        # Configure Gemini
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options=types.HttpOptions(api_version='v1alpha')
        )

    def run(self):
        """Run the code generator in interactive mode."""
        print("Welcome to the LikeMinds Android Feed SDK Code Generator!")
        print("Type 'exit' to quit.")
        print("--------------------------------------------------")
        
        while True:
            user_input = input("\nWhat project would you like to generate? ")
            
            if user_input.lower() == 'exit':
                break
                
            try:
                print("\nGenerating project...")
                success = self.create_project(user_input)
                
                if success:
                    print("\nProject generated successfully!")
                else:
                    print("\nFailed to generate project. Please check the error messages above.")
                    
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                break

    def _get_template_files(self) -> Dict[str, str]:
        """
        Get all non-build configuration files from the template project.
        
        Returns:
            Dict[str, str]: Dictionary mapping file paths to their contents
        """
        template_dir = os.path.join(os.getcwd(), "code_generator", "likeminds-feed-android-social-feed-theme")
        template_files = {}
        
        # Walk through the template directory
        for root, _, files in os.walk(template_dir):
            for file in files:
                # Get the relative path
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                
                # Skip build configuration files
                if rel_path in BUILD_CONFIG_FILES:
                    continue
                    
                # Skip .git directory and other hidden files
                if rel_path.startswith('.') or '/.git/' in rel_path:
                    continue
                    
                # Read file content
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                    template_files[rel_path] = content
                except Exception as e:
                    print(f"Error reading template file {rel_path}: {str(e)}")
                    
        return template_files

    def _create_prompt(self, user_input: str) -> str:
        """Create a prompt for the Gemini model."""
        # Load documentation
        docs_manager = DocumentationManager(self.settings.documentation_path)
        documentation = docs_manager.load_documentation()
        
        # Get template files
        template_files = self._get_template_files()
        
        # Format template files for the prompt
        template_examples = "\n\nTemplate Project Files (created for a social feed project):\n"
        for path, content in template_files.items():
            template_examples += f"\nFile: {path}\nContent:\n{content}\n"
        
        prompt = f"""You are an expert Android developer specializing in the LikeMinds Feed SDK. 
        Your task is to generate Android project code based on the following request: {user_input}

        Follow these guidelines:
        1. Use the LikeMinds Feed SDK documentation provided below for implementation details
        2. Generate ALL necessary files EXCEPT the following build configuration files: {BUILD_CONFIG_FILES}
        3. Use the correct SDK classes and methods as specified in the documentation
        4. Follow Android best practices and Kotlin coding conventions
        5. Include proper error handling and logging
        6. Use the default username and API key provided in the settings
        7. The namespace should be in the format: com.example.[project_name_lowercase]
        8. The applicationId should match the namespace
        9. IMPORTANT: When importing LikeMinds SDK classes, use 'com.likeminds' instead of 'community.likeminds'
           Example: import com.likeminds.feed.android.core.LMFeedCore
        10. Use the template project files provided below as reference for implementation. These files were created for a social feed project, so adapt them according to your specific requirements.

        Documentation:
        {documentation}

        Default Settings:
        - Username: {self.settings.default_username}
        - API Key: {self.settings.default_api_key}

        {template_examples}

        Return a JSON object with the following structure:
        {{
            "project_name": "string",
            "namespace": "string",  // e.g., "com.example.socialfeedapp"
            "application_id": "string",  // e.g., "com.example.socialfeedapp"
            "files": [
                {{
                    "path": "string",  // Path relative to project root
                    "content": "string"  // File content
                }}
            ]
        }}

        Example response:
        {{
            "project_name": "SocialFeedApp",
            "namespace": "com.example.socialfeedapp",
            "application_id": "com.example.socialfeedapp",
            "files": [
                {{
                    "path": "app/src/main/java/com/example/socialfeedapp/MainActivity.kt",
                    "content": "package com.example.socialfeedapp\\n\\nimport com.likeminds.feed.android.core.LMFeedCore\\n..."
                }}
            ]
        }}

        CRITICAL: Your response must be a valid JSON object. Do not include any markdown formatting, additional text, or explanations."""
        
        return prompt

    async def generate_code(self, user_input: str, on_chunk: Optional[Callable[[Dict], None]] = None) -> Optional[Dict]:
        """Generate code using the Gemini model."""
        try:
            # Create prompt
            prompt = self._create_prompt(user_input)
            
            # Generate content with streaming
            print("\nGenerating code...")
            response = self.client.models.generate_content_stream(
                model=self.settings.model_name,
                contents=prompt,
            )
            
            # Process streaming response
            full_response = ""
            for chunk in response:
                if chunk.text:
                    chunk_text = chunk.text
                    print(chunk_text, end='', flush=True)
                    full_response += chunk_text
                    if on_chunk:
                        await on_chunk({
                            "type": "Text",
                            "value": chunk_text
                        })
            
            print("\n")  # Add newline after streaming
            
            # Clean up the response to ensure it's valid JSON
            # Remove any markdown formatting or extra text
            full_response = full_response.strip()
            if full_response.startswith("```json"):
                full_response = full_response[7:]
            if full_response.endswith("```"):
                full_response = full_response[:-3]
            full_response = full_response.strip()
            
            # Print the cleaned response for debugging
            print("Cleaned Response:\n", full_response)
            
            # Parse response
            try:
                return json.loads(full_response)
            except json.JSONDecodeError as e:
                error_msg = f"Error: Invalid JSON response from model. Please try again.\nJSON Parse Error: {str(e)}"
                print(error_msg)
                if on_chunk:
                    await on_chunk({
                        "type": "Error",
                        "value": error_msg
                    })
                return None
                
        except Exception as e:
            error_msg = f"\nError: {str(e)}"
            print(error_msg)
            if on_chunk:
                await on_chunk({
                    "type": "Error",
                    "value": error_msg
                })
            return None

    async def create_project(self, user_input: str, on_chunk: Optional[Callable[[Dict], None]] = None) -> bool:
        """
        Generate and create a complete Android project.
        
        Args:
            user_input (str): User's input describing the project to generate
            on_chunk (Optional[Callable[[Dict], None]]): Optional callback function to handle each chunk of output
            
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            # Generate code
            project_data = await self.generate_code(user_input, on_chunk)
            if not project_data:
                return False
            
            # Create project
            return self.project_creator.create_project(project_data, on_chunk)
            
        except Exception as e:
            error_msg = f"\nError: {str(e)}"
            print(error_msg)
            if on_chunk:
                await on_chunk({
                    "type": "Error",
                    "value": error_msg
                })
            return False