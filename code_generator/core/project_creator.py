"""
Project creator agent for generating actual Android projects from generated code.
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable
from code_generator.config import Settings

class ProjectCreator:
    """
    Agent responsible for creating actual Android projects from generated code.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the project creator.
        
        Args:
            settings (Settings): Settings object containing configuration
        """
        self.settings = settings
        self.output_dir = os.path.join(os.getcwd(), self.settings.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _build_docker_image(self, project_dir: str) -> bool:
        """
        Build the Docker image for the project.
        
        Args:
            project_dir (str): Path to the project directory
            
        Returns:
            bool: True if build was successful, False otherwise
        """
        try:
            # Get the relative path from code_generator directory
            rel_project_dir = os.path.relpath(project_dir, os.path.join(os.getcwd(), "code_generator"))
            print(f"Relative project directory: {rel_project_dir}")  # Debugging output
            
            # Build the Docker image
            print(f"\nBuilding Docker image for project: {rel_project_dir}")
            build_cmd = [
                "docker", "build",
                "-t", "likeminds-feed-builder",
                "--build-arg", f"PROJECT_DIR={rel_project_dir}",
                "."
            ]
            
            result = subprocess.run(build_cmd, cwd=os.path.join(os.getcwd(), "code_generator"), capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error building Docker image: {result.stderr}")
                return False
                
            print("Docker image built successfully!")
            
            # Create output directory for APK
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
            
            # Copy the APK from the container
            print("\nCopying APK to output directory...")
            run_cmd = [
                "docker", "run", "--rm",
                "-v", f"{output_dir}:/output",
                "likeminds-feed-builder",
                "cp", "project/app/build/outputs/apk/debug/app-debug.apk", "/output/"
            ]
            
            result = subprocess.run(run_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error copying APK: {result.stderr}")
                return False
                
            print("APK copied successfully!")
            return True
            
        except Exception as e:
            print(f"Error in Docker build process: {str(e)}")
            return False
    
    def create_project(self, project_data: Dict, on_chunk: Optional[Callable[[Dict], None]] = None) -> bool:
        """
        Create a complete Android project from the generated data.
        
        Args:
            project_data (Dict): Project data containing file structure and content
            on_chunk (Optional[Callable[[Dict], None]]): Optional callback function for progress updates
            
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            if not project_data:
                print("Error: No project data provided")
                return False
                
            if "project_name" not in project_data:
                print("Error: Project name not found in project data")
                return False
                
            if "files" not in project_data:
                print("Error: No files found in project data")
                return False
            
            # Create project directory
            project_name = project_data["project_name"]
            project_dir = os.path.join(self.output_dir, project_name)
            print(f"\nCreating project directory: {project_dir}")
            os.makedirs(project_dir, exist_ok=True)
            
            # Get template directory path
            template_dir = os.path.join(os.getcwd(), "code_generator", "likeminds-feed-android-social-feed-theme")
            
            # Copy Gradle wrapper files
            gradle_wrapper_files = [
                'gradlew',
                'gradlew.bat',
                'gradle/wrapper/gradle-wrapper.jar'
            ]
            
            for file in gradle_wrapper_files:
                src_path = os.path.join(template_dir, file)
                dst_path = os.path.join(project_dir, file)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy file
                shutil.copy2(src_path, dst_path)
            
            # Create files from generated data
            print("Creating project files...")
            for file_data in project_data["files"]:
                file_path = file_data["path"]
                content = file_data["content"]
                
                full_path = os.path.join(project_dir, file_path)
                print(f"Creating file: {full_path}")
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
                
                # Call on_chunk callback if provided
                if on_chunk:
                    on_chunk({
                        "type": "Result",
                        "value": file_path
                    })
            
            # Build Docker image and get APK
            return self._build_docker_image(project_dir)
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False 