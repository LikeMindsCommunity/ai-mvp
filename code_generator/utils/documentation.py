"""
Documentation management utilities for the code generator.
"""

import os
from typing import Optional

class DocumentationManager:
    """
    Manages loading and handling of SDK documentation.
    """
    
    def __init__(self, documentation_path: str):
        """
        Initialize the documentation manager.
        
        Args:
            documentation_path (str): Path to the documentation file
        """
        self.documentation_path = documentation_path
        self._documentation: Optional[str] = None
    
    def load_documentation(self) -> str:
        """
        Load the documentation file into memory.
        
        Returns:
            str: The contents of the documentation file
            
        Raises:
            FileNotFoundError: If the documentation file doesn't exist
        """
        if self._documentation is None:
            if not os.path.exists(self.documentation_path):
                raise FileNotFoundError(f"Documentation file not found at {self.documentation_path}")
            
            with open(self.documentation_path, 'r', encoding='utf-8') as f:
                self._documentation = f.read()
        
        return self._documentation
    
    def clear_cache(self):
        """Clear the cached documentation."""
        self._documentation = None 