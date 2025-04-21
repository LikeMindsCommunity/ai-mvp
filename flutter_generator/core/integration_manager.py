"""
Integration manager for Flutter code builds and deployment.
"""

import os
import subprocess
import threading
import time
import pty
import select
import signal
import fcntl
import termios
import struct
from typing import Tuple, Optional, Dict, Any
import urllib.request
import urllib.error

from flutter_generator.config import Settings

class FlutterIntegrationManager:
    """
    Manager for Flutter integration and deployment.
    """
    
    def __init__(self, settings: Settings = None, generation_id: str = None, integration_path: str = None):
        """
        Initialize the integration manager.
        
        Args:
            settings (Settings, optional): Settings for configuration
            generation_id (str, optional): Unique ID for this generation
            integration_path (str, optional): Path to the integration directory for this generation
        """
        self.settings = settings or Settings()
        self.root_dir = os.getcwd()
        self.generation_id = generation_id
        self.integration_path = integration_path
        self.flutter_process = None
        self.process_fd = None
        self.process_pid = None
        self.process_thread = None
        self.is_running = False
        self.log_path = None
        
        # Set up log directory
        self._setup_log_directory()
    
    def _setup_log_directory(self):
        """Set up the log directory for this integration."""
        if self.generation_id:
            log_dir = os.path.join(self.root_dir, "logs", self.generation_id)
        else:
            log_dir = os.path.join(self.root_dir, "logs")
            
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = log_dir
    
    def run_command_with_timeout(self, cmd: str, timeout: int = None, working_dir: str = None) -> Tuple[int, str]:
        """
        Run a command with timeout and capture output.
        
        Args:
            cmd (str): Command to run
            timeout (int, optional): Timeout in seconds
            working_dir (str, optional): Directory to run command in
            
        Returns:
            Tuple[int, str]: Exit code and command output
        """
        if timeout is None:
            timeout = self.settings.command_timeout
            
        # Save current directory
        current_dir = os.getcwd()
        
        try:
            # Change to working directory if specified
            if working_dir:
                os.chdir(working_dir)
                
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
        finally:
            # Return to original directory
            os.chdir(current_dir)
    
    def _read_process_output(self, fd):
        """Read and handle output from the interactive Flutter process."""
        log_file = os.path.join(self.log_path, "flutter.log")
        
        with open(log_file, 'w') as log:
            while self.is_running:
                try:
                    # Use select to check if there's data to read
                    r, _, _ = select.select([fd], [], [], 0.5)
                    if not r:
                        continue
                        
                    output = os.read(fd, 4096).decode('utf-8', errors='replace')
                    if not output:
                        break
                        
                    # Write to log file and flush to ensure it's saved immediately
                    log.write(output)
                    log.flush()
                    
                    # Print to console for monitoring
                    print(output, end='', flush=True)
                except Exception as e:
                    print(f"Error reading process output: {str(e)}")
                    break
                    
        # Mark the process as no longer running when the output loop ends
        self.is_running = False
    
    def send_command_to_flutter(self, command: str) -> bool:
        """
        Send a command to the running Flutter process.
        
        Args:
            command (str): Single character command like 'r' for hot reload, 'R' for hot restart
            
        Returns:
            bool: True if command was sent successfully
        """
        if not self.is_running or self.process_fd is None:
            print("Cannot send command - Flutter process is not running")
            return False
            
        try:
            os.write(self.process_fd, command.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Failed to send command to Flutter process: {str(e)}")
            return False
    
    def start_flutter_app(self) -> Optional[str]:
        """
        Start the Flutter app using flutter run in interactive mode.
        
        Returns:
            Optional[str]: URL or connection info to access the app, or None if failed
        """
        try:
            # First stop any existing Flutter web server processes
            self.stop_flutter_app()
            
            # Determine integration directory to use
            integration_dir = self.integration_path
            if not integration_dir:
                integration_dir = os.path.join(self.root_dir, self.settings.integration_path)
            
            # Ensure we're in the integration directory
            os.chdir(integration_dir)
            
            # Run flutter pub get to update dependencies
            print("Running flutter pub get...")
            subprocess.run('flutter pub get', shell=True, check=True)
            
            # Get host and port from environment
            host = os.environ.get("WEB_HOST", "0.0.0.0") 
            port = int(os.environ.get("FLUTTER_WEB_PORT", "8080"))
            
            print(f"Starting Flutter web server on {host}:{port} in interactive mode...")
            cmd = f"flutter run -d web-server --web-port {port} --web-hostname {host}"
            
            # Start the process in a pseudo-terminal to allow for interactive commands
            master_fd, slave_fd = pty.openpty()
            
            # Set the terminal size to avoid Flutter UI issues
            rows, cols = 50, 120
            fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
            
            # Start the Flutter process connected to our PTY
            process = subprocess.Popen(
                cmd.split(),
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid,  # Start in a new session
                close_fds=True
            )
            
            # Close the slave side now that the child has it
            os.close(slave_fd)
            
            # Store process information
            self.flutter_process = process
            self.process_fd = master_fd
            self.process_pid = process.pid
            self.is_running = True
            
            # Start thread to read and handle output
            self.process_thread = threading.Thread(
                target=self._read_process_output,
                args=(master_fd,)
            )
            self.process_thread.daemon = True
            self.process_thread.start()
            
            print(f"Flutter process started with PID {process.pid}")
            
            # Function to verify if a web server is accepting connections
            def is_server_running(url, max_attempts=12, delay=5):
                """Check if a server is running by making an HTTP request."""
                print(f"Verifying web server at {url}...")
                
                for attempt in range(max_attempts):
                    try:
                        print(f"Attempt {attempt+1}/{max_attempts} to connect to {url}")
                        
                        # Try to open the URL with a timeout
                        # Add cache-busting parameter to the URL
                        cache_buster = f"?cb={int(time.time())}"
                        cache_bust_url = f"{url}{cache_buster}"
                        response = urllib.request.urlopen(cache_bust_url, timeout=5)
                        
                        # If we get a response, the server is running
                        if response.getcode() == 200:
                            print(f"Server at {url} is responding!")
                            return True
                    except (urllib.error.URLError, ConnectionRefusedError) as e:
                        print(f"Server not responding yet: {e}")
                    except Exception as e:
                        print(f"Unexpected error checking server: {e}")
                    
                    # Check if process is still running
                    if not self.is_running or process.poll() is not None:
                        print("Flutter process has terminated unexpectedly")
                        return False
                    
                    # Wait before next attempt
                    time.sleep(delay)
                
                print(f"Server verification timed out after {max_attempts * delay} seconds")
                return False
            
            # Check both log file and make an actual HTTP request
            local_url = f"http://{host}:{port}"
            
            time.sleep(15)
            if is_server_running(local_url):
                print("Flutter web server confirmed running!")
                os.chdir(self.root_dir)
                return local_url
            
            # If verification failed, stop the process
            self.stop_flutter_app()
            
            # Return to root directory
            os.chdir(self.root_dir)
            return None
            
        except Exception as e:
            print(f"Error starting Flutter app: {str(e)}")
            self.stop_flutter_app()
            if os.getcwd() != self.root_dir:
                os.chdir(self.root_dir)
            return None
    
    def hot_restart(self) -> bool:
        """Trigger a hot restart of the Flutter app."""
        return self.send_command_to_flutter('R')
    
    def hot_reload(self) -> bool:
        """Trigger a hot reload of the Flutter app."""
        return self.send_command_to_flutter('r')
    
    def stop_flutter_app(self):
        """Stop the running Flutter app and clean up resources."""
        # Check if we have a running process
        if self.flutter_process is not None:
            try:
                # Try to gracefully terminate first
                if self.process_pid:
                    print(f"Stopping Flutter process with PID {self.process_pid}...")
                    os.killpg(os.getpgid(self.process_pid), signal.SIGTERM)
                    
                    # Give it a moment to terminate
                    time.sleep(2)
                    
                    # If still running, force kill
                    if self.flutter_process.poll() is None:
                        os.killpg(os.getpgid(self.process_pid), signal.SIGKILL)
                        
            except Exception as e:
                print(f"Error stopping Flutter process: {str(e)}")
                
            # Clean up resources
            self.flutter_process = None
            self.process_pid = None
            
            # Close file descriptor if open
            if self.process_fd is not None:
                try:
                    os.close(self.process_fd)
                except:
                    pass
                self.process_fd = None
                
            # Reset flag
            self.is_running = False
            
            print("Flutter process stopped")
            
        # Also attempt to kill any stray flutter processes
        try:
            if os.name == 'posix':
                # For Unix-like systems (Linux, macOS)
                os.system("pkill -f 'flutter run -d web-server'")
            else:
                # For Windows
                os.system("taskkill /F /IM flutter.exe")
        except:
            pass 