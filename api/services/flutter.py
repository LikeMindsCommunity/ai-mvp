import os
import uuid
import asyncio
import docker
from typing import Optional, Dict, Tuple
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlutterProjectManager:
    def __init__(self, base_path: str = "projects"):
        self.base_path = base_path
        self.docker_available = False
        try:
            # Set a shorter timeout for Docker client initialization
            self.docker_client = docker.from_env(timeout=10)
            # Test the connection
            self.docker_client.ping()
            self.docker_available = True
            logger.info("Docker connection established successfully")
        except Exception as e:
            logger.warning(f"Docker is not available or not responding: {str(e)}")
            self.docker_client = None
        
        self.active_projects: Dict[str, datetime] = {}
        os.makedirs(base_path, exist_ok=True)

    async def create_project(self, project_id: Optional[str] = None) -> str:
        """Create a new Flutter project"""
        if not project_id:
            project_id = str(uuid.uuid4())
        
        project_path = os.path.join(self.base_path, project_id)
        
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            
            # Create basic Flutter project structure manually if Docker is not available
            if not self.docker_available:
                logger.info(f"Creating basic project structure for {project_id} without Docker")
                await self._create_basic_structure(project_path)
            else:
                # Create Flutter project using Docker
                try:
                    logger.info(f"Creating Flutter project {project_id} using Docker")
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
                except Exception as e:
                    logger.error(f"Docker container failed: {str(e)}")
                    # Fallback to basic structure creation
                    await self._create_basic_structure(project_path)
            
            self.active_projects[project_id] = datetime.now()
        
        return project_id

    async def _create_basic_structure(self, project_path: str):
        """Create a basic Flutter project structure without Docker"""
        # Create lib directory
        lib_path = os.path.join(project_path, "lib")
        os.makedirs(lib_path, exist_ok=True)
        
        # Create a basic main.dart file
        main_dart = os.path.join(lib_path, "main.dart")
        with open(main_dart, "w") as f:
            f.write("""
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const Center(
        child: Text('Docker not available. Use manual Flutter setup.'),
      ),
    );
  }
}
""")
        
        # Create build/web directory for preview
        web_path = os.path.join(project_path, "build", "web")
        os.makedirs(web_path, exist_ok=True)
        
        # Create a basic index.html
        index_html = os.path.join(web_path, "index.html")
        with open(index_html, "w") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
  <title>Flutter Web Preview</title>
  <style>
    body { 
      display: flex; 
      justify-content: center; 
      align-items: center; 
      height: 100vh; 
      font-family: Arial, sans-serif;
    }
    .message {
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 5px;
      background-color: #f8f8f8;
      max-width: 600px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="message">
    <h2>Docker not available for Flutter compilation</h2>
    <p>Please set up Flutter locally or ensure Docker is running to use the full functionality.</p>
    <pre>flutter create myapp && cd myapp && flutter run -d chrome</pre>
  </div>
</body>
</html>
""")

    async def update_code(self, project_id: str, code: str) -> Tuple[bool, Optional[str]]:
        """Update the main.dart file with new code"""
        project_path = os.path.join(self.base_path, project_id)
        main_dart_path = os.path.join(project_path, "lib", "main.dart")
        
        try:
            os.makedirs(os.path.dirname(main_dart_path), exist_ok=True)
            with open(main_dart_path, "w") as f:
                f.write(code)
            logger.info(f"Successfully updated code for project {project_id}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to update code for project {project_id}: {str(e)}")
            return False, str(e)

    async def compile_web(self, project_id: str) -> Tuple[bool, Optional[str]]:
        """Compile the Flutter project for web"""
        project_path = os.path.join(self.base_path, project_id)
        
        # If Docker is not available, return a message
        if not self.docker_available:
            logger.warning("Skipping web compilation because Docker is not available")
            return True, "Docker is not available for compilation. Using fallback preview."
        
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
            logger.error(f"Docker compilation failed: {str(e)}")
            # If Docker fails, we still provide a basic preview
            return True, f"Docker compilation error: {str(e)}. Using fallback preview."

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