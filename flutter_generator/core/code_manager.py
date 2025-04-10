"""
Code management utilities for the Flutter code generator.
"""

import os
import re
import subprocess
import threading
from typing import List, Tuple

from flutter_generator.config import Settings

class FlutterCodeManager:
    """
    Manager for Flutter code file operations.
    """
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the code manager.
        
        Args:
            settings (Settings, optional): Settings for configuration
        """
        self.settings = settings or Settings()
        self.latest_code = None
        self.root_dir = os.getcwd()
    
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
        Save Dart code to a file.
        
        Args:
            code (str): The Dart code to save
            index (int, optional): File index for naming
            
        Returns:
            str: Path to the saved file
        """
        # Make sure we're in the root directory
        os.chdir(self.root_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.settings.output_path, exist_ok=True)
        
        # Generate filename
        filename = os.path.join(
            self.settings.output_path, 
            f'flutter_code_{index + 1}.dart'
        )
        
        # Write the code to file
        with open(filename, 'w') as f:
            f.write(code)
        
        # Store the latest code
        self.latest_code = code
        
        return filename
    
    def copy_to_integration(self, source_file: str) -> bool:
        """
        Copy generated code to the integration project.
        
        Args:
            source_file (str): Path to the source code file
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        try:
            # Make sure we're in the root directory
            os.chdir(self.root_dir)
            
            # Read the source code
            with open(source_file, 'r') as source:
                code = source.read()
            
            # Ensure integration directory exists with lib subfolder
            integration_lib_path = os.path.join(self.settings.integration_path, 'lib')
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
                exit_code = process.wait(timeout=15)  # 15 second timeout
                thread.join(timeout=1)
                collected_output = ''.join(output)
                
                # Check for analysis issues
                if exit_code != 0 or "error" in collected_output.lower() or "warning" in collected_output.lower():
                    return False, collected_output
                return True, ""
            except subprocess.TimeoutExpired:
                process.kill()
                return False, "Flutter analyze command timed out after 15 seconds"
                
        except Exception as e:
            return False, f"Error analyzing Flutter code: {str(e)}" 