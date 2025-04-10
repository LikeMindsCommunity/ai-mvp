"""
Main entry point for the document parser package.
"""

from document_parser.core import DocumentParser
from document_parser.config import Settings

def main():
    """Main entry point for the document parser."""
    try:
        # Initialize settings and document parser
        settings = Settings()
        parser = DocumentParser(settings)
        
        # Generate combined document
        parser.generate_combined_document()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
