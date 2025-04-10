#!/bin/bash
# Production server script for LikeMinds Flutter Integration Assistant API
# This script includes enhanced error handling and proper logging

# Configuration
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/server.log"
PORT=8001
HOST="0.0.0.0"
WORKERS=4  # Number of worker processes (adjust based on CPU cores)

# Create log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo "Created log directory: $LOG_DIR"
fi

# Function to check if a port is already in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "Warning: Port $port is already in use!"
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        echo "Process using port $port: $(ps -p $pid -o comm=)"
        return 1
    fi
    return 0
}

# Function to kill any existing server instances
kill_existing_server() {
    echo "Checking for existing server processes..."
    if pgrep -f "uvicorn api.main:app" > /dev/null; then
        echo "Stopping existing server processes..."
        pkill -f "uvicorn api.main:app"
        sleep 2
    fi
}

# Start the server with proper configuration
start_server() {
    # Set the Python path to the current directory
    export PYTHONPATH=$PWD
    
    # Ensure projects directory exists
    mkdir -p projects
    
    # Start the server with production settings
    echo "Starting server on http://$HOST:$PORT with $WORKERS workers"
    echo "Logs will be written to $LOG_FILE"
    
    # Use logging, workers, and proper timeouts
    python -m uvicorn api.main:app \
        --host $HOST \
        --port $PORT \
        --workers $WORKERS \
        --log-level info \
        --timeout-keep-alive 120 \
        --log-config=none \
        >> "$LOG_FILE" 2>&1 &
    
    # Store the process ID
    SERVER_PID=$!
    echo "Server started with PID: $SERVER_PID"
    echo $SERVER_PID > "$LOG_DIR/server.pid"
    
    # Wait a moment and check if the server is still running
    sleep 3
    if ps -p $SERVER_PID > /dev/null; then
        echo "Server is running successfully!"
        echo "To check logs: tail -f $LOG_FILE"
        echo "To stop the server: ./stop_server.sh"
    else
        echo "Error: Server failed to start! Check logs for details."
        tail -n 20 "$LOG_FILE"
        exit 1
    fi
}

# Main execution
echo "=== LikeMinds Flutter Integration Assistant API ==="
echo "Starting production server..."

# Check Docker status (warn but continue if not available)
if ! docker info > /dev/null 2>&1; then
    echo "Warning: Docker is not available. Some functionality will be limited."
fi

# Kill any existing server instances
kill_existing_server

# Check if the port is available
if check_port $PORT; then
    # Start the server
    start_server
else
    echo "Error: Could not start server because port $PORT is in use."
    echo "Please free up the port or change the PORT variable in this script."
    exit 1
fi 