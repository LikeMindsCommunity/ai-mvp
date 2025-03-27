import logging
import json
import os
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from langchain.prompts import PromptTemplate
from ..utils.llm_client import get_llm_client
from .base_agent import BaseAgent
from .agent_communication import AgentCommunication, Message

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CodeGenerationAgent(BaseAgent):
    """
    Agent responsible for generating code based on requirements analysis
    and architecture planning. Generates production-ready implementation
    for SDK integration.
    """
    
    def __init__(self, name: str = "code_generation"):
        """
        Initialize the Code Generation Agent.
        
        Args:
            name: Name for this agent instance
        """
        super().__init__(name)
        self.communication = AgentCommunication(self.id)
        self.llm_client = get_llm_client()
        
        # Register message handlers
        self.communication.register_handler("generate_code", self._handle_generate_code)
        
        # Initialize prompt templates
        self._init_prompts()
        
        # Cache for generated code
        self.generated_code_cache = {}
        
        self.logger.info("Code Generation Agent initialized")
    
    def _init_prompts(self):
        """Initialize prompt templates used by this agent."""
        self.code_generation_prompt = PromptTemplate(
            input_variables=["architecture_plan", "file_details", "platform", "sdk_info"],
            template="""
You are an expert software developer specializing in SDK integration.
Your task is to generate high-quality production-ready code for a specific file based on the architecture plan.

# SDK Information:
{sdk_info}

# Architecture Plan:
{architecture_plan}

# File to Implement:
{file_details}

# Target Platform:
{platform}

Please generate the complete code implementation for this file. Your code should:
1. Follow best practices for {platform} development
2. Include proper error handling
3. Be well-documented with comments
4. Implement all required functionality described in the architecture plan
5. Be ready for production use

Your response should only contain the code, without any explanations or markdown formatting.
Do not include backticks or language tags - only provide the actual code that would go in the file.
"""
        )
        
        self.template_selection_prompt = PromptTemplate(
            input_variables=["file_path", "file_purpose", "platform"],
            template="""
Given a file that needs to be generated, select the most appropriate template as a starting point.

# File Path:
{file_path}

# File Purpose:
{file_purpose}

# Target Platform:
{platform}

Select the most appropriate template from the following options:
1. Basic Component
2. Service/Client
3. API Integration
4. UI Component
5. Utility/Helper
6. Configuration
7. Custom Hook
8. Custom Type Definitions
9. No template (generate from scratch)

Respond with only the number of the selected template. For example: "2"
"""
        )
        
        self.code_documentation_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
Generate comprehensive documentation for the provided code.

# Code:
{code}

# File Path:
{file_path}

# Target Platform:
{platform}

Please provide:
1. A detailed file header comment describing the purpose and functionality of this file
2. Function/method documentation where missing
3. Complex logic explanation where needed

Your response should only contain the documented code, without any explanations or markdown formatting.
Do not include backticks or language tags - only provide the actual code that would go in the file.
"""
        )
        
        self.error_handling_prompt = PromptTemplate(
            input_variables=["code", "platform"],
            template="""
Enhance the provided code with proper error handling following best practices for {platform}.

# Code:
{code}

# Target Platform:
{platform}

Add appropriate error handling to the code:
1. Add try/catch blocks where necessary
2. Handle potential errors in API calls, file operations, etc.
3. Implement proper error logging and user feedback
4. Consider edge cases

Your response should only contain the enhanced code, without any explanations or markdown formatting.
Do not include backticks or language tags - only provide the actual code that would go in the file.
"""
        )
    
    def _get_platform_templates(self, platform: str) -> Dict[str, str]:
        """
        Get code templates for a specific platform.
        
        Args:
            platform: Target platform
            
        Returns:
            Dictionary of template names to template content
        """
        # In a real implementation, these would be loaded from files
        # For now, we'll just return some basic templates
        
        if platform == "React Native":
            return {
                "Basic Component": """
import React from 'react';
import { View, Text } from 'react-native';

/**
 * ComponentName - Description of the component
 * 
 * @param {Object} props - Component props
 * @returns {React.ReactElement} The rendered component
 */
const ComponentName = (props) => {
  return (
    <View>
      <Text>Component Content</Text>
    </View>
  );
};

export default ComponentName;
""",
                "Service/Client": """
/**
 * Service description
 */
class ServiceName {
  /**
   * Initialize the service
   */
  constructor(config = {}) {
    this.config = config;
  }

  /**
   * Method description
   * 
   * @param {Object} params - Method parameters
   * @returns {Promise<Object>} Result description
   */
  async methodName(params) {
    try {
      // Implementation
      return result;
    } catch (error) {
      console.error('Error in methodName:', error);
      throw error;
    }
  }
}

export default ServiceName;
""",
                "API Integration": """
import axios from 'axios';

/**
 * API client for interacting with the service
 */
class ApiClient {
  /**
   * Initialize the API client
   * 
   * @param {Object} config - Configuration options
   */
  constructor(config = {}) {
    this.baseURL = config.baseURL || 'https://api.example.com';
    this.apiKey = config.apiKey;
    
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      }
    });
  }

  /**
   * Make a request to the API
   * 
   * @param {string} method - HTTP method
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request data
   * @returns {Promise<Object>} API response
   */
  async request(method, endpoint, data = null) {
    try {
      const response = await this.client({
        method,
        url: endpoint,
        data: method !== 'get' ? data : undefined,
        params: method === 'get' ? data : undefined
      });
      return response.data;
    } catch (error) {
      console.error(`API Error (${method} ${endpoint}):`, error);
      throw error;
    }
  }
}

export default ApiClient;
""",
                "UI Component": """
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';

/**
 * ComponentName - Description of the component
 * 
 * @param {Object} props - Component props
 * @returns {React.ReactElement} The rendered component
 */
const ComponentName = ({ title, data = [], loading, onItemPress }) => {
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}
      {data.map((item, index) => (
        <View key={index} style={styles.item} onPress={() => onItemPress?.(item)}>
          <Text>{item.name}</Text>
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  item: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#EEEEEE',
  },
});

export default ComponentName;
"""
            }
        elif platform == "iOS":
            return {
                "Basic Component": """
import UIKit

/**
 * ClassName - Description of the class
 */
class ClassName: UIViewController {
    
    // MARK: - Properties
    
    // MARK: - Lifecycle Methods
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }
    
    // MARK: - Setup
    
    private func setupUI() {
        // Setup UI components
    }
    
    // MARK: - Actions
    
    @objc private func buttonTapped() {
        // Handle button tap
    }
}
""",
                "Service/Client": """
import Foundation

/**
 * Service description
 */
class ServiceName {
    
    // MARK: - Properties
    
    private let config: [String: Any]
    
    // MARK: - Initialization
    
    init(config: [String: Any] = [:]) {
        self.config = config
    }
    
    // MARK: - Public Methods
    
    /**
     * Method description
     *
     * - Parameters:
     *   - params: Method parameters
     * - Returns: Result description
     * - Throws: Possible errors
     */
    func methodName(params: [String: Any]) throws -> Any {
        // Implementation
        return result
    }
}
"""
            }
        else:
            # Return some generic templates
            return {
                "Basic Component": """
// Basic component template
// Replace with actual implementation
""",
                "Service/Client": """
// Service client template
// Replace with actual implementation
"""
            }
    
    async def _execute(
        self, 
        requirements_analysis: Dict[str, Any], 
        architecture_plan: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate code based on requirements analysis and architecture plan.
        
        Args:
            requirements_analysis: Analyzed requirements from Requirements Analysis Agent
            architecture_plan: Architecture plan from Code Planning Agent
            context: Optional additional context
            
        Returns:
            Generated code files
        """
        context = context or {}
        platform = architecture_plan.get("platform", "React Native")
        
        # Get SDK information for this platform
        sdk_info = self._get_sdk_info_for_platform(platform)
        
        self.logger.info(f"Generating code for platform: {platform}")
        
        # Get file structure from architecture plan
        file_structure = architecture_plan.get("file_structure", [])
        
        # Generate code for each file
        generated_files = {}
        for file_info in file_structure:
            file_path = file_info.get("path", "")
            if not file_path:
                continue
                
            self.logger.info(f"Generating code for file: {file_path}")
            
            file_code = await self._generate_file_code(
                file_info=file_info,
                architecture_plan=architecture_plan,
                platform=platform,
                sdk_info=sdk_info
            )
            
            # Add error handling
            file_code = await self._add_error_handling(file_code, platform)
            
            # Add documentation
            file_code = await self._add_documentation(file_code, file_path, platform)
            
            # Store the generated code
            generated_files[file_path] = file_code
            
            # Cache the generated code
            self.generated_code_cache[file_path] = {
                "code": file_code,
                "timestamp": datetime.utcnow().isoformat(),
                "platform": platform
            }
        
        # Create a result object
        result = {
            "platform": platform,
            "generated_files": generated_files,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update agent state with the generation results
        self.set_state("latest_generation", result)
        
        return result
    
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
"""
        }
        
        return platform_sdk_info.get(platform, "Information not available for this platform")
    
    async def _generate_file_code(
        self, 
        file_info: Dict[str, Any],
        architecture_plan: Dict[str, Any],
        platform: str,
        sdk_info: str
    ) -> str:
        """
        Generate code for a specific file.
        
        Args:
            file_info: Information about the file to generate
            architecture_plan: Architecture plan
            platform: Target platform
            sdk_info: SDK information
            
        Returns:
            Generated code
        """
        file_path = file_info.get("path", "")
        file_purpose = file_info.get("purpose", "")
        key_elements = file_info.get("key_elements", [])
        
        # Check if we need to use a template
        template_code = await self._select_template(file_path, file_purpose, platform)
        
        # Convert architecture plan to string if it's a dict
        if isinstance(architecture_plan, dict):
            architecture_plan_str = json.dumps(architecture_plan, indent=2)
        else:
            architecture_plan_str = str(architecture_plan)
        
        # Prepare the prompt
        prompt = self.code_generation_prompt.format(
            architecture_plan=architecture_plan_str,
            file_details=json.dumps(file_info, indent=2),
            platform=platform,
            sdk_info=sdk_info
        )
        
        try:
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Clean up the response (remove any markdown code blocks if present)
            code = self._clean_code_response(response)
            
            self.logger.info(f"Generated code for file: {file_path}")
            return code
            
        except Exception as e:
            self.logger.error(f"Error generating code for {file_path}: {str(e)}", exc_info=True)
            return f"// Error generating code: {str(e)}\n" + (template_code or "// Template code not available")
    
    async def _select_template(self, file_path: str, file_purpose: str, platform: str) -> str:
        """
        Select an appropriate template for the file.
        
        Args:
            file_path: Path of the file
            file_purpose: Purpose of the file
            platform: Target platform
            
        Returns:
            Template code or empty string if no template is selected
        """
        try:
            # Get available templates for the platform
            templates = self._get_platform_templates(platform)
            if not templates:
                return ""
            
            # Prepare the prompt
            prompt = self.template_selection_prompt.format(
                file_path=file_path,
                file_purpose=file_purpose,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Extract the template number
            match = re.search(r'(\d+)', response)
            if match:
                template_number = int(match.group(1))
                
                # Map template number to template name
                template_names = list(templates.keys())
                if 1 <= template_number <= len(template_names):
                    template_name = template_names[template_number - 1]
                    return templates.get(template_name, "")
                elif template_number == 9:  # No template
                    return ""
            
            # If template selection fails, use the first template as a fallback
            if templates:
                return next(iter(templates.values()))
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Error selecting template: {str(e)}", exc_info=True)
            return ""
    
    def _clean_code_response(self, response: str) -> str:
        """
        Clean up code response from LLM.
        
        Args:
            response: Response from LLM
            
        Returns:
            Cleaned code
        """
        # Remove markdown code blocks if present
        code_block_match = re.search(r'```(?:\w+)?\s*([\s\S]*?)\s*```', response)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        return response.strip()
    
    async def _add_error_handling(self, code: str, platform: str) -> str:
        """
        Add error handling to generated code.
        
        Args:
            code: Generated code
            platform: Target platform
            
        Returns:
            Code with error handling
        """
        try:
            # Prepare the prompt
            prompt = self.error_handling_prompt.format(
                code=code,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Clean up the response
            enhanced_code = self._clean_code_response(response)
            
            self.logger.info("Added error handling to code")
            return enhanced_code
            
        except Exception as e:
            self.logger.error(f"Error adding error handling: {str(e)}", exc_info=True)
            return code  # Return original code if error handling fails
    
    async def _add_documentation(self, code: str, file_path: str, platform: str) -> str:
        """
        Add documentation to generated code.
        
        Args:
            code: Generated code
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Documented code
        """
        try:
            # Prepare the prompt
            prompt = self.code_documentation_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Clean up the response
            documented_code = self._clean_code_response(response)
            
            self.logger.info(f"Added documentation to {file_path}")
            return documented_code
            
        except Exception as e:
            self.logger.error(f"Error adding documentation: {str(e)}", exc_info=True)
            return code  # Return original code if documentation fails
    
    async def _handle_generate_code(self, message: Message):
        """
        Handle generate_code messages from other agents.
        
        Args:
            message: The received message
        """
        try:
            # Extract data from message
            requirements_analysis = message.content.get("requirements_analysis", {})
            architecture_plan = message.content.get("architecture_plan", {})
            context = message.content.get("context", {})
            
            # Generate code
            code_generation_result = await self._execute(
                requirements_analysis, 
                architecture_plan, 
                context
            )
            
            # Send response
            response = message.create_reply({"generation_result": code_generation_result})
            await self.communication.broker.publish(response)
            
        except Exception as e:
            self.logger.error(f"Error handling generate_code: {str(e)}", exc_info=True)
            
            # Send error response
            error_response = message.create_reply({
                "error": str(e),
                "message": "Failed to generate code"
            })
            await self.communication.broker.publish(error_response)
    
    def cleanup(self):
        """Clean up resources when the agent is no longer needed."""
        self.communication.cleanup() 