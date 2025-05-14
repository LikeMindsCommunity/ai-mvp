"""
Code Generation Agent for creating Flutter code snippets and examples.
"""

from typing import List, Dict, Any, Optional
import json
import re

from agents.base import BaseAgent
from agno.tools.reasoning import ReasoningTools


class CodeGenAgent(BaseAgent):
    """Agent for generating Flutter code based on requirements and documentation."""
    
    def __init__(self, use_claude: bool = False):
        """
        Initialize the code generation agent.
        
        Args:
            use_claude: Whether to use Claude instead of Gemini (recommended for code generation)
        """
        # Define instructions for the agent
        instructions = [
            "You are an expert Flutter developer specializing in the LikeMinds SDK.",
            "Generate correct, idiomatic Flutter code that follows best practices.",
            "Always include necessary imports in your code.",
            "Structure your code to be easily understandable and maintainable.",
            "When generating multiple files, clearly mark the boundaries between files.",
            "Include clear comments explaining complex logic or SDK-specific functionality."
        ]
        
        # Initialize the base agent
        super().__init__(
            use_claude=use_claude,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=instructions,
            markdown=True
        )
    
    def generate_code(
        self, 
        requirements: str,
        retrieved_docs: str,
        project_context: Optional[str] = None,
        existing_code: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate Flutter code based on requirements and documentation.
        
        Args:
            requirements: The requirements for the code to generate
            retrieved_docs: Documentation snippets retrieved from the vector store
            project_context: Optional context about the project structure
            existing_code: Optional existing code to modify/extend
            
        Returns:
            A dictionary of file names to file contents
        """
        # Build the prompt
        prompt = "# Code Generation Task\n\n"
        prompt += f"## Requirements\n{requirements}\n\n"
        
        if project_context:
            prompt += f"## Project Context\n{project_context}\n\n"
            
        if existing_code:
            prompt += f"## Existing Code\n```dart\n{existing_code}\n```\n\n"
            
        prompt += f"## Retrieved Documentation\n{retrieved_docs}\n\n"
        
        prompt += """## Instructions
Generate Flutter code that meets the requirements above. Include all necessary imports.
If multiple files are needed, clearly mark each file with '--- filename.dart ---' before the code.
Ensure the code follows Flutter best practices and properly integrates with the LikeMinds SDK.
"""
        
        # Get the response from the agent
        response = self.ask(prompt, stream=False, show_reasoning=True)
        
        # Parse the generated code
        return self._parse_generated_code(response)
    
    def _parse_generated_code(self, response: str) -> Dict[str, str]:
        """
        Parse the generated code from the agent's response.
        
        Args:
            response: The raw response from the agent (as string)
            
        Returns:
            A dictionary mapping file names to file contents
        """
        # Ensure response is a string
        if not isinstance(response, str):
            print(f"Warning: Response is not a string but {type(response)}. Converting to string.")
            response = str(response)
        
        # Extract code blocks
        code_files = {}
        
        try:
            # Check if the response contains multiple files
            file_pattern = r"---\s*([a-zA-Z0-9_./]+\.dart)\s*---"
            file_matches = re.finditer(file_pattern, response)
            
            # Get the positions of all file markers
            file_positions = []
            for match in file_matches:
                file_positions.append((match.group(1), match.end()))
            
            if file_positions:
                # Multiple files detected
                for i, (file_name, start_pos) in enumerate(file_positions):
                    # Find the end position (either the next file marker or the end of the response)
                    end_pos = len(response)
                    if i < len(file_positions) - 1:
                        next_file_marker = f"--- {file_positions[i+1][0]} ---"
                        potential_end = response.find(next_file_marker, start_pos)
                        if potential_end != -1:
                            end_pos = potential_end
                    
                    # Extract the code
                    code = response[start_pos:end_pos].strip()
                    
                    # Remove code block markers if present
                    code = self._clean_code_block(code)
                    
                    code_files[file_name] = code
            else:
                # Look for code blocks in markdown
                dart_blocks = re.finditer(r"```dart(.*?)```", response, re.DOTALL)
                for block in dart_blocks:
                    # Extract the code and store it in the files dict
                    code = block.group(1).strip()
                    code_files["chat_screen.dart"] = code
                    break  # Just use the first one for now
                
                # If no dart-specific blocks, look for generic code blocks
                if not code_files:
                    code_blocks = re.finditer(r"```(.*?)```", response, re.DOTALL)
                    for block in code_blocks:
                        code = block.group(1).strip()
                        if "import 'package:flutter" in code or "StatelessWidget" in code or "StatefulWidget" in code:
                            # Looks like Dart code
                            code_files["chat_screen.dart"] = code
                            break
                
                # If still nothing, use the whole response (not ideal)
                if not code_files:
                    code_files["filename.dart"] = response.strip()
        
        except Exception as e:
            print(f"Error parsing code: {e}")
            # In case of an error, return the whole text as a file
            code_files["error_parsed_code.dart"] = response.strip()
        
        return code_files
    
    def _clean_code_block(self, code: str) -> str:
        """Clean a code block by removing markdown code block markers."""
        # Remove leading and trailing code block markers
        if code.startswith("```dart"):
            code = code[7:]
        elif code.startswith("```"):
            code = code[3:]
            
        if code.endswith("```"):
            code = code[:-3]
            
        return code.strip() 