"""
Example script to demonstrate how to use the agent orchestrator.
"""

import os
import json
from dotenv import load_dotenv

from agents.orchestrator import Orchestrator
from agents.simple_agent import SimpleAgent


def test_simple_agent():
    """Test the simple agent to ensure basic functionality works."""
    print("\n=== Testing Simple Agent with Gemini ===\n")
    
    agent = SimpleAgent(use_claude=False)  # Explicitly use Gemini
    response = agent.print_response(
        "What is Flutter and how does it relate to mobile app development?",
        stream=True,
        show_reasoning=True
    )
    
    print(f"Response from Simple Agent:\n{response}\n")


def test_orchestrator():
    """Test the full orchestrator with a Flutter integration query."""
    print("\n=== Testing Orchestrator with Gemini models ===\n")
    
    orchestrator = Orchestrator()
    query = "How do I implement a chat feature using the LikeMinds SDK in Flutter?"
    
    print(f"Processing query: {query}\n")
    response = orchestrator.process_query(query)
    
    print("Response structure:\n")
    print(f"query: {type(query)}")
    print(f"plan: {type(response['plan'])}")
    print(f"project_context: {type(response['project_context'])}")
    print(f"retrieved_docs: {len(response['retrieved_docs'])} documents")
    print(f"code_files: {len(response['code_files'])} files generated")
    
    for filename in response['code_files']:
        print(f"  - {filename}")
    
    print(f"timing: Total {response['timing']['total']:.2f}s")
    print(f"  - query_planning: {response['timing']['query_planning']:.2f}s")
    print(f"  - information_retrieval: {response['timing']['information_retrieval']:.2f}s")
    print(f"  - code_generation: {response['timing']['code_generation']:.2f}s")
    
    # Save the generated code to files
    os.makedirs("output", exist_ok=True)
    for filename, code in response['code_files'].items():
        output_path = os.path.join("output", filename)
        with open(output_path, "w") as f:
            f.write(code)
        print(f"\nSaved example file to {output_path}")


if __name__ == "__main__":
    # Make sure to load environment variables
    load_dotenv()
    
    # Test the simple agent first
    test_simple_agent()
    
    # Then test the orchestrator
    test_orchestrator() 