"""
GitHub integration domain models.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class GitHubTokenCreate(BaseModel):
    """GitHub token creation model."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    scope: Optional[str] = None
    expires_at: Optional[datetime] = None


class GitHubToken(BaseModel):
    """GitHub token response model."""
    id: str
    user_id: str
    token_type: str
    access_token: str
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True


class GitHubAuthResponse(BaseModel):
    """GitHub OAuth URL response."""
    provider: str
    url: HttpUrl


class GitHubRepository(BaseModel):
    """GitHub repository basic information."""
    name: str
    description: Optional[str] = None
    html_url: HttpUrl
    language: Optional[str] = None
    


class GitHubRepositoryList(BaseModel):
    """List of GitHub repositories."""
    repositories: List[GitHubRepository]


class GitHubRepositoryImport(BaseModel):
    """Model for importing a GitHub repository."""
    repo_full_name: str
    branch: Optional[str] = None
    project_id: Optional[str] = None
    path: Optional[str] = None


class GitHubRepositoryImportResponse(BaseModel):
    """Response after initiating a repository import."""
    repository_id: str
    status: str
    message: str
    project_id: Optional[str] = None


class GitHubRepositoryStatus(BaseModel):
    """Status of a GitHub repository import."""
    id: str
    repo_name: str
    repo_full_name: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_synced_at: Optional[datetime] = None
    selected_branch: Optional[str] = None
    selected_path: Optional[str] = None
    flutter_projects: Optional[List[str]] = None
    has_codebase_summary: Optional[bool] = None 