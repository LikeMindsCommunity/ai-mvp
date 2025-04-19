"""
Configuration settings for the Flutter code generator.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """
    Configuration settings for the Flutter code generator.
    Provides default values and environment variable loading.
    """
    
    def __init__(self):
        """Initialize settings with default values and load environment variables."""
        # API Configuration
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
        
        # Project paths
        self.integration_path = os.getenv("INTEGRATION_PATH", "integration")
        self.output_path = os.getenv("OUTPUT_PATH", "output")
        
        # Web server settings
        self.web_host = os.getenv("WEB_HOST", "localhost")
        self.web_port = int(os.getenv("WEB_PORT", "8080"))
        
        # Command timeout settings
        self.command_timeout = int(os.getenv("COMMAND_TIMEOUT", "300"))
        self.build_timeout = int(os.getenv("BUILD_TIMEOUT", "6000"))
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file")
        
        # Create required directories if they don't exist
        os.makedirs(self.output_path, exist_ok=True)
        
        # Ensure integration directory exists
        if not os.path.exists(self.integration_path):
            raise ValueError(f"Integration directory not found at: {self.integration_path}")
            
        # Validate model name
        if self.gemini_model not in ["gemini-2.5-pro-preview-03-25"]:
            raise ValueError("GEMINI_MODEL must be 'gemini-2.5-pro-preview-03-25'")
            
        # Validate port number
        if not (1024 <= self.web_port <= 65535):
            raise ValueError(f"Invalid web port number: {self.web_port}")
            
        # Validate timeouts
        if self.command_timeout < 1:
            raise ValueError(f"Invalid command timeout: {self.command_timeout}")
        if self.build_timeout < 1:
            raise ValueError(f"Invalid build timeout: {self.build_timeout}") 