"""
Configuration settings for the code generator.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default values
DEFAULT_DOCUMENTATION_PATH = "combined_documentation.md"

class Settings:
    """
    Configuration settings for the code generator.
    Provides default values and environment variable loading.
    """
    
    def __init__(self):
        """Initialize settings with default values and load environment variables."""
        # API Configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "701a4436-6bab-45b7-92e5-a1c61763e229")
        self.model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro-exp-03-25")
        
        # Default values for code generation
        self.default_username = "test"
        
        # Documentation path
        self.documentation_path = DEFAULT_DOCUMENTATION_PATH
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file") 