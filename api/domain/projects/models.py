from typing import Dict, Any
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    """Project creation model."""
    name: str
    description: str = None

class ProjectUpdate(BaseModel):
    """Project update model."""
    name: str = None
    description: str = None
    settings: Dict[str, Any] = None

class ProjectShare(BaseModel):
    """Project sharing model."""
    user_email: str
    role: str = "viewer"  # Default role is viewer 