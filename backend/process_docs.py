#!/usr/bin/env python3
"""
Script to process LikeMinds documentation and store it in ChromaDB.
This script scans all markdown files in the specified directories, 
chunks them, generates embeddings, and stores them in ChromaDB for retrieval.
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv
from app.core.document_processor.document_processor import DocumentProcessor

# Load environment variables
load_dotenv()

# Check for required API keys
required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"ERROR: Missing required API keys: {', '.join(missing_keys)}")
    print("Please add them to your .env file")
    exit(1)

async def process_documentation(directories, output_file="processing_stats.json"):
    """
    Process documentation in the specified directories.
    
    Args:
        directories: List of directories to process
        output_file: Output file for processing statistics
    """
    # Initialize the document processor
    processor = DocumentProcessor(
        chunk_size=800,
        chunk_overlap=100
    )
    
    # Convert all directories to absolute paths
    abs_directories = []
    for directory in directories:
        if not os.path.isabs(directory):
            # Use Path to handle cross-platform path resolution
            directory = str(Path(directory).resolve())
        abs_directories.append(directory)
    
    # Process each directory
    for directory in abs_directories:
        print(f"\n{'=' * 80}")
        print(f"Processing directory: {directory}")
        print(f"{'=' * 80}")
        
        if not os.path.exists(directory):
            print(f"Directory does not exist: {directory}")
            continue
        
        # Process the directory
        try:
            stats = await processor.process_directory(directory)
            print(f"\nProcessed {stats['total_documents']} documents in {directory}")
            print(f"Created {stats['total_chunks']} chunks")
        except Exception as e:
            print(f"Error processing directory {directory}: {str(e)}")
    
    # Save processing statistics
    processor.save_stats(output_file)
    print(f"\nProcessing complete. Statistics saved to {output_file}")
    
    # Print any errors at the end
    if processor.stats["processing_warnings"]:
        print("\nERRORS and WARNINGS:")
        for warning in processor.stats["processing_warnings"]:
            print(f"- {warning}")

def main():
    """Main entry point"""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory to ensure imports work correctly
    os.chdir(script_dir)
    
    parser = argparse.ArgumentParser(description="Process LikeMinds documentation for RAG")
    parser.add_argument(
        "--directories", 
        nargs="+", 
        default=["../docs/chat", "../docs/feed"],
        help="Directories to process (default: ../docs/chat ../docs/feed)"
    )
    parser.add_argument(
        "--output", 
        default="processing_stats.json",
        help="Output file for processing statistics (default: processing_stats.json)"
    )
    
    args = parser.parse_args()
    
    # Run the processing
    asyncio.run(process_documentation(args.directories, args.output))

if __name__ == "__main__":
    main() 