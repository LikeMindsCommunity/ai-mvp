#!/usr/bin/env python

"""
WebSocket debugging script for stream type issues.
"""

import asyncio
import json
import websockets
import sys

async def debug_websocket():
    """Connect to the websocket and print all messages with their types."""
    try:
        uri = "ws://localhost:8000/api/flutter"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("Connection established!")
            
            # Send a test message
            message = {
                "type": "GenerateCode",
                "user_query": "How to integrate LikeMinds Chat SDK in Flutter?"
            }
            
            print(f"Sending message: {json.dumps(message, indent=2)}")
            await websocket.send(json.dumps(message))
            
            # Receive and print all messages
            print("\nStreaming response messages (Ctrl+C to stop):")
            print("-" * 50)
            
            try:
                while True:
                    response = await websocket.recv()
                    data = json.loads(response)
                    
                    # Debug print the full message
                    print(f"\nMessage Type: {data.get('type', 'UNKNOWN')}")
                    print(f"Value Type: {type(data.get('value', None)).__name__}")
                    print(f"Value: {data.get('value', None)}")
                    print("-" * 50)
                    
            except websockets.exceptions.ConnectionClosed:
                print("\nConnection closed by server")
                
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(debug_websocket())
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(0) 