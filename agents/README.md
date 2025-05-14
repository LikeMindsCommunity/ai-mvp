# LikeMinds Flutter Integration Assistant (Agno Agents)

This directory contains the implementation of a RAG-based agentic flow for the "LikeMinds Flutter Integration Assistant" using the Agno framework with Google's Gemini models.

## Overview

The implementation follows a modular architecture with multiple specialized agents coordinated by an orchestrator. All agents use Gemini models by default:

1. **QueryPlannerAgent** - Analyzes user intent and plans the approach
2. **InformationRetrievalAgent** - Retrieves relevant documentation using a vector database
3. **ProjectContextAgent** - Gathers information about the Flutter project
4. **CodeGenAgent** - Generates Flutter code based on requirements and documentation
5. **Orchestrator** - Coordinates the agents and manages the flow of information

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ANTHROPIC_API_KEY=your_claude_api_key  # Optional, only if you want to use Claude
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   GITHUB_TOKEN=your_github_token
   VECTOR_DB_PATH=./vector_db
   PROJECT_TEMP_DIR=./tmp
   ```

3. Create the necessary directories:
   ```bash
   mkdir -p vector_db tmp output
   ```

## Usage

### Basic Example

```python
from agents.orchestrator import Orchestrator

# Initialize the orchestrator (uses Gemini by default)
orchestrator = Orchestrator()

# Set the current project (if applicable)
orchestrator.set_project("your_project_id")

# Process a query
response = orchestrator.process_query(
    "How do I implement a chat feature using the LikeMinds SDK?"
)

# Access the generated code and other information
code_files = response["code_files"]
retrieved_docs = response["retrieved_docs"]
plan = response["plan"]
```

### Run the Example Script

```bash
python -m agents.example
```

## Implementation Details

### Model Configuration

The system uses Google's Gemini models by default. The specific model used is configured in `config.py`:

```python
DEFAULT_MODEL = "gemini-2.5-flash-preview-04-17"
```

While the system is designed to work with Gemini, it also supports Claude models by setting the `use_claude` parameter to `True` in the agent initialization.

### Vector Database

The system uses ChromaDB as the default vector database for storing and retrieving document embeddings. The database is initialized in the `InformationRetrievalAgent` when needed.

### Code Generation

The `CodeGenAgent` generates Flutter code based on the user's requirements and retrieved documentation. It uses a prompt template that includes:

- User requirements
- Project context (if available)
- Retrieved documentation
- Existing code (if applicable)

### Project Context

The `ProjectContextAgent` extracts information from Flutter projects, including:

- Basic project metadata
- Dependencies from `pubspec.yaml`
- Project structure
- LikeMinds SDK integration details

## Future Improvements

- Implement vector database population tools
- Add code analysis and validation using Flutter tools
- Create a FastAPI interface for WebSocket communication
- Implement a task queue for long-running operations
- Add debugging and refinement capabilities 