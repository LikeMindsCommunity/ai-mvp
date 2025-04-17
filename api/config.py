"""
Configuration module for the API.
"""
import os
from typing import Optional
from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    # Base settings
    app_name: str = "Flutter Integration Assistant"
    debug: bool = Field(default=False)
    
    # Supabase configuration
    supabase_url: str = Field(...)
    supabase_anon_key: str = Field(...)
    
    # JWT settings
    jwt_secret: str = Field(...)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # Google AI settings
    google_api_key: Optional[str] = None
    
    class Config:
        """Configuration for settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"


class TokenPayload(BaseModel):
    """
    Token payload model.
    """
    sub: str
    exp: int


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings: Application settings
    """
    return Settings() 