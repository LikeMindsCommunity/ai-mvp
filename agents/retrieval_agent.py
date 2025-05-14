"""
Information Retrieval Agent for the RAG system.
This agent handles vector search and document retrieval.
"""

from typing import List, Dict, Any, Optional
import os

from agents.base import BaseAgent
from agents.config import VECTOR_DB_PATH, VECTOR_DB_TYPE
from agno.tools.reasoning import ReasoningTools


class InformationRetrievalAgent(BaseAgent):
    """Agent for retrieving relevant information from documentation and code."""
    
    def __init__(
        self,
        vector_db_path: str = VECTOR_DB_PATH,
        use_claude: bool = False
    ):
        """
        Initialize the information retrieval agent.
        
        Args:
            vector_db_path: Path to the vector database
            use_claude: Whether to use Claude instead of Gemini
        """
        # Define instructions for the agent
        instructions = [
            "You are a retrieval expert that finds relevant information from documents.",
            "For each query, return the most relevant information from the vector database.",
            "Include source information with each retrieved chunk."
        ]
        
        # Initialize the base agent
        super().__init__(
            use_claude=use_claude,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=instructions,
            markdown=True
        )
        
        self.vector_db_path = vector_db_path
        # We'll initialize the vector DB connection later to avoid
        # loading it unless actually needed
        self.vector_db = None
        
    def _init_vector_db(self):
        """Initialize the vector database connection if not already initialized."""
        if self.vector_db is not None:
            return
            
        # This is a placeholder - we'll implement the actual vector DB connection
        # once we determine which library to use (ChromaDB, etc.)
        if VECTOR_DB_TYPE.lower() == "chroma":
            # Import ChromaDB here to avoid importing it if not used
            try:
                import chromadb
                self.vector_db = chromadb.PersistentClient(path=self.vector_db_path)
                print(f"Connected to ChromaDB at {self.vector_db_path}")
            except ImportError:
                print("Error: ChromaDB not installed. Run 'pip install chromadb'")
                raise
        else:
            raise ValueError(f"Unsupported vector database type: {VECTOR_DB_TYPE}")
            
    def retrieve(
        self, 
        query: str, 
        collection_name: str = "flutter_docs",
        num_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: The search query
            collection_name: Name of the collection to search
            num_results: Number of results to retrieve
            filters: Optional metadata filters
            
        Returns:
            List of documents with their content and metadata
        """
        self._init_vector_db()
        
        # This is a placeholder for the actual retrieval logic
        try:
            # Get the collection
            collection = self.vector_db.get_collection(name=collection_name)
            
            # Run the query
            results = collection.query(
                query_texts=[query],
                n_results=num_results,
                # Filters would be applied here if provided
            )
            
            # Check if we got any results
            if not results["documents"] or not results["documents"][0]:
                print(f"No documents found for query: {query}")
                return []
            
            # Format the results
            documents = []
            for i in range(len(results["documents"][0])):
                documents.append({
                    "content": results["documents"][0][i],
                    "metadata": {
                        "id": results["ids"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None,
                        "source": results["metadatas"][0][i].get("source", "Unknown"),
                        "type": results["metadatas"][0][i].get("type", "Unknown"),
                    }
                })
                
            return documents
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            # Return some default information when retrieval fails
            return [{
                "content": "LikeMinds is a community and chat SDK for Flutter that enables developers to add social features to their applications. It provides real-time messaging, user profiles, feeds, and engagement features.",
                "metadata": {
                    "id": "default_likeminds_info",
                    "source": "Default information (vector DB error)",
                    "type": "introduction"
                }
            }]
    
    def retrieve_and_format(
        self, 
        query: str,
        collection_name: str = "flutter_docs",
        num_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Retrieve documents and format them as a string for the LLM.
        
        Args:
            query: The search query
            collection_name: Name of the collection to search
            num_results: Number of results to retrieve
            filters: Optional metadata filters
            
        Returns:
            Formatted string with all retrieved content
        """
        documents = self.retrieve(
            query=query,
            collection_name=collection_name,
            num_results=num_results,
            filters=filters
        )
        
        if not documents:
            return "No relevant documents found. Please provide general information based on your knowledge."
        
        # Format the documents into a string
        result = "### Retrieved Documents\n\n"
        for i, doc in enumerate(documents):
            result += f"#### Document {i+1}\n"
            result += f"{doc['content']}\n\n"
            result += f"**Source**: {doc['metadata'].get('source', 'Unknown')}\n"
            result += f"**Type**: {doc['metadata'].get('type', 'Unknown')}\n\n"
            result += "---\n\n"
            
        return result 