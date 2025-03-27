import logging
import asyncio
import uuid
from typing import Dict, Any, List, Optional, Callable, Awaitable
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseAgent(ABC):
    """
    Base agent class that provides common functionality for all agents.
    Agents are specialized components that perform specific tasks in the system.
    """
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: Unique identifier for this agent
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
        self.state: Dict[str, Any] = {}
        self.callbacks: Dict[str, List[Callable[..., Awaitable[None]]]] = {
            "on_start": [],
            "on_complete": [],
            "on_error": []
        }
        self.logger.info(f"Agent {name} initialized with ID {self.id}")
    
    def set_state(self, key: str, value: Any) -> None:
        """
        Set a state value for the agent.
        
        Args:
            key: State key
            value: State value
        """
        self.state[key] = value
        self.logger.debug(f"Set state '{key}' for agent {self.name}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get a state value for the agent.
        
        Args:
            key: State key
            default: Default value if key doesn't exist
            
        Returns:
            The state value or default if not found
        """
        return self.state.get(key, default)
    
    def register_callback(self, event: str, callback: Callable[..., Awaitable[None]]) -> None:
        """
        Register a callback for a specific event.
        
        Args:
            event: Event name (on_start, on_complete, on_error)
            callback: Async callback function
        """
        if event not in self.callbacks:
            raise ValueError(f"Unknown event type: {event}")
        self.callbacks[event].append(callback)
        self.logger.debug(f"Registered {event} callback for agent {self.name}")
    
    async def trigger_callbacks(self, event: str, *args, **kwargs) -> None:
        """
        Trigger all callbacks for a specific event.
        
        Args:
            event: Event name
            *args, **kwargs: Arguments to pass to callbacks
        """
        if event not in self.callbacks:
            return
        
        for callback in self.callbacks[event]:
            try:
                await callback(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in {event} callback: {str(e)}", exc_info=True)
    
    async def execute(self, *args, **kwargs) -> Any:
        """
        Execute the agent's task with proper logging and error handling.
        
        Args:
            *args, **kwargs: Arguments to pass to _execute
            
        Returns:
            The result of the agent's task
        """
        start_time = __import__('time').time()
        self.logger.info(f"Starting execution of agent {self.name}")
        
        try:
            # Trigger start callbacks
            await self.trigger_callbacks("on_start", *args, **kwargs)
            
            # Execute the agent's task
            result = await self._execute(*args, **kwargs)
            
            # Log execution time
            execution_time = __import__('time').time() - start_time
            self.logger.info(f"Agent {self.name} completed in {execution_time:.2f}s")
            
            # Trigger complete callbacks
            await self.trigger_callbacks("on_complete", result, *args, **kwargs)
            
            return result
            
        except Exception as e:
            # Log error
            self.logger.error(f"Error in agent {self.name}: {str(e)}", exc_info=True)
            
            # Trigger error callbacks
            await self.trigger_callbacks("on_error", e, *args, **kwargs)
            
            # Re-raise the exception
            raise
    
    @abstractmethod
    async def _execute(self, *args, **kwargs) -> Any:
        """
        Implement the agent's core functionality.
        Must be implemented by subclasses.
        
        Returns:
            The result of the agent's task
        """
        pass 