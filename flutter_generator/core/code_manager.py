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
        # Map of file paths to content
        self.files = {}
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
            
        # Create the directory structure
        os.makedirs(integration_dir, exist_ok=True)
        
        # Copy contents from the template integration directory
        template_dir = os.path.join(self.root_dir, self.settings.integration_path)
        
        if not os.path.exists(template_dir):
            raise ValueError(f"Template integration directory not found at: {template_dir}")
        
        print(f"Copying integration template from {template_dir} to {integration_dir}")
        
        # Loop through all items in template directory and copy them
        for item in os.listdir(template_dir):
            source = os.path.join(template_dir, item)
            destination = os.path.join(integration_dir, item)
            
            if os.path.isdir(source):
                # Skip any existing output files
                if item == "build" or item == ".dart_tool":
                    continue
                # Ensure the destination directory exists
                os.makedirs(destination, exist_ok=True)
                # Use shutil.copytree with dirs_exist_ok parameter
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                # Copy the file
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
    
    def parse_file_blocks(self, generated_text: str) -> List[dict]:
        """
        Parse multi-file code blocks from generated text.
        
        Args:
            generated_text (str): Raw text containing multi-file code blocks
            
        Returns:
            List[dict]: List of file operations containing path and content
        """
        # Updated pattern to only capture file path and content
        pattern = r'<file path="([^"]+)"[^>]*>\n(.*?)</file>'
        matches = re.finditer(pattern, generated_text, re.DOTALL)
        
        file_operations = []
        for match in matches:
            path = match.group(1)
            content = match.group(2).rstrip()  # Remove trailing whitespace
            
            # Handle case where content might start with a newline
            if content.startswith('\n'):
                content = content[1:]
            
            file_operations.append({
                "path": path,
                "content": content
            })
        
        return file_operations
    
    def add_file(self, path: str, content: str) -> None:
        """
        Add or replace a file in the project.
        
        Args:
            path (str): The path of the file relative to the integration directory
            content (str): The complete content to write to the file
        """
        # Make sure we have a files dictionary to track all files
        if not hasattr(self, 'files'):
            self.files = {}
            
        # Store the complete file content
        self.files[path] = content
    
    def save_files(self) -> List[str]:
        """
        Save all files to the project directory.
        
        Returns:
            List[str]: Paths to all saved files
        """
        saved_files = []
        
        # Make sure we're in the root directory
        os.chdir(self.root_dir)
        
        # Check if we have files to save
        if not hasattr(self, 'files') or not self.files:
            return saved_files
        
        # Save each file
        for path, content in self.files.items():
            full_path = os.path.join(self.integration_path, path)
            
            # Create directory structure if needed
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write the file
            with open(full_path, 'w') as f:
                f.write(content)
            
            saved_files.append(full_path)
            
            # If this is a Dart file, store the latest code
            if path.endswith('.dart') and 'main.dart' in path:
                self.latest_code = content
        
        return saved_files
    
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
        Copy generated code to the integration project.
        If the source file contains multi-file blocks, extracts and saves each file.
        Otherwise, falls back to copying the entire file to main.dart.
        
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
            
            # Check if the code contains multi-file blocks
            file_operations = self.parse_file_blocks(code)
            
            if file_operations:
                # Process multi-file code
                for file_op in file_operations:
                    self.add_file(
                        path=file_op['path'],
                        content=file_op['content']
                    )
                
                # Save all files
                self.save_files()
                
                # For backward compatibility, set latest_code to main.dart if present
                main_dart_path = 'lib/main.dart'
                if main_dart_path in self.files:
                    self.latest_code = self.files[main_dart_path]
            else:
                # Legacy mode - assume it's a single file for main.dart
                # Ensure integration directory exists with lib subfolder
                integration_lib_path = os.path.join(integration_dir, 'lib')
                os.makedirs(integration_lib_path, exist_ok=True)
                
                # Write to main.dart
                main_dart_path = os.path.join(integration_lib_path, 'main.dart')
                with open(main_dart_path, 'w') as target:
                    target.write(code)
                
                # Store in files dictionary for consistency
                self.files['lib/main.dart'] = code
                
                # Set latest code
                self.latest_code = code
            
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
            
            # Get list of Dart files to analyze
            dart_files = []
            for root, _, files in os.walk(os.path.join(integration_dir, 'lib')):
                for file in files:
                    if file.endswith('.dart'):
                        # Get relative path from integration directory
                        rel_path = os.path.relpath(os.path.join(root, file), integration_dir)
                        dart_files.append(rel_path)
            
            if not dart_files:
                return True, "No Dart files to analyze"
            
            # Prepare analyze command to analyze all Dart files
            analyze_cmd = 'flutter analyze ' + ' '.join(dart_files) + ' --no-fatal-infos'
            
            # Run Flutter analyze command
            process = subprocess.Popen(
                analyze_cmd,
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
            
    def analyze_project(self) -> dict:
        """
        Perform project-wide analysis on all files.
        
        Returns:
            dict: Analysis results containing status, issues, and statistics
        """
        results = {
            "success": True,
            "message": "",
            "issues": [],
            "statistics": {
                "total_files": 0,
                "dart_files": 0,
                "yaml_files": 0,
                "total_lines": 0,
                "file_types": {}
            }
        }
        
        try:
            # Make sure integration directory exists
            integration_dir = self._setup_integration_dir()
            
            # Check if we have files
            if not hasattr(self, 'files') or not self.files:
                results["success"] = False
                results["message"] = "No files to analyze"
                return results
            
            # Count files by type
            for path in self.files:
                results["statistics"]["total_files"] += 1
                
                # Get file extension
                _, ext = os.path.splitext(path)
                ext = ext.lstrip('.')
                
                # Count file type
                if ext not in results["statistics"]["file_types"]:
                    results["statistics"]["file_types"][ext] = 0
                results["statistics"]["file_types"][ext] += 1
                
                # Count specific file types
                if ext == "dart":
                    results["statistics"]["dart_files"] += 1
                elif ext == "yaml" or ext == "yml":
                    results["statistics"]["yaml_files"] += 1
                
                # Count lines
                line_count = self.files[path].count('\n') + 1
                results["statistics"]["total_lines"] += line_count
            
            # Check for main.dart existence
            if "lib/main.dart" not in self.files:
                results["issues"].append({
                    "severity": "error",
                    "message": "Missing main.dart file",
                    "path": "lib/main.dart"
                })
            
            # Check pubspec.yaml
            if "pubspec.yaml" not in self.files:
                results["issues"].append({
                    "severity": "warning",
                    "message": "Missing pubspec.yaml file",
                    "path": "pubspec.yaml"
                })
            
            # Analyze Dart code
            dart_success, dart_message = self.analyze_flutter_code()
            if not dart_success:
                results["success"] = False
                results["message"] = "Dart code analysis failed"
                
                # Parse analysis output to extract specific issues
                for line in dart_message.split('\n'):
                    if "error" in line.lower() or "warning" in line.lower():
                        # Extract file path from error message if possible
                        path_match = re.search(r'lib/[^\s:]+', line)
                        path = path_match.group(0) if path_match else "unknown"
                        
                        # Extract severity
                        severity = "error" if "error" in line.lower() else "warning"
                        
                        results["issues"].append({
                            "severity": severity,
                            "message": line.strip(),
                            "path": path
                        })
            
            # Dependency analysis for pubspec.yaml
            if "pubspec.yaml" in self.files:
                # Check for Flutter SDK dependency
                if "sdk: " not in self.files["pubspec.yaml"]:
                    results["issues"].append({
                        "severity": "warning",
                        "message": "Missing Flutter SDK constraint in pubspec.yaml",
                        "path": "pubspec.yaml"
                    })
                
                # Check for common required packages
                for package in ["flutter", "cupertino_icons"]:
                    if package not in self.files["pubspec.yaml"]:
                        results["issues"].append({
                            "severity": "info",
                            "message": f"Missing common package: {package}",
                            "path": "pubspec.yaml"
                        })
            
            # Determine overall status based on issues
            has_errors = any(issue["severity"] == "error" for issue in results["issues"])
            if has_errors:
                results["success"] = False
                results["message"] = "Analysis found critical issues"
            elif results["issues"]:
                results["message"] = "Analysis found non-critical issues"
            else:
                results["message"] = "Analysis completed successfully"
            
            return results
            
        except Exception as e:
            results["success"] = False
            results["message"] = f"Error during project analysis: {str(e)}"
            return results
    
    def convert_to_multi_file_format(self, dart_code: str) -> str:
        """
        Convert a single Dart file to multi-file format.
        This is useful for transitioning legacy code to the new format.
        
        Args:
            dart_code (str): Single dart file content
            
        Returns:
            str: Multi-file formatted code
        """
        # Check if already in multi-file format
        if "<file path=" in dart_code:
            return dart_code
        
        # Create a basic Flutter app structure with the provided code as main.dart
        multi_file_code = f"""<file path="lib/main.dart">
{dart_code}
</file>

<file path="pubspec.yaml" section="dependencies">
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
</file>
"""
        return multi_file_code
    
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