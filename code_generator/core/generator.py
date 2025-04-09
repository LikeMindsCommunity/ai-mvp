"""
Core code generation functionality.
"""

import json
import os
from typing import Dict, List, Optional
import google.generativeai as genai
from code_generator import Settings, DocumentationManager, ProjectCreator

class CodeGenerator:
    """
    Uses Gemini to generate code based on documentation.
    """
    
    def __init__(self, settings: Settings):
        """Initialize the code generator with settings."""
        self.settings = settings
        self.model = genai.GenerativeModel(settings.model_name)
        genai.configure(api_key=settings.gemini_api_key)
    
    def _create_prompt(self, user_input: str) -> str:
        """Create a prompt for the Gemini model."""
        # Load documentation
        docs_manager = DocumentationManager(self.settings.documentation_path)
        documentation = docs_manager.load_documentation()
        
        prompt = f"""You are an expert Android developer specializing in the LikeMinds Feed SDK. 
        Your task is to generate Android project code based on the following request: {user_input}

        Follow these guidelines:
        1. Use the LikeMinds Feed SDK documentation provided below for implementation details
        2. Generate only the necessary files in the app/src directory
        3. Use the correct SDK classes and methods as specified in the documentation
        4. Follow Android best practices and Kotlin coding conventions
        5. Include proper error handling and logging
        6. Use the default username and API key provided in the settings

        Documentation:
        {documentation}

        Default Settings:
        - Username: {self.settings.default_username}
        - API Key: {self.settings.default_api_key}

        Return a JSON object with the following structure:
        {{
            "project_name": "string",
            "files": [
                {{
                    "path": "string",
                    "content": "string"
                }}
            ]
        }}

        Example response:
        {{
            "project_name": "SocialFeedApp",
            "files": [
                {{
                    "path": "app/src/main/java/com/example/socialfeed/MainActivity.kt",
                    "content": "package com.example.socialfeed\\n\\nimport ..."
                }}
            ]
        }}

        CRITICAL: Your response must be a valid JSON object. Do not include any markdown formatting, additional text, or explanations."""
        
        return prompt

    def generate_code(self, user_input: str) -> Dict:
        """
        Generate code based on user input.
        
        Args:
            user_input (str): User's input describing the project to generate
            
        Returns:
            Dict: Generated project structure and files
        """
        try:
            prompt = self._create_prompt(user_input)
            response = self.model.generate_content(prompt)
            
            # Print raw response for debugging
            print("\nRaw response from model:")
            print("----------------------")
            print(response.text)
            print("----------------------\n")
            
            # Clean the response by removing markdown code block markers
            cleaned_response = response.text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Try to parse the response as JSON
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {str(e)}")
                print("Response was not valid JSON. Please check the raw response above.")
                raise
                
        except Exception as e:
            print(f"Error generating code: {str(e)}")
            raise
    
    def create_project(self, user_input: str) -> bool:
        """
        Generate and create a complete Android project.
        
        Args:
            user_input (str): User's input describing the project to generate
            
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            # Generate project data
            project_data = self.generate_code(user_input)
            
            # Create project using template
            creator = ProjectCreator(template_repo_url=self.settings.template_repo_url)
            return creator.create_project(project_data)
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False 