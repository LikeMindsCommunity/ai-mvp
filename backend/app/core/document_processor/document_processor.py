import os
import glob
from typing import Dict, Any, List, Optional
import asyncio
import json
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

from .document_analyzer import DocumentAnalyzer
from .document_chunker import DocumentationChunker
from .embedding_generator import EmbeddingGenerator
# Remove circular import
# from ..vector_store.chroma_store import ChromaStore

class DocumentProcessor:
    """
    Orchestrates the document processing pipeline for LikeMinds documentation.
    Handles chunking, analysis, embedding generation, and storage.
    """
    
    def __init__(self, 
                chunk_size: int = 800, 
                chunk_overlap: int = 100,
                embedding_model: str = "text-embedding-3-large",
                persist_directory: str = "./chroma_db"):
        """
        Initialize the document processor with all required components.
        
        Args:
            chunk_size: Maximum chunk size for the text splitter
            chunk_overlap: Overlap between chunks
            embedding_model: Name of the embedding model to use
            persist_directory: Directory to persist ChromaDB
        """
        self.chunker = DocumentationChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.analyzer = DocumentAnalyzer()
        self.embedding_generator = EmbeddingGenerator(model=embedding_model)
        self.persist_directory = persist_directory
        
        # Don't initialize ChromaStore here to avoid circular import
        self.vector_store = None
        
        self.stats = {
            "total_documents": 0,
            "total_chunks": 0,
            "product_areas": {
                "chat": 0,
                "feed": 0
            },
            "platforms": {},
            "average_chunk_size": 0,
            "processing_warnings": []
        }
        
        print(f"Document processor initialized with chunk size={chunk_size}, overlap={chunk_overlap}")
    
    def _initialize_vector_store(self):
        """
        Lazily initialize the vector store when needed.
        This avoids circular imports.
        """
        if self.vector_store is None:
            # Import here to avoid circular import
            from ..vector_store.chroma_store import ChromaStore
            self.vector_store = ChromaStore()
            print(f"Vector store initialized with path {self.persist_directory}")

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract and derive metadata from the file path and content.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Dictionary containing metadata
        """
        path = Path(file_path)
        
        # Determine product area (chat or feed)
        if "/docs/" in file_path or "\\docs\\" in file_path:
            product_area = "chat"
            self.stats["product_areas"]["chat"] += 1
        elif "/feed/" in file_path or "\\feed\\" in file_path:
            product_area = "feed"
            self.stats["product_areas"]["feed"] += 1
        else:
            product_area = "other"
        
        # Determine platform/technology
        platform_dirs = ["Android", "Flutter", "iOS", "React", "React_Native", "REST-API"]
        platform = "general"
        for p in platform_dirs:
            if f"/{p}/" in file_path or f"\\{p}\\" in file_path:
                platform = p
                self.stats["platforms"][platform] = self.stats["platforms"].get(platform, 0) + 1
                break
        
        # Determine document type based on directory structure or naming conventions
        if "getting-started" in file_path.lower():
            doc_type = "tutorial"
        elif "api-reference" in file_path.lower() or "api" in file_path.lower():
            doc_type = "api"
        elif "concepts" in file_path.lower():
            doc_type = "concept"
        else:
            doc_type = "guide"
            
        # Extract title from the file name
        title = path.stem.replace("-", " ").title()
        
        # Create metadata object
        metadata = {
            "source": file_path,
            "title": title,
            "product_area": product_area,
            "platform": platform,
            "document_type": doc_type,
            "path_in_hierarchy": "/".join(path.parts[-3:]) if len(path.parts) >= 3 else str(path)
        }
        
        return metadata
    
    def extract_content_from_markdown(self, file_path: str) -> str:
        """
        Extract content from a markdown file, including front matter.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Extracted content as text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.strip():
                self.stats["processing_warnings"].append(f"Empty content in {file_path}")
                return ""
                
            return content
            
        except Exception as e:
            error_msg = f"Error extracting content from {file_path}: {str(e)}"
            print(error_msg)
            self.stats["processing_warnings"].append(error_msg)
            return ""
    
    def get_tokens_estimate(self, text: str) -> int:
        """
        Estimate the number of tokens in the text.
        
        Args:
            text: The text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        # A very rough estimate: ~4 characters per token for English text
        return len(text) // 4
    
    async def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a single documentation file through the entire pipeline.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            List of processed chunks with embeddings
        """
        try:
            print(f"Processing document: {file_path}")
            
            # Extract content and metadata
            content = self.extract_content_from_markdown(file_path)
            if not content.strip():
                print(f"  - Warning: Empty content in {file_path}")
                return []
            
            metadata = self.extract_metadata(file_path)
            
            # Chunk the document
            chunks = self.chunker.chunk_document(content, metadata)
            
            if not chunks:
                print(f"  - Warning: No chunks created for {file_path}")
                return []
                
            print(f"  - Created {len(chunks)} chunks")
            
            # Keep track of statistics
            self.stats["total_chunks"] += len(chunks)
            self.stats["total_documents"] += 1
            
            if chunks:
                avg_chunk_size = sum(self.get_tokens_estimate(chunk["content"]) for chunk in chunks) / len(chunks)
                self.stats["average_chunk_size"] = (
                    (self.stats["average_chunk_size"] * (self.stats["total_chunks"] - len(chunks)) + 
                    avg_chunk_size * len(chunks)) / self.stats["total_chunks"]
                )
            
            # Generate embeddings
            chunks_with_embeddings = await self.embedding_generator.generate_embeddings(chunks)
            print(f"  - Generated embeddings for {len(chunks_with_embeddings)} chunks")
            
            # Initialize vector store lazily when needed
            self._initialize_vector_store()
            
            # Store chunks in vector database
            await self.vector_store.add_documents(chunks_with_embeddings)
            
            return chunks_with_embeddings
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            print(f"  - ERROR: {error_msg}")
            self.stats["processing_warnings"].append(error_msg)
            return []
    
    async def process_directory(self, directory: str, file_pattern: str = "**/*.md") -> Dict[str, Any]:
        """
        Process all markdown files in a directory and its subdirectories.
        
        Args:
            directory: Directory to process
            file_pattern: Glob pattern for files to process
            
        Returns:
            Processing statistics
        """
        # Find all markdown files
        file_pattern_full = os.path.join(directory, file_pattern)
        file_paths = glob.glob(file_pattern_full, recursive=True)
        print(f"Found {len(file_paths)} markdown files to process in {directory}")
        
        if not file_paths:
            self.stats["processing_warnings"].append(f"No files found matching pattern {file_pattern_full}")
            return self.stats
        
        # Process files in batches to avoid overwhelming the API
        batch_size = 10
        total_processed = 0
        
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(file_paths) + batch_size - 1)//batch_size}: {len(batch)} files")
            
            # Process files concurrently
            tasks = [self.process_document(file_path) for file_path in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for exceptions
            for j, result in enumerate(results):
                if isinstance(result, Exception):
                    error_msg = f"Error processing {batch[j]}: {str(result)}"
                    print(f"  - ERROR: {error_msg}")
                    self.stats["processing_warnings"].append(error_msg)
            
            total_processed += len(batch)
            print(f"Progress: {total_processed}/{len(file_paths)} files processed")
        
        return self.stats
    
    def save_stats(self, output_file: str = "processing_stats.json") -> None:
        """
        Save processing statistics to a JSON file.
        
        Args:
            output_file: Output file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nProcessing statistics saved to {output_file}")
        print(f"Total documents processed: {self.stats['total_documents']}")
        print(f"Total chunks created: {self.stats['total_chunks']}")
        print(f"Average chunk size (tokens): {self.stats['average_chunk_size']:.2f}")
        print(f"Chat documents: {self.stats['product_areas']['chat']}")
        print(f"Feed documents: {self.stats['product_areas']['feed']}")
        
        if self.stats["processing_warnings"]:
            print(f"\nWarnings ({len(self.stats['processing_warnings'])}):")
            for warning in self.stats["processing_warnings"][:5]:
                print(f"- {warning}")
            if len(self.stats["processing_warnings"]) > 5:
                print(f"... {len(self.stats['processing_warnings']) - 5} more warnings") 