from typing import Dict, Any, Optional
from api.infrastructure.database import get_supabase_client
import httpx

async def create_project(name: str, description: Optional[str] = None, jwt: str = None) -> Dict[str, Any]:
    """
    Create a new project.
    
    Args:
        name: Project name
        description: Project description (optional)
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
        
        # Create the project
        data = client.from_('projects').insert({
            'owner_id': user_id,
            'name': name,
            'description': description
        }).execute()
        
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project creation error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project creation failed: {str(e)}")

async def get_projects(jwt: str) -> Dict[str, Any]:
    """
    Get all projects for the authenticated user.
    
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
        
        # Query the projects for this user
        result = client.from_('projects').select('*').eq('owner_id', user_id).execute()
        return result
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project retrieval error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project retrieval failed: {str(e)}")

async def get_project(project_id: str, jwt: str) -> Dict[str, Any]:
    """
    Get a project by ID.
    
    Args:
        project_id: Project ID
        jwt: Supabase JWT token
        
    Returns:
        Dict containing project data
        
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
        
        # Query the project
        result = client.from_('projects').select('*').eq('id', project_id).eq('owner_id', user_id).execute()
        return result
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
        Dict containing updated project data
        
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
        
        # Check if user is owner
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return {"data": None}
        
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
        Dict containing deletion result
        
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
        
        # Check if user is owner
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return {"data": None}
        
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
        Dict containing sharing result
        
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
        
        # Check if current user is owner
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', owner_id).execute()
        if not owner_check.data:
            return {"data": None}
        
        # Get user ID from email
        user_result = client.from_('user_profiles').select('id').eq('email', user_email).execute()
        if not user_result.data:
            raise ValueError(f"User with email {user_email} not found")
        
        target_user_id = user_result.data[0]['id']
        
        # Check if already shared
        existing_check = client.from_('project_members').select('*').eq('project_id', project_id).eq('user_id', target_user_id).execute()
        
        if existing_check.data:
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
                'role': role
            }).execute()
        
        return result
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Project sharing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Project sharing failed: {str(e)}") 