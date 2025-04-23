"""
GitHub integration API endpoints.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
import asyncio
from fastapi.responses import RedirectResponse

from api.infrastructure.auth import get_current_user
from api.config import get_settings
from api.domain.github.models import (
    GitHubToken, 
    GitHubAuthResponse,
    GitHubRepository, 
    GitHubRepositoryList,
    GitHubRepositoryImport,
    GitHubRepositoryImportResponse,
    GitHubRepositoryStatus,
    GitHubAppAuthUrl,
    GitHubAppCallback,
    GitHubAppInstallation
)
from api.infrastructure.auth.service import sign_in_with_github
from api.infrastructure.database import get_supabase_client
from api.infrastructure.github.service import (
    store_github_token, 
    get_github_token, 
    delete_github_token,
    list_github_repositories,
    import_github_repository,
    get_repository_status,
    # GitHub App specific services
    get_github_app_installation_url,
    list_github_app_installations,
    get_installation_token,
    link_github_app_installation,
    get_user_installation,
    refresh_installation_token,
    unlink_github_app_installation
)
from api.presentation.exceptions import APIException
from pydantic import BaseModel

router = APIRouter(prefix="/api/github", tags=["github"])

# Legacy OAuth endpoint - replaced by GitHub App installation
# Keeping for backward compatibility but should point users to new flow
@router.post("/connect", response_model=GitHubAuthResponse, deprecated=True)
async def connect_github_account():
    """
    Deprecated: Get the GitHub OAuth URL to connect a GitHub account.
    Use /api/github/app/install instead for GitHub App installation flow.
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


@router.delete("/token", response_model=Dict[str, bool])
async def disconnect_github_account(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Disconnect a GitHub account (remove token).
    """
    try:
        user_id = current_user["id"]
        success = await delete_github_token(user_id)
        
        if not success:
            APIException.raise_not_found("GitHub account not found")
            
        return {"success": True}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub disconnection", e)


@router.get("/repositories", response_model=GitHubRepositoryList)
async def get_github_repositories(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get GitHub repositories for the current user.
    """
    try:
        user_id = current_user["id"]
        repo_list = await list_github_repositories(user_id)
        return GitHubRepositoryList(**repo_list)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repositories retrieval", e)


@router.post("/repositories/import", response_model=GitHubRepositoryImportResponse)
async def import_repository(
    import_data: GitHubRepositoryImport,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Import a GitHub repository for the current user.
    """
    try:
        user_id = current_user["id"]
        import_result = await import_github_repository(user_id, import_data)
        return GitHubRepositoryImportResponse(**import_result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository import", e)


@router.get("/repositories/{import_id}/status", response_model=GitHubRepositoryStatus)
async def get_import_status(
    import_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get the status of a GitHub repository import.
    """
    try:
        status = await get_repository_status(import_id)
        return GitHubRepositoryStatus(**status)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository status retrieval", e)


# GitHub App specific endpoints

@router.post("/app/install", response_model=GitHubAppAuthUrl)
async def install_github_app():
    """
    Get the URL to install the GitHub App.
    """
    try:
        result = await get_github_app_installation_url()
        return GitHubAppAuthUrl(**result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App installation URL", e)


@router.get("/app/callback")
async def github_app_callback(
    installation_id: Optional[int] = Query(None),
    setup_action: Optional[str] = Query(None),
    user_token: Optional[str] = Query(None)
):
    """
    Handle GitHub App installation callback.
    
    This endpoint will be called after a user installs the GitHub App.
    The installation_id will be linked to the current user.
    """
    try:
        # Validate parameters
        if not installation_id:
            APIException.raise_bad_request("Missing installation_id parameter")
        
        # Log the params received
        print(f"GitHub App callback received: installation_id={installation_id}, setup_action={setup_action}")
        
        settings = get_settings()
        frontend_url = settings.frontend_url
        
        # Redirect to the main integration tester page with installation parameters
        # The frontend will handle displaying the success notification and linking
        redirect_url = f"{frontend_url}?installation_id={installation_id}&setup_action={setup_action}"
        print(f"Redirecting to frontend: {redirect_url}")
        
        return RedirectResponse(url=redirect_url)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App callback", e)


@router.get("/app/installation", response_model=Dict[str, Any])
async def get_github_app_installation(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the GitHub App installation for the current user.
    """
    try:
        user_id = current_user["id"]
        installation = await get_user_installation(user_id)
        
        if not installation:
            return {"installed": False}
            
        return {"installed": True, "installation": installation}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App installation retrieval", e)


@router.post("/app/refresh-token", response_model=Optional[GitHubToken])
async def refresh_github_app_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Refresh the GitHub App installation token for the current user.
    """
    try:
        user_id = current_user["id"]
        token = await refresh_installation_token(user_id)
        
        if not token:
            APIException.raise_not_found("No GitHub App installation found")
            
        return token
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App token refresh", e)


@router.delete("/app/installation", response_model=Dict[str, bool])
async def uninstall_github_app(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Unlink the GitHub App installation from the current user.
    This doesn't uninstall the app from GitHub, just removes the link in our database.
    """
    try:
        user_id = current_user["id"]
        success = await unlink_github_app_installation(user_id)
        
        if not success:
            APIException.raise_not_found("No GitHub App installation found")
            
        return {"success": True}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App uninstallation", e)


@router.post("/app/link-installation", response_model=Dict[str, Any])
async def link_installation(
    installation_data: dict,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Link a GitHub App installation to the current user.
    
    This endpoint should be called by the frontend after the GitHub App installation
    is complete and the user is redirected back to the frontend.
    
    Request body:
    {
        "installation_id": int  # The GitHub App installation ID
    }
    """
    try:
        user_id = current_user["id"]
        
        # Extract installation_id from request body
        if "installation_id" not in installation_data:
            APIException.raise_bad_request("Missing installation_id in request body")
        
        installation_id = installation_data["installation_id"]
        if not isinstance(installation_id, int):
            try:
                installation_id = int(installation_id)
            except (ValueError, TypeError):
                APIException.raise_bad_request("installation_id must be an integer")
        
        # Link installation to user
        result = await link_github_app_installation(user_id, installation_id)
        
        return {"success": True, "installation": result}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App installation linking", e) 