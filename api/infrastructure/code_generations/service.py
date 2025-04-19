from typing import Dict, Any
from api.infrastructure.database import get_supabase_client
import httpx

async def create_code_generation(project_id: str, prompt: str, jwt: str) -> Dict[str, Any]:
    """
    Create a new code generation record.
    
    Args:
        project_id: Project ID
        prompt: Generation prompt
        jwt: User JWT token
        
    Returns:
        Dict containing code generation data
        
    Raises:
        ValueError: If record creation fails
    """
    client = get_supabase_client()
    try:
        # Validate token and set the session
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # Create the code generation record
        data = client.from_('code_generations').insert({
            'project_id': project_id,
            'user_id': user_id,
            'prompt': prompt,
            'status': 'pending'
        }).execute()
        
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Code generation record creation error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Code generation record creation failed: {str(e)}")

async def update_code_generation(generation_id: str, update_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
    """
    Update a code generation record.
    
    Args:
        generation_id: Generation ID
        update_data: Data to update
        jwt: User JWT token
        
    Returns:
        Dict containing updated code generation data
        
    Raises:
        ValueError: If record update fails
    """
    client = get_supabase_client()
    try:
        # Validate token and set the session
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Update the code generation record
        data = client.from_('code_generations').update(update_data).eq('id', generation_id).execute()
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Code generation update error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Code generation update failed: {str(e)}") 