from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1)

class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]
    email_confirmation_required: Optional[bool] = False
    refresh_token: Optional[str] = None

class RefreshToken(BaseModel):
    """Token refresh request model."""
    refresh_token: str

class PasswordReset(BaseModel):
    """Password reset request model."""
    email: EmailStr

class PasswordChange(BaseModel):
    """Password change request model."""
    current_password: str
    new_password: str = Field(..., min_length=8) 