"""
Interface for Flutter code generator service.
"""

from typing import Optional, Dict, Callable, Awaitable, Any

class FlutterGeneratorService:
    """Interface defining the Flutter code generator service."""
    
    async def generate_flutter_code(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default") -> Dict[str, Any]:
        """
        Generate Flutter code based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            
        Returns:
            Dict[str, Any]: Response containing the generation result
        """
        raise NotImplementedError
    
    async def fix_flutter_code(self, user_query: str, error_message: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default") -> Dict[str, Any]:
        """
        Fix Flutter code based on analysis errors.
        
        Args:
            user_query (str): The original user query
            error_message (str): The Flutter analysis error message
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            
        Returns:
            Dict[str, Any]: Response containing the fixed code generation result
        """
        raise NotImplementedError 