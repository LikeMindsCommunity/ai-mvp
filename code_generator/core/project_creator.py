"""
Project creator agent for generating actual Android projects from generated code.
"""

import os
import subprocess
import shutil
from typing import Dict, List
import json

class ProjectCreator:
    """
    Agent responsible for creating actual Android projects from generated code.
    """
    
    def __init__(self, project_name: str, generated_code: Dict[str, str]):
        """
        Initialize the project creator.
        
        Args:
            project_name (str): Name of the project to create
            generated_code (Dict[str, str]): Dictionary containing file paths and their content
        """
        self.project_name = project_name
        self.generated_code = generated_code
        self.project_path = os.path.abspath(project_name)
    
    def create_project_structure(self):
        """Create the basic Android project structure."""
        try:
            # Create project directory
            os.makedirs(self.project_path, exist_ok=True)
            
            # Create standard Android directories
            directories = [
                'app/src/main/java',
                'app/src/main/res/layout',
                'app/src/main/res/values',
                'app/src/main/res/drawable',
                'gradle/wrapper'
            ]
            
            for directory in directories:
                os.makedirs(os.path.join(self.project_path, directory), exist_ok=True)
            
            print(f"Created project structure at {self.project_path}")
            return True
        except Exception as e:
            print(f"Error creating project structure: {str(e)}")
            return False
    
    def create_gradle_files(self):
        """Create Gradle configuration files."""
        try:
            # Create root build.gradle
            root_build_gradle = os.path.join(self.project_path, 'build.gradle')
            with open(root_build_gradle, 'w') as f:
                f.write(self.generated_code.get('build.gradle', ''))
            
            # Create app/build.gradle
            app_build_gradle = os.path.join(self.project_path, 'app/build.gradle')
            os.makedirs(os.path.dirname(app_build_gradle), exist_ok=True)
            with open(app_build_gradle, 'w') as f:
                f.write(self.generated_code.get('app/build.gradle', ''))
            
            # Create settings.gradle
            settings_gradle = os.path.join(self.project_path, 'settings.gradle')
            with open(settings_gradle, 'w') as f:
                f.write(self.generated_code.get('settings.gradle', ''))
            
            # Create gradle wrapper
            gradle_wrapper = os.path.join(self.project_path, 'gradlew')
            with open(gradle_wrapper, 'w') as f:
                f.write(self.generated_code.get('gradlew', ''))
            
            # Make gradlew executable
            os.chmod(gradle_wrapper, 0o755)
            
            print("Created Gradle configuration files")
            return True
        except Exception as e:
            print(f"Error creating Gradle files: {str(e)}")
            return False
    
    def create_source_files(self):
        """Create Java/Kotlin source files."""
        try:
            for file_path, content in self.generated_code.items():
                if file_path.endswith(('.java', '.kt')):
                    full_path = os.path.join(self.project_path, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w') as f:
                        f.write(content)
            
            print("Created source files")
            return True
        except Exception as e:
            print(f"Error creating source files: {str(e)}")
            return False
    
    def create_resource_files(self):
        """Create Android resource files."""
        try:
            for file_path, content in self.generated_code.items():
                if file_path.endswith(('.xml', '.png', '.jpg')):
                    full_path = os.path.join(self.project_path, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w') as f:
                        f.write(content)
            
            print("Created resource files")
            return True
        except Exception as e:
            print(f"Error creating resource files: {str(e)}")
            return False
    
    def create_project(self) -> bool:
        """
        Create the complete Android project.
        
        Returns:
            bool: True if project was created successfully, False otherwise
        """
        try:
            if not self.create_project_structure():
                return False
            
            if not self.create_gradle_files():
                return False
            
            if not self.create_source_files():
                return False
            
            if not self.create_resource_files():
                return False
            
            print(f"Successfully created Android project at {self.project_path}")
            return True
        except Exception as e:
            print(f"Error creating project: {str(e)}")
            return False
    
    def build_project(self) -> bool:
        """
        Build the created project using Gradle.
        
        Returns:
            bool: True if build was successful, False otherwise
        """
        try:
            # Change to project directory
            os.chdir(self.project_path)
            
            # Run Gradle build
            result = subprocess.run(['./gradlew', 'build'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Project built successfully")
                return True
            else:
                print(f"Build failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error building project: {str(e)}")
            return False 