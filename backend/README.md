# LikeMinds Integration Agent - Backend

This directory contains the backend implementation for the LikeMinds Integration Agent, a microservices-based architecture designed to provide code generation, documentation analysis, and SDK integration capabilities.

## Directory Structure

```
backend/
├── agents/                   # Agent services for intelligent processing
│   ├── documentation/        # Documentation understanding agents
│   ├── coding/               # Code generation agents  
│   └── core/                 # Core agent infrastructure
├── processors/               # Data transformation services
│   ├── docs/                 # Document processing services
│   └── code/                 # Code processing services
├── vector/                   # Vector database services
│   ├── docs/                 # Document vector services
│   └── code/                 # Code vector services
├── project/                  # Project management services
│   ├── demo/                 # Demo repository services
│   ├── environment/          # Environment management services
│   ├── deployment/           # Deployment services
│   ├── output/               # Code output services
│   └── analysis/             # Code analysis services
├── infrastructure/           # Shared infrastructure services
│   ├── observability/        # Monitoring and tracing services
│   ├── messaging/            # Messaging services
│   └── auth/                 # Authentication services
└── requirements.txt          # Project dependencies
```

## Technology Stack

- FastAPI for API implementation
- LangChain/LangGraph for agent orchestration
- ChromaDB for vector storage
- PostgreSQL for operational data
- MongoDB for document storage
- Redis for caching
- RabbitMQ for messaging
- Kubernetes for deployment

## Development Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start local services: `docker-compose up -d`
3. Run the development server: `python -m backend.main`

## Testing

Run tests with: `pytest`

## Deployment

The backend is designed to be deployed on Kubernetes. See the deployment documentation for details. 