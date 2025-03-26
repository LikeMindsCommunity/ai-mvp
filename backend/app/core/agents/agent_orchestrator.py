import os
from typing import Dict, Any, List, Optional
import time
import json
from ..config.env import API_KEYS, CHROMA_DB_PATH

from .query_understanding_agent import QueryUnderstandingAgent
from .context_retrieval_agent import ContextRetrievalAgent
from .response_generation_agent import ResponseGenerationAgent
from ..vector_store.chroma_store import ChromaStore
from ..document_processor.embedding_generator import EmbeddingGenerator

class AgentOrchestrator:
    """
    Coordinates the interaction between various agents in the RAG system.
    Manages the flow of information from query to response through multiple specialized agents.
    """
    
    def __init__(self):
        """
        Initialize the agent orchestrator with all required agents and components.
        """
        # Initialize agents
        self.query_agent = QueryUnderstandingAgent()
        self.retrieval_agent = ContextRetrievalAgent()
        self.response_agent = ResponseGenerationAgent()
        
        # Initialize vector store
        self.vector_store = ChromaStore()
        self.embedding_generator = EmbeddingGenerator()
        
        # Initialize metrics collection
        self.metrics = {
            "queries_processed": 0,
            "avg_response_time": 0,
            "total_chunks_retrieved": 0
        }
    
    async def process_query(self, 
                          query: str,
                          initial_results: int = 10,
                          final_results: int = 5) -> Dict[str, Any]:
        """
        Process a user query through the entire agent pipeline.
        
        Args:
            query: The user query
            initial_results: Number of initial results to retrieve
            final_results: Number of final results to use for response
            
        Returns:
            Dictionary containing the response and process metadata
        """
        start_time = time.time()
        metrics = {
            "start_time": start_time,
            "steps": {}
        }
        
        try:
            # Step 1: Query Understanding
            step_start = time.time()
            query_analysis = await self.query_agent.analyze_query(query)
            metrics["steps"]["query_understanding"] = {
                "duration": time.time() - step_start,
                "output": query_analysis
            }
            
            # Step 2: Context Retrieval
            step_start = time.time()
            
            # Generate query embedding
            query_embedding = await self.embedding_generator.generate_query_embedding(query)
            
            # Build filters from query analysis
            filters = {}
            if query_analysis.get("platform") and query_analysis["platform"] not in ["unknown", "any", None]:
                filters["platform"] = query_analysis["platform"]
                
            if query_analysis.get("feature") and query_analysis["feature"] not in ["unknown", None]:
                filters["product_area"] = query_analysis["feature"]
            
            # Retrieve initial context
            initial_chunks = await self.vector_store.search(
                query=query,
                filters=filters,
                limit=initial_results
            )
            
            # Refine context with context agent
            refined_context = await self.retrieval_agent.refine_context(
                query=query,
                query_analysis=query_analysis,
                retrieved_chunks=initial_chunks
            )
            
            context = refined_context.get("chunks", [])[:final_results]
            
            metrics["steps"]["context_retrieval"] = {
                "duration": time.time() - step_start,
                "num_contexts": len(context),
                "information_gaps": refined_context.get("information_gaps", []),
                "suggested_queries": refined_context.get("suggested_follow_up_queries", [])
            }
            
            # Step 3: Response Generation
            step_start = time.time()
            response = await self.response_agent.generate_response(
                query=query,
                query_analysis=query_analysis,
                context=context
            )
            metrics["steps"]["response_generation"] = {
                "duration": time.time() - step_start
            }
            
            # Add metrics to the response
            end_time = time.time()
            metrics["total_duration"] = end_time - start_time
            response["metrics"] = metrics
            
            # Update overall metrics
            self._update_metrics(True, metrics["total_duration"])
            
            return response
        except Exception as e:
            end_time = time.time()
            error_response = {
                "error": str(e),
                "metrics": metrics,
                "query": query
            }
            
            # Add total duration
            error_response["metrics"]["total_duration"] = end_time - start_time
            
            # Update overall metrics
            self._update_metrics(False, error_response["metrics"]["total_duration"])
            
            return error_response
    
    def _update_metrics(self, success: bool, duration: float) -> None:
        """
        Update the metrics after processing a query.
        
        Args:
            success: Whether the query was processed successfully
            duration: Processing duration in seconds
        """
        self.metrics["queries_processed"] += 1
        
        if success:
            self.metrics["avg_response_time"] = (self.metrics["avg_response_time"] * (self.metrics["queries_processed"] - 1) + duration) / self.metrics["queries_processed"]
        else:
            self.metrics["avg_response_time"] = (self.metrics["avg_response_time"] * (self.metrics["queries_processed"] - 1) + duration) / self.metrics["queries_processed"]
        
        # Update total chunks retrieved
        self.metrics["total_chunks_retrieved"] += len(context)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics for the orchestrator.
        
        Returns:
            Dictionary containing metrics
        """
        return self.metrics 