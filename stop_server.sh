#!/bin/bash
# Script to stop the LikeMinds Flutter Integration Assistant API server gracefully

LOG_DIR="logs"
PID_FILE="$LOG_DIR/server.pid"

# Function to gracefully stop a process
graceful_stop() {
    local pid=$1
    local max_wait=10  # Maximum seconds to wait
    
    # Check if process exists
    if ! ps -p $pid > /dev/null; then
        echo "Process $pid is not running."
        return 0
    fi
    
    echo "Sending SIGTERM to process $pid..."
    kill -15 $pid 2>/dev/null
    
    # Wait for graceful shutdown
    for i in $(seq 1 $max_wait); do
        if ! ps -p $pid > /dev/null; then
            echo "Process $pid stopped gracefully."
            return 0
        fi
        sleep 1
        echo "Waiting for process to stop... ($i/$max_wait)"
    done
    
    # Force kill if still running
    echo "Process didn't stop gracefully. Sending SIGKILL..."
    kill -9 $pid 2>/dev/null
    
    # Check if process is gone
    if ps -p $pid > /dev/null; then
        echo "Failed to kill process $pid!"
        return 1
    else
        echo "Process $pid forcefully terminated."
        return 0
    fi
}

# Check for PID file
if [ -f "$PID_FILE" ]; then
    SERVER_PID=$(cat "$PID_FILE")
    echo "Found server PID: $SERVER_PID"
    graceful_stop $SERVER_PID
    
    # Clean up PID file
    rm -f "$PID_FILE"
else
    echo "No PID file found. Trying to find server process..."
    
    # Try to find the server process
    SERVER_PIDS=$(pgrep -f "uvicorn api.main:app")
    
    if [ -z "$SERVER_PIDS" ]; then
        echo "No server processes found."
        exit 0
    fi
    
    # Stop each found process
    for pid in $SERVER_PIDS; do
        echo "Found server process: $pid"
        graceful_stop $pid
    done
fi

echo "Server shutdown complete." 