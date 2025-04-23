"""
GitHub integration API endpoints.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio

from api.infrastructure.auth import get_current_user
from api.domain.github.models import (
    GitHubToken, 
    GitHubAuthResponse,
    GitHubRepository, 
    GitHubRepositoryList,
    GitHubRepositoryImport,
    GitHubRepositoryImportResponse,
    GitHubRepositoryStatus
)
from api.infrastructure.auth.service import sign_in_with_github
from api.infrastructure.database import get_supabase_client
from api.infrastructure.github.service import (
    store_github_token, 
    get_github_token, 
    delete_github_token,
    list_github_repositories,
    import_github_repository,
    get_repository_status
)
from api.presentation.exceptions import APIException
from pydantic import BaseModel
from api.config import get_settings
from github import Github, GithubIntegration, Auth

settings = get_settings()  

router = APIRouter(prefix="/api/github", tags=["github"])



@router.get("/repositories", response_model=GitHubRepositoryList)
async def get_github_repositories(
    private_key: str = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAoCLcubDEIxw3Kizt1HrLZmjF4V/Uecioi1UoRfuL8qAP8Wcw
9J/4Gwbg69wU0EwfX5/EpnWtYw7OYII49z/pJsSuUcYqMbC/T/FWDGryycJMH1yb
uAlTcL/jLpqlFjDxmL55ooP8F48eZjDDYu591Pnqzrw7yHObjhGzYT3L0eYY9K6O
PdqBdvCgSSERkumZpa18wCADizYFaoI6pdgn5b81p4s1+24shPWBk+bk600vxQab
CeYpoUDsOr+j84oTnTJj8WyoW6k1TNCT7orlanhtsfg21uBzsMjXWwwgLXLrVsAs
FQigllzaupWszBiiaCBDmp4c13u/2vz/UjJa9QIDAQABAoIBAGtN0RAQ1e0c/A4j
2x41RlSSQn654zvT7LSo1HrIi0eCYAyH9DMHeo5Jtq/1YnENgTxnZ7OPSScGhd3/
hMKRLd9Pjeu32RBA+oFMGzfo9lWh/7ZILQROI3565nWVJKhRFaMfh4wR2vvCaEFb
zaFeZC0xZlkvovO4G/VAAS5Y5Vn5QTnJhyxZqGAPKeebIVQkbIjaZbPFweHomXNf
vdYLIscn3xeUO+VaXMGOSdvWwjsdokEAX145zem04/EFHZ6G+rwrua7ctSMBbHm5
DUfBxAADhW5HQS9GTP8h0AZ7OYMa04Q36HyVmLCY8nX5V58mKNkMvqwBukOk4N7C
dN1yFyECgYEAzq3p9pQMkBYGwHO2KiThwkSwwgNO64T3YTAPjPx6jrQ49hBYxSfF
6RFb4n1gargfzZDNp+uIFyIjfaArzq1WhcFm1HBuv3dF/udQF9CHSVv8EtoAbV1l
VD7ccH2wCrsMInYBMXNzIGPI3GWE2LGb0Bey/kLe+xtDnGKvEhNTfk0CgYEAxlmd
r9yt0wJB/JF+Ir+mbWjc+qORGCqPL1Go4RoSfi8W+XusoQDzVxpkUIkWdtTLJkYL
lTJs8rwZEV5EBjhmTEPKLIuvxBwqjaaXI1X/8zs6wmYmXg1jeh6WOuW2OvaYBDuo
1yxz1wglz5MlBiny07TId+Ku6CfY89D8XoMiM0kCgYA3q8bqoWRk51n4OvLllTuu
bXxDNkrqy80qw5xcuKF2kPsK5MpUiOsZZZCfiHARLvl6ELgktB/bQ1nV++/w4uX8
b2T4cjSSpFkZWUtMruHSE9HpbglRbCfgMnKEZoalzU5udeTKYjOvlNFE9J99ExJK
UifnrzGK6AQlOru3nbcOvQKBgQCnLHje9Bv9MHX1LZsmJmla5Xr6NEniGFy+ARFZ
R+Q2PfIbK8V/nZF65F+QETrBxO/Dvl2czfdNToPCQ7UJmRd/R9NqYAEwRJ0I7lOM
ELu8gTsxBW9o7dfd4VG1Kk7Au328c5wGXwzzO4bCwL3/x/NFw6UChifsu0j7ljRe
ZB+7IQKBgQC3uN4zv8Cp6KJPRrDqjZ37G1FH3BfAzfPOGl+BodI1VwxAakaOtZUB
fkeQ/pwonstATDlKguJy39jugFAys/lTyCI2Kpw4Z1GPPHBFtrl9i7u05y2rY3Gj
MQoTA69OUk+Hu7cn8Gxbo3Y3yMyTIz1BIvLkAdh8xbT9wmZ8f6PHEA==
-----END RSA PRIVATE KEY-----
""", # TODO: Get from Settings.py
    app_id: str = settings.github_app_id,
    ):
    """
    List GitHub repositories for a user
    """
    try:
        
        user = await get_current_user()
        user_id = user["id"]

        client = await get_supabase_client()
        github_installation_id = client.from_('github_app_installations').select('installation_id').eq('user_id', user_id).execute()

        # Get the GitHub token for the user


        print(f"Installation ID: {github_installation_id}")
        print(f"Private Key: {private_key}")
        print(f"App ID: {app_id}")
        auth = Auth.AppAuth(app_id, private_key)
        gi = GithubIntegration(auth=auth)
        # Get installation
        git_installation = gi.get_app_installation(github_installation_id)
        
    
        # List repositories
        repos = []
        for repo in git_installation.get_repos():
            repos.append({
                "name": repo.name,
                "html_url": repo.html_url
            })
       
        return GitHubRepositoryList(repositories=repos)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repositories listing", e)


@router.post("/connect", response_model=GitHubAuthResponse)
async def connect_github_account():
    """
    Get the GitHub OAuth URL to connect a GitHub account.
    """
    try:
        result = await sign_in_with_github()
        return result
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub connection", e)


@router.get("/token", response_model=Optional[GitHubToken])
async def get_github_account(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the connected GitHub account for the current user.
    """
    try:
        user_id = current_user["id"]
        token = await get_github_token(user_id)
        return token
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub account retrieval", e)


@router.delete("/token", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_github_account(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Disconnect the GitHub account for the current user.
    """
    try:
        user_id = current_user["id"]
        success = await delete_github_token(user_id)
        
        if not success:
            APIException.raise_not_found("GitHub account not found")
            
        return None
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub account disconnection", e)



@router.post("/repositories/import", response_model=GitHubRepositoryImportResponse)
async def import_repository(
    repo_import: GitHubRepositoryImport,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Import a GitHub repository for code generation.
    
    This either creates a standalone repository record or associates 
    it with an existing project based on the project_id parameter.
    """
    try:
        user_id = current_user["id"]
        
        # If project_id is specified, verify it exists and belongs to the user
        if repo_import.project_id:
            client = get_supabase_client()
            project_response = client.from_('projects').select('id').eq('id', repo_import.project_id).execute()
            
            if not project_response.data or len(project_response.data) == 0:
                APIException.raise_not_found(f"Project {repo_import.project_id} not found")
                
        result = await import_github_repository(user_id, repo_import)
        
        return GitHubRepositoryImportResponse(
            repository_id=result["repository_id"],
            status=result["status"],
            message=result["message"],
            project_id=repo_import.project_id
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository import", e)


@router.get("/repositories/{repository_id}/status", response_model=GitHubRepositoryStatus)
async def get_repository_import_status(
    repository_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get the status of a GitHub repository import.
    """
    try:
        user_id = current_user["id"]
        result = await get_repository_status(user_id, repository_id)
        
        # Check if codebase.txt exists
        has_codebase_summary = False
        if result["status"] == "ready" and result.get("selected_path") is not None:
            try:
                from api.infrastructure.github.repository_manager import GitHubRepositoryManager
                repo_manager = GitHubRepositoryManager()
                
                # Calculate repository path
                repo_dir = repo_manager.get_repository_path(repository_id)
                project_path = result.get("selected_path", "")
                
                if project_path:
                    project_dir = repo_dir / project_path
                else:
                    project_dir = repo_dir
                
                # Check if codebase.txt exists
                codebase_file = project_dir / "codebase.txt"
                has_codebase_summary = codebase_file.exists()
            except Exception:
                # If there's an error checking the file, assume it doesn't exist
                has_codebase_summary = False
        
        # Get flutter projects from metadata
        flutter_projects = []
        if result.get("metadata") and isinstance(result["metadata"], dict):
            flutter_projects = result["metadata"].get("flutter_projects", [])
        
        return GitHubRepositoryStatus(
            id=result["id"],
            repo_name=result["repo_name"],
            repo_full_name=result["repo_full_name"],
            status=result["status"],
            error_message=result.get("error_message"),
            created_at=result["created_at"],
            updated_at=result["updated_at"],
            last_synced_at=result.get("last_synced_at"),
            selected_branch=result.get("selected_branch"),
            selected_path=result.get("selected_path"),
            flutter_projects=flutter_projects,
            has_codebase_summary=has_codebase_summary
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository status retrieval", e)


@router.post("/repositories/{repository_id}/process", response_model=GitHubRepositoryImportResponse)
async def process_repository(
    repository_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Manually process a GitHub repository to clone it, scan for Flutter projects,
    and generate the codebase summary.
    """
    try:
        user_id = current_user["id"]
        
        # Verify the repository exists and belongs to the user
        result = await get_repository_status(user_id, repository_id)
        
        # Start repository processing
        from api.infrastructure.github.repository_manager import GitHubRepositoryManager
        
        # Start the repository processing task in the background
        asyncio.create_task(
            GitHubRepositoryManager().process_repository(repository_id, user_id)
        )
        
        return GitHubRepositoryImportResponse(
            repository_id=repository_id,
            status="processing",
            message=f"Repository {result['repo_full_name']} processing initiated"
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository processing", e)


class ProjectPathSelect(BaseModel):
    """Model for selecting a project path."""
    project_path: str

@router.post("/repositories/{repository_id}/select-path", response_model=GitHubRepositoryStatus)
async def select_project_path(
    repository_id: str,
    path_data: ProjectPathSelect,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Select a specific Flutter project path within a repository.
    This will update the repository and regenerate the codebase summary.
    """
    try:
        user_id = current_user["id"]
        
        # Verify the repository exists and belongs to the user
        result = await get_repository_status(user_id, repository_id)
        
        # Verify that the path exists in the Flutter projects list
        flutter_projects = []
        if result.get("metadata") and isinstance(result["metadata"], dict):
            flutter_projects = result["metadata"].get("flutter_projects", [])
        
        if path_data.project_path and path_data.project_path not in flutter_projects:
            APIException.raise_bad_request(f"Project path '{path_data.project_path}' not found in repository")
        
        # Update the selected path
        client = get_supabase_client()
        client.from_("github_repositories").update({
            "selected_path": path_data.project_path
        }).eq("id", repository_id).execute()
        
        # Generate a new codebase summary
        from api.infrastructure.github.repository_manager import GitHubRepositoryManager
        repo_manager = GitHubRepositoryManager()
        
        # Start the codebase summary generation in the background
        asyncio.create_task(
            repo_manager.generate_codebase_summary(repository_id, path_data.project_path)
        )
        
        # Get the updated repository status
        result = await get_repository_status(user_id, repository_id)
        
        # We need to update the result with the same format as the status endpoint
        return await get_repository_import_status(repository_id, current_user)
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub project path selection", e)


class RepositoryUrlImport(BaseModel):
    """Model for importing a GitHub repository by URL."""
    repository_url: str
    project_id: Optional[str] = None

@router.post("/import-repository", response_model=GitHubRepositoryImportResponse)
async def import_repository_url(
    repo_data: RepositoryUrlImport,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Import a GitHub repository by URL for backward compatibility.
    This converts the URL into a GitHubRepositoryImport and calls the standard import endpoint.
    """
    try:
        # Convert repository URL to repository full name
        repo_full_name = repo_data.repository_url
        
        # Remove github.com prefix if present
        if repo_full_name.startswith("https://github.com/"):
            repo_full_name = repo_full_name[19:]  # Remove "https://github.com/"
        elif repo_full_name.startswith("http://github.com/"):
            repo_full_name = repo_full_name[18:]  # Remove "http://github.com/"
        
        # Remove .git suffix if present
        if repo_full_name.endswith(".git"):
            repo_full_name = repo_full_name[:-4]  # Remove ".git"
            
        # Create GitHubRepositoryImport
        repo_import = GitHubRepositoryImport(
            repo_full_name=repo_full_name,
            project_id=repo_data.project_id
        )
        
        # Call the standard import endpoint
        user_id = current_user["id"]
        result = await import_github_repository(user_id, repo_import)
        
        return GitHubRepositoryImportResponse(
            repository_id=result["repository_id"],
            status=result["status"],
            message=result["message"],
            project_id=repo_data.project_id
        )
    except ValueError as e:
        APIException.raise_bad_request(str(e))
    except HTTPException:
        raise
    except Exception as e:
        APIException.raise_server_error("GitHub repository import", e) 