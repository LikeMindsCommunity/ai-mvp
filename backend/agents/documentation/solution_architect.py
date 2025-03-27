"""
Solution Architect Agent.

This agent creates integration solutions from documentation based on user queries.
"""

import logging
import json
import re
import asyncio
from typing import Dict, Any, List, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import Anthropic

from ..core import trace, monitor

logger = logging.getLogger(__name__)

class SolutionArchitectAgent:
    """
    Agent that creates integration solutions from documentation.
    """
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Solution Architect Agent.
        
        Args:
            model_name: The name of the LLM model to use
        """
        self.llm = Anthropic(model=model_name)
        self.prompt = PromptTemplate(
    template="""
    # Solution Architect: LikeMinds SDK Integration Specialist

    You are a Solution Architect specializing exclusively in LikeMinds SDK integration. Your expertise is in frontend SDK implementation across multiple platforms. Your responsibility is to provide accurate, documentation-based solutions without hallucinating features or approaches that aren't explicitly supported by LikeMinds.

    ## User Request
    ```
    {query}
    ```

    ## Query Analysis
    ```json
    {query_analysis}
    ```

    ## Documentation Evidence
    Below is the relevant documentation from LikeMinds SDK repositories. Base your entire solution on this evidence:
    
    ```
    {context}
    ```

    ## Solution Requirements

    1. Create a structured, implementation-focused solution document addressing the user's integration needs
    2. Base your solution EXCLUSIVELY on the provided documentation context
    3. DO NOT recommend approaches, methods, or features not explicitly mentioned in the documentation
    4. Concentrate on frontend SDK implementation (Android, iOS, React, React Native, Flutter)
    5. If the documentation is insufficient to address any aspect of the query, explicitly state this limitation rather than inventing a solution

    ## Solution Document Structure

    Produce a comprehensive Markdown document with the following sections:

    ### 1. Solution Overview
    - Concise summary of the implementation approach
    - Confirmation of SDK version and platform compatibility
    - Clear statement of what the solution will achieve

    ### 2. Prerequisites
    - Required dependencies and setup
    - SDK initialization requirements
    - Authentication prerequisites if applicable

    ### 3. Implementation Steps
    - Numbered, sequential steps for implementation
    - Each step should reference specific documentation evidence
    - Platform-specific considerations clearly labeled

    ### 4. Code Implementation
    - Practical code examples in appropriate language (Kotlin/Swift/JavaScript/Dart)
    - Complete, functional code snippets (not pseudocode)
    - Comments explaining key aspects of the implementation

    ### 5. Configuration Options
    - Required and optional configuration parameters
    - Customization possibilities within documented capabilities
    - Default values and their implications

    ### 6. Integration Considerations
    - Potential implementation challenges
    - Performance implications
    - Security considerations
    - Known limitations documented in the SDK

    ### 7. Testing Guidelines
    - Verification steps to ensure proper implementation
    - Test scenarios covering key functionality

    ### 8. Documentation References
    - Specific citations to relevant sections of the documentation
    - Links to SDK references (represented as relative paths)

    ## Important Guidelines

    - CRITICAL: Reference ONLY capabilities that are explicitly documented in the provided context
    - Format all code examples with appropriate syntax highlighting (```kotlin, ```swift, etc.)
    - If multiple implementation options exist, present them in order of recommendation based on documented best practices
    - When the documentation contains warnings or deprecation notices, highlight these prominently
    - If any part of the query cannot be answered based on the documentation, clearly state: "This aspect is not covered in the current documentation. Please consult the LikeMinds support team for guidance."
    - Use precise technical language from the SDK documentation
    - Maintain consistent terminology with the LikeMinds SDK documentation

    Produce a solution document that a developer could follow to implement the required functionality with confidence, relying exclusively on documented capabilities of the LikeMinds SDK.
    """,
    input_variables=["query", "query_analysis", "context"]
)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        # Initialize next steps prompt
        self.next_steps_prompt = PromptTemplate(
            template="""
            Based on the following solution document and query analysis, suggest 3-5 
            specific next steps for the developer to take after implementing this solution.
            
            Solution Document (first 1000 chars):
            ```
            {solution_document}
            ```
            
            Query Analysis:
            ```
            {query_analysis}
            ```
            
            Focus on:
            1. Verification steps to ensure correct implementation
            2. Common pitfalls to avoid
            3. Related features that might enhance this implementation
            4. Testing scenarios
            
            Return a list of clear, actionable next steps, with each step on a new line.
            """,
            input_variables=["solution_document", "query_analysis"]
        )
        self.next_steps_chain = LLMChain(llm=self.llm, prompt=self.next_steps_prompt)
    
    def _validate_solution(self, solution_document: str, context_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate that the solution only references content from the provided documentation.
        
        Args:
            solution_document: The generated solution document
            context_documents: The documentation context used for generation
            
        Returns:
            Validation results with confidence score and potential issues
        """
        # Extract all context content for validation
        all_context_content = " ".join([doc["content"] for doc in context_documents])
        
        validation_issues = []
        confidence_score = 1.0
        
        # Check for code elements not supported by documentation
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", solution_document, re.DOTALL)
        
        for code_block in code_blocks:
            # Extract method calls and class references
            methods = re.findall(r"\.\w+\(", code_block)
            classes = re.findall(r"new\s+(\w+)", code_block)
            
            # Check if these elements appear in documentation
            for method in methods:
                method_name = method[1:-1]  # Remove the dot and parenthesis
                if method_name and len(method_name) > 3 and method_name not in all_context_content:
                    validation_issues.append(f"Method '{method_name}' not found in documentation")
                    confidence_score -= 0.1
            
            for class_name in classes:
                if class_name and len(class_name) > 3 and class_name not in all_context_content:
                    validation_issues.append(f"Class '{class_name}' not found in documentation")
                    confidence_score -= 0.1
        
        # Check for API references not in documentation
        api_patterns = [
            r"LikeMinds\.\w+", 
            r"Chat\.\w+",
            r"Feed\.\w+",
            r"LMFeed\.\w+",
            r"LMChat\.\w+",
            r"@LikeMinds"
        ]
        
        for pattern in api_patterns:
            api_references = re.findall(pattern, solution_document)
            for reference in api_references:
                if reference and reference not in all_context_content:
                    validation_issues.append(f"API reference '{reference}' not found in documentation")
                    confidence_score -= 0.1
        
        # Check for claims of support for platforms not in documentation
        platform_support_claims = re.findall(r"supported on (\w+)", solution_document.lower())
        for platform in platform_support_claims:
            if platform not in all_context_content.lower():
                validation_issues.append(f"Platform support claim for '{platform}' not found in documentation")
                confidence_score -= 0.1
        
        # Ensure confidence doesn't go below 0
        confidence_score = max(0.0, confidence_score)
        
        return {
            "confidence_score": confidence_score,
            "validation_issues": validation_issues,
            "is_valid": confidence_score > 0.7
        }
    
    @trace("solution_architect_agent.generate_contextual_next_steps")
    async def generate_contextual_next_steps(
        self,
        solution_document: str,
        query_analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Generate contextually relevant next steps using LLM.
        
        Args:
            solution_document: The generated solution
            query_analysis: The query analysis data
            
        Returns:
            List of contextually relevant next steps
        """
        try:
            with monitor("solution_architect_agent.generate_next_steps", {}):
                # Limit size for token efficiency
                solution_excerpt = solution_document[:1000] if len(solution_document) > 1000 else solution_document
                
                result = await asyncio.wait_for(
                    self.next_steps_chain.arun(
                        solution_document=solution_excerpt,
                        query_analysis=json.dumps(query_analysis)
                    ),
                    timeout=10.0  # 10-second timeout
                )
                
                # Parse list items
                next_steps = [step.strip() for step in result.split("\n") if step.strip() and not step.startswith("```")]
                if next_steps:
                    # Clean up any numbering
                    clean_steps = []
                    for step in next_steps:
                        # Remove numbering patterns like "1. ", "Step 1: ", etc.
                        clean_step = re.sub(r"^\d+\.\s*|^Step\s+\d+:\s*", "", step)
                        if clean_step:
                            clean_steps.append(clean_step)
                    return clean_steps
                
                # Fall back to rule-based approach if no steps were generated
                return self._generate_next_steps(query_analysis)
                
        except (Exception, asyncio.TimeoutError) as e:
            logger.warning(f"Error generating contextual next steps: {str(e)}")
            # Fall back to rule-based approach
            return self._generate_next_steps(query_analysis)
    
    @trace("solution_architect_agent.create_solution")
    async def create_solution(
        self,
        query: str,
        query_analysis: Dict[str, Any],
        context_documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a solution document based on the user query and context.
        
        Args:
            query: The original user query
            query_analysis: The output from the QueryUnderstandingAgent
            context_documents: The output from the ContextRetrievalAgent
            
        Returns:
            A dictionary containing the solution document and metadata
        """
        try:
            # Format the query analysis
            query_analysis_str = json.dumps(query_analysis, indent=2)
            
            # Check token budget
            query_tokens = len(query.split())
            context_tokens = sum(len(doc['content'].split()) for doc in context_documents)
            
            # If context is too large, prioritize by relevance score
            max_context_tokens = 6000  # Approx limit for Claude context
            if context_tokens > max_context_tokens:
                logger.warning(f"Context too large ({context_tokens} tokens), prioritizing top documents")
                # Sort by relevance score and limit
                sorted_docs = sorted(context_documents, key=lambda x: x['relevance_score'], reverse=True)
                prioritized_docs = []
                current_tokens = 0
                
                for doc in sorted_docs:
                    doc_tokens = len(doc['content'].split())
                    if current_tokens + doc_tokens <= max_context_tokens:
                        prioritized_docs.append(doc)
                        current_tokens += doc_tokens
                    else:
                        # Try to add a truncated version
                        available_tokens = max_context_tokens - current_tokens
                        if available_tokens > 100:  # Only add if we can include something meaningful
                            words = doc['content'].split()
                            truncated_content = " ".join(words[:available_tokens])
                            truncated_doc = doc.copy()
                            truncated_doc['content'] = truncated_content + "... [truncated]"
                            prioritized_docs.append(truncated_doc)
                        break
                
                context_documents = prioritized_docs
            
            # Format the context documents
            context_str = ""
            for i, doc in enumerate(context_documents):
                context_str += f"Document {i+1}: {doc['source']}\n"
                context_str += f"Relevance Score: {doc['relevance_score']}\n"
                context_str += f"Content:\n{doc['content']}\n\n"
            
            # Generate the solution document with timeout
            with monitor("solution_architect_agent.create_solution", 
                        {"query_length": len(query), "context_count": len(context_documents)}):
                try:
                    solution_document = await asyncio.wait_for(
                        self.chain.arun(
                            query=query,
                            query_analysis=query_analysis_str,
                            context=context_str
                        ),
                        timeout=30.0  # 30-second timeout for solution generation
                    )
                except asyncio.TimeoutError:
                    logger.error("Solution generation timed out")
                    return {
                        "solution_document": "Error: Solution generation timed out. Please try again with a more specific query or contact support.",
                        "next_steps": ["Contact support for assistance with this complex query."],
                        "metadata": {
                            "error": "Timeout",
                            "context_count": len(context_documents)
                        }
                    }
            
            # Validate the solution
            validation_result = self._validate_solution(solution_document, context_documents)
            
            # Generate next steps using the enhanced contextual method
            next_steps = await self.generate_contextual_next_steps(solution_document, query_analysis)
            
            # Add validation warning if confidence is low
            if not validation_result["is_valid"]:
                warning_header = "\n\n## ⚠️ Solution Confidence Warning\n\n"
                warning_header += "This solution may contain references to methods, classes, or features not explicitly mentioned in the documentation. "
                warning_header += "Please verify all implementation details against the official LikeMinds SDK documentation before proceeding.\n\n"
                
                if validation_result["validation_issues"]:
                    warning_header += "Potential issues detected:\n"
                    for issue in validation_result["validation_issues"][:5]:  # Show only top 5 issues
                        warning_header += f"- {issue}\n"
                
                solution_document = warning_header + solution_document
            
            return {
                "solution_document": solution_document,
                "next_steps": next_steps,
                "validation_result": validation_result,
                "relevant_context": [doc["source"] for doc in context_documents],
                "metadata": {
                    "context_count": len(context_documents),
                    "solution_length": len(solution_document),
                    "confidence_score": validation_result["confidence_score"],
                    "generated_timestamp": monitor.current_timestamp()
                }
            }
                
        except Exception as e:
            logger.error(f"Error in solution architect agent: {str(e)}", exc_info=True)
            return {
                "solution_document": f"Error generating solution: {str(e)}",
                "next_steps": ["Contact support for assistance with this issue."],
                "metadata": {
                    "error": str(e)
                }
            }
    
    def _generate_next_steps(self, query_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate suggested next steps based on the query analysis.
        
        Args:
            query_analysis: The output from the QueryUnderstandingAgent
            
        Returns:
            A list of suggested next steps
        """
        query_type = query_analysis.get("query_type", "").lower()
        intent = query_analysis.get("intent", {}).get("primary", "").lower()
        
        next_steps = []
        
        if "how-to" in query_type or "implementation" in query_type:
            next_steps.append("Try implementing the solution with your specific use case")
            next_steps.append("Read the related API reference documentation for detailed parameter info")
        
        elif "troubleshooting" in query_type:
            next_steps.append("Verify your implementation against the provided solution")
            next_steps.append("Check your API credentials and network connectivity")
            next_steps.append("Review server logs for additional error details")
        
        elif "clarification" in query_type:
            next_steps.append("Explore the linked documentation for more details")
            next_steps.append("Try a sample implementation to better understand the concept")
        
        # Add generic next steps if none matched or to supplement specific ones
        if not next_steps or len(next_steps) < 2:
            next_steps.append("Explore our documentation for working examples")
            next_steps.append("Contact our support team for more support")
        
        return next_steps 