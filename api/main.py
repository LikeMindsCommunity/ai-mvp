"""
Main FastAPI application for Flutter Integration Assistant.
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.presentation.websocket_handler import WebSocketHandler

app = FastAPI(
    title="Flutter Integration Assistant API",
    description="API for generating Flutter code integrations with LikeMinds SDK",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket handler
websocket_handler = WebSocketHandler()

@app.websocket("/api/flutter")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for Flutter code generation.
    
    Expected message format:
    {
        "type": "GenerateCode",
        "user_query": "string"  # The query for code generation
    }
    
    OR
    
    {
        "type": "FixCode",
        "user_query": "string",  # The original query
        "error_message": "string"  # Error message from Flutter analysis
    }
    
    Response format:
    {
        "type": "Text" | "Error" | "Success" | "AnalysisError" | "Result",
        "value": "string" | object
    }
    """
    await websocket_handler.handle_websocket(websocket)

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {
        "status": "online",
        "message": "Flutter Integration Assistant API is running",
        "websocket_endpoint": "/api/flutter"
    }

def start():
    """Start the FastAPI application with Uvicorn."""
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start() 