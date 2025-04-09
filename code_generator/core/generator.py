"""
Core code generation functionality.
"""

import os
import json
from typing import Dict, Optional
import google.generativeai as genai
from code_generator.config import Settings
from code_generator.utils.documentation import DocumentationManager
from code_generator.core.project_creator import ProjectCreator

class CodeGenerator:
    """
    Uses Gemini to generate code based on documentation.
    """
    
    def __init__(self, api_key: str, model_name: str, template_repo_url: str = None):
        """
        Initialize the code generator.
        
        Args:
            api_key (str): Gemini API key
            model_name (str): Name of the Gemini model to use
            template_repo_url (str, optional): URL of the template repository to use as base
        """
        self.model = genai.GenerativeModel(model_name)
        genai.configure(api_key=api_key)
        self.template_repo_url = template_repo_url
        self.docs_manager = DocumentationManager("combined_documentation.md")
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a prompt for the Gemini model.
        
        Args:
            user_input (str): User's input describing the project to generate
            
        Returns:
            str: Formatted prompt for the model
        """
        documentation = self.docs_manager.load_documentation()
        example_json = r'''{
    "project_name": "SocialFeedApp",
    "files": {
        "app/src/main/java/com/example/app/MainActivity.kt": "package com.example.app\\n\\nimport androidx.appcompat.app.AppCompatActivity\\nimport android.os.Bundle\\n\\nclass MainActivity : AppCompatActivity() {\\n    override fun onCreate(savedInstanceState: Bundle?) {\\n        super.onCreate(savedInstanceState)\\n        setContentView(R.layout.activity_main)\\n    }\\n}",
        "app/src/main/res/layout/activity_main.xml": "<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?>\\n<androidx.constraintlayout.widget.ConstraintLayout xmlns:android=\\"http://schemas.android.com/apk/res/android\\"\\n    android:layout_width=\\"match_parent\\"\\n    android:layout_height=\\"match_parent\\">\\n</androidx.constraintlayout.widget.ConstraintLayout>"
    }
}'''
        return f"""You are an Android project generation assistant for the LikeMinds Android Feed SDK.
Your task is to generate only the app-specific code for an Android project that will use the SDK.

Documentation:
{documentation}

User Request: {user_input}

IMPORTANT: Your response must be a valid JSON object with the following structure:
{{
    "project_name": "string (name of the project)",
    "files": {{
        "app/src/main/java/com/example/app/MainActivity.kt": "string (Kotlin code)",
        "app/src/main/java/com/example/app/...": "string (additional Kotlin files)",
        "app/src/main/res/layout/activity_main.xml": "string (XML layout)",
        "app/src/main/res/...": "string (additional resource files)"
    }}
}}

CRITICAL INSTRUCTIONS:
1. Your response must be a valid JSON object and nothing else
2. Do not include any markdown formatting, code blocks, or additional text
3. All strings must be properly escaped:
   - Use double quotes for JSON property names and string values
   - Escape double quotes within strings with backslash: \\"
   - Escape backslashes with another backslash: \\\\
   - Escape newlines with \\n
4. The JSON must be properly formatted with correct indentation
5. Only include files that should go in the app/src directory
6. Use the template repository's package name and structure
7. Follow the SDK documentation for implementation details
8. Use the correct SDK classes and methods as described in the documentation

Example of a valid response:
{example_json}"""

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
            creator = ProjectCreator(template_repo_url=self.template_repo_url)
            return creator.create_project(project_data)
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False 