from typing import Dict, Any
from pydantic import BaseModel, HttpUrl

class ProfileUpdate(BaseModel):
    """Profile update model."""
    full_name: str = None
    avatar_url: str = None
    preferences: Dict[str, Any] = None 