"""
Base Agent class providing common functionality for all agents.

This module defines the BaseAgent abstract class which serves as the foundation
for all agent implementations in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler

class BaseAgent(ABC):
    """Base class for all agents in the system.
    
    Provides common functionality and defines the interface that all agents must implement.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        model_name: str = "claude-3-sonnet-20240229",
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        system_prompt: Optional[str] = None,
    ):
        """Initialize a base agent.
        
        Args:
            name: The name of the agent
            description: A description of the agent's purpose
            model_name: The name of the LLM model to use
            callbacks: Optional list of callback handlers
            system_prompt: Optional system prompt to initialize the agent
        """
        self.name = name
        self.description = description
        self.model_name = model_name
        self.callbacks = callbacks or []
        self.system_prompt = system_prompt
        self.conversation_history: List[Any] = []
        
        if system_prompt:
            self.conversation_history.append(SystemMessage(content=system_prompt))
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent on the given input data.
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            The output from the agent
        """
        pass
    
    def add_message(self, message: str, role: str = "human"):
        """Add a message to the agent's conversation history.
        
        Args:
            message: The message content
            role: The role of the message sender (human or ai)
        """
        if role.lower() == "human":
            self.conversation_history.append(HumanMessage(content=message))
        elif role.lower() == "ai":
            self.conversation_history.append(AIMessage(content=message))
        else:
            raise ValueError(f"Unsupported role: {role}")
    
    def clear_history(self):
        """Clear the conversation history.
        
        If there was a system prompt, it will be preserved.
        """
        system_messages = [m for m in self.conversation_history 
                           if isinstance(m, SystemMessage)]
        self.conversation_history = system_messages 