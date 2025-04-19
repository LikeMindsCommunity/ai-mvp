from typing import Dict, Any, Optional
from api.infrastructure.database import get_supabase_client
import httpx
from fastapi import HTTPException

def user_to_dict(user) -> Dict[str, Any]:
    """Convert Supabase User object to dictionary."""
    if hasattr(user, 'model_dump'):
        # Pydantic v2 model
        return user.model_dump()
    elif hasattr(user, 'dict'):
        # Pydantic v1 model
        return user.dict()
    elif hasattr(user, '__dict__'):
        # Regular Python object
        return vars(user)
    else:
        # Fallback
        return {
            "id": getattr(user, "id", None),
            "email": getattr(user, "email", None),
            "app_metadata": getattr(user, "app_metadata", None),
            "user_metadata": getattr(user, "user_metadata", None),
            "created_at": getattr(user, "created_at", None),
        } 

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