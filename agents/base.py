"""
Base agent class for all specialized agents in the system.
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from typing import List, Dict, Any, Optional

from agents.config import DEFAULT_MODEL, CLAUDE_MODEL


class BaseAgent:
    """Base agent class that handles common agent functionality."""
    
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL,
        use_claude: bool = False,
        tools: List[Any] = None,
        instructions: List[str] = None,
        markdown: bool = True,
    ):
        """
        Initialize the base agent with the specified model and configuration.
        
        Args:
            model_id: The model ID to use (defaults to config.DEFAULT_MODEL)
            use_claude: Whether to use Claude instead of Gemini
            tools: List of tools to provide to the agent
            instructions: List of instructions for the agent
            markdown: Whether to enable markdown formatting
        """
        tools = tools or []
        instructions = instructions or []
        
        # Configure the appropriate model
        if use_claude:
            self.model = Claude(id=CLAUDE_MODEL)
        else:
            self.model = Gemini(id=model_id)
            
        # Create the agent
        self.agent = Agent(
            model=self.model,
            tools=tools,
            instructions=instructions,
            markdown=markdown
        )
    
    def ask(self, query: str, stream: bool = True, show_reasoning: bool = False) -> str:
        """
        Ask the agent a question and get a response.
        
        Args:
            query: The query to ask the agent
            stream: Whether to stream the response
            show_reasoning: Whether to show the agent's reasoning process
            
        Returns:
            The agent's response as a string
        """
        response = self.agent.run(
            query, 
            stream=stream, 
            show_full_reasoning=show_reasoning,
            stream_intermediate_steps=show_reasoning
        )
        
        # Extract the text content from the RunResponse object
        # The RunResponse has a __str__ method, so we can convert it to string
        return str(response)
    
    def print_response(self, query: str, stream: bool = True, show_reasoning: bool = False) -> None:
        """
        Ask the agent a question and print the response.
        
        Args:
            query: The query to ask the agent
            stream: Whether to stream the response
            show_reasoning: Whether to show the agent's reasoning process
        """
        self.agent.print_response(
            query, 
            stream=stream, 
            show_full_reasoning=show_reasoning,
            stream_intermediate_steps=show_reasoning
        ) 