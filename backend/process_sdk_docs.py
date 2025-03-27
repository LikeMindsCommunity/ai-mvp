#!/usr/bin/env python3
"""
Script to process SDK architecture documentation and add it to the vector database.
This provides the AI assistant with structured knowledge about the SDKs.
"""

import os
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv
from app.core.document_processor.document_processor import DocumentProcessor
from app.core.vector_store.chroma_store import ChromaStore

# Load environment variables
load_dotenv()

async def process_sdk_documentation(doc_path, output_file="sdk_docs_processing_stats.json"):
    """
    Process SDK architecture documentation and add it to the vector database.
    
    Args:
        doc_path: Path to the SDK documentation markdown file
        output_file: Output file for processing statistics
    """
    print(f"\n{'=' * 80}")
    print(f"Processing SDK architecture documentation: {doc_path}")
    print(f"{'=' * 80}")
    
    if not os.path.exists(doc_path):
        print(f"Documentation file does not exist: {doc_path}")
        return
    
    # Initialize the document processor with smaller chunks for more granular retrieval
    processor = DocumentProcessor(
        chunk_size=500,
        chunk_overlap=150
    )
    
    # Process the document
    try:
        # Extract content
        with open(doc_path, 'r') as f:
            content = f.read()
        
        # Create metadata for the SDK documentation
        metadata = {
            "source": str(doc_path),
            "title": "SDK Architecture Guide",
            "document_type": "sdk_architecture",
            "content_type": "sdk_knowledge",
            "importance": "high"
        }
        
        # Chunk the document
        chunks = processor.chunker.chunk_document(content, metadata)
        print(f"Created {len(chunks)} chunks from SDK documentation")
        
        # Generate embeddings
        chunks_with_embeddings = await processor.embedding_generator.generate_embeddings(chunks)
        print(f"Generated embeddings for {len(chunks_with_embeddings)} chunks")
        
        # Initialize vector store
        vector_store = ChromaStore(collection_name="sdk_knowledge")
        
        # Store chunks in vector database
        await vector_store.add_documents(chunks_with_embeddings)
        print(f"Stored {len(chunks_with_embeddings)} chunks in vector database")
        
        # Save stats
        stats = {
            "file_processed": str(doc_path),
            "chunks_created": len(chunks),
            "chunks_embedded": len(chunks_with_embeddings)
        }
        
        with open(output_file, 'w') as f:
            import json
            json.dump(stats, f, indent=2)
        
        print(f"Processing complete. Statistics saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing SDK documentation: {str(e)}")

async def main():
    """Main entry point"""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory to ensure imports work correctly
    os.chdir(script_dir)
    
    parser = argparse.ArgumentParser(description="Process SDK architecture documentation")
    parser.add_argument(
        "--doc-path", 
        default="../docs/sdk_architecture_guide.md",
        help="Path to the SDK architecture markdown file (default: ../docs/sdk_architecture_guide.md)"
    )
    parser.add_argument(
        "--output", 
        default="sdk_docs_processing_stats.json",
        help="Output file for processing statistics (default: sdk_docs_processing_stats.json)"
    )
    
    args = parser.parse_args()
    
    # Run the processing
    await process_sdk_documentation(args.doc_path, args.output)

if __name__ == "__main__":
    asyncio.run(main()) 