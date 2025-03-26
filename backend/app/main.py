from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import logging
import uvicorn
import json
import time

from app.core.orchestrator import AgentOrchestrator
from app.core.config.env import HOST, PORT

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="LikeMinds RAG API")

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],  # Added Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class QueryRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    stream: Optional[bool] = False


# Initialize orchestrator
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing LikeMinds RAG API")
    app.state.orchestrator = AgentOrchestrator()


# Health check endpoint
@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "LikeMinds RAG API"}


# Query endpoint
@app.post("/api/query", tags=["Query"])
async def process_query(request: QueryRequest):
    """
    Process a user query through the RAG pipeline and return a response with sources.
    """
    # If streaming is requested, use streaming response
    if request.stream:
        return await stream_query(request)
        
    try:
        # Get orchestrator from app state
        orchestrator = app.state.orchestrator
        
        # Process the query
        result = await orchestrator.process_query(
            query=request.query,
            conversation_history=request.conversation_history
        )
        
        return result
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# Streaming query endpoint
@app.get("/api/query", tags=["Query"])
async def stream_query_get(request: Request):
    """
    Stream the query processing using Server-Sent Events (SSE) with GET parameters.
    """
    # Extract query parameters
    query = request.query_params.get("query")
    stream = request.query_params.get("stream", "false").lower() == "true"
    
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    if not stream:
        raise HTTPException(status_code=400, detail="Stream parameter must be 'true' for streaming responses")
    
    # Create a request object compatible with the stream_query function
    query_request = QueryRequest(
        query=query,
        conversation_history=[],
        stream=True
    )
    
    return await stream_query(query_request)


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
            # Get orchestrator from app state
            orchestrator = app.state.orchestrator
            
            # Step 1: Query Understanding
            yield f"data: {json.dumps({'event': 'status', 'data': {'status': 'understanding_query', 'message': 'Analyzing your query...'}})} \n\n"
            
            step_start = time.time()
            query_analysis = await orchestrator.query_agent.enhance_query(request.query)
            enhanced_query = query_analysis
            
            metrics["steps"]["query_understanding"] = {
                "duration": time.time() - step_start,
                "output": {"enhanced_query": enhanced_query}
            }
            
            yield f"data: {json.dumps({'event': 'query_analysis', 'data': {'enhanced_query': enhanced_query}})} \n\n"
            
            # Step 2: Context Retrieval
            yield f"data: {json.dumps({'event': 'status', 'data': {'status': 'retrieving_context', 'message': 'Retrieving relevant documentation...'}})} \n\n"
            
            step_start = time.time()
            query_embedding = await orchestrator.embedding_generator.generate_query_embedding(request.query)
            
            # Build filters from query analysis
            filters = {}
            
            # Retrieve initial context
            initial_chunks = await orchestrator.vector_store.search(
                query=request.query,
                query_embedding=query_embedding,
                n_results=10,  # Default initial results
                filter_dict=filters
            )
            
            yield f"data: {json.dumps({'event': 'initial_chunks', 'data': {'count': len(initial_chunks), 'chunks': initial_chunks}})} \n\n"
            
            # Step 3: Reranking (if needed)
            ranked_chunks = await orchestrator.retrieval_agent.rerank_documents(
                enhanced_query,
                initial_chunks
            )
            
            metrics["steps"]["context_retrieval"] = {
                "duration": time.time() - step_start,
                "context_count": len(ranked_chunks)
            }
            
            yield f"data: {json.dumps({'event': 'ranked_chunks', 'data': {'count': len(ranked_chunks), 'chunks': ranked_chunks[:5]}})} \n\n"
            
            # Step 4: Response Generation
            yield f"data: {json.dumps({'event': 'status', 'data': {'status': 'generating_response', 'message': 'Generating response based on retrieved context...'}})} \n\n"
            
            step_start = time.time()
            
            # Get sources first from basic context analysis
            sources = [doc.get("metadata", {}).get("source", "Unknown source") for doc in ranked_chunks[:5]]
            sources = list(set(sources))  # Remove duplicates
            
            # Stream the response token by token
            current_token = ""
            try:
                async for token in orchestrator.response_agent.generate_response_stream(
                    request.query,
                    enhanced_query,
                    ranked_chunks[:5],  # Default final results
                    request.conversation_history or []
                ):
                    # Send each token as it's generated
                    yield f"data: {json.dumps({'event': 'token', 'data': {'token': token}})} \n\n"
                    current_token += token
                
                # No need to call generate_response again, just use the sources we already have
                metrics["steps"]["response_generation"] = {
                    "duration": time.time() - step_start
                }
                
                # Calculate total processing time
                metrics["total_time"] = time.time() - start_time
                
                # Return final response metadata (sources, metrics)
                yield f"data: {json.dumps({'event': 'response_complete', 'data': {'sources': sources, 'metrics': metrics}})} \n\n"
            except Exception as e:
                logger.error(f"Error streaming response: {str(e)}", exc_info=True)
                yield f"data: {json.dumps({'event': 'error', 'data': {'error': f'Error generating streaming response: {str(e)}'}})} \n\n"
            
            # End of stream
            yield f"data: {json.dumps({'event': 'done', 'data': {'status': 'completed', 'message': 'Query processing completed'}})} \n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming query: {str(e)}", exc_info=True)
            # Send error message
            yield f"data: {json.dumps({'event': 'error', 'data': {'error': str(e)}})} \n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


# Start the server if running as a script
if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True) 