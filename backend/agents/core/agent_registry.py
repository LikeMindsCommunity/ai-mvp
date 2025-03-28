"""
Agent registry module for managing agent lifecycle.

This module provides functionality for registering, finding, and managing
the lifecycle of agents in the system.
"""

from typing import Any, Dict, List, Optional, Type
import logging
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AgentRegistry:
    """Registry for managing agents in the system."""
    
    def __init__(self):
        """Initialize the agent registry."""
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, Type[BaseAgent]] = {}
    
    def register_agent_type(self, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """Register an agent type with the registry.
        
        Args:
            agent_type: The type identifier for the agent
            agent_class: The agent class
        """
        if agent_type in self.agent_types:
            logger.warning(f"Agent type {agent_type} already registered, overwriting")
        
        self.agent_types[agent_type] = agent_class
        logger.info(f"Registered agent type: {agent_type}")
    
    def create_agent(
        self, 
        agent_id: str, 
        agent_type: str, 
        name: str, 
        description: str,
        **kwargs
    ) -> BaseAgent:
        """Create and register an agent instance.
        
        Args:
            agent_id: The unique identifier for the agent
            agent_type: The type of agent to create
            name: The name of the agent
            description: A description of the agent
            **kwargs: Additional arguments to pass to the agent constructor
            
        Returns:
            The created agent instance
            
        Raises:
            ValueError: If the agent type is not registered
            ValueError: If an agent with the given ID already exists
        """
        if agent_type not in self.agent_types:
            raise ValueError(f"Agent type {agent_type} not registered")
        
        if agent_id in self.agents:
            raise ValueError(f"Agent with ID {agent_id} already exists")
        
        agent_class = self.agent_types[agent_type]
        agent = agent_class(name=name, description=description, **kwargs)
        self.agents[agent_id] = agent
        
        logger.info(f"Created agent: {agent_id} (type: {agent_type})")
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID.
        
        Args:
            agent_id: The ID of the agent to get
            
        Returns:
            The agent instance or None if not found
        """
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents.
        
        Returns:
            A list of agent information dictionaries
        """
        return [
            {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description,
                "type": type(agent).__name__,
            }
            for agent_id, agent in self.agents.items()
        ]
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry.
        
        Args:
            agent_id: The ID of the agent to remove
            
        Returns:
            True if the agent was removed, False if not found
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"Removed agent: {agent_id}")
            return True
        
        logger.warning(f"Attempted to remove non-existent agent: {agent_id}")
        return False


# Create a global instance of the agent registry
agent_registry = AgentRegistry() 