"""
Main FastAPI application for Flutter Integration Assistant.
"""

import os
import json
import yaml
from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.presentation.websocket_handler import WebSocketHandler

# Create FastAPI app with custom OpenAPI URL
app = FastAPI(
    title="Flutter Integration Assistant API",
    description="API for generating Flutter code integrations with LikeMinds SDK",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
    openapi_url=None  # Disable default OpenAPI schema
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "websocket_endpoint": "/api/flutter",
        "documentation": "/docs",
        "websocket_tester": "/websocket-tester"
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

def start(reload=True):
    """Start the FastAPI application with Uvicorn."""
    # Check if SSL is enabled
    enable_ssl = os.environ.get("ENABLE_SSL", "false").lower() == "true"
    ssl_cert = os.environ.get("SSL_CERT_FILE", "/app/ssl/cert.pem")
    ssl_key = os.environ.get("SSL_KEY_FILE", "/app/ssl/key.pem")
    ssl_port = int(os.environ.get("SSL_PORT", 8443))
    
    if enable_ssl and os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        print(f"Starting server with SSL support on port {ssl_port}")
        uvicorn.run(
            "api.main:app", 
            host="0.0.0.0", 
            port=ssl_port,
            reload=reload,
            reload_dirs=["api"],
            reload_excludes=["integration"],
            ssl_keyfile=ssl_key,
            ssl_certfile=ssl_cert
        )
    else:
        # Standard non-SSL startup
        port = int(os.environ.get("API_PORT", 8000))
        print(f"Starting server without SSL on port {port}")
        uvicorn.run(
            "api.main:app", 
            host="0.0.0.0", 
            port=port, 
            reload=reload,
            reload_dirs=["api"],
            reload_excludes=["integration"]
        )

if __name__ == "__main__":
    start() 