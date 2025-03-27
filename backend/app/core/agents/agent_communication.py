import logging
import asyncio
import uuid
import json
from typing import Dict, Any, List, Optional, Callable, Awaitable
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_communication")

class Message:
    """
    Represents a message sent between agents.
    """
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        message_type: str,
        content: Dict[str, Any],
        correlation_id: Optional[str] = None,
        reply_to: Optional[str] = None
    ):
        """
        Initialize a new message.
        
        Args:
            sender: ID of the sender agent
            recipient: ID of the recipient agent
            message_type: Type of message (e.g., 'request', 'response', 'notification')
            content: Message content as a dictionary
            correlation_id: Optional ID to correlate requests with responses
            reply_to: Optional ID to specify where to send replies
        """
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type
        self.content = content
        self.correlation_id = correlation_id or self.id
        self.reply_to = reply_to
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type,
            "content": self.content,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a message from a dictionary."""
        message = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            message_type=data["message_type"],
            content=data["content"],
            correlation_id=data.get("correlation_id"),
            reply_to=data.get("reply_to")
        )
        message.id = data["id"]
        message.timestamp = data["timestamp"]
        return message
    
    def create_reply(self, content: Dict[str, Any], message_type: str = "response") -> 'Message':
        """
        Create a reply message to this message.
        
        Args:
            content: Content of the reply
            message_type: Type of the reply message
            
        Returns:
            A new Message instance representing the reply
        """
        return Message(
            sender=self.recipient,
            recipient=self.reply_to or self.sender,
            message_type=message_type,
            content=content,
            correlation_id=self.correlation_id
        )


class MessageBroker:
    """
    Manages message routing between agents.
    Implements a publish-subscribe pattern for inter-agent communication.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one message broker exists."""
        if cls._instance is None:
            cls._instance = super(MessageBroker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the message broker if not already initialized."""
        if not getattr(self, "_initialized", False):
            self._subscribers: Dict[str, List[Callable[[Message], Awaitable[None]]]] = {}
            self._message_history: List[Message] = []
            self._max_history_size = 1000
            self._initialized = True
            logger.info("Message broker initialized")
    
    async def publish(self, message: Message) -> None:
        """
        Publish a message to all subscribers of the recipient.
        
        Args:
            message: The message to publish
        """
        # Store message in history
        self._add_to_history(message)
        
        # Log the message
        logger.debug(f"Publishing message from {message.sender} to {message.recipient}")
        
        # If recipient is "broadcast", send to all subscribers
        if message.recipient == "broadcast":
            tasks = []
            for topic, subscribers in self._subscribers.items():
                for subscriber in subscribers:
                    tasks.append(self._deliver_message(subscriber, message))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            return
        
        # Otherwise, send only to the specified recipient's subscribers
        if message.recipient in self._subscribers:
            tasks = []
            for subscriber in self._subscribers[message.recipient]:
                tasks.append(self._deliver_message(subscriber, message))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _deliver_message(self, subscriber: Callable[[Message], Awaitable[None]], message: Message) -> None:
        """
        Deliver a message to a subscriber with error handling.
        
        Args:
            subscriber: The subscriber callback
            message: The message to deliver
        """
        try:
            await subscriber(message)
        except Exception as e:
            logger.error(f"Error delivering message to subscriber: {str(e)}", exc_info=True)
    
    def subscribe(self, topic: str, callback: Callable[[Message], Awaitable[None]]) -> None:
        """
        Subscribe to messages for a specific topic (usually an agent ID).
        
        Args:
            topic: The topic to subscribe to (usually the agent ID)
            callback: Async function to call when a message is received
        """
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        
        self._subscribers[topic].append(callback)
        logger.debug(f"Added subscriber to topic {topic}")
    
    def unsubscribe(self, topic: str, callback: Callable[[Message], Awaitable[None]]) -> None:
        """
        Unsubscribe from a topic.
        
        Args:
            topic: The topic to unsubscribe from
            callback: The callback to remove
        """
        if topic in self._subscribers and callback in self._subscribers[topic]:
            self._subscribers[topic].remove(callback)
            logger.debug(f"Removed subscriber from topic {topic}")
            
            # Remove topic if no subscribers left
            if not self._subscribers[topic]:
                del self._subscribers[topic]
    
    def get_message_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent message history.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        return [msg.to_dict() for msg in self._message_history[-limit:]]
    
    def _add_to_history(self, message: Message) -> None:
        """
        Add a message to the history, maintaining maximum size.
        
        Args:
            message: Message to add to history
        """
        self._message_history.append(message)
        
        # Trim history if too large
        if len(self._message_history) > self._max_history_size:
            self._message_history = self._message_history[-self._max_history_size:]


class AgentCommunication:
    """
    Helper class to simplify agent communication.
    This can be used within agents to send and receive messages.
    """
    
    def __init__(self, agent_id: str):
        """
        Initialize communication for an agent.
        
        Args:
            agent_id: ID of the agent using this communication helper
        """
        self.agent_id = agent_id
        self.broker = MessageBroker()
        self.message_handlers: Dict[str, Callable[[Message], Awaitable[None]]] = {}
        self.pending_requests: Dict[str, asyncio.Future] = {}
        
        # Subscribe to messages for this agent
        self.broker.subscribe(self.agent_id, self._on_message_received)
        logger.info(f"Agent communication initialized for agent {agent_id}")
    
    async def _on_message_received(self, message: Message) -> None:
        """
        Handle received messages.
        
        Args:
            message: The received message
        """
        # Check if this is a response to a pending request
        if message.correlation_id in self.pending_requests:
            future = self.pending_requests[message.correlation_id]
            if not future.done():
                future.set_result(message)
            return
        
        # Otherwise, route to appropriate message handler
        if message.message_type in self.message_handlers:
            try:
                await self.message_handlers[message.message_type](message)
            except Exception as e:
                logger.error(f"Error in message handler for {message.message_type}: {str(e)}", exc_info=True)
    
    def register_handler(self, message_type: str, handler: Callable[[Message], Awaitable[None]]) -> None:
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: Type of messages to handle
            handler: Async function to call when a message of this type is received
        """
        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type {message_type} in agent {self.agent_id}")
    
    async def send_message(self, recipient: str, message_type: str, content: Dict[str, Any]) -> None:
        """
        Send a message to another agent.
        
        Args:
            recipient: ID of the recipient agent
            message_type: Type of message to send
            content: Message content
        """
        message = Message(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content
        )
        await self.broker.publish(message)
    
    async def broadcast_message(self, message_type: str, content: Dict[str, Any]) -> None:
        """
        Broadcast a message to all agents.
        
        Args:
            message_type: Type of message to send
            content: Message content
        """
        await self.send_message("broadcast", message_type, content)
    
    async def send_request(self, recipient: str, content: Dict[str, Any], timeout: float = 30.0) -> Message:
        """
        Send a request and wait for a response.
        
        Args:
            recipient: ID of the recipient agent
            content: Request content
            timeout: Maximum time to wait for a response in seconds
            
        Returns:
            Response message
            
        Raises:
            asyncio.TimeoutError: If no response is received within the timeout
        """
        # Create a future to wait for the response
        future = asyncio.get_event_loop().create_future()
        
        # Create and send the request message
        message = Message(
            sender=self.agent_id,
            recipient=recipient,
            message_type="request",
            content=content,
            reply_to=self.agent_id
        )
        
        # Store the future
        self.pending_requests[message.correlation_id] = future
        
        # Send the message
        await self.broker.publish(message)
        
        try:
            # Wait for the response
            return await asyncio.wait_for(future, timeout)
        finally:
            # Clean up the pending request
            if message.correlation_id in self.pending_requests:
                del self.pending_requests[message.correlation_id]
    
    def cleanup(self) -> None:
        """Unsubscribe from the broker when done."""
        self.broker.unsubscribe(self.agent_id, self._on_message_received)
        logger.info(f"Agent communication cleaned up for agent {self.agent_id}") 