"""
GitHub integration service.
"""
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime, timedelta
import asyncio

from api.infrastructure.database import get_supabase_client
from api.infrastructure.auth.jwt import user_to_dict
from api.domain.github.models import GitHubToken, GitHubRepositoryImport


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
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub token storage HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub token storage failed: {str(e)}")


async def get_github_token(user_id: str) -> Optional[GitHubToken]:
    """
    Get a GitHub token for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        GitHubToken if found, None otherwise
        
    Raises:
        ValueError: If token retrieval fails
    """
    client = get_supabase_client()
    try:
        result = client.from_('github_tokens').select('*').eq('user_id', user_id).eq('is_active', True).execute()
        
        if not result or not result.data or len(result.data) == 0:
            return None
            
        return GitHubToken(**result.data[0])
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub token retrieval HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub token retrieval failed: {str(e)}")


async def delete_github_token(user_id: str) -> bool:
    """
    Delete a GitHub token for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        True if deleted, False otherwise
        
    Raises:
        ValueError: If token deletion fails
    """
    client = get_supabase_client()
    try:
        result = client.from_('github_tokens').delete().eq('user_id', user_id).execute()
        
        return result and result.data and len(result.data) > 0
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub token deletion HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub token deletion failed: {str(e)}")


async def list_github_repositories(access_token: str) -> List[Dict[str, Any]]:
    """
    List GitHub repositories for a user using their GitHub token.
    
    Args:
        access_token: GitHub access token
        
    Returns:
        List of repositories
        
    Raises:
        ValueError: If repository listing fails
    """
    try:
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/user/repos', headers=headers)
            response.raise_for_status()
            
            repos = response.json()
            return repos
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub repository listing HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub repository listing failed: {str(e)}")


async def import_github_repository(user_id: str, repo_import: GitHubRepositoryImport) -> Dict[str, Any]:
    """
    Import a GitHub repository.
    
    Args:
        user_id: User ID
        repo_import: Repository import data
        
    Returns:
        Dict containing import status
        
    Raises:
        ValueError: If repository import fails
    """
    client = get_supabase_client()
    try:
        # Get GitHub token
        token = await get_github_token(user_id)
        if not token:
            raise ValueError("No GitHub token found for user")
        
        # Get repository details from GitHub
        headers = {
            'Authorization': f'token {token.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(f'https://api.github.com/repos/{repo_import.repo_full_name}', headers=headers)
            response.raise_for_status()
            
            repo_data = response.json()
        
        # Prepare repository record
        repo_insert = {
            'user_id': user_id,
            'project_id': repo_import.project_id,
            'repo_name': repo_data['name'],
            'repo_full_name': repo_data['full_name'],
            'repo_url': repo_data['html_url'],
            'default_branch': repo_data['default_branch'],
            'selected_branch': repo_import.branch or repo_data['default_branch'],
            'clone_url': repo_data['clone_url'],
            'selected_path': repo_import.path,
            'status': 'pending',
            'metadata': {
                'github_id': repo_data['id'],
                'description': repo_data['description'],
                'language': repo_data['language'],
                'private': repo_data['private'],
                'fork': repo_data['fork'],
                'created_at': repo_data['created_at'],
                'updated_at': repo_data['updated_at'],
                'pushed_at': repo_data['pushed_at']
            }
        }
        
        # Insert repository
        result = client.from_('github_repositories').insert(repo_insert).execute()
        
        if not result or not result.data or len(result.data) == 0:
            raise ValueError(f"Failed to import GitHub repository {repo_import.repo_full_name}")
            
        imported_repo = result.data[0]
        repository_id = imported_repo['id']
        
        # Start repository processing in the background
        from api.infrastructure.github.repository_manager import GitHubRepositoryManager
        
        # Start the repository processing task in the background
        asyncio.create_task(
            GitHubRepositoryManager().process_repository(repository_id, user_id)
        )
        
        return {
            'repository_id': repository_id,
            'status': 'pending',
            'message': f'Repository {repo_import.repo_full_name} import initiated'
        }
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub repository import HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub repository import failed: {str(e)}")


async def get_repository_status(user_id: str, repository_id: str) -> Dict[str, Any]:
    """
    Get the status of a GitHub repository import.
    
    Args:
        user_id: User ID
        repository_id: Repository ID
        
    Returns:
        Dict containing repository status
        
    Raises:
        ValueError: If repository status retrieval fails
    """
    client = get_supabase_client()
    try:
        result = client.from_('github_repositories').select('*').eq('id', repository_id).eq('user_id', user_id).execute()
        
        if not result or not result.data or len(result.data) == 0:
            raise ValueError(f"Repository {repository_id} not found")
            
        return result.data[0]
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub repository status HTTP error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub repository status retrieval failed: {str(e)}") 