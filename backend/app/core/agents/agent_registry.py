import logging
from typing import Dict, Type, List, Any, Optional, Union
from .base_agent import BaseAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_registry")

class AgentRegistry:
    """
    A registry to manage all agents in the system.
    Provides methods to register, retrieve, and manage agent instances.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one registry exists."""
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the registry if not already initialized."""
        if not getattr(self, "_initialized", False):
            self._agent_classes: Dict[str, Type[BaseAgent]] = {}
            self._agent_instances: Dict[str, BaseAgent] = {}
            self._initialized = True
            logger.info("Agent registry initialized")
    
    def register_agent_class(self, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """
        Register an agent class with the registry.
        
        Args:
            agent_type: Type identifier for this agent class
            agent_class: Agent class (should be a subclass of BaseAgent)
        """
        if not issubclass(agent_class, BaseAgent):
            raise TypeError(f"Agent class must be a subclass of BaseAgent, got {agent_class}")
        
        self._agent_classes[agent_type] = agent_class
        logger.info(f"Registered agent class '{agent_type}'")
    
    def create_agent(self, agent_class_or_type: Union[str, Type[BaseAgent]], **kwargs) -> BaseAgent:
        """
        Create a new agent instance and register it.
        
        Args:
            agent_class_or_type: Type name or class of agent to create
            **kwargs: Additional arguments to pass to the agent constructor
            
        Returns:
            The created agent instance
        """
        # Generate a default name if not provided
        if 'name' not in kwargs:
            if isinstance(agent_class_or_type, str):
                kwargs['name'] = f"{agent_class_or_type}_agent"
            else:
                kwargs['name'] = f"{agent_class_or_type.__name__}_agent"
        
        agent_name = kwargs['name']
        
        # Check if this agent already exists
        if agent_name in self._agent_instances:
            logger.info(f"Agent '{agent_name}' already exists, returning existing instance")
            return self._agent_instances[agent_name]
            
        # Create the agent based on type or class
        if isinstance(agent_class_or_type, str):
            # Agent type was provided
            if agent_class_or_type not in self._agent_classes:
                raise ValueError(f"Unknown agent type: {agent_class_or_type}")
            
            agent_class = self._agent_classes[agent_class_or_type]
            agent = agent_class(**kwargs)
        else:
            # Agent class was provided
            if not issubclass(agent_class_or_type, BaseAgent):
                raise TypeError(f"Agent class must be a subclass of BaseAgent, got {agent_class_or_type}")
            
            agent = agent_class_or_type(**kwargs)
        
        # Register the agent instance
        self._agent_instances[agent_name] = agent
        logger.info(f"Created agent instance '{agent_name}' of type '{agent.__class__.__name__}'")
        
        return agent
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent instance by name.
        
        Args:
            name: Name of the agent to retrieve
            
        Returns:
            The agent instance or None if not found
        """
        return self._agent_instances.get(name)
    
    def get_agents_by_type(self, agent_type: str) -> List[BaseAgent]:
        """
        Get all agent instances of a specific type.
        
        Args:
            agent_type: Type of agents to retrieve
            
        Returns:
            List of agent instances of the specified type
        """
        agent_class = self._agent_classes.get(agent_type)
        if not agent_class:
            return []
        
        return [
            agent for agent in self._agent_instances.values()
            if isinstance(agent, agent_class)
        ]
    
    def remove_agent(self, name: str) -> None:
        """
        Remove an agent from the registry.
        
        Args:
            name: Name of the agent to remove
        """
        if name in self._agent_instances:
            del self._agent_instances[name]
            logger.info(f"Removed agent '{name}' from registry")
    
    @property
    def registered_agent_types(self) -> List[str]:
        """Get a list of all registered agent types."""
        return list(self._agent_classes.keys())
    
    @property
    def registered_agents(self) -> List[str]:
        """Get a list of all registered agent names."""
        return list(self._agent_instances.keys())
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about all registered agents.
        
        Returns:
            Dictionary with information about all registered agents
        """
        return {
            "agent_types": self.registered_agent_types,
            "agent_instances": [
                {
                    "name": name,
                    "type": agent.__class__.__name__,
                    "id": agent.id
                }
                for name, agent in self._agent_instances.items()
            ]
        } 