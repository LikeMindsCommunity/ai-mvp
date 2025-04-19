"""
User profile API endpoints.
"""
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl

from api.infrastructure.users import service
from api.infrastructure.auth import get_current_user
from api.domain.users.models import ProfileUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=Dict[str, Any])
async def get_my_profile(token: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the current user's profile.
    
    Args:
        token: User data with access token from the auth dependency
    
    Returns:
        Dict containing profile data
    """
    try:
        result = await service.get_profile(token.get('access_token'))
        if not result or not result.data:
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
    token: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update the current user's profile.
    
    Args:
        profile_data: Profile data to update
        token: User data with access token from the auth dependency
    
    Returns:
        Dict containing updated profile data
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in profile_data.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
            
        result = await service.update_profile(update_data, token.get('access_token'))
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found or update failed"
            )
        return result
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