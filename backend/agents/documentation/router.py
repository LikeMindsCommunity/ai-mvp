"""
Router for the Documentation Agent service.
"""

import time
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from .models import DocumentationRequest, DocumentationResponse, DocumentContext
from ...infrastructure.auth import get_current_user
from .orchestrator.service import process_documentation

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/process", response_model=DocumentationResponse)
async def process_request(
    request: DocumentationRequest,
    user = Depends(get_current_user)
) -> DocumentationResponse:
    """
    Process a documentation request.
    """
    logger.info(f"Processing documentation request: {request.query}")
    
    try:
        start_time = time.time()
        
        # Process the request
        result = await process_documentation(request, user)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Return the response
        return DocumentationResponse(
            solution_document=result["solution_document"],
            relevant_context=result["relevant_context"],
            next_steps=result.get("next_steps"),
            request_id=str(uuid.uuid4()),
            processing_time=processing_time,
            metadata=result.get("metadata")
        )
    except Exception as e:
        logger.error(f"Error processing documentation request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """
    Get the status of the Documentation Agent service.
    """
    return {
        "service": "Documentation Agent",
        "status": "running",
        "timestamp": time.time()
    } 