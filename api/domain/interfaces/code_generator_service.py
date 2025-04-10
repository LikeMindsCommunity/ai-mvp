from typing import Optional, Dict, Callable

class CodeGeneratorService:
    """Interface for code generator service."""
    
    def generate_project(self, user_query: str, on_chunk: Callable[[str], None]) -> Optional[Dict]:
        """
        Generate a project based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable[[str], None]): Callback function to handle each chunk of output
            
        Returns:
            Optional[Dict]: The generated project data or None if generation failed
        """
        raise NotImplementedError 