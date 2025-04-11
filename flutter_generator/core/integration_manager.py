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
        self.flutter_process = None
    
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
    
    def start_flutter_app(self) -> Optional[str]:
        """
        Start the Flutter app using flutter run.
        
        Returns:
            Optional[str]: URL or connection info to access the app, or None if failed
        """
        try:
            # Kill any existing Flutter process
            self.stop_flutter_app()
            
            # Ensure we're in the integration directory
            os.chdir(os.path.join(self.root_dir, self.settings.integration_path))
            
            # Start Flutter run in the background
            print(f"Starting Flutter run in {os.getcwd()}")
            
            # Use a different approach to start Flutter
            flutter_cmd = "flutter run -d web-server --web-port 8080"
            
            # Try alternate ports if default is in use
            port = 8080
            for attempt in range(3):
                try:
                    cmd = f"flutter run -d web-server --web-port {port}"
                    print(f"Attempting to start Flutter on port {port}")
                    
                    self.flutter_process = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    
                    # Wait a bit to see if Flutter starts successfully
                    time.sleep(5)
                    
                    # Check if the process is still running
                    if self.flutter_process.poll() is None:
                        print(f"Flutter dev server started successfully on port {port}")
                        # Restore working directory
                        os.chdir(self.root_dir)
                        
                        # Return the URL for the Flutter web app
                        return f"http://localhost:{port}"
                    else:
                        # Process exited, check output
                        output, _ = self.flutter_process.communicate(timeout=1)
                        print(f"Flutter failed to start on port {port}: {output}")
                        # Try next port
                        port += 1
                        
                except Exception as e:
                    print(f"Error starting Flutter on port {port}: {str(e)}")
                    port += 1
            
            # Restore working directory if we reach here
            os.chdir(self.root_dir)
            
            print("Failed to start Flutter app after multiple attempts")
            return None
            
        except Exception as e:
            print(f"Error starting Flutter app: {str(e)}")
            # Restore working directory
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return None
    
    def stop_flutter_app(self):
        """Stop the Flutter app if it's running."""
        if self.flutter_process and self.flutter_process.poll() is None:
            try:
                # Try to terminate gracefully first
                self.flutter_process.terminate()
                time.sleep(2)
                
                # Force kill if still running
                if self.flutter_process.poll() is None:
                    self.flutter_process.kill()
                    
                print("Flutter app stopped")
            except Exception as e:
                print(f"Error stopping Flutter app: {str(e)}")
            
            self.flutter_process = None 