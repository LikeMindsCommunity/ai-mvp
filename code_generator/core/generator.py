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
        You are a project generation assistant for the LikeMinds Android Feed SDK.
        Use the following documentation to generate a complete Android project that matches the user's request.
        
        Examples of existing projects:
        1. qna-feed: Generated from "generate qna feed theme"
        2. social-feed: Generated from "generate social feed theme"
        3. video-feed: Generated from "generate video feed theme"
        
        Note: In the example projects, likeminds-feed-android-core is added as a local package in their root build.gradle.
        However, in your generated project, you should use the dependency as specified in the documentation instead of local package references.
        
        Documentation:
        {documentation}
        
        User Request: {user_input}
        
        Please generate a complete Android project that includes:
        1. Project structure (directories and files)
        2. Gradle configuration files (build.gradle, settings.gradle)
        3. Android manifest
        4. Core components (Activities, Fragments, ViewModels)
        5. UI layouts and resources
        6. Dependencies and configurations
        7. Documentation and README
        
        The project should:
        - Follow Android best practices and conventions
        - Use the LikeMinds Feed SDK components
        - Include proper error handling and state management
        - Be modular and maintainable
        - Include necessary imports and dependencies
        - Follow the same structure as existing feed projects
        - Use the SDK dependency from documentation, not local package references
        
        IMPORTANT: When generating code that requires a username, use "{self.settings.default_username}" and for the api key use "{self.settings.default_api_key}".
        
        Generate the project structure and files in a format that can be easily created and used.
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