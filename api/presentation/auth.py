"""
Authentication API endpoints.
"""
from typing import Dict, Any, Optional
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import RedirectResponse
import json

from api.infrastructure.auth import get_current_user, create_access_token, user_to_dict
from api.domain.auth.models import UserCreate, UserLogin, Token, RefreshToken, PasswordReset, PasswordChange
from api.infrastructure.auth.service import sign_up, sign_in, sign_out, sign_in_with_github, handle_github_callback, refresh_token, request_password_reset, change_password
from api.config import get_settings
from api.presentation.exceptions import APIException

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Routes
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> Token:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
    
    Returns:
        Token: Authentication token and user data
    """
    try:
        # Create a new user in Supabase Auth
        result = await sign_up(
            email=user_data.email, 
            password=user_data.password,
            user_metadata={"full_name": user_data.full_name}
        )
        
        if result.user is None:
            APIException.raise_bad_request("Registration failed")
        
        # Convert user object to dictionary
        user_dict = user_to_dict(result.user)
        
        # Check if session exists (it won't if email confirmation is required)
        if result.session is None:
            # Return a special response indicating email confirmation is needed
            return Token(
                access_token="",  # Empty token since we don't have a session yet
                user=user_dict,
                email_confirmation_required=True
            )
        
        # Get the session data (when email confirmation is not required)
        return Token(
            access_token=result.session.access_token,
            refresh_token=result.session.refresh_token,
            user=user_dict
        )
    
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Registration", e)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin) -> Token:
    """
    Authenticate a user and return a token.
    
    Args:
        user_data: User login data
    
    Returns:
        Token: Authentication token and user data
    """
    try:
        result = await sign_in(
            email=user_data.email,
            password=user_data.password
        )
        
        if result.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convert user object to dictionary
        user_dict = user_to_dict(result.user)
        
        return Token(
            access_token=result.session.access_token,
            refresh_token=result.session.refresh_token,
            user=user_dict
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Login", e)

@router.post("/login/oauth")
async def login_with_oauth_form(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """
    Authenticate a user using OAuth2 password form.
    This endpoint is used by the OAuth2PasswordBearer dependency.
    
    Args:
        form_data: OAuth2 form data with username and password fields
    
    Returns:
        Dict with access token and token type
    """
    try:
        result = await sign_in(
            email=form_data.username,  # OAuth2 uses username field for email
            password=form_data.password
        )
        
        if result.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("OAuth login", e)

# Add this alias for Swagger UI - it will redirect to the OAuth endpoint
@router.post("/swagger-auth")
async def swagger_auth(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """
    Alias endpoint for Swagger UI authentication.
    This is an alias for /api/auth/login/oauth that may be easier to find.
    
    Args:
        form_data: OAuth2 form data with username and password fields
    
    Returns:
        Dict with access token and token type
    """
    return await login_with_oauth_form(form_data)

@router.post("/logout", response_model=Dict[str, Any])
async def logout(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Log out the current user.
    
    Args:
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict with success message
    """
    try:
        # Extract the access token from the user dictionary
        access_token = user.get('access_token')
        if not access_token:
            APIException.raise_bad_request("No access token available")
            
        # Sign out with the token
        await sign_out(access_token)
        
        # Return success response
        return {"data": {"message": "Successfully logged out"}}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Logout", e)

@router.post("/github", response_model=Dict[str, Any])
async def github_sign_in():
    """
    Get the GitHub OAuth URL for sign in.
    """
    try:
        result = await sign_in_with_github()
        return result
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub sign in", e)

@router.get("/github/callback")
async def github_callback(code: str = Query(...)):
    """
    Handle the GitHub OAuth callback.
    """
    settings = get_settings()
    try:
        result = await handle_github_callback(code)
        
        # Properly format the redirect URL with the session data
        # Integration tester is configured as the frontend for OAuth callback
        callback_url = settings.frontend_url  # This already points to integration-tester
        
        # JSON stringify the session data for the frontend using custom encoder
        session_json = json.dumps(result, cls=DateTimeEncoder)
        
        # Redirect to frontend with session data
        return RedirectResponse(
            url=f"{callback_url}?session={session_json}"
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub callback", e)

@router.get("/github/app/installation")
async def github_app_installation():
    """
    Get the GitHub App installation ID & save it in Github App Installation in DB corresponding to user id.
    """
    settings = get_settings()
    try:
        #http://localhost:8000/api/auth/github/callback?code=9ac5da52f88528e072f0&installation_id=65173162&setup_action=install

        # Fetch the installation ID and call the github integration to get the repositories
        # Link it with the user account 
        # store in the db
        
        # Redirect to frontend with session data
        return RedirectResponse(
            url=f"{callback_url}?session={session_json}"
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub App installation", e)


@router.post("/refresh", response_model=Token)
async def refresh_auth_token(token_data: RefreshToken) -> Token:
    """
    Refresh an authentication token.
    
    Args:
        token_data: Refresh token data
    
    Returns:
        Token: New authentication token and user data
    """
    try:
        result = await refresh_token(token_data.refresh_token)
        
        return Token(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=result["user"]
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Token refresh", e)

@router.post("/reset-password", response_model=Dict[str, Any])
async def reset_password(reset_data: PasswordReset) -> Dict[str, Any]:
    """
    Request a password reset email.
    
    Args:
        reset_data: Email for password reset
    
    Returns:
        Dict with a success message
    """
    try:
        result = await request_password_reset(reset_data.email)
        return {"data": result}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Password reset request", e)

@router.post("/change-password", response_model=Dict[str, Any])
async def change_user_password(password_data: PasswordChange, user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Change a user's password.
    
    Args:
        password_data: Current and new password
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict with a success message
    """
    try:
        # Extract the access token from the user dictionary
        access_token = user.get('access_token')
        if not access_token:
            APIException.raise_bad_request("No access token available")
            
        result = await change_password(
            access_token=access_token,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )
        
        return {"data": result}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Password change", e) 