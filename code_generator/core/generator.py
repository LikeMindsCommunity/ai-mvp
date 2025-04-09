"""
Core code generation functionality using Gemini 2.5 Pro model.
"""

from typing import Optional
from google import genai
from code_generator.config import Settings
from code_generator.utils import DocumentationManager

class CodeGenerator:
    """
    Core code generation class that handles the interaction with Gemini model
    and manages the code generation process.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the code generator with settings.
        
        Args:
            settings (Optional[Settings]): Settings object for configuration
        """
        self.settings = settings or Settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key)
        self.docs_manager = DocumentationManager(self.settings.documentation_path)
        
    def generate_code(self, user_input: str, stream: bool = False) -> str:
        """
        Generate code based on user input and documentation context.
        
        Args:
            user_input (str): The user's request for code generation
            stream (bool): Whether to stream the response in real-time
            
        Returns:
            str: The generated code with all necessary imports and setup
        """
        prompt = self._create_prompt(user_input)
        
        if stream:
            return self._generate_streaming(prompt)
        return self._generate_complete(prompt)
    
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
        
        Generate the project in a format that can be easily created using Android Studio or command line tools.
        Include all necessary files and configurations to make the project immediately buildable and runnable.
        """
    
    def _generate_streaming(self, prompt: str) -> str:
        """
        Generate code with streaming output.
        
        Args:
            prompt (str): The formatted prompt
            
        Returns:
            str: Empty string (output is printed directly)
        """
        print("\nGenerating code (streaming):")
        print("-" * 50)
        for chunk in self.client.models.generate_content_stream(
            model=self.settings.model_name,
            contents=prompt
        ):
            print(chunk.text, end="", flush=True)
        print("\n" + "-" * 50)
        return ""
    
    def _generate_complete(self, prompt: str) -> str:
        """
        Generate code with complete output.
        
        Args:
            prompt (str): The formatted prompt
            
        Returns:
            str: The generated code
        """
        response = self.client.models.generate_content(
            model=self.settings.model_name,
            contents=prompt
        )
        return response.text 