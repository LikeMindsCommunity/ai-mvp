#!/usr/bin/env python

"""
Entry point script to start the Flutter Integration Assistant API server.
"""

import os
import sys
import signal
import subprocess
import atexit
from api.main import start

def cleanup_flutter_processes():
    """Kill any running Flutter processes when server exits."""
    print("Shutting down - cleaning up Flutter processes...")
    
    if os.name == 'posix':  # Linux/Mac
        try:
            # Use pkill to forcefully kill any Flutter processes
            print("Looking for Flutter processes to terminate...")
            check_cmd = "ps aux | grep 'flutter run' | grep -v grep"
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"Found Flutter processes to terminate:\n{result.stdout}")
                # Use SIGKILL (-9) to ensure processes are terminated
                kill_cmd = "pkill -9 -f 'flutter run'"
                subprocess.run(kill_cmd, shell=True)
                print("Flutter processes terminated successfully.")
            else:
                print("No Flutter processes found.")
        except Exception as e:
            print(f"Error cleaning up Flutter processes: {e}")

def signal_handler(sig, frame):
    """Handle termination signals (SIGINT, SIGTERM)."""
    print(f"Received signal {sig}, shutting down server...")
    cleanup_flutter_processes()
    sys.exit(0)

if __name__ == "__main__":
    # Register cleanup handler to run on exit
    atexit.register(cleanup_flutter_processes)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Docker stop
    
    # Check if required files exist
    required_files = ['prompt.txt', 'docs.txt', 'code.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file '{file}' not found")
            sys.exit(1)
    
    # Check if integration directory exists
    if not os.path.exists('integration'):
        print("Error: 'integration' directory not found")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    print("Starting Flutter Integration Assistant API...")
    try:
        start()
    finally:
        # Ensure cleanup happens even if start() raises an exception
        cleanup_flutter_processes() 