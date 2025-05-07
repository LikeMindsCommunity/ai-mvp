"""
Configuration settings for the code generator.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Configuration settings for the code generator.
    Provides default values and environment variable loading.
    """
    
    def __init__(self):
        """Initialize settings with default values and load environment variables."""
        # Gemini configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model_name = os.getenv("GEMINI_MODEL_NAME")
        
        # Project configuration
        self.output_dir = os.getenv("OUTPUT_DIR")
        
        # Documentation paths
        self.docs_path = os.getenv("DOCS_PATH")
        self.sdk_code_path = os.getenv("SDK_CODE_PATH")
        
        # Default values for code generation
        self.default_username = "test"
        self.default_api_key = "701a4436-6bab-45b7-92e5-a1c61763e229"
        
        # Validate settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate all required settings are present and valid."""
        # Validate Gemini configuration
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file")
        
        if not self.gemini_model_name:
            raise ValueError("GEMINI_MODEL_NAME not found in environment variables or .env file")
        
        if self.gemini_model_name not in ["gemini-2.5-pro-preview-03-25", "gemini-2.5-pro-exp-03-25", "gemini-2.5-flash-preview-04-17"]:
            raise ValueError("GEMINI_MODEL_NAME must be one of: gemini-2.5-pro-preview-03-25, gemini-2.5-pro-exp-03-25")
        
        # Validate project configuration
        if not self.output_dir:
            raise ValueError("OUTPUT_DIR not found in environment variables or .env file")
        
        # Validate documentation paths
        if not self.docs_path:
            raise ValueError("DOCS_PATH not found in environment variables or .env file")
        if not os.path.exists(self.docs_path):
            raise ValueError(f"Documentation file not found at: {self.docs_path}")
        if not os.path.isfile(self.docs_path):
            raise ValueError(f"Documentation path must be a file: {self.docs_path}")
        
        if not self.sdk_code_path:
            raise ValueError("SDK_CODE_PATH not found in environment variables or .env file")
        if not os.path.exists(self.sdk_code_path):
            raise ValueError(f"SDK code file not found at: {self.sdk_code_path}")
        if not os.path.isfile(self.sdk_code_path):
            raise ValueError(f"SDK code path must be a file: {self.sdk_code_path}")
            