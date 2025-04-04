"""
Code Generator for LikeMinds Android Feed SDK

This script provides an interactive interface to generate code for the LikeMinds Android Feed SDK
using the Gemini 2.5 Pro model. It uses the combined documentation as context to generate
accurate and relevant code snippets based on user requests.

The Gemini 2.5 Pro model has a context window of 1 million tokens, which includes both
input tokens (prompt + documentation) and output tokens (generated code).
"""

import os
from google import genai
from dotenv import load_dotenv

class CodeGenerator:
    """
    A class that handles code generation for the LikeMinds Android Feed SDK.
    
    This class uses the Gemini 2.5 Pro model to generate code based on user requests
    and the SDK documentation. It provides an interactive interface for users to
    request specific code implementations.
    
    The model has a context window of 1 million tokens, which is shared between
    input and output tokens.
    """
    
    def __init__(self, documentation_path: str = "combined_documentation.md"):
        """
        Initialize the CodeGenerator with documentation path.
        
        Args:
            documentation_path (str): Path to the combined documentation file containing
                                    the SDK's API reference and usage examples.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file")
        
        # Initialize the Gemini client with the API key
        self.client = genai.Client(api_key=api_key)
        
        # Load and store the SDK documentation for context
        self.documentation = self._load_documentation(documentation_path)
    
    def _load_documentation(self, path: str) -> str:
        """
        Load the combined documentation file into memory.
        
        Args:
            path (str): Path to the documentation file
            
        Returns:
            str: The contents of the documentation file
            
        Raises:
            FileNotFoundError: If the documentation file doesn't exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Documentation file not found at {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_code(self, user_input: str, stream: bool = False) -> str:
        """
        Generate code based on user input and documentation context.
        
        This method creates a prompt that includes the SDK documentation and user's request,
        then uses the Gemini model to generate appropriate code.
        
        Args:
            user_input (str): The user's request for code generation
            stream (bool): Whether to stream the response in real-time
            
        Returns:
            str: The generated code with all necessary imports and setup
            
        Raises:
            Exception: If there's an error during code generation
        """
        # Create a detailed prompt that includes the SDK documentation and user's request
        prompt = f"""
        You are a code generation assistant for the LikeMinds Android Feed SDK.
        Use the following documentation to generate code that matches the user's request.
        Only use components and methods that are documented here.
        
        Documentation:
        {self.documentation}
        
        User Request: {user_input}
        
        Please generate the code that best matches the user's request.
        Include all necessary imports and follow the SDK's patterns and conventions.
        Keep the response concise and focused on the requested functionality.
        """
        
        if stream:
            # Generate code using streaming
            print("\nGenerating code (streaming):")
            print("-" * 50)
            for chunk in self.client.models.generate_content_stream(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt
            ):
                print(chunk.text, end="", flush=True)
            print("\n" + "-" * 50)
            return ""  # Return empty string since we're printing directly
        else:
            # Generate code using the Gemini 2.5 Pro model
            response = self.client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt
            )
            return response.text
    
    def interactive_mode(self):
        """
        Run the code generator in interactive mode.
        
        This method provides a command-line interface for users to:
        1. Enter their code generation requests
        2. View the generated code
        3. Exit the program
        
        The method handles errors gracefully and provides clear feedback to the user.
        """
        print("Welcome to the LikeMinds Android Feed SDK Code Generator!")
        print("Type 'exit' to quit.")
        print("-" * 50)
        
        while True:
            user_input = input("\nWhat code would you like to generate? ")
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            try:
                # Ask user if they want to stream the response
                stream_input = input("Would you like to stream the response? (y/n): ").lower()
                stream = stream_input == 'y'
                
                generated_code = self.generate_code(user_input, stream=stream)
                
                if not stream:
                    print("\nGenerated Code:")
                    print("-" * 50)
                    print(generated_code)
                    print("-" * 50)
            except Exception as e:
                print(f"Error generating code: {str(e)}")

def main():
    """
    Main entry point for the code generator.
    
    This function:
    1. Initializes the CodeGenerator
    2. Handles any initialization errors
    3. Starts the interactive mode
    """
    try:
        # Initialize and run the code generator
        generator = CodeGenerator()
        generator.interactive_mode()
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please make sure you have set your Gemini API key in the .env file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 