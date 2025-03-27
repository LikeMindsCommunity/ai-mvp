#!/usr/bin/env python3
"""
Test script to verify that code has been properly embedded in the vector database.
This script allows querying the code repository collection to retrieve relevant code snippets.
"""

import os
import asyncio
import argparse
from dotenv import load_dotenv
from app.core.vector_store.chroma_store import ChromaStore

# Load environment variables
load_dotenv()

async def search_code(query, limit=5, collection_name="code_repository"):
    """
    Search for code snippets relevant to the given query.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        collection_name: Name of the vector store collection
        
    Returns:
        List of search results
    """
    print(f"Searching for: {query}")
    print(f"Collection: {collection_name}")
    print(f"Limit: {limit}")
    print("-" * 80)
    
    # Initialize the vector store
    vector_store = ChromaStore(collection_name=collection_name)
    
    # Search for results
    results = await vector_store.similarity_search(query, limit=limit)
    
    return results

def display_results(results):
    """Display search results in a readable format."""
    if not results:
        print("No results found.")
        return
    
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  File: {result['metadata'].get('file_path', 'Unknown')}")
        print(f"  Repository: {result['metadata'].get('repository_path', 'Unknown')}")
        print(f"  Language: {result['metadata'].get('language', 'Unknown')}")
        
        # Display content with line numbers
        print("\n  Content:")
        content_lines = result["content"].split("\n")
        for j, line in enumerate(content_lines, 1):
            print(f"    {j}: {line}")
        
        print(f"\n  Metadata:")
        for key, value in result["metadata"].items():
            if key not in ["file_path", "repository_path", "language"]:
                print(f"    {key}: {value}")
        
        print("-" * 80)

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Search code repositories in vector database")
    parser.add_argument("query", nargs="?", default=None, help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results (default: 5)")
    parser.add_argument("--collection", default="code_repository", help="Vector store collection name (default: code_repository)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("=== Code Repository Search (Interactive Mode) ===")
        print("Enter 'exit' to quit")
        
        while True:
            query = input("\nEnter search query: ")
            if query.lower() in ["exit", "quit", "q"]:
                break
            
            results = await search_code(query, args.limit, args.collection)
            display_results(results)
    
    elif args.query:
        results = await search_code(args.query, args.limit, args.collection)
        display_results(results)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main()) 