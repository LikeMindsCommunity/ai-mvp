"""
Interface for Flutter code generator service.

Response Types:
- Text: Status updates and progress messages
- Code: Generated code content
- Chat: Conversational explanations and plans
- Error: Error messages
- Success: Success notifications
- AnalysisError: Flutter code analysis errors
- Result: Final result with URL and file path information
"""

from typing import Optional, Dict, Callable, Awaitable, Any

class FlutterGeneratorService:
    """Interface defining the Flutter code generator service."""
    
    async def generate_flutter_code(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, project_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Generate Flutter code based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this instead of generating a UUID.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: Response containing the generation result
        """
        raise NotImplementedError
    
    async def generate_conversation(self, user_query: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", db_generation_id: str = None, project_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Generate conversational explanation and plan for Flutter code implementation.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            db_generation_id (str, optional): Database-generated ID for this generation. If provided, will use this to update the record.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: The generated conversation result
        """
        raise NotImplementedError
    
    async def fix_flutter_code(self, user_query: str, error_message: str, on_chunk: Callable[[Dict[str, Any]], Awaitable[None]], session_id: str = "default", generation_id: str = None, project_id: str = None, access_token: str = None) -> Dict[str, Any]:
        """
        Fix Flutter code based on analysis errors.
        
        Args:
            user_query (str): The original user query
            error_message (str): The Flutter analysis error message
            on_chunk (Callable): Callback function to handle streaming output chunks
            session_id (str, optional): Unique identifier for the user session. Defaults to "default".
            generation_id (str, optional): Generation ID to fix. If not provided, uses the latest generation.
            project_id (str, optional): Project ID this generation belongs to.
            access_token (str, optional): User's JWT access token for database operations.
            
        Returns:
            Dict[str, Any]: Response containing the fixed code generation result
        """
        raise NotImplementedError
        
    def cleanup_generation(self, project_id: str) -> bool:
        """
        Clean up resources for a project.
        
        Args:
            project_id (str): Project ID to clean up
            
        Returns:
            bool: True if cleanup was successful
        """
        raise NotImplementedError 