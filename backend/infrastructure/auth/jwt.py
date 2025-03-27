"""
Authentication module for handling JWT tokens and user authentication.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from ..config.settings import settings

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """
    User model for authentication.
    """
    id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token data
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        return jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # For development purposes, we're just decoding the token
    # In production, you would validate against a database
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real implementation, you would fetch the user from a database
    # For now, we'll just return a user object with the ID from the token
    return User(
        id=user_id,
        username=payload.get("username", ""),
        email=payload.get("email"),
        full_name=payload.get("full_name"),
    )


# Optional dependency for routes that don't require authentication
async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    
    Args:
        token: Optional JWT token from Authorization header
        
    Returns:
        User if authenticated, None otherwise
    """
    if token is None:
        return None
    
    try:
        return await get_current_user(token)
    except HTTPException:
        return None 