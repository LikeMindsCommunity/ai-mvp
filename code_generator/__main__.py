"""
Main entry point for the code generator package.
"""

import os
from dotenv import load_dotenv
from code_generator.core.generator import CodeGenerator
from code_generator.config.settings import Settings

def main():
    """
    Main function to run the code generator.
    """
    # Load environment variables
    load_dotenv()
    
    # Get settings
    settings = Settings()
    
    # Create code generator
    generator = CodeGenerator(
        api_key=settings.gemini_api_key,
        model_name=settings.model_name,
        template_repo_url=os.getenv("TEMPLATE_REPO_URL")
    )
    
    print("Welcome to the LikeMinds Android Feed SDK Code Generator!")
    print("Type 'exit' to quit.")
    print("--------------------------------------------------")
    
    while True:
        user_input = input("\nWhat project would you like to generate? ")
        
        if user_input.lower() == 'exit':
            break
            
        try:
            print("\nGenerating project...")
            success = generator.create_project(user_input)
            
            if success:
                print("\nProject generated successfully!")
            else:
                print("\nFailed to generate project. Please check the error messages above.")
                
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break

if __name__ == "__main__":
    main() 