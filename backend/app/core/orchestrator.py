import os
import uuid
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

from .agents.query_understanding_agent import QueryUnderstandingAgent
from .agents.context_retrieval_agent import ContextRetrievalAgent
from .agents.response_generation_agent import ResponseGenerationAgent
from .agents.code_requirements_analysis_agent import CodeRequirementsAnalysisAgent
from .agents.code_planning_agent import CodePlanningAgent
from .agents.code_generation_agent import CodeGenerationAgent
from .agents.code_validation_agent import CodeValidationAgent
from .agents.agent_registry import AgentRegistry
from .document_processor.embedding_generator import EmbeddingGenerator
from .vector_store.chroma_store import ChromaStore

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrates the RAG workflow by coordinating the different agents:
    1. Query Understanding Agent: Analyzes and enhances the user query
    2. Context Retrieval Agent: Retrieves relevant document chunks 
    3. Response Generation Agent: Generates the final response
    
    Also orchestrates the Code Generation workflow:
    1. Code Requirements Analysis Agent: Analyzes user requirements and extracts structured information
    2. Code Planning Agent: Creates architecture and implementation plans based on requirements
    3. Code Generation Agent: Generates code based on plans and requirements
    4. Code Validation Agent: Validates generated code for quality, security, and best practices
    """
    
    def __init__(self):
        """Initialize the orchestrator with all required agents."""
        # Initialize the agent registry
        self.agent_registry = AgentRegistry()
        
        # Register and initialize RAG agents
        self.query_agent = self.agent_registry.create_agent(QueryUnderstandingAgent, name="query_understanding_agent")
        self.retrieval_agent = self.agent_registry.create_agent(ContextRetrievalAgent, name="context_retrieval_agent")
        self.response_agent = self.agent_registry.create_agent(ResponseGenerationAgent, name="response_generation_agent")
        
        # Register and initialize Code Generation agents
        self.requirements_agent = self.agent_registry.create_agent(CodeRequirementsAnalysisAgent, name="code_requirements_analysis_agent")
        self.planning_agent = self.agent_registry.create_agent(CodePlanningAgent, name="code_planning_agent")
        self.generation_agent = self.agent_registry.create_agent(CodeGenerationAgent, name="code_generation_agent")
        self.validation_agent = self.agent_registry.create_agent(CodeValidationAgent, name="code_validation_agent")
        
        # Initialize other components
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = ChromaStore()
        
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process a user query through the full RAG pipeline.
        
        Args:
            query: The user's query text
            conversation_history: Optional list of previous conversation turns
            
        Returns:
            Dictionary containing the response, sources, and metrics
        """
        start_time = __import__('time').time()
        conversation_history = conversation_history or []
        metrics = {}
        
        # Step 1: Query understanding - enhance the original query
        logger.info(f"Processing query: {query}")
        enhanced_query = await self.query_agent.enhance_query(query, conversation_history)
        metrics["query_enhancement_time"] = __import__('time').time() - start_time
        logger.info(f"Enhanced query: {enhanced_query}")
        
        # Step 2: Generate embedding for the enhanced query
        query_embedding_time = __import__('time').time()
        query_embedding = await self.embedding_generator.generate_query_embedding(enhanced_query)
        metrics["query_embedding_time"] = __import__('time').time() - query_embedding_time
        
        # Step 3: Retrieve relevant context
        retrieval_time = __import__('time').time()
        context_docs = await self.vector_store.search(query_embedding, n_results=5)
        metrics["retrieval_time"] = __import__('time').time() - retrieval_time
        logger.info(f"Retrieved {len(context_docs)} documents")
        
        # Step 4: Rerank and filter documents (if needed)
        reranking_time = __import__('time').time()
        ranked_docs = await self.retrieval_agent.rerank_documents(enhanced_query, context_docs)
        metrics["reranking_time"] = __import__('time').time() - reranking_time
        
        # Step 5: Generate final response
        response_time = __import__('time').time()
        response, sources = await self.response_agent.generate_response(
            query, 
            enhanced_query, 
            ranked_docs, 
            conversation_history
        )
        metrics["response_generation_time"] = __import__('time').time() - response_time
        
        # Calculate total processing time
        metrics["total_time"] = __import__('time').time() - start_time
        
        # Return formatted response
        return {
            "query": query,
            "enhanced_query": enhanced_query,
            "response": response,
            "sources": sources,
            "metrics": metrics
        }
        
    async def process_code_generation(self, requirements: str, platform: str, additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a code generation request through the full pipeline.
        
        Args:
            requirements: The user's requirements in natural language
            platform: Target platform (e.g., "React Native", "iOS", "Android")
            additional_context: Optional additional context like preferences, constraints, etc.
            
        Returns:
            Dictionary containing the generated code, validation results, and metrics
        """
        start_time = __import__('time').time()
        metrics = {}
        additional_context = additional_context or {}
        
        # Step 1: Analyze requirements
        logger.info(f"Analyzing requirements for {platform} platform")
        requirements_time = __import__('time').time()
        requirements_analysis = await self.requirements_agent.execute({
            "action": "analyze_requirements",
            "requirements": requirements,
            "platform": platform,
            "additional_context": additional_context
        })
        metrics["requirements_analysis_time"] = __import__('time').time() - requirements_time
        logger.info(f"Requirements analysis completed")
        
        # Step 2: Create code plan
        planning_time = __import__('time').time()
        code_plan = await self.planning_agent.execute({
            "action": "create_plan",
            "requirements_analysis": requirements_analysis,
            "platform": platform,
            "additional_context": additional_context
        })
        metrics["planning_time"] = __import__('time').time() - planning_time
        logger.info(f"Code planning completed")
        
        # Step 3: Generate code
        generation_time = __import__('time').time()
        generated_code = await self.generation_agent.execute({
            "action": "generate_code",
            "requirements_analysis": requirements_analysis,
            "code_plan": code_plan,
            "platform": platform,
            "additional_context": additional_context
        })
        metrics["generation_time"] = __import__('time').time() - generation_time
        logger.info(f"Code generation completed")
        
        # Step 4: Validate code
        validation_time = __import__('time').time()
        validation_results = await self.validation_agent.execute({
            "action": "validate_code",
            "generated_code": generated_code,
            "requirements_analysis": requirements_analysis,
            "code_plan": code_plan,
            "platform": platform
        })
        metrics["validation_time"] = __import__('time').time() - validation_time
        logger.info(f"Code validation completed")
        
        # Calculate total processing time
        metrics["total_time"] = __import__('time').time() - start_time
        
        # Return formatted response
        return {
            "requirements": requirements,
            "platform": platform,
            "requirements_analysis": requirements_analysis,
            "code_plan": code_plan,
            "generated_code": generated_code,
            "validation_results": validation_results,
            "metrics": metrics
        } 