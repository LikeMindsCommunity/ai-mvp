from typing import Optional, Dict
from fastapi import WebSocket
from code_generator.core import CodeGenerator
from code_generator.config import Settings
from api.domain import CodeGeneratorService

class CodeGeneratorServiceImpl(CodeGeneratorService):
    """Implementation of the code generator service."""
    
    def __init__(self):
        """Initialize the service with settings."""
        self.settings = Settings()
        self.generator = CodeGenerator(self.settings)
    
    async def generate_project(self, user_query: str, websocket: WebSocket) -> Optional[Dict]:
        """
        Generate a project based on user query.
        
        Args:
            user_query (str): The user's input query
            websocket (WebSocket): WebSocket connection for sending updates
            
        Returns:
            Optional[Dict]: The generated project data or None if generation failed
        """
        try:
            # Create project using the generator
            success = await self.generator.create_project(user_query, websocket)
            return {"success": success}
        except Exception as e:
            await websocket.send_json({
                "type": "Error",
                "value": str(e)
            })
            return None 