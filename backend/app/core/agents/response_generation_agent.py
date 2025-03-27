import os
from typing import Dict, Any, List, Tuple, AsyncGenerator
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from ..config.env import RESPONSE_MODEL, API_KEYS
from .base_agent import BaseAgent

class ResponseGenerationAgent(BaseAgent):
    """
    Agent responsible for generating comprehensive responses to user queries
    based on retrieved context. Uses Claude 3.7 Sonnet for advanced reasoning.
    """
    
    def __init__(self, name="response_generation_agent", **kwargs):
        """
        Initialize the Response Generation Agent with Claude 3.7 Sonnet.
        
        Args:
            name: Name of the agent instance
            **kwargs: Additional arguments passed to the BaseAgent constructor
        """
        super().__init__(name=name, **kwargs)
        
        self.llm = ChatAnthropic(
            model=RESPONSE_MODEL,
            anthropic_api_key=API_KEYS["ANTHROPIC_API_KEY"],
            streaming=True
        )
        
        # Define prompt template for response generation
        self.response_prompt = PromptTemplate.from_template(
            """You are an expert developer support assistant for the LikeMinds SDK, specializing in helping developers implement chat and social feed features in their applications. You provide detailed, helpful responses based on official documentation.

USER QUERY: {query}

ENHANCED QUERY: {enhanced_query}

RELEVANT DOCUMENTATION CONTEXT:
{context}

Your task is to provide a comprehensive response to the user's query using the provided documentation context. Follow these guidelines:

1. Answer directly and precisely, focusing on addressing the user's specific question or problem
2. Include relevant code examples when available in the context
3. Explain implementation steps in a clear, structured manner
4. Consider the specific platform mentioned in the query (if any)
5. If the context lacks specific information to fully answer the query, acknowledge this and provide the best guidance possible based on related information
6. Use Markdown formatting to structure your response with headers, code blocks, etc.

Format your response as follows:
1. Start with a concise title summarizing the query topic
2. Provide a clear, step-by-step explanation
3. Include code examples or implementation details when relevant
4. Summarize key points at the end if the response is lengthy
5. Mention which sources you used for specific information

DO NOT make up information that isn't supported by the provided context. If you're unsure, say so rather than providing incorrect information.

{conversation_context}"""
        )
    
    async def generate_response_stream(self, 
                                      query: str, 
                                      enhanced_query: str,
                                      context: List[Dict[str, Any]],
                                      conversation_history: List[Dict[str, str]] = None) -> AsyncGenerator[str, None]:
        """
        Generate a response to the user query based on the retrieved context, streaming tokens as they're generated.
        
        Args:
            query: The original user query
            enhanced_query: The enhanced query used for retrieval
            context: List of retrieved document chunks with relevance scores
            conversation_history: Optional conversation history
            
        Yields:
            Tokens of the generated response as they become available
        """
        try:
            # Format conversation context if available
            conversation_context = ""
            if conversation_history and len(conversation_history) > 0:
                conversation_context = "CONVERSATION HISTORY:\n"
                for msg in conversation_history[-3:]:  # Only use the last 3 messages for context
                    role = msg.get("role", "user").capitalize()
                    content = msg.get("content", "")
                    conversation_context += f"{role}: {content}\n"
            
            # Format context into a string
            context_str = ""
            sources = []
            
            for i, doc in enumerate(context):
                # Add document to context
                source = doc.get("metadata", {}).get("source", "Unknown")
                if source not in sources:
                    sources.append(source)
                
                context_str += f"[SOURCE{i+1}] "
                context_str += f"From: {source}\n"
                
                # Include metadata info when available
                metadata = doc.get("metadata", {})
                if metadata.get("platform"):
                    context_str += f"Platform: {metadata.get('platform')}\n"
                if metadata.get("product_area"):
                    context_str += f"Feature: {metadata.get('product_area')}\n"
                if metadata.get("title"):
                    context_str += f"Title: {metadata.get('title')}\n"
                
                context_str += f"Content:\n{doc.get('content', '')}\n\n"
            
            # Prepare prompt
            prompt = self.response_prompt.format(
                query=query,
                enhanced_query=enhanced_query,
                context=context_str,
                conversation_context=conversation_context
            )
            
            # Generate streaming response
            message = HumanMessage(content=prompt)
            
            # Stream the response
            async for chunk in self.llm.astream([message]):
                if hasattr(chunk, 'content'):
                    yield chunk.content
            
        except Exception as e:
            print(f"Error generating streaming response: {str(e)}")
            yield f"I apologize, but I encountered an error while generating a response: {str(e)}"
            
    async def generate_response(self, 
                               query: str, 
                               enhanced_query: str,
                               context: List[Dict[str, Any]],
                               conversation_history: List[Dict[str, str]] = None) -> Tuple[str, List[str]]:
        """
        Generate a response to the user query based on retrieved context.
        
        Args:
            query: The original user query
            enhanced_query: Enhanced query from understanding agent
            context: List of relevant document chunks with metadata
            conversation_history: Optional conversation history
            
        Returns:
            Tuple containing (response_text, sources)
        """
        # Format conversation context if available
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            conversation_context = "CONVERSATION HISTORY:\n"
            for msg in conversation_history[-3:]:  # Only use the last 3 messages for context
                role = msg.get("role", "user").capitalize()
                content = msg.get("content", "")
                conversation_context += f"{role}: {content}\n"
                
        # Format context for the prompt
        context_text = ""
        references = []
        
        for i, chunk in enumerate(context):
            # Add source reference
            source = chunk["metadata"].get("source", "Unknown source")
            if source not in references:
                references.append(source)
            ref_id = references.index(source) + 1
            
            # Format chunk content with relevance information
            context_text += f"SOURCE[{ref_id}] Relevance Score: {chunk.get('relevance_score', 'N/A')}/10\n"
            context_text += f"Content: {chunk['content']}\n"
            
            # Add code blocks if available in metadata
            if chunk["metadata"].get("has_code", False) and chunk["metadata"].get("code_blocks"):
                for code_block in chunk["metadata"]["code_blocks"]:
                    context_text += f"Code Example: {code_block}\n"
            
            context_text += f"Metadata: {json.dumps({k: v for k, v in chunk['metadata'].items() if k not in ['code_blocks']})}\n\n"
        
        # Add reference list at the end
        context_text += "REFERENCES:\n"
        for i, ref in enumerate(references):
            context_text += f"[{i+1}] {ref}\n"
        
        # Generate prompt
        prompt = self.response_prompt.format(
            query=query,
            enhanced_query=enhanced_query,
            context=context_text,
            conversation_context=conversation_context
        )
        
        # Get response from Claude using LangChain
        message = HumanMessage(content=prompt)
        response = await self.llm.ainvoke([message])
        response_text = response.content
        
        return response_text, references 

    async def _execute(self, task_input: Dict[str, Any]) -> Any:
        """
        Implement the BaseAgent execute method.
        
        Args:
            task_input: Dictionary containing task parameters
            
        Returns:
            Tuple containing (response_text, sources)
        """
        query = task_input.get("query", "")
        enhanced_query = task_input.get("enhanced_query", "")
        context = task_input.get("context", [])
        conversation_history = task_input.get("conversation_history", [])
        
        return await self.generate_response(query, enhanced_query, context, conversation_history) 