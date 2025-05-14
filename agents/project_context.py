"""
Project Context Agent for managing Flutter project information.
"""

from typing import List, Dict, Any, Optional
import os
import json
import subprocess
from pathlib import Path

from agents.base import BaseAgent
from agents.config import PROJECT_TEMP_DIR
from agno.tools.reasoning import ReasoningTools


class ProjectContextAgent(BaseAgent):
    """Agent for managing Flutter project context and information."""
    
    def __init__(self, use_claude: bool = False):
        """
        Initialize the project context agent.
        
        Args:
            use_claude: Whether to use Claude instead of Gemini
        """
        # Define instructions for the agent
        instructions = [
            "You are an expert in analyzing Flutter projects and providing relevant context.",
            "Extract key information from project files like pubspec.yaml.",
            "Identify the project structure and important dependencies.",
            "Determine the configuration of the LikeMinds SDK in the project."
        ]
        
        # Initialize the base agent
        super().__init__(
            use_claude=use_claude,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=instructions,
            markdown=True
        )
    
    def get_project_context(self, project_id: str) -> Dict[str, Any]:
        """
        Get context information for a specific project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            A dictionary containing project context information
        """
        project_path = self._get_project_path(project_id)
        
        # Check if the project exists
        if not os.path.exists(project_path):
            return {
                "error": "Project not found",
                "project_id": project_id,
                "project_path": project_path
            }
        
        # Get basic project information
        project_info = self._get_project_info(project_path)
        
        # Get pubspec.yaml information
        pubspec_info = self._parse_pubspec(project_path)
        
        # Get structure information
        structure_info = self._analyze_project_structure(project_path)
        
        # Combine all information
        return {
            "project_id": project_id,
            "project_path": project_path,
            "project_info": project_info,
            "pubspec": pubspec_info,
            "structure": structure_info
        }
    
    def _get_project_path(self, project_id: str) -> str:
        """Get the absolute path to the project directory."""
        return os.path.join(PROJECT_TEMP_DIR, project_id)
    
    def _get_project_info(self, project_path: str) -> Dict[str, Any]:
        """Get basic project information."""
        try:
            # Check if it's a Flutter project by running flutter doctor
            result = subprocess.run(
                ["flutter", "--version"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            flutter_installed = result.returncode == 0
            
            return {
                "is_flutter_project": os.path.exists(os.path.join(project_path, "pubspec.yaml")),
                "flutter_installed": flutter_installed,
                "last_modified": os.path.getmtime(project_path)
            }
        except Exception as e:
            return {
                "is_flutter_project": os.path.exists(os.path.join(project_path, "pubspec.yaml")),
                "flutter_installed": False,
                "error": str(e)
            }
    
    def _parse_pubspec(self, project_path: str) -> Dict[str, Any]:
        """Parse the pubspec.yaml file and extract relevant information."""
        pubspec_path = os.path.join(project_path, "pubspec.yaml")
        
        if not os.path.exists(pubspec_path):
            return {"error": "pubspec.yaml not found"}
        
        try:
            # Simple parsing without loading the full YAML
            # to avoid adding pyyaml dependency for this example
            with open(pubspec_path, 'r') as f:
                content = f.read()
            
            # Extract basic information using string operations
            name = self._extract_field(content, "name:")
            description = self._extract_field(content, "description:")
            version = self._extract_field(content, "version:")
            
            # Extract dependencies
            dependencies = {}
            if "dependencies:" in content:
                dep_section = content.split("dependencies:")[1]
                if "dev_dependencies:" in dep_section:
                    dep_section = dep_section.split("dev_dependencies:")[0]
                    
                # Extract each dependency
                for line in dep_section.split("\n"):
                    if ":" in line and not line.strip().startswith("#"):
                        parts = line.strip().split(":", 1)
                        if len(parts) == 2:
                            dep_name = parts[0].strip()
                            dep_version = parts[1].strip()
                            if dep_name and dep_name != "flutter":  # Skip flutter: sdk line
                                dependencies[dep_name] = dep_version
            
            # Check specifically for LikeMinds SDK
            has_likeminds = any(dep.startswith("likeminds") for dep in dependencies.keys())
            
            return {
                "name": name,
                "description": description,
                "version": version,
                "dependencies": dependencies,
                "has_likeminds_sdk": has_likeminds
            }
            
        except Exception as e:
            return {"error": f"Failed to parse pubspec.yaml: {str(e)}"}
    
    def _analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """Analyze the project structure and identify key files and directories."""
        try:
            lib_path = os.path.join(project_path, "lib")
            if not os.path.exists(lib_path):
                return {"error": "lib directory not found"}
            
            # Get directory structure
            structure = {
                "lib_files": [],
                "directories": [],
                "total_files": 0
            }
            
            # Walk through the lib directory
            for root, dirs, files in os.walk(lib_path):
                # Count total files
                structure["total_files"] += len(files)
                
                # Add directories
                for dir_name in dirs:
                    rel_path = os.path.relpath(os.path.join(root, dir_name), project_path)
                    structure["directories"].append(rel_path)
                
                # Add Dart files
                for file_name in files:
                    if file_name.endswith(".dart"):
                        rel_path = os.path.relpath(os.path.join(root, file_name), project_path)
                        structure["lib_files"].append(rel_path)
            
            # Look for LikeMinds integration
            likeminds_files = [f for f in structure["lib_files"] if "likeminds" in f.lower()]
            
            return {
                **structure,
                "likeminds_files": likeminds_files,
                "has_likeminds_integration": len(likeminds_files) > 0
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze project structure: {str(e)}"}
    
    def _extract_field(self, content: str, field_prefix: str) -> str:
        """Extract a field value from the pubspec content."""
        if field_prefix in content:
            line = content.split(field_prefix)[1].split("\n")[0].strip()
            return line
        return "" 