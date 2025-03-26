import os
from typing import Dict, Any, List
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from ..config.env import CONTEXT_MODEL, API_KEYS

class ContextRetrievalAgent:
    """
    Agent responsible for reranking and filtering retrieved document chunks
    to ensure relevance to the query. Uses GPT-4o for advanced relevance scoring.
    """
    
    def __init__(self):
        """
        Initialize the Context Retrieval Agent with GPT-4o.
        """
        self.llm = ChatOpenAI(
            model=CONTEXT_MODEL,
            openai_api_key=API_KEYS["OPENAI_API_KEY"]
        )
        
        # Define prompt template for relevance scoring with a simplified approach
        self.relevance_prompt = """You are an expert context evaluator for a RAG system focused on LikeMinds SDK documentation.
Your task is to analyze the relevance of retrieved document chunks to a user's enhanced query.

ENHANCED QUERY: {{query}}

DOCUMENT CHUNKS:
{{chunks}}

For each chunk, analyze its relevance to the query and assign a numerical score from 0 to 10 where:
- 10: Perfect match that directly answers the query
- 7-9: Highly relevant, contains important information related to the query
- 4-6: Moderately relevant, contains some related information
- 1-3: Slightly relevant, has minor connections to the query
- 0: Not relevant at all

Provide your assessment as a JSON array where each item contains:
1. chunk_id: The ID of the document chunk
2. relevance_score: Your numerical score (0-10)
3. reasoning: A brief 1-2 sentence explanation for your scoring

Example response format:
```json
[
  {
    "chunk_id": "1",
    "relevance_score": 8,
    "reasoning": "Contains specific implementation details that directly address the query about X."
  },
  {
    "chunk_id": "2",
    "relevance_score": 3,
    "reasoning": "Mentions the topic but lacks specific details needed to answer the query."
  }
]
```"""
    
    async def rerank_documents(self, enhanced_query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rerank retrieved documents based on relevance to the enhanced query.
        
        Args:
            enhanced_query: The enhanced user query
            documents: List of retrieved document chunks
            
        Returns:
            Reranked document list with relevance scores
        """
        if not documents:
            return []
            
        # Format document chunks for the prompt, avoiding format string issues
        chunks_text = ""
        for i, doc in enumerate(documents):
            # Safe access to ID field
            doc_id = str(doc.get('id', f'chunk_{i}'))
            
            chunks_text += f"CHUNK {i+1} (ID: {doc_id}):\n"
            chunks_text += f"Content: {doc.get('content', 'No content')}\n"
            
            # Safely format metadata as string
            metadata_str = "Metadata: "
            if 'metadata' in doc and isinstance(doc['metadata'], dict):
                for key, value in doc['metadata'].items():
                    if key not in ["code_blocks"] and value is not None:
                        metadata_str += f"{key}: {value}, "
                chunks_text += f"{metadata_str.rstrip(', ')}\n\n"
            else:
                chunks_text += "No metadata available\n\n"
        
        # Use string replacement instead of format to avoid JSON parsing issues
        prompt = self.relevance_prompt.replace("{{query}}", enhanced_query).replace("{{chunks}}", chunks_text)
        
        # Get relevance scores from GPT-4o
        message = HumanMessage(content=prompt)
        response = await self.llm.ainvoke([message])
        response_text = response.content
        
        # Extract JSON output
        import re
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
        
        if not json_match:
            # Try to extract JSON without code block markers
            try:
                rankings = json.loads(response_text.strip())
            except:
                # Return original documents if parsing fails
                print("Warning: Failed to parse relevance rankings from model response")
                return documents
        else:
            try:
                rankings = json.loads(json_match.group(1))
            except:
                # Return original documents if parsing fails
                print("Warning: Failed to parse relevance rankings from JSON codeblock")
                return documents
        
        # Match rankings with documents and add relevance scores
        ranked_docs = []
        for doc in documents:
            doc_id = str(doc.get('id', ''))
            doc_ranking = next((r for r in rankings if str(r.get('chunk_id', '')) == doc_id), None)
            
            if doc_ranking:
                # Add relevance score and reasoning to document
                doc['relevance_score'] = doc_ranking.get('relevance_score', 5)
                doc['relevance_reasoning'] = doc_ranking.get('reasoning', '')
                ranked_docs.append(doc)
            else:
                # Keep original document if no ranking found
                doc['relevance_score'] = 5  # Default score
                doc['relevance_reasoning'] = 'No explicit ranking available'
                ranked_docs.append(doc)
        
        # Sort by relevance score (descending)
        ranked_docs.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return ranked_docs