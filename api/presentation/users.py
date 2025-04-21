"""
User profile API endpoints.
"""
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl

from api.infrastructure.users import service
from api.infrastructure.auth import get_current_user
from api.domain.users.models import ProfileUpdate
from api.presentation.exceptions import APIException

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
        APIException.check_result(result, "Profile retrieval")
        return {"data": result.data if result.data else None}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Profile retrieval", e)

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
    # Filter out None values
    update_data = {k: v for k, v in profile_data.model_dump().items() if v is not None}
    
    if not update_data:
        APIException.raise_bad_request("No data provided for update")
        
    try:
        result = await service.update_profile(update_data, token.get('access_token'))
        APIException.check_result(result, "Profile update")
        return {"data": result.data if result.data else None}
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Profile update", e) 