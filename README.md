# LikeMinds Documentation RAG System

A Retrieval-Augmented Generation (RAG) system for the LikeMinds SDK documentation. This system provides accurate and contextual answers to user queries about LikeMinds Chat and Feed SDKs by leveraging both Claude 3.7 Sonnet and GPT-4.

## Architecture

This project uses a modern stack with:

- **Backend**: Python/FastAPI with LangChain for orchestration
- **Frontend**: React with Chakra UI
- **Vector Database**: ChromaDB
- **LLMs**: Claude 3.7 Sonnet and GPT-4o

### Core Components

1. **Document Processing Pipeline**
   - Document Analysis (Claude 3.7 Sonnet)
   - Chunking Strategy
   - Embedding Generation (OpenAI)

2. **Agent System**
   - Query Understanding Agent (Claude 3.7 Sonnet)
   - Context Retrieval Agent (GPT-4o)
   - Response Generation Agent (Claude 3.7 Sonnet)

3. **Frontend**
   - Query Interface
   - Response Display
   - Documentation Browser

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- OpenAI API key
- Anthropic API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/likeminds-rag.git
   cd likeminds-rag
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```
   
   On Windows:
   ```
   set OPENAI_API_KEY=your_openai_api_key
   set ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

4. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   python -m app.main
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`

### Processing Documentation

Before using the system, you need to process the documentation:

```bash
curl -X POST "http://localhost:8000/api/process" \
     -H "Content-Type: application/json" \
     -d '{"directory": "/path/to/likeminds-docs", "file_pattern": "**/*.md"}'
```

## Features

- **Semantic Search**: Find relevant documentation based on intent, not just keywords
- **Context-Aware Responses**: Generate answers that consider the entire context of the documentation
- **Platform-Specific Results**: Filter results by platform (Android, iOS, React, Flutter, etc.)
- **Code Examples**: Extract and present relevant code examples
- **Comprehensive Explanations**: Generate detailed explanations with references to the source documentation

## Development

### Project Structure

```
retrieval/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   │   ├── document_processor/  # Document processing
│   │   │   ├── agents/             # Agent implementations
│   │   │   └── vector_store/       # Vector store operations
│   │   ├── models/        # Data models
│   │   └── services/      # Business logic
│   ├── tests/             # Test files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   └── utils/         # Utility functions
│   └── package.json
└── docs/                  # Project documentation
```

## API Documentation

API documentation is available at `http://localhost:8000/docs` when the backend is running.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 