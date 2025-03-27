"""
Code Generation Agent.

This agent generates implementation code based on requirements and code plans.
"""

import logging
import os
import json
import re
from typing import Dict, Any, List, Optional, Union
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import Anthropic

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class CodeGenerationAgent:
    """
    Agent that generates implementation code based on requirements and code plans.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Code Generation Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = Anthropic(model=model_name)
        self.code_prompt = PromptTemplate(
            template="""
            # SDK Implementation Code Generator

            ## Context
            You are creating production-ready code to integrate the LikeMinds SDK for the following:
            - Platform: {platform}
            - Language: {language}
            - File: {file_path}
            - SDK Component: {sdk_component}

            ## Input Documentation
            ### Implementation Requirements
            ```
            {requirements}
            ```

            ### Code Plan
            ```
            {code_plan}
            ```

            ### SDK Documentation Context
            ```
            {sdk_documentation}
            ```

            ## Implementation Guidelines
            1. Follow the exact SDK implementation patterns shown in the SDK documentation
            2. Use the proper SDK initialization sequence for the platform
            3. Implement proper error handling for SDK operations
            4. Use SDK-provided model classes rather than creating custom ones
            5. Follow platform-specific best practices for the integration
            6. Include necessary imports for SDK components
            7. Add clear comments explaining SDK interaction points
            8. Use correct SDK method signatures and parameters
            9. Implement proper lifecycle management for SDK resources

            ## Output Instructions
            Generate complete, production-ready code for {file_path} that properly integrates the LikeMinds {sdk_component} SDK.
            
            Respond with ONLY the code, nothing else. Do not include explanations outside of code comments.
            """,
            input_variables=["platform", "language", "file_path", "requirements", "code_plan", "dependencies", "sdk_component", "sdk_documentation"]
        )
        
        self.file_structure_prompt = PromptTemplate(
            template="""
            # SDK Integration File Structure Generator

            ## Context
            You are creating a file structure for integrating the LikeMinds SDK:
            - Platform: {platform}
            - Language: {language}
            - SDK Component: {sdk_component}

            ## Input Documentation
            ### Requirements
            ```
            {requirements}
            ```

            ### Code Plan
            ```
            {code_plan}
            ```

            ### SDK Documentation
            ```
            {sdk_documentation}
            ```

            ## Output Guidelines
            Create a comprehensive file structure that:
            1. Follows platform conventions for organizing code ({platform})
            2. Separates SDK initialization from usage
            3. Organizes files according to the SDK component being integrated
            4. Includes necessary configuration files
            5. Follows typical project structure for {language}

            Provide a JSON list of objects, each with the following fields:
            - 'path': Relative file path
            - 'description': Purpose of the file
            - 'sdk_components': List of SDK classes/interfaces used in this file
            - 'contents': List of main functions/classes in the file
            """,
            input_variables=["requirements", "code_plan", "platform", "language", "sdk_component", "sdk_documentation"]
        )
        
        self.code_chain = LLMChain(llm=self.llm, prompt=self.code_prompt)
        self.file_structure_chain = LLMChain(llm=self.llm, prompt=self.file_structure_prompt)
    
    @trace("code_generation_agent.generate_file_structure")
    async def generate_file_structure(
        self,
        requirements: Dict[str, Any],
        code_plan: Dict[str, Any],
        platform: str,
        language: str,
        sdk_component: str = "chat",
        sdk_documentation: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate a file structure based on the requirements and code plan.
        
        Args:
            requirements: Structured requirements from RequirementAnalysisAgent
            code_plan: Code plan from CodePlanningAgent
            platform: Target platform (e.g., 'android', 'ios', 'react-native')
            language: Programming language to use
            sdk_component: LikeMinds SDK component ('chat' or 'feed')
            sdk_documentation: Optional SDK documentation to guide the structure
            
        Returns:
            A list of dictionaries containing file paths and descriptions
        """
        try:
            # Format the inputs as strings
            requirements_str = json.dumps(requirements, indent=2)
            code_plan_str = json.dumps(code_plan, indent=2)
            
            # Execute the chain
            with monitor("code_generation_agent.generate_file_structure", 
                        {"req_length": len(requirements_str), "plan_length": len(code_plan_str)}):
                result = await self.file_structure_chain.arun(
                    requirements=requirements_str,
                    code_plan=code_plan_str,
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation or "No specific SDK documentation provided."
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
                return [{
                    "path": f"{sdk_component.lower()}Integration.{self._get_file_extension(language)}",
                    "description": f"Main entry point for {sdk_component} SDK integration",
                    "sdk_components": [f"LikeMinds{sdk_component.capitalize()}SDK"],
                    "contents": [f"initialize{sdk_component.capitalize()}SDK()", f"use{sdk_component.capitalize()}Features()"]
                }]
                
        except Exception as e:
            logger.error(f"Error generating file structure: {str(e)}", exc_info=True)
            return [{
                "path": f"{sdk_component.lower()}Integration.{self._get_file_extension(language)}",
                "description": f"Error generating file structure: {str(e)}",
                "sdk_components": [f"LikeMinds{sdk_component.capitalize()}SDK"],
                "contents": [f"initialize{sdk_component.capitalize()}SDK()"]
            }]
    
    def _get_file_extension(self, language: str) -> str:
        """Get the appropriate file extension for the given language."""
        extensions = {
            "kotlin": "kt",
            "java": "java",
            "swift": "swift",
            "javascript": "js",
            "typescript": "ts",
            "python": "py",
            "dart": "dart",
        }
        return extensions.get(language.lower(), "txt")
    
    @trace("code_generation_agent.generate_code")
    async def generate_code(
        self,
        file_path: str,
        requirements: Dict[str, Any],
        code_plan: Dict[str, Any],
        platform: str,
        language: str,
        sdk_component: str = "chat",
        sdk_documentation: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """
        Generate implementation code for a specific file with LikeMinds SDK integration.
        
        Args:
            file_path: Path to the file to generate
            requirements: Structured requirements from RequirementAnalysisAgent
            code_plan: Code plan from CodePlanningAgent
            platform: Target platform (e.g., 'android', 'ios', 'react-native')
            language: Programming language to use
            sdk_component: LikeMinds SDK component ('chat' or 'feed')
            sdk_documentation: Relevant SDK documentation sections
            dependencies: Optional list of dependencies
            
        Returns:
            The generated code as a string
        """
        try:
            # Format the inputs as strings
            requirements_str = json.dumps(requirements, indent=2)
            code_plan_str = json.dumps(code_plan, indent=2)
            dependencies_str = ", ".join(dependencies) if dependencies else "None specified"
            
            # Execute the chain
            with monitor("code_generation_agent.generate_code", 
                        {"file": file_path, "platform": platform, "sdk_component": sdk_component}):
                result = await self.code_chain.arun(
                    file_path=file_path,
                    requirements=requirements_str,
                    code_plan=code_plan_str,
                    platform=platform,
                    language=language,
                    dependencies=dependencies_str,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation or "No specific SDK documentation provided."
                )
            
            # Clean up the result
            # Sometimes the LLM might include code blocks with backticks
            code_block_match = re.search(r'```(?:\w+)?\n(.*?)\n```', result, re.DOTALL)
            if code_block_match:
                return code_block_match.group(1)
            
            return result
                
        except Exception as e:
            logger.error(f"Error generating code for {file_path}: {str(e)}", exc_info=True)
            return f"# Error generating code: {str(e)}"
    
    @trace("code_generation_agent.validate_sdk_usage")
    async def validate_sdk_usage(
        self,
        generated_code: str,
        platform: str,
        sdk_component: str,
        sdk_documentation: str
    ) -> Dict[str, Any]:
        """
        Validate proper SDK usage in the generated code.
        
        Args:
            generated_code: The generated implementation code
            platform: Target platform
            sdk_component: LikeMinds SDK component ('chat' or 'feed')
            sdk_documentation: SDK documentation content
            
        Returns:
            Validation results with any issues found
        """
        # Implement a validation prompt to check SDK usage
        validation_prompt = PromptTemplate(
            template="""
            Analyze the following generated code for correct LikeMinds SDK usage.
            
            Generated Code:
            ```
            {code}
            ```
            
            SDK Documentation:
            ```
            {sdk_documentation}
            ```
            
            Platform: {platform}
            SDK Component: {sdk_component}
            
            Identify any issues with SDK usage, including:
            1. Missing or incorrect SDK initialization
            2. Improper method calls or parameters
            3. Missing error handling for SDK operations
            4. Incorrect threading/async patterns
            5. Missing permissions or configuration
            
            Respond with a JSON object containing these fields:
            - valid: boolean indicating if the SDK usage is correct
            - issues: array of objects with 'type', 'description', and 'severity' fields
            - suggestions: array of improvement suggestions
            - sdk_classes_used: array of SDK classes used in the code
            - initialization_correct: boolean indicating if initialization is correct
            - error_handling_score: number from 0-1 rating the error handling
            """,
            input_variables=["code", "platform", "sdk_component", "sdk_documentation"]
        )
        
        validation_chain = LLMChain(llm=self.llm, prompt=validation_prompt)
        
        try:
            with monitor("code_generation_agent.validate_sdk_usage"):
                result = await validation_chain.arun(
                    code=generated_code,
                    platform=platform,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation
                )
            
            try:
                validation_result = json.loads(result)
                return validation_result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse validation result as JSON: {result}")
                # Try to extract JSON if it's in a code block
                json_match = re.search(r'```json\n(.*?)\n```', result, re.DOTALL)
                if json_match:
                    try:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "valid": False,
                    "parsing_error": "Failed to parse validation result",
                    "raw_result": result
                }
        except Exception as e:
            logger.error(f"Error validating SDK usage: {str(e)}")
            return {
                "valid": False,
                "error": str(e)
            }
    
    @trace("code_generation_agent.generate_project")
    async def generate_project(
        self,
        requirements: Dict[str, Any],
        code_plan: Dict[str, Any],
        platform: str,
        language: str,
        output_dir: str,
        sdk_component: str = "chat",
        sdk_documentation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete project based on requirements and code plan.
        
        Args:
            requirements: Structured requirements from RequirementAnalysisAgent
            code_plan: Code plan from CodePlanningAgent
            platform: Target platform (e.g., 'android', 'ios', 'react-native')
            language: Programming language to use
            output_dir: Directory to save the generated files
            sdk_component: LikeMinds SDK component ('chat' or 'feed')
            sdk_documentation: SDK documentation content
            
        Returns:
            A dictionary with information about the generated project
        """
        try:
            # Generate file structure with SDK documentation context
            file_structure = await self.generate_file_structure(
                requirements, code_plan, platform, language, sdk_component, sdk_documentation
            )
            
            # Track validation results
            validation_results = {}
            generated_files = []
            
            for file_info in file_structure:
                file_path = file_info["path"]
                full_path = os.path.join(output_dir, file_path)
                
                # Create directory if needed
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Generate code with SDK context
                code = await self.generate_code(
                    file_path=file_path,
                    requirements=requirements,
                    code_plan=code_plan,
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation,
                    dependencies=requirements.get("dependencies", [])
                )
                
                # Validate SDK usage if this file uses SDK components
                if sdk_documentation and "sdk_components" in file_info and file_info["sdk_components"]:
                    validation = await self.validate_sdk_usage(
                        generated_code=code,
                        platform=platform,
                        sdk_component=sdk_component,
                        sdk_documentation=sdk_documentation
                    )
                    validation_results[file_path] = validation
                    
                    # If validation fails critically, modify code to fix issues
                    if validation and not validation.get("valid", True) and validation.get("suggestions"):
                        # Add validation suggestions as comments
                        comment_prefix = "//" if language.lower() in ["javascript", "typescript", "kotlin", "java", "swift", "c#"] else "#"
                        suggestion_comments = "\n".join([
                            f"{comment_prefix} TODO: {suggestion}" for suggestion in validation.get("suggestions", [])
                        ])
                        code = suggestion_comments + "\n\n" + code
                
                # Save the file
                with open(full_path, "w") as f:
                    f.write(code)
                
                generated_files.append({
                    "path": file_path,
                    "full_path": full_path,
                    "size": len(code),
                    "sdk_components_used": file_info.get("sdk_components", [])
                })
            
            return {
                "status": "success",
                "files": generated_files,
                "file_count": len(generated_files),
                "output_dir": output_dir,
                "validation_results": validation_results,
                "sdk_component": sdk_component
            }
                
        except Exception as e:
            logger.error(f"Error generating project: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "output_dir": output_dir
            } 