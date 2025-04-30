"""
Code management utilities for the Flutter code generator.
"""

import os
import re
import subprocess
import threading
import uuid
import shutil
from typing import List, Tuple, Optional

from flutter_generator.config import Settings

class FlutterCodeManager:
    """
    Manager for Flutter code file operations.
    """
    
    def __init__(self, settings: Settings = None, project_id: str = None, generation_id: str = None):
        """
        Initialize the code manager.
        
        Args:
            settings (Settings, optional): Settings for configuration
            project_id (str, optional): Project ID this generation belongs to
            generation_id (str, optional): Unique ID for this generation
        """
        self.settings = settings or Settings()
        self.latest_code = None
        self.root_dir = os.getcwd()
        self.project_id = project_id or str(uuid.uuid4())
        self.generation_id = generation_id or str(uuid.uuid4())
        self.project_dir = self._create_project_dir()
        self.generations_dir = self._create_generations_dir()
        self.integration_path = os.path.join(self.project_dir, "integration")
        # Initialize integration directory immediately
        self._setup_integration_dir()
        
        # Properties for existing project mode
        self.is_existing_project = False
        self.existing_project_code = None
        self.existing_project_analysis = None
    
    def set_existing_project_mode(self, is_existing_project: bool) -> None:
        """
        Set whether this is an existing project or new project mode.
        
        Args:
            is_existing_project (bool): True if working with an existing project
        """
        self.is_existing_project = is_existing_project
        
    def set_existing_project_code(self, code: str) -> None:
        """
        Set the existing project code for reference.
        
        Args:
            code (str): The ingested code from the existing project
        """
        self.existing_project_code = code
        
    def set_existing_project_analysis(self, analysis: str) -> None:
        """
        Set the analysis of the existing project.
        
        Args:
            analysis (str): The analysis text from the conversation manager
        """
        self.existing_project_analysis = analysis
    
    def _create_project_dir(self) -> str:
        """
        Create a directory for this project.
        
        Returns:
            str: Path to the project directory
        """
        project_dir = os.path.join(self.settings.output_path, self.project_id)
        os.makedirs(project_dir, exist_ok=True)
        return project_dir
    
    def _create_generations_dir(self) -> str:
        """
        Create a directory to store all generations for this project.
        
        Returns:
            str: Path to the generations directory
        """
        generations_dir = os.path.join(self.project_dir, "generations")
        os.makedirs(generations_dir, exist_ok=True)
        return generations_dir
        
    def _setup_integration_dir(self) -> str:
        """
        Set up the integration directory for this project by copying from the template.
        Only creates the integration directory once per project.
        
        Returns:
            str: Path to the integration directory
        """
        # Create integration directory within project directory
        integration_dir = os.path.join(self.project_dir, "integration")
        
        # Skip if already set up (check for pubspec.yaml to verify it's a valid Flutter project)
        if os.path.exists(os.path.join(integration_dir, 'pubspec.yaml')):
            return integration_dir
            
        # Create the directory
        os.makedirs(integration_dir, exist_ok=True)
        
        # Copy contents from the template integration directory
        template_dir = os.path.join(self.root_dir, self.settings.integration_path)
        
        # Loop through all items in template directory and copy them
        for item in os.listdir(template_dir):
            source = os.path.join(template_dir, item)
            destination = os.path.join(integration_dir, item)
            
            if os.path.isdir(source):
                # Skip any existing output files
                if item == "build" or item == ".dart_tool":
                    continue
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
                
        return integration_dir
    
    def extract_dart_code(self, text: str) -> List[str]:
        """
        Extract Dart code blocks from text.
        
        Args:
            text (str): Raw text containing Dart code blocks
            
        Returns:
            List[str]: List of extracted Dart code blocks
        """
        pattern = r"```(?:dart|flutter)?\n(.*?)```"
        matches = re.finditer(pattern, text, re.DOTALL)
        dart_codes = []
        
        for match in matches:
            code = match.group(1).strip()
            if any(keyword in code for keyword in ['void main()', 'class', 'import', 'Widget']):
                dart_codes.append(code)
        
        return dart_codes
    
    def save_dart_code(self, code: str, index: int = 0) -> str:
        """
        Save Dart code to a file in the generations directory.
        
        Args:
            code (str): The Dart code to save
            index (int, optional): File index for naming
            
        Returns:
            str: Path to the saved file
        """
        # Make sure we're in the root directory
        os.chdir(self.root_dir)
        
        # Generate filename using generation_id
        if index == 0:
            filename = os.path.join(self.generations_dir, f'{self.generation_id}.dart')
        else:
            filename = os.path.join(self.generations_dir, f'{self.generation_id}_{index + 1}.dart')
        
        # Write the code to file
        with open(filename, 'w') as f:
            f.write(code)
        
        # Store the latest code
        self.latest_code = code
        
        return filename
    
    def copy_to_integration(self, source_file: str) -> bool:
        """
        Copy generated code to the integration project's main.dart file.
        
        Args:
            source_file (str): Path to the source code file
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        try:
            # Make sure we're in the root directory
            os.chdir(self.root_dir)
            
            # Set up the integration directory for this project (only once)
            integration_dir = self._setup_integration_dir()
            
            # Read the source code
            with open(source_file, 'r') as source:
                code = source.read()
            
            # Ensure integration directory exists with lib subfolder
            integration_lib_path = os.path.join(integration_dir, 'lib')
            os.makedirs(integration_lib_path, exist_ok=True)
            
            # Write to main.dart
            main_dart_path = os.path.join(integration_lib_path, 'main.dart')
            with open(main_dart_path, 'w') as target:
                target.write(code)
            
            return True
        except Exception as e:
            print(f"Error copying code: {str(e)}")
            return False
    
    def analyze_flutter_code(self) -> Tuple[bool, str]:
        """
        Analyze Flutter code for errors.
        
        Returns:
            Tuple[bool, str]: Success status and error message if any
        """
        try:
            # Set up the integration directory if not already done
            integration_dir = self._setup_integration_dir()
            
            # Change to integration directory
            os.chdir(integration_dir)
            
            # Run Flutter analyze command
            process = subprocess.Popen(
                'flutter analyze lib/main.dart --no-fatal-infos',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Collect output with timeout
            output = []
            def collect_output():
                for line in process.stdout:
                    output.append(line)
            
            # Start output collection thread
            thread = threading.Thread(target=collect_output)
            thread.daemon = True
            thread.start()
            
            # Wait for process to complete with timeout
            try:
                exit_code = process.wait(timeout=300)  # 5 minute timeout
                thread.join(timeout=1)
                collected_output = ''.join(output)
                
                # Change back to root directory
                os.chdir(self.root_dir)
                
                # Check for analysis issues
                if exit_code != 0 or "error" in collected_output.lower() or "warning" in collected_output.lower():
                    return False, collected_output
                return True, ""
            except subprocess.TimeoutExpired:
                process.kill()
                os.chdir(self.root_dir)
                return False, "Flutter analyze command timed out after 300 seconds"
                
        except Exception as e:
            # Make sure we're back in the root directory
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return False, f"Error analyzing Flutter code: {str(e)}"
            
    def cleanup(self):
        """
        Clean up resources after generation is complete or failed.
        Only removes the generation directory if needed.
        """
        try:
            if self.settings.auto_cleanup and os.path.exists(self.project_dir):
                shutil.rmtree(self.project_dir)
        except Exception as e:
            print(f"Error cleaning up project files: {str(e)}") 