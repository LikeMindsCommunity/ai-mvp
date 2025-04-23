"""
Project management API endpoints.
"""
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, UUID4

from api.infrastructure.projects import service
from api.infrastructure.auth import get_current_user
from api.domain.projects.models import ProjectCreate, ProjectUpdate, ProjectShare
from api.presentation.exceptions import APIException

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new project, optionally with a GitHub repository.
    
    Args:
        project_data: Project creation data
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing created project data
    """
    try:
        github_repo = None
        if project_data.github_repo:
            github_repo = project_data.github_repo.dict()
            
        result = await service.create_project(
            name=project_data.name,
            description=project_data.description,
            github_repo=github_repo, 
            settings=project_data.settings,
            jwt=user.get('access_token')
        )
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project creation", e)

@router.post("/import-github", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def import_github_repo_as_project(
    project_data: ProjectCreate,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new project by importing a GitHub repository.
    
    Args:
        project_data: Project creation data with GitHub repository information
        user: Current authenticated user (from dependency)
    
    Returns:
        Dict containing created project data
    """
    if not project_data.github_repo:
        APIException.raise_bad_request("GitHub repository information is required")
        
    try:
        github_repo = project_data.github_repo.dict()
            
        result = await service.create_project(
            name=project_data.name,
            description=project_data.description,
            github_repo=github_repo,
            settings=project_data.settings,
            jwt=user.get('access_token')
        )
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub project import", e)

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
        return APIException.format_list_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project retrieval", e)

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
        APIException.check_result(result, "Project retrieval")
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project retrieval", e)

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
    # Filter out None values
    update_data = {k: v for k, v in project_data.dict().items() if v is not None}
    
    if not update_data:
        APIException.raise_bad_request("No data provided for update")
    
    try:
        result = await service.update_project(
            project_id=str(project_id), 
            project_data=update_data, 
            jwt=user.get('access_token')
        )
        APIException.check_result(result, "Project update")
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project update", e)

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
        APIException.check_result(result, "Project deletion")
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project deletion", e)

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
        APIException.check_result(result, "Project sharing")
        return APIException.format_response(result)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("Project sharing", e) 