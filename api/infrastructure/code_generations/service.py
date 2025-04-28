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
        insert_result = client.from_('code_generations')\
            .insert({
                'project_id': project_id,
                'user_id': user_id,
                'prompt': prompt,
                'status': 'pending'
            })\
            .execute()

        if not insert_result or not insert_result.data or len(insert_result.data) == 0:
            raise ValueError("Failed to insert code generation record")

        generation_id = insert_result.data[0]['id']

        # Fetch the inserted row with all columns
        data = client.from_('code_generations')\
            .select('id, project_id, user_id, prompt, ai_response, code_content, conversation, status, output_path, web_url, created_at, updated_at')\
            .eq('id', generation_id)\
            .single()\
            .execute()
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
        update_result = client.from_('code_generations')\
            .update(update_data)\
            .eq('id', generation_id)\
            .execute()
        
        if not update_result or not update_result.data or len(update_result.data) == 0:
            raise ValueError("Failed to update code generation record")
        
        # Fetch the updated row with all columns
        data = client.from_('code_generations')\
            .select('id, project_id, user_id, prompt, ai_response, code_content, conversation, status, output_path, web_url, created_at, updated_at')\
            .eq('id', generation_id)\
            .single()\
            .execute()
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Code generation update error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Code generation update failed: {str(e)}")

async def get_project_conversations(project_id: str, jwt: str) -> Dict[str, Any]:
    """
    Get all code generations for a project ordered by created time.
    
    Args:
        project_id: Project ID
        jwt: User JWT token
        
    Returns:
        Dict containing conversation history for the project
        
    Raises:
        ValueError: If fetching conversations fails
    """
    client = get_supabase_client()
    try:
        # Validate token and set the session
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get all code generations for this project ordered by created_at
        data = client.from_('code_generations')\
            .select('id, project_id, user_id, prompt, ai_response, code_content, conversation, status, output_path, web_url, created_at, updated_at')\
            .eq('project_id', project_id)\
            .order('created_at', desc=False)\
            .execute()
            
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Fetching project conversations error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Fetching project conversations failed: {str(e)}")

async def get_generation_by_id(generation_id: str, jwt: str) -> Dict[str, Any]:
    """
    Get a code generation by ID.
    
    Args:
        generation_id: Generation ID
        jwt: User JWT token
        
    Returns:
        Dict containing code generation data
        
    Raises:
        ValueError: If fetching fails
    """
    client = get_supabase_client()
    try:
        # Validate token and set the session
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get the generation by ID
        data = client.from_('code_generations')\
            .select('id, project_id, user_id, prompt, ai_response, code_content, conversation, status, output_path, web_url, created_at, updated_at')\
            .eq('id', generation_id)\
            .single()\
            .execute()
            
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Fetching generation error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Fetching generation failed: {str(e)}")

async def get_pending_generation(project_id: str, jwt: str) -> Dict[str, Any]:
    """
    Get the most recent pending generation for a project.
    
    Args:
        project_id: Project ID
        jwt: User JWT token
        
    Returns:
        Dict containing the pending generation or None if no pending generation exists
        
    Raises:
        ValueError: If fetching fails
    """
    client = get_supabase_client()
    try:
        # Validate token and set the session
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get the most recent pending generation for this project
        data = client.from_('code_generations')\
            .select('id, project_id, user_id, prompt, ai_response, code_content, conversation, status, output_path, web_url, created_at, updated_at')\
            .eq('project_id', project_id)\
            .eq('status', 'pending')\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
            
        if not data or not data.data or len(data.data) == 0:
            return None
            
        # Return the first (and only) result with proper data access
        return {
            "data": data.data[0]  # Access the first element of the data list
        }
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Fetching pending generation error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Fetching pending generation failed: {str(e)}") 