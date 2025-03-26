from typing import Dict, Any, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import uuid
import hashlib

class DocumentationChunker:
    """
    Chunks documentation into smaller pieces for embedding and retrieval.
    Uses langchain's RecursiveCharacterTextSplitter with custom configurations
    for documentation markdown files.
    """
    
    def __init__(self, chunk_size=800, chunk_overlap=100):
        """
        Initialize the chunker with specified size and overlap.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        # Custom separators optimized for markdown documentation
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                # Headers first
                "## ", 
                "### ",
                "#### ",
                # Then paragraph breaks
                "\n\n", 
                "\n", 
                # Then sentence endings
                ". ", 
                "! ", 
                "? ", 
                # Then other punctuation
                "; ", 
                ": ", 
                " ", 
                ""
            ]
        )
        
        # Regex patterns for extracting code blocks
        self.code_block_pattern = re.compile(r'```(?:\w+)?\s*\n(.*?)\n```', re.DOTALL)
        
    def preserve_code_blocks(self, content: str) -> List[Dict[str, Any]]:
        """
        Extracts code blocks from content for separate processing.
        
        Args:
            content: Markdown content with code blocks
            
        Returns:
            List of dictionaries with code blocks and their positions
        """
        code_blocks = []
        for match in self.code_block_pattern.finditer(content):
            code_blocks.append({
                "code": match.group(1),
                "start": match.start(),
                "end": match.end()
            })
        return code_blocks
    
    def generate_chunk_id(self, source: str, chunk_index: int) -> str:
        """
        Generate a unique ID for a chunk.
        
        Args:
            source: Source file path
            chunk_index: Index of chunk in the document
            
        Returns:
            Unique ID string
        """
        # Create a stable ID based on source and chunk index
        source_hash = hashlib.md5(source.encode('utf-8')).hexdigest()[:8]
        return f"chunk_{source_hash}_{chunk_index}"
    
    def chunk_document(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunks a document into smaller pieces while preserving context.
        
        Args:
            content: The document content to chunk
            metadata: Metadata about the document
            
        Returns:
            List of dictionaries containing chunks with their metadata
        """
        # Extract code blocks first
        code_blocks = self.preserve_code_blocks(content)
        
        # Split the content
        chunks = self.splitter.split_text(content)
        
        # Process chunks with metadata
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            # Check if this chunk contains any code blocks
            chunk_code_blocks = []
            for code_block in code_blocks:
                # Simple heuristic to check if code block belongs to this chunk
                if any(code in chunk for code in code_block["code"].split('\n')[:2]):
                    chunk_code_blocks.append(code_block["code"])
            
            # Generate a unique ID for this chunk
            chunk_id = self.generate_chunk_id(metadata["source"], i)
            
            # Create chunk with metadata
            processed_chunks.append({
                "id": chunk_id,
                "content": chunk,
                "source": metadata["source"],
                "title": metadata.get("title", ""),
                "chunk_id": chunk_id,  # For backward compatibility
                "chunk_number": i,
                "total_chunks": len(chunks),
                "embedding": [],  # Will be filled in by the embedding generator
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "has_code": len(chunk_code_blocks) > 0,
                    "code_blocks": chunk_code_blocks
                }
            })
        
        return processed_chunks 