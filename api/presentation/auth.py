"""
Authentication API endpoints.
"""
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from api.infrastructure.database import SupabaseManager
from api.infrastructure.auth import get_current_user, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
supabase_manager = SupabaseManager()

# Models
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

# Helper function to convert Supabase User to dict
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
        result = await supabase_manager.sign_up(
            email=user_data.email, 
            password=user_data.password,
            user_metadata={"full_name": user_data.full_name}
        )
        
        if result.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed"
            )
        
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
            user=user_dict
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )

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
        result = await supabase_manager.sign_in(
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
            user=user_dict
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

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
        result = await supabase_manager.sign_in(
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
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(user: Dict[str, Any] = Depends(get_current_user)) -> None:
    """
    Log out the current user.
    
    Args:
        user: Current authenticated user (from dependency)
    """
    try:
        # The token is already in the client from the dependency
        await supabase_manager.sign_out(None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout error: {str(e)}"
        ) 