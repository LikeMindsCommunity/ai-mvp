"""
Models for the Documentation Agent service.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ConversationMessage(BaseModel):
    """
    A single message in a conversation history.
    """
    user: str = Field(..., description="The message from the user")
    assistant: str = Field(..., description="The response from the assistant")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the message was sent")

class DocumentationRequest(BaseModel):
    """
    A request to the Documentation Agent.
    """
    query: str = Field(..., description="The user's query about documentation")
    project_id: str = Field(..., description="The project ID for context")
    platform: str = Field(..., description="The platform (e.g., 'android', 'ios', 'web')")
    conversation_history: Optional[List[ConversationMessage]] = Field(
        default=None, description="Previous conversation history"
    )
    user_id: Optional[str] = Field(default=None, description="The ID of the user making the request")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata for the request"
    )

class DocumentContext(BaseModel):
    """
    A piece of documentation context.
    """
    content: str = Field(..., description="The content of the documentation")
    source: str = Field(..., description="The source of the documentation")
    relevance_score: float = Field(..., description="The relevance score of the context")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata about the context"
    )

class DocumentationResponse(BaseModel):
    """
    A response from the Documentation Agent.
    """
    solution_document: str = Field(..., description="The solution document")
    relevant_context: List[DocumentContext] = Field(
        ..., description="The relevant context used to generate the solution"
    )
    next_steps: Optional[List[str]] = Field(
        default=None, description="Suggested next steps for the user"
    )
    request_id: str = Field(..., description="The unique ID for this request")
    processing_time: float = Field(..., description="Time taken to process in seconds")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata about the response"
    ) 