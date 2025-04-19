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

class Settings(BaseSettings):
    """Settings model."""
    # Supabase settings
    supabase_url: str = Field(default=os.getenv("SUPABASE_URL", ""))
    supabase_anon_key: str = Field(default=os.getenv("SUPABASE_ANON_KEY", ""))
    supabase_service_key: str = Field(default=os.getenv("SUPABASE_SERVICE_KEY", ""))
    
    # JWT settings
    jwt_secret: str = Field(default=os.getenv("JWT_SECRET", "your-secret-key-for-jwt-signing"))
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day
    
    # API settings
    google_api_key: Optional[str] = Field(default=os.getenv("GOOGLE_API_KEY", None))
    gemini_model: Optional[str] = Field(default=os.getenv("GEMINI_MODEL", None))
    
    # Host settings
    web_host: Optional[str] = Field(default=os.getenv("WEB_HOST", None))
    public_host: Optional[str] = Field(default=os.getenv("PUBLIC_HOST", None))
    flutter_web_port: Optional[str] = Field(default=os.getenv("FLUTTER_WEB_PORT", None))
    web_port: Optional[str] = Field(default=os.getenv("WEB_PORT", None))
    api_port: Optional[str] = Field(default=os.getenv("API_PORT", None))
    
    # Timeout settings
    command_timeout: Optional[str] = Field(default=os.getenv("COMMAND_TIMEOUT", None))
    build_timeout: Optional[str] = Field(default=os.getenv("BUILD_TIMEOUT", None))
    
    # AI API keys
    anthropic_api_key: Optional[str] = Field(default=os.getenv("ANTHROPIC_API_KEY", None))
    openai_api_key: Optional[str] = Field(default=os.getenv("OPENAI_API_KEY", None))

    class Config:
        env_file = ".env"
        extra = "ignore"  # Allows extra fields in the settings

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings: Application settings
    """
    return Settings() 