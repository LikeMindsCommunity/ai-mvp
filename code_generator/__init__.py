"""
Code Generator for LikeMinds Android Feed SDK

This package provides an interactive interface to generate code for the LikeMinds Android Feed SDK
using the Gemini 2.5 Pro model. It uses the combined documentation as context to generate
accurate and relevant code snippets based on user requests.
"""

from code_generator.core import CodeGenerator
from code_generator.config.settings import Settings
from code_generator.utils import DocumentationManager

__version__ = "0.1.0"
__all__ = ["CodeGenerator", "Settings", "DocumentationManager"] 