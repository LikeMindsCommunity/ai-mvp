import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from ..document_processor.embedding_generator import EmbeddingGenerator
from ..config.env import CHROMA_DB_PATH

class ChromaStore:
    """
    Vector store implementation using ChromaDB. This class handles storing and retrieving
    document chunks by their embeddings for semantic similarity search.
    """
    
    def __init__(self, collection_name: str = "likeminds_docs"):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            collection_name: Name of the ChromaDB collection to use
        """
        # Get database path from environment or use default
        self.db_path = CHROMA_DB_PATH
        
        # Set up ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None  # We'll handle embeddings separately
        )
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator()
        
    async def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document dictionaries with embeddings
        """
        if not documents:
            print("Warning: No documents to add to vector store")
            return
            
        try:
            # Prepare the data for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_text = []
            
            for doc in documents:
                # Check for required fields
                if "id" not in doc:
                    print(f"Warning: Document missing ID field: {doc.get('source', 'unknown')}")
                    continue
                    
                if not doc.get("embedding"):
                    print(f"Warning: Document missing embedding: {doc['id']}")
                    continue
                
                # Add document to batch
                ids.append(str(doc["id"]))
                embeddings.append(doc["embedding"])
                
                # Handle metadata differently to ensure compatibility
                metadata = {
                    "source": doc.get("source", ""),
                    "title": doc.get("title", ""),
                    "chunk_id": doc.get("chunk_id", ""),
                    "chunk_number": doc.get("chunk_number", 0),
                    "total_chunks": doc.get("total_chunks", 1),
                    "product_area": doc.get("metadata", {}).get("product_area", ""),
                    "platform": doc.get("metadata", {}).get("platform", ""),
                    "document_type": doc.get("metadata", {}).get("document_type", "")
                }
                metadatas.append(metadata)
                documents_text.append(doc["content"])
            
            if not ids:
                print("Warning: No valid documents to add after filtering")
                return
                
            # Add documents to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_text
            )
            
            print(f"Added {len(ids)} documents to ChromaDB collection")
            
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {str(e)}")
        
    async def search(
        self, 
        query_embedding: List[float] = None,
        query: str = None,
        n_results: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using the query embedding or text.
        
        Args:
            query_embedding: Embedding vector for the query
            query: Text query (will generate embedding if query_embedding not provided)
            n_results: Number of results to return
            filter_dict: Dictionary of metadata filters
            
        Returns:
            List of retrieved documents with their similarity scores
        """
        try:
            # Prepare where clause if filter is provided
            where = filter_dict if filter_dict else None
            
            # Ensure we have an embedding to search with
            if query_embedding is None and query is not None:
                query_embedding = await self.embedding_generator.generate_query_embedding(query)
                
            if not query_embedding and not query:
                print("Error: Must provide either query_embedding or query")
                return []
                
            # Search parameters
            search_params = {
                "n_results": n_results,
                "where": where,
                "include": ["documents", "metadatas", "distances"]
            }
            
            # Search by embedding or by text
            if query_embedding:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    **search_params
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    **search_params
                )
            
            # Handle empty results
            if not results.get("ids") or not results["ids"][0]:
                return []
                
            # Format results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                # Calculate relevance score (1.0 is best, 0.0 is worst)
                score = 1.0 - min(results["distances"][0][i], 1.0)
                
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "score": score,
                    "relevance_score": round(score * 10, 1)  # Scale to 0-10 for easier human interpretation
                })
                
            return formatted_results
            
        except Exception as e:
            print(f"Error searching ChromaDB: {str(e)}")
            return []

    async def delete_collection(self):
        """
        Delete the current collection.
        """
        self.client.delete_collection(self.collection.name)

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current collection.
        
        Returns:
            Dictionary with collection stats
        """
        try:
            count = self.collection.count()
            return {
                "name": self.collection.name,
                "document_count": count
            }
        except Exception as e:
            return {
                "name": self.collection.name if hasattr(self, "collection") else "unknown",
                "error": str(e)
            } 