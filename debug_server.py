import logging
import sys
import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from api.routes import generate

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("websocket_debug")

app = FastAPI(
    title="LikeMinds Flutter Integration Assistant API [DEBUG MODE]",
    description="API for generating and previewing Flutter code with WebSocket debugging",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for regular endpoints
app.include_router(generate.router, prefix="/api/v1", tags=["generation"])

# Mount static files for web previews
app.mount("/preview", StaticFiles(directory="projects"), name="preview")

# Explicitly define WebSocket endpoint for debugging
@app.websocket("/ws/{project_id}")
async def websocket_debug_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket endpoint for debugging"""
    logger.debug(f"WebSocket connection attempt for project: {project_id}")
    
    try:
        await websocket.accept()
        logger.info(f"WebSocket connection accepted for project: {project_id}")
        
        # Send a welcome message
        await websocket.send_json({
            "type": "status",
            "data": {
                "status": "connected",
                "project_id": project_id,
                "message": "Debug WebSocket connected successfully"
            }
        })
        
        try:
            while True:
                # Wait for any client messages
                data = await websocket.receive_text()
                logger.debug(f"Received message from client: {data}")
                
                # Echo back the message for debugging
                await websocket.send_json({
                    "type": "echo",
                    "data": {
                        "received": data,
                        "project_id": project_id
                    }
                })
                
                # Handle compile command
                if data == "compile":
                    logger.info(f"Compile command received for project: {project_id}")
                    await websocket.send_json({
                        "type": "status",
                        "data": {
                            "status": "compiling",
                            "project_id": project_id
                        }
                    })
                    
                    # Simulate compilation process
                    import asyncio
                    await asyncio.sleep(1)
                    
                    # Send completion message
                    await websocket.send_json({
                        "type": "completion",
                        "data": {
                            "success": True,
                            "project_id": project_id,
                            "message": "Debug compilation completed"
                        }
                    })
                    
        except Exception as e:
            logger.error(f"Error in WebSocket communication: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "data": {
                    "error": str(e),
                    "project_id": project_id
                }
            })
            
    except Exception as e:
        logger.error(f"Failed to establish WebSocket connection: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LikeMinds Flutter Integration Assistant API [DEBUG MODE]",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

# Debug endpoint to test project existence
@app.get("/debug/project/{project_id}")
async def test_project(project_id: str):
    """Test if a project exists"""
    project_path = os.path.join("projects", project_id)
    exists = os.path.exists(project_path)
    return JSONResponse({
        "project_id": project_id,
        "exists": exists,
        "path": project_path if exists else None
    })

if __name__ == "__main__":
    # Create projects directory if it doesn't exist
    os.makedirs("projects", exist_ok=True)
    
    # Run server with debugging
    uvicorn.run("debug_server:app", host="0.0.0.0", port=8001, log_level="debug", reload=True) 