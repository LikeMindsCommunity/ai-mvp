"""
Orchestrator for coordinating the different agents in the system.
"""

from typing import List, Dict, Any, Optional
import json
import os
import time

from agents.query_planner import QueryPlannerAgent
from agents.retrieval_agent import InformationRetrievalAgent
from agents.project_context import ProjectContextAgent
from agents.code_gen import CodeGenAgent


class Orchestrator:
    """
    Orchestrator for coordinating the different agents in the system.
    
    This class manages the flow of information between agents and handles
    the overall process of responding to user queries about Flutter integration.
    """
    
    def __init__(self):
        """Initialize the orchestrator with the necessary agents."""
        # Initialize the agents
        self.query_planner = QueryPlannerAgent(use_claude=False)
        self.retrieval_agent = InformationRetrievalAgent(use_claude=False)
        self.project_context_agent = ProjectContextAgent(use_claude=False)
        self.code_gen_agent = CodeGenAgent(use_claude=False)
        
        # State for tracking the current interaction
        self.current_project_id = None
        self.conversation_history = []
    
    def set_project(self, project_id: str) -> Dict[str, Any]:
        """
        Set the current project for the orchestrator.
        
        Args:
            project_id: The ID of the project to set
            
        Returns:
            Project context information
        """
        self.current_project_id = project_id
        return self.project_context_agent.get_project_context(project_id)
    
    def process_query(
        self, 
        query: str, 
        project_id: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user query through the agent system.
        
        Args:
            query: The user's query about Flutter integration
            project_id: Optional project ID (if not already set)
            conversation_history: Optional conversation history
            
        Returns:
            A dictionary containing the response and any generated code
        """
        # Set the project if provided
        if project_id:
            self.current_project_id = project_id
            
        # Use provided conversation history or the stored one
        if conversation_history:
            self.conversation_history = conversation_history
            
        # Record start time for tracking performance
        start_time = time.time()
        steps_timing = {}
        
        # Step 1: Plan the query using the QueryPlannerAgent
        step_start = time.time()
        plan = self.query_planner.plan_query(query, self.conversation_history)
        steps_timing["query_planning"] = time.time() - step_start
        
        # Step 2: Get project context if available
        project_context = None
        if self.current_project_id:
            step_start = time.time()
            project_context = self.project_context_agent.get_project_context(self.current_project_id)
            steps_timing["project_context"] = time.time() - step_start
        
        # Step 3: Retrieve relevant information using the InformationRetrievalAgent
        step_start = time.time()
        retrieval_query = " ".join(plan.get("keywords", []))
        if not retrieval_query:
            retrieval_query = query
            
        retrieved_docs = self.retrieval_agent.retrieve_and_format(
            query=retrieval_query,
            num_results=7  # Adjust based on needs
        )
        steps_timing["information_retrieval"] = time.time() - step_start
        
        # Step 4: Generate code if needed
        code_files = {}
        if "code_examples" in plan.get("required_information", []) or "code" in query.lower():
            step_start = time.time()
            
            # Format project context as string if available
            project_context_str = None
            if project_context:
                project_context_str = json.dumps(project_context, indent=2)
            
            code_files = self.code_gen_agent.generate_code(
                requirements=query,
                retrieved_docs=retrieved_docs,
                project_context=project_context_str
            )
            steps_timing["code_generation"] = time.time() - step_start
        
        # Step 5: Generate the final response
        step_start = time.time()
        
        # Build response based on results
        response = {
            "query": query,
            "plan": plan,
            "project_context": project_context,
            "retrieved_docs": retrieved_docs,
            "code_files": code_files,
            "timing": {
                "total": time.time() - start_time,
                "steps": steps_timing
            }
        }
        
        # Update conversation history
        self.conversation_history.append({
            "user": query,
            "assistant": "Response generated successfully"  # This would typically be the text response
        })
        
        return response 