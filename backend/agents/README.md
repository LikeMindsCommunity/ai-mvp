# Agent Services

This directory contains the intelligent agent services that form the core of the LikeMinds Integration Agent.

## Components

### Documentation Agents

The documentation directory contains agents for understanding and processing documentation:

- **Query Understanding**: Analyzes user queries to understand intent
- **Context Retrieval**: Fetches relevant documentation context
- **Solution Architect**: Creates integration solutions from documentation
- **Agent Orchestrator**: Manages the documentation agent workflow

### Coding Agents

The coding directory contains agents for generating and managing code:

- **Requirement Analysis**: Structures requirements for code generation
- **Code Planning**: Creates code architecture and plans
- **Code Generation**: Produces implementation code
- **Code Validation**: Verifies code quality
- **Agent Orchestrator**: Manages the coding agent workflow

### Core Agents

The core directory contains shared agent infrastructure:

- **Base Agent**: Provides common agent functionality
- **Agent Communication**: Handles message passing between agents
- **Agent Registry**: Manages agent lifecycle

## Implementation Plan

### Week 1: Core Agent Framework
- Implement base agent class
- Create agent registry
- Set up LangChain/LangGraph integration
- Implement basic agent communication

### Week 2: Documentation Agent Basic Components
- Implement query understanding component
- Create context retrieval component
- Set up solution architect component
- Build documentation agent orchestrator

### Week 3: Coding Agent Basic Components
- Implement requirement analysis component
- Create code planning component
- Set up code generation component
- Implement code validation component
- Build coding agent orchestrator

### Week 4: Advanced Features
- Integrate with vector services
- Add memory management
- Implement agent tracing
- Create agent dashboards

## Technology Stack

- LangChain 0.1.7+ for agent components
- LangGraph 0.0.30+ for agent workflows
- FastAPI for API endpoints
- Claude-3-Sonnet model for primary reasoning
- Redis for agent memory
- OpenTelemetry for agent tracing 