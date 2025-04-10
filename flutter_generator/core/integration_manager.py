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
            self.stop_web_server()
            
            # Ensure we're in the build/web directory of the integration project
            build_web_dir = os.path.join(self.root_dir, self.settings.integration_path, 'build', 'web')
            
            # Check if build/web directory exists
            if not os.path.exists(build_web_dir):
                print(f"Web build directory not found: {build_web_dir}")
                # Try to create it as a fallback
                os.makedirs(build_web_dir, exist_ok=True)
                # Create a simple index.html file as fallback
                with open(os.path.join(build_web_dir, 'index.html'), 'w') as f:
                    f.write('<html><body><h1>Flutter Build Not Found</h1><p>The Flutter web build did not complete successfully.</p></body></html>')
            
            # Start a simple HTTP server to serve the web build
            os.chdir(build_web_dir)
            
            # Use a different approach to start the server
            port = self.settings.web_port
            
            # Try alternate ports if the default is in use
            for attempt in range(3):
                try:
                    self.web_server_process = subprocess.Popen(
                        f"python -m http.server {port}",
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    
                    # Give the server a moment to start
                    time.sleep(2)
                    
                    # Check if the server started successfully
                    if self.web_server_process.poll() is None:
                        print(f"Web server started successfully on port {port}")
                        # Restore working directory
                        os.chdir(self.root_dir)
                        return f"http://{self.settings.web_host}:{port}"
                    else:
                        # Server failed to start, try another port
                        output, _ = self.web_server_process.communicate(timeout=1)
                        print(f"Failed to start web server on port {port}: {output}")
                        port += 1
                except Exception as e:
                    print(f"Error starting server on port {port}: {str(e)}")
                    port += 1
            
            # Restore working directory
            os.chdir(self.root_dir)
            
            print("Failed to start web server after multiple attempts")
            return None
            
        except Exception as e:
            print(f"Error serving web build: {str(e)}")
            # Restore working directory
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return None
    
    def stop_web_server(self):
        """Stop the web server if it's running."""
        if self.web_server_process and self.web_server_process.poll() is None:
            try:
                self.web_server_process.terminate()
                time.sleep(1)
                # Force kill if still running
                if self.web_server_process.poll() is None:
                    self.web_server_process.kill()
            except Exception as e:
                print(f"Error stopping web server: {str(e)}")
            
            self.web_server_process = None 