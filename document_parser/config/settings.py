"""
Configuration settings for the document parser.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default values
DEFAULT_OUTPUT_FILE = "combined_documentation.md"

class Settings:
    """
    Configuration settings for the document parser.
    Provides default values and environment variable loading.
    """
    
    def __init__(self):
        """Initialize settings with default values and load environment variables."""
        # Repository configuration
        self.repo_url = os.getenv("REPO_URL")
        self.included_dirs = os.getenv("INCLUDED_DIRS", "").split(",")
        self.excluded_dirs = os.getenv("EXCLUDED_DIRS", "").split(",")
        
        # Output configuration
        self.output_file = os.getenv("OUTPUT_FILE", DEFAULT_OUTPUT_FILE)
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present."""
        if not self.repo_url:
            raise ValueError("REPO_URL not found in environment variables or .env file")
        if not self.included_dirs or self.included_dirs == [""]:
            raise ValueError("INCLUDED_DIRS not found in environment variables or .env file") 