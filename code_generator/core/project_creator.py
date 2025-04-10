"""
Project creator agent for generating actual Android projects from generated code.
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional
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
            project_dir = os.path.join(self.output_dir, project_name)
            print(f"\nCreating project directory: {project_dir}")
            os.makedirs(project_dir, exist_ok=True)
            
            # Get template directory path
            template_dir = os.path.join(os.getcwd(), "code_generator", "likeminds-feed-android-social-feed-theme")
            
            # Copy Gradle wrapper files
            gradle_wrapper_files = [
                'gradlew',
                'gradlew.bat',
                'gradle/wrapper/gradle-wrapper.properties'
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
            
            return True
            
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False 