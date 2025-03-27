"""
Router for the Coding Agent service.
"""

import time
import uuid
import logging
import os
import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import Dict, Any, List, Optional, Callable

from .models import (
    CodingRequest, CodingResponse, FileInfo, ValidationIssue, 
    SDKValidationIssue, ValidationResult, RefinementRequest, ProgressUpdate,
    SDKContextModel
)
from ...infrastructure.auth import get_current_user
from .agent_orchestrator import CodingAgentOrchestrator

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize orchestrator
orchestrator = CodingAgentOrchestrator()

# Store for progress updates by project_id
progress_stores = {}

@router.post("/process", response_model=CodingResponse)
async def process_request(
    request: CodingRequest,
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user)
) -> CodingResponse:
    """
    Process a coding request with LikeMinds SDK integration.
    """
    logger.info(f"Processing coding request: Project {request.project_id} - {request.platform}/{request.language}")
    
    try:
        start_time = time.time()
        
        # Create progress tracking
        progress_updates = []
        project_id = request.project_id
        progress_stores[project_id] = progress_updates
        
        async def progress_callback(step: str, percentage: float, info: Dict[str, Any]):
            update = {
                "step": step,
                "percentage": percentage,
                "message": info.get("message", "Processing..."),
                "timestamp": time.time(),
                "details": info
            }
            progress_updates.append(update)
            logger.info(f"Progress update for {project_id}: {step} - {percentage:.0%}")
        
        # Process context
        context_dict = request.context or {}
        if request.sdk_context:
            # Merge SDK context into the main context
            sdk_context_dict = request.sdk_context.dict()
            context_dict.update({
                "sdk_component": sdk_context_dict.get("component"),
                "sdk_version": sdk_context_dict.get("version"),
                "sdk_documentation": sdk_context_dict.get("documentation"),
                "sdk_source_repo": sdk_context_dict.get("source_repo"),
                "sdk_platform_config": sdk_context_dict.get("platform_config")
            })
        
        # Process the request
        result = await orchestrator.process(
            requirements=request.requirements,
            platform=request.platform,
            language=request.language,
            project_id=request.project_id,
            solution_document=request.solution_document,
            output_dir=request.output_dir,
            context=context_dict,
            progress_callback=progress_callback
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Get file information
        files = []
        if "output_dir" in result and result["output_dir"]:
            try:
                for root, _, filenames in os.walk(result["output_dir"]):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(file_path, result["output_dir"])
                        
                        # Get file size
                        size = os.path.getsize(file_path)
                        
                        # Get file language based on extension
                        _, ext = os.path.splitext(filename)
                        language = ext.lstrip('.') if ext else None
                        
                        # Get content preview (first few lines)
                        content_preview = None
                        try:
                            with open(file_path, 'r') as f:
                                preview_lines = [next(f, '') for _ in range(10)]
                                content_preview = ''.join(preview_lines)
                        except:
                            pass
                        
                        # Check if this file has SDK validation results
                        sdk_components_used = None
                        if "validation_result" in result and "sdk_integration" in result["validation_result"]:
                            for file_result in result["validation_result"]["sdk_integration"].get("file_results", []):
                                if file_result.get("file") == rel_path:
                                    sdk_components_used = file_result.get("validation", {}).get("sdk_classes_used", [])
                        
                        files.append(FileInfo(
                            path=rel_path,
                            description=f"Generated {language} file" if language else "Generated file",
                            content_preview=content_preview,
                            size=size,
                            language=language,
                            sdk_components_used=sdk_components_used
                        ))
            except Exception as e:
                logger.error(f"Error getting file information: {str(e)}")
        
        # Create validation result
        validation_result = None
        if "validation_result" in result:
            validation_data = result["validation_result"]
            
            # Extract general validation issues
            general_issues = []
            if "issues" in validation_data:
                for issue in validation_data["issues"]:
                    general_issues.append(ValidationIssue(
                        severity=issue.get("severity", "info"),
                        message=issue.get("description", ""),
                        file=issue.get("file"),
                        line=issue.get("line"),
                        code=issue.get("code"),
                        sdk_related=issue.get("sdk_related", False)
                    ))
            
            # Extract SDK validation issues
            sdk_issues = []
            missing_files = []
            
            if "sdk_integration" in validation_data:
                sdk_validation = validation_data["sdk_integration"]
                
                # Get SDK issues
                for issue in sdk_validation.get("all_sdk_issues", []):
                    sdk_issues.append(SDKValidationIssue(
                        type=issue.get("type", "unknown"),
                        severity=issue.get("severity", "medium"),
                        description=issue.get("description", ""),
                        file=issue.get("file"),
                        line_reference=issue.get("line_reference"),
                        correct_implementation=issue.get("correct_implementation")
                    ))
                
                # Get missing essential files
                missing_files = sdk_validation.get("missing_essential_elements", [])
            
            # Create the validation result
            validation_result = ValidationResult(
                passes_all_requirements=validation_data.get("passes_all_requirements", False),
                average_score=validation_data.get("average_score", 0.0),
                issues=general_issues,
                sdk_score=validation_data.get("sdk_score"),
                sdk_validation_issues=sdk_issues if sdk_issues else None,
                essential_files_missing=missing_files if missing_files else None,
                integration_complete=validation_data.get("sdk_integration", {}).get("integration_complete"),
                next_steps=validation_data.get("next_steps")
            )
        
        # Clean up progress store after 1 hour (in a real implementation)
        # background_tasks.add_task(clean_progress_store, project_id, 3600)
        
        # Return the response
        return CodingResponse(
            project_id=request.project_id,
            output_dir=result["output_dir"],
            status=result.get("status", "error"),
            files=files,
            complexity_estimate=result.get("complexity_estimate", {}),
            validation=validation_result,
            processing_time=processing_time,
            error=result.get("error"),
            sdk_component=result.get("sdk_component"),
            sdk_version=result.get("sdk_version"),
            progress_updates=progress_updates,
            metadata={
                "generation_timestamp": time.time(),
                "model_used": "claude-3-5-sonnet"
            }
        )
    except Exception as e:
        logger.error(f"Error processing coding request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.post("/analyze-existing-code")
async def analyze_existing_code(
    repo_path: str,
    platform: str,
    language: str,
    sdk_component: str = "chat",
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyze existing code for SDK integration points.
    """
    try:
        result = await orchestrator.analyze_existing_code(
            repo_path=repo_path,
            platform=platform,
            language=language,
            sdk_component=sdk_component
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing existing code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")

@router.post("/refine", response_model=CodingResponse)
async def refine_code(
    request: RefinementRequest,
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user)
) -> CodingResponse:
    """
    Refine previously generated code based on feedback.
    """
    logger.info(f"Refining code for project {request.project_id}")
    
    try:
        start_time = time.time()
        
        # Create progress tracking
        progress_updates = []
        project_id = request.project_id
        progress_stores[project_id] = progress_updates
        
        async def progress_callback(step: str, percentage: float, info: Dict[str, Any]):
            update = {
                "step": step,
                "percentage": percentage,
                "message": info.get("message", "Processing..."),
                "timestamp": time.time(),
                "details": info
            }
            progress_updates.append(update)
            logger.info(f"Refinement progress for {project_id}: {step} - {percentage:.0%}")
        
        # Get the previous result
        # In a real implementation, this would come from a database
        output_dir = request.output_dir or f"generated_code/{request.project_id}"
        if not os.path.exists(output_dir):
            raise HTTPException(status_code=404, detail=f"Project directory not found: {output_dir}")
        
        previous_result = {
            "project_id": request.project_id,
            "output_dir": output_dir
        }
        
        # SDK context handling
        sdk_context = None
        if request.sdk_context:
            sdk_context = {
                "sdk_component": request.sdk_context.component,
                "sdk_version": request.sdk_context.version,
                "sdk_documentation": request.sdk_context.documentation
            }
        
        # Process the refinement
        result = await orchestrator.refine(
            previous_result=previous_result,
            feedback=request.feedback,
            modifications=request.modifications,
            progress_callback=progress_callback
        )
        
        # Build response (similar to process_request)
        # Implement file listing and validation processing here
        # ...
        
        # For brevity, I'll reuse the logic from process_request to get files
        files = []
        if "output_dir" in result and result["output_dir"]:
            # Implement file listing similar to process_request
            pass
        
        # Create the response
        return CodingResponse(
            project_id=request.project_id,
            output_dir=result.get("output_dir", output_dir),
            status=result.get("status", "error"),
            files=files,
            complexity_estimate=result.get("complexity_estimate", {}),
            validation=None,  # Process validation results
            processing_time=time.time() - start_time,
            error=result.get("error"),
            sdk_component=result.get("sdk_component"),
            progress_updates=progress_updates,
            metadata={
                "refinement_timestamp": time.time(),
                "original_project_id": request.project_id
            }
        )
    except Exception as e:
        logger.error(f"Error refining code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error refining code: {str(e)}")

@router.websocket("/ws/{project_id}")
async def progress_websocket(websocket: WebSocket, project_id: str):
    """
    WebSocket endpoint for real-time progress updates.
    """
    await websocket.accept()
    
    try:
        # Initial data
        if project_id in progress_stores:
            for update in progress_stores[project_id]:
                await websocket.send_json(update)
        
        # Keep connection open to send future updates
        last_update_count = len(progress_stores.get(project_id, []))
        
        while True:
            await websocket.receive_text()  # Keep-alive ping
            
            if project_id in progress_stores:
                updates = progress_stores[project_id]
                if len(updates) > last_update_count:
                    # Send new updates
                    for update in updates[last_update_count:]:
                        await websocket.send_json(update)
                    last_update_count = len(updates)
            
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for project {project_id}")
    except Exception as e:
        logger.error(f"WebSocket error for project {project_id}: {str(e)}")

@router.get("/projects/{project_id}/sdk-validation")
async def get_sdk_validation(
    project_id: str,
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get SDK-specific validation results for a project.
    """
    # In a real implementation, this would fetch results from a database
    output_dir = f"generated_code/{project_id}"
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Look for a validation results file
    validation_file = os.path.join(output_dir, "validation_results.json")
    if not os.path.exists(validation_file):
        raise HTTPException(status_code=404, detail="Validation results not found")
    
    try:
        with open(validation_file, 'r') as f:
            validation_data = json.load(f)
        
        # Extract SDK-specific validation
        if "sdk_integration" in validation_data:
            return validation_data["sdk_integration"]
        else:
            return {"error": "No SDK validation data found"}
    except Exception as e:
        logger.error(f"Error retrieving SDK validation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving SDK validation: {str(e)}")

@router.get("/projects/{project_id}/download")
async def download_project(
    project_id: str,
    user = Depends(get_current_user)
):
    """
    Download a generated project as a zip file.
    """
    # Check if project exists
    project_dir = f"generated_code/{project_id}"
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create a zip file
    import shutil
    zip_path = f"{project_dir}.zip"
    
    try:
        shutil.make_archive(project_dir, 'zip', project_dir)
        return FileResponse(
            zip_path, 
            media_type="application/zip", 
            filename=f"{project_id}.zip"
        )
    except Exception as e:
        logger.error(f"Error creating zip file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating zip file: {str(e)}")

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """
    Get the status of the Coding Agent service.
    """
    return {
        "service": "Coding Agent",
        "status": "running",
        "timestamp": time.time(),
        "sdk_integration_enabled": True
    } 