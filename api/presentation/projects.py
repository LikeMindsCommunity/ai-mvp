"""
Project management API endpoints.
"""
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, UUID4

from api.infrastructure.database import SupabaseManager
from api.infrastructure.auth import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])
supabase_manager = SupabaseManager()

class ProjectCreate(BaseModel):
    """Project creation model."""
    name: str
    description: str = None

class ProjectUpdate(BaseModel):
    """Project update model."""
    name: str = None
    description: str = None
    settings: Dict[str, Any] = None

class ProjectShare(BaseModel):
    """Project sharing model."""
    user_email: str
    role: str = "viewer"  # Default role is viewer

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
        result = await supabase_manager.create_project(
            name=project_data.name,
            description=project_data.description,
            jwt=user.session.access_token
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
        result = await supabase_manager.get_projects(user.session.access_token)
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
        result = await supabase_manager.get_project(str(project_id), user.session.access_token)
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
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
            
        result = await supabase_manager.update_project(
            str(project_id), 
            update_data, 
            user.session.access_token
        )
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have permission to update it"
            )
            
        return result.data[0]  # Return the first (and only) updated project
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

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID4 = Path(..., description="The ID of the project to delete"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a project.
    
    Args:
        project_id: Project ID
        user: Current authenticated user (from dependency)
    """
    try:
        result = await supabase_manager.delete_project(str(project_id), user.session.access_token)
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have permission to delete it"
            )
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
        share_data: Project sharing data
        project_id: Project ID
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing sharing result data
    """
    try:
        # Call the RPC function to share the project
        result = await supabase_manager.client.rpc(
            'share_project',
            {
                'project_id': str(project_id),
                'user_email': share_data.user_email,
                'role': share_data.role
            }
        ).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to share the project"
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
            detail=f"Project sharing error: {str(e)}"
        ) 