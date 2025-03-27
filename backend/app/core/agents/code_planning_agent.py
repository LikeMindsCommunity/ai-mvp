import logging
import json
import os
from typing import Dict, Any, List, Optional, Tuple
import re
from langchain.prompts import PromptTemplate
from ..utils.llm_client import get_llm_client
from .base_agent import BaseAgent
from .agent_communication import AgentCommunication, Message

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CodePlanningAgent(BaseAgent):
    """
    Agent responsible for creating high-level architecture and implementation
    plans based on analyzed requirements.
    """
    
    def __init__(self, name: str = "code_planning"):
        """
        Initialize the Code Planning Agent.
        
        Args:
            name: Name for this agent instance
        """
        super().__init__(name)
        self.communication = AgentCommunication(self.id)
        self.llm_client = get_llm_client()
        
        # Register message handlers
        self.communication.register_handler("create_plan", self._handle_create_plan)
        
        # Initialize prompt templates
        self._init_prompts()
        
        self.logger.info("Code Planning Agent initialized")
    
    def _init_prompts(self):
        """Initialize prompt templates used by this agent."""
        self.architecture_planning_prompt = PromptTemplate(
            input_variables=["requirements_analysis", "platform", "sdk_info"],
            template="""
You are a software architect specializing in SDK integration. 
Your task is to create a detailed implementation plan based on the analyzed requirements.

# SDK Information:
{sdk_info}

# Requirements Analysis:
{requirements_analysis}

# Target Platform:
{platform}

Please create a detailed architecture plan with the following sections:

1. Component Architecture - Design a component architecture that fulfills these requirements
2. Data Flow - Describe the flow of data between components
3. Implementation Steps - Provide a step-by-step implementation plan
4. File Structure - Suggest a file structure for the implementation
5. Interface Definitions - Define key interfaces/classes with methods and properties
6. Configuration Options - Specify any configuration options needed

Provide your plan in the following JSON format:
```json
{{
  "component_architecture": [
    {{
      "name": "component_name",
      "purpose": "What this component is responsible for",
      "dependencies": ["other_component_names"]
    }}
  ],
  "data_flow": [
    {{
      "from": "source_component",
      "to": "destination_component",
      "data": "What data is being passed",
      "trigger": "What triggers this flow"
    }}
  ],
  "implementation_steps": [
    {{
      "step": 1,
      "description": "Description of what to implement",
      "components": ["affected_components"],
      "dependencies": [0],  // References to previous step numbers (0 means no dependencies)
      "estimated_complexity": "low|medium|high"
    }}
  ],
  "file_structure": [
    {{
      "path": "file/path.extension",
      "purpose": "What this file is for",
      "key_elements": ["Classes/functions to implement"]
    }}
  ],
  "interface_definitions": [
    {{
      "name": "InterfaceName",
      "type": "class|interface|function",
      "description": "Purpose of this interface",
      "methods": [
        {{
          "name": "methodName",
          "parameters": [
            {{ "name": "paramName", "type": "paramType", "description": "param description" }}
          ],
          "return_type": "return type",
          "description": "What this method does"
        }}
      ],
      "properties": [
        {{ "name": "propertyName", "type": "propertyType", "description": "property description" }}
      ]
    }}
  ],
  "configuration_options": [
    {{
      "name": "configOption",
      "type": "optionType",
      "default_value": "defaultValue",
      "description": "What this option configures"
    }}
  ]
}}
```

Ensure your plan is tailored specifically for {platform} platform implementation.
Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.dependency_analysis_prompt = PromptTemplate(
            input_variables=["requirements_analysis", "platform"],
            template="""
Analyze the following requirements and identify all necessary dependencies for implementing the integration on the specified platform.

# Requirements Analysis:
{requirements_analysis}

# Target Platform:
{platform}

Please identify:
1. Required SDK dependencies with versions
2. Third-party libraries needed
3. Development tools required

Format your analysis as JSON:
```json
{{
  "sdk_dependencies": [
    {{
      "name": "dependency_name",
      "version": "^1.0.0",
      "purpose": "What this dependency is used for",
      "installation_command": "npm install dependency_name"
    }}
  ],
  "third_party_libraries": [
    {{
      "name": "library_name",
      "version": "^2.0.0",
      "purpose": "What this library is used for",
      "installation_command": "npm install library_name"
    }}
  ],
  "development_tools": [
    {{
      "name": "tool_name",
      "purpose": "What this tool is used for",
      "setup_instructions": "Brief setup instructions"
    }}
  ]
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
    
    async def _execute(
        self, 
        requirements_analysis: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create architecture and implementation plans based on requirements analysis.
        
        Args:
            requirements_analysis: Analyzed requirements from Requirements Analysis Agent
            context: Optional additional context
            
        Returns:
            Architecture and implementation plans
        """
        context = context or {}
        platforms = requirements_analysis.get("platforms", ["React Native"])
        platform = platforms[0]  # For now, just use the first platform
        
        # Get SDK information for this platform
        sdk_info = self._get_sdk_info_for_platform(platform)
        
        self.logger.info(f"Creating architecture plan for platform: {platform}")
        
        # Step 1: Create architecture plan
        architecture_plan = await self._create_architecture_plan(
            requirements_analysis, 
            platform, 
            sdk_info
        )
        
        # Step 2: Analyze dependencies
        dependencies = await self._analyze_dependencies(requirements_analysis, platform)
        
        # Step 3: Combine results
        complete_plan = {
            **architecture_plan,
            "dependencies": dependencies,
            "platform": platform,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
        
        # Update agent state with the planning results
        self.set_state("latest_plan", complete_plan)
        self.set_state("target_platform", platform)
        
        return complete_plan
    
    def _get_sdk_info_for_platform(self, platform: str) -> str:
        """
        Get detailed SDK information for a specific platform.
        
        Args:
            platform: Target platform
            
        Returns:
            SDK information as a string
        """
        # This would typically fetch from a database or knowledge base
        # For now, we'll return some static information based on platforms
        
        platform_sdk_info = {
            "React Native": """
LikeMinds Chat SDK for React Native:

Core Components:
- ChatClient: Main client for connecting to the LikeMinds service
- Conversation: Represents a chat conversation with multiple users
- Message: Represents a single message within a conversation
- User: Represents a user in the system
- ChatUI: Pre-built UI components for chat interfaces

Key Features:
- Real-time messaging
- Typing indicators
- Read receipts
- Media attachment support
- User presence
- Conversation management
- Push notifications
- Offline support

Installation:
```
npm install @likeminds/chat-rn
```

Basic Integration Steps:
1. Initialize the SDK with your API key
2. Authenticate users
3. Create or join conversations
4. Send and receive messages
5. Display conversations and messages using provided UI components or custom UI
""",
            "iOS": """
LikeMinds Chat SDK for iOS:

Core Components:
- LMChatClient: Main client for connecting to the LikeMinds service
- LMConversation: Represents a chat conversation with multiple users
- LMMessage: Represents a single message within a conversation
- LMUser: Represents a user in the system
- LMChatUI: Pre-built UI components for chat interfaces

Key Features:
- Real-time messaging
- Typing indicators
- Read receipts
- Media attachment support
- User presence
- Conversation management
- Push notifications
- Offline support

Installation:
```
pod 'LikeMindsChat'
```

Basic Integration Steps:
1. Initialize the SDK with your API key
2. Authenticate users
3. Create or join conversations
4. Send and receive messages
5. Display conversations and messages using provided UI components or custom UI
""",
            "Android": """
LikeMinds Chat SDK for Android:

Core Components:
- ChatClient: Main client for connecting to the LikeMinds service
- Conversation: Represents a chat conversation with multiple users
- Message: Represents a single message within a conversation
- User: Represents a user in the system
- ChatUI: Pre-built UI components for chat interfaces

Key Features:
- Real-time messaging
- Typing indicators
- Read receipts
- Media attachment support
- User presence
- Conversation management
- Push notifications
- Offline support

Installation:
```
implementation 'com.likeminds:chat:1.0.0'
```

Basic Integration Steps:
1. Initialize the SDK with your API key
2. Authenticate users
3. Create or join conversations
4. Send and receive messages
5. Display conversations and messages using provided UI components or custom UI
""",
            "Flutter": """
LikeMinds Chat SDK for Flutter:

Core Components:
- ChatClient: Main client for connecting to the LikeMinds service
- Conversation: Represents a chat conversation with multiple users
- Message: Represents a single message within a conversation
- User: Represents a user in the system
- ChatUI: Pre-built UI components for chat interfaces

Key Features:
- Real-time messaging
- Typing indicators
- Read receipts
- Media attachment support
- User presence
- Conversation management
- Push notifications
- Offline support

Installation:
```
flutter pub add likeminds_chat
```

Basic Integration Steps:
1. Initialize the SDK with your API key
2. Authenticate users
3. Create or join conversations
4. Send and receive messages
5. Display conversations and messages using provided UI components or custom UI
"""
        }
        
        return platform_sdk_info.get(platform, "Information not available for this platform")
    
    async def _create_architecture_plan(
        self, 
        requirements_analysis: Dict[str, Any], 
        platform: str, 
        sdk_info: str
    ) -> Dict[str, Any]:
        """
        Create a detailed architecture plan.
        
        Args:
            requirements_analysis: Analyzed requirements
            platform: Target platform
            sdk_info: SDK information
            
        Returns:
            Architecture plan
        """
        self.logger.info("Creating architecture plan")
        
        # Convert requirements analysis to string if it's a dict
        if isinstance(requirements_analysis, dict):
            requirements_analysis_str = json.dumps(requirements_analysis, indent=2)
        else:
            requirements_analysis_str = str(requirements_analysis)
        
        # Prepare the prompt
        prompt = self.architecture_planning_prompt.format(
            requirements_analysis=requirements_analysis_str,
            platform=platform,
            sdk_info=sdk_info
        )
        
        try:
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response)
                self.logger.info("Architecture plan created successfully")
                return result
            except json.JSONDecodeError:
                self.logger.error("Failed to parse architecture plan response as JSON")
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
                return self._create_fallback_architecture_plan(platform)
                
        except Exception as e:
            self.logger.error(f"Error in architecture planning: {str(e)}", exc_info=True)
            return self._create_fallback_architecture_plan(platform)
    
    def _create_fallback_architecture_plan(self, platform: str) -> Dict[str, Any]:
        """
        Create a minimal fallback architecture plan when the LLM fails.
        
        Args:
            platform: Target platform
            
        Returns:
            Basic architecture plan
        """
        return {
            "component_architecture": [
                {
                    "name": "ChatClient",
                    "purpose": "Main client for connecting to the LikeMinds service",
                    "dependencies": []
                },
                {
                    "name": "ChatUI",
                    "purpose": "UI components for displaying chat interfaces",
                    "dependencies": ["ChatClient"]
                }
            ],
            "data_flow": [
                {
                    "from": "User",
                    "to": "ChatClient",
                    "data": "Authentication credentials",
                    "trigger": "App initialization"
                },
                {
                    "from": "ChatClient",
                    "to": "ChatUI",
                    "data": "Message data",
                    "trigger": "New message received"
                }
            ],
            "implementation_steps": [
                {
                    "step": 1,
                    "description": "Initialize the SDK",
                    "components": ["ChatClient"],
                    "dependencies": [0],
                    "estimated_complexity": "low"
                },
                {
                    "step": 2,
                    "description": "Implement user authentication",
                    "components": ["ChatClient"],
                    "dependencies": [1],
                    "estimated_complexity": "medium"
                },
                {
                    "step": 3,
                    "description": "Implement chat UI",
                    "components": ["ChatUI"],
                    "dependencies": [2],
                    "estimated_complexity": "medium"
                }
            ],
            "file_structure": [
                {
                    "path": "ChatClient.js",
                    "purpose": "Main client implementation",
                    "key_elements": ["initializeSDK", "authenticateUser", "sendMessage", "receiveMessage"]
                },
                {
                    "path": "ChatUI.js",
                    "purpose": "UI components",
                    "key_elements": ["ConversationList", "MessageList", "MessageInput"]
                }
            ],
            "interface_definitions": [
                {
                    "name": "ChatClient",
                    "type": "class",
                    "description": "Main client for the LikeMinds service",
                    "methods": [
                        {
                            "name": "initialize",
                            "parameters": [
                                {"name": "apiKey", "type": "string", "description": "Your API key"}
                            ],
                            "return_type": "Promise<void>",
                            "description": "Initializes the SDK"
                        }
                    ],
                    "properties": []
                }
            ],
            "configuration_options": [
                {
                    "name": "apiKey",
                    "type": "string",
                    "default_value": "",
                    "description": "Your LikeMinds API key"
                }
            ]
        }
    
    async def _analyze_dependencies(
        self, 
        requirements_analysis: Dict[str, Any], 
        platform: str
    ) -> Dict[str, Any]:
        """
        Analyze dependencies needed for implementation.
        
        Args:
            requirements_analysis: Analyzed requirements
            platform: Target platform
            
        Returns:
            Dependency analysis
        """
        self.logger.info("Analyzing dependencies")
        
        # Convert requirements analysis to string if it's a dict
        if isinstance(requirements_analysis, dict):
            requirements_analysis_str = json.dumps(requirements_analysis, indent=2)
        else:
            requirements_analysis_str = str(requirements_analysis)
        
        # Prepare the prompt
        prompt = self.dependency_analysis_prompt.format(
            requirements_analysis=requirements_analysis_str,
            platform=platform
        )
        
        try:
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response)
                self.logger.info("Dependency analysis completed successfully")
                return result
            except json.JSONDecodeError:
                self.logger.error("Failed to parse dependency analysis response as JSON")
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
                return self._create_fallback_dependency_analysis(platform)
                
        except Exception as e:
            self.logger.error(f"Error in dependency analysis: {str(e)}", exc_info=True)
            return self._create_fallback_dependency_analysis(platform)
    
    def _create_fallback_dependency_analysis(self, platform: str) -> Dict[str, Any]:
        """
        Create a minimal fallback dependency analysis when the LLM fails.
        
        Args:
            platform: Target platform
            
        Returns:
            Basic dependency analysis
        """
        if platform == "React Native":
            return {
                "sdk_dependencies": [
                    {
                        "name": "@likeminds/chat-rn",
                        "version": "^1.0.0",
                        "purpose": "LikeMinds Chat SDK for React Native",
                        "installation_command": "npm install @likeminds/chat-rn"
                    }
                ],
                "third_party_libraries": [],
                "development_tools": [
                    {
                        "name": "react-native-cli",
                        "purpose": "Command-line tools for React Native development",
                        "setup_instructions": "npm install -g react-native-cli"
                    }
                ]
            }
        elif platform == "iOS":
            return {
                "sdk_dependencies": [
                    {
                        "name": "LikeMindsChat",
                        "version": "~> 1.0",
                        "purpose": "LikeMinds Chat SDK for iOS",
                        "installation_command": "pod 'LikeMindsChat'"
                    }
                ],
                "third_party_libraries": [],
                "development_tools": [
                    {
                        "name": "CocoaPods",
                        "purpose": "Dependency manager for Swift and Objective-C",
                        "setup_instructions": "gem install cocoapods"
                    }
                ]
            }
        elif platform == "Android":
            return {
                "sdk_dependencies": [
                    {
                        "name": "com.likeminds:chat",
                        "version": "1.0.0",
                        "purpose": "LikeMinds Chat SDK for Android",
                        "installation_command": "implementation 'com.likeminds:chat:1.0.0'"
                    }
                ],
                "third_party_libraries": [],
                "development_tools": [
                    {
                        "name": "Android Studio",
                        "purpose": "IDE for Android development",
                        "setup_instructions": "Download from https://developer.android.com/studio"
                    }
                ]
            }
        elif platform == "Flutter":
            return {
                "sdk_dependencies": [
                    {
                        "name": "likeminds_chat",
                        "version": "^1.0.0",
                        "purpose": "LikeMinds Chat SDK for Flutter",
                        "installation_command": "flutter pub add likeminds_chat"
                    }
                ],
                "third_party_libraries": [],
                "development_tools": [
                    {
                        "name": "Flutter SDK",
                        "purpose": "SDK for Flutter development",
                        "setup_instructions": "Download from https://flutter.dev/docs/get-started/install"
                    }
                ]
            }
        else:
            return {
                "sdk_dependencies": [],
                "third_party_libraries": [],
                "development_tools": []
            }
    
    async def _handle_create_plan(self, message: Message):
        """
        Handle create_plan messages from other agents.
        
        Args:
            message: The received message
        """
        try:
            # Extract requirements analysis from message
            requirements_analysis = message.content.get("requirements_analysis", {})
            context = message.content.get("context", {})
            
            # Create plan
            plan = await self._execute(requirements_analysis, context)
            
            # Send response
            response = message.create_reply({"plan": plan})
            await self.communication.broker.publish(response)
            
        except Exception as e:
            self.logger.error(f"Error handling create_plan: {str(e)}", exc_info=True)
            
            # Send error response
            error_response = message.create_reply({
                "error": str(e),
                "message": "Failed to create plan"
            })
            await self.communication.broker.publish(error_response)
    
    def cleanup(self):
        """Clean up resources when the agent is no longer needed."""
        self.communication.cleanup() 