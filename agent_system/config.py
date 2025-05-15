"""
Configuration module for Agno agents.

This module loads environment variables from .env and provides them to Agno agents.
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class AgnoConfig(BaseModel):
    """
    Configuration settings for Agno framework.
    
    This class provides access to environment variables needed by Agno agents.
    """
    # API Keys
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # Agno Configuration
    # Note: The Agno framework uses .run() method (not run_response) and returns a RunResponse object
    # containing the AI's response and various metadata. In testing, we mock this to return a simple string.
    default_model_id: str = "gemini-2.5-flash-preview-04-17"
    
agno_config = AgnoConfig()

def setup_agno_environment():
    """
    Set up environment variables for Agno.
    
    This function sets up any required environment variables for Agno to work.
    These are automatically loaded from your .env file.
    """
    # Set up Google API key for Agno
    os.environ["GOOGLE_API_KEY"] = agno_config.google_api_key
    
    # You can add more environment setup here if needed
    
    print(f"Using Agno with model: {agno_config.default_model_id}") 