from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from api.services.websocket import WebSocketManager
from api.services.flutter import FlutterProjectManager

router = APIRouter()
websocket_manager = WebSocketManager()

async def get_flutter_manager():
    return FlutterProjectManager()

@router.websocket("/ws/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: str,
    flutter_manager: FlutterProjectManager = Depends(get_flutter_manager)
):
    """WebSocket endpoint for real-time project updates"""
    try:
        await websocket_manager.connect(websocket, project_id)
        await websocket_manager.send_status(project_id, "connected")
        
        try:
            while True:
                # Wait for any client messages
                data = await websocket.receive_text()
                
                # Handle client requests
                if data == "compile":
                    await websocket_manager.send_status(project_id, "compiling")
                    
                    # Compile the project
                    success, error = await flutter_manager.compile_web(project_id)
                    if not success:
                        await websocket_manager.send_error(project_id, f"Compilation failed: {error}")
                        continue
                    
                    # Get preview URL
                    preview_path = await flutter_manager.get_web_preview_path(project_id)
                    if preview_path:
                        await websocket_manager.send_preview_update(project_id, f"/preview/{project_id}")
                        await websocket_manager.send_completion(project_id, True)
                    else:
                        await websocket_manager.send_error(project_id, "Failed to get preview path")
                
        except WebSocketDisconnect:
            await websocket_manager.disconnect(websocket, project_id)
            
    except Exception as e:
        await websocket_manager.send_error(project_id, str(e))
        await websocket_manager.disconnect(websocket, project_id) 