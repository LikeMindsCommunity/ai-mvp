# LikeMinds RAG Documentation Assistant

This repository contains scripts to create a retrieval-augmented generation (RAG) system for the LikeMinds documentation using LangChain and LangGraph with Google's Gemini model.

## Setup

1. Install the required dependencies:

```bash
pip install langchain langchain-google-genai langchain_community langchain_core faiss-cpu python-dotenv langgraph
```

If you want to use `UnstructuredMarkdownLoader` instead of the simpler `TextLoader`, you'll need to install additional dependencies:

```bash
pip install unstructured
```

2. Create a `.env` file in the root directory with your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

3. Make sure you have a `prompt.txt` file containing your system instructions for the assistant.

4. Ensure your documentation markdown files are in the `docs/chat` directory.

5. For source code integration, place or clone the LikeMinds Flutter SDK in the `likeminds-chat-flutter` directory, or update the `SDK_SOURCE_PATH` variable in the script to point to your SDK location.

## Scripts

### 1. `langchain.py`

This script implements a basic RAG system using LangChain components. It:

- Creates or loads a FAISS vector database from markdown documentation
- Processes user queries using a conversational retrieval chain 
- Maintains conversation history for context using ConversationBufferMemory
- Extracts and saves Flutter/Dart code from responses

Run the script:

```bash
python langchain.py
```

### 2. `langgraph_memory.py`

This script implements a modern RAG workflow using LangGraph with built-in memory. It:

- Uses a state-based approach with TypedDict for structured workflow
- Maintains conversation history as a list of message objects in the graph state
- Processes documents and generates responses in separate graph nodes
- Preserves chat context between questions for coherent follow-up responses
- Indexes both documentation and SDK source code for more accurate answers
- Differentiates between documentation and source code snippets in context

This implementation follows LangChain's recommended approach for memory management in v0.3+ as described in their [migration guide](https://python.langchain.com/docs/versions/migrating_memory/).

Run the script:

```bash
python langgraph_memory.py
```

### 3. `langgraph_assistant.py` (Deprecated)

This script implements a multi-step workflow using LangGraph with conditional branching. It has been deprecated in favor of the more modern memory-based approach in `langgraph_memory.py`.

## Memory Management

The repository showcases two approaches to memory management:

1. **Traditional approach (langchain.py)**: Uses `ConversationBufferMemory` to store chat history
2. **Modern approach (langgraph_memory.py)**: Uses LangGraph's state management to:
   - Store message history directly in the graph state
   - Maintain context between runs
   - Provide a more maintainable and extensible architecture

The modern approach is recommended for new projects as it provides more flexibility and aligns with LangChain's development roadmap.

## Vector Store Configuration

The `langgraph_memory.py` script creates a vector store from two sources:

1. **Documentation Files**: Markdown files from the `docs/chat` directory
2. **Source Code Files**: Dart files from the LikeMinds Flutter SDK

The vector store is configured to:
- Use smaller chunk sizes for code (1000 characters vs 1500 for documentation)
- Provide source information with each chunk for better context
- Handle both code and documentation appropriately

## Troubleshooting

If you encounter errors related to missing packages, ensure you've installed all dependencies:

- **ModuleNotFoundError: No module named 'unstructured'**: Install it with `pip install unstructured`
- **ImportError issues with langchain packages**: Make sure you have the latest versions with `pip install -U langchain langchain-google-genai langchain_community langchain_core`
- **SDK source path not found**: The script will warn you if the SDK path doesn't exist but will still work with documentation only

## Key Features

- **Efficient Retrieval**: Uses semantic search to find relevant documentation and code
- **Conversation Memory**: Maintains chat history for contextual responses
- **Vector Database**: Stores embeddings of documentation and source code for fast retrieval
- **Code Extraction**: Automatically extracts Flutter/Dart code examples
- **Modern Architecture**: LangGraph version uses a state-based workflow for better memory management
- **Source Context**: Clearly identifies whether context comes from documentation or source code

## Customization

- Edit the `prompt.txt` file to customize the system instructions
- Modify the chunking parameters in each script to adjust how documentation and code are split
- Add more nodes to the LangGraph workflow for additional processing steps
- Update the `SDK_SOURCE_PATH` variable to point to your SDK location

## Output

The scripts save extracted Flutter/Dart code to the `output` directory with filenames like `flutter_code_1.dart`, `flutter_code_2.dart`, etc.

## Extending the System

- Add more document loaders to support different file formats
- Implement more sophisticated code validation
- Add a web interface for interactive querying
- Integrate with GitHub or other version control for code revision history
- Add advanced memory techniques like conversation summarization or entity extraction
