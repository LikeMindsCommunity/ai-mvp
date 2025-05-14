import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Model configurations
DEFAULT_MODEL = "gemini-2.5-flash-preview-04-17"  # Default model to use
CLAUDE_MODEL = "claude-3-7-sonnet-latest"  # Default Claude model

# Vector database settings
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chroma")  # Default to ChromaDB
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")  # Local storage path

# Project settings
PROJECT_TEMP_DIR = os.getenv("PROJECT_TEMP_DIR", "./tmp")  # Temporary directory for project files 