"""
Agent communication module for handling message passing between agents.

This module provides functionality for agents to communicate with each other
in a structured and traceable way.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import uuid
import json
import asyncio
from datetime import datetime

@dataclass
class AgentMessage:
    """A message between agents."""
    
    sender_id: str
    receiver_id: str
    content: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create a message from a dictionary."""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]) 
                if isinstance(data.get("timestamp"), str) 
                else data.get("timestamp", datetime.now()),
        )


class AgentCommunicationManager:
    """Manages communication between agents."""
    
    def __init__(self):
        """Initialize the communication manager."""
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.message_history: List[AgentMessage] = []
    
    def register_agent(self, agent_id: str) -> None:
        """Register an agent with the communication manager.
        
        Args:
            agent_id: The ID of the agent to register
        """
        if agent_id not in self.message_queues:
            self.message_queues[agent_id] = asyncio.Queue()
    
    async def send_message(self, message: AgentMessage) -> None:
        """Send a message to an agent.
        
        Args:
            message: The message to send
        """
        # Store the message in history
        self.message_history.append(message)
        
        # Make sure the receiver is registered
        self.register_agent(message.receiver_id)
        
        # Add the message to the receiver's queue
        await self.message_queues[message.receiver_id].put(message)
    
    async def receive_message(self, agent_id: str, timeout: Optional[float] = None) -> Optional[AgentMessage]:
        """Receive a message for an agent.
        
        Args:
            agent_id: The ID of the agent receiving the message
            timeout: Optional timeout in seconds
            
        Returns:
            The received message or None if timeout occurred
        """
        # Make sure the agent is registered
        self.register_agent(agent_id)
        
        try:
            if timeout is not None:
                return await asyncio.wait_for(self.message_queues[agent_id].get(), timeout)
            else:
                return await self.message_queues[agent_id].get()
        except asyncio.TimeoutError:
            return None
    
    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """Get all messages for a specific agent.
        
        Args:
            agent_id: The ID of the agent
            
        Returns:
            List of messages where the agent is either sender or receiver
        """
        return [
            msg for msg in self.message_history
            if msg.sender_id == agent_id or msg.receiver_id == agent_id
        ]


# Create a global instance of the communication manager
communication_manager = AgentCommunicationManager() 