"""
Query Understanding Agent.

This agent analyzes user queries to understand intent and extract key information.
"""

import logging
import asyncio
import json
from typing import Dict, Any, List, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class QueryUnderstandingAgent:
    """
    Agent that analyzes user queries to understand intent and extract key information.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Query Understanding Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = ChatAnthropic(model=model_name)
        self.prompt = PromptTemplate(
            template="""
            # Query Understanding Agent for LikeMinds SDK

            You are an expert AI assistant specializing in understanding developer queries related to LikeMinds SDK integration. Your purpose is to accurately parse and analyze user questions about implementing chat and feed functionality using the LikeMinds SDK across multiple platforms.

            ## Input Query Analysis
            Analyze the following user query:
            
            ```
            {query}
            ```

            ## Conversation Context
            Previous messages that may provide additional context:
            ```
            {conversation_history}
            ```

            ## Project Context
            Current project information that may be relevant:
            ```
            {project_context}
            ```

            ## Analysis Instructions
            Perform a comprehensive analysis of the query with special attention to LikeMinds SDK specifics:

            1. **Primary Intent**: What is the developer trying to accomplish with the LikeMinds SDK?
            - Implement new feature
            - Customizing existing implementation
            - Troubleshooting integration
            - Understanding capabilities
            - Migrate from another solution

            2. **SDK Components**: Identify which parts of the LikeMinds SDK are relevant
            - Chat SDK
            - Feed SDK
            - Authentication components
            - UI elements
            - Backend integration points

            3. **Platform Target**: Determine which platform(s) the developer is working with
            - Android (Kotlin/Java)
            - iOS (Swift)
            - React Native
            - React (Web)
            - Flutter
            - Other/unspecified

            4. **Integration Phase**: Assess where the developer is in their integration journey
            - Initial exploration
            - Starting implementation
            - Modifying existing implementation
            - Debugging issues
            - Optimizing performance

            5. **Technical Constraints**: Identify any technical limitations or requirements
            - Version compatibility
            - UI customization needs
            - Authentication requirements
            - Performance considerations
            - Data management requirements

            6. **Query Type Classification**:
            - Implementation guidance
            - Code example request
            - Configuration question
            - Troubleshooting help
            - Capability exploration
            - Best practices inquiry

            ## Output Format
            Provide your analysis as a structured JSON object with the following fields:

            ```json
            {
            "intent": {
                "primary": "string",
                "secondary": "string",
                "action_items": ["string"]
            },
            "sdk_components": {
                "primary": "string",
                "related": ["string"]
            },
            "platform": {
                "primary": "string",
                "alternatives": ["string"]
            },
            "integration_phase": "string",
            "technical_requirements": {
                "constraints": ["string"],
                "customization_needs": ["string"]
            },
            "query_type": "string",
            "complexity_level": "simple|moderate|complex",
            "confidence_score": 0.0,
            "ambiguities": ["string"],
            "recommended_approach": "string"
            }
            ```

            Be precise and nuanced in your analysis. If details are ambiguous, indicate this in the "ambiguities" field rather than making assumptions. Pay special attention to platform-specific nuances in SDK implementation. Your analysis will be used to route the query to appropriate documentation and code generation services.
            """,
            input_variables=["query", "conversation_history", "project_context"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        # Define expected schema for validation
        self.expected_schema = {
            "intent": {"primary", "secondary", "action_items"},
            "sdk_components": {"primary", "related"},
            "platform": {"primary", "alternatives"},
            "integration_phase": str,
            "technical_requirements": {"constraints", "customization_needs"},
            "query_type": str,
            "complexity_level": str,
            "confidence_score": float,
            "ambiguities": list,
            "recommended_approach": str
        }
    
    def _validate_schema(self, data: Dict[str, Any]) -> bool:
        """
        Validate the response against the expected schema.
        
        Args:
            data: The parsed JSON response from the LLM
            
        Returns:
            True if the schema is valid, False otherwise
        """
        try:
            # Check top-level keys
            for key in ["intent", "sdk_components", "platform", "integration_phase", 
                       "technical_requirements", "query_type", "complexity_level", 
                       "confidence_score", "ambiguities", "recommended_approach"]:
                if key not in data:
                    logger.warning(f"Missing required key in response: {key}")
                    return False
            
            # Check nested structure for intent
            if not all(k in data["intent"] for k in ["primary", "secondary", "action_items"]):
                logger.warning("Invalid intent structure in response")
                return False
                
            # Check nested structure for sdk_components
            if not all(k in data["sdk_components"] for k in ["primary", "related"]):
                logger.warning("Invalid sdk_components structure in response")
                return False
                
            # Check nested structure for platform
            if not all(k in data["platform"] for k in ["primary", "alternatives"]):
                logger.warning("Invalid platform structure in response")
                return False
                
            # Check nested structure for technical_requirements
            if not all(k in data["technical_requirements"] for k in ["constraints", "customization_needs"]):
                logger.warning("Invalid technical_requirements structure in response")
                return False
                
            # Check types for known fields
            if not isinstance(data["confidence_score"], (int, float)):
                logger.warning("confidence_score is not a number")
                return False
                
            if not isinstance(data["ambiguities"], list):
                logger.warning("ambiguities is not a list")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Schema validation error: {str(e)}")
            return False
    
    @trace("query_understanding_agent.analyze")
    async def analyze(
        self, 
        query: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        project_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a user query to understand intent and extract key information.
        
        Args:
            query: The user's query text
            conversation_history: Optional previous conversation messages
            project_context: Optional context about the user's project
            
        Returns:
            A dictionary containing the analysis results
        """
        try:
            # Input validation
            if not query or len(query.strip()) == 0:
                logger.error("Empty query provided")
                return {
                    "intent": {
                        "primary": "error",
                        "secondary": "",
                        "action_items": []
                    },
                    "sdk_components": {
                        "primary": "",
                        "related": []
                    },
                    "platform": {
                        "primary": "",
                        "alternatives": []
                    },
                    "integration_phase": "error",
                    "technical_requirements": {
                        "constraints": [],
                        "customization_needs": []
                    },
                    "query_type": "error",
                    "complexity_level": "unknown",
                    "confidence_score": 0.0,
                    "ambiguities": ["Empty query provided"],
                    "recommended_approach": "Provide a specific question about the LikeMinds SDK",
                    "error": "Query cannot be empty"
                }

            # Check for overly long inputs to prevent token overflow
            if len(query) > 4000:
                logger.warning(f"Query exceeds recommended length: {len(query)} chars")
                query = query[:4000] + "... [truncated due to length]"
            
            # Format conversation history for the prompt
            formatted_history = ""
            if conversation_history:
                # Limit conversation history to prevent token overflow
                limited_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
                formatted_history = "\n".join([
                    f"User: {msg.get('user', '')}\nAssistant: {msg.get('assistant', '')}"
                    for msg in limited_history
                ])
            
            # Format project context
            formatted_project = ""
            if project_context:
                # More structured handling of project context
                if isinstance(project_context, dict):
                    formatted_lines = []
                    for key, value in project_context.items():
                        if isinstance(value, dict):
                            formatted_lines.append(f"{key}:")
                            for sub_key, sub_value in value.items():
                                formatted_lines.append(f"  {sub_key}: {sub_value}")
                        else:
                            formatted_lines.append(f"{key}: {value}")
                    formatted_project = "\n".join(formatted_lines)
                else:
                    formatted_project = str(project_context)
            
            # Execute the chain with timeout handling
            with monitor("query_understanding_agent.analyze", {"query_length": len(query)}):
                try:
                    result = await asyncio.wait_for(
                        self.chain.arun(
                            query=query,
                            conversation_history=formatted_history,
                            project_context=formatted_project
                        ),
                        timeout=15.0  # 15-second timeout
                    )
                except asyncio.TimeoutError:
                    logger.error("LLM query analysis timed out")
                    return {
                        "intent": {
                            "primary": "error",
                            "secondary": "",
                            "action_items": []
                        },
                        "sdk_components": {
                            "primary": "",
                            "related": []
                        },
                        "platform": {
                            "primary": "",
                            "alternatives": []
                        },
                        "integration_phase": "error",
                        "technical_requirements": {
                            "constraints": [],
                            "customization_needs": []
                        },
                        "query_type": "error",
                        "complexity_level": "unknown",
                        "confidence_score": 0.0,
                        "ambiguities": ["Analysis timed out"],
                        "recommended_approach": "Try again with a simpler query or contact support",
                        "error": "Request timed out"
                    }
            
            # Process and return the result
            try:
                parsed_result = json.loads(result)
                
                # Validate the schema
                if not self._validate_schema(parsed_result):
                    logger.warning("LLM response failed schema validation")
                    parsed_result["schema_validation"] = False
                    
                    # Check confidence threshold
                    if parsed_result.get("confidence_score", 0) < 0.4:
                        parsed_result["ambiguities"] = parsed_result.get("ambiguities", []) + ["Low confidence in analysis"]
                        
                return parsed_result
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM output as JSON: {result}")
                # Fallback to a basic structure if parsing fails
                return {
                    "intent": {
                        "primary": "unknown",
                        "secondary": "",
                        "action_items": []
                    },
                    "sdk_components": {
                        "primary": "",
                        "related": []
                    },
                    "platform": {
                        "primary": "",
                        "alternatives": []
                    },
                    "integration_phase": "unknown",
                    "technical_requirements": {
                        "constraints": [],
                        "customization_needs": []
                    },
                    "query_type": "unknown",
                    "complexity_level": "moderate",
                    "confidence_score": 0.5,
                    "ambiguities": ["Failed to parse LLM output as JSON"],
                    "recommended_approach": "Retry with more specific query",
                    "raw_output": result
                }
                
        except Exception as e:
            logger.error(f"Error in query understanding agent: {str(e)}", exc_info=True)
            return {
                "intent": {
                    "primary": "error",
                    "secondary": "",
                    "action_items": []
                },
                "sdk_components": {
                    "primary": "",
                    "related": []
                },
                "platform": {
                    "primary": "",
                    "alternatives": []
                },
                "integration_phase": "error",
                "technical_requirements": {
                    "constraints": [],
                    "customization_needs": []
                },
                "query_type": "error",
                "complexity_level": "unknown",
                "confidence_score": 0.0,
                "ambiguities": [f"Error processing query: {str(e)}"],
                "recommended_approach": "Retry or contact support",
                "error": str(e)
            }