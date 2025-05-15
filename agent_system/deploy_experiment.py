"""
Experiment with Agno's deployment features.

This module explores Agno's capability to run and potentially deploy tasks.
"""

import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools

from agent_system.config import agno_config, setup_agno_environment

# Setup environment for Agno
setup_agno_environment()

class DeploymentExperiment:
    """
    Class to experiment with Agno's deployment features.
    """
    
    def __init__(self):
        """Initialize the deployment experiment."""
        self.agent = Agent(
            model=Gemini(id=agno_config.default_model_id),
            description="You are a Flutter integration expert assistant.",
            instructions=[
                "Think step by step when analyzing Flutter integration questions.",
                "Provide concise, accurate answers with code examples when appropriate.",
            ],
            tools=[ReasoningTools(add_instructions=True)],
            markdown=True,
        )
    
    def analyze_flutter_integration(self, query: str) -> str:
        """
        Analyze a Flutter integration question using a reasoning agent.
        
        Args:
            query: The integration question to analyze
            
        Returns:
            The agent's response
        """
        print(f"Analyzing Flutter integration question: {query}")
        response = self.agent.run(
            query,
            show_full_reasoning=True,
        )
        return response
    
    async def analyze_flutter_integration_async(self, query: str) -> str:
        """
        Asynchronously analyze a Flutter integration question.
        
        Args:
            query: The integration question to analyze
            
        Returns:
            The agent's response
        """
        print(f"Asynchronously analyzing Flutter integration question: {query}")
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.agent.run(
                query,
                show_full_reasoning=True,
            )
        )
        return response

def run_experiment():
    """Run the deployment experiment."""
    experiment = DeploymentExperiment()
    
    # Test synchronous execution
    response = experiment.analyze_flutter_integration(
        "How would I integrate LikeMinds chat SDK into a Flutter application with a custom theme?"
    )
    print("\n==== Agent Response (Sync) ====\n")
    print(response)
    print("\n==== End of Response ====\n")
    
    # Test asynchronous execution
    async def run_async_test():
        response = await experiment.analyze_flutter_integration_async(
            "What are the best practices for handling errors in a LikeMinds chat integration?"
        )
        print("\n==== Agent Response (Async) ====\n")
        print(response)
        print("\n==== End of Response ====\n")
    
    asyncio.run(run_async_test())
    
if __name__ == "__main__":
    run_experiment() 