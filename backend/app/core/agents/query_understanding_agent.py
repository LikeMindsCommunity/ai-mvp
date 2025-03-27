import os
from typing import Dict, Any, List, Optional
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from ..config.env import QUERY_MODEL, API_KEYS
from .base_agent import BaseAgent

class QueryUnderstandingAgent(BaseAgent):
    """
    Agent responsible for understanding and enhancing user queries.
    Uses Claude 3.7 Sonnet for advanced query understanding and expansion.
    """
    
    def __init__(self, name="query_understanding_agent", **kwargs):
        """
        Initialize the Query Understanding Agent with Claude 3.7 Sonnet.
        
        Args:
            name: Name of the agent instance
            **kwargs: Additional arguments passed to the BaseAgent constructor
        """
        super().__init__(name=name, **kwargs)
        
        self.llm = ChatAnthropic(
            model=QUERY_MODEL,
            anthropic_api_key=API_KEYS["ANTHROPIC_API_KEY"]
        )
        
        # Define prompt template for query enhancement
        self.query_enhancement_prompt = PromptTemplate.from_template(
            """You are an expert query understanding system for LikeMinds SDK documentation. Your task is to analyze and enhance user queries to improve retrieval of relevant documentation.

USER QUERY: {query}

{conversation_context}

Follow these steps:
1. Understand the core intent of the query
2. Identify key concepts, feature names, and technical terms
3. Expand acronyms and technical terms into their full forms
4. Add relevant synonyms and alternative phrasings
5. Identify the platform or language context if mentioned (iOS, Android, etc.)
6. Consider any implicit requirements or constraints

Then, rewrite the query to be more comprehensive. Keep the enhanced query focused and concise while including critical details for retrieval. The enhanced query should be no more than 2-3 sentences.

FORMAT YOUR RESPONSE AS THE ENHANCED QUERY ONLY. Do not include explanations, metadata, or any other text."""
        )
    
    async def enhance_query(self, 
                           query: str, 
                           conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Analyzes and enhances a user query for better retrieval.
        
        Args:
            query: The original user query
            conversation_history: Optional list of previous conversation turns
            
        Returns:
            Enhanced query for better context retrieval
        """
        # Format conversation context if available
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            conversation_context = "CONVERSATION HISTORY:\n"
            # Include up to 3 most recent turns
            for turn in conversation_history[-3:]:
                if "user" in turn:
                    conversation_context += f"User: {turn['user']}\n"
                if "assistant" in turn:
                    conversation_context += f"Assistant: {turn['assistant']}\n"
            conversation_context += "\nUse this conversation history to understand the context of the current query."
        
        # Generate prompt
        prompt = self.query_enhancement_prompt.format(
            query=query,
            conversation_context=conversation_context
        )
        
        # Get enhanced query from Claude
        message = HumanMessage(content=prompt)
        response = await self.llm.ainvoke([message])
        enhanced_query = response.content.strip()
        
        return enhanced_query
        
    async def _execute(self, task_input: Dict[str, Any]) -> Any:
        """
        Implement the BaseAgent execute method.
        
        Args:
            task_input: Dictionary containing task parameters
            
        Returns:
            Enhanced query string
        """
        query = task_input.get("query", "")
        conversation_history = task_input.get("conversation_history", [])
        
        return await self.enhance_query(query, conversation_history) 