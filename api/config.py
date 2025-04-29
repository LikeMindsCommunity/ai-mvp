"""
Configuration module for the API.
"""
import os
import re
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
    
    # GitHub App settings
    github_app_id: str = Field(default=os.getenv("GITHUB_APP_ID", ""))
    github_app_name: str = Field(default=os.getenv("GITHUB_APP_NAME", ""))
    github_app_client_id: str = Field(default=os.getenv("GITHUB_APP_CLIENT_ID", ""))
    github_app_client_secret: str = Field(default=os.getenv("GITHUB_APP_CLIENT_SECRET", ""))
    github_app_private_key_path: str = Field(default=os.getenv("GITHUB_APP_PRIVATE_KEY_PATH", ""))
    # Define private key as a field with exclude=True to avoid serialization issues
    github_app_private_key: Optional[str] = Field(default=None, exclude=True)
    
    # Use app name as the slug by default
    @property
    def github_app_slug(self) -> str:
        """Get GitHub App slug from name or environment variable."""
        env_slug = os.getenv("GITHUB_APP_SLUG", "")
        if env_slug:
            return env_slug
        # Convert app name to slug format (lowercase, dashes instead of spaces)
        if self.github_app_name:
            return self.github_app_name.lower().replace(" ", "-")
        return ""
    
    def model_post_init(self, __context) -> None:
        """Initialize fields after model creation."""
        # Handle GitHub private key after initialization
        if not self.github_app_private_key:
            # Priority 1: Use the file if it exists
            if self.github_app_private_key_path and os.path.exists(self.github_app_private_key_path):
                try:
                    with open(self.github_app_private_key_path, "r") as f:
                        key_content = f.read().strip()
                        self.github_app_private_key = self._ensure_pem_format(key_content)
                        # Successfully loaded from file
                        return
                except Exception as e:
                    print(f"Warning: Failed to read private key from file: {e}")
            
            # Priority 2: Use environment variable
            env_key = os.getenv("GITHUB_APP_PRIVATE_KEY", "")
            if env_key:
                # Clean up the key - remove quotes and handle escaped newlines
                cleaned_key = self._clean_private_key(env_key)
                self.github_app_private_key = self._ensure_pem_format(cleaned_key)
    
    def _clean_private_key(self, key: str) -> str:
        """Clean private key from environment variable format."""
        # Remove surrounding quotes if present
        key = key.strip()
        if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
            key = key[1:-1]
        
        # Handle literal \n in the string by replacing with actual newlines
        key = key.replace('\\n', '\n')
        
        # Remove any BEGIN/END lines so we can standardize the format
        key = re.sub(r'-----BEGIN.*?-----', '', key)
        key = re.sub(r'-----END.*?-----', '', key)
        
        # Remove excess whitespace
        key = key.strip()
        
        return key
    
    def _ensure_pem_format(self, key: str) -> str:
        """Ensure the key is in valid PEM format."""
        # First clean up the key
        key = self._clean_private_key(key)
        
        # Add proper BEGIN/END tags if they're missing
        if not key.startswith("-----BEGIN"):
            key = "-----BEGIN RSA PRIVATE KEY-----\n" + key + "\n-----END RSA PRIVATE KEY-----"
        
        return key

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