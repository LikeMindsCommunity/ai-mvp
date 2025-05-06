"""
JWT token and authentication helper functions.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.config import get_settings
from api.infrastructure.database import SupabaseManager

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/swagger-auth")
supabase_manager = SupabaseManager()

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

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get the current authenticated user using Supabase authentication.
    
    Args:
        token: Supabase JWT token
    
    Returns:
        Dict containing user data with access_token
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Let Supabase client handle token validation
        user_response = supabase_manager.client.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Convert user object to dictionary
        user_dict = user_to_dict(user_response.user)
        
        # Add the access token to the user data
        user_dict["access_token"] = token
        
        return user_dict
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    Note: This is only used for custom tokens, not Supabase authentication.
    
    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time delta
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt