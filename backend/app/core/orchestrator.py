import os
import uuid
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

from .agents.query_understanding_agent import QueryUnderstandingAgent
from .agents.context_retrieval_agent import ContextRetrievalAgent
from .agents.response_generation_agent import ResponseGenerationAgent
from .document_processor.embedding_generator import EmbeddingGenerator
from .vector_store.chroma_store import ChromaStore

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrates the RAG workflow by coordinating the different agents:
    1. Query Understanding Agent: Analyzes and enhances the user query
    2. Context Retrieval Agent: Retrieves relevant document chunks 
    3. Response Generation Agent: Generates the final response
    """
    
    def __init__(self):
        """Initialize the orchestrator with all required agents."""
        self.query_agent = QueryUnderstandingAgent()
        self.retrieval_agent = ContextRetrievalAgent()
        self.response_agent = ResponseGenerationAgent()
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = ChromaStore()
        
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process a user query through the full RAG pipeline.
        
        Args:
            query: The user's query text
            conversation_history: Optional list of previous conversation turns
            
        Returns:
            Dictionary containing the response, sources, and metrics
        """
        start_time = __import__('time').time()
        conversation_history = conversation_history or []
        metrics = {}
        
        # Step 1: Query understanding - enhance the original query
        logger.info(f"Processing query: {query}")
        enhanced_query = await self.query_agent.enhance_query(query, conversation_history)
        metrics["query_enhancement_time"] = __import__('time').time() - start_time
        logger.info(f"Enhanced query: {enhanced_query}")
        
        # Step 2: Generate embedding for the enhanced query
        query_embedding_time = __import__('time').time()
        query_embedding = await self.embedding_generator.generate_query_embedding(enhanced_query)
        metrics["query_embedding_time"] = __import__('time').time() - query_embedding_time
        
        # Step 3: Retrieve relevant context
        retrieval_time = __import__('time').time()
        context_docs = await self.vector_store.search(query_embedding, n_results=5)
        metrics["retrieval_time"] = __import__('time').time() - retrieval_time
        logger.info(f"Retrieved {len(context_docs)} documents")
        
        # Step 4: Rerank and filter documents (if needed)
        reranking_time = __import__('time').time()
        ranked_docs = await self.retrieval_agent.rerank_documents(enhanced_query, context_docs)
        metrics["reranking_time"] = __import__('time').time() - reranking_time
        
        # Step 5: Generate final response
        response_time = __import__('time').time()
        response, sources = await self.response_agent.generate_response(
            query, 
            enhanced_query, 
            ranked_docs, 
            conversation_history
        )
        metrics["response_generation_time"] = __import__('time').time() - response_time
        
        # Calculate total processing time
        metrics["total_time"] = __import__('time').time() - start_time
        
        # Return formatted response
        return {
            "query": query,
            "enhanced_query": enhanced_query,
            "response": response,
            "sources": sources,
            "metrics": metrics
        } 