#!/bin/bash
# Script to start the FastAPI server on port 8001 to avoid conflicts with Docker

# Kill any existing uvicorn processes
pkill -f "uvicorn api.main:app" 2>/dev/null

# Set the Python path to the current directory
export PYTHONPATH=$PWD

# Start the server on port 8001 with increased timeout
echo "Starting server on http://localhost:8001"
python -m uvicorn api.main:app --port 8001 --timeout-keep-alive 120 