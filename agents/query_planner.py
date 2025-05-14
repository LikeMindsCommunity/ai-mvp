"""
Query Planner Agent for understanding user intent and planning approach.
"""

from typing import List, Dict, Any, Optional
import json

from agents.base import BaseAgent
from agno.tools.reasoning import ReasoningTools


class QueryPlannerAgent(BaseAgent):
    """Agent for analyzing user intent and planning the approach to answering."""
    
    def __init__(self, use_claude: bool = False):
        """
        Initialize the query planner agent.
        
        Args:
            use_claude: Whether to use Claude instead of Gemini (recommended for complex reasoning)
        """
        # Define instructions for the agent
        instructions = [
            "You are an expert in understanding Flutter integration queries.",
            "For each user query, analyze the intent and break it down into actionable steps.",
            "Identify which parts of the query require specific documentation or code examples.",
            "Generate a structured plan with relevant keywords to guide information retrieval.",
            "Include specific concepts that should be searched for in Flutter and LikeMinds documentation.",
            "Always format the output as JSON with the following structure: {\"intent\": \"string\", \"keywords\": [\"string\"], \"steps\": [\"string\"], \"required_information\": [\"string\"]}",
        ]
        
        # Initialize the base agent with reasoning tools
        super().__init__(
            use_claude=use_claude,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=instructions,
            markdown=True
        )
    
    def plan_query(self, user_query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Analyze a user query and create a structured plan.
        
        Args:
            user_query: The user's query about Flutter integration
            conversation_history: Optional list of prior conversation turns
            
        Returns:
            A structured plan as a dictionary with keys:
            - intent: The identified user intent
            - keywords: List of relevant keywords to search for
            - steps: List of steps to answer the query
            - required_information: Types of information needed (docs, code, etc.)
        """
        # Combine conversation history if provided
        context = ""
        if conversation_history:
            context = "Previous conversation:\n"
            for turn in conversation_history:
                if "user" in turn:
                    context += f"User: {turn['user']}\n"
                if "assistant" in turn:
                    context += f"Assistant: {turn['assistant']}\n"
            context += "\n"
        
        # Create a fallback plan based on the user query
        fallback_plan = self._create_fallback_plan(user_query)
        
        # Create the full prompt
        prompt = f"{context}Analyze the following user query about Flutter integration:\n\n{user_query}\n\n"
        prompt += "Respond with a JSON object containing:\n"
        prompt += "1. The user's intent\n"
        prompt += "2. Key search terms/keywords\n"
        prompt += "3. Step-by-step plan to address the query\n"
        prompt += "4. Required information types (documentation, code examples, etc.)\n\n"
        prompt += "Format your response as a valid JSON object with this structure:\n"
        prompt += "{\"intent\": \"string\", \"keywords\": [\"string\"], \"steps\": [\"string\"], \"required_information\": [\"string\"]}"
        
        try:
            # Get the response from the agent
            response = self.ask(prompt, stream=False, show_reasoning=False)
            
            # Parse the JSON response
            # Find JSON block in the response, if it's formatted with markdown
            json_text = ""
            if "```json" in response:
                json_text = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_text = response.split("```")[1].split("```")[0].strip()
            else:
                # Try to find anything that looks like JSON
                import re
                json_match = re.search(r'(\{.*\})', response, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)
                else:
                    json_text = response.strip()
            
            if not json_text:
                print("No JSON content found in response, using fallback plan")
                return fallback_plan
                
            plan = json.loads(json_text)
            
            # Ensure all required fields exist
            required_fields = ["intent", "keywords", "steps", "required_information"]
            for field in required_fields:
                if field not in plan:
                    plan[field] = fallback_plan[field]
            
            return plan
            
        except Exception as e:
            print(f"Error parsing plan response: {e}")
            # Return the fallback plan if parsing failed
            return fallback_plan
    
    def _create_fallback_plan(self, user_query: str) -> Dict[str, Any]:
        """Create a fallback plan based on the user query."""
        # Default plan for chat implementation
        if "chat" in user_query.lower() and "likeminds" in user_query.lower():
            return {
                "intent": "Implementing chat feature with LikeMinds SDK in Flutter",
                "keywords": ["LikeMinds", "chat", "Flutter", "implementation", "SDK", "real-time messaging"],
                "steps": [
                    "Install LikeMinds SDK", 
                    "Initialize the SDK", 
                    "Create chat UI", 
                    "Implement chat functionality",
                    "Test the implementation"
                ],
                "required_information": ["documentation", "code_examples", "api_reference"]
            }
        # Generic fallback plan
        else:
            # Extract potential keywords from the query
            keywords = [word for word in user_query.split() if len(word) > 3]
            return {
                "intent": f"Understanding how to use {user_query}",
                "keywords": keywords[:5],  # Take up to 5 keywords
                "steps": ["Research the topic", "Analyze requirements", "Provide solution"],
                "required_information": ["documentation", "code_examples"]
            } 