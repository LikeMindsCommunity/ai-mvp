"""
Orchestrator service for the Documentation Agent.
This manages the workflow of processing documentation requests.
"""

import logging
import time
import uuid
from typing import Dict, Any, List

from langchain.chat_models import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph
import langgraph.graph as lg

from ..models import DocumentationRequest, DocumentContext
from ..query_understanding.service import process_query
from ..context_retrieval.service import retrieve_context
from ..solution_architect.service import create_solution
from ....infrastructure.config import settings
from ....infrastructure.observability import trace, monitor

# Configure logging
logger = logging.getLogger(__name__)

@trace("documentation_agent.process")
async def process_documentation(
    request: DocumentationRequest,
    user: Any
) -> Dict[str, Any]:
    """
    Process a documentation request through the agent workflow.
    
    Args:
        request: The documentation request
        user: The authenticated user
        
    Returns:
        Dictionary containing the solution and context
    """
    logger.info(f"Processing documentation request: {request.query}")
    
    try:
        # Initialize request tracking
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Initialize the LLM with monitoring
        llm = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            temperature=0,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            callbacks=[monitor.get_helicone_callback()]
        )
        
        # Create memory if there's conversation history
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        if request.conversation_history:
            for message in request.conversation_history:
                memory.chat_memory.add_user_message(message.user)
                memory.chat_memory.add_ai_message(message.assistant)
        
        # Create the workflow graph
        workflow = create_documentation_workflow(llm)
        
        # Execute the workflow
        result = await workflow.ainvoke({
            "query": request.query,
            "user_id": user.id if user else None,
            "project_id": request.project_id,
            "platform": request.platform,
            "memory": memory,
            "request_id": request_id
        })
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare the result
        return {
            "solution_document": result["solution_document"],
            "relevant_context": result["relevant_context"],
            "next_steps": result.get("next_steps"),
            "request_id": request_id,
            "processing_time": processing_time
        }
    
    except Exception as e:
        logger.error(f"Error in documentation agent: {str(e)}", exc_info=True)
        monitor.record_exception(e)
        raise

def create_documentation_workflow(llm: Any) -> StateGraph:
    """
    Create the documentation agent workflow graph using LangGraph.
    
    Args:
        llm: The language model to use
        
    Returns:
        A LangGraph state graph
    """
    # Define the workflow states
    workflow = StateGraph(agents=[
        "query_understanding",
        "context_retrieval",
        "solution_architect"
    ])
    
    # Define the initial state
    workflow.add_node("query_understanding", process_query)
    workflow.add_node("context_retrieval", retrieve_context)
    workflow.add_node("solution_architect", create_solution)
    
    # Define the edges (workflow)
    workflow.add_edge("query_understanding", "context_retrieval")
    workflow.add_edge("context_retrieval", "solution_architect")
    
    # Set the entry point
    workflow.set_entry_point("query_understanding")
    
    # Compile the graph
    return workflow.compile() 