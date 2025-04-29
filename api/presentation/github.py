"""
GitHub App integration routes.
Handles installation, repository listing, and cloning endpoints.
"""
from typing import Dict, Any, List, Optional
import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Query

from api.infrastructure.auth import get_current_user
from api.infrastructure.github.service import (
    get_installation_url,
    exchange_installation_token,
    store_installation_token,
    list_repositories,
    get_repository,
    clone_repository,
    get_installation_token,
    store_repository
)

router = APIRouter(prefix="/api/github", tags=["github"])

@router.get("/install-url")
async def get_github_install_url(
    redirect_url: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """Get GitHub App installation URL if user hasn't installed yet."""
    try:
        url = await get_installation_url(current_user["id"], redirect_url)
        return {"install_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/installation-status")
async def check_installation_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Check if the user has a valid GitHub installation."""
    try:
        token = await get_installation_token(current_user["id"])
        if token:
            return {
                "has_installation": True,
                "installation_id": token["installation_id"]
            }
        return {"has_installation": False}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/callback")
async def github_callback(
    installation_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Handle GitHub App installation callback."""
    try:
        # Exchange installation ID for token
        token_data = await exchange_installation_token(installation_id)
        
        # Store token
        stored_token = await store_installation_token(
            current_user["id"],
            installation_id,
            token_data
        )
        
        return {"status": "success", "installation_id": installation_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/repositories")
async def list_github_repositories(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """List repositories available to the user's installation."""
    try:
        repos = await list_repositories(current_user["id"])
        return repos
    except ValueError as e:
        error_message = str(e)
        status_code = 400
        
        # Provide more specific error codes for different error types
        if "No GitHub installation found" in error_message:
            status_code = 404
            error_message = "No GitHub installation found. Please install the GitHub App first."
        elif "public key" in error_message.lower() or "private key" in error_message.lower():
            # Server configuration issue
            status_code = 500
            error_message = "Server configuration error: Invalid GitHub App private key. Please contact support."
        elif "token" in error_message.lower() and "expired" in error_message.lower():
            status_code = 401
            error_message = "GitHub token has expired. Please reinstall the GitHub App."
        
        raise HTTPException(status_code=status_code, detail=error_message)

@router.post("/clone")
async def clone_github_repository(
    repo_id: int,
    project_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Clone a GitHub repository and set it up as a project."""
    try:
        # Get fresh token for cloning
        token = await get_installation_token(current_user["id"])
        if not token:
            raise ValueError("No valid installation token found")
        
        # Get all repositories from GitHub (not from DB)
        all_repos = await list_repositories(current_user["id"])
        
        # Find the requested repository in the fetched list
        repo_data = next((repo for repo in all_repos if repo["id"] == repo_id), None)
        if not repo_data:
            raise ValueError("Repository not found in your GitHub installation")
            
        # Clone to project directory
        destination = f"output/{project_id}"
        try:
            await clone_repository(
                repo_data["clone_url"],
                destination,
                token["access_token"]
            )
        except ValueError as e:
            # Handle token expiration specially
            if str(e) == "TOKEN_EXPIRED":
                # Force refresh token and retry
                token = await get_installation_token(current_user["id"], force_refresh=True)
                if not token:
                    raise ValueError("Failed to refresh token")
                
                # Retry with new token
                await clone_repository(
                    repo_data["clone_url"],
                    destination,
                    token["access_token"],
                    retry_on_401=False  # Don't retry again to avoid infinite recursion
                )
            else:
                # Re-raise other errors
                raise
        
        # Store repository in database only after successful cloning
        stored_repo = await store_repository(current_user["id"], repo_data)
        
        return {
            "status": "success",
            "project_id": project_id,
            "repository": stored_repo
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
) -> Dict[str, Any]:
    """
    Handle GitHub webhook events.
    
    This endpoint receives webhook events from GitHub and processes them
    based on the event type.
    
    Currently supported events:
    - ping: Validate the webhook setup
    - push: Handle repository updates
    
    Headers:
    - X-GitHub-Event: Type of event (ping, push, etc.)
    """
    # Process based on event type
    if x_github_event == "ping":
        return {"status": "success", "message": "Webhook received successfully"}
    elif x_github_event == "push":
        # Handle repository updates
        payload = await request.json()
        
        # TODO: Implement logic to mark repositories as outdated
        # This could include:
        # 1. Extract repository info from payload
        # 2. Update github_repositories table to mark as outdated
        # 3. Notify users of updates via websocket or other mechanism
        
        return {"status": "success", "message": "Push event processed"}
    else:
        # Log but accept other events
        return {"status": "success", "message": f"Event {x_github_event} acknowledged but not processed"} 