import asyncio
import websockets
import json
import sys
import argparse

# Configuration
API_URL = "http://localhost:8001"

async def test_websocket_connection(project_id):
    """Test WebSocket connection and basic message exchange"""
    websocket_url = f"ws://localhost:8001/ws/{project_id}"
    print(f"\n=== Testing WebSocket connection to: {websocket_url} ===")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            print("✓ WebSocket connection established successfully")
            
            # Receive initial connection message
            response = await asyncio.wait_for(websocket.recv(), timeout=2)
            print(f"Received message: {response}")
            
            # Send a compile command
            print("Sending 'compile' command...")
            await websocket.send("compile")
            
            # Wait for several responses
            try:
                for _ in range(3):  # Try to get a few messages
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print(f"Received message: {response}")
            except asyncio.TimeoutError:
                print("No more messages received within timeout period")
            
            return True
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"✗ Connection closed with error: {e}")
        return False
    except ConnectionRefusedError:
        print(f"✗ Connection refused. Is the server running?")
        return False
    except Exception as e:
        print(f"✗ WebSocket test failed with error: {e}")
        return False

async def main():
    parser = argparse.ArgumentParser(description='Test WebSocket functionality')
    parser.add_argument('--project-id', type=str, required=True, 
                        help='Project ID to use for WebSocket testing')
    args = parser.parse_args()
    
    # Test WebSocket with the provided project ID
    success = await test_websocket_connection(args.project_id)
    
    # Print result
    print("\n=== WebSocket Test Result ===")
    print(f"WebSocket functionality: {'✓ SUCCESS' if success else '✗ FAILED'}")
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main()) 