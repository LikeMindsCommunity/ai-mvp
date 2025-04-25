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
        # API Configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL_NAME")
        # Template repository URL   
        self.template_repo_url = os.getenv("TEMPLATE_REPO_URL")  
        # Output directory for generated projects
        self.output_dir = os.getenv("OUTPUT_DIR")
        # Documentation and SDK code paths
        self.docs_path = os.getenv("DOCS_PATH")
        self.sdk_code_path = os.getenv("SDK_CODE_PATH")

        # Default values for code generation
        self.default_username = "test"
        self.default_api_key = "701a4436-6bab-45b7-92e5-a1c61763e229"
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present and have valid values."""
        # Validate Gemini API Key
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file")
        if len(self.gemini_api_key) < 32:
            raise ValueError("GEMINI_API_KEY must be at least 32 characters long")
            
        # Validate Model Name
        if not self.model_name:
            raise ValueError("GEMINI_MODEL_NAME not found in environment variables or .env file")
        print(f"Model name from settings: {self.model_name}")
        if self.model_name not in ["gemini-2.5-pro-exp-03-25", "gemini-2.5-pro-preview-03-25"]:
            raise ValueError("GEMINI_MODEL_NAME must be either 'gemini-2.5-pro-exp-03-25' or 'gemini-2.5-pro-preview-03-25'")
            
        # Validate Template Repository URL
        if not self.template_repo_url:
            raise ValueError("TEMPLATE_REPO_URL not found in environment variables or .env file")
        if not self.template_repo_url.startswith(("http://", "https://")):
            raise ValueError("TEMPLATE_REPO_URL must be a valid HTTP/HTTPS URL")

        # Validate Output Directory
        if not self.output_dir:
            raise ValueError("OUTPUT_DIR not found in environment variables or .env file")
            
        # Validate Documentation and SDK Code Paths
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
            