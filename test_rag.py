#!/usr/bin/env python3
"""
Test script for the LikeMinds RAG system.
This script initializes the components and runs a simple query.
"""

import os
import asyncio
import json
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check required environment variables
required_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set them in the .env file or environment.")
    exit(1)

# Test individual components
async def test_query_understanding_agent():
    try:
        from backend.app.core.agents.query_understanding_agent import QueryUnderstandingAgent
        print("🔍 Testing Query Understanding Agent...")
        agent = QueryUnderstandingAgent()
        test_query = "How do I implement chat in React Native?"
        result = await agent.analyze_query(test_query)
        print(f"✅ Query Understanding Agent Test Successful!")
        print(f"Result: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error testing Query Understanding Agent: {str(e)}")
        traceback.print_exc()
        return False

async def test_context_retrieval_agent():
    try:
        from backend.app.core.agents.context_retrieval_agent import ContextRetrievalAgent
        print("🔍 Testing Context Retrieval Agent...")
        agent = ContextRetrievalAgent()
        print(f"✅ Context Retrieval Agent Initialized Successfully!")
        return True
    except Exception as e:
        print(f"❌ Error testing Context Retrieval Agent: {str(e)}")
        traceback.print_exc()
        return False

async def test_response_generation_agent():
    try:
        from backend.app.core.agents.response_generation_agent import ResponseGenerationAgent
        print("🔍 Testing Response Generation Agent...")
        agent = ResponseGenerationAgent()
        print(f"✅ Response Generation Agent Initialized Successfully!")
        return True
    except Exception as e:
        print(f"❌ Error testing Response Generation Agent: {str(e)}")
        traceback.print_exc()
        return False

async def test_embedding_generator():
    try:
        from backend.app.core.document_processor.embedding_generator import EmbeddingGenerator
        print("🔍 Testing Embedding Generator...")
        generator = EmbeddingGenerator()
        test_query = "How do I implement chat in React Native?"
        embedding = await generator.generate_query_embedding(test_query)
        print(f"✅ Embedding Generator Test Successful! (Embedding dimension: {len(embedding)})")
        return True
    except Exception as e:
        print(f"❌ Error testing Embedding Generator: {str(e)}")
        traceback.print_exc()
        return False

async def test_document_analyzer():
    try:
        from backend.app.core.document_processor.document_analyzer import DocumentAnalyzer
        print("🔍 Testing Document Analyzer...")
        analyzer = DocumentAnalyzer()
        test_content = "# Chat Implementation\nThis document explains how to implement chat in React Native using LikeMinds SDK."
        test_metadata = {"platform": "React Native", "product_area": "chat"}
        result = await analyzer.analyze_document(test_content, test_metadata)
        print(f"✅ Document Analyzer Test Successful!")
        print(f"Result: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error testing Document Analyzer: {str(e)}")
        traceback.print_exc()
        return False

async def test_query():
    try:
        # Import the agent orchestrator
        from backend.app.core.agents.agent_orchestrator import AgentOrchestrator
        
        print("🔧 Initializing the agent orchestrator...")
        orchestrator = AgentOrchestrator(vector_store_path="./backend/chroma_db")
        
        # Define a test query
        test_query = "How do I implement chat in React Native?"
        
        print(f"🔍 Processing query: '{test_query}'")
        response = await orchestrator.process_query(
            query=test_query,
            initial_results=3,
            final_results=2
        )
        
        # Print the response
        print("\n✅ Query processing complete!")
        print("\n📊 Response Metrics:")
        print(f"  Total Duration: {response['metrics']['total_duration']:.2f} seconds")
        
        # Print steps timing
        for step, data in response["metrics"]["steps"].items():
            if "duration" in data:
                print(f"  {step.replace('_', ' ').title()}: {data['duration']:.2f} seconds")
        
        print("\n📝 AI Response:")
        print("=" * 80)
        print(response["response"])
        print("=" * 80)
        
        # Print sources
        if "sources" in response and response["sources"]:
            print("\n📚 Sources:")
            for i, source in enumerate(response["sources"]):
                print(f"  {i+1}. {source}")
                
        return True
    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")
        traceback.print_exc()
        return False

async def run_tests():
    print("🧪 Running component tests...")
    
    # Test individual components first
    components_success = True
    
    print("\n[1/5] Testing Query Understanding Agent")
    if not await test_query_understanding_agent():
        components_success = False
        
    print("\n[2/5] Testing Context Retrieval Agent")
    if not await test_context_retrieval_agent():
        components_success = False
        
    print("\n[3/5] Testing Response Generation Agent")
    if not await test_response_generation_agent():
        components_success = False
        
    print("\n[4/5] Testing Embedding Generator")
    if not await test_embedding_generator():
        components_success = False
        
    print("\n[5/5] Testing Document Analyzer")
    if not await test_document_analyzer():
        components_success = False
    
    # Only run full integration test if all components pass
    if components_success:
        print("\n🚀 All component tests passed! Running integration test...")
        integration_success = await test_query()
        if integration_success:
            print("\n✨ All tests passed successfully!")
        else:
            print("\n⚠️ Integration test failed, but individual components look good.")
            print("This might be due to missing vector data in ChromaDB.")
    else:
        print("\n⚠️ Some component tests failed. Skipping integration test.")

if __name__ == "__main__":
    print("🚀 Testing the LikeMinds RAG system...")
    asyncio.run(run_tests()) 