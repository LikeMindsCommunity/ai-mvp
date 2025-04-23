from typing import Dict, Any, Optional
from pydantic import BaseModel

class GitHubRepoInfo(BaseModel):
    """GitHub repository information for project creation."""
    repo_full_name: str
    branch: Optional[str] = None
    path: Optional[str] = None

class ProjectCreate(BaseModel):
    """Project creation model."""
    name: str
    description: Optional[str] = None
    github_repo: Optional[GitHubRepoInfo] = None
    settings: Optional[Dict[str, Any]] = None

class ProjectUpdate(BaseModel):
    """Project update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class ProjectShare(BaseModel):
    """Project sharing model."""
    user_email: str
    role: str = "viewer"  # Default role is viewer 