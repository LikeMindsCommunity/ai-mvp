#!/usr/bin/env python3
"""
Script to process LikeMinds code repositories and store them in ChromaDB.
This script scans all code files in the specified repositories,
analyzes them, chunks them, and stores the chunks in ChromaDB for retrieval.
"""

import os
import sys
import asyncio
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
from app.core.code_processor.code_processor import CodeProcessor
from app.core.vector_store.chroma_store import ChromaStore

# Load environment variables
load_dotenv()

# Check for required API keys
required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"ERROR: Missing required API keys: {', '.join(missing_keys)}")
    print("Please add them to your .env file")
    exit(1)

async def process_code_repositories(repositories, output_file="code_processing_stats.json"):
    """
    Process code repositories in the specified directories.
    
    Args:
        repositories: List of repository directories to process
        output_file: Output file for processing statistics
    """
    # Initialize the code processor
    processor = CodeProcessor(max_chunk_size=1000)
    
    # Initialize the vector store
    vector_store = ChromaStore(collection_name="code_repository")
    
    # Statistics
    stats = {
        "total_repositories": 0,
        "total_files": 0,
        "total_chunks": 0,
        "languages": {},
        "processing_warnings": []
    }
    
    # Convert all repositories to absolute paths
    abs_repositories = []
    for repo in repositories:
        if not os.path.isabs(repo):
            # Use Path to handle cross-platform path resolution
            repo = str(Path(repo).resolve())
        abs_repositories.append(repo)
    
    # Process each repository
    for repo_path in abs_repositories:
        print(f"\n{'=' * 80}")
        print(f"Processing repository: {repo_path}")
        print(f"{'=' * 80}")
        
        if not os.path.exists(repo_path):
            print(f"Repository does not exist: {repo_path}")
            stats["processing_warnings"].append(f"Repository does not exist: {repo_path}")
            continue
        
        # Process the repository
        try:
            repo_result = await processor.process_repository(Path(repo_path))
            print(f"\nProcessed repository: {repo_path}")
            
            if "error" in repo_result:
                print(f"Error processing repository: {repo_result['error']}")
                stats["processing_warnings"].append(f"Error processing repository {repo_path}: {repo_result['error']}")
                continue
            
            # Update statistics
            stats["total_repositories"] += 1
            stats["total_files"] += repo_result["analysis"]["total_files"]
            
            # Update language statistics
            for lang, count in repo_result["analysis"]["languages"].items():
                stats["languages"][lang] = stats["languages"].get(lang, 0) + count
            
            # Extract all chunks from the repository results
            all_chunks = []
            
            def extract_chunks(file_results, prefix=""):
                """Recursively extract chunks from nested file results"""
                extracted = []
                if isinstance(file_results, dict):
                    if "chunks" in file_results:
                        # This is a file result
                        for chunk in file_results["chunks"]:
                            # Add repository path and file path to metadata
                            chunk["metadata"]["repository_path"] = repo_path
                            chunk["metadata"]["file_path"] = file_results["file_path"]
                            extracted.append(chunk)
                    else:
                        # This is a directory
                        for key, value in file_results.items():
                            new_prefix = f"{prefix}/{key}" if prefix else key
                            extracted.extend(extract_chunks(value, new_prefix))
                return extracted
            
            # Extract chunks from the organized files
            chunks = extract_chunks(repo_result["files"])
            all_chunks.extend(chunks)
            
            # Update chunk statistics
            stats["total_chunks"] += len(chunks)
            print(f"Extracted {len(chunks)} chunks from repository")
            
            # Store chunks in vector database
            if chunks:
                await vector_store.add_documents(chunks)
                print(f"Stored {len(chunks)} chunks in vector database")
            
        except Exception as e:
            error_msg = f"Error processing repository {repo_path}: {str(e)}"
            print(error_msg)
            stats["processing_warnings"].append(error_msg)
    
    # Save processing statistics
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"\nProcessing complete. Statistics saved to {output_file}")
    
    # Print summary statistics
    print("\nSummary:")
    print(f"Processed {stats['total_repositories']} repositories")
    print(f"Processed {stats['total_files']} files")
    print(f"Created {stats['total_chunks']} chunks")
    print("\nLanguage distribution:")
    for lang, count in stats["languages"].items():
        print(f"- {lang}: {count} files")
    
    # Print any errors at the end
    if stats["processing_warnings"]:
        print("\nERRORS and WARNINGS:")
        for warning in stats["processing_warnings"]:
            print(f"- {warning}")

def main():
    """Main entry point"""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory to ensure imports work correctly
    os.chdir(script_dir)
    
    parser = argparse.ArgumentParser(description="Process LikeMinds code repositories for RAG")
    parser.add_argument(
        "--repositories", 
        nargs="+", 
        default=["../repos/chat", "../repos/feed"],
        help="Repositories to process (default: ../repos/chat ../repos/feed)"
    )
    parser.add_argument(
        "--output", 
        default="code_processing_stats.json",
        help="Output file for processing statistics (default: code_processing_stats.json)"
    )
    
    args = parser.parse_args()
    
    # Run the processing
    asyncio.run(process_code_repositories(args.repositories, args.output))

if __name__ == "__main__":
    main() 