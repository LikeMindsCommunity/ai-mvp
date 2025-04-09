"""
Project creator agent for generating actual Android projects from generated code.
"""

import os
import subprocess
import shutil
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional
from code_generator import Settings

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
    
    def create_project(self, project_data: Dict) -> bool:
        """
        Create a complete Android project from the generated data.
        
        Args:
            project_data (Dict): Project data containing file structure and content
            
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
            project_path = os.path.join(self.output_dir, project_name)
            print(f"\nCreating project directory: {project_path}")
            
            if self.settings.template_repo_url:
                # Clone template repository
                print(f"Cloning template repository: {self.settings.template_repo_url}")
                subprocess.run(['git', 'clone', self.settings.template_repo_url, project_path], check=True)
                
                # Remove .git directory to start fresh
                shutil.rmtree(os.path.join(project_path, '.git'))
            else:
                os.makedirs(project_path, exist_ok=True)
                # Create basic project structure
                self._create_basic_structure(project_path)
            
            # Create app-specific files
            print("Creating app-specific files...")
            for file_path, content in project_data["files"].items():
                # Only process files in app/src directory
                if not file_path.startswith('app/src/'):
                    continue
                    
                full_path = os.path.join(project_path, file_path)
                print(f"Creating file: {full_path}")
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
            
            # Build the project
            print("\nBuilding project...")
            return self.build_project(project_path)
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False
    
    def _create_basic_structure(self, project_path: str) -> None:
        """
        Create basic project structure if no template is provided.
        
        Args:
            project_path (str): Path to the project directory
        """
        # Create app directory
        app_dir = os.path.join(project_path, "app")
        os.makedirs(app_dir, exist_ok=True)
        
        # Create src directory
        src_dir = os.path.join(app_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        # Create main directory
        main_dir = os.path.join(src_dir, "main")
        os.makedirs(main_dir, exist_ok=True)
        
        # Create java directory
        java_dir = os.path.join(main_dir, "java")
        os.makedirs(java_dir, exist_ok=True)
        
        # Create res directory
        res_dir = os.path.join(main_dir, "res")
        os.makedirs(res_dir, exist_ok=True)
        
        # Note: No need to create Gradle files as they will be copied from template
    
    def build_project(self, project_path: str) -> bool:
        """
        Build the created project using Gradle.
        
        Args:
            project_path (str): Path to the project directory
            
        Returns:
            bool: True if build was successful, False otherwise
        """
        try:
            # Change to project directory
            print(f"Changing to project directory: {project_path}")
            os.chdir(project_path)
            
            # Run Gradle build
            print("Running Gradle build...")
            result = subprocess.run(['./gradlew', 'build'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Project built successfully")
                return True
            else:
                print(f"Build failed with error code: {result.returncode}")
                print("Build output:")
                print(result.stdout)
                print("Build error:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"Error building project: {str(e)}")
            return False 