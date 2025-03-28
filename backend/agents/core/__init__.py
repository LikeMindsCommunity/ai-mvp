"""
Core module for shared functionality across agents.

This module re-exports functionality from the infrastructure module
for backward compatibility and convenience.
"""

from ...infrastructure import (
    User, 
    get_current_user, 
    get_optional_user, 
    create_access_token,
    settings,
    trace,
    monitor,
)

# Import core agent functionality
from .base_agent import BaseAgent
from .agent_communication import AgentMessage, AgentCommunicationManager, communication_manager
from .agent_registry import AgentRegistry, agent_registry
from .langchain_integration import create_llm, create_chat_prompt_template, LangGraphBuilder

__all__ = [
    # Infrastructure exports
    "User", 
    "get_current_user", 
    "get_optional_user", 
    "create_access_token",
    "settings",
    "trace",
    "monitor",
    
    # Core agent exports
    "BaseAgent",
    "AgentMessage",
    "AgentCommunicationManager",
    "communication_manager",
    "AgentRegistry",
    "agent_registry",
    "create_llm",
    "create_chat_prompt_template",
    "LangGraphBuilder",
] 