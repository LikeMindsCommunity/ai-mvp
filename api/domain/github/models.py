from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

class GitHubToken(BaseModel):
    """GitHub OAuth token model."""
    access_token: str
    token_type: str = "bearer"
    scope: Optional[str] = None
    expires_at: Optional[datetime] = None

class GitHubAuthResponse(BaseModel):
    """GitHub OAuth authentication response."""
    provider: str = "github"
    url: str

class GitHubRepository(BaseModel):
    """GitHub repository model."""
    id: int
    name: str
    full_name: str
    private: bool
    description: Optional[str] = None
    html_url: HttpUrl
    default_branch: str
    
class GitHubRepositoryList(BaseModel):
    """List of GitHub repositories."""
    repositories: List[GitHubRepository]

class GitHubRepositoryImport(BaseModel):
    """GitHub repository import request."""
    repository_name: Optional[str] = None
    owner: Optional[str] = None
    name: Optional[str] = None
    branch: Optional[str] = "main" 
    target_path: Optional[str] = None
    project_id: Optional[str] = None
    
    def get_full_repo_name(self) -> str:
        """
        Get the full repository name in the format owner/name.
        If repository_name is provided, it's used directly.
        Otherwise, owner and name are combined.
        Raises ValueError if neither format is provided.
        """
        if self.repository_name:
            return self.repository_name
        elif self.owner and self.name:
            return f"{self.owner}/{self.name}"
        else:
            raise ValueError("Either repository_name or both owner and name must be provided")

class GitHubRepositoryImportResponse(BaseModel):
    """GitHub repository import response."""
    id: str
    repository_name: str
    status: str = "pending"
    message: Optional[str] = None

class GitHubRepositoryStatus(BaseModel):
    """GitHub repository status."""
    id: str
    repository_name: str
    status: str
    message: Optional[str] = None
    imported_at: Optional[datetime] = None
    
# GitHub App specific models
class GitHubAppInstallation(BaseModel):
    """GitHub App installation model."""
    id: int
    app_id: int
    account: Dict[str, Any]
    repository_selection: str
    access_tokens_url: str
    repositories_url: str
    html_url: str
    target_type: str
    created_at: datetime
    updated_at: datetime
    
class GitHubAppAuthUrl(BaseModel):
    """GitHub App installation URL model."""
    url: str
    
class GitHubAppCallback(BaseModel):
    """GitHub App callback parameters."""
    installation_id: Optional[int] = None
    setup_action: Optional[str] = None
    code: Optional[str] = None
    state: Optional[str] = None

class GitHubAppToken(BaseModel):
    """GitHub App installation token."""
    token: str
    expires_at: datetime
    installation_id: int 