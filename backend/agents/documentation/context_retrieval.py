"""
Context Retrieval Agent.

This agent fetches relevant documentation context based on user queries.
"""

import logging
from typing import Dict, Any, List, Optional
from langchain.vectorstores import Redis
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class ContextRetrievalAgent:
    """
    Agent that retrieves relevant documentation context based on user queries.
    """
    
    def __init__(self, 
                redis_url: str = "redis://localhost:6379",
                embedding_model: str = "text-embedding-3-small",
                index_name: str = "documentation"):
        """
        Initialize the Context Retrieval Agent.
        
        Args:
            redis_url: URL for the Redis vector store
            embedding_model: Name of the embedding model to use
            index_name: Name of the Redis index to use
        """
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = Redis.from_existing_index(
            embeddings=self.embeddings,
            redis_url=redis_url,
            index_name=index_name
        )
    
    @trace("context_retrieval_agent.search")
    async def search(
        self,
        query: str,
        analyzed_query: Dict[str, Any],
        project_id: str,
        platform: str = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documentation context.
        
        Args:
            query: The original user query
            analyzed_query: The output from the QueryUnderstandingAgent
            project_id: The project ID for context
            platform: Optional platform filter (e.g., 'android', 'ios', 'web')
            k: Number of results to return
            
        Returns:
            A list of relevant context documents
        """
        try:
            # Build search query with enhanced context
            entities = analyzed_query.get("entities", [])
            entity_text = " ".join(entities) if entities else ""
            
            # Combine original query with extracted entities for better search
            enhanced_query = f"{query} {entity_text}"
            
            # Add metadata filters
            filter_dict = {"project_id": project_id}
            if platform:
                filter_dict["platform"] = platform
            
            # Perform the search
            with monitor("context_retrieval_agent.search", 
                        {"query_length": len(enhanced_query), "k": k}):
                docs = await self.vectorstore.asimilarity_search_with_relevance_scores(
                    enhanced_query, 
                    k=k,
                    filter=filter_dict
                )
            
            # Format the results
            results = []
            for doc, score in docs:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "relevance_score": score,
                    "metadata": doc.metadata
                })
                
            return results
                
        except Exception as e:
            logger.error(f"Error in context retrieval agent: {str(e)}", exc_info=True)
            return []
    
    @trace("context_retrieval_agent.add_document")
    async def add_document(
        self, 
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Add a document to the vectorstore.
        
        Args:
            content: The document content
            metadata: Metadata for the document
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a document
            doc = Document(page_content=content, metadata=metadata)
            
            # Add it to the vectorstore
            with monitor("context_retrieval_agent.add_document", 
                        {"content_length": len(content)}):
                await self.vectorstore.aadd_documents([doc])
            
            return True
                
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}", exc_info=True)
            return False 
    
    @trace("context_retrieval_agent.search_with_reranking")
    async def search_with_reranking(
        self,
        query: str,
        analyzed_query: Dict[str, Any],
        project_id: str,
        platform: str = None,
        k: int = 5,
        reranking_factor: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search with an additional reranking step for improved relevance.
        
        Args:
            query: The original user query
            analyzed_query: The output from the QueryUnderstandingAgent
            project_id: The project ID for context
            platform: Optional platform filter
            k: Number of results to return
            reranking_factor: Weight given to semantic vs. keyword matching
            
        Returns:
            A list of relevant context documents with improved ranking
        """
        # Initial vector search (retrieve more than needed for reranking)
        initial_results = await self.search(query, analyzed_query, project_id, platform, k=k*2)
        
        # Extract sdk component and integration phase from analyzed query
        sdk_components = analyzed_query.get("sdk_components", {})
        integration_phase = analyzed_query.get("integration_phase", "")
        
        # Reranking logic
        for result in initial_results:
            # Base score from vector similarity
            base_score = result["relevance_score"]
            
            # Component match bonus
            component_match_score = 0
            if sdk_components:
                primary_component = sdk_components.get("primary", "")
                if primary_component and primary_component.lower() in result["content"].lower():
                    component_match_score = 0.2
            
            # Code example bonus for implementation questions
            code_example_score = 0
            if integration_phase == "starting implementation" and "```" in result["content"]:
                code_example_score = 0.15
                
            # Platform specificity bonus
            platform_score = 0
            if platform and platform.lower() in result["metadata"].get("platform", "").lower():
                platform_score = 0.1
                
            # Calculate final score with weights
            result["final_score"] = (
                reranking_factor * base_score + 
                (1 - reranking_factor) * (component_match_score + code_example_score + platform_score)
            )
        
        # Sort by final score and return top k
        reranked_results = sorted(initial_results, key=lambda x: x["final_score"], reverse=True)[:k]
        
        return reranked_results 