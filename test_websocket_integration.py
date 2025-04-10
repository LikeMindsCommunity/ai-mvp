import asyncio
import websockets
import requests
import json
import sys
import time
import argparse
from datetime import datetime

# Configuration
API_URL = "http://localhost:8001"

def log_message(message, level="INFO"):
    """Print a formatted log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

async def test_websocket(project_id, timeout=10):
    """Test WebSocket connection and basic functionality"""
    websocket_url = f"ws://localhost:8001/ws/{project_id}"
    log_message(f"Connecting to WebSocket: {websocket_url}")
    
    try:
        async with websockets.connect(websocket_url, ping_interval=None, close_timeout=5) as websocket:
            log_message("WebSocket connection established", "SUCCESS")
            
            # Wait for initial message
            log_message("Waiting for initial connection message...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
                log_message(f"Received: {response}", "SUCCESS")
            except asyncio.TimeoutError:
                log_message("Timeout waiting for initial message", "ERROR")
                return False
            
            # Send compile command
            log_message("Sending 'compile' command...")
            await websocket.send("compile")
            
            # Wait for responses
            message_count = 0
            success = False
            try:
                start_time = time.time()
                while time.time() - start_time < timeout and message_count < 3:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    log_message(f"Received message {message_count + 1}: {response}")
                    message_count += 1
                    
                    # Check if we received a completion message
                    try:
                        data = json.loads(response)
                        if data.get('type') == 'completion' and data.get('data', {}).get('success'):
                            log_message("Received successful completion message", "SUCCESS")
                            success = True
                    except:
                        pass
            except asyncio.TimeoutError:
                log_message(f"No more messages received after {message_count} messages")
            
            return success or message_count > 0
            
    except websockets.exceptions.ConnectionClosedError as e:
        log_message(f"WebSocket connection closed with error: {e}", "ERROR")
        return False
    except ConnectionRefusedError:
        log_message("Connection refused. Is the server running?", "ERROR")
        return False
    except Exception as e:
        log_message(f"WebSocket test failed: {str(e)}", "ERROR")
        return False

def create_test_project():
    """Create a test project and return its ID"""
    url = f"{API_URL}/api/v1/generate"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "Create a simple Flutter app with a counter",
        "project_id": None
    }
    
    log_message(f"Creating test project via {url}...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            project_id = response_data.get('project_id')
            if project_id:
                log_message(f"Project created successfully with ID: {project_id}", "SUCCESS")
                return project_id
            else:
                log_message("No project ID returned in the response", "ERROR")
                return None
        else:
            log_message(f"Failed to create project. Status code: {response.status_code}", "ERROR")
            log_message(f"Response: {response.text}", "ERROR")
            return None
    except Exception as e:
        log_message(f"Error creating project: {str(e)}", "ERROR")
        return None

def check_project_exists(project_id):
    """Check if a project exists"""
    try:
        url = f"{API_URL}/debug/project/{project_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('exists', False)
        return False
    except Exception as e:
        log_message(f"Error checking project: {str(e)}", "ERROR")
        return False

async def main():
    parser = argparse.ArgumentParser(description='Test WebSocket functionality')
    parser.add_argument('--project-id', type=str, help='Use an existing project ID instead of creating a new one')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds for WebSocket operations')
    args = parser.parse_args()
    
    project_id = args.project_id
    
    # If no project ID is provided, create a new one
    if not project_id:
        project_id = create_test_project()
        if not project_id:
            log_message("Failed to create a test project. Exiting.", "ERROR")
            sys.exit(1)
    else:
        # Check if the provided project exists
        if check_project_exists(project_id):
            log_message(f"Using existing project: {project_id}", "INFO")
        else:
            log_message(f"Project {project_id} does not exist", "WARNING")
    
    # Test WebSocket connection
    success = await test_websocket(project_id, args.timeout)
    
    # Print summary
    log_message("\n=== Test Results ===")
    if success:
        log_message("WebSocket test completed successfully", "SUCCESS")
        sys.exit(0)
    else:
        log_message("WebSocket test failed", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 