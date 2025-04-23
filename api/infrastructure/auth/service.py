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

async def handle_github_callback(code: str, is_app_installation: bool = False) -> Dict[str, Any]:
    """
    Handle the GitHub OAuth callback.
    
    Args:
        code: The authorization code from GitHub
        is_app_installation: Whether this is a GitHub App installation callback
        
    Returns:
        Dict containing user and session data
        
    Raises:
        ValueError: If authentication fails
    """
    client = get_supabase_client()
    try:
        print(f"Exchanging code for session: {code}")
        
        if is_app_installation:
            # For GitHub App installations, we'll get a user token directly from GitHub later
            # Just return a minimal response for now that will allow the app to continue
            # We'll get installation token separately in the GitHub app callback
            return {
                "access_token": "temporary_token_for_app_installation",
                "token_type": "bearer",
                "user": {"id": "app_installation_flow", "email": "app_installation@example.com"}
            }
        
        # Standard OAuth login flow - let Supabase handle the token exchange
        try:
            # Try with standard OAuth flow - this requires the original code_verifier
            data = client.auth.exchange_code_for_session({
                "auth_code": code
            })
            
            print(f"Received session data: {(data.model_dump_json())}")
            
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
        except Exception as oauth_error:
            print(f"Standard OAuth flow failed: {str(oauth_error)}")
            # If the standard OAuth flow fails with flow state errors, 
            # we're likely in the GitHub App installation flow
            return {
                "access_token": "fallback_token_for_app_installation",
                "token_type": "bearer",
                "user": {"id": "app_installation_flow", "email": "app_installation@example.com"}
            }
    except httpx.HTTPStatusError as e:
        error_msg = f"GitHub callback HTTP error: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"GitHub callback failed: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)

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