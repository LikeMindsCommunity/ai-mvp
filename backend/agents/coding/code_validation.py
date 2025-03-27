"""
Code Validation Agent.

This agent verifies code quality against requirements and best practices.
"""

import logging
import os
import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import Anthropic

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class CodeValidationAgent:
    """
    Agent that verifies code quality against requirements and best practices.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Code Validation Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = Anthropic(model=model_name)
        self.validation_prompt = PromptTemplate(
            template="""
            You are an expert code reviewer with deep expertise in software quality.
            
            Platform: {platform}
            Language: {language}
            File: {file_path}
            
            Original Requirements:
            {requirements}
            
            Code Plan:
            {code_plan}
            
            Code to Review:
            ```
            {code}
            ```
            
            Analyze this code for:
            1. Functionality: Does it fulfill the requirements?
            2. Best practices: Does it follow language and platform best practices?
            3. Error handling: Is error handling appropriate and complete?
            4. Security: Are there any security concerns?
            5. Performance: Are there any performance issues?
            
            Respond with a JSON containing:
            - issues: List of specific issues (each with 'type', 'severity', 'description', 'line' if applicable)
            - suggestions: List of improvement suggestions
            - score: Overall quality score (0-100)
            - passes_requirements: Boolean indicating whether all requirements are met
            """,
            input_variables=["platform", "language", "file_path", "requirements", "code_plan", "code"]
        )
        self.validation_chain = LLMChain(llm=self.llm, prompt=self.validation_prompt)
        
        # SDK-specific validation prompt
        self.sdk_validation_prompt = PromptTemplate(
            template="""
            # LikeMinds SDK Integration Code Review

            ## Context
            - Platform: {platform}
            - Language: {language}
            - File: {file_path}
            - SDK Component: {sdk_component}
            - SDK Version: {sdk_version}

            ## Documentation Context
            ```
            {sdk_documentation}
            ```

            ## Code Under Review
            ```
            {code}
            ```

            ## Review Focus Areas
            1. **SDK Initialization**: Is the SDK properly initialized according to documentation?
            2. **Authentication Flow**: Is user authentication implemented correctly?
            3. **SDK Method Usage**: Are SDK methods called with correct parameters?
            4. **Error Handling**: Are SDK errors and exceptions properly handled?
            5. **Lifecycle Management**: Are resources properly managed throughout the app lifecycle?
            6. **Threading Model**: Does the code respect the SDK's threading requirements?
            7. **Configuration Options**: Are SDK configuration options properly set?
            8. **SDK Best Practices**: Does the implementation follow recommended patterns?

            ## Validation Output Format
            Provide a comprehensive review in JSON format with the following structure:
            ```json
            {
              "sdk_validation": {
                "initialization_correct": true|false,
                "authentication_implemented": true|false,
                "method_usage_correct": true|false,
                "error_handling_quality": "none|basic|comprehensive",
                "lifecycle_management_correct": true|false,
                "threading_model_correct": true|false,
                "configuration_complete": true|false
              },
              "issues": [
                {
                  "type": "initialization|authentication|method_usage|error_handling|lifecycle|threading|configuration",
                  "severity": "critical|high|medium|low",
                  "description": "Detailed description of the issue",
                  "line_reference": "Method or line number reference",
                  "correct_implementation": "Example of correct implementation"
                }
              ],
              "missing_required_elements": [
                "Description of required SDK elements that are missing"
              ],
              "suggestions": [
                "Improvement suggestion"
              ],
              "sdk_score": 0-100,
              "implementation_correct": true|false
            }
            ```

            Focus exclusively on SDK integration quality, not general code style or structure issues.
            """,
            input_variables=["platform", "language", "file_path", "code", "sdk_component", "sdk_version", "sdk_documentation"]
        )
        self.sdk_validation_chain = LLMChain(llm=self.llm, prompt=self.sdk_validation_prompt)
    
    @trace("code_validation_agent.run_static_analysis")
    async def run_static_analysis(
        self,
        file_path: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Run static analysis tools on a code file.
        
        Args:
            file_path: Path to the file to analyze
            language: Programming language of the file
            
        Returns:
            Dictionary with static analysis results
        """
        try:
            results = {
                "tool": None,
                "issues": [],
                "passed": True
            }
            
            if language.lower() == "python":
                results["tool"] = "pylint"
                cmd = ["pylint", "--output-format=json", file_path]
            elif language.lower() in ["javascript", "typescript"]:
                results["tool"] = "eslint"
                cmd = ["eslint", "--format=json", file_path]
            else:
                return {
                    "tool": "none",
                    "error": f"No static analysis tool configured for {language}",
                    "issues": [],
                    "passed": False
                }
            
            with monitor("code_validation_agent.static_analysis", 
                        {"language": language, "tool": results["tool"]}):
                process = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse the output based on the tool
            if results["tool"] == "pylint":
                if process.returncode != 0 and process.stdout:
                    results["issues"] = json.loads(process.stdout)
                    results["passed"] = False
            elif results["tool"] == "eslint":
                if process.returncode != 0 and process.stdout:
                    eslint_output = json.loads(process.stdout)
                    for file_result in eslint_output:
                        if file_result["errorCount"] > 0 or file_result["warningCount"] > 0:
                            results["issues"].extend(file_result["messages"])
                            results["passed"] = False
            
            return results
                
        except Exception as e:
            logger.error(f"Error in static analysis: {str(e)}", exc_info=True)
            return {
                "tool": results.get("tool", "unknown"),
                "error": str(e),
                "issues": [],
                "passed": False
            }
    
    @trace("code_validation_agent.validate_against_requirements")
    async def validate_against_requirements(
        self,
        file_path: str,
        code: str,
        requirements: Dict[str, Any],
        code_plan: Dict[str, Any],
        platform: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Validate code against requirements and best practices.
        
        Args:
            file_path: Path to the file being validated
            code: The code content to validate
            requirements: Structured requirements from RequirementAnalysisAgent
            code_plan: Code plan from CodePlanningAgent
            platform: Target platform
            language: Programming language
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Format the inputs
            requirements_str = json.dumps(requirements, indent=2)
            code_plan_str = json.dumps(code_plan, indent=2)
            
            # Execute the validation chain
            with monitor("code_validation_agent.validate", 
                        {"file": file_path, "code_length": len(code)}):
                result = await self.validation_chain.arun(
                    platform=platform,
                    language=language,
                    file_path=file_path,
                    requirements=requirements_str,
                    code_plan=code_plan_str,
                    code=code
                )
            
            # Process the result
            try:
                parsed_result = json.loads(result)
                return parsed_result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM output as JSON: {result}")
                # Extract structured content if possible
                import re
                json_match = re.search(r'```json\n(.*?)\n```', result, re.DOTALL)
                if json_match:
                    try:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    except json.JSONDecodeError:
                        pass
                
                # Fallback to a basic structure
                return {
                    "issues": [{
                        "type": "parsing_error",
                        "severity": "high",
                        "description": "Failed to parse validation results"
                    }],
                    "suggestions": ["Review the code manually"],
                    "score": 0,
                    "passes_requirements": False,
                    "raw_output": result
                }
                
        except Exception as e:
            logger.error(f"Error in validation agent: {str(e)}", exc_info=True)
            return {
                "issues": [{
                    "type": "validation_error",
                    "severity": "critical",
                    "description": f"Error during validation: {str(e)}"
                }],
                "suggestions": ["Fix the validation process and try again"],
                "score": 0,
                "passes_requirements": False,
                "error": str(e)
            }
    
    @trace("code_validation_agent.unit_test_generation")
    async def generate_unit_tests(
        self,
        file_path: str,
        code: str,
        requirements: Dict[str, Any],
        language: str
    ) -> str:
        """
        Generate unit tests for the given code.
        
        Args:
            file_path: Path to the file being tested
            code: The code content to test
            requirements: Structured requirements from RequirementAnalysisAgent
            language: Programming language
            
        Returns:
            String containing unit test code
        """
        test_prompt = PromptTemplate(
            template="""
            You are an expert in writing unit tests.
            
            Language: {language}
            File: {file_path}
            
            Requirements:
            {requirements}
            
            Code to Test:
            ```
            {code}
            ```
            
            Write comprehensive unit tests for this code that:
            1. Test all public functions and methods
            2. Include positive and negative test cases
            3. Test edge cases
            4. Follow best practices for {language} testing
            
            Respond with ONLY the unit test code, nothing else.
            """,
            input_variables=["language", "file_path", "requirements", "code"]
        )
        
        test_chain = LLMChain(llm=self.llm, prompt=test_prompt)
        
        try:
            # Format the inputs
            requirements_str = json.dumps(requirements, indent=2)
            
            # Execute the test generation chain
            with monitor("code_validation_agent.generate_tests", 
                        {"file": file_path, "code_length": len(code)}):
                test_code = await test_chain.arun(
                    language=language,
                    file_path=file_path,
                    requirements=requirements_str,
                    code=code
                )
            
            # Clean up the result
            import re
            code_block_match = re.search(r'```(?:\w+)?\n(.*?)\n```', test_code, re.DOTALL)
            if code_block_match:
                return code_block_match.group(1)
            
            return test_code
                
        except Exception as e:
            logger.error(f"Error generating tests for {file_path}: {str(e)}", exc_info=True)
            return f"# Error generating tests: {str(e)}"
    
    @trace("code_validation_agent.validate_project")
    async def validate_project(
        self,
        project_dir: str,
        requirements: Dict[str, Any],
        code_plan: Dict[str, Any],
        platform: str,
        language: str,
        sdk_component: str = "chat",
        sdk_documentation: Optional[str] = None,
        sdk_version: str = "latest"
    ) -> Dict[str, Any]:
        """
        Validate all code files in a project with special focus on SDK integration.
        
        Args:
            project_dir: Directory containing the project
            requirements: Structured requirements from RequirementAnalysisAgent
            code_plan: Code plan from CodePlanningAgent
            platform: Target platform
            language: Programming language
            sdk_component: LikeMinds SDK component being used
            sdk_documentation: SDK documentation
            sdk_version: SDK version
            
        Returns:
            Dictionary with validation results
        """
        try:
            results = {
                "files": [],
                "passes_all_requirements": True,
                "overall_score": 0,
                "issues": [],
                "sdk_component": sdk_component
            }
            
            # Get all relevant code files in the project
            file_extensions = self._get_file_extensions(language)
            code_files = []
            
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        code_files.append(os.path.join(root, file))
            
            # No code files found
            if not code_files:
                results["issues"].append({
                    "type": "project_error",
                    "severity": "critical",
                    "description": f"No {language} code files found in project directory"
                })
                results["passes_all_requirements"] = False
                return results
            
            # Validate each file
            total_score = 0
            sdk_related_issues = []
            
            for file_path in code_files:
                relative_path = os.path.relpath(file_path, project_dir)
                
                # Read the file
                with open(file_path, "r") as f:
                    code_content = f.read()
                
                # Skip empty files
                if not code_content.strip():
                    continue
                
                # Run validation against requirements
                validation = await self.validate_against_requirements(
                    file_path=relative_path,
                    code=code_content,
                    requirements=requirements,
                    code_plan=code_plan,
                    platform=platform,
                    language=language
                )
                
                # Add SDK-specific tags to issues if they relate to SDK
                if "issues" in validation:
                    for issue in validation["issues"]:
                        if any(sdk_term in issue.get("description", "").lower() for sdk_term in 
                               ["sdk", "likeminds", "api", "initialization", sdk_component.lower()]):
                            issue["sdk_related"] = True
                            sdk_related_issues.append({
                                "file": relative_path,
                                "issue": issue
                            })
                
                # Run static analysis if available
                try:
                    static_analysis = await self.run_static_analysis(file_path, language)
                    validation["static_analysis"] = static_analysis
                except Exception as e:
                    validation["static_analysis"] = {
                        "error": str(e),
                        "passed": False
                    }
                
                # Update the file results
                file_result = {
                    "file_path": relative_path,
                    "validation": validation,
                    "score": validation.get("score", 0),
                    "passes_requirements": validation.get("passes_requirements", False)
                }
                
                # Update project-level results
                total_score += file_result["score"]
                if not file_result["passes_requirements"]:
                    results["passes_all_requirements"] = False
                
                results["files"].append(file_result)
            
            # Calculate the average score
            if results["files"]:
                results["average_score"] = total_score / len(results["files"])
            else:
                results["average_score"] = 0
            
            # Add SDK-specific validation summary
            results["sdk_validation"] = {
                "component": sdk_component,
                "issues_count": len(sdk_related_issues),
                "sdk_related_issues": sdk_related_issues
            }
            
            # Run specialized SDK validation if SDK documentation is provided
            if sdk_documentation:
                sdk_integration = await self.validate_sdk_integration(
                    project_dir=project_dir,
                    requirements=requirements,
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation,
                    sdk_version=sdk_version
                )
                
                # Add detailed SDK validation results
                results["sdk_integration"] = sdk_integration
                
                # Update project validation status based on SDK integration completeness
                if not sdk_integration.get("integration_complete", False):
                    results["passes_all_requirements"] = False
                    
                # Add SDK integration score
                results["sdk_score"] = sdk_integration.get("overall_sdk_integration_score", 0)
                
                # Add SDK-specific issues to the main issues list
                for issue in sdk_integration.get("all_sdk_issues", []):
                    if issue.get("severity") in ["critical", "high"]:
                        results["issues"].append({
                            "type": "sdk_integration",
                            "severity": issue.get("severity"),
                            "description": issue.get("description", ""),
                            "file": issue.get("file", ""),
                            "sdk_component": sdk_component
                        })
                
                # Add missing essential SDK files as issues
                for missing in sdk_integration.get("missing_essential_elements", []):
                    results["issues"].append({
                        "type": "sdk_integration",
                        "severity": "high",
                        "description": missing,
                        "sdk_component": sdk_component
                    })
            
            return results
                
        except Exception as e:
            logger.error(f"Error validating project: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "passes_all_requirements": False,
                "files": [],
                "overall_score": 0,
                "sdk_component": sdk_component
            }
    
    def _get_file_extensions(self, language: str) -> List[str]:
        """
        Get file extensions for a given language.
        
        Args:
            language: Programming language
            
        Returns:
            List of file extensions
        """
        language = language.lower()
        extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "java": [".java"],
            "c#": [".cs"],
            "c++": [".cpp", ".cc", ".h", ".hpp"],
            "go": [".go"],
            "rust": [".rs"],
            "swift": [".swift"],
            "kotlin": [".kt"],
            "ruby": [".rb"],
            "php": [".php"]
        }
        
        return extensions.get(language, [f".{language}"])
    
    @trace("code_validation_agent.verify_sdk_patterns")
    async def verify_sdk_patterns(
        self,
        code: str,
        platform: str,
        language: str,
        sdk_component: str,
        sdk_documentation: str,
        sdk_version: str = "latest"
    ) -> Dict[str, Any]:
        """
        Verify that the code follows established SDK implementation patterns.
        
        Args:
            code: The code to verify
            platform: Target platform
            language: Programming language
            sdk_component: LikeMinds SDK component being used
            sdk_documentation: Relevant SDK documentation
            sdk_version: SDK version being targeted
            
        Returns:
            Dictionary with pattern verification results
        """
        try:
            with monitor("code_validation_agent.verify_sdk_patterns", 
                        {"platform": platform, "sdk_component": sdk_component}):
                result = await self.sdk_validation_chain.arun(
                    platform=platform,
                    language=language,
                    file_path="",  # Not needed for pattern verification
                    code=code,
                    sdk_component=sdk_component,
                    sdk_version=sdk_version,
                    sdk_documentation=sdk_documentation
                )
            
            try:
                parsed_result = json.loads(result)
                return parsed_result
            except json.JSONDecodeError:
                logger.error(f"Failed to parse SDK validation result as JSON: {result}")
                import re
                json_match = re.search(r'```json\n(.*?)\n```', result, re.DOTALL)
                if json_match:
                    try:
                        parsed_json = json.loads(json_match.group(1))
                        return parsed_json
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "sdk_validation": {
                        "initialization_correct": False,
                        "authentication_implemented": False,
                        "method_usage_correct": False,
                        "error_handling_quality": "none",
                        "lifecycle_management_correct": False,
                        "threading_model_correct": False,
                        "configuration_complete": False
                    },
                    "issues": [{
                        "type": "validation_error",
                        "severity": "critical",
                        "description": "Failed to parse validation results"
                    }],
                    "sdk_score": 0,
                    "implementation_correct": False,
                    "raw_output": result
                }
        except Exception as e:
            logger.error(f"Error verifying SDK patterns: {str(e)}")
            return {
                "sdk_validation": {
                    "initialization_correct": False,
                    "method_usage_correct": False,
                    "error_handling_quality": "none",
                },
                "issues": [{
                    "type": "validation_error",
                    "severity": "critical",
                    "description": f"Error during validation: {str(e)}"
                }],
                "sdk_score": 0,
                "implementation_correct": False
            }
    
    def _get_essential_sdk_files(self, platform: str, sdk_component: str) -> List[str]:
        """Get patterns for essential SDK integration files by platform."""
        platform = platform.lower()
        sdk_component = sdk_component.lower()
        
        # Platform-specific essential file patterns
        essential_patterns = {
            "android": {
                "chat": ["application", "chatactivity", "messageholder", "chatfragment", "chatviewmodel"],
                "feed": ["application", "feedactivity", "postviewholder", "feedfragment", "feedviewmodel"]
            },
            "ios": {
                "chat": ["appdelegate", "chatviewcontroller", "messageview", "chatmanager"],
                "feed": ["appdelegate", "feedviewcontroller", "postview", "feedmanager"]
            },
            "react-native": {
                "chat": ["app.js", "index.js", "chatscreen", "messagecomponent", "chatservice"],
                "feed": ["app.js", "index.js", "feedscreen", "postcomponent", "feedservice"]
            },
            "flutter": {
                "chat": ["main.dart", "chat_screen", "message_widget", "chat_service"],
                "feed": ["main.dart", "feed_screen", "post_widget", "feed_service"]
            },
            "react": {
                "chat": ["app.js", "index.js", "chatcomponent", "messagecomponent", "chatservice"],
                "feed": ["app.js", "index.js", "feedcomponent", "postcomponent", "feedservice"]
            }
        }
        
        # Get patterns for platform and component
        return essential_patterns.get(platform, {}).get(sdk_component, [])
    
    def _check_for_sdk_imports(self, code: str, platform: str, sdk_component: str) -> bool:
        """Check if code contains SDK imports."""
        platform = platform.lower()
        sdk_component = sdk_component.lower()
        
        # Platform-specific SDK import patterns
        import_patterns = {
            "android": {
                "chat": ["import com.likeminds.chat", "LMChat", "ChatClient"],
                "feed": ["import com.likeminds.feed", "LMFeed", "FeedClient"]
            },
            "ios": {
                "chat": ["import LikeMindsChat", "LMChatClient"],
                "feed": ["import LikeMindsFeed", "LMFeedClient"]
            },
            "react-native": {
                "chat": ["from 'likeminds-chat-react-native'", "LMChat"],
                "feed": ["from 'likeminds-feed-react-native'", "LMFeed"]
            },
            "flutter": {
                "chat": ["import 'package:likeminds_chat_flutter'", "LMChat"],
                "feed": ["import 'package:likeminds_feed_flutter'", "LMFeed"]
            },
            "react": {
                "chat": ["from 'likeminds-chat-react'", "LMChat"],
                "feed": ["from 'likeminds-feed-react'", "LMFeed"]
            }
        }
        
        # Get import patterns for platform and component
        patterns = import_patterns.get(platform, {}).get(sdk_component, [])
        
        # Check if any pattern is in the code
        return any(pattern.lower() in code.lower() for pattern in patterns)
        
    def _calculate_sdk_score(
        self, 
        validation_results: List[Dict[str, Any]], 
        missing_elements: List[str]
    ) -> int:
        """Calculate overall SDK integration score."""
        if not validation_results:
            return 0
            
        # Penalize for missing essential elements
        missing_penalty = min(len(missing_elements) * 20, 100)
        
        # Calculate average score from file validations
        total_score = 0
        for result in validation_results:
            if "validation" in result and "sdk_score" in result["validation"]:
                total_score += result["validation"]["sdk_score"]
        
        average_score = total_score / len(validation_results) if validation_results else 0
        
        # Apply missing element penalty
        final_score = max(0, average_score - missing_penalty)
        
        return round(final_score)
        
    @trace("code_validation_agent.validate_sdk_integration")
    async def validate_sdk_integration(
        self,
        project_dir: str,
        requirements: Dict[str, Any],
        platform: str,
        language: str,
        sdk_component: str,
        sdk_documentation: str,
        sdk_version: str = "latest"
    ) -> Dict[str, Any]:
        """
        Validate SDK integration across an entire project.
        
        Args:
            project_dir: Directory containing the project
            requirements: Structured requirements
            platform: Target platform
            language: Programming language
            sdk_component: LikeMinds SDK component being used
            sdk_documentation: Relevant SDK documentation
            sdk_version: SDK version being targeted
            
        Returns:
            Dictionary with SDK integration validation results
        """
        try:
            # Get list of essential SDK integration files based on platform
            essential_patterns = self._get_essential_sdk_files(platform, sdk_component)
            
            # Find all code files in the project
            file_extensions = self._get_file_extensions(language)
            code_files = []
            
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        rel_path = os.path.relpath(os.path.join(root, file), project_dir)
                        code_files.append({
                            "path": os.path.join(root, file),
                            "rel_path": rel_path,
                            "is_essential": any(pattern in rel_path.lower() for pattern in essential_patterns)
                        })
            
            # Validate each file, prioritizing essential files
            validation_results = []
            all_sdk_issues = []
            missing_essential_elements = []
            essential_files_found = set()
            
            # Check for essential file patterns
            for pattern in essential_patterns:
                if not any(pattern in file["rel_path"].lower() for file in code_files):
                    missing_essential_elements.append(f"Missing essential SDK integration file matching pattern: {pattern}")
            
            # Sort files to validate essential files first
            code_files.sort(key=lambda x: not x["is_essential"])
            
            for file_info in code_files:
                file_path = file_info["path"]
                rel_path = file_info["rel_path"]
                
                # Read file content
                with open(file_path, "r") as f:
                    code = f.read()
                
                # Skip empty files
                if not code.strip():
                    continue
                    
                # Check if file contains SDK imports
                has_sdk_imports = self._check_for_sdk_imports(code, platform, sdk_component)
                
                # If essential or contains SDK imports, do deep validation
                if file_info["is_essential"] or has_sdk_imports:
                    # Mark essential pattern as found
                    for pattern in essential_patterns:
                        if pattern in rel_path.lower():
                            essential_files_found.add(pattern)
                    
                    # Perform SDK pattern verification
                    sdk_validation = await self.verify_sdk_patterns(
                        code=code,
                        platform=platform,
                        language=language,
                        sdk_component=sdk_component,
                        sdk_documentation=sdk_documentation,
                        sdk_version=sdk_version
                    )
                    
                    # Track issues
                    if "issues" in sdk_validation:
                        for issue in sdk_validation["issues"]:
                            issue["file"] = rel_path
                            all_sdk_issues.append(issue)
                    
                    validation_results.append({
                        "file": rel_path,
                        "is_essential": file_info["is_essential"],
                        "has_sdk_imports": has_sdk_imports,
                        "validation": sdk_validation
                    })
            
            # Check for missing essential patterns
            for pattern in essential_patterns:
                if pattern not in essential_files_found:
                    missing_essential_elements.append(f"Missing essential SDK integration file matching pattern: {pattern}")
            
            # Compile final results
            return {
                "platform": platform,
                "language": language,
                "sdk_component": sdk_component,
                "sdk_version": sdk_version,
                "file_results": validation_results,
                "all_sdk_issues": all_sdk_issues,
                "missing_essential_elements": missing_essential_elements,
                "essential_patterns_found": len(essential_files_found),
                "essential_patterns_total": len(essential_patterns),
                "overall_sdk_integration_score": self._calculate_sdk_score(validation_results, missing_essential_elements),
                "integration_complete": len(missing_essential_elements) == 0 and not any(
                    issue["severity"] in ["critical", "high"] for issue in all_sdk_issues
                )
            }
        except Exception as e:
            logger.error(f"Error validating SDK integration: {str(e)}")
            return {
                "error": str(e),
                "platform": platform,
                "language": language,
                "sdk_component": sdk_component,
                "file_results": [],
                "all_sdk_issues": [{
                    "type": "validation_error",
                    "severity": "critical",
                    "description": f"Error during validation: {str(e)}"
                }],
                "integration_complete": False
            }
    
    @trace("code_validation_agent.generate_sdk_tests")
    async def generate_sdk_tests(
        self,
        code: str,
        platform: str,
        language: str,
        sdk_component: str,
        sdk_documentation: str
    ) -> str:
        """
        Generate SDK-specific unit tests.
        
        Args:
            code: The code to test
            platform: Target platform
            language: Programming language
            sdk_component: LikeMinds SDK component
            sdk_documentation: SDK documentation
            
        Returns:
            Generated unit test code
        """
        sdk_test_prompt = PromptTemplate(
            template="""
            # SDK Integration Test Generator

            ## Context
            - Platform: {platform}
            - Language: {language}
            - SDK Component: {sdk_component}

            ## Implementation Code
            ```
            {code}
            ```

            ## SDK Documentation
            ```
            {sdk_documentation}
            ```

            ## Test Generation Instructions
            Generate comprehensive unit tests for the LikeMinds SDK integration that:

            1. Test SDK initialization with valid and invalid credentials
            2. Verify proper authentication flow
            3. Test core SDK functionality based on the code implementation
            4. Verify error handling for common SDK error scenarios
            5. Test lifecycle management (initialization, teardown)
            6. Mock SDK network responses for predictable testing

            Include appropriate mock objects and test dependencies for {platform}.

            Respond with ONLY the test code, nothing else.
            """,
            input_variables=["code", "platform", "language", "sdk_component", "sdk_documentation"]
        )
        
        sdk_test_chain = LLMChain(llm=self.llm, prompt=sdk_test_prompt)
        
        try:
            with monitor("code_validation_agent.generate_sdk_tests"):
                test_code = await sdk_test_chain.arun(
                    code=code,
                    platform=platform,
                    language=language,
                    sdk_component=sdk_component,
                    sdk_documentation=sdk_documentation
                )
            
            # Clean up result
            import re
            code_block_match = re.search(r'```(?:\w+)?\n(.*?)\n```', test_code, re.DOTALL)
            if code_block_match:
                return code_block_match.group(1)
            
            return test_code
        except Exception as e:
            logger.error(f"Error generating SDK tests: {str(e)}")
            return f"# Error generating SDK tests: {str(e)}" 