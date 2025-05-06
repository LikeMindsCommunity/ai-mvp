"""
Repository source code ingestion utility.

This module provides functions to ingest code from a cloned GitHub repository
using the gitingest package, making it accessible for LLM-based analysis.
"""

import os
import subprocess
import asyncio
from typing import Optional, Tuple, Callable, Awaitable
import logging

logger = logging.getLogger(__name__)

def ingest_repo(project_id: str) -> Tuple[bool, str]:
    """
    Ingest source code from a cloned GitHub repository.
    
    Args:
        project_id (str): The project ID of the cloned repository
        
    Returns:
        Tuple[bool, str]: Success status and path to ingest.txt file or error message
    """
    try:
        # Define paths
        repo_path = os.path.join("output", project_id, "integration")
        output_path = os.path.join(repo_path, "ingest.txt")
        
        # Check if repo exists
        if not os.path.exists(repo_path):
            return False, f"Repository path does not exist: {repo_path}"
        
        # Run gitingest command
        logger.info(f"Ingesting repository for project {project_id}")
        cmd = ["gitingest", repo_path, "--output", output_path]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Check if ingest file was created
        if not os.path.exists(output_path):
            return False, f"Ingest file was not created: {output_path}"
        
        logger.info(f"Successfully ingested repository for project {project_id}")
        return True, output_path
        
    except subprocess.CalledProcessError as e:
        error_message = f"Error ingesting repository: {e.stderr}"
        logger.error(error_message)
        return False, error_message
    except Exception as e:
        error_message = f"Unexpected error during repository ingestion: {str(e)}"
        logger.error(error_message)
        return False, error_message

async def ingest_repo_async(project_id: str, on_status: Optional[Callable[[str], Awaitable[None]]] = None) -> Tuple[bool, str]:
    """
    Asynchronously ingest source code from a cloned GitHub repository.
    
    Args:
        project_id (str): The project ID of the cloned repository
        on_status (Optional[Callable]): Callback for status updates
        
    Returns:
        Tuple[bool, str]: Success status and path to ingest.txt file or error message
    """
    if on_status:
        await on_status(f"Starting repository ingestion for project {project_id}")
    
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ingest_repo, project_id)

def get_ingest_text(project_id: str) -> Optional[str]:
    """
    Get the ingested text for a project.
    
    Args:
        project_id (str): The project ID of the cloned repository
        
    Returns:
        Optional[str]: The ingested text or None if not found
    """
    try:
        ingest_path = os.path.join("output", project_id, "integration", "ingest.txt")
        
        # If ingest file doesn't exist, try to create it
        if not os.path.exists(ingest_path):
            success, result = ingest_repo(project_id)
            if not success:
                logger.error(f"Failed to create ingest file: {result}")
                return None
            ingest_path = result
        
        # Read the ingest file
        with open(ingest_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        logger.error(f"Error reading ingest file: {str(e)}")
        return None

async def get_ingest_text_async(project_id: str, on_status: Optional[Callable[[str], Awaitable[None]]] = None) -> Optional[str]:
    """
    Asynchronously get the ingested text for a project.
    
    Args:
        project_id (str): The project ID of the cloned repository
        on_status (Optional[Callable]): Callback for status updates
        
    Returns:
        Optional[str]: The ingested text or None if not found
    """
    if on_status:
        await on_status(f"Retrieving ingested text for project {project_id}")
    
    # Check if ingest file exists
    ingest_path = os.path.join("output", project_id, "integration", "ingest.txt")
    
    # If ingest file doesn't exist, try to create it
    if not os.path.exists(ingest_path):
        if on_status:
            await on_status(f"Ingest file not found, creating it for project {project_id}")
        
        success, result = await ingest_repo_async(project_id, on_status)
        if not success:
            if on_status:
                await on_status(f"Failed to create ingest file: {result}")
            return None
        ingest_path = result
    
    # Read the ingest file in a non-blocking way
    try:
        loop = asyncio.get_event_loop()
        
        def read_file():
            with open(ingest_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        return await loop.run_in_executor(None, read_file)
    except Exception as e:
        if on_status:
            await on_status(f"Error reading ingest file: {str(e)}")
        return None

async def ensure_ingest_exists(project_id: str, on_status: Optional[Callable[[str], Awaitable[None]]] = None) -> Tuple[bool, str]:
    """
    Ensure that an ingest file exists for the given project, creating it if necessary.
    
    Args:
        project_id (str): The project ID
        on_status (Optional[Callable]): Callback for status updates
        
    Returns:
        Tuple[bool, str]: Success flag and message
    """
    ingest_path = os.path.join("output", project_id, "integration", "ingest.txt")
    
    # If ingest file already exists, we're good
    if os.path.exists(ingest_path):
        if on_status:
            await on_status(f"Ingest file already exists for project {project_id}")
        return True, "Ingest file already exists"
    
    # Otherwise, create it
    return await ingest_repo_async(project_id, on_status) 