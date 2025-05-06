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

async def refresh_token(refresh_token: str) -> Dict[str, Any]:
    """
    Refresh an authentication token.
    
    Args:
        refresh_token: The refresh token from previous authentication
        
    Returns:
        Dict containing new access token, refresh token, and user data
        
    Raises:
        ValueError: If token refresh fails
    """
    client = get_supabase_client()
    try:
        # Refresh the session
        data = client.auth.refresh_session(refresh_token)
        
        if not data or not data.session:
            raise ValueError("Failed to refresh token")
            
        # Convert user object to dictionary
        user_data = user_to_dict(data.user)
        
        return {
            "access_token": data.session.access_token,
            "refresh_token": data.session.refresh_token,
            "token_type": "bearer",
            "user": user_data
        }
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Token refresh error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Token refresh failed: {str(e)}")

async def request_password_reset(email: str) -> Dict[str, Any]:
    """
    Request a password reset email.
    
    Args:
        email: The user's email address
        
    Returns:
        Dict with a success message
        
    Raises:
        ValueError: If the password reset request fails
    """
    client = get_supabase_client()
    try:
        result = client.auth.reset_password_email(email)
        return {"message": "Password reset email sent successfully"}
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Password reset error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Password reset request failed: {str(e)}")

async def change_password(access_token: str, current_password: str, new_password: str) -> Dict[str, Any]:
    """
    Change a user's password.
    
    Args:
        access_token: The current access token
        current_password: The current password
        new_password: The new password
        
    Returns:
        Dict with a success message
        
    Raises:
        ValueError: If the password change fails
    """
    client = get_supabase_client()
    try:
        # First verify the token by getting the user
        user_response = client.auth.get_user(access_token)
        if not user_response or not user_response.user:
            raise ValueError("Invalid authentication token")
        
        # Update the password
        client.auth.update_user(
            {"password": new_password},
        )
        
        return {"message": "Password changed successfully"}
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Password change error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Password change failed: {str(e)}") 