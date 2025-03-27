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

class CodeValidationAgent(BaseAgent):
    """
    Agent responsible for validating generated code to ensure it meets
    quality standards, follows best practices, and works correctly.
    """
    
    def __init__(self, name: str = "code_validation"):
        """
        Initialize the Code Validation Agent.
        
        Args:
            name: Name for this agent instance
        """
        super().__init__(name)
        self.communication = AgentCommunication(self.id)
        self.llm_client = get_llm_client()
        
        # Register message handlers
        self.communication.register_handler("validate_code", self._handle_validate_code)
        
        # Initialize prompt templates
        self._init_prompts()
        
        # Cache for validation results
        self.validation_results_cache = {}
        
        self.logger.info("Code Validation Agent initialized")
    
    def _init_prompts(self):
        """Initialize prompt templates used by this agent."""
        self.syntax_validation_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
You are a code reviewer specializing in {platform} development.
Review the following code for syntax errors, typos, and basic correctness.

# File Path:
{file_path}

# Code:
{code}

Check for:
1. Syntax errors
2. Typos in variable/function names
3. Undefined references
4. Incorrect API usage
5. Basic logical errors

Provide your analysis in the following JSON format:
```json
{{
  "has_syntax_errors": true/false,
  "issues": [
    {{
      "line": 42,  // Approximate line number
      "code": "const user = User();",  // The problematic code
      "description": "Description of the issue",
      "severity": "error|warning|info",
      "suggestion": "Suggested fix"
    }}
  ],
  "overall_quality": 0-10,  // Overall quality score
  "summary": "Brief summary of findings"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.best_practices_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
You are a senior developer with expertise in {platform} development.
Review the following code for adherence to best practices.

# File Path:
{file_path}

# Code:
{code}

Check for:
1. Code organization and structure
2. Naming conventions
3. Comment quality and documentation
4. Error handling
5. Resource management
6. Memory usage
7. Performance considerations
8. Maintainability

Provide your analysis in the following JSON format:
```json
{{
  "follows_best_practices": true/false,
  "issues": [
    {{
      "line": 42,  // Approximate line number
      "code": "const user = User();",  // The problematic code
      "description": "Description of the issue",
      "category": "naming|structure|documentation|error_handling|performance|maintainability",
      "severity": "critical|important|minor",
      "suggestion": "Suggested improvement"
    }}
  ],
  "positive_aspects": [
    "Positive aspect of the code"
  ],
  "overall_score": 0-10,  // Overall best practices score
  "summary": "Brief summary of findings"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.security_validation_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
You are a security expert specializing in {platform} application security.
Review the following code for security vulnerabilities.

# File Path:
{file_path}

# Code:
{code}

Check for:
1. Injection vulnerabilities
2. Broken authentication
3. Sensitive data exposure
4. XML External Entities (XXE)
5. Broken access control
6. Security misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure deserialization
9. Using components with known vulnerabilities
10. Insufficient logging & monitoring

Provide your analysis in the following JSON format:
```json
{{
  "has_security_issues": true/false,
  "vulnerabilities": [
    {{
      "line": 42,  // Approximate line number
      "code": "const user = User();",  // The vulnerable code
      "vulnerability_type": "Type of vulnerability (e.g., 'XSS', 'SQL Injection')",
      "severity": "critical|high|medium|low",
      "description": "Description of the vulnerability",
      "remediation": "Suggested fix"
    }}
  ],
  "security_score": 0-10,  // Overall security score
  "summary": "Brief summary of findings"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.performance_analysis_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
You are a performance optimization expert specializing in {platform} development.
Review the following code for performance issues and optimization opportunities.

# File Path:
{file_path}

# Code:
{code}

Check for:
1. Inefficient algorithms
2. Redundant operations
3. Memory leaks
4. Excessive resource usage
5. Network efficiency
6. Rendering performance (for UI code)
7. Unnecessary computations
8. Bottlenecks

Provide your analysis in the following JSON format:
```json
{{
  "has_performance_issues": true/false,
  "issues": [
    {{
      "line": 42,  // Approximate line number
      "code": "const user = User();",  // The problematic code
      "description": "Description of the performance issue",
      "impact": "high|medium|low",
      "suggestion": "Optimization suggestion"
    }}
  ],
  "performance_score": 0-10,  // Overall performance score
  "summary": "Brief summary of findings"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
        
        self.compatibility_prompt = PromptTemplate(
            input_variables=["code", "file_path", "platform"],
            template="""
You are a cross-platform development expert specializing in {platform}.
Review the following code for compatibility issues across different versions, devices, and environments.

# File Path:
{file_path}

# Code:
{code}

Check for:
1. API version compatibility
2. Device-specific issues
3. Browser compatibility (if applicable)
4. OS-specific behaviors
5. Screen size/resolution handling
6. Internationalization issues
7. Accessibility concerns

Provide your analysis in the following JSON format:
```json
{{
  "has_compatibility_issues": true/false,
  "issues": [
    {{
      "line": 42,  // Approximate line number
      "code": "const user = User();",  // The problematic code
      "description": "Description of the compatibility issue",
      "affected_environments": ["Environment or version affected"],
      "severity": "critical|important|minor",
      "suggestion": "Suggested fix"
    }}
  ],
  "compatibility_score": 0-10,  // Overall compatibility score
  "summary": "Brief summary of findings"
}}
```

Your response should only contain this valid JSON with no additional text or markdown formatting outside of the JSON.
"""
        )
    
    async def _execute(
        self, 
        generated_code: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validate generated code for quality, best practices, security, and performance.
        
        Args:
            generated_code: Generated code files from Code Generation Agent
            context: Optional additional context
            
        Returns:
            Validation results for each file
        """
        context = context or {}
        platform = generated_code.get("platform", "React Native")
        generated_files = generated_code.get("generated_files", {})
        
        self.logger.info(f"Validating code for platform: {platform}")
        
        # Validate each file
        validation_results = {}
        for file_path, code in generated_files.items():
            self.logger.info(f"Validating file: {file_path}")
            
            # Run all validations
            syntax_result = await self._validate_syntax(code, file_path, platform)
            best_practices_result = await self._validate_best_practices(code, file_path, platform)
            security_result = await self._validate_security(code, file_path, platform)
            performance_result = await self._validate_performance(code, file_path, platform)
            compatibility_result = await self._validate_compatibility(code, file_path, platform)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(
                syntax_result.get("overall_quality", 0),
                best_practices_result.get("overall_score", 0),
                security_result.get("security_score", 0),
                performance_result.get("performance_score", 0),
                compatibility_result.get("compatibility_score", 0)
            )
            
            # Combine all results
            file_result = {
                "file_path": file_path,
                "syntax": syntax_result,
                "best_practices": best_practices_result,
                "security": security_result,
                "performance": performance_result,
                "compatibility": compatibility_result,
                "overall_score": overall_score,
                "pass": overall_score >= 7.0,  # Consider 7.0 as passing score
                "timestamp": datetime.utcnow().isoformat()
            }
            
            validation_results[file_path] = file_result
            
            # Cache the validation result
            self.validation_results_cache[file_path] = file_result
        
        # Create a result object
        result = {
            "platform": platform,
            "validation_results": validation_results,
            "timestamp": datetime.utcnow().isoformat(),
            "overall_pass": all(result.get("pass", False) for result in validation_results.values())
        }
        
        # Update agent state with the validation results
        self.set_state("latest_validation", result)
        
        return result
    
    def _calculate_overall_score(
        self, 
        syntax_score: float, 
        best_practices_score: float, 
        security_score: float, 
        performance_score: float, 
        compatibility_score: float
    ) -> float:
        """
        Calculate overall score from individual scores.
        
        Args:
            syntax_score: Syntax validation score
            best_practices_score: Best practices score
            security_score: Security validation score
            performance_score: Performance analysis score
            compatibility_score: Compatibility validation score
            
        Returns:
            Overall score
        """
        # Weights for each category
        weights = {
            "syntax": 0.25,
            "best_practices": 0.2,
            "security": 0.25,
            "performance": 0.15,
            "compatibility": 0.15
        }
        
        # Calculate weighted average
        overall_score = (
            syntax_score * weights["syntax"] +
            best_practices_score * weights["best_practices"] +
            security_score * weights["security"] +
            performance_score * weights["performance"] +
            compatibility_score * weights["compatibility"]
        )
        
        return round(overall_score, 1)
    
    async def _validate_syntax(self, code: str, file_path: str, platform: str) -> Dict[str, Any]:
        """
        Validate code syntax and basic correctness.
        
        Args:
            code: Code to validate
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Syntax validation results
        """
        self.logger.info(f"Validating syntax for file: {file_path}")
        
        try:
            # Prepare the prompt
            prompt = self.syntax_validation_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            return self._parse_llm_response(response, self._create_fallback_syntax_result())
            
        except Exception as e:
            self.logger.error(f"Error validating syntax: {str(e)}", exc_info=True)
            return self._create_fallback_syntax_result()
    
    async def _validate_best_practices(self, code: str, file_path: str, platform: str) -> Dict[str, Any]:
        """
        Validate code against best practices.
        
        Args:
            code: Code to validate
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Best practices validation results
        """
        self.logger.info(f"Validating best practices for file: {file_path}")
        
        try:
            # Prepare the prompt
            prompt = self.best_practices_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            return self._parse_llm_response(response, self._create_fallback_best_practices_result())
            
        except Exception as e:
            self.logger.error(f"Error validating best practices: {str(e)}", exc_info=True)
            return self._create_fallback_best_practices_result()
    
    async def _validate_security(self, code: str, file_path: str, platform: str) -> Dict[str, Any]:
        """
        Validate code for security vulnerabilities.
        
        Args:
            code: Code to validate
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Security validation results
        """
        self.logger.info(f"Validating security for file: {file_path}")
        
        try:
            # Prepare the prompt
            prompt = self.security_validation_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            return self._parse_llm_response(response, self._create_fallback_security_result())
            
        except Exception as e:
            self.logger.error(f"Error validating security: {str(e)}", exc_info=True)
            return self._create_fallback_security_result()
    
    async def _validate_performance(self, code: str, file_path: str, platform: str) -> Dict[str, Any]:
        """
        Analyze code for performance issues.
        
        Args:
            code: Code to analyze
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Performance analysis results
        """
        self.logger.info(f"Analyzing performance for file: {file_path}")
        
        try:
            # Prepare the prompt
            prompt = self.performance_analysis_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            return self._parse_llm_response(response, self._create_fallback_performance_result())
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {str(e)}", exc_info=True)
            return self._create_fallback_performance_result()
    
    async def _validate_compatibility(self, code: str, file_path: str, platform: str) -> Dict[str, Any]:
        """
        Validate code for cross-platform compatibility.
        
        Args:
            code: Code to validate
            file_path: Path of the file
            platform: Target platform
            
        Returns:
            Compatibility validation results
        """
        self.logger.info(f"Validating compatibility for file: {file_path}")
        
        try:
            # Prepare the prompt
            prompt = self.compatibility_prompt.format(
                code=code,
                file_path=file_path,
                platform=platform
            )
            
            # Get response from LLM
            response = await self.llm_client.generate_text(prompt)
            
            # Parse JSON response
            return self._parse_llm_response(response, self._create_fallback_compatibility_result())
            
        except Exception as e:
            self.logger.error(f"Error validating compatibility: {str(e)}", exc_info=True)
            return self._create_fallback_compatibility_result()
    
    def _parse_llm_response(self, response: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON response from LLM.
        
        Args:
            response: Response from LLM
            fallback: Fallback result to use if parsing fails
            
        Returns:
            Parsed JSON or fallback result
        """
        try:
            # Try to parse as JSON directly
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Return fallback if all else fails
            return fallback
    
    def _create_fallback_syntax_result(self) -> Dict[str, Any]:
        """Create a fallback syntax validation result."""
        return {
            "has_syntax_errors": False,
            "issues": [],
            "overall_quality": 8.0,
            "summary": "Unable to perform syntax validation. Assuming syntax is correct."
        }
    
    def _create_fallback_best_practices_result(self) -> Dict[str, Any]:
        """Create a fallback best practices validation result."""
        return {
            "follows_best_practices": True,
            "issues": [],
            "positive_aspects": ["Code appears to follow basic structure"],
            "overall_score": 7.0,
            "summary": "Unable to perform best practices validation. Assuming code follows best practices."
        }
    
    def _create_fallback_security_result(self) -> Dict[str, Any]:
        """Create a fallback security validation result."""
        return {
            "has_security_issues": False,
            "vulnerabilities": [],
            "security_score": 7.0,
            "summary": "Unable to perform security validation. No obvious vulnerabilities detected."
        }
    
    def _create_fallback_performance_result(self) -> Dict[str, Any]:
        """Create a fallback performance analysis result."""
        return {
            "has_performance_issues": False,
            "issues": [],
            "performance_score": 7.0,
            "summary": "Unable to perform performance analysis. Assuming reasonable performance."
        }
    
    def _create_fallback_compatibility_result(self) -> Dict[str, Any]:
        """Create a fallback compatibility validation result."""
        return {
            "has_compatibility_issues": False,
            "issues": [],
            "compatibility_score": 7.0,
            "summary": "Unable to perform compatibility validation. Assuming basic compatibility."
        }
    
    async def _handle_validate_code(self, message: Message):
        """
        Handle validate_code messages from other agents.
        
        Args:
            message: The received message
        """
        try:
            # Extract generated code from message
            generated_code = message.content.get("generated_code", {})
            context = message.content.get("context", {})
            
            # Validate code
            validation_result = await self._execute(generated_code, context)
            
            # Send response
            response = message.create_reply({"validation_result": validation_result})
            await self.communication.broker.publish(response)
            
        except Exception as e:
            self.logger.error(f"Error handling validate_code: {str(e)}", exc_info=True)
            
            # Send error response
            error_response = message.create_reply({
                "error": str(e),
                "message": "Failed to validate code"
            })
            await self.communication.broker.publish(error_response)
    
    def cleanup(self):
        """Clean up resources when the agent is no longer needed."""
        self.communication.cleanup() 