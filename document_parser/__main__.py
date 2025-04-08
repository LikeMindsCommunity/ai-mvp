"""
Main entry point for the document parser package.
"""

from document_parser import DocumentParser, Settings

def main():
    """Main entry point for the document parser."""
    try:
        # Initialize settings and document parser
        settings = Settings()
        parser = DocumentParser(settings)
        
        # Generate combined document
        parser.generate_combined_document()
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please make sure you have set the required environment variables:")
        print("- REPO_URL: URL of the Git repository")
        print("- INCLUDED_DIRS: Comma-separated list of directories to include")
        print("- EXCLUDED_DIRS (optional): Comma-separated list of directories to exclude")
        print("- OUTPUT_FILE (optional): Path to save the combined documentation")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
