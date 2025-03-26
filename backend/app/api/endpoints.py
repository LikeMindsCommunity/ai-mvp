from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import json
import asyncio
import time

from ..core.agents.agent_orchestrator import AgentOrchestrator
from ..core.document_processor.document_processor import DocumentProcessor

# Initialize router
router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator(vector_store_path="./chroma_db")

# Initialize document processor
doc_processor = DocumentProcessor(
    chunk_size=800,
    chunk_overlap=100,
    embedding_model="text-embedding-3-large",
    persist_directory="./chroma_db"
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    initial_results: Optional[int] = 10
    final_results: Optional[int] = 5
    stream: Optional[bool] = False

class ProcessDirectoryRequest(BaseModel):
    directory: str
    file_pattern: Optional[str] = "**/*.md"

class ProcessingResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Query endpoint
@router.post("/query")
async def query(request: QueryRequest):
    """
    Process a query using the RAG system.
    """
    # If streaming is requested, use the streaming endpoint
    if request.stream:
        return await stream_query(request)
    
    try:
        response = await orchestrator.process_query(
            query=request.query,
            initial_results=request.initial_results,
            final_results=request.final_results
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_query(request: QueryRequest):
    """
    Stream the query processing using Server-Sent Events (SSE).
    """
    async def event_generator():
        start_time = time.time()
        metrics = {
            "start_time": start_time,
            "steps": {}
        }
        
        try:
            # Step 1: Query Understanding
            yield json.dumps({
                "event": "status",
                "data": {
                    "status": "understanding_query",
                    "message": "Analyzing your query..."
                }
            }) + "\n\n"
            
            step_start = time.time()
            query_analysis = await orchestrator.query_agent.analyze_query(request.query)
            metrics["steps"]["query_understanding"] = {
                "duration": time.time() - step_start,
                "output": query_analysis
            }
            
            yield json.dumps({
                "event": "query_analysis",
                "data": query_analysis
            }) + "\n\n"
            
            # Step 2: Context Retrieval
            yield json.dumps({
                "event": "status",
                "data": {
                    "status": "retrieving_context",
                    "message": "Retrieving relevant documentation..."
                }
            }) + "\n\n"
            
            step_start = time.time()
            query_embedding = await orchestrator.embedding_generator.generate_query_embedding(request.query)
            
            # Build filters from query analysis
            filters = {}
            if query_analysis.get("platform") and query_analysis["platform"] not in ["unknown", "any", None]:
                filters["platform"] = query_analysis["platform"]
                
            if query_analysis.get("feature") and query_analysis["feature"] not in ["unknown", None]:
                filters["product_area"] = query_analysis["feature"]
            
            # Retrieve initial context
            initial_chunks = await orchestrator.vector_store.search(
                query=request.query,
                query_embedding=query_embedding,
                n_results=request.initial_results,
                filter_dict=filters
            )
            
            yield json.dumps({
                "event": "initial_chunks",
                "data": {
                    "count": len(initial_chunks),
                    "chunks": initial_chunks
                }
            }) + "\n\n"
            
            # Step 3: Reranking (if needed)
            ranked_chunks = await orchestrator.retrieval_agent.rerank_context(
                query=request.query,
                enhanced_query=query_analysis.get("enhanced_query", request.query),
                context=initial_chunks
            )
            
            metrics["steps"]["context_retrieval"] = {
                "duration": time.time() - step_start,
                "context_count": len(ranked_chunks)
            }
            
            yield json.dumps({
                "event": "ranked_chunks",
                "data": {
                    "count": len(ranked_chunks),
                    "chunks": ranked_chunks[:request.final_results]
                }
            }) + "\n\n"
            
            # Step 4: Response Generation
            yield json.dumps({
                "event": "status",
                "data": {
                    "status": "generating_response",
                    "message": "Generating response based on retrieved context..."
                }
            }) + "\n\n"
            
            step_start = time.time()
            response, sources = await orchestrator.response_agent.generate_response(
                request.query,
                query_analysis.get("enhanced_query", request.query),
                ranked_chunks[:request.final_results],
                []  # Empty conversation history
            )
            
            metrics["steps"]["response_generation"] = {
                "duration": time.time() - step_start
            }
            
            # Calculate total processing time
            metrics["total_time"] = time.time() - start_time
            
            # Return final response
            yield json.dumps({
                "event": "response",
                "data": {
                    "query": request.query,
                    "enhanced_query": query_analysis.get("enhanced_query", request.query),
                    "response": response,
                    "sources": sources,
                    "metrics": metrics
                }
            }) + "\n\n"
            
            # End of stream
            yield json.dumps({
                "event": "done",
                "data": {
                    "status": "completed",
                    "message": "Query processing completed"
                }
            }) + "\n\n"
            
        except Exception as e:
            # Send error message
            yield json.dumps({
                "event": "error",
                "data": {
                    "error": str(e)
                }
            }) + "\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# Background processing tasks store
processing_tasks = {}

# Helper for background processing
async def process_directory_background(task_id: str, directory: str, file_pattern: str):
    try:
        results = await doc_processor.process_directory(
            directory=directory,
            file_pattern=file_pattern
        )
        
        # Save stats to a file
        doc_processor.save_stats(f"processing_stats_{task_id}.json")
        
        # Update task status
        processing_tasks[task_id] = {
            "status": "completed",
            "results": results
        }
    except Exception as e:
        # Update task status with error
        processing_tasks[task_id] = {
            "status": "failed",
            "error": str(e)
        }

# Process directory endpoint
@router.post("/process")
async def process_directory(request: ProcessDirectoryRequest, background_tasks: BackgroundTasks):
    """
    Start processing a directory of documents.
    """
    # Generate a task ID
    import uuid
    task_id = str(uuid.uuid4())
    
    # Store initial task status
    processing_tasks[task_id] = {
        "status": "processing",
        "directory": request.directory,
        "file_pattern": request.file_pattern
    }
    
    # Add task to background
    background_tasks.add_task(
        process_directory_background,
        task_id=task_id,
        directory=request.directory,
        file_pattern=request.file_pattern
    )
    
    return ProcessingResponse(
        task_id=task_id,
        status="processing",
        message="Document processing started in the background"
    )

# Get task status endpoint
@router.get("/process/{task_id}")
async def get_task_status(task_id: str):
    """
    Get the status of a processing task.
    """
    if task_id not in processing_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return processing_tasks[task_id]

# Get metrics endpoint
@router.get("/metrics")
async def get_metrics():
    """
    Get system metrics.
    """
    return {
        "agent_metrics": orchestrator.get_metrics(),
        "vector_store": doc_processor.vector_store.get_collection_stats()
    }

# Add a new endpoint for streaming query that accepts GET parameters
@router.get("/query")
async def stream_query_get(request: Request):
    """
    Stream the query processing using Server-Sent Events (SSE) with GET parameters.
    """
    # Extract query parameters
    query = request.query_params.get("query")
    initial_results = int(request.query_params.get("initial_results", "10"))
    final_results = int(request.query_params.get("final_results", "5"))
    
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Create a request object compatible with the stream_query function
    query_request = QueryRequest(
        query=query,
        initial_results=initial_results,
        final_results=final_results,
        stream=True
    )
    
    return await stream_query(query_request) 