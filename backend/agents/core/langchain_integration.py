"""
LangChain integration module for the core agent submodule.

This module provides functionality for integrating LangChain and LangGraph
with the agent system.
"""

from typing import Any, Dict, List, Optional, Union
from langchain.chat_models import ChatAnthropic
from langchain.memory import ChatMessageHistory
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langgraph.graph import END, StateGraph
import json

def create_llm(
    model_name: str = "claude-3-sonnet-20240229",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    callbacks: Optional[List[BaseCallbackHandler]] = None,
) -> ChatAnthropic:
    """Create a LangChain LLM instance.
    
    Args:
        model_name: The name of the model to use
        temperature: The temperature to use
        max_tokens: The maximum number of tokens to generate
        callbacks: Optional list of callback handlers
        
    Returns:
        A LangChain LLM instance
    """
    return ChatAnthropic(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        callbacks=callbacks,
    )

def create_chat_prompt_template(
    system_template: str,
    human_template: str,
    input_variables: List[str],
) -> ChatPromptTemplate:
    """Create a LangChain chat prompt template.
    
    Args:
        system_template: The system message template
        human_template: The human message template
        input_variables: The input variables for the template
        
    Returns:
        A LangChain chat prompt template
    """
    return ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template),
    ]).partial(input_variables=input_variables)

class LangGraphBuilder:
    """Builder for LangGraph workflows."""
    
    def __init__(self):
        """Initialize the LangGraph builder."""
        self.graph = None
        self.nodes = {}
    
    def create_graph(self, name: str):
        """Create a new LangGraph workflow.
        
        Args:
            name: The name of the workflow
            
        Returns:
            Self for method chaining
        """
        self.graph = StateGraph(name)
        return self
    
    def add_node(self, name: str, function: Any):
        """Add a node to the workflow.
        
        Args:
            name: The name of the node
            function: The function to execute for this node
            
        Returns:
            Self for method chaining
        """
        self.nodes[name] = function
        self.graph.add_node(name, function)
        return self
    
    def add_edge(self, source: str, target: Union[str, END]):
        """Add an edge between nodes in the workflow.
        
        Args:
            source: The source node name
            target: The target node name or END
            
        Returns:
            Self for method chaining
        """
        self.graph.add_edge(source, target)
        return self
    
    def add_conditional_edge(self, source: str, condition_function: Any, targets: Dict[str, Union[str, END]]):
        """Add a conditional edge between nodes.
        
        Args:
            source: The source node name
            condition_function: Function that returns the edge to follow
            targets: Mapping of condition values to target nodes
            
        Returns:
            Self for method chaining
        """
        self.graph.add_conditional_edges(
            source, 
            condition_function,
            targets
        )
        return self
    
    def compile(self):
        """Compile the workflow.
        
        Returns:
            The compiled workflow
        """
        return self.graph.compile() 