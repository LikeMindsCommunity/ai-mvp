#!/usr/bin/env python

"""
Comprehensive WebSocket connection test script.
"""

import asyncio
import json
import websockets
import sys

async def receive_messages(websocket):
    """Receive and print messages from the WebSocket."""
    try:
        while True:
            response = await websocket.recv()
            parsed_response = json.loads(response)
            
            # Format the response nicely
            print(f"\n[{parsed_response['type']}] {parsed_response['value']}")
            
            # Check if this is a final result
            if parsed_response['type'] == 'Result':
                print("\n=== Final Result ===")
                print(json.dumps(parsed_response['value'], indent=2))
                print("===================")
                return
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error receiving messages: {str(e)}")

async def test_connection():
    """Test connection to the WebSocket server with full message handling."""
    try:
        uri = "ws://localhost:8000/api/flutter"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("Connection established!")
            
            # Send a test message
            message = {
                "type": "GenerateCode",
                "user_query": "Create a simple Flutter hello world app"
            }
            
            print(f"Sending message: {json.dumps(message, indent=2)}")
            await websocket.send(json.dumps(message))
            
            # Receive all messages
            print("\nReceiving messages:")
            await receive_messages(websocket)
            
            print("\nTest completed successfully!")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(test_connection())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(0) 