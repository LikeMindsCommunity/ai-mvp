"""
Integration manager for Flutter code builds and deployment.
"""

import os
import subprocess
import threading
import time
from typing import Tuple, Optional
import urllib.request
import urllib.error

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
            # First stop any existing Flutter web server processes
            self.stop_flutter_app()
            
            # Ensure we're in the integration directory
            os.chdir(os.path.join(self.root_dir, self.settings.integration_path))
            
            # Run flutter pub get to update dependencies
            print("Running flutter pub get...")
            subprocess.run('flutter pub get', shell=True, check=True)
            
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(self.root_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "flutter.log")
            
            # Get host and port from environment
            host = os.environ.get("WEB_HOST", "0.0.0.0") 
            port = int(os.environ.get("FLUTTER_WEB_PORT", "8080"))
            
            print(f"Starting Flutter web server on {host}:{port}...")
            cmd = f"flutter run -d web-server --web-port {port} --web-hostname {host}"
            
            # Start the process and redirect output to log file
            # Use nohup to keep it running if parent process exits
            start_cmd = f"nohup {cmd} > {log_file} 2>&1 &"
            subprocess.run(start_cmd, shell=True)
            
            # Function to verify if a web server is accepting connections
            def is_server_running(url, max_attempts=12, delay=5):
                """Check if a server is running by making an HTTP request."""
                print(f"Verifying web server at {url}...")
                
                for attempt in range(max_attempts):
                    try:
                        print(f"Attempt {attempt+1}/{max_attempts} to connect to {url}")
                        
                        # Try to open the URL with a timeout
                        response = urllib.request.urlopen(url, timeout=5)
                        
                        # If we get a response, the server is running
                        if response.getcode() == 200:
                            print(f"Server at {url} is responding!")
                            return True
                    except (urllib.error.URLError, ConnectionRefusedError) as e:
                        print(f"Server not responding yet: {e}")
                    except Exception as e:
                        print(f"Unexpected error checking server: {e}")
                        
                    # Check log file for errors
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            content = f.read()
                            if "Address already in use" in content:
                                print(f"Error: Port {port} is already in use!")
                                return False
                            elif "Failed to start" in content or "Error:" in content:
                                print(f"Error detected in logs: {content[-500:]}")
                                return False
                    
                    # Wait before next attempt
                    time.sleep(delay)
                
                print(f"Server verification timed out after {max_attempts * delay} seconds")
                return False
            
            # Check both log file and make an actual HTTP request
            local_url = f"http://{host}:{port}"
            
            # Get the public host for client-facing URLs
            public_host = os.environ.get("PUBLIC_HOST", "0.0.0.0")
            public_url = f"http://{public_host}:{port}"
            
            if is_server_running(local_url):
                print("Flutter web server confirmed running!")
                print(f"Public URL: {public_url}")
                os.chdir(self.root_dir)
                return local_url
            
            # If verification failed, check log for clues
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    content = f.read()
                    print(f"Server failed to start. Last log output:\n{content[-1000:]}")
            
            # Return to root directory
            os.chdir(self.root_dir)
            return None
            
        except Exception as e:
            print(f"Error starting Flutter app: {str(e)}")
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return None
    
    def stop_flutter_app(self):
        """Stop only Flutter web server processes while preserving other Flutter processes."""
        # Try to kill specific process if we have a reference
        if self.flutter_process and self.flutter_process.poll() is None:
            try:
                self.flutter_process.terminate()
                time.sleep(1)
                if self.flutter_process.poll() is None:
                    self.flutter_process.kill()
                print("Terminated specific Flutter process")
            except Exception as e:
                print(f"Error terminating specific process: {str(e)}")
        
        # Target only Flutter web server processes
        if os.name == 'posix':
            try:
                # First check if any Flutter web server processes exist
                # This is a very specific pattern that targets only web servers
                check_cmd = "ps aux | grep 'flutter.*run.*web-server' | grep -v grep"
                result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    print("Found Flutter web server processes:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"  {line.strip()}")
                    
                    # Kill only Flutter web server processes
                    kill_cmd = "pkill -f 'flutter.*run.*web-server'"
                    subprocess.run(kill_cmd, shell=True)
                    
                    # Double check if they're gone
                    time.sleep(1)
                    check_again = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                    if check_again.returncode == 0 and check_again.stdout.strip():
                        print("Web server processes still running, using stronger kill...")
                        subprocess.run("pkill -9 -f 'flutter.*run.*web-server'", shell=True)
                    
                    print("Flutter web server processes terminated")
                else:
                    print("No Flutter web server processes found running")
            except Exception as e:
                print(f"Error in process management: {str(e)}")
        
        # Reset the process reference
        self.flutter_process = None 