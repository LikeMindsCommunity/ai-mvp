"""
Coding Agent Orchestrator.

This agent orchestrates the coding agent workflow.
"""

import logging
import uuid
import time
import os
from typing import Dict, Any, List, Optional, Callable, Union

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from langgraph.graph import END

from .requirement_analysis import RequirementAnalysisAgent
from .code_planning import CodePlanningAgent
from .code_generation import CodeGenerationAgent
from .code_validation import CodeValidationAgent
from ..core import trace, monitor

logger = logging.getLogger(__name__)

class SDKContext(BaseModel):
    """Data model for SDK integration context."""
    component: str = Field(default="chat", description="SDK component to integrate (chat/feed)")
    version: str = Field(default="latest", description="SDK version to target")
    documentation: Optional[str] = Field(default=None, description="SDK documentation content")
    source_repo: Optional[str] = Field(default=None, description="Source repository URL for SDK examples")
    platform_config: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific configuration")

class CodingAgentOrchestrator:
    """
    Orchestrator that manages the coding agent workflow.
    """
    
    def __init__(self, output_dir: str = "generated_code"):
        """
        Initialize the Coding Agent Orchestrator with all required agents.
        
        Args:
            output_dir: Default directory for generated code
        """
        self.requirement_analysis_agent = RequirementAnalysisAgent()
        self.code_planning_agent = CodePlanningAgent()
        self.code_generation_agent = CodeGenerationAgent()
        self.code_validation_agent = CodeValidationAgent()
        self.output_dir = output_dir
    
    @trace("coding_agent_orchestrator.process")
    async def process(
        self,
        requirements: str,
        platform: str,
        language: str,
        project_id: str,
        solution_document: Optional[str] = None,
        output_dir: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[str, float, Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Process a coding request through the agent workflow.
        
        Args:
            requirements: The user's requirements text
            platform: Target platform (e.g., 'web', 'mobile', 'backend')
            language: Programming language to use
            project_id: Unique identifier for this project
            solution_document: Optional solution document from documentation system
            output_dir: Optional custom output directory
            context: Optional additional context with sdk_component, sdk_version, and sdk_documentation
            progress_callback: Optional callback function for reporting progress updates
            
        Returns:
            A dictionary containing the generated code and metadata
        """
        try:
            start_time = time.time()
            
            # Set up the output directory
            project_output_dir = output_dir or os.path.join(self.output_dir, project_id)
            os.makedirs(project_output_dir, exist_ok=True)
            
            # Extract SDK-specific information from context and create SDK context
            context_dict = context or {}
            sdk_context = SDKContext(
                component=context_dict.get("sdk_component", "chat"),
                version=context_dict.get("sdk_version", "latest"),
                documentation=context_dict.get("sdk_documentation", None),
                source_repo=context_dict.get("sdk_source_repo", None),
                platform_config=context_dict.get("sdk_platform_config", {})
            )
            
            # Step 1: Analyze requirements
            logger.info("Analyzing requirements")
            if progress_callback:
                progress_callback("requirement_analysis", 0.1, {"message": "Analyzing requirements"})
                
            structured_requirements = await self.requirement_analysis_agent.analyze(
                requirements=requirements,
                platform=platform,
                language=language,
                solution_document=solution_document,
                context=context
            )
            
            # Step 2: Create code plan
            logger.info("Creating code plan")
            if progress_callback:
                progress_callback("code_planning", 0.3, {"message": "Creating code plan"})
                
            code_plan = await self.code_planning_agent.create_plan(
                requirements=structured_requirements,
                platform=platform,
                language=language,
                sdk_component=sdk_context.component,
                sdk_version=sdk_context.version,
                existing_code_context=context_dict.get("existing_code_context", None)
            )
            
            # Step 3: Estimate complexity
            if progress_callback:
                progress_callback("complexity_estimation", 0.4, {"message": "Estimating complexity"})
                
            complexity_estimate = await self.code_planning_agent.estimate_complexity(code_plan)
            
            # Step 4: Generate code
            logger.info("Generating code")
            if progress_callback:
                progress_callback("code_generation", 0.5, {"message": "Generating code"})
                
            generation_result = await self.code_generation_agent.generate_project(
                requirements=structured_requirements,
                code_plan=code_plan,
                platform=platform,
                language=language,
                output_dir=project_output_dir,
                sdk_component=sdk_context.component,
                sdk_documentation=sdk_context.documentation
            )
            
            # Step 5: Validate code
            logger.info("Validating code")
            if progress_callback:
                progress_callback("code_validation", 0.8, {"message": "Validating code"})
                
            validation_result = await self.code_validation_agent.validate_project(
                project_dir=project_output_dir,
                requirements=structured_requirements,
                code_plan=code_plan,
                platform=platform,
                language=language,
                sdk_component=sdk_context.component,
                sdk_documentation=sdk_context.documentation,
                sdk_version=sdk_context.version
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Final progress update
            if progress_callback:
                progress_status = "success" if validation_result.get("passes_all_requirements", False) else "needs_review"
                progress_callback("complete", 1.0, {"message": f"Process complete: {progress_status}"})
            
            # Return the final result
            return {
                "project_id": project_id,
                "output_dir": project_output_dir,
                "requirements": structured_requirements,
                "code_plan": code_plan,
                "complexity_estimate": complexity_estimate,
                "generation_result": generation_result,
                "validation_result": validation_result,
                "processing_time": processing_time,
                "status": "success" if validation_result.get("passes_all_requirements", False) else "needs_review",
                "sdk_component": sdk_context.component,
                "sdk_version": sdk_context.version
            }
                
        except Exception as e:
            logger.error(f"Error in coding agent orchestrator: {str(e)}", exc_info=True)
            
            # Error progress update
            if progress_callback:
                progress_callback("error", 1.0, {"message": f"Error: {str(e)}"})
                
            return {
                "project_id": project_id,
                "output_dir": project_output_dir if 'project_output_dir' in locals() else None,
                "status": "error",
                "error": str(e),
                "processing_time": time.time() - start_time
            }
    
    def build_workflow_graph(self) -> StateGraph:
        """
        Build an enhanced workflow graph for SDK integration.
        
        Returns:
            A LangGraph StateGraph representing the workflow
        """
        # Create workflow graph
        workflow = StateGraph(name="sdk_integration_workflow")
        
        # Add nodes for each step in the process
        workflow.add_node("requirement_analysis", self.requirement_analysis_agent.analyze)
        workflow.add_node("code_planning", self.code_planning_agent.create_plan)
        workflow.add_node("complexity_estimation", self.code_planning_agent.estimate_complexity)
        workflow.add_node("code_generation", self.code_generation_agent.generate_project)
        workflow.add_node("code_validation", self.code_validation_agent.validate_project)
        workflow.add_node("sdk_validation", self.code_validation_agent.validate_sdk_integration)
        
        # Connect the nodes with proper error handling
        workflow.add_edge("requirement_analysis", "code_planning")
        workflow.add_edge("code_planning", "complexity_estimation")
        workflow.add_edge("complexity_estimation", "code_generation")
        workflow.add_edge("code_generation", "code_validation")
        workflow.add_edge("code_validation", "sdk_validation")
        
        # Add conditional edges based on SDK validation results
        workflow.add_conditional_edges(
            "sdk_validation",
            lambda x: (
                "code_planning" if not x.get("integration_complete", False) and 
                               len(x.get("missing_essential_elements", [])) > 0 else
                "code_generation" if not x.get("integration_complete", False) else
                END
            ),
            {
                "code_planning": "code_planning",
                "code_generation": "code_generation"
            }
        )
        
        # Set the entry point
        workflow.set_entry_point("requirement_analysis")
        
        return workflow
        
    def build_simple_workflow_graph(self) -> StateGraph:
        """
        Build a simpler linear workflow graph without SDK-specific validation.
        
        Returns:
            A LangGraph StateGraph representing the workflow
        """
        # Create workflow graph
        workflow = StateGraph(name="coding_workflow")
        
        # Add nodes for each step in the process
        workflow.add_node("requirement_analysis", self.requirement_analysis_agent.analyze)
        workflow.add_node("code_planning", self.code_planning_agent.create_plan)
        workflow.add_node("complexity_estimation", self.code_planning_agent.estimate_complexity)
        workflow.add_node("code_generation", self.code_generation_agent.generate_project)
        workflow.add_node("code_validation", self.code_validation_agent.validate_project)
        
        # Connect the nodes
        workflow.add_edge("requirement_analysis", "code_planning")
        workflow.add_edge("code_planning", "complexity_estimation")
        workflow.add_edge("complexity_estimation", "code_generation")
        workflow.add_edge("code_generation", "code_validation")
        workflow.add_edge("code_validation", END)
        
        # Conditional edge for replan if validation fails
        workflow.add_conditional_edges(
            "code_validation",
            lambda x: "replan" if not x["passes_all_requirements"] and x["average_score"] < 60 else END,
            {
                "replan": "code_planning"
            }
        )
        
        # Set the entry point
        workflow.set_entry_point("requirement_analysis")
        
        return workflow

    @trace("coding_agent_orchestrator.analyze_existing_code")
    async def analyze_existing_code(
        self,
        repo_path: str,
        platform: str,
        language: str,
        sdk_component: str
    ) -> Dict[str, Any]:
        """
        Analyze existing code structure to identify integration points.
        
        Args:
            repo_path: Path to the repository
            platform: Target platform
            language: Programming language
            sdk_component: LikeMinds SDK component
            
        Returns:
            Analysis of the codebase with integration points
        """
        try:
            if not os.path.exists(repo_path):
                return {
                    "error": f"Repository path does not exist: {repo_path}",
                    "status": "error"
                }
            
            # Identify key files based on platform and language
            file_extensions = self._get_file_extensions(language)
            code_files = []
            
            for root, _, files in os.walk(repo_path):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, repo_path)
                        with open(file_path, 'r', errors='ignore') as f:
                            try:
                                content = f.read()
                                code_files.append({
                                    "path": rel_path,
                                    "content": content,
                                    "size": len(content)
                                })
                            except Exception as e:
                                logger.warning(f"Error reading file {file_path}: {str(e)}")
            
            # Platform-specific patterns to identify integration points
            integration_patterns = self._get_integration_patterns(platform, sdk_component)
            
            # Identify potential integration points
            integration_points = []
            for pattern in integration_patterns:
                for file_info in code_files:
                    if pattern.lower() in file_info["path"].lower() or pattern.lower() in file_info["content"].lower():
                        integration_points.append({
                            "file": file_info["path"],
                            "pattern": pattern,
                            "type": "file_match"
                        })
            
            # Analyze existing code structure
            logger.info(f"Analyzing code structure for {platform} using {language}")
            
            # Use code planning agent to analyze the structure
            code_structure = await self.code_planning_agent.analyze_code_structure(
                code_files=code_files[:10],  # Limit to 10 files for performance
                platform=platform,
                language=language,
                sdk_component=sdk_component
            )
            
            return {
                "repo_path": repo_path,
                "file_count": len(code_files),
                "analyzed_files": [f["path"] for f in code_files[:10]],
                "integration_points": integration_points,
                "code_structure": code_structure,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing existing code: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
    
    @trace("coding_agent_orchestrator.refine")
    async def refine(
        self,
        previous_result: Dict[str, Any],
        feedback: str,
        modifications: List[Dict[str, Any]],
        progress_callback: Optional[Callable[[str, float, Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """
        Refine a previous code generation based on feedback and specific modifications.
        
        Args:
            previous_result: The result from a previous process call
            feedback: User feedback on the previous result
            modifications: List of specific modifications to make
            progress_callback: Optional callback function for reporting progress updates
            
        Returns:
            Updated result with refined code
        """
        try:
            start_time = time.time()
            
            if "project_id" not in previous_result or "output_dir" not in previous_result:
                raise ValueError("Invalid previous result: missing project_id or output_dir")
            
            project_id = previous_result["project_id"]
            output_dir = previous_result["output_dir"]
            
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                raise ValueError(f"Previous output directory not found: {output_dir}")
            
            # Extract original parameters
            requirements = previous_result.get("requirements", {})
            code_plan = previous_result.get("code_plan", {})
            platform = code_plan.get("platform", "")
            language = code_plan.get("language", "")
            sdk_component = previous_result.get("sdk_component", "chat")
            
            # Notify progress
            if progress_callback:
                progress_callback("refine_start", 0.1, {"message": "Starting refinement process"})
            
            # Create refinement plan based on feedback
            logger.info(f"Creating refinement plan for {project_id}")
            if progress_callback:
                progress_callback("refine_planning", 0.2, {"message": "Creating refinement plan"})
                
            refinement_plan = await self.code_planning_agent.create_refinement_plan(
                original_plan=code_plan,
                feedback=feedback,
                modifications=modifications
            )
            
            # Identify files to modify
            files_to_modify = []
            for mod in modifications:
                if "file_path" in mod:
                    file_path = os.path.join(output_dir, mod["file_path"])
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            content = f.read()
                        files_to_modify.append({
                            "path": mod["file_path"],
                            "content": content,
                            "modification": mod.get("description", "")
                        })
            
            # Generate refined code
            if progress_callback:
                progress_callback("refine_generation", 0.5, {"message": "Generating refined code"})
                
            refinement_result = await self.code_generation_agent.refine_code(
                requirements=requirements,
                code_plan=code_plan,
                refinement_plan=refinement_plan,
                files_to_modify=files_to_modify,
                feedback=feedback,
                output_dir=output_dir,
                platform=platform,
                language=language,
                sdk_component=sdk_component
            )
            
            # Validate refined code
            if progress_callback:
                progress_callback("refine_validation", 0.8, {"message": "Validating refined code"})
                
            validation_result = await self.code_validation_agent.validate_project(
                project_dir=output_dir,
                requirements=requirements,
                code_plan=code_plan,
                platform=platform,
                language=language,
                sdk_component=sdk_component
            )
            
            # Final progress update
            if progress_callback:
                progress_status = "success" if validation_result.get("passes_all_requirements", False) else "needs_review"
                progress_callback("refine_complete", 1.0, {"message": f"Refinement complete: {progress_status}"})
            
            # Return the refined result
            processing_time = time.time() - start_time
            return {
                "project_id": project_id,
                "output_dir": output_dir,
                "requirements": requirements,
                "code_plan": code_plan,
                "refinement_plan": refinement_plan,
                "refinement_result": refinement_result,
                "validation_result": validation_result,
                "processing_time": processing_time,
                "status": "success" if validation_result.get("passes_all_requirements", False) else "needs_review",
                "sdk_component": sdk_component
            }
            
        except Exception as e:
            logger.error(f"Error in refinement process: {str(e)}", exc_info=True)
            
            # Error progress update
            if progress_callback:
                progress_callback("error", 1.0, {"message": f"Error during refinement: {str(e)}"})
                
            return {
                "error": str(e),
                "status": "error",
                "processing_time": time.time() - start_time
            }
    
    def _get_file_extensions(self, language: str) -> List[str]:
        """Get file extensions for the given language."""
        language = language.lower()
        extensions = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "java": [".java"],
            "kotlin": [".kt"],
            "swift": [".swift"],
            "dart": [".dart"],
            "c#": [".cs"],
            "objective-c": [".m", ".h"]
        }
        return extensions.get(language, [f".{language}"])
    
    def _get_integration_patterns(self, platform: str, sdk_component: str) -> List[str]:
        """Get integration patterns for the given platform and SDK component."""
        platform = platform.lower()
        sdk_component = sdk_component.lower()
        
        patterns = {
            "android": {
                "chat": ["MainActivity", "Application", "ChatActivity", "ChatFragment", "ChatViewModel"],
                "feed": ["MainActivity", "Application", "FeedActivity", "FeedFragment", "FeedViewModel"]
            },
            "ios": {
                "chat": ["AppDelegate", "SceneDelegate", "ChatViewController", "MessageCell"],
                "feed": ["AppDelegate", "SceneDelegate", "FeedViewController", "PostCell"]
            },
            "react-native": {
                "chat": ["App.js", "Navigation", "ChatScreen", "MessageItem"],
                "feed": ["App.js", "Navigation", "FeedScreen", "PostItem"]
            },
            "flutter": {
                "chat": ["main.dart", "chat_screen", "message_widget"],
                "feed": ["main.dart", "feed_screen", "post_widget"]
            },
            "web": {
                "chat": ["app.js", "chat", "messages", "components"],
                "feed": ["app.js", "feed", "posts", "components"]
            }
        }
        
        return patterns.get(platform, {}).get(sdk_component, [])

# Create a singleton instance for use in FastAPI router
orchestrator = CodingAgentOrchestrator()

async def process_coding_request(
    requirements: str,
    platform: str,
    language: str,
    project_id: Optional[str] = None,
    output_dir: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    solution_document: Optional[str] = None,
    user: Optional[Dict[str, Any]] = None,
    progress_callback: Optional[Callable[[str, float, Dict[str, Any]], None]] = None
) -> Dict[str, Any]:
    """
    Process a coding request.
    
    Args:
        requirements: The user's requirements text
        platform: Target platform (e.g., 'web', 'mobile', 'backend')
        language: Programming language to use
        project_id: Optional unique identifier for this project
        output_dir: Optional custom output directory
        context: Optional additional context with SDK information
        solution_document: Optional solution document from documentation system
        user: Optional user information
        progress_callback: Optional callback for reporting progress
        
    Returns:
        A dictionary containing the generated code and metadata
    """
    # Generate a project ID if not provided
    if not project_id:
        project_id = str(uuid.uuid4())
    
    # Process the request with the orchestrator
    return await orchestrator.process(
        requirements=requirements,
        platform=platform,
        language=language,
        project_id=project_id,
        solution_document=solution_document,
        output_dir=output_dir,
        context=context,
        progress_callback=progress_callback
    ) 