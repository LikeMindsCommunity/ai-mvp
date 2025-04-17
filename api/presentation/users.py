"""
User profile API endpoints.
"""
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl

from api.infrastructure.database import SupabaseManager
from api.infrastructure.auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])
supabase_manager = SupabaseManager()

class ProfileUpdate(BaseModel):
    """Profile update model."""
    full_name: str = None
    avatar_url: HttpUrl = None
    preferences: Dict[str, Any] = None

@router.get("/me", response_model=Dict[str, Any])
async def get_my_profile(user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the current user's profile.
    
    Args:
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing profile data
    """
    try:
        result = await supabase_manager.get_profile(user.session.access_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        return result.data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile retrieval error: {str(e)}"
        )

@router.put("/me", response_model=Dict[str, Any])
async def update_my_profile(
    profile_data: ProfileUpdate,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update the current user's profile.
    
    Args:
        profile_data: Profile data to update
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing updated profile data
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
            
        result = await supabase_manager.update_profile(update_data, user.session.access_token)
        return result.data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update error: {str(e)}"
        ) 