"""
Main FastAPI application for Flutter Integration Assistant.
"""

import os
import json
import yaml
from fastapi import FastAPI, WebSocket, HTTPException, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.presentation.websocket_handler import WebSocketHandler
from api.presentation.auth import router as auth_router
from api.presentation.users import router as users_router
from api.presentation.projects import router as projects_router
from api.presentation.github import router as github_router
from api.infrastructure.auth import get_current_user
from api.config import get_settings

settings = get_settings()

# Create FastAPI app with custom OpenAPI URL
app = FastAPI(
    title="Flutter Integration Assistant API",
    description="API for generating Flutter code integrations with LikeMinds SDK",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
    openapi_url=None  # Disable default OpenAPI schema
)

# Add proper CORS middleware with correct settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-mvp-frontend.pages.dev"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=1728000,
)

# Add a catch-all exception handler to ensure CORS headers are present even on errors
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """Ensure all error responses include CORS headers"""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "https://ai-mvp-frontend.pages.dev",
            "Access-Control-Allow-Credentials": "true",
        },
    )

# Add a dedicated OPTIONS route handler for all paths
@app.options("/{path:path}")
async def options_handler(request: Request, path: str):
    """Handle all OPTIONS requests explicitly"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "https://ai-mvp-frontend.pages.dev",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "1728000",
        }
    )


# Add middleware to handle trailing slashes for API endpoints
@app.middleware("http")
async def add_trailing_slash_middleware(request: Request, call_next):
    """Ensure consistent trailing slash behavior for API endpoints"""
    path = request.url.path
    
    # Only process API paths that don't end with a slash
    if path.startswith("/api/") and not path.endswith("/") and "." not in path.split("/")[-1]:
        # Skip for OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)
            
        # Create new URL with trailing slash
        new_url = str(request.url.replace(path=f"{path}/"))
        response = RedirectResponse(new_url, status_code=307)
        
        # Add CORS headers to the redirect
        response.headers["Access-Control-Allow-Origin"] = "https://ai-mvp-frontend.pages.dev"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response
        
    return await call_next(request)

# Try to mount static files directory for SwaggerUI
try:
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")
    
    # Create the static directory if it doesn't exist
    os.makedirs(static_dir, exist_ok=True)
    
    # Mount the static directory
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(github_router) 

# Initialize WebSocket handler
websocket_handler = WebSocketHandler()

@app.websocket("/api/flutter")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT access token"),
    project_id: str = Query(..., description="Project ID to associate with this session")
):
    """
    WebSocket endpoint for Flutter code generation, with authentication and project context.
    
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
    # Authentication verification happens in the handler
    await websocket_handler.handle_websocket(websocket, token, project_id)

@app.get("/status")
async def root():
    """Status endpoint for API health check."""
    return {
        "status": "online",
        "message": "Flutter Integration Assistant API is running",
        "websocket_endpoint": "/api/flutter",
        "authentication": "/api/auth/login",
        "documentation": "/docs",
        "websocket_tester": "/websocket-tester",
        "api_tester": "/api-tester",
        "integration_tester": "/integration-tester"
    }

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_spec():
    """Return the OpenAPI specification as JSON."""
    # Path to the custom OpenAPI specification
    openapi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "openapi", "openapi.yaml")
    
    try:
        with open(openapi_path, "r") as f:
            yaml_content = yaml.safe_load(f)
            return yaml_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading OpenAPI spec: {str(e)}")

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def get_swagger_ui_html(request: Request):
    """Serve custom Swagger UI."""
    swagger_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flutter Integration Assistant API - Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
        <style>
            body {
                margin: 0;
                padding: 0;
            }
            .swagger-ui .topbar {
                background-color: #1565c0;
            }
            .swagger-ui .info {
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js" charset="UTF-8"></script>
        <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout",
                    withCredentials: true,
                    tagsSorter: "alpha"
                });
                window.ui = ui;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=swagger_html)

@app.get("/websocket-tester", response_class=HTMLResponse, include_in_schema=False)
async def get_websocket_tester():
    """Serve WebSocket tester HTML page."""
    # Path to the WebSocket tester HTML file
    tester_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              "static", "websocket_tester.html")
    
    try:
        with open(tester_path, "r") as f:
            html_content = f.read()
            return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading WebSocket tester: {str(e)}")

@app.get("/integration-tester", response_class=HTMLResponse, include_in_schema=False)
async def get_integration_tester():
    """Serve Integration tester HTML page."""
    # Path to the Integration tester HTML file
    tester_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              "static", "integration_tester.html")
    
    try:
        with open(tester_path, "r") as f:
            html_content = f.read()
            return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading Integration tester: {str(e)}")

# Add specific GET route for /api/projects without trailing slash to avoid 405 errors
@app.get("/api/projects")
async def get_projects_redirect():
    """Redirect GET requests from /api/projects to /api/projects/ to avoid 405 errors"""
    return RedirectResponse(url="/api/projects/", status_code=307)

@app.post("/api/projects")
async def post_projects_redirect(request: Request):
    """Redirect POST requests from /api/projects to /api/projects/ to avoid 405 errors"""
    return RedirectResponse(url="/api/projects/", status_code=307)

@app.put("/api/projects/{project_id}")
async def put_project_redirect(project_id: str):
    """Redirect PUT requests for project updates to avoid 405 errors"""
    return RedirectResponse(url=f"/api/projects/{project_id}/", status_code=307)

@app.delete("/api/projects/{project_id}")
async def delete_project_redirect(project_id: str):
    """Redirect DELETE requests for project deletion to avoid 405 errors"""
    return RedirectResponse(url=f"/api/projects/{project_id}/", status_code=307)

def start(reload=True):
    """Start the FastAPI application with Uvicorn."""
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=reload,
        reload_dirs=["api"],  # Only watch the api directory
        reload_excludes=["integration"]  # Explicitly exclude integration directory
    )

if __name__ == "__main__":
    start() 