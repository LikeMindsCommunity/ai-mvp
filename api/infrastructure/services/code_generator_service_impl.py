from typing import Optional, Dict, Callable
from code_generator.config.settings import Settings
from code_generator.core.generator import CodeGenerator
from api.domain import CodeGeneratorService

class CodeGeneratorServiceImpl(CodeGeneratorService):
    """Implementation of the code generator service."""
    
    def __init__(self):
        """Initialize the service with settings."""
        self.settings = Settings()
        self.generator = CodeGenerator(self.settings)
    
    async def generate_project(self, user_query: str, on_chunk: Callable[[Dict], None]) -> Optional[Dict]:
        """
        Generate a project based on user query.
        
        Args:
            user_query (str): The user's input query
            on_chunk (Callable[[Dict], None]): Callback function to handle each chunk of output
            
        Returns:
            Optional[Dict]: The generated project data or None if generation failed
        """
        try:
            # Create project using the generator
            success = await self.generator.create_project(user_query, on_chunk)
            return {"success": success}
        except Exception as e:
            await on_chunk({
                "type": "Error",
                "value": str(e)
            })
            return None 