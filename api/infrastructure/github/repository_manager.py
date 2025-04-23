"""
GitHub repository management service.
Handles repository cloning, scanning, and cleanup.
"""
import os
import shutil
import subprocess
import asyncio
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from api.infrastructure.database import get_supabase_client
from api.infrastructure.github.service import get_github_token
from api.config import get_settings

class GitHubRepositoryManager:
    """
    Manages GitHub repositories including cloning, scanning, and cleanup operations.
    """
    
    def __init__(self):
        """Initialize the repository manager with configuration."""
        self.settings = get_settings()
        self.base_output_dir = Path(os.path.join(os.getcwd(), "output"))
        
        # Create output directory if it doesn't exist
        os.makedirs(self.base_output_dir, exist_ok=True)
    
    def get_repository_path(self, repository_id: str) -> Path:
        """Get the filesystem path for a repository."""
        # First check if there's a project ID associated with this repository
        try:
            client = get_supabase_client()
            result = client.from_("github_repositories").select("project_id").eq("id", repository_id).execute()
            
            if result and result.data and len(result.data) > 0 and result.data[0].get("project_id"):
                # If there's a project ID, use that as the directory
                project_id = result.data[0]["project_id"]
                return self.base_output_dir / project_id
        except Exception as e:
            print(f"Error getting project ID for repository {repository_id}: {str(e)}")
        
        # Fall back to using repository ID as directory if no project ID or on error
        return self.base_output_dir / repository_id
    
    async def update_repository_status(self, repository_id: str, status: str, error_message: Optional[str] = None) -> None:
        """Update the repository status in the database."""
        client = get_supabase_client()
        
        update_data = {"status": status}
        if error_message:
            update_data["error_message"] = error_message
            
        try:
            client.from_("github_repositories").update(update_data).eq("id", repository_id).execute()
        except Exception as e:
            print(f"Error updating repository status: {str(e)}")
    
    async def clone_repository(self, repository_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Clone a GitHub repository.
        
        Args:
            repository_id: ID of the repository in the database
            user_id: ID of the user who owns the repository
            
        Returns:
            Tuple of (success, error_message)
        """
        client = get_supabase_client()
        
        try:
            # Get repository details
            result = client.from_("github_repositories").select("*").eq("id", repository_id).eq("user_id", user_id).execute()
            
            if not result or not result.data or len(result.data) == 0:
                return False, f"Repository {repository_id} not found"
                
            repo_data = result.data[0]
            
            # Update status to cloning
            await self.update_repository_status(repository_id, "cloning")
            
            # Get the GitHub token for authentication
            token = await get_github_token(user_id)
            if not token:
                await self.update_repository_status(repository_id, "error", "No GitHub token found")
                return False, "No GitHub token found"
                
            # Create a temporary directory for the repository
            repo_dir = self.get_repository_path(repository_id)
            if repo_dir.exists():
                # Clean up existing directory
                shutil.rmtree(repo_dir)
                
            os.makedirs(repo_dir, exist_ok=True)
            
            # Construct authenticated clone URL
            clone_url = repo_data["clone_url"]
            if clone_url.startswith("https://"):
                auth_clone_url = clone_url.replace("https://", f"https://{token.access_token}@")
            else:
                auth_clone_url = clone_url
                
            # Get the selected branch
            branch = repo_data.get("selected_branch") or repo_data.get("default_branch", "main")
            
            # Clone the repository
            cmd = [
                "git", "clone",
                "--depth", "1",  # Shallow clone
                "--single-branch",  # Single branch only
                "--branch", branch,  # Specific branch
                auth_clone_url,
                str(repo_dir)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                # Strip token from error message for security
                error_message = stderr.decode("utf-8").replace(token.access_token, "TOKEN")
                await self.update_repository_status(repository_id, "error", f"Git clone failed: {error_message}")
                return False, f"Git clone failed: {error_message}"
                
            # Clone succeeded, now update status to "analyzing"
            await self.update_repository_status(repository_id, "analyzing")
            
            # Return success
            return True, None
            
        except Exception as e:
            error_message = f"Repository cloning error: {str(e)}"
            await self.update_repository_status(repository_id, "error", error_message)
            return False, error_message
    
    async def scan_for_flutter_projects(self, repository_id: str) -> Tuple[bool, Optional[List[str]], Optional[str]]:
        """
        Scan repository for Flutter projects by looking for pubspec.yaml files.
        
        Args:
            repository_id: ID of the repository
            
        Returns:
            Tuple of (success, flutter_project_paths, error_message)
        """
        try:
            repo_dir = self.get_repository_path(repository_id)
            
            if not repo_dir.exists():
                return False, None, "Repository directory not found"
                
            # Find all pubspec.yaml files
            pubspec_files = []
            for root, dirs, files in os.walk(repo_dir):
                # Skip .git directory
                if '.git' in dirs:
                    dirs.remove('.git')
                    
                if 'pubspec.yaml' in files:
                    project_path = os.path.relpath(root, str(repo_dir))
                    if project_path == '.':
                        project_path = ''  # Root directory
                    pubspec_files.append(project_path)
            
            return True, pubspec_files, None
            
        except Exception as e:
            error_message = f"Error scanning for Flutter projects: {str(e)}"
            return False, None, error_message
    
    async def generate_codebase_summary(self, repository_id: str, project_path: str = '') -> Tuple[bool, Optional[str]]:
        """
        Generate a flat codebase.txt summary of the repository.
        
        Args:
            repository_id: ID of the repository
            project_path: Path to the Flutter project within the repository
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            repo_dir = self.get_repository_path(repository_id)
            
            if not repo_dir.exists():
                return False, "Repository directory not found"
                
            # Determine the project directory
            project_dir = repo_dir
            if project_path:
                project_dir = repo_dir / project_path
                
            if not project_dir.exists():
                return False, f"Project path '{project_path}' not found in repository"
                
            # Create the codebase summary file
            summary_file = project_dir / "codebase.txt"
            
            # Use find and grep to list all Dart files and their contents
            cmd = f'find "{project_dir}" -name "*.dart" | grep -v "\\.git/" | sort | xargs cat > "{summary_file}"'
            
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_message = stderr.decode("utf-8")
                return False, f"Failed to generate codebase summary: {error_message}"
                
            # Check if the summary file was created and has content
            if not summary_file.exists() or summary_file.stat().st_size == 0:
                return False, "No Dart files found to generate codebase summary"
                
            return True, None
            
        except Exception as e:
            error_message = f"Error generating codebase summary: {str(e)}"
            return False, error_message
    
    async def process_repository(self, repository_id: str, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Process a repository: clone, scan for Flutter projects, and generate codebase summary.
        
        Args:
            repository_id: ID of the repository
            user_id: ID of the user who owns the repository
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Get repository info to check if it's associated with a project
            client = get_supabase_client()
            repo_result = client.from_("github_repositories").select("*").eq("id", repository_id).eq("user_id", user_id).execute()
            
            if not repo_result or not repo_result.data or len(repo_result.data) == 0:
                return False, f"Repository {repository_id} not found"
            
            repo_data = repo_result.data[0]
            project_id = repo_data.get("project_id")
            
            # Clone the repository
            clone_success, clone_error = await self.clone_repository(repository_id, user_id)
            if not clone_success:
                return False, clone_error
                
            # Scan for Flutter projects
            scan_success, flutter_paths, scan_error = await self.scan_for_flutter_projects(repository_id)
            if not scan_success:
                await self.update_repository_status(repository_id, "error", scan_error)
                return False, scan_error
                
            # Update the repository record with the Flutter project paths
            
            # Use the first Flutter project path if one is found
            project_path = flutter_paths[0] if flutter_paths else ''
            
            # Save the Flutter project paths
            update_data = {
                "selected_path": project_path,
                "metadata": {
                    "flutter_projects": flutter_paths
                }
            }
            
            client.from_("github_repositories").update(update_data).eq("id", repository_id).execute()
            
            # Generate codebase summary
            summary_success, summary_error = await self.generate_codebase_summary(repository_id, project_path)
            if not summary_success:
                await self.update_repository_status(repository_id, "error", summary_error)
                return False, summary_error
                
            # All steps completed successfully
            await self.update_repository_status(repository_id, "ready")
            
            # Update last synced timestamp
            client.from_("github_repositories").update({"last_synced_at": "now()"}).eq("id", repository_id).execute()
            
            # If this repository is associated with a project, update the project settings
            if project_id:
                try:
                    # Get current project settings
                    project_result = client.from_("projects").select("settings").eq("id", project_id).execute()
                    if project_result and project_result.data and len(project_result.data) > 0:
                        settings = project_result.data[0].get("settings") or {}
                        
                        # Update settings with repository info
                        settings.update({
                            "github_repo_status": "ready",
                            "github_last_synced": repo_data.get("last_synced_at") or "now()",
                            "flutter_projects": flutter_paths,
                            "selected_path": project_path,
                            "has_codebase_summary": True
                        })
                        
                        # Update project settings
                        client.from_("projects").update({"settings": settings}).eq("id", project_id).execute()
                except Exception as e:
                    print(f"Error updating project settings for {project_id}: {str(e)}")
                    # Don't fail the whole operation if updating project settings fails
            
            return True, None
            
        except Exception as e:
            error_message = f"Error processing repository: {str(e)}"
            await self.update_repository_status(repository_id, "error", error_message)
            return False, error_message
    
    async def cleanup_repository(self, repository_id: str) -> Tuple[bool, Optional[str]]:
        """
        Clean up a repository directory.
        
        Args:
            repository_id: ID of the repository
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            repo_dir = self.get_repository_path(repository_id)
            
            if repo_dir.exists():
                shutil.rmtree(repo_dir)
                
            return True, None
            
        except Exception as e:
            error_message = f"Error cleaning up repository: {str(e)}"
            return False, error_message 