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
    Main code generator class that uses Gemini to generate code based on documentation.
    """
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the code generator with settings.
        
        Args:
            settings (Settings, optional): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.docs_manager = DocumentationManager(self.settings.documentation_path)
        
        # Configure Gemini
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel(self.settings.model_name)
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a detailed prompt that includes documentation and user request.
        
        Args:
            user_input (str): The user's request
            
        Returns:
            str: Formatted prompt with documentation context
        """
        documentation = self.docs_manager.load_documentation()
        return f"""
        You are an Android project generation assistant for the LikeMinds Android Feed SDK.
        Your task is to create a complete Android project that integrates the SDK based on the user's request.
        
        Documentation:
        {documentation}
        
        User Request: {user_input}
        
        Generate a complete Android project that includes:
        
        1. Project Structure:
           - Create a new Android project with proper package structure
           - Include all necessary directories (app/, build/, gradle/, etc.)
           - Follow Android project conventions
        
        2. Gradle Configuration:
           - Create root build.gradle with necessary plugins and repositories
           - Create app/build.gradle with SDK dependencies and configurations
           - Include settings.gradle for project settings
           - Add gradle wrapper files (gradlew, gradlew.bat)
           - Configure proper Android SDK versions and build tools
        
        3. Core Components:
           - Generate Activities and Fragments
           - Create ViewModels for state management
           - Implement necessary interfaces and classes
           - Add proper dependency injection setup
        
        4. UI Implementation:
           - Create layout files (XML)
           - Add necessary resources (drawables, strings, colors)
           - Implement proper navigation
           - Follow Material Design guidelines
        
        5. SDK Integration:
           - Add SDK dependencies in build.gradle
           - Implement SDK initialization
           - Create necessary configurations
           - Add proper error handling
        
        6. Documentation:
           - Create a README.md with setup instructions
           - Add code comments explaining implementation
           - Include usage examples
        
        The project should:
        - Follow Android best practices and conventions
        - Use the latest stable versions of dependencies
        - Include proper error handling and logging
        - Be modular and maintainable
        - Support both debug and release builds
        - Include proper ProGuard rules if needed
        
        IMPORTANT: When generating code that requires a username, use "{self.settings.default_username}" and for the api key use "{self.settings.default_api_key}".
        
        CRITICAL INSTRUCTION: Your response must be a valid JSON object and nothing else. Do not include any markdown formatting, code blocks, or additional text.
        
        Your response must follow this exact JSON structure:
        {{
            "project_name": "name-of-project",
            "files": {{
                "build.gradle": "plugins {{\n    id 'com.android.application'\n    id 'org.jetbrains.kotlin.android'\n}}\n...",
                "app/build.gradle": "android {{\n    namespace 'com.example.app'\n    ...",
                "settings.gradle": "rootProject.name = 'name-of-project'\n...",
                "app/src/main/AndroidManifest.xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<manifest ...",
                "app/src/main/java/com/example/app/MainActivity.kt": "package com.example.app\n\nimport ...",
                "app/src/main/res/layout/activity_main.xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<androidx.constraintlayout...",
                "README.md": "# Project Name\n\n## Setup Instructions\n..."
            }}
        }}
        
        Example of a valid response:
        {{
            "project_name": "social-feed",
            "files": {{
                "build.gradle": "plugins {{\n    id 'com.android.application'\n    id 'org.jetbrains.kotlin.android'\n}}\n\ndependencies {{\n    implementation 'com.likeminds:feed-sdk:1.0.0'\n}}",
                "app/build.gradle": "android {{\n    namespace 'com.example.socialfeed'\n    compileSdk 34\n\n    defaultConfig {{\n        applicationId \"com.example.socialfeed\"\n        minSdk 24\n        targetSdk 34\n    }}\n}}",
                "app/src/main/AndroidManifest.xml": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\">\n    <application\n        android:name=\".SocialFeedApplication\"\n        ...>\n    </application>\n</manifest>",
                "app/src/main/java/com/example/socialfeed/SocialFeedActivity.kt": "package com.example.socialfeed\n\nimport androidx.appcompat.app.AppCompatActivity\nimport com.likeminds.feed.LikeMindsFeed\n\nclass SocialFeedActivity : AppCompatActivity() {{\n    override fun onCreate(savedInstanceState: Bundle?) {{\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_social_feed)\n        \n        // Initialize SDK\n        LikeMindsFeed.init(this, \"{self.settings.default_api_key}\", \"{self.settings.default_username}\")\n    }}\n}}"
            }}
        }}
        
        Remember: Your response must be a valid JSON object and nothing else. Do not include any markdown formatting, code blocks, or additional text.
        """
    
    def generate_code(self, user_input: str) -> Optional[Dict]:
        """
        Generate code based on user input and documentation.
        
        Args:
            user_input (str): The user's request
            
        Returns:
            Optional[Dict]: Generated code and project structure, or None if generation failed
        """
        try:
            # Create prompt and get response from Gemini
            prompt = self._create_prompt(user_input)
            response = self.model.generate_content(prompt)
            
            # Print raw response for debugging
            print("\nRaw response from model:")
            print("----------------------")
            print(response.text)
            print("----------------------\n")
            
            # Clean the response by removing markdown formatting and invalid characters
            cleaned_response = response.text.strip()
            
            # Remove markdown code block markers
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            # Remove any non-printable characters and extra whitespace
            cleaned_response = ''.join(char for char in cleaned_response if char.isprintable())
            cleaned_response = ' '.join(cleaned_response.split())
            
            # Print cleaned response for debugging
            print("\nCleaned response:")
            print("----------------------")
            print(cleaned_response)
            print("----------------------\n")
            
            # Parse the response as JSON
            try:
                generated_project = json.loads(cleaned_response)
                return generated_project
            except json.JSONDecodeError as e:
                print(f"Error parsing generated code: {str(e)}")
                print("Response was not valid JSON. Please check the raw and cleaned responses above.")
                return None
                
        except Exception as e:
            print(f"Error generating code: {str(e)}")
            return None
    
    def create_project(self, user_input: str) -> bool:
        """
        Generate and create a complete Android project.
        
        Args:
            user_input (str): The user's request
            
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            # Generate the project structure and code
            generated_project = self.generate_code(user_input)
            if not generated_project:
                return False
            
            # Create the project using ProjectCreator
            project_name = generated_project.get('project_name', 'android-project')
            project_creator = ProjectCreator(project_name, generated_project.get('files', {}))
            
            # Create and build the project
            if not project_creator.create_project():
                return False
            
            return project_creator.build_project()
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False 