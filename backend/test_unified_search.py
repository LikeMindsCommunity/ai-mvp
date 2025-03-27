#!/usr/bin/env python3
"""
Test script to perform unified search across all collections in the vector database.
This allows querying code, documentation, and SDK knowledge simultaneously.
"""

import os
import asyncio
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv
from app.core.vector_store.chroma_store import ChromaStore

# Load environment variables
load_dotenv()

async def unified_search(query, limit=5, collections=None):
    """
    Search across multiple collections in the vector database.
    
    Args:
        query: The search query
        limit: Maximum number of results to return per collection
        collections: List of collections to search (defaults to all available)
        
    Returns:
        Dict mapping collection names to search results
    """
    print(f"Searching for: {query}")
    print(f"Max results per collection: {limit}")
    print("-" * 80)
    
    # Default collections
    all_collections = ["code_repository", "documentation", "sdk_knowledge"]
    
    # Use provided collections or defaults
    collections = collections or all_collections
    
    # Search each collection
    results = {}
    for collection_name in collections:
        try:
            # Initialize the vector store for this collection
            vector_store = ChromaStore(collection_name=collection_name)
            
            # Search for results
            collection_results = await vector_store.similarity_search(query, limit=limit)
            
            # Add to results dict
            results[collection_name] = collection_results
            
            print(f"Found {len(collection_results)} results in {collection_name}")
        except Exception as e:
            print(f"Error searching collection {collection_name}: {str(e)}")
            results[collection_name] = []
    
    return results

def display_results(results_by_collection):
    """Display search results in a readable format by collection."""
    print("\n" + "=" * 80)
    print("SEARCH RESULTS")
    print("=" * 80)
    
    total_results = sum(len(results) for results in results_by_collection.values())
    if total_results == 0:
        print("No results found in any collection.")
        return
    
    # Display results by collection
    for collection_name, results in results_by_collection.items():
        if not results:
            continue
            
        print(f"\n## {collection_name.upper()} ({len(results)} results)\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            
            # Display source information
            if collection_name == "code_repository":
                print(f"  File: {result['metadata'].get('file_path', 'Unknown')}")
                print(f"  Repository: {result['metadata'].get('repository_path', 'Unknown')}")
                print(f"  Language: {result['metadata'].get('language', 'Unknown')}")
            elif collection_name == "documentation":
                print(f"  Document: {result['metadata'].get('title', 'Unknown')}")
                print(f"  Source: {result['metadata'].get('source', 'Unknown')}")
                print(f"  Type: {result['metadata'].get('document_type', 'Unknown')}")
            elif collection_name == "sdk_knowledge":
                print(f"  Source: {result['metadata'].get('source', 'Unknown')}")
                print(f"  Content Type: {result['metadata'].get('content_type', 'Unknown')}")
            
            # Display content with line numbers
            print("\n  Content:")
            content_lines = result["content"].split("\n")
            for j, line in enumerate(content_lines[:15], 1):
                print(f"    {j}: {line}")
            
            if len(content_lines) > 15:
                print(f"    ... and {len(content_lines) - 15} more lines")
            
            # Display additional metadata
            print("\n  Metadata:")
            exclusions = ["file_path", "repository_path", "language", "title", "source", "document_type", "content_type"]
            for key, value in result["metadata"].items():
                if key not in exclusions:
                    print(f"    {key}: {value}")
            
            print("-" * 80)

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Unified search across all vector database collections")
    parser.add_argument("query", nargs="?", default=None, help="Search query")
    parser.add_argument("--limit", type=int, default=3, help="Maximum number of results per collection (default: 3)")
    parser.add_argument("--collections", nargs="+", help="Collections to search (default: all collections)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("=== Unified Search (Interactive Mode) ===")
        print("Enter 'exit' to quit")
        
        while True:
            query = input("\nEnter search query: ")
            if query.lower() in ["exit", "quit", "q"]:
                break
            
            results = await unified_search(query, args.limit, args.collections)
            display_results(results)
    
    elif args.query:
        results = await unified_search(args.query, args.limit, args.collections)
        display_results(results)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())