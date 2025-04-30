"""
Main entry point for the code generator.
"""

import sys
import asyncio
import os
from code_generator.config.settings import Settings
from code_generator.core.generator import CodeGenerator

async def main():
    """Main entry point for the code generator."""
    try:
        # Load settings
        settings = Settings()
        
        # Initialize generator
        generator = CodeGenerator(settings)
        
        # Run the generator
        generator.run()
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 