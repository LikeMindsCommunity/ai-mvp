"""
Script to set up a basic vector database for testing.
"""

import os
import chromadb
from agents.config import VECTOR_DB_PATH

# Sample Flutter and LikeMinds documentation
SAMPLE_DOCS = [
    {
        "id": "flutter_intro_1",
        "text": "Flutter is Google's UI toolkit for building beautiful, natively compiled applications for mobile, web, and desktop from a single codebase. Flutter works with existing code, is used by developers and organizations around the world, and is free and open source.",
        "metadata": {"source": "flutter.dev", "type": "introduction"}
    },
    {
        "id": "flutter_widgets_1",
        "text": "Flutter widgets are built using a modern framework that takes inspiration from React. The central idea is that you build your UI out of widgets. Widgets describe what their view should look like given their current configuration and state.",
        "metadata": {"source": "flutter.dev", "type": "widgets"}
    },
    {
        "id": "likeminds_intro_1",
        "text": "LikeMinds is a community and chat SDK for Flutter that enables developers to add social features to their applications. It provides real-time messaging, user profiles, feeds, and engagement features.",
        "metadata": {"source": "likeminds.io", "type": "introduction"}
    },
    {
        "id": "likeminds_chat_1",
        "text": "The LikeMinds Chat SDK provides a complete solution for implementing real-time chat in your Flutter application. It includes features like message delivery status, typing indicators, file sharing, and push notifications.",
        "metadata": {"source": "likeminds.io", "type": "chat"}
    },
    {
        "id": "likeminds_installation_1",
        "text": "To install the LikeMinds SDK, add the dependency to your pubspec.yaml file: likeminds_flutter_sdk: ^latest_version. Then run 'flutter pub get' to install the package.",
        "metadata": {"source": "likeminds.io", "type": "installation"}
    },
    {
        "id": "likeminds_initialization_1",
        "text": "Initialize the LikeMinds SDK in your application by calling LMChat.instance.initialize(apiKey). This should be done before using any other SDK features, typically in your app's initialization phase.",
        "metadata": {"source": "likeminds.io", "type": "initialization"}
    },
    {
        "id": "likeminds_chat_implementation_1",
        "text": "To implement a chat feature, first create a chat room using LMChat.instance.createChatRoom(). Then use LMChat.instance.getChatMessages() to retrieve messages and LMChat.instance.sendMessage() to send new messages.",
        "metadata": {"source": "likeminds.io", "type": "implementation"}
    }
]


def setup_test_vector_db():
    """Set up a test vector database with sample Flutter and LikeMinds documentation."""
    # Create the vector database directory if it doesn't exist
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    
    # Initialize the ChromaDB client
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    
    # Create or get the collection
    try:
        collection = client.get_collection(name="flutter_docs")
        print("Collection already exists, updating...")
        # Delete existing documents to re-add them
        collection.delete(where={})
    except Exception as e:
        print(f"Collection does not exist, creating new one: {e}")
        collection = client.create_collection(name="flutter_docs")
        print("Created new collection: flutter_docs")
    
    # Extract the data
    ids = [doc["id"] for doc in SAMPLE_DOCS]
    texts = [doc["text"] for doc in SAMPLE_DOCS]
    metadatas = [doc["metadata"] for doc in SAMPLE_DOCS]
    
    # Add the documents to the collection
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    
    print(f"Added {len(SAMPLE_DOCS)} documents to the vector database")
    return collection


if __name__ == "__main__":
    # Set up the test vector database
    collection = setup_test_vector_db()
    
    # Test a query
    results = collection.query(
        query_texts=["How do I implement chat in LikeMinds?"],
        n_results=2
    )
    
    print("\nTest query results:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"\nDocument {i+1}:")
        print(f"Content: {doc}")
        print(f"ID: {results['ids'][0][i]}")
        print(f"Distance: {results['distances'][0][i]}")
        metadata = results["metadatas"][0][i]
        print(f"Source: {metadata['source']}, Type: {metadata['type']}") 