"""
Hello World example with Agno and Gemini API.

This is a simple example of using Agno to create an agent that uses Google's Gemini API.
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini

from agent_system.config import agno_config, setup_agno_environment

def run_hello_world():
    """
    Create and run a simple Agno agent using Google's Gemini API.
    """
    # Setup environment for Agno
    setup_agno_environment()
    
    # Create an agent with Google's Gemini model
    print("Creating agent...")
    agent = Agent(
        model=Gemini(id=agno_config.default_model_id),
        description="You are a helpful assistant specialized in Flutter and Dart development.",
        instructions=[
            "Provide concise and accurate answers about Flutter and Dart.",
            "Include code examples when appropriate.",
        ],
        markdown=True,
    )
    
    # Get a response from the agent
    print("Getting response from agent...")
    query = "What is Flutter and how does it differ from other mobile app frameworks?"
    print(f"Query: {query}")
    response = agent.run(query)
    print(f"Response: {response}")
    
    # Print the response
    print("\n==== Hello World Agent Response ====\n")
    print(response)
    print("\n==== End of Response ====\n")
    
    return response

if __name__ == "__main__":
    run_hello_world() 