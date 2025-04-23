"""
GitHub integration API endpoints.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio

from api.infrastructure.auth import get_current_user
from api.domain.github.models import (
    GitHubToken, 
    GitHubAuthResponse,
    GitHubRepository, 
    GitHubRepositoryList,
    GitHubRepositoryImport,
    GitHubRepositoryImportResponse,
    GitHubRepositoryStatus
)
from api.infrastructure.auth.service import sign_in_with_github
from api.infrastructure.database import get_supabase_client
from api.infrastructure.github.service import (
    store_github_token, 
    get_github_token, 
    delete_github_token,
    list_github_repositories,
    import_github_repository,
    get_repository_status
)
from api.presentation.exceptions import APIException
from pydantic import BaseModel

router = APIRouter(prefix="/api/github", tags=["github"])

@router.post("/connect", response_model=GitHubAuthResponse)
async def connect_github_account():
    """
    Get the GitHub OAuth URL to connect a GitHub account.
    """
    try:
        result = await sign_in_with_github()
        return result
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub connection", e)


@router.get("/token", response_model=Optional[GitHubToken])
async def get_github_account(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the connected GitHub account for the current user.
    """
    try:
        user_id = current_user["id"]
        token = await get_github_token(user_id)
        return token
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub account retrieval", e)


@router.delete("/token", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_github_account(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Disconnect the GitHub account for the current user.
    """
    try:
        user_id = current_user["id"]
        success = await delete_github_token(user_id)
        
        if not success:
            APIException.raise_not_found("GitHub account not found")
            
        return None
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub account disconnection", e)


@router.get("/repositories", response_model=GitHubRepositoryList)
async def get_github_repositories(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    List GitHub repositories for the current user.
    """
    try:
        user_id = current_user["id"]
        token = await get_github_token(user_id)
        
        if not token:
            APIException.raise_not_found("No GitHub account connected")
            
        repositories = await list_github_repositories(token.access_token)
        return GitHubRepositoryList(repositories=repositories)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repositories listing", e)


@router.post("/repositories/import", response_model=GitHubRepositoryImportResponse)
async def import_repository(
    repo_import: GitHubRepositoryImport,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Import a GitHub repository for code generation.
    
    This either creates a standalone repository record or associates 
    it with an existing project based on the project_id parameter.
    """
    try:
        user_id = current_user["id"]
        
        # If project_id is specified, verify it exists and belongs to the user
        if repo_import.project_id:
            client = get_supabase_client()
            project_response = client.from_('projects').select('id').eq('id', repo_import.project_id).execute()
            
            if not project_response.data or len(project_response.data) == 0:
                APIException.raise_not_found(f"Project {repo_import.project_id} not found")
                
        result = await import_github_repository(user_id, repo_import)
        
        return GitHubRepositoryImportResponse(
            repository_id=result["repository_id"],
            status=result["status"],
            message=result["message"],
            project_id=repo_import.project_id
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository import", e)


@router.get("/repositories/{repository_id}/status", response_model=GitHubRepositoryStatus)
async def get_repository_import_status(
    repository_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get the status of a GitHub repository import.
    """
    try:
        user_id = current_user["id"]
        result = await get_repository_status(user_id, repository_id)
        
        # Check if codebase.txt exists
        has_codebase_summary = False
        if result["status"] == "ready" and result.get("selected_path") is not None:
            try:
                from api.infrastructure.github.repository_manager import GitHubRepositoryManager
                repo_manager = GitHubRepositoryManager()
                
                # Calculate repository path
                repo_dir = repo_manager.get_repository_path(repository_id)
                project_path = result.get("selected_path", "")
                
                if project_path:
                    project_dir = repo_dir / project_path
                else:
                    project_dir = repo_dir
                
                # Check if codebase.txt exists
                codebase_file = project_dir / "codebase.txt"
                has_codebase_summary = codebase_file.exists()
            except Exception:
                # If there's an error checking the file, assume it doesn't exist
                has_codebase_summary = False
        
        # Get flutter projects from metadata
        flutter_projects = []
        if result.get("metadata") and isinstance(result["metadata"], dict):
            flutter_projects = result["metadata"].get("flutter_projects", [])
        
        return GitHubRepositoryStatus(
            id=result["id"],
            repo_name=result["repo_name"],
            repo_full_name=result["repo_full_name"],
            status=result["status"],
            error_message=result.get("error_message"),
            created_at=result["created_at"],
            updated_at=result["updated_at"],
            last_synced_at=result.get("last_synced_at"),
            selected_branch=result.get("selected_branch"),
            selected_path=result.get("selected_path"),
            flutter_projects=flutter_projects,
            has_codebase_summary=has_codebase_summary
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository status retrieval", e)


@router.post("/repositories/{repository_id}/process", response_model=GitHubRepositoryImportResponse)
async def process_repository(
    repository_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Manually process a GitHub repository to clone it, scan for Flutter projects,
    and generate the codebase summary.
    """
    try:
        user_id = current_user["id"]
        
        # Verify the repository exists and belongs to the user
        result = await get_repository_status(user_id, repository_id)
        
        # Start repository processing
        from api.infrastructure.github.repository_manager import GitHubRepositoryManager
        
        # Start the repository processing task in the background
        asyncio.create_task(
            GitHubRepositoryManager().process_repository(repository_id, user_id)
        )
        
        return GitHubRepositoryImportResponse(
            repository_id=repository_id,
            status="processing",
            message=f"Repository {result['repo_full_name']} processing initiated"
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository processing", e)


class ProjectPathSelect(BaseModel):
    """Model for selecting a project path."""
    project_path: str

@router.post("/repositories/{repository_id}/select-path", response_model=GitHubRepositoryStatus)
async def select_project_path(
    repository_id: str,
    path_data: ProjectPathSelect,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Select a specific Flutter project path within a repository.
    This will update the repository and regenerate the codebase summary.
    """
    try:
        user_id = current_user["id"]
        
        # Verify the repository exists and belongs to the user
        result = await get_repository_status(user_id, repository_id)
        
        # Verify that the path exists in the Flutter projects list
        flutter_projects = []
        if result.get("metadata") and isinstance(result["metadata"], dict):
            flutter_projects = result["metadata"].get("flutter_projects", [])
        
        if path_data.project_path and path_data.project_path not in flutter_projects:
            APIException.raise_bad_request(f"Project path '{path_data.project_path}' not found in repository")
        
        # Update the selected path
        client = get_supabase_client()
        client.from_("github_repositories").update({
            "selected_path": path_data.project_path
        }).eq("id", repository_id).execute()
        
        # Generate a new codebase summary
        from api.infrastructure.github.repository_manager import GitHubRepositoryManager
        repo_manager = GitHubRepositoryManager()
        
        # Start the codebase summary generation in the background
        asyncio.create_task(
            repo_manager.generate_codebase_summary(repository_id, path_data.project_path)
        )
        
        # Get the updated repository status
        result = await get_repository_status(user_id, repository_id)
        
        # We need to update the result with the same format as the status endpoint
        return await get_repository_import_status(repository_id, current_user)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub project path selection", e)


class RepositoryUrlImport(BaseModel):
    """Model for importing a GitHub repository by URL."""
    repository_url: str
    project_id: Optional[str] = None

@router.post("/import-repository", response_model=GitHubRepositoryImportResponse)
async def import_repository_url(
    repo_data: RepositoryUrlImport,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Import a GitHub repository by URL for backward compatibility.
    This converts the URL into a GitHubRepositoryImport and calls the standard import endpoint.
    """
    try:
        # Convert repository URL to repository full name
        repo_full_name = repo_data.repository_url
        
        # Remove github.com prefix if present
        if repo_full_name.startswith("https://github.com/"):
            repo_full_name = repo_full_name[19:]  # Remove "https://github.com/"
        elif repo_full_name.startswith("http://github.com/"):
            repo_full_name = repo_full_name[18:]  # Remove "http://github.com/"
        
        # Remove .git suffix if present
        if repo_full_name.endswith(".git"):
            repo_full_name = repo_full_name[:-4]  # Remove ".git"
            
        # Create GitHubRepositoryImport
        repo_import = GitHubRepositoryImport(
            repo_full_name=repo_full_name,
            project_id=repo_data.project_id
        )
        
        # Call the standard import endpoint
        user_id = current_user["id"]
        result = await import_github_repository(user_id, repo_import)
        
        return GitHubRepositoryImportResponse(
            repository_id=result["repository_id"],
            status=result["status"],
            message=result["message"],
            project_id=repo_data.project_id
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository import", e) 