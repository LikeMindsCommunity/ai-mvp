"""
Configuration settings for the application.
Loads environment variables and provides a centralized configuration.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Application settings
    PORT: int = Field(8000, env="PORT")
    DEBUG: bool = Field(False, env="DEBUG")
    ENVIRONMENT: str = Field("production", env="ENVIRONMENT")
    
    # Database connections
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    RABBITMQ_URL: str = Field(..., env="RABBITMQ_URL")
    
    # ChromaDB settings
    CHROMADB_HOST: str = Field("localhost", env="CHROMADB_HOST")
    CHROMADB_PORT: int = Field(8000, env="CHROMADB_PORT")
    
    # MinIO settings
    MINIO_ENDPOINT: str = Field(..., env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(..., env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field(..., env="MINIO_SECRET_KEY")
    MINIO_SECURE: bool = Field(False, env="MINIO_SECURE")
    
    # API keys
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Observability
    HELICONE_API_KEY: Optional[str] = Field(None, env="HELICONE_API_KEY")
    HELICONE_BASE_URL: str = Field("https://api.helicone.ai", env="HELICONE_BASE_URL")
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Set OpenAI API key as environment variable (for libraries that use it directly)
if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# Set Anthropic API key as environment variable (for libraries that use it directly)
if settings.ANTHROPIC_API_KEY:
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY 