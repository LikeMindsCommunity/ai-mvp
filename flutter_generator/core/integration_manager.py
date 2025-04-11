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
            
            # Debug info about the environment
            # print(f"Current directory: {os.getcwd()}")
            # print(f"Directory content: {os.listdir('.')}")
            print(f"Flutter version: {subprocess.check_output('flutter --version', shell=True).decode()}")
            
            # Verify Flutter is installed and working
            flutter_check = subprocess.run('which flutter', shell=True, capture_output=True, text=True)
            if flutter_check.returncode != 0:
                print("ERROR: Flutter command not found. Make sure Flutter is installed and in PATH.")
                os.chdir(self.root_dir)
                return None
            
            # print(f"Flutter binary location: {flutter_check.stdout.strip()}")
            
            # Use environment variables or defaults for host and port
            host = os.environ.get("WEB_HOST", "localhost")
            port = int(os.environ.get("FLUTTER_WEB_PORT", "8080"))
            
            # Create a log file for Flutter output
            log_dir = os.path.join(self.root_dir, "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "flutter.log")
            
            # Run flutter pub get first to make sure dependencies are updated
            print("Running flutter pub get...")
            pub_get = subprocess.run('flutter pub get', shell=True, capture_output=True, text=True)
            print(f"flutter pub get output: {pub_get.stdout}")
            if pub_get.stderr:
                print(f"flutter pub get errors: {pub_get.stderr}")
            
            # Construct the command for running Flutter web
            cmd = f"flutter run -d web-server --web-port {port} --web-hostname {host}"
            print(f"Running Flutter command: {cmd}")
            
            # Modified approach for Docker: start process in background but keep output visible
            if os.name == 'posix':  # Linux/Mac
                # Create a script file to run the Flutter command
                script_path = os.path.join(log_dir, "run_flutter.sh")
                with open(script_path, 'w') as script:
                    script.write("#!/bin/bash\n")
                    script.write(f"cd {os.getcwd()}\n")
                    script.write(f"{cmd} | tee {log_file}")
                
                # Make the script executable
                os.chmod(script_path, 0o755)
                
                # Run the script in background but redirect output to both console and file
                print("STARTING FLUTTER IN BACKGROUND (output will appear in Docker logs)")
                process_cmd = f"bash {script_path} &"
                os.system(process_cmd)
                
                # Wait a bit to let things start
                time.sleep(5)
                
                # Check if Flutter mentions the web server is running in the log file
                try:
                    with open(log_file, 'r') as f:
                        log_content = f.read()
                        if "is being served at" in log_content:
                            print("FLUTTER SERVER STARTED SUCCESSFULLY!")
                            print(log_content)
                        else:
                            print("Waiting for Flutter server to start...")
                            print("Current log content:")
                            print(log_content)
                except Exception as e:
                    print(f"Error reading log file: {str(e)}")
            else:
                # Windows approach
                print("Running on Windows is not fully supported in Docker")
                with open(log_file, 'w') as f:
                    self.flutter_process = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    
                    # Start a thread to continuously read and print output
                    def log_output():
                        for line in self.flutter_process.stdout:
                            print(f"FLUTTER > {line.strip()}")
                            f.write(line)
                            f.flush()
                    
                    thread = threading.Thread(target=log_output)
                    thread.daemon = True
                    thread.start()
            
            print(f"Flutter web server should be running at http://{host}:{port}")
            print(f"Process started. Check Docker logs for Flutter output.")
            
            # Return to root directory
            os.chdir(self.root_dir)
            
            # Return the URL
            return f"http://{host}:{port}"
            
        except Exception as e:
            print(f"Error starting Flutter app: {str(e)}")
            # Print traceback for better debugging
            import traceback
            traceback.print_exc()
            
            # Restore working directory
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return None
    
    def stop_flutter_app(self):
        """Stop the Flutter app if it's running."""
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
        
        # Always try to kill all Flutter processes using pkill on Linux/Mac
        if os.name == 'posix':
            try:
                print("Killing all Flutter processes...")
                # First check if any processes exist
                check_cmd = "ps aux | grep 'flutter run' | grep -v grep"
                result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    print(f"Found Flutter processes:\n{result.stdout}")
                    # Kill the processes
                    kill_cmd = "pkill -f 'flutter run'"
                    subprocess.run(kill_cmd, shell=True)
                    
                    # Double check if they're gone
                    time.sleep(1)
                    check_again = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                    if check_again.returncode == 0 and check_again.stdout.strip():
                        print("Processes still running, using stronger pkill...")
                        subprocess.run("pkill -9 -f 'flutter run'", shell=True)
                    
                    print("All Flutter processes terminated")
                else:
                    print("No Flutter processes found running")
            except Exception as e:
                print(f"Error in pkill: {str(e)}")
        
        # Reset the process reference
        self.flutter_process = None 