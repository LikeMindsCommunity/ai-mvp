from typing import Dict, Any
from api.infrastructure.database import get_supabase_client
import httpx

async def get_profile(jwt: str) -> Dict[str, Any]:
    """
    Get the current user's profile from Supabase.
    
    Args:
        jwt: Supabase JWT token
        
    Returns:
        Dict containing profile data
        
    Raises:
        ValueError: If profile retrieval fails
    """
    client = get_supabase_client()
    try:
        # First validate the token by getting the user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # No need to set the session, just pass the access token with the request
        # Get user ID from the authenticated user
        user_id = user_response.user.id
            
        # Query the profiles table directly with the access token in Authorization header
        data = client.from_('user_profiles').select('*').eq('id', user_id).single().execute()
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Profile retrieval error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Profile retrieval failed: {str(e)}")

async def update_profile(profile_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
    """
    Update the current user's profile in Supabase.
    
    Args:
        profile_data: Profile data to update
        jwt: Supabase JWT token
        
    Returns:
        Dict containing updated profile data
        
    Raises:
        ValueError: If profile update fails
    """
    client = get_supabase_client()
    try:
        # First validate the token by getting the user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Get user ID from the authenticated user
        user_id = user_response.user.id
        
        # First verify we can read the profile
        current_profile = client.from_('user_profiles') \
            .select('*') \
            .eq('id', user_id) \
            .single() \
            .execute()
            
        if not current_profile or not current_profile.data:
            raise ValueError(f"Profile not found for user ID: {user_id}")
        
        # Add updated_at timestamp
        profile_data['updated_at'] = 'now()'
        
        # Set the auth header explicitly
        client.postgrest.auth(jwt)
        
        # Update the profile - RLS policy will ensure we can only update our own profile
        update_result = client.from_('user_profiles') \
            .update(profile_data) \
            .eq('id', user_id) \
            .execute()
            
        if not update_result or not update_result.data or len(update_result.data) == 0:
            raise ValueError(f"Update failed for user ID: {user_id}. Please check RLS policies.")
            
        # The updated profile is in update_result.data[0] since update returns an array
        profile = update_result.data[0]
        
        # Handle null avatar_url
        if 'avatar_url' in profile and profile['avatar_url'] is None:
            profile['avatar_url'] = ""
            
        return update_result
            
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Profile update error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Profile update failed: {str(e)}")
