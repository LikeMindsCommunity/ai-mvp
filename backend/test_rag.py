import os
import sys
import json
import asyncio
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Check for required environment variables
required_env_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set them in your .env file or environment.")
    sys.exit(1)

# Import application modules
from app.core.orchestrator import AgentOrchestrator
from app.core.vector_store.chroma_store import ChromaStore
from app.core.document_processor.embedding_generator import EmbeddingGenerator

async def test_vector_store():
    """Test retrieval from ChromaDB collection directly"""
    print("\n🔍 Testing ChromaDB Vector Store...")
    
    try:
        # Initialize the vector store
        vector_store = ChromaStore()
        embedding_generator = EmbeddingGenerator()
        
        # Print collection info
        collection_size = vector_store.collection.count()
        print(f"✅ Connected to ChromaDB collection with {collection_size} documents")
        
        # Test retrieving documents - Chat query
        print("\n📚 Testing retrieval for Chat query...")
        chat_query = "How do I implement group chat in Flutter?"
        print(f"Query: {chat_query}")
        
        chat_embedding = await embedding_generator.generate_query_embedding(chat_query)
        chat_results = await vector_store.search(
            query_embedding=chat_embedding, 
            n_results=3,
            filter_dict={"product_area": "chat"}
        )
        
        if chat_results:
            print(f"Retrieved {len(chat_results)} documents")
            for i, doc in enumerate(chat_results):
                print(f"\n[Document {i+1}] Score: {doc['relevance_score']:.2f}/10")
                print(f"Source: {doc['metadata'].get('source', 'Unknown')}")
                print(f"Platform: {doc['metadata'].get('platform', 'Unknown')}")
                print(f"Content preview: {doc['content'][:150]}...")
        else:
            print("❌ No chat documents retrieved")
            
        # Test retrieving documents - Feed query
        print("\n📱 Testing retrieval for Feed query...")
        feed_query = "How do I create a social feed with LikeMinds?"
        print(f"Query: {feed_query}")
        
        feed_embedding = await embedding_generator.generate_query_embedding(feed_query)
        feed_results = await vector_store.search(
            query_embedding=feed_embedding, 
            n_results=3,
            filter_dict={"product_area": "feed"}
        )
        
        if feed_results:
            print(f"Retrieved {len(feed_results)} documents")
            for i, doc in enumerate(feed_results):
                print(f"\n[Document {i+1}] Score: {doc['relevance_score']:.2f}/10")
                print(f"Source: {doc['metadata'].get('source', 'Unknown')}")
                print(f"Platform: {doc['metadata'].get('platform', 'Unknown')}")
                print(f"Content preview: {doc['content'][:150]}...")
        else:
            print("❌ No feed documents retrieved")
            
        return True
    except Exception as e:
        print(f"❌ Error testing vector store: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_queries():
    """Test the full RAG pipeline with different queries"""
    print("\n🧪 Testing RAG pipeline with real queries...")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Define test queries for both Chat and Feed
    test_queries = [
        {
            "product": "Chat", 
            "query": "How do I integrate LikeMinds chat SDK in my Flutter app?"
        },
        {
            "product": "Chat", 
            "query": "How can I implement message reactions in group chats?"
        },
        {
            "product": "Feed", 
            "query": "How do I create a social feed with posts in my app?"
        },
        {
            "product": "Feed", 
            "query": "What are the different components in the LikeMinds feed module?"
        }
    ]
    
    results = []
    
    # Test each query
    for i, test in enumerate(test_queries):
        print(f"\n[{i+1}/{len(test_queries)}] Testing {test['product']} query:")
        print(f"Query: {test['query']}")
        
        try:
            # Process query
            start_time = __import__('time').time()
            response = await orchestrator.process_query(test['query'])
            duration = __import__('time').time() - start_time
            
            # Track success
            results.append({
                "product": test["product"],
                "query": test["query"],
                "success": True,
                "duration": duration,
                "sources_count": len(response["sources"])
            })
            
            # Print summary
            print(f"✅ Response generated in {duration:.2f}s")
            print(f"Sources: {len(response['sources'])}")
            
            # Print response preview
            response_preview = response["response"][:150] + "..." if len(response["response"]) > 150 else response["response"]
            print(f"Response preview: {response_preview}")
            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            results.append({
                "product": test["product"],
                "query": test["query"],
                "success": False,
                "error": str(e)
            })
    
    # Print results summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n📊 Results: {successful}/{len(test_queries)} queries successful")
    
    if successful > 0:
        avg_duration = sum(r["duration"] for r in results if r["success"]) / successful
        print(f"Average response time: {avg_duration:.2f}s")
    
    return results

async def run_custom_query(query: str):
    """Run a custom query through the RAG system"""
    print(f"\n🔎 Running custom query: {query}")
    
    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        
        # Process query
        start_time = __import__('time').time()
        result = await orchestrator.process_query(query)
        duration = __import__('time').time() - start_time
        
        # Print results
        print(f"\n--- RESPONSE (generated in {duration:.2f}s) ---")
        print(result["response"])
        
        print("\n--- SOURCES ---")
        for i, source in enumerate(result["sources"]):
            print(f"[{i+1}] {source}")
        
        print("\n--- METRICS ---")
        for key, value in result["metrics"].items():
            print(f"{key}: {value}")
            
        return True
    except Exception as e:
        print(f"❌ Error processing custom query: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run tests or process a custom query"""
    print("🚀 LikeMinds RAG System Test")
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-vector-store":
            await test_vector_store()
        elif sys.argv[1] == "--test-queries":
            await test_queries()
        elif sys.argv[1] == "--query" and len(sys.argv) > 2:
            # Join all remaining arguments as the query
            query = " ".join(sys.argv[2:])
            await run_custom_query(query)
        else:
            print("Invalid arguments.")
            print("Usage:")
            print("  python test_rag.py --test-vector-store   # Test vector store retrieval")
            print("  python test_rag.py --test-queries        # Test predefined queries")
            print("  python test_rag.py --query \"Your question here\"  # Run a custom query")
    else:
        # If no arguments, run all tests
        print("Running all tests...")
        vector_store_ok = await test_vector_store()
        
        if vector_store_ok:
            await test_queries()
            
            # Ask if user wants to run a custom query
            print("\nWould you like to run a custom query? (y/n)")
            response = input().strip().lower()
            
            if response == 'y':
                print("Enter your query:")
                query = input().strip()
                if query:
                    await run_custom_query(query)

if __name__ == "__main__":
    asyncio.run(main())