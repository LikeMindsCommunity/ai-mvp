"""
A simple agent for testing Agno integration.
"""

from agents.base import BaseAgent
from agno.tools.reasoning import ReasoningTools


class SimpleAgent(BaseAgent):
    """A simple agent for testing basic Agno functionality."""
    
    def __init__(self, use_claude: bool = False):
        """
        Initialize the simple agent with reasoning capabilities.
        
        Args:
            use_claude: Whether to use Claude instead of Gemini
        """
        # Define instructions for the agent
        instructions = [
            "You are a helpful assistant for Flutter developers.",
            "Answer questions about Flutter and the LikeMinds SDK clearly and concisely.",
            "If you don't know something, admit it rather than making up information."
        ]
        
        # Initialize the base agent with reasoning tools
        super().__init__(
            use_claude=use_claude,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=instructions,
            markdown=True
        )
    
    def print_response(self, query: str, stream: bool = True, show_reasoning: bool = False) -> str:
        """
        Print the response to a query and return it as a string.
        
        Args:
            query: The query to ask
            stream: Whether to stream the response
            show_reasoning: Whether to show the reasoning process
            
        Returns:
            The response as a string
        """
        # Call the print_response method of the base agent
        self.agent.print_response(
            query, 
            stream=stream, 
            show_full_reasoning=show_reasoning,
            stream_intermediate_steps=show_reasoning
        )
        
        # Also get the response as a string to return
        return self.ask(query, stream=False, show_reasoning=False)


if __name__ == "__main__":
    # Simple test to ensure the agent works
    agent = SimpleAgent(use_claude=True)
    agent.print_response(
        "What is Flutter and how does it relate to mobile app development?",
        stream=True,
        show_reasoning=True
    ) 