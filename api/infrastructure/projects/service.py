from typing import Dict, Any, Optional, List
from api.infrastructure.database import get_supabase_client
import httpx
import os
import asyncio
from pathlib import Path

from api.domain.github.models import GitHubRepositoryImport
from api.infrastructure.github.service import get_github_token, import_github_repository

async def create_project(
    name: str, 
    description: Optional[str] = None, 
    github_repo: Optional[Dict[str, Any]] = None, 
    settings: Optional[Dict[str, Any]] = None,
    jwt: str = None
) -> Dict[str, Any]:
    """
    Create a new project, optionally with a GitHub repository.
    
    Args:
        name: Project name
        description: Project description (optional)
        github_repo: GitHub repository information (optional)
        settings: Project settings (optional)
        jwt: Supabase JWT token
        
    Returns:
        Dict containing project data
        
    Raises:
        ValueError: If project creation fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Create the project
        project_data = {
            'owner_id': user_id,
            'name': name,
            'description': description
        }
        
        if settings:
            project_data['settings'] = settings
            
        # Insert the project
        data = client.from_('projects').insert(project_data).execute()
        
        if not data or not data.data or len(data.data) == 0:
            raise ValueError("Failed to create project")
            
        project = data.data[0]
        project_id = project['id']
        
        # If a GitHub repository is specified, import it
        if github_repo:
            # Create a new project directory
            output_dir = Path(os.path.join(os.getcwd(), "output", project_id))
            os.makedirs(output_dir, exist_ok=True)
            
            # Import the GitHub repository
            repo_import = GitHubRepositoryImport(
                repo_full_name=github_repo.get('repo_full_name'),
                branch=github_repo.get('branch'),
                project_id=project_id,
                path=github_repo.get('path')
            )
            
            try:
                # Import the repository
                import_result = await import_github_repository(user_id, repo_import)
                
                # Update project with GitHub repository information
                github_info = {
                    'github_repo_id': import_result.get('repository_id'),
                    'github_repo_name': repo_import.repo_full_name,
                    'source_type': 'github'
                }
                
                # Update the project with GitHub info
                if settings:
                    settings.update(github_info)
                else:
                    settings = github_info
                    
                client.from_('projects').update({'settings': settings}).eq('id', project_id).execute()
                
                # Return the updated project data
                project['settings'] = settings
                
            except Exception as e:
                # Log the error but continue with project creation
                print(f"GitHub repository import failed: {str(e)}")
                # We don't want to fail project creation if GitHub import fails
                
        return data
        
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project creation error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project creation failed: {str(e)}")

async def get_projects(jwt: str) -> Dict[str, Any]:
    """
    Get all projects for the authenticated user.
    This includes:
    - Projects owned by the user
    - Projects where the user is a member
    
    Args:
        jwt: Supabase JWT token
        
    Returns:
        Dict containing projects data
        
    Raises:
        ValueError: If project retrieval fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Get all projects the user has access to (RLS will handle access control)
        result = client.from_('projects').select('*').execute()
        
        # Add is_owner flag to each project
        if result.data:
            for project in result.data:
                project['is_owner'] = project['owner_id'] == user_id
        
        return result
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project retrieval error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project retrieval failed: {str(e)}")

async def get_project(project_id: str, jwt: str) -> Dict[str, Any]:
    """
    Get a project by ID with member details.
    
    Args:
        project_id: Project ID
        jwt: Supabase JWT token
        
    Returns:
        Dict containing project data with member details or None if not found/no access
        
    Raises:
        ValueError: If project retrieval fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Get the project
        project_response = client.from_('projects').select('*').eq('id', project_id).single().execute()
        if not project_response.data:
            return None
            
        project_response.data['is_owner'] = project_response.data['owner_id'] == user_id
        return project_response
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project retrieval error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project retrieval failed: {str(e)}")

async def update_project(project_id: str, project_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
    """
    Update a project.
    
    Args:
        project_id: Project ID
        project_data: Project data to update
        jwt: Supabase JWT token
        
    Returns:
        Dict containing updated project data or None if not found/no access
        
    Raises:
        ValueError: If project update fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Check if user is owner
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return None
        
        # Update the project
        result = client.from_('projects').update(project_data).eq('id', project_id).execute()
        return result
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project update error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project update failed: {str(e)}")

async def delete_project(project_id: str, jwt: str) -> Dict[str, Any]:
    """
    Delete a project.
    
    Args:
        project_id: Project ID
        jwt: Supabase JWT token
        
    Returns:
        Dict containing deletion result or None if not found/no access
        
    Raises:
        ValueError: If project deletion fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Check if user is owner
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return None
        
        # Delete the project
        result = client.from_('projects').delete().eq('id', project_id).execute()
        return result
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project deletion error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project deletion failed: {str(e)}")

async def share_project(project_id: str, user_email: str, role: str, jwt: str) -> Dict[str, Any]:
    """
    Share a project with another user.
    
    Args:
        project_id: Project ID
        user_email: Email of user to share with
        role: Role to assign (viewer, editor, admin)
        jwt: Supabase JWT token
        
    Returns:
        Dict containing sharing result or None if not found/no access
        
    Raises:
        ValueError: If project sharing fails
    """
    client = get_supabase_client()
    try:
        # Validate token and get user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        owner_id = user_response.user.id
        
        # Explicitly set the auth header with JWT
        client.postgrest.auth(jwt)
        
        # Check if current user is owner
        project_response = client.from_('projects').select('*').eq('id', project_id).execute()
        if not project_response.data or len(project_response.data) == 0:
            return None
            
        project = project_response.data[0]
        if project['owner_id'] != owner_id:
            return None
        
        # Get user ID from email
        user_response = client.from_('user_profiles').select('id').eq('email', user_email).execute()
        if not user_response.data or len(user_response.data) == 0:
            raise ValueError(f"User with email {user_email} not found")
        
        target_user_id = user_response.data[0]['id']
        
        # Don't allow sharing with self
        if target_user_id == owner_id:
            raise ValueError("Cannot share project with yourself")
        
        # Check if already shared
        existing_response = client.from_('project_members').select('*').eq('project_id', project_id).eq('user_id', target_user_id).execute()
        
        try:
            if existing_response.data and len(existing_response.data) > 0:
                # Update existing share
                result = client.from_('project_members').update({
                    'role': role,
                    'updated_at': 'now()'
                }).eq('project_id', project_id).eq('user_id', target_user_id).execute()
            else:
                # Add new share
                result = client.from_('project_members').insert({
                    'project_id': project_id,
                    'user_id': target_user_id,
                    'role': role,
                    'created_by': owner_id
                }).execute()
            return result
        except Exception as e:
            raise ValueError(f"Failed to update project members: {str(e)}")
            
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project sharing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project sharing failed: {str(e)}") 