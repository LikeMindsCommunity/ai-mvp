"""
Authentication helper functions.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from api.config import get_settings, TokenPayload
from api.infrastructure.database import SupabaseManager

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
supabase_manager = SupabaseManager()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get the current authenticated user.
    
    Args:
        token: JWT token
    
    Returns:
        Dict containing user data
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # We're using Supabase's JWT, but we still validate it here for early error detection
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        token_data = TokenPayload(**payload)
        
        # Check if the token is expired
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        # JWT validation failed, but Supabase will handle this so we let it through
        pass
    
    try:
        # Use Supabase's authentication to get the current user
        supabase_manager.client.auth.set_session(token)
        user = supabase_manager.client.auth.get_user()
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
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