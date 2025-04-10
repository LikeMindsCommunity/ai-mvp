"""
Generates code using the Gemini model based on documentation.
"""

import json
import os
import subprocess
import shutil
from typing import Dict, Optional, Callable

import google.genai as genai
from google.genai import types
from code_generator.config import Settings
from code_generator.core.project_creator import ProjectCreator
from code_generator.utils import DocumentationManager

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

    def _get_template_build_config(self) -> str:
        """Get the build configuration from the template repository."""
        try:
            # Use the local template directory
            template_dir = os.path.join(os.getcwd(), "code_generator", "likeminds-feed-android-social-feed-theme")
            
            # Read build configuration files
            build_config = []
            
            # Read build.gradle
            with open(os.path.join(template_dir, 'build.gradle'), 'r') as f:
                build_config.append("build.gradle:\n" + f.read())
            
            # Read gradle.properties
            with open(os.path.join(template_dir, 'gradle.properties'), 'r') as f:
                build_config.append("gradle.properties:\n" + f.read())
            
            # Read settings.gradle
            with open(os.path.join(template_dir, 'settings.gradle'), 'r') as f:
                build_config.append("settings.gradle:\n" + f.read())
            
            # Read local.properties
            with open(os.path.join(template_dir, 'local.properties'), 'r') as f:
                build_config.append("local.properties:\n" + f.read())
            
            # Skip binary files (gradlew and gradlew.bat)
            
            # Read gradle directory files
            gradle_dir = os.path.join(template_dir, 'gradle')
            if os.path.exists(gradle_dir):
                for root, dirs, files in os.walk(gradle_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, template_dir)
                        
                        # Skip binary files
                        if file.endswith('.jar') or file.endswith('.bat'):
                            continue
                            
                        try:
                            with open(file_path, 'r') as f:
                                build_config.append(f"{relative_path}:\n" + f.read())
                        except UnicodeDecodeError:
                            # Skip binary files
                            continue
            
            return "\n\n".join(build_config)
            
        except Exception as e:
            print(f"Error getting template build configuration: {str(e)}")
            return ""

    def _create_prompt(self, user_input: str) -> str:
        """Create a prompt for the Gemini model."""
        # Load documentation
        docs_manager = DocumentationManager(self.settings.documentation_path)
        documentation = docs_manager.load_documentation()
        
        # Get template build configuration
        build_config = self._get_template_build_config()
        
        prompt = f"""You are an expert Android developer specializing in the LikeMinds Feed SDK. 
        Your task is to generate Android project code based on the following request: {user_input}

        Follow these guidelines:
        1. Use the LikeMinds Feed SDK documentation provided below for implementation details
        2. Generate ALL necessary files including build configuration files
        3. Use the correct SDK classes and methods as specified in the documentation
        4. Follow Android best practices and Kotlin coding conventions
        5. Include proper error handling and logging
        6. Use the default username and API key provided in the settings
        7. Use the template's build configuration files as a reference for your generated files

        Documentation:
        {documentation}

        Default Settings:
        - Username: {self.settings.default_username}
        - API Key: {self.settings.default_api_key}

        Template Build Configuration:
        {build_config}

        Return a JSON object with the following structure:
        {{
            "project_name": "string",
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
            "files": [
                {{
                    "path": "build.gradle",
                    "content": "plugins { ... }"
                }},
                {{
                    "path": "app/build.gradle",
                    "content": "plugins { ... }"
                }},
                {{
                    "path": "settings.gradle",
                    "content": "rootProject.name = ..."
                }},
                {{
                    "path": "gradle.properties",
                    "content": "org.gradle.jvmargs=..."
                }},
                {{
                    "path": "app/src/main/java/com/example/socialfeed/MainActivity.kt",
                    "content": "package com.example.socialfeed\\n\\nimport ..."
                }}
            ]
        }}

        CRITICAL: Your response must be a valid JSON object. Do not include any markdown formatting, additional text, or explanations."""
        
        return prompt

    def generate_code(self, user_input: str, on_chunk: Callable[[str], None] = None) -> Optional[Dict]:
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
                        on_chunk(chunk_text)
            
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
                    on_chunk(error_msg)
                return None
                
        except Exception as e:
            error_msg = f"\nError: {str(e)}"
            print(error_msg)
            if on_chunk:
                on_chunk(error_msg)
            return None

    def create_project(self, user_input: str, on_chunk: Callable[[str], None] = None) -> bool:
        """
        Generate and create a complete Android project.
        
        Args:
            user_input (str): User's input describing the project to generate
            on_chunk (Callable[[str], None], optional): Callback function to handle each chunk of output
            
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            # Generate project data
            project_data = self.generate_code(user_input, on_chunk)
            
            # Create project using template
            return self.project_creator.create_project(project_data)
            
        except Exception as e:
            error_msg = f"Error creating project: {str(e)}"
            print(error_msg)
            if on_chunk:
                on_chunk(error_msg)
            return False