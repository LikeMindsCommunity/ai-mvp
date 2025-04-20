"""
Project management API endpoints.
"""
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, UUID4

from api.infrastructure.projects import service
from api.infrastructure.auth import get_current_user
from api.domain.projects.models import ProjectCreate, ProjectUpdate, ProjectShare

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new project.
    
    Args:
        project_data: Project creation data
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing created project data
    """
    try:
        result = await service.create_project(
            name=project_data.name,
            description=project_data.description,
            jwt=user.get('access_token')
        )
        # Return the first item from the data array since Supabase returns an array
        return result.data[0] if result.data else None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project creation error: {str(e)}"
        )

@router.get("/", response_model=List[Dict[str, Any]])
async def get_projects(user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get all projects for the current user.
    
    Args:
        user: Current authenticated user (from dependency)
    
    Returns:
        List of projects
    """
    try:
        result = await service.get_projects(jwt=user.get('access_token'))
        return result.data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project retrieval error: {str(e)}"
        )

@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_project(
    project_id: UUID4 = Path(..., description="The ID of the project to get"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a project by ID.
    
    Args:
        project_id: Project ID
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing project data
    """
    try:
        result = await service.get_project(
            project_id=str(project_id), 
            jwt=user.get('access_token')
        )
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        # Return the first item from the data array
        return result.data[0] if result.data else None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project retrieval error: {str(e)}"
        )

@router.put("/{project_id}", response_model=Dict[str, Any])
async def update_project(
    project_data: ProjectUpdate,
    project_id: UUID4 = Path(..., description="The ID of the project to update"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update a project.
    
    Args:
        project_data: Project update data
        project_id: Project ID
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing updated project data
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in project_data.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        result = await service.update_project(
            project_id=str(project_id), 
            project_data=update_data, 
            jwt=user.get('access_token')
        )
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have access"
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
            detail=f"Project update error: {str(e)}"
        )

@router.delete("/{project_id}", response_model=Dict[str, Any])
async def delete_project(
    project_id: UUID4 = Path(..., description="The ID of the project to delete"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a project.
    
    Args:
        project_id: Project ID
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing deletion result
    """
    try:
        result = await service.delete_project(
            project_id=str(project_id), 
            jwt=user.get('access_token')
        )
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have access"
            )
            
        return {"success": True, "message": "Project deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project deletion error: {str(e)}"
        )

@router.post("/{project_id}/share", response_model=Dict[str, Any])
async def share_project(
    share_data: ProjectShare,
    project_id: UUID4 = Path(..., description="The ID of the project to share"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Share a project with another user.
    
    Args:
        share_data: Sharing details (user email and role)
        project_id: Project ID
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing sharing result
    """
    try:
        result = await service.share_project(
            project_id=str(project_id), 
            user_email=share_data.user_email,
            role=share_data.role,
            jwt=user.get('access_token')
        )
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have access"
            )
            
        return {"success": True, "message": f"Project shared with {share_data.user_email}"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project sharing error: {str(e)}"
        ) 