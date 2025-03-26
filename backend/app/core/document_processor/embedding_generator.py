import os
from typing import Dict, Any, List
from langchain_openai import OpenAIEmbeddings
from tenacity import retry, stop_after_attempt, wait_exponential
from ..config.env import EMBEDDING_MODEL, API_KEYS

class EmbeddingGenerator:
    """
    Generates embeddings for document chunks using OpenAI's embedding models.
    These embeddings are used for semantic search and retrieval.
    """
    
    def __init__(self, model: str = None):
        """
        Initialize the embedding generator with OpenAI's embedding model.
        
        Args:
            model: The OpenAI embedding model to use (default: from config)
        """
        self.embedding_model = OpenAIEmbeddings(
            model=model or EMBEDDING_MODEL,
            openai_api_key=API_KEYS["OPENAI_API_KEY"]
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates embeddings for a list of document chunks.
        
        Args:
            chunks: List of dictionaries containing document chunks and metadata
            
        Returns:
            List of dictionaries with the original chunks plus their embeddings
        """
        if not chunks:
            return []
            
        # Extract just the content for embedding
        texts = [chunk["content"] for chunk in chunks]
        
        # Generate embeddings
        try:
            embeddings = await self.embedding_model.aembed_documents(texts)
            
            # Add embeddings to original chunks
            for i, embedding in enumerate(embeddings):
                chunks[i]["embedding"] = embedding
                
            return chunks
            
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            # Return chunks with empty embeddings rather than failing
            for chunk in chunks:
                if "embedding" not in chunk or not chunk["embedding"]:
                    chunk["embedding"] = []
            return chunks
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generates an embedding for a query string.
        
        Args:
            query: The query text to embed
            
        Returns:
            Embedding vector for the query
        """
        try:
            return await self.embedding_model.aembed_query(query)
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            # Return empty embedding in case of error
            return [] 