"""
Main entry point for the code generator package.
"""

import sys
from code_generator import CodeGenerator, Settings

def main():
    """Main entry point for the code generator."""
    try:
        # Initialize settings and code generator
        settings = Settings()
        generator = CodeGenerator(settings)
        
        print("Welcome to the LikeMinds Android Feed SDK Code Generator!")
        print("Type 'exit' to quit.")
        print("-" * 50)
        
        while True:
            user_input = input("\nWhat project would you like to generate? ")
            
            if user_input.lower() == 'exit':
                break
            
            print("\nGenerating project...")
            if generator.create_project(user_input):
                print("\nProject generated successfully!")
            else:
                print("\nFailed to generate project. Please try again.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 