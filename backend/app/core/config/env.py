"""
Environment configuration module for loading and validating environment variables.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def validate_env_vars(required_vars: List[str]) -> Dict[str, Optional[str]]:
    """
    Validate required environment variables and return their values.
    
    Args:
        required_vars: List of required environment variable names
        
    Returns:
        Dictionary mapping environment variable names to their values
        
    Raises:
        ValueError: If any required environment variable is missing
    """
    env_vars = {var: os.getenv(var) for var in required_vars}
    missing_vars = [var for var, value in env_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return env_vars

# Required API keys for LLM services
API_KEYS = validate_env_vars([
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
])

# Vector DB configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./backend/chroma_db")

# Model configurations
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
QUERY_MODEL = os.getenv("QUERY_MODEL", "claude-3-7-sonnet-20250219")
CONTEXT_MODEL = os.getenv("CONTEXT_MODEL", "gpt-4o")
RESPONSE_MODEL = os.getenv("RESPONSE_MODEL", "claude-3-7-sonnet-20250219")

# API settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000")) 