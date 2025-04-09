import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import generate, preview

app = FastAPI(
    title="LikeMinds Flutter Integration Assistant API",
    description="API for generating and previewing Flutter code",
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

# Include routers
app.include_router(generate.router, prefix="/api/v1", tags=["generation"])
app.include_router(preview.router, tags=["preview"])

# Mount static files for web previews
app.mount("/preview", StaticFiles(directory="projects"), name="preview")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Create projects directory if it doesn't exist
    os.makedirs("projects", exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LikeMinds Flutter Integration Assistant API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    } 