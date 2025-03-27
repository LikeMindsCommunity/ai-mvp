import logging
import json
from typing import Dict, Any, List, Optional, Tuple
import re
from langchain.prompts import PromptTemplate
from ..utils.llm_client import get_llm_client
from .base_agent import BaseAgent
from .agent_communication import AgentCommunication

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CodeRequirementsAnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing user requirements and extracting
    structured information for code generation.
    """
    
    def __init__(self, name: str = "requirements_analysis"):
        """
        Initialize the Requirements Analysis Agent.
        
        Args:
            name: Name for this agent instance
        """
        super().__init__(name)
        self.communication = AgentCommunication(self.id)
        self.llm_client = get_llm_client()
        
        # Register message handlers
        self.communication.register_handler("analyze_requirements", self._handle_analyze_requirements)
        
        # Initialize prompt templates
        self._init_prompts()
        
        self.logger.info("Requirements Analysis Agent initialized")
    
    def _init_prompts(self):
        """Initialize prompt templates used by this agent."""
        self.requirements_analysis_prompt = PromptTemplate(
            input_variables=["requirements", "sdk_info"],
            template="""
You are a technical requirements analyzer specializing in SDK integration. 
Your task is to analyze user requirements and extract structured information for code generation.

# SDK Context Information:
{sdk_info}

# User Requirements:
{requirements}

Please analyze these requirements and extract the following information:
1. Platform - Detect which platform(s) the integration is targeting (React Native, iOS, Android, Flutter)
2. SDK Components - Identify which SDK components will be needed for implementation
3. Customization Needs - Detect any customization requirements
4. Dependencies - Identify any external dependencies or libraries needed

Provide your analysis in the following JSON format:
```json
{{
  "platforms": ["platform1", "platform2"], 
  "sdk_components": [
    {{
      "name": "component_name",
      "purpose": "What this component will be used for",
      "config_options": {{"option1": "value1", "option2": "value2"}}
    }}
  ],
  "customization_needs": [
    {{
      "feature": "feature_name",
      "description": "Description of what needs to be customized",
      "complexity": "low|medium|high"
    }}
  ],
  "dependencies": [
    {{
      "name": "dependency_name",
      "purpose": "Why this dependency is needed",
      "version_constraints": "Version requirements if any"
    }}
  ],
  "requirements_summary": "A brief summary of the core requirements",
  "integration_approach": "Suggested high-level approach for integration"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.platform_detection_prompt = PromptTemplate(
            input_variables=["requirements"],
            template="""
Analyze the following user requirements and determine the platform(s) the user is targeting for SDK integration.

User Requirements:
{requirements}

First, identify any explicit mentions of platforms (React Native, iOS, Android, Flutter, Web).
Second, look for indirect clues about the platform (like mentioning specific frameworks, file types, or development environments).

Output your analysis as JSON:
```json
{{
  "platforms": ["platform1", "platform2"],
  "confidence": 0.85,  # A number between 0 and 1 indicating confidence level
  "explicit_mentions": true/false,  # Whether platforms were explicitly mentioned
  "reasoning": "Brief explanation of your reasoning"
}}
```

Your response should only contain this valid JSON with no additional text or markdown.
"""
        )
    
    async def _execute(self, requirements: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze requirements and extract structured information.
        
        Args:
            requirements: The user's requirements as a string
            context: Optional additional context
            
        Returns:
            Structured analysis of the requirements
        """
        context = context or {}
        
        # Step 1: Detect platforms
        platform_info = await self._detect_platforms(requirements)
        self.logger.info(f"Detected platforms: {platform_info['platforms']}")
        
        # Step 2: Retrieve relevant SDK information based on platforms
        sdk_info = await self._get_sdk_info(platform_info['platforms'])
        
        # Step 3: Perform comprehensive analysis
        analysis = await self._analyze_requirements(requirements, sdk_info)
        
        # Step 4: Validate the analysis
        validated_analysis = self._validate_analysis(analysis)
        
        # Update agent state with the analysis results
        self.set_state("latest_analysis", validated_analysis)
        self.set_state("detected_platforms", platform_info['platforms'])
        
        return validated_analysis
    
    async def _detect_platforms(self, requirements: str) -> Dict[str, Any]:
        """
        Detect which platform(s) the integration is targeting.
        
        Args:
            requirements: User requirements
            
        Returns:
            Platform detection information
        """
        self.logger.info("Detecting platforms from requirements")
        
        try:
            # Prepare the prompt
            prompt = self.platform_detection_prompt.format(requirements=requirements)
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response)
                self.logger.info(f"Platform detection completed: {result['platforms']}")
                return result
            except json.JSONDecodeError:
                self.logger.error("Failed to parse platform detection response as JSON")
                # Fallback to simple regex-based detection
                return self._fallback_platform_detection(requirements)
                
        except Exception as e:
            self.logger.error(f"Error in platform detection: {str(e)}", exc_info=True)
            return self._fallback_platform_detection(requirements)
    
    def _fallback_platform_detection(self, requirements: str) -> Dict[str, Any]:
        """
        Fallback method for platform detection using regex patterns.
        
        Args:
            requirements: User requirements
            
        Returns:
            Platform detection information
        """
        platforms = []
        text = requirements.lower()
        
        # Simple regex-based detection
        if re.search(r'\breact.?native\b', text):
            platforms.append("React Native")
        if re.search(r'\bios\b|\bswift\b|\bobjective.?c\b|\bxcode\b', text):
            platforms.append("iOS")
        if re.search(r'\bandroid\b|\bkotlin\b|\bjava\b|\bandroid studio\b', text):
            platforms.append("Android")
        if re.search(r'\bflutter\b|\bdart\b', text):
            platforms.append("Flutter")
        if re.search(r'\bweb\b|\bjavascript\b|\bhtml\b|\bcss\b|\breact\b|\bangular\b|\bvue\b', text) and not re.search(r'\breact.?native\b', text):
            platforms.append("Web")
        
        # If no platform detected, default to React Native (our primary focus)
        if not platforms:
            platforms = ["React Native"]
            
        return {
            "platforms": platforms,
            "confidence": 0.6,
            "explicit_mentions": bool(platforms),
            "reasoning": "Fallback detection using keyword matching"
        }
    
    async def _get_sdk_info(self, platforms: List[str]) -> str:
        """
        Retrieve relevant SDK information based on detected platforms.
        
        Args:
            platforms: List of detected platforms
            
        Returns:
            SDK information as a string
        """
        # This would typically fetch from a database or knowledge base
        # For now, we'll return some static information based on platforms
        
        platform_info = {
            "React Native": "LikeMinds Chat SDK for React Native supports real-time messaging, media sharing, and customizable UI components.",
            "iOS": "LikeMinds Chat SDK for iOS provides native Swift implementation with UIKit components.",
            "Android": "LikeMinds Chat SDK for Android offers Kotlin/Java APIs with Material Design components.",
            "Flutter": "LikeMinds Chat SDK for Flutter enables cross-platform development with consistent APIs.",
            "Web": "LikeMinds Chat SDK for Web supports modern browsers with React components."
        }
        
        # Get SDK info for each detected platform
        sdk_info = "\n\n".join([platform_info.get(platform, "Information not available") for platform in platforms])
        
        # Add general SDK information
        sdk_info += """
        
General SDK Features:
- Real-time messaging with typing indicators
- Media sharing (images, videos, files)
- Group conversations and channels
- User presence indicators
- Read receipts
- Push notifications
- End-to-end encryption
- Custom message types
- Reaction support
- Thread replies
- User profiles and avatars
"""
        
        return sdk_info
    
    async def _analyze_requirements(self, requirements: str, sdk_info: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of requirements.
        
        Args:
            requirements: User requirements
            sdk_info: SDK information
            
        Returns:
            Structured analysis of requirements
        """
        self.logger.info("Performing comprehensive requirements analysis")
        
        # Prepare the prompt
        prompt = self.requirements_analysis_prompt.format(
            requirements=requirements,
            sdk_info=sdk_info
        )
        
        try:
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response)
                self.logger.info("Requirements analysis completed successfully")
                return result
            except json.JSONDecodeError:
                self.logger.error("Failed to parse requirements analysis response as JSON")
                # Extract JSON from text (in case there's markdown or other text)
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group(1))
                        self.logger.info("Extracted JSON from response")
                        return result
                    except json.JSONDecodeError:
                        self.logger.error("Failed to parse extracted JSON")
                        
                # Return a minimal fallback result
                return self._create_fallback_analysis(requirements)
                
        except Exception as e:
            self.logger.error(f"Error in requirements analysis: {str(e)}", exc_info=True)
            return self._create_fallback_analysis(requirements)
    
    def _create_fallback_analysis(self, requirements: str) -> Dict[str, Any]:
        """
        Create a minimal fallback analysis when the LLM fails.
        
        Args:
            requirements: User requirements
            
        Returns:
            Basic analysis structure
        """
        return {
            "platforms": ["React Native"],  # Default to React Native
            "sdk_components": [
                {
                    "name": "ChatUI",
                    "purpose": "Basic chat interface",
                    "config_options": {}
                }
            ],
            "customization_needs": [],
            "dependencies": [],
            "requirements_summary": "Implement basic chat functionality.",
            "integration_approach": "Standard SDK integration"
        }
    
    def _validate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean up the analysis results.
        
        Args:
            analysis: Raw analysis from LLM
            
        Returns:
            Validated and cleaned analysis
        """
        # Ensure all required fields are present
        required_fields = [
            "platforms", 
            "sdk_components", 
            "customization_needs", 
            "dependencies",
            "requirements_summary",
            "integration_approach"
        ]
        
        for field in required_fields:
            if field not in analysis:
                analysis[field] = [] if field in ["platforms", "sdk_components", "customization_needs", "dependencies"] else ""
        
        # Ensure platforms is a list
        if not isinstance(analysis["platforms"], list):
            analysis["platforms"] = [analysis["platforms"]] if analysis["platforms"] else ["React Native"]
        
        # Normalize platform names
        platform_mapping = {
            "reactnative": "React Native",
            "react-native": "React Native",
            "react native": "React Native",
            "rn": "React Native",
            "ios": "iOS",
            "android": "Android",
            "flutter": "Flutter",
            "web": "Web"
        }
        
        analysis["platforms"] = [
            platform_mapping.get(p.lower().replace(" ", ""), p)
            for p in analysis["platforms"]
        ]
        
        # Add timestamps
        analysis["timestamp"] = __import__('datetime').datetime.utcnow().isoformat()
        
        return analysis
    
    async def _handle_analyze_requirements(self, message):
        """
        Handle analyze_requirements messages from other agents.
        
        Args:
            message: The received message
        """
        try:
            # Extract requirements from message
            requirements = message.content.get("requirements", "")
            context = message.content.get("context", {})
            
            # Analyze requirements
            analysis = await self._execute(requirements, context)
            
            # Send response
            response = message.create_reply({"analysis": analysis})
            await self.communication.broker.publish(response)
            
        except Exception as e:
            self.logger.error(f"Error handling analyze_requirements: {str(e)}", exc_info=True)
            
            # Send error response
            error_response = message.create_reply({
                "error": str(e),
                "message": "Failed to analyze requirements"
            })
            await self.communication.broker.publish(error_response)
    
    def cleanup(self):
        """Clean up resources when the agent is no longer needed."""
        self.communication.cleanup() 