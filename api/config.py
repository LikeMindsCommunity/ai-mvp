"""
Configuration module for the API.
"""
import os
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class TokenPayload(BaseModel):
    """Token payload model."""
    exp: int
    sub: str

def read_private_key(file_path: str) -> Optional[str]:
    """
    Read the private key from a file.
    
    Args:
        file_path (str): Path to the private key file.
        
    Returns:
        Optional[str]: Private key content or None if not found.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading private key file: {e}")
        return None
class Settings(BaseSettings):
    """Settings model."""
    # Supabase settings
    supabase_url: str = Field(default=os.getenv("SUPABASE_URL", ""))
    supabase_anon_key: str = Field(default=os.getenv("SUPABASE_ANON_KEY", ""))
    supabase_service_key: str = Field(default=os.getenv("SUPABASE_SERVICE_KEY", ""))
    
    # Frontend settings
    frontend_url: str = Field(default=os.getenv("FRONTEND_URL", "http://localhost:8080"))
    frontend_callback_path: str = Field(default=os.getenv("FRONTEND_CALLBACK_PATH", ""))

        # JWT settings
    jwt_secret: str = Field(default=os.getenv("JWT_SECRET", "your-secret-key-for-jwt-signing"))
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day
    
    # API settings
    api_url: str = Field(default=os.getenv("API_URL", "http://localhost:8000"))
    google_api_key: str = Field(default=os.getenv("GOOGLE_API_KEY", ""))
    gemini_model: str = Field(default=os.getenv("GEMINI_MODEL", "gemini-2.5-pro-preview-03-25"))
    
    # Host settings
    web_host: str = Field(default=os.getenv("WEB_HOST", "0.0.0.0"))
    public_host: str = Field(default=os.getenv("PUBLIC_HOST", "localhost"))
    flutter_web_port: int = Field(default=int(os.getenv("FLUTTER_WEB_PORT", "8080")))
    web_port: int = Field(default=int(os.getenv("WEB_PORT", "8080")))
    api_port: int = Field(default=int(os.getenv("API_PORT", "8000")))
    
    # Timeout settings
    command_timeout: int = Field(default=int(os.getenv("COMMAND_TIMEOUT", "600")))
    build_timeout: int = Field(default=int(os.getenv("BUILD_TIMEOUT", "6000")))

    # GitHub settings
    github_app_id: str = Field(default=os.getenv("GITHUB_APP_ID", ""))

    
    # with open(os.getenv("GITHUB_PRIVATE_KEY_PATH"), "r") as key_file:
    #         github_private_key = key_file.read()
    # #github_private_key:str = read_private_key(os.getenv("", ""))
    # # github_private_key: str = Field(default=)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings: Application settings
    """
    return Settings() 


