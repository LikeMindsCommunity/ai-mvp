#!/usr/bin/env python

"""
WebSocket connection test script.
"""

import asyncio
import json
import websockets

async def test_connection():
    """Test connection to the WebSocket server."""
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
            
            print(f"Sending message: {message}")
            await websocket.send(json.dumps(message))
            
            # Receive initial response
            response = await websocket.recv()
            print(f"Received response: {response}")
            
            # Close after a short time
            print("Test successful, closing connection after 2 seconds...")
            await asyncio.sleep(2)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection()) 