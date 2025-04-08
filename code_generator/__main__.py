"""
Main entry point for the code generator.
"""

from code_generator import CodeGenerator, Settings

def main():
    """
    Main entry point for the code generator.
    
    This function:
    1. Initializes the CodeGenerator with settings
    2. Handles any initialization errors
    3. Starts the interactive mode
    """
    try:
        # Initialize settings and code generator
        settings = Settings()
        generator = CodeGenerator(settings)
        
        # Start interactive mode
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
                
                generated_code = generator.generate_code(user_input, stream=stream)
                
                if not stream:
                    print("\nGenerated Code:")
                    print("-" * 50)
                    print(generated_code)
                    print("-" * 50)
            except Exception as e:
                print(f"Error generating code: {str(e)}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please make sure you have set your Gemini API key in the .env file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 