"""
Documentation Agent Orchestrator.

This agent orchestrates the documentation agent workflow.
"""

import logging
import uuid
import time
from typing import Dict, Any, List, Optional

from langgraph.graph import StateGraph
from langgraph.graph import END

from .models import DocumentationRequest, DocumentationResponse, DocumentContext
from .query_understanding import QueryUnderstandingAgent
from .context_retrieval import ContextRetrievalAgent
from .solution_architect import SolutionArchitectAgent
from ..core import trace, monitor

logger = logging.getLogger(__name__)

class DocumentationAgentOrchestrator:
    """
    Orchestrator that manages the documentation agent workflow.
    """
    
    def __init__(self):
        """
        Initialize the Documentation Agent Orchestrator with all required agents.
        """
        self.query_understanding_agent = QueryUnderstandingAgent()
        self.context_retrieval_agent = ContextRetrievalAgent()
        self.solution_architect_agent = SolutionArchitectAgent()
    
    @trace("documentation_agent_orchestrator.process")
    async def process(
        self,
        request: DocumentationRequest
    ) -> Dict[str, Any]:
        """
        Process a documentation request through the agent workflow.
        
        Args:
            request: The documentation request to process
            
        Returns:
            A dictionary containing the solution and metadata
        """
        try:
            start_time = time.time()
            
            # Step 1: Analyze the query
            logger.info("Analyzing query")
            query_analysis = await self.query_understanding_agent.analyze(
                query=request.query,
                conversation_history=request.conversation_history,
                project_context={"project_id": request.project_id, "platform": request.platform}
            )
            
            # Step 2: Retrieve relevant context
            logger.info("Retrieving context")
            context_documents = await self.context_retrieval_agent.search(
                query=request.query,
                analyzed_query=query_analysis,
                project_id=request.project_id,
                platform=request.platform
            )
            
            # Step 3: Create the solution document
            logger.info("Creating solution")
            solution_result = await self.solution_architect_agent.create_solution(
                query=request.query,
                query_analysis=query_analysis,
                context_documents=context_documents
            )
            
            # Convert context documents to DocumentContext objects
            context_list = []
            for doc in context_documents:
                context_list.append(DocumentContext(
                    content=doc["content"],
                    source=doc["source"],
                    relevance_score=doc["relevance_score"],
                    metadata=doc.get("metadata", {})
                ))
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Return the final result
            return {
                "solution_document": solution_result["solution_document"],
                "relevant_context": context_list,
                "next_steps": solution_result.get("next_steps", []),
                "request_id": str(uuid.uuid4()),
                "processing_time": processing_time,
                "metadata": {
                    "query_analysis": query_analysis,
                    "solution_metadata": solution_result.get("metadata", {})
                }
            }
                
        except Exception as e:
            logger.error(f"Error in documentation agent orchestrator: {str(e)}", exc_info=True)
            return {
                "solution_document": f"Error processing documentation request: {str(e)}",
                "relevant_context": [],
                "next_steps": ["Contact support for assistance with this issue."],
                "request_id": str(uuid.uuid4()),
                "processing_time": time.time() - start_time,
                "metadata": {
                    "error": str(e)
                }
            }
    
    def build_workflow_graph(self) -> StateGraph:
        """
        Build a LangGraph workflow for the documentation agent process.
        
        Returns:
            A LangGraph StateGraph representing the workflow
        """
        # Create workflow graph
        workflow = StateGraph(name="documentation_workflow")
        
        # Add nodes for each step in the process
        workflow.add_node("query_understanding", self.query_understanding_agent.analyze)
        workflow.add_node("context_retrieval", self.context_retrieval_agent.search)
        workflow.add_node("solution_creation", self.solution_architect_agent.create_solution)
        
        # Connect the nodes
        workflow.add_edge("query_understanding", "context_retrieval")
        workflow.add_edge("context_retrieval", "solution_creation")
        workflow.add_edge("solution_creation", END)
        
        # Set the entry point
        workflow.set_entry_point("query_understanding")
        
        return workflow

# Create a singleton instance for use in FastAPI router
orchestrator = DocumentationAgentOrchestrator()

async def process_documentation(
    request: DocumentationRequest,
    user: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process a documentation request.
    
    Args:
        request: The documentation request to process
        user: Optional user information
        
    Returns:
        A dictionary containing the solution and metadata
    """
    # Add user information to the request if provided
    if user and not request.user_id:
        request.user_id = user.get("id")
    
    # Process the request with the orchestrator
    return await orchestrator.process(request) 