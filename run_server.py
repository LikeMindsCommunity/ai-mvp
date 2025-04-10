#!/usr/bin/env python

"""
Entry point script to start the Flutter Integration Assistant API server.
"""

import os
import sys
from api.main import start

if __name__ == "__main__":
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
    start() 