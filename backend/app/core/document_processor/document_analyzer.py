import os
from typing import Dict, Any
import json
import re
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from ..config.env import QUERY_MODEL, API_KEYS

class DocumentAnalyzer:
    """
    Analyzes documentation content using Claude 3.7 Sonnet to extract key information.
    Uses advanced reasoning to understand documentation structure and content.
    """
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model=QUERY_MODEL,
            anthropic_api_key=API_KEYS["ANTHROPIC_API_KEY"]
        )
        
    async def analyze_document(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes documentation content and extracts structured information.
        
        Args:
            content: The documentation content to analyze
            metadata: Metadata about the document like platform, product area
            
        Returns:
            Dictionary containing structured analysis of the document
        """
        analysis_prompt = PromptTemplate.from_template(
            """You are an expert documentation analyzer. Analyze this LikeMinds documentation content and extract:
1. Key concepts and terminology
2. Code examples and their context
3. Relationships with other components
4. Platform-specific considerations
5. Main functionality described
6. Usage patterns

Content: {content}
Metadata: {metadata}

Provide a structured analysis with the following format:

```json
{{
  "key_concepts": ["concept1", "concept2"],
  "code_examples": [
    {{"code": "example1", "language": "language", "context": "description"}}
  ],
  "related_components": ["component1", "component2"],
  "platform_considerations": ["consideration1", "consideration2"],
  "main_functionality": "description",
  "usage_patterns": ["pattern1", "pattern2"]
}}
```

Ensure the output is valid JSON. Only include fields if they're present in the content."""
        )
        
        # Format prompt
        prompt = analysis_prompt.format(
            content=content,
            metadata=json.dumps(metadata)
        )
        
        # Invoke Claude 3.7 Sonnet for analysis using LangChain
        message = HumanMessage(content=prompt)
        response = await self.llm.ainvoke([message])
        response_text = response.content
        
        # Extract the JSON part from the response
        try:
            # Find JSON block using regex
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                result = json.loads(json_str)
            else:
                # Attempt to parse the entire response as JSON if no code block is found
                result = json.loads(response_text)
                
            return result
        except Exception as e:
            # Return a basic structure with error information if parsing fails
            return {
                "error": str(e),
                "raw_response": response_text
            } 