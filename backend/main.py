#!/usr/bin/env python3
"""
Main entry point for the LikeMinds Integration Agent backend.
This initializes all services and starts the FastAPI application.
"""

import os
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

from infrastructure.config import settings
from infrastructure.auth import get_current_user
from infrastructure.observability import trace, monitor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LikeMinds Integration Agent",
    description="Backend for the LikeMinds Integration Agent",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
# These will be implemented as services are developed
from agents.documentation.router import router as documentation_router
from agents.coding.router import router as coding_router
# from project.demo.router import router as demo_router
# from project.environment.router import router as environment_router

# Root endpoint
@app.get("/")
@trace("root_endpoint")
async def root():
    """Root endpoint that returns service status."""
    return {
        "service": "LikeMinds Integration Agent",
        "status": "running",
        "version": "0.1.0",
    }

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes probes."""
    return {"status": "healthy"}

# Add routers
# These will be enabled as services are developed
app.include_router(documentation_router, prefix="/api/agents/documentation", tags=["Documentation Agent"])
app.include_router(coding_router, prefix="/api/agents/coding", tags=["Coding Agent"])
# app.include_router(demo_router, prefix="/api/project/demo", tags=["Demo Repository"])
# app.include_router(environment_router, prefix="/api/project/environment", tags=["Environment"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting LikeMinds Integration Agent on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 