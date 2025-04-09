import os
import uuid
import asyncio
import docker
from typing import Optional, Dict, Tuple
from datetime import datetime

class FlutterProjectManager:
    def __init__(self, base_path: str = "projects"):
        self.base_path = base_path
        self.docker_client = docker.from_env()
        self.active_projects: Dict[str, datetime] = {}
        os.makedirs(base_path, exist_ok=True)

    async def create_project(self, project_id: Optional[str] = None) -> str:
        """Create a new Flutter project"""
        if not project_id:
            project_id = str(uuid.uuid4())
        
        project_path = os.path.join(self.base_path, project_id)
        
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            # Create Flutter project using Docker
            try:
                self.docker_client.containers.run(
                    "cirrusci/flutter:latest",
                    command=f"flutter create --platforms web .",
                    volumes={
                        os.path.abspath(project_path): {
                            'bind': '/app',
                            'mode': 'rw'
                        }
                    },
                    working_dir="/app",
                    remove=True
                )
                self.active_projects[project_id] = datetime.now()
            except Exception as e:
                raise Exception(f"Failed to create Flutter project: {str(e)}")
        
        return project_id

    async def update_code(self, project_id: str, code: str) -> Tuple[bool, Optional[str]]:
        """Update the main.dart file with new code"""
        project_path = os.path.join(self.base_path, project_id)
        main_dart_path = os.path.join(project_path, "lib", "main.dart")
        
        try:
            os.makedirs(os.path.dirname(main_dart_path), exist_ok=True)
            with open(main_dart_path, "w") as f:
                f.write(code)
            return True, None
        except Exception as e:
            return False, str(e)

    async def compile_web(self, project_id: str) -> Tuple[bool, Optional[str]]:
        """Compile the Flutter project for web"""
        project_path = os.path.join(self.base_path, project_id)
        
        try:
            container = self.docker_client.containers.run(
                "cirrusci/flutter:latest",
                command="flutter build web",
                volumes={
                    os.path.abspath(project_path): {
                        'bind': '/app',
                        'mode': 'rw'
                    }
                },
                working_dir="/app",
                detach=True
            )
            
            # Wait for compilation to complete
            result = container.wait()
            logs = container.logs().decode('utf-8')
            container.remove()
            
            if result['StatusCode'] == 0:
                return True, None
            return False, logs
            
        except Exception as e:
            return False, str(e)

    async def get_web_preview_path(self, project_id: str) -> Optional[str]:
        """Get the path to the compiled web files"""
        web_build_path = os.path.join(self.base_path, project_id, "build", "web")
        return web_build_path if os.path.exists(web_build_path) else None

    async def cleanup_old_projects(self, max_age_hours: int = 24):
        """Clean up projects older than max_age_hours"""
        current_time = datetime.now()
        projects_to_remove = []
        
        for project_id, creation_time in self.active_projects.items():
            age = (current_time - creation_time).total_seconds() / 3600
            if age > max_age_hours:
                projects_to_remove.append(project_id)
        
        for project_id in projects_to_remove:
            await self.delete_project(project_id)

    async def delete_project(self, project_id: str):
        """Delete a project"""
        project_path = os.path.join(self.base_path, project_id)
        if os.path.exists(project_path):
            import shutil
            shutil.rmtree(project_path)
        if project_id in self.active_projects:
            del self.active_projects[project_id] 