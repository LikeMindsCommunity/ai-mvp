"""
Code Planning Agent.

This agent creates code architecture and plans based on structured requirements.
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import Anthropic

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class CodePlanningAgent:
    """
    Agent that creates code architecture and plans based on structured requirements.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Code Planning Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = Anthropic(model=model_name)
        self.prompt = PromptTemplate(
            template="""
            # Code Planning Agent for LikeMinds SDK Integration

            ## Role Definition
            You are a senior software architect specializing in mobile and web SDK integration, with deep expertise in the LikeMinds SDK architecture. Your responsibility is to translate structured requirements into detailed, implementable code plans that align with platform-specific best practices.

            ## Input Parameters
            ### Structured Requirements
            ```json
            {requirements}
            ```

            ### Technical Context
            - Platform: {platform}
            - Language: {language}
            - SDK Component: {sdk_component}
            - SDK Version: {sdk_version}

            ### Existing Codebase (if applicable)
            ```
            {existing_code_context}
            ```

            ## Planning Objectives
            Create a comprehensive, production-ready code architecture plan that:
            1. Follows established patterns for the {platform} platform
            2. Implements LikeMinds {sdk_component} SDK features efficiently
            3. Maintains separation of concerns and modular design
            4. Considers existing codebase integration points
            5. Maximizes code reusability and maintainability

            ## Output Structure
            Provide a detailed code plan in JSON format with the following sections:

            ```json
            {
              "architecture_overview": {
                "description": "High-level description of the architecture approach",
                "pattern": "Architectural pattern being used (e.g., MVVM, MVC)",
                "key_considerations": ["List of architectural considerations"]
              },
              "component_structure": [
                {
                  "name": "ComponentName",
                  "type": "Class/Interface/Module",
                  "purpose": "Component's responsibility",
                  "relationships": ["Relationships to other components"],
                  "sdk_integration_points": ["SDK classes/methods this component interacts with"]
                }
              ],
              "data_model": [
                {
                  "name": "ModelName",
                  "properties": [
                    {
                      "name": "propertyName",
                      "type": "dataType",
                      "purpose": "What this property represents"
                    }
                  ],
                  "mapping": "How this maps to SDK models"
                }
              ],
              "implementation_sequence": [
                {
                  "phase": "Phase number and name",
                  "steps": [
                    {
                      "step": "Implementation step",
                      "components": ["Components involved"],
                      "testing_considerations": "How to verify this step"
                    }
                  ],
                  "estimated_effort": "Low/Medium/High"
                }
              ],
              "file_structure": [
                {
                  "path": "path/to/file",
                  "purpose": "File's purpose",
                  "contents": ["Key classes/functions in this file"],
                  "dependencies": ["External dependencies"]
                }
              ],
              "integration_interfaces": [
                {
                  "name": "InterfaceName",
                  "purpose": "Interface purpose",
                  "methods": [
                    {
                      "name": "methodName",
                      "parameters": ["param1: type", "param2: type"],
                      "return_type": "returnType",
                      "purpose": "Method purpose"
                    }
                  ],
                  "sdk_methods_used": ["SDK methods used by this interface"]
                }
              ],
              "configuration_management": {
                "required_settings": [
                  {
                    "name": "Setting name",
                    "purpose": "Setting purpose",
                    "default_value": "Default value",
                    "configuration_location": "Where this is configured"
                  }
                ],
                "initialization_sequence": [
                  "Step-by-step initialization process"
                ]
              },
              "error_handling": {
                "strategy": "Overall error handling approach",
                "error_scenarios": [
                  {
                    "scenario": "Error scenario description",
                    "handling_approach": "How this error is handled"
                  }
                ]
              },
              "performance_considerations": [
                {
                  "area": "Performance-sensitive area",
                  "optimization_strategy": "How to optimize this area"
                }
              ],
              "testing_strategy": {
                "unit_testing": ["Components to unit test"],
                "integration_testing": ["Integration points to test"],
                "ui_testing": ["UI elements to test"]
              }
            }
            ```

            ## Platform-Specific Guidelines

            ### Android
            - Follow Kotlin best practices and Android architecture components
            - Consider Activity/Fragment lifecycle management
            - Use ViewModels for UI-related data handling
            - Implement proper background threading for network operations
            - Follow Material Design guidelines for UI components
            - Consider configuration changes and process death

            ### iOS
            - Follow Swift best practices and Apple Human Interface Guidelines
            - Implement proper memory management
            - Consider view controller lifecycle
            - Use SwiftUI or UIKit appropriately based on requirements
            - Consider background state handling

            ### React Native
            - Balance between native modules and JavaScript implementation
            - Consider cross-platform component design
            - Implement proper event handling between JS and native layers
            - Optimize for both Android and iOS simultaneously

            ### Flutter
            - Utilize widget composition and state management best practices
            - Implement platform channels for native SDK integration
            - Follow proper asset management approaches
            - Consider stateful/stateless widget separation

            ### React (Web)
            - Follow component-based architecture
            - Implement proper state management (Context, Redux, etc.)
            - Consider browser compatibility
            - Optimize for web performance

            ## LikeMinds SDK Integration Considerations
            - Ensure proper SDK initialization at appropriate application lifecycle point
            - Implement user authentication flow according to SDK requirements
            - Handle offline scenarios and data synchronization
            - Implement proper event handling for real-time updates
            - Follow SDK's threading/async patterns
            - Consider pagination and data loading patterns for feeds and chat history

            ## Critical Requirements
            Create a plan that a senior developer can follow to implement a production-quality integration with the LikeMinds SDK. Focus on practical, implementable architecture rather than theoretical patterns. Your plan should be specific to the {platform} platform and {language} language, with clear integration points to the LikeMinds SDK.
            """,
            input_variables=["requirements", "platform", "language", "sdk_component", "sdk_version", "existing_code_context"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    @trace("code_planning_agent.create_plan")
    async def create_plan(
        self,
        requirements: Dict[str, Any],
        platform: str,
        language: str,
        sdk_component: str = "chat",
        sdk_version: str = "latest",
        existing_code_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a code architecture and plan based on structured requirements.
        
        Args:
            requirements: Structured requirements from RequirementAnalysisAgent
            platform: Target platform (e.g., 'android', 'ios', 'react-native')
            language: Programming language to use
            sdk_component: LikeMinds SDK component ('chat' or 'feed')
            sdk_version: Version of the SDK to target
            existing_code_context: Optional context about existing codebase
            
        Returns:
            A dictionary containing the detailed code plan
        """
        try:
            # Format the requirements as a string
            requirements_str = json.dumps(requirements, indent=2)
            
            # Execute the chain
            with monitor("code_planning_agent.create_plan", 
                        {"req_length": len(requirements_str)}):
                result = await self.chain.arun(
                    requirements=requirements_str,
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component,
                    sdk_version=sdk_version,
                    existing_code_context=existing_code_context or "No existing code context provided."
                )
            
            # Process the result
            try:
                parsed_result = json.loads(result)
                return parsed_result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM output as JSON: {result}")
                # Extract structured content if possible
                json_match = re.search(r'```json\n(.*?)\n```', result, re.DOTALL)
                if json_match:
                    try:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    except json.JSONDecodeError:
                        pass
                
                # Fallback to a basic structure
                return {
                    "architecture_overview": {
                        "description": "Error creating code plan",
                        "pattern": "Unknown",
                        "key_considerations": ["Error parsing LLM output"]
                    },
                    "component_structure": [],
                    "data_model": [],
                    "implementation_sequence": [],
                    "file_structure": [],
                    "integration_interfaces": [],
                    "configuration_management": {
                        "required_settings": [],
                        "initialization_sequence": []
                    },
                    "error_handling": {
                        "strategy": "Not specified",
                        "error_scenarios": []
                    },
                    "performance_considerations": [],
                    "testing_strategy": {
                        "unit_testing": [],
                        "integration_testing": [],
                        "ui_testing": []
                    },
                    "raw_output": result
                }
                
        except Exception as e:
            logger.error(f"Error in code planning agent: {str(e)}", exc_info=True)
            return {
                "architecture_overview": {
                    "description": "Error: " + str(e),
                    "pattern": "Error",
                    "key_considerations": ["An error occurred during plan generation"]
                },
                "component_structure": [],
                "data_model": [],
                "implementation_sequence": [],
                "file_structure": [],
                "integration_interfaces": [],
                "error": str(e)
            }
    
    @trace("code_planning_agent.validate_architecture")
    async def validate_architecture(
        self,
        code_plan: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """
        Validate that the architecture plan follows platform best practices.
        
        Args:
            code_plan: The code architecture plan
            platform: Target platform
            
        Returns:
            Validation results with recommendations
        """
        platform_patterns = {
            "android": ["MVVM", "Clean Architecture", "Repository Pattern"],
            "ios": ["MVVM", "Coordinator Pattern", "VIPER"],
            "react-native": ["Component-based", "Redux", "Context API"],
            "flutter": ["BLoC", "Provider", "GetX"],
            "react": ["Component-based", "Redux", "Custom Hooks"]
        }
        
        # Get the architectural pattern from the plan
        architecture_info = code_plan.get("architecture_overview", {})
        pattern = architecture_info.get("pattern", "").lower()
        
        # Check if pattern matches platform recommendations
        platform_specific_patterns = platform_patterns.get(platform.lower(), [])
        pattern_matches = any(recommended.lower() in pattern 
                             for recommended in platform_specific_patterns)
        
        # Validate component structure
        components = code_plan.get("component_structure", [])
        sdk_integration_points_defined = all(
            "sdk_integration_points" in component and component["sdk_integration_points"]
            for component in components if components
        )
        
        # Validate initialization sequence
        config_mgmt = code_plan.get("configuration_management", {})
        has_init_sequence = "initialization_sequence" in config_mgmt and config_mgmt["initialization_sequence"]
        
        # Compile recommendations
        recommendations = []
        
        if not pattern_matches:
            recommendations.append(
                f"Consider using one of the recommended patterns for {platform}: {', '.join(platform_specific_patterns)}"
            )
        
        if not sdk_integration_points_defined:
            recommendations.append(
                "Clearly define SDK integration points for each component that interacts with the LikeMinds SDK"
            )
        
        if not has_init_sequence:
            recommendations.append(
                "Add a detailed SDK initialization sequence to ensure proper setup"
            )
        
        return {
            "is_valid": pattern_matches and sdk_integration_points_defined and has_init_sequence,
            "recommendations": recommendations,
            "architecture_score": sum([
                1 if pattern_matches else 0,
                1 if sdk_integration_points_defined else 0,
                1 if has_init_sequence else 0
            ]) / 3.0  # Normalized score between 0 and 1
        }
    
    @trace("code_planning_agent.estimate_complexity")
    async def estimate_complexity(
        self,
        code_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimate the complexity of implementing the code plan.
        
        Args:
            code_plan: The code plan generated by this agent
            
        Returns:
            A dictionary with complexity metrics
        """
        # Calculate complexity metrics
        component_count = len(code_plan.get("component_structure", []))
        file_count = len(code_plan.get("file_structure", []))
        
        # Get implementation sequence for better estimation
        implementation_sequence = code_plan.get("implementation_sequence", [])
        implementation_steps = sum(len(phase.get("steps", [])) for phase in implementation_sequence) if implementation_sequence else 0
        
        # Calculate effort based on implementation sequence if available
        if implementation_sequence:
            effort_map = {"Low": 1, "Medium": 2, "High": 3}
            total_effort = sum(effort_map.get(phase.get("estimated_effort", "Medium"), 2) for phase in implementation_sequence)
            estimated_hours = total_effort * 8  # Rough estimate: each effort point is about 8 hours
        else:
            # Fallback to older heuristic if implementation_sequence not available
            time_per_file = 1.0  # hours
            estimated_hours = file_count * time_per_file
        
        # Determine complexity level
        if file_count <= 3 and component_count <= 5:
            complexity_level = "Simple"
        elif file_count <= 10 and component_count <= 15:
            complexity_level = "Moderate"
        else:
            complexity_level = "Complex"
        
        # Calculate interfaces and data models
        interface_count = len(code_plan.get("integration_interfaces", []))
        data_model_count = len(code_plan.get("data_model", []))
        
        # Check for SDK integration complexity
        has_error_handling = bool(code_plan.get("error_handling", {}).get("error_scenarios", []))
        has_performance_considerations = bool(code_plan.get("performance_considerations", []))
        has_testing_strategy = bool(code_plan.get("testing_strategy", {}).get("unit_testing", []))
        
        # Calculate complexity score (0-100)
        complexity_score = min(100, (
            (component_count * 3) + 
            (file_count * 2) + 
            (interface_count * 3) +
            (data_model_count * 2) +
            (20 if has_error_handling else 0) +
            (15 if has_performance_considerations else 0) +
            (15 if has_testing_strategy else 0)
        ))
        
        return {
            "complexity_level": complexity_level,
            "complexity_score": complexity_score,
            "component_count": component_count,
            "file_count": file_count,
            "interface_count": interface_count,
            "data_model_count": data_model_count,
            "implementation_steps": implementation_steps,
            "estimated_hours": estimated_hours,
            "estimated_days": round(estimated_hours / 6, 1),  # Assuming 6 productive hours per day
            "has_error_handling": has_error_handling,
            "has_performance_considerations": has_performance_considerations,
            "has_testing_strategy": has_testing_strategy
        } 