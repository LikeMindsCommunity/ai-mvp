"""
Common exception handling utilities for the presentation layer.
"""
from fastapi import HTTPException, status
from typing import Optional, Any, TypeVar, Dict

T = TypeVar('T')

class APIException:
    """Utility class for handling common API exceptions."""
    
    @staticmethod
    def raise_not_found(message: str = "Resource not found or you don't have access") -> None:
        """Raise a 404 Not Found exception."""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
    
    @staticmethod
    def raise_bad_request(message: str) -> None:
        """Raise a 400 Bad Request exception."""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    @staticmethod
    def raise_server_error(operation: str, error: Exception) -> None:
        """Raise a 500 Internal Server Error exception."""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{operation} error: {str(error)}"
        ) from error
    
    @staticmethod
    def check_result(result: Optional[Any], operation: str) -> None:
        """Check if result exists and has data, raise 404 if not."""
        if not result or not result.data:
            APIException.raise_not_found()
    
    @staticmethod
    def format_response(result: Any) -> Dict[str, Any]:
        """Format successful response with data wrapper."""
        return {"data": result.data[0] if result.data else None}
    
    @staticmethod
    def format_list_response(result: Any) -> Any:
        """Format successful list response."""
        return result.data if result and result.data else [] 