#!/usr/bin/env python

"""
WebSocket streaming test script to debug chunk delivery timing.
"""

import asyncio
import json
import time
import websockets
import sys

async def debug_websocket_streaming():
    """Connect to the websocket and print all messages with timing information."""
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
            start_time = time.time()
            await websocket.send(json.dumps(message))
            
            # Receive and print all messages with timestamps
            print("\nStreaming response messages with timestamps:")
            print("-" * 50)
            
            chunk_count = 0
            last_chunk_time = start_time
            
            try:
                while True:
                    response = await websocket.recv()
                    current_time = time.time()
                    data = json.loads(response)
                    chunk_count += 1
                    
                    # Calculate timing
                    time_since_start = current_time - start_time
                    time_since_last = current_time - last_chunk_time
                    last_chunk_time = current_time
                    
                    # Debug print the timing info
                    print(f"\nChunk #{chunk_count}")
                    print(f"Time since start: {time_since_start:.4f}s")
                    print(f"Time since last chunk: {time_since_last:.4f}s")
                    print(f"Message Type: {data.get('type', 'UNKNOWN')}")
                    print(f"Value Type: {type(data.get('value', None)).__name__}")
                    
                    # Print value snippet
                    value = data.get('value', '')
                    if isinstance(value, str) and len(value) > 100:
                        print(f"Value snippet: {value[:100]}...")
                    else:
                        print(f"Value: {value}")
                    
                    print("-" * 50)
                    
            except websockets.exceptions.ConnectionClosed:
                print("\nConnection closed by server")
                print(f"Total chunks received: {chunk_count}")
                print(f"Total time: {time.time() - start_time:.4f}s")
                
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(debug_websocket_streaming()) 