from fastapi import FastAPI, WebSocket
from api.presentation import WebSocketHandler

app = FastAPI()
websocket_handler = WebSocketHandler()

@app.websocket("/api/ttandroid")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for code generation.
    
    Expected message format:
    {
        "user_query": "string"  # The query for code generation
    }
    
    Response format:
    {
        "type": "Text" | "Error" | "Result",
        "value": "string" | object
    }
    """
    await websocket_handler.handle_websocket(websocket) 