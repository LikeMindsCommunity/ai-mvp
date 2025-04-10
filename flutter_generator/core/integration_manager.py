"""
Integration manager for Flutter code builds and deployment.
"""

import os
import subprocess
import threading
import time
from typing import Tuple, Optional

from flutter_generator.config import Settings

class FlutterIntegrationManager:
    """
    Manager for Flutter integration and deployment.
    """
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the integration manager.
        
        Args:
            settings (Settings, optional): Settings for configuration
        """
        self.settings = settings or Settings()
        self.root_dir = os.getcwd()
        self.web_server_process = None
    
    def run_command_with_timeout(self, cmd: str, timeout: int = None) -> Tuple[int, str]:
        """
        Run a command with timeout and capture output.
        
        Args:
            cmd (str): Command to run
            timeout (int, optional): Timeout in seconds
            
        Returns:
            Tuple[int, str]: Exit code and command output
        """
        if timeout is None:
            timeout = self.settings.command_timeout
        
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True
        )
        
        output = []
        def collect_output():
            for line in process.stdout:
                output.append(line)
        
        thread = threading.Thread(target=collect_output)
        thread.daemon = True
        thread.start()
        
        try:
            exit_code = process.wait(timeout=timeout)
            thread.join(timeout=1)
            return exit_code, ''.join(output)
        except subprocess.TimeoutExpired:
            process.kill()
            return -1, f"Command timed out after {timeout} seconds: {cmd}"
    
    def serve_web_build(self) -> Optional[str]:
        """
        Serve the Flutter web build using a local server.
        
        Returns:
            Optional[str]: URL to access the web app, or None if failed
        """
        try:
            # Kill any existing server process
            if self.web_server_process and self.web_server_process.poll() is None:
                self.web_server_process.terminate()
                time.sleep(1)
            
            # Ensure we're in the build/web directory of the integration project
            build_web_dir = os.path.join(self.root_dir, self.settings.integration_path, 'build', 'web')
            
            # Check if build/web directory exists
            if not os.path.exists(build_web_dir):
                print(f"Web build directory not found: {build_web_dir}")
                return None
            
            # Start a simple HTTP server to serve the web build
            os.chdir(build_web_dir)
            self.web_server_process = subprocess.Popen(
                f"python -m http.server {self.settings.web_port}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Give the server a moment to start
            time.sleep(1)
            
            # Check if the server started successfully
            if self.web_server_process.poll() is not None:
                print("Failed to start web server")
                return None
            
            # Restore working directory
            os.chdir(self.root_dir)
            
            # Return the URL to access the web app
            return f"http://{self.settings.web_host}:{self.settings.web_port}"
            
        except Exception as e:
            print(f"Error serving web build: {str(e)}")
            return None
    
    def stop_web_server(self):
        """Stop the web server if it's running."""
        if self.web_server_process and self.web_server_process.poll() is None:
            self.web_server_process.terminate()
            time.sleep(1)
            # Force kill if still running
            if self.web_server_process.poll() is None:
                self.web_server_process.kill()
            
            self.web_server_process = None 