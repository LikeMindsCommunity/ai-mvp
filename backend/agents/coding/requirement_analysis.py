"""
Requirement Analysis Agent.

This agent structures requirements for code generation.
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

class RequirementAnalysisAgent:
    """
    Agent that analyzes and structures requirements for code generation.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Requirement Analysis Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = Anthropic(model=model_name)
        self.prompt = PromptTemplate(
            template="""
            # Requirements Analysis Agent for LikeMinds SDK Integration

            ## Agent Role
            You are a specialized requirements engineer focusing exclusively on LikeMinds SDK integration projects. Your expertise spans multiple platforms (Android, iOS, Web, React Native, Flutter) and you excel at translating developer needs into structured, implementable specifications.

            ## Input Requirements
            Developer request to analyze:
            ```
            {requirements}
            ```

            ## Solution Context
            Additional context from documentation or previous analysis:
            ```
            {context}
            ```

            ## Technical Parameters
            - Target Platform: {platform}
            - Implementation Language: {language}
            - SDK Component: {sdk_component}

            ## Analysis Instructions
            Analyze the requirements with specific attention to LikeMinds SDK integration patterns. Your analysis should:

            1. Focus on real-world implementation scenarios for chat and social features
            2. Consider platform-specific best practices and limitations
            3. Identify potential edge cases in messaging and content delivery
            4. Align with documented SDK capabilities rather than theoretical possibilities
            5. Anticipate authentication and user management requirements

            ## Output Specifications
            Provide a comprehensive requirements specification in JSON format with the following sections:

            ```json
            {
              "functional_requirements": [
                {
                  "id": "FR-01",
                  "title": "Requirement title",
                  "description": "Detailed description",
                  "priority": "High|Medium|Low",
                  "sdk_features": ["specific SDK features needed"]
                }
              ],
              "technical_requirements": [
                {
                  "id": "TR-01",
                  "title": "Requirement title",
                  "description": "Technical implementation details",
                  "platform_specific": {
                    "platform_name": "Implementation considerations"
                  }
                }
              ],
              "ui_requirements": [
                {
                  "id": "UI-01",
                  "component": "Component name",
                  "description": "UI behavior description",
                  "customization_points": ["Customizable aspects"]
                }
              ],
              "data_requirements": [
                {
                  "id": "DR-01",
                  "data_entity": "Entity name",
                  "fields": ["Required fields"],
                  "persistence": "Local|Remote|Both",
                  "sync_requirements": "Description of synchronization needs"
                }
              ],
              "integration_touchpoints": [
                {
                  "id": "IT-01",
                  "touchpoint": "Integration point description",
                  "existing_code_changes": "Required modifications to existing code",
                  "new_components": "New components to be created"
                }
              ],
              "dependencies": [
                {
                  "id": "DEP-01",
                  "dependency_type": "Library|Service|Configuration",
                  "name": "Dependency name",
                  "version": "Version requirements",
                  "purpose": "Why this dependency is needed"
                }
              ],
              "testing_criteria": [
                {
                  "id": "TC-01",
                  "scenario": "Test scenario description",
                  "expected_outcome": "Expected behavior",
                  "edge_cases": ["Specific edge cases to test"]
                }
              ],
              "implementation_phases": [
                {
                  "id": "IP-01",
                  "phase": "Phase name",
                  "description": "What to implement in this phase",
                  "dependencies": ["IDs of dependent requirements"]
                }
              ]
            }
            ```

            ## Critical Guidelines

            1. **Specificity**: Each requirement should be specific and actionable, not vague
            2. **Completeness**: Address all aspects of the integration, including initialization, authentication, and message handling
            3. **Realism**: Only include requirements that are feasible with the current LikeMinds SDK
            4. **Platform Awareness**: Acknowledge platform-specific implementation differences
            5. **Code Readiness**: Requirements should be detailed enough to directly inform code generation
            6. **Integration Focus**: Pay special attention to how new features will integrate with existing code
            7. **User Experience**: Consider the end-user experience in feature implementation
            8. **Performance Implications**: Note any requirements with potential performance impact

            Your analysis will drive code generation and integration planning, so emphasize clarity, completeness, and technical accuracy.
            """,
            input_variables=["requirements", "context", "platform", "language", "sdk_component"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    @trace("requirement_analysis_agent.analyze")
    async def analyze(
        self,
        requirements: str,
        platform: str,
        language: str,
        sdk_component: str = "chat",  # Default to chat if not specified
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze and structure requirements for code generation.
        
        Args:
            requirements: The user's requirements text
            platform: Target platform (e.g., 'web', 'mobile', 'backend')
            language: Programming language to use
            sdk_component: LikeMinds SDK component to use (e.g., 'chat', 'feed')
            context: Optional additional context
            
        Returns:
            A structured requirements specification
        """
        try:
            # Execute the chain
            with monitor("requirement_analysis_agent.analyze", 
                        {"req_length": len(requirements)}):
                result = await self.chain.arun(
                    requirements=requirements,
                    context=context or "",
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component
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
                    "functional_requirements": [
                        {
                            "id": "FR-01",
                            "title": "Implement Requirements",
                            "description": requirements,
                            "priority": "High",
                            "sdk_features": [f"{sdk_component} SDK integration"]
                        }
                    ],
                    "technical_requirements": [
                        {
                            "id": "TR-01",
                            "title": f"Use {language} on {platform}",
                            "description": f"Implement using {language} for {platform}",
                            "platform_specific": {
                                f"{platform}": "Standard implementation"
                            }
                        }
                    ],
                    "ui_requirements": [],
                    "data_requirements": [],
                    "integration_touchpoints": [],
                    "dependencies": [
                        {
                            "id": "DEP-01",
                            "dependency_type": "Library",
                            "name": "LikeMinds SDK",
                            "version": "latest",
                            "purpose": f"Core {sdk_component} functionality"
                        }
                    ],
                    "testing_criteria": [
                        {
                            "id": "TC-01",
                            "scenario": "Basic functionality",
                            "expected_outcome": "Code runs without errors",
                            "edge_cases": []
                        }
                    ],
                    "implementation_phases": [
                        {
                            "id": "IP-01",
                            "phase": "Initial Implementation",
                            "description": "Implement basic functionality",
                            "dependencies": []
                        }
                    ],
                    "raw_output": result
                }
                
        except Exception as e:
            logger.error(f"Error in requirement analysis agent: {str(e)}", exc_info=True)
            return {
                "functional_requirements": [
                    {
                        "id": "FR-01",
                        "title": "Error analyzing requirements",
                        "description": str(e),
                        "priority": "High",
                        "sdk_features": []
                    }
                ],
                "technical_requirements": [],
                "ui_requirements": [],
                "data_requirements": [],
                "integration_touchpoints": [],
                "dependencies": [],
                "testing_criteria": [],
                "implementation_phases": [],
                "error": str(e)
            }
    
    @trace("requirement_analysis_agent.validate")
    async def validate(
        self,
        structured_requirements: Dict[str, Any],
        sdk_capabilities: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate structured requirements for completeness and consistency.
        
        Args:
            structured_requirements: The structured requirements to validate
            sdk_capabilities: Optional known SDK capabilities for validation
            
        Returns:
            A dictionary with validation results
        """
        validation_issues = []
        warnings = []
        
        # Check for required sections
        required_sections = [
            "functional_requirements",
            "technical_requirements",
            "ui_requirements",
            "dependencies"
        ]
        
        # Validate section presence
        for section in required_sections:
            if section not in structured_requirements:
                validation_issues.append(f"Missing section: {section}")
            elif not structured_requirements[section]:
                warnings.append(f"Empty section: {section}")
        
        # Validate against SDK capabilities if provided
        if sdk_capabilities and "functional_requirements" in structured_requirements:
            for req in structured_requirements["functional_requirements"]:
                if "sdk_features" in req:
                    for feature in req["sdk_features"]:
                        if feature not in sdk_capabilities.get("features", []):
                            warnings.append(f"Potential unsupported feature: {feature}")
        
        # Validate dependencies
        if "dependencies" in structured_requirements:
            for dep in structured_requirements["dependencies"]:
                if dep.get("dependency_type") == "Library" and sdk_capabilities:
                    version = dep.get("version", "")
                    if version and version not in sdk_capabilities.get("compatible_versions", []):
                        warnings.append(f"Potential version compatibility issue: {dep.get('name', 'Unknown')} {version}")
        
        # Return validation results
        if validation_issues:
            return {
                "is_valid": False,
                "issues": validation_issues,
                "warnings": warnings,
                "suggestions": self._generate_suggestions(validation_issues, warnings)
            }
        
        return {
            "is_valid": True,
            "warnings": warnings,
            "suggestions": self._generate_suggestions([], warnings)
        }
    
    def _generate_suggestions(
        self,
        missing_sections: List[str],
        warnings: List[str]
    ) -> List[str]:
        """
        Generate suggestions for missing or empty requirement sections.
        
        Args:
            missing_sections: List of missing sections
            warnings: List of warnings
            
        Returns:
            A list of suggestions
        """
        suggestions = []
        
        # Generate suggestions based on missing sections
        section_suggestions = {
            "functional_requirements": "Add specific functionality descriptions detailing what the code should accomplish",
            "technical_requirements": "Specify technical aspects like frameworks, design patterns, or architectural approaches",
            "ui_requirements": "Define UI components, behaviors, and customization points",
            "dependencies": "List required libraries, services, or external systems",
            "data_requirements": "Specify data entities, fields, and persistence requirements",
            "integration_touchpoints": "Define how new code integrates with existing systems",
            "testing_criteria": "Include test scenarios, expected outcomes, and edge cases",
            "implementation_phases": "Break down implementation into logical phases with dependencies"
        }
        
        for section in missing_sections:
            if section in section_suggestions:
                suggestions.append(section_suggestions[section])
        
        # Add suggestions based on warnings
        if any("unsupported feature" in warning for warning in warnings):
            suggestions.append("Verify SDK capabilities before including features that may not be supported")
        
        if any("version compatibility" in warning for warning in warnings):
            suggestions.append("Check SDK version compatibility requirements")
        
        if any("Empty section" in warning for warning in warnings):
            suggestions.append("Complete all sections for comprehensive requirements specification")
        
        return suggestions 