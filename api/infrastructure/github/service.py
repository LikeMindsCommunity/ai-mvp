"""
GitHub App integration service.
Handles GitHub App installation, token management, and repository operations.
"""
from typing import Dict, Any, List, Optional
import jwt
import time
import httpx
import subprocess
from datetime import datetime, timedelta, timezone
import os

from api.config import get_settings
from api.infrastructure.database import get_supabase_client

settings = get_settings()

# GitHub API endpoints
GITHUB_API_URL = "https://api.github.com"
GITHUB_APP_INSTALLATIONS_URL = f"{GITHUB_API_URL}/app/installations"

async def generate_jwt() -> str:
    """
    Generate a JWT for GitHub App authentication.
    
    Returns:
        str: JWT token for GitHub App
    
    Raises:
        ValueError: If GitHub App credentials are missing
    """
    app_id = settings.github_app_id
    private_key = settings.github_app_private_key
    
    if not app_id:
        raise ValueError("GitHub App ID not configured")
    
    if not private_key:
        raise ValueError("GitHub App private key not configured")
    
    # Try to use the file directly if the key loading failed
    if private_key and "BEGIN RSA PRIVATE KEY" not in private_key:
        key_path = settings.github_app_private_key_path
        if key_path and os.path.exists(key_path):
            try:
                with open(key_path, "r") as f:
                    private_key = f.read().strip()
            except Exception as e:
                raise ValueError(f"Failed to read private key from file: {e}")
    
    try:
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + (10 * 60),  # 10 minutes expiration
            "iss": app_id
        }
        
        token = jwt.encode(
            payload,
            private_key,
            algorithm="RS256"
        )
        
        return token
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"JWT generation failed: {error_details}")
        
        # Try to inspect the key for common problems
        if private_key:
            key_preview = private_key[:50] + "..." if len(private_key) > 50 else private_key
            print(f"Key preview: {key_preview}")
            
        raise ValueError(f"Failed to generate GitHub App JWT: {str(e)}")

async def get_installation_url(user_id: str, redirect_url: Optional[str] = None) -> str:
    """
    Get the GitHub App installation URL for a user.
    
    Args:
        user_id: User ID to associate with installation
        redirect_url: Optional URL to redirect to after installation
        
    Returns:
        str: GitHub App installation URL
        
    Raises:
        ValueError: If GitHub App is not configured
    """
    slug = settings.github_app_slug
    if not slug:
        raise ValueError("GitHub App slug not configured - check GITHUB_APP_NAME or GITHUB_APP_SLUG settings")
    
    url = f"https://github.com/apps/{slug}/installations/new"
    
    # Add redirect URL if provided
    if redirect_url:
        url += f"?redirect_uri={redirect_url}"
    
    return url

async def exchange_installation_token(installation_id: int) -> Dict[str, Any]:
    """
    Exchange an installation ID for an access token.
    
    Args:
        installation_id: GitHub App installation ID
        
    Returns:
        Dict containing token data:
        {
            "token": str,
            "expires_at": str (ISO format),
            "refresh_at": str (ISO format)
        }
        
    Raises:
        ValueError: If token exchange fails
    """
    jwt_token = await generate_jwt()
    
    url = f"{GITHUB_API_URL}/app/installations/{installation_id}/access_tokens"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {jwt_token}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            expires_at = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
            refresh_at = expires_at - timedelta(minutes=10)  # Refresh 10 minutes before expiry
            
            return {
                "token": data["token"],
                "expires_at": expires_at.isoformat(),
                "refresh_at": refresh_at.isoformat()
            }
        except httpx.HTTPError as e:
            raise ValueError(f"Failed to exchange installation token: {str(e)}")

async def store_installation_token(
    user_id: str,
    installation_id: int,
    token_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Store or update a GitHub installation token.
    
    Args:
        user_id: User ID
        installation_id: GitHub installation ID
        token_data: Token data from exchange_installation_token()
        
    Returns:
        Dict containing stored token data
        
    Raises:
        ValueError: If token storage fails
    """
    client = get_supabase_client()
    
    try:
        # Upsert the token record
        data = {
            "user_id": user_id,
            "installation_id": installation_id,
            "access_token": token_data["token"],
            "expires_at": token_data["expires_at"],
            "refresh_at": token_data["refresh_at"]
        }
        
        result = client.from_("github_tokens")\
            .upsert(data, on_conflict="user_id,installation_id")\
            .execute()
            
        return result.data[0] if result.data else None
    except Exception as e:
        raise ValueError(f"Failed to store installation token: {str(e)}")

async def get_installation_token(user_id: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get a valid installation token for a user, refreshing if needed.
    
    Args:
        user_id: User ID
        force_refresh: Force token refresh even if it's not expired
        
    Returns:
        Dict containing token data or None if no token found
        
    Raises:
        ValueError: If token refresh fails
    """
    client = get_supabase_client()
    
    try:
        # Get the token record
        result = client.from_("github_tokens")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
            
        if not result.data:
            return None
            
        token = result.data[0]
        # Make sure we use timezone-aware datetime
        now = datetime.now(timezone.utc)
        refresh_at = datetime.fromisoformat(token["refresh_at"])
        
        # Check if token needs refresh or force refresh is requested
        if now >= refresh_at or force_refresh:
            # Get fresh token
            new_token = await exchange_installation_token(token["installation_id"])
            # Store it
            token = await store_installation_token(
                user_id,
                token["installation_id"],
                new_token
            )
        
        return token
    except Exception as e:
        raise ValueError(f"Failed to get installation token: {str(e)}")

async def list_repositories(user_id: str) -> List[Dict[str, Any]]:
    """
    List GitHub repositories available to a user's installation.
    
    Args:
        user_id: User ID
        
    Returns:
        List of repository data
        
    Raises:
        ValueError: If repository listing fails
    """
    try:
        # First attempt with existing token
        token = await get_installation_token(user_id)
        if not token:
            raise ValueError("No GitHub installation found")
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token['access_token']}"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # Get repositories
                response = await client.get(
                    f"{GITHUB_API_URL}/installation/repositories",
                    headers=headers
                )
                response.raise_for_status()
                repos = response.json()["repositories"]
                
                # Return the repositories list without storing in the database
                return repos
            except httpx.HTTPStatusError as e:
                # If we get a 401 Unauthorized, try refreshing the token and retry once
                if e.response.status_code == 401:
                    # Force refresh token
                    token = await get_installation_token(user_id, force_refresh=True)
                    if not token:
                        raise ValueError("No GitHub installation found")
                    
                    headers = {
                        "Accept": "application/vnd.github.v3+json",
                        "Authorization": f"token {token['access_token']}"
                    }
                    
                    # Retry with new token
                    response = await client.get(
                        f"{GITHUB_API_URL}/installation/repositories",
                        headers=headers
                    )
                    response.raise_for_status()
                    repos = response.json()["repositories"]
                    return repos
                else:
                    raise ValueError(f"Failed to list repositories: {str(e)}")
            except httpx.HTTPError as e:
                raise ValueError(f"Failed to list repositories: {str(e)}")
    except ValueError as e:
        # Re-raise with original message
        raise ValueError(str(e))
    except Exception as e:
        # Handle other exceptions
        raise ValueError(f"Failed to list repositories: {str(e)}")

async def store_repository(user_id: str, repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store a GitHub repository in the database after successful cloning.
    
    Args:
        user_id: User ID
        repo_data: Repository data from GitHub API
        
    Returns:
        Stored repository data
        
    Raises:
        ValueError: If storage fails
    """
    token = await get_installation_token(user_id)
    if not token:
        raise ValueError("No GitHub installation found")
    
    try:
        # Store in our cache
        client = get_supabase_client()
        data = {
            "user_id": user_id,
            "installation_id": token["installation_id"],
            "repo_id": repo_data["id"],
            "name": repo_data["name"],
            "full_name": repo_data["full_name"],
            "clone_url": repo_data["clone_url"],
            "default_branch": repo_data["default_branch"],
            "private": repo_data["private"],
            "language": repo_data.get("language"),
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }
        
        result = client.from_("github_repositories")\
            .upsert(data, on_conflict="installation_id,repo_id")\
            .execute()
        
        return data
    except Exception as e:
        raise ValueError(f"Failed to store repository: {str(e)}")

async def get_repository(user_id: str, repo_id: int) -> Optional[Dict[str, Any]]:
    """
    Get details for a specific repository.
    
    Args:
        user_id: User ID
        repo_id: GitHub repository ID
        
    Returns:
        Dict containing repository data or None if not found
        
    Raises:
        ValueError: If repository fetch fails
    """
    client = get_supabase_client()
    
    try:
        result = client.from_("github_repositories")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("repo_id", repo_id)\
            .execute()
            
        return result.data[0] if result.data else None
    except Exception as e:
        raise ValueError(f"Failed to get repository: {str(e)}")

async def clone_repository(clone_url: str, destination_path: str, access_token: str, retry_on_401: bool = True) -> None:
    """
    Clone a GitHub repository to a local path.
    
    Args:
        clone_url: Repository clone URL
        destination_path: Local path to clone to
        access_token: GitHub access token
        retry_on_401: Whether to retry with a fresh token if we receive a 401 error
        
    Raises:
        ValueError: If cloning fails
    """
    # Insert access token into clone URL
    auth_url = clone_url.replace(
        "https://",
        f"https://x-access-token:{access_token}@"
    )
    
    # Define the integration directory within the project folder
    integration_path = os.path.join(destination_path, "integration")
    
    # Make sure the parent directory exists
    os.makedirs(os.path.dirname(integration_path), exist_ok=True)
    
    # Use git clone --depth 1 to get only latest commit
    try:
        # Clone the repository directly to the integration directory
        subprocess.run(
            ["git", "clone", "--depth", "1", auth_url, integration_path],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        
        # Check if the error is due to authentication failure
        if "Authentication failed" in error_message and retry_on_401:
            # The original URL and token can be extracted from the error message
            # or passed in separately if needed
            raise ValueError("TOKEN_EXPIRED")
        else:
            raise ValueError(f"Failed to clone repository: {error_message}") 