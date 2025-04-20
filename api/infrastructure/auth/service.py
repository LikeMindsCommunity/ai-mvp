from typing import Dict, Any, Optional
import datetime
from api.infrastructure.database import get_supabase_client
import httpx
from fastapi import HTTPException
from api.config import get_settings

def user_to_dict(user) -> Dict[str, Any]:
    """Convert Supabase User object to dictionary and handle datetime objects."""
    result = {}
    
    if hasattr(user, 'model_dump'):
        # Pydantic v2 model
        result = user.model_dump()
    elif hasattr(user, 'dict'):
        # Pydantic v1 model
        result = user.dict()
    elif hasattr(user, '__dict__'):
        # Regular Python object
        result = vars(user)
    else:
        # Fallback
        result = {
            "id": getattr(user, "id", None),
            "email": getattr(user, "email", None),
            "app_metadata": getattr(user, "app_metadata", None),
            "user_metadata": getattr(user, "user_metadata", None),
            "created_at": getattr(user, "created_at", None),
        }
    
    # Convert datetime objects to ISO format strings
    for key, value in list(result.items()):
        if isinstance(value, datetime.datetime):
            result[key] = value.isoformat()
        elif isinstance(value, dict):
            # Recursively process nested dictionaries
            for nested_key, nested_value in list(value.items()):
                if isinstance(nested_value, datetime.datetime):
                    value[nested_key] = nested_value.isoformat()
    
    return result

def get_supabase_manager():
    return get_supabase_client()

async def sign_up(email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Sign up a new user.
    
    Args:
        email: User email
        password: User password
        user_metadata: Optional user metadata
        
    Returns:
        Dict containing user and session data
        
    Raises:
        ValueError: If sign up fails
    """
    client = get_supabase_client()
    try:
        data = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": user_metadata or {}
            }
        })
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Authentication error: {str(e)}")

async def sign_in(email: str, password: str) -> Dict[str, Any]:
    """
    Sign in an existing user.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        Dict containing user and session data
        
    Raises:
        ValueError: If sign in fails
    """
    client = get_supabase_client()
    try:
        data = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Authentication error: {str(e)}")

async def sign_out(jwt: str) -> None:
    """
    Sign out a user by invalidating their session.
    
    Args:
        jwt: Supabase JWT token
        
    Raises:
        ValueError: If authentication fails
    """
    client = get_supabase_client()
    try:
        # First validate the token by getting the user
        user_response = client.auth.get_user(jwt)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
            
        # Directly sign out without setting the session
        # NOTE: This might not invalidate the token server-side,
        # but it will clear the client-side session
        client.auth.sign_out()
    except HTTPException as e:
        raise ValueError(e.detail)
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Authentication error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Sign out error: {str(e)}")

async def sign_in_with_github() -> Dict[str, Any]:
    """
    Get the GitHub OAuth sign in URL.
    
    Returns:
        Dict containing the GitHub OAuth URL
        
    Raises:
        ValueError: If getting the URL fails
    """
    client = get_supabase_client()
    settings = get_settings()
    try:
        # Get the GitHub OAuth URL from Supabase
        response = client.auth.sign_in_with_oauth({
            "provider": "github",
            "options": {
                "redirect_to": f"{settings.api_url}/api/auth/github/callback"  # Redirect to our backend first
            }
        })
        # Convert the OAuthResponse to a dictionary
        return {
            "provider": response.provider,
            "url": response.url
        }
    except httpx.HTTPStatusError as e:
        raise ValueError(f"GitHub authentication error: {str(e)}")
    except Exception as e:
        raise ValueError(f"GitHub sign in failed: {str(e)}")

async def handle_github_callback(code: str) -> Dict[str, Any]:
    """
    Handle the GitHub OAuth callback.
    
    Args:
        code: The authorization code from GitHub
        
    Returns:
        Dict containing user and session data
        
    Raises:
        ValueError: If authentication fails
    """
    client = get_supabase_client()
    try:
        # Exchange the code for a session - note the parameter format
        print(f"Exchanging code for session: {code}")
        data = client.auth.exchange_code_for_session({
            "auth_code": code
        })
        
        print(f"Received session data type: {(data.model_dump_json())}")
        
        if not data:
            raise ValueError("No data returned from exchange_code_for_session")
            
        # Check session and user data
        has_session = hasattr(data, 'session') and data.session is not None
        has_user = hasattr(data, 'user') and data.user is not None
        
        if not has_session or not has_user:
            error_msg = f"Incomplete session data: has_session={has_session}, has_user={has_user}"
            print(error_msg)
            raise ValueError(error_msg)
        
        # Structure the response using our helper functions that handle datetime objects
        user_data = user_to_dict(data.user)
        
        return {
            "access_token": data.session.access_token,
            "token_type": "bearer",
            "user": user_data
        }
    except httpx.HTTPStatusError as e:
        error_msg = f"GitHub callback HTTP error: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"GitHub callback failed: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg) 