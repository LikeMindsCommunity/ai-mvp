"""
GitHub integration service.
"""
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime, timedelta
import asyncio
import jwt as pyjwt
import time
import json
import os

from api.config import get_settings
from api.infrastructure.database import get_supabase_client
from api.infrastructure.auth.jwt import user_to_dict
from api.domain.github.models import (
    GitHubToken, 
    GitHubRepositoryImport,
    GitHubAppInstallation,
    GitHubAppToken
)

# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
GITHUB_APP_INSTALLATIONS_URL = f"{GITHUB_API_URL}/app/installations"
GITHUB_APP_URL = "https://github.com/apps"


async def store_github_token(user_id: str, token_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store a GitHub access token for a user.
    
    Args:
        user_id: User ID
        token_data: Token data including access_token, refresh_token, etc.
        
    Returns:
        Dict containing stored token data
        
    Raises:
        ValueError: If token storage fails
    """
    client = get_supabase_client()
    try:
        # Check if a token already exists for this user
        existing_token = client.from_('github_tokens').select('id').eq('user_id', user_id).execute()
        
        # Calculate expires_at if not provided
        if 'expires_in' in token_data and 'expires_at' not in token_data:
            expires_in = token_data.pop('expires_in', 0)
            if expires_in > 0:
                token_data['expires_at'] = (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat()
                
        # Prepare token data
        token_insert = {
            'user_id': user_id,
            'access_token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'token_type': token_data.get('token_type', 'bearer'),
            'scope': token_data.get('scope'),
            'expires_at': token_data.get('expires_at')
        }
        
        # Update or insert token
        if existing_token and existing_token.data and len(existing_token.data) > 0:
            # Update existing token
            token_id = existing_token.data[0]['id']
            result = client.from_('github_tokens').update(token_insert).eq('id', token_id).execute()
        else:
            # Insert new token
            result = client.from_('github_tokens').insert(token_insert).execute()
        
        if not result or not result.data or len(result.data) == 0:
            raise ValueError(f"Failed to store GitHub token for user {user_id}")
            
        return result.data[0]
    except Exception as e:
        raise ValueError(f"Error storing GitHub token: {str(e)}")


async def get_github_token(user_id: str) -> Optional[GitHubToken]:
    """
    Get the GitHub access token for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        GitHubToken or None if not found
        
    Raises:
        ValueError: If token retrieval fails
    """
    client = get_supabase_client()
    try:
        # Get token from database
        result = client.from_('github_tokens').select('*').eq('user_id', user_id).execute()
        
        if not result.data or len(result.data) == 0:
            return None
            
        token_data = result.data[0]
        
        # Parse expires_at to datetime if present
        # expires_at = None
        # if token_data.get('expires_at'):
        #     expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
        #     # Check if token is expired
        #     if expires_at <= datetime.now():
        #         # Token is expired, attempt to refresh it
        #         if token_data.get('refresh_token'):
        #             # TODO: Implement token refresh logic
        #             pass
        #         return None
                
        return GitHubToken(
            access_token=token_data['access_token'],
            token_type=token_data['token_type'],
            scope=token_data.get('scope'),
            # expires_at=expires_at  # Use the parsed datetime object instead of the string
        )
    except Exception as e:
        raise ValueError(f"Error retrieving GitHub token: {str(e)}")


async def delete_github_token(user_id: str) -> bool:
    """
    Delete the GitHub access token for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        True if deleted successfully, False if not found
        
    Raises:
        ValueError: If token deletion fails
    """
    client = get_supabase_client()
    try:
        # Delete token from database
        result = client.from_('github_tokens').delete().eq('user_id', user_id).execute()
        
        if not result.data or len(result.data) == 0:
            return False
            
        return True
    except Exception as e:
        raise ValueError(f"Error deleting GitHub token: {str(e)}")


async def list_github_repositories(user_id: str) -> Dict[str, Any]:
    """
    List GitHub repositories for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Dict containing repositories
        
    Raises:
        ValueError: If repository listing fails
    """
    token = await get_github_token(user_id)
    if not token:
        raise ValueError("GitHub token not found")
    
    # Also get installation if it exists
    installation = await get_user_installation(user_id)
        
    try:
        async with httpx.AsyncClient() as client:
            # GitHub App tokens use Bearer auth, regular OAuth tokens use token auth
            auth_header = f"Bearer {token.access_token}"
            
            # If this is a GitHub App token (from an installation), we need to use a different endpoint
            if installation:
                # First try to get installation repositories
                response = await client.get(
                    f"{GITHUB_API_URL}/installation/repositories",
                    headers={
                        "Authorization": auth_header,
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
            else:
                # For regular OAuth tokens, use the user/repos endpoint
                response = await client.get(
                    f"{GITHUB_API_URL}/user/repos",
                    headers={
                        "Authorization": auth_header,
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
            
            response.raise_for_status()
            
            # Parse repository data
            data = response.json()
            
            # For installation tokens, the response format is different
            if installation:
                repositories = data.get("repositories", [])
            else:
                repositories = data
            
            # Transform to our model format
            return {
                "repositories": [
                    {
                        "id": repo["id"],
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "private": repo["private"],
                        "description": repo["description"],
                        "html_url": repo["html_url"],
                        "default_branch": repo["default_branch"]
                    }
                    for repo in repositories
                ]
            }
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error listing GitHub repositories: {str(e)}")


async def import_github_repository(user_id: str, import_data: GitHubRepositoryImport) -> Dict[str, Any]:
    """
    Import a GitHub repository.
    
    Args:
        user_id: User ID
        import_data: Repository import data
        
    Returns:
        Dict containing import status
        
    Raises:
        ValueError: If repository import fails
    """
    # Get full repository name from either repository_name or owner/name combination
    try:
        print(f"Import request data: {import_data}")
        full_repo_name = import_data.get_full_repo_name()
        print(f"Full repo name: {full_repo_name}")
    except ValueError as e:
        print(f"Error getting repository name: {str(e)}")
        raise ValueError(str(e))
    
    token = await get_github_token(user_id)
    if not token:
        print(f"No GitHub token found for user {user_id}")
        raise ValueError("GitHub token not found")
    
    # Also get installation if it exists
    installation = await get_user_installation(user_id)
    print(f"User installation: {installation}")
        
    client = get_supabase_client()
    try:
        # GitHub App tokens always use Bearer auth
        auth_header = f"Bearer {token.access_token}"
        
        # Verify repository exists
        async with httpx.AsyncClient() as http_client:
            # Construct proper repository URL for GitHub App or OAuth tokens
            repo_url = f"{GITHUB_API_URL}/repos/{full_repo_name}"
            print(f"Checking repository at URL: {repo_url}")
            
            response = await http_client.get(
                repo_url,
                headers={
                    "Authorization": auth_header,
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            response.raise_for_status()
            repo_data = response.json()
            print(f"Repository exists: {repo_data['full_name']}, id: {repo_data['id']}")
            
        # Create repository record using github_repositories table
        repo_record = {
            "user_id": user_id,
            "repo_name": repo_data["name"],
            "repo_full_name": full_repo_name,
            "repo_url": repo_data["html_url"],
            "clone_url": repo_data["clone_url"],
            "default_branch": repo_data.get("default_branch", "main"),
            "selected_branch": import_data.branch,
            "selected_path": import_data.target_path,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Add installation_id if available
        if installation:
            repo_record["installation_id"] = str(installation["installation_id"])
            repo_record["auth_method"] = "app"
        else:
            repo_record["auth_method"] = "oauth"
        
        # Add project_id if provided and validate it
        if import_data.project_id:
            # Verify the project exists
            try:
                project_result = client.from_('projects').select('id').eq('id', import_data.project_id).execute()
                if not project_result.data or len(project_result.data) == 0:
                    raise ValueError(f"Project with ID {import_data.project_id} not found")
                
                repo_record["project_id"] = import_data.project_id
                print(f"Validated project ID: {import_data.project_id}")
            except Exception as e:
                print(f"Error validating project ID: {str(e)}")
                raise ValueError(f"Invalid project ID: {import_data.project_id}. {str(e)}")
        
        print(f"Creating repository record: {repo_record}")
        try:
            result = client.from_('github_repositories').insert(repo_record).execute()
            
            if not result.data or len(result.data) == 0:
                print("Failed to create repository record - no data returned from database")
                raise ValueError(f"Failed to create repository record")
                
            repo_id = result.data[0]["id"]
            print(f"Repository record created with ID: {repo_id}")
            
            # TODO: Queue background task to clone repository and process
            
            return {
                "id": repo_id,
                "repository_name": full_repo_name,
                "status": "pending",
                "message": "Repository import queued"
            }
        except Exception as e:
            error_detail = str(e)
            if hasattr(e, 'json') and callable(e.json):
                try:
                    error_json = e.json()
                    if error_json:
                        error_detail = f"Database error: {json.dumps(error_json)}"
                    else:
                        error_detail = "Database error: Empty response from API"
                except:
                    error_detail = f"Database error: Could not parse response"
            
            print(f"Error creating repository record: {error_detail}")
            # Check for foreign key violation, which could indicate the project_id reference issue
            if "projects" in error_detail and "violates foreign key constraint" in error_detail:
                raise ValueError(f"Invalid project ID or projects table does not exist. Please check that the projects table is properly created.")
            else:
                raise ValueError(f"Failed to create repository record: {error_detail}")
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code} for URL {e.request.url}: {e.response.text}"
        print(error_msg)
        if e.response.status_code == 404:
            raise ValueError(f"Repository {full_repo_name} not found")
        raise ValueError(f"GitHub API error: {error_msg}")
    except Exception as e:
        error_msg = f"Error importing GitHub repository: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        raise ValueError(error_msg)


async def get_repository_status(import_id: str) -> Dict[str, Any]:
    """
    Get the status of a GitHub repository import.
    
    Args:
        import_id: Repository ID
        
    Returns:
        Dict containing repository status
        
    Raises:
        ValueError: If status retrieval fails
    """
    client = get_supabase_client()
    try:
        # Get repository record
        result = client.from_('github_repositories').select('*').eq('id', import_id).execute()
        
        if not result.data or len(result.data) == 0:
            raise ValueError(f"Repository record {import_id} not found")
            
        repo_record = result.data[0]
        
        return {
            "id": repo_record["id"],
            "repository_name": repo_record["repo_full_name"],
            "status": repo_record["status"],
            "message": repo_record.get("error_message"),
            "last_synced_at": repo_record.get("last_synced_at")
        }
    except Exception as e:
        raise ValueError(f"Error retrieving repository status: {str(e)}")

# GitHub App specific methods

def _generate_github_app_jwt() -> str:
    """
    Generate a GitHub App JWT for API authentication.
    
    Returns:
        JWT token for GitHub App
    """
    settings = get_settings()
    
    # Current time and expiration time (10 minutes from now)
    now = int(time.time())
    payload = {
        "iat": now,  # Issued at time
        "exp": now + 600,  # Expiration time (10 minutes from now)
        "iss": settings.github_app_id  # GitHub App ID
    }
    
    # Create JWT token
    try:
        # Try to get private key from file if path is provided
        private_key = ""
        if settings.github_app_private_key_path and os.path.exists(settings.github_app_private_key_path):
            try:
                with open(settings.github_app_private_key_path, 'r') as key_file:
                    private_key = key_file.read()
                print(f"Loaded GitHub App private key from file: {settings.github_app_private_key_path}")
            except Exception as e:
                print(f"Error reading private key file: {str(e)}")
                
        # Fall back to environment variable if file reading failed or path is not provided
        if not private_key and settings.github_app_private_key:
            private_key = settings.github_app_private_key.replace('\\n', '\n')
            print("Using GitHub App private key from environment variable")
            
        if not private_key:
            raise ValueError("GitHub App private key not found - provide either GITHUB_APP_PRIVATE_KEY or GITHUB_APP_PRIVATE_KEY_PATH")
            
        encoded_jwt = pyjwt.encode(payload, private_key, algorithm="RS256")
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Error generating GitHub App JWT: {str(e)}")

async def get_github_app_installation_url() -> Dict[str, Any]:
    """
    Get the GitHub App installation URL.
    
    Returns:
        Dict containing the GitHub App installation URL
    """
    settings = get_settings()
    
    try:
        url = f"{GITHUB_APP_URL}/{settings.github_app_name}/installations/new"
        return {
            "url": url
        }
    except Exception as e:
        raise ValueError(f"Error generating GitHub App installation URL: {str(e)}")

async def list_github_app_installations() -> List[GitHubAppInstallation]:
    """
    List GitHub App installations.
    
    Returns:
        List of GitHub App installations
    """
    try:
        jwt_token = _generate_github_app_jwt()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GITHUB_APP_INSTALLATIONS_URL,
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            response.raise_for_status()
            installations = response.json()
            
            return [
                GitHubAppInstallation(
                    id=installation["id"],
                    app_id=installation["app_id"],
                    account=installation["account"],
                    repository_selection=installation["repository_selection"],
                    access_tokens_url=installation["access_tokens_url"],
                    repositories_url=installation["repositories_url"],
                    html_url=installation["html_url"],
                    target_type=installation["target_type"],
                    created_at=datetime.fromisoformat(installation["created_at"].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(installation["updated_at"].replace('Z', '+00:00'))
                )
                for installation in installations
            ]
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error listing GitHub App installations: {str(e)}")

async def get_installation_token(installation_id: int) -> GitHubAppToken:
    """
    Get an installation access token for a GitHub App installation.
    
    Args:
        installation_id: Installation ID
        
    Returns:
        Installation access token
    """
    try:
        jwt_token = _generate_github_app_jwt()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GITHUB_API_URL}/app/installations/{installation_id}/access_tokens",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            return GitHubAppToken(
                token=token_data["token"],
                expires_at=datetime.fromisoformat(token_data["expires_at"].replace('Z', '+00:00')),
                installation_id=installation_id
            )
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error getting installation token: {str(e)}")

async def link_github_app_installation(user_id: str, installation_id: int) -> Dict[str, Any]:
    """
    Link a GitHub App installation to a user.
    
    Args:
        user_id: User ID
        installation_id: GitHub App installation ID
        
    Returns:
        Dict containing the linked installation
    """
    client = get_supabase_client()
    try:
        # Get installation token to verify it's valid
        installation_token = await get_installation_token(installation_id)
        
        # Store installation data in database
        installation_data = {
            "user_id": user_id,
            "installation_id": installation_id
        }
        
        # Check if user already has an installation
        existing = client.from_('github_app_installations').select('id').eq('user_id', user_id).execute()
        
        if existing.data and len(existing.data) > 0:
            # Update existing installation
            result = client.from_('github_app_installations').update(installation_data).eq('user_id', user_id).execute()
        else:
            # Insert new installation - explicitly cast user_id to get past RLS
            result = client.from_('github_app_installations').insert(installation_data).execute()
        
        if not result.data or len(result.data) == 0:
            raise ValueError(f"Failed to link GitHub App installation")
            
        # Store access token in github_tokens table for compatibility with existing code
        token_data = {
            "access_token": installation_token.token,
            "token_type": "bearer",
            "scope": "repo",
            "expires_at": installation_token.expires_at.isoformat()
        }
        
        await store_github_token(user_id, token_data)
        
        return {
            "id": result.data[0]["id"],
            "user_id": user_id,
            "installation_id": installation_id,
            "created_at": result.data[0]["created_at"]
        }
    except Exception as e:
        raise ValueError(f"Error linking GitHub App installation: {str(e)}")

async def get_user_installation(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the GitHub App installation for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Dict containing the user's installation or None if not found
    """
    client = get_supabase_client()
    try:
        # Get installation from database
        result = client.from_('github_app_installations').select('*').eq('user_id', user_id).execute()
        
        if not result.data or len(result.data) == 0:
            return None
            
        return result.data[0]
    except Exception as e:
        raise ValueError(f"Error getting user installation: {str(e)}")

async def refresh_installation_token(user_id: str) -> Optional[GitHubToken]:
    """
    Refresh the GitHub App installation token for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Updated GitHubToken or None if no installation found
    """
    try:
        # Get user's installation
        installation = await get_user_installation(user_id)
        
        if not installation:
            return None
            
        # Get new installation token
        installation_token = await get_installation_token(installation["installation_id"])
        
        # Store token
        token_data = {
            "access_token": installation_token.token,
            "token_type": "bearer",
            "scope": "repo",
            "expires_at": installation_token.expires_at.isoformat()
        }
        
        await store_github_token(user_id, token_data)
        
        return GitHubToken(
            access_token=installation_token.token,
            token_type="bearer",
            scope="repo",
            expires_at=installation_token.expires_at
        )
    except Exception as e:
        raise ValueError(f"Error refreshing installation token: {str(e)}")

async def unlink_github_app_installation(user_id: str) -> bool:
    """
    Unlink a GitHub App installation from a user.
    
    Args:
        user_id: User ID
        
    Returns:
        True if unlinked successfully, False if no installation found
    """
    client = get_supabase_client()
    try:
        # Delete installation from database
        result = client.from_('github_app_installations').delete().eq('user_id', user_id).execute()
        
        if not result.data or len(result.data) == 0:
            return False
            
        # Also delete token
        await delete_github_token(user_id)
        
        return True
    except Exception as e:
        raise ValueError(f"Error unlinking GitHub App installation: {str(e)}") 