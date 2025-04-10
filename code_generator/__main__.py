"""
Main entry point for the code generator.
"""

import sys
from code_generator.config import Settings
from code_generator.core import CodeGenerator

def main():
    """Main entry point for the code generator."""
    try:
        # Initialize settings
        settings = Settings()
        
        # Initialize code generator
        generator = CodeGenerator(settings)
        
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
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 