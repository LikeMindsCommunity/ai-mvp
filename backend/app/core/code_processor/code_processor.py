import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
import asyncio
import json

from .code_analyzer import CodeAnalyzer
from .code_chunker import CodeChunker
from .ast_parser import ASTParser

logger = logging.getLogger(__name__)

class CodeProcessor:
    """Main processor class that orchestrates code analysis, chunking, and AST parsing."""
    
    def __init__(self, max_chunk_size: int = 1000):
        self.analyzer = CodeAnalyzer()
        self.chunker = CodeChunker(max_chunk_size=max_chunk_size)
        self.ast_parser = ASTParser()
        
    async def process_file(self, file_path: Path) -> Dict:
        """
        Processes a single code file, extracting all relevant information.
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Dict containing all processed information including:
            - analysis results
            - code chunks
            - AST information
            - metadata
        """
        try:
            # Read file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Process file in parallel
            analysis_task = self.analyzer.analyze_file(file_path)
            chunks_task = self.chunker.chunk_file(file_path, content)
            ast_task = self.ast_parser.parse_file(file_path, content)
            
            # Wait for all tasks to complete
            analysis, chunks, ast_info = await asyncio.gather(
                analysis_task,
                chunks_task,
                ast_task
            )
            
            # Combine results
            result = {
                'file_path': str(file_path),
                'analysis': analysis,
                'chunks': chunks,
                'ast_info': ast_info,
                'metadata': {
                    'size': len(content),
                    'num_lines': len(content.splitlines()),
                    'file_type': self._get_file_type(file_path)
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return {
                'file_path': str(file_path),
                'error': str(e)
            }
    
    async def process_directory(self, dir_path: Path, exclude_patterns: Optional[List[str]] = None) -> List[Dict]:
        """
        Processes all code files in a directory recursively.
        
        Args:
            dir_path: Path to the directory
            exclude_patterns: List of glob patterns to exclude
            
        Returns:
            List of processing results for each file
        """
        try:
            results = []
            exclude_patterns = exclude_patterns or ['node_modules/**', 'venv/**', '**/__pycache__/**']
            
            # Get all code files
            code_files = []
            for ext in ['.py', '.js', '.jsx', '.ts', '.tsx']:
                code_files.extend(dir_path.rglob(f'*{ext}'))
            
            # Filter out excluded files
            from fnmatch import fnmatch
            filtered_files = []
            for file in code_files:
                if not any(fnmatch(str(file), pattern) for pattern in exclude_patterns):
                    filtered_files.append(file)
            
            # Process all files in parallel
            tasks = [self.process_file(file) for file in filtered_files]
            results = await asyncio.gather(*tasks)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing directory {dir_path}: {str(e)}")
            return [{
                'directory': str(dir_path),
                'error': str(e)
            }]
    
    async def process_repository(self, repo_path: Path) -> Dict:
        """
        Processes an entire code repository, organizing results by directory structure.
        
        Args:
            repo_path: Path to the repository root
            
        Returns:
            Dict containing organized processing results and repository-level analysis
        """
        try:
            # Process all files
            results = await self.process_directory(repo_path)
            
            # Organize results by directory
            organized_results = {}
            for result in results:
                if 'error' not in result:
                    path = Path(result['file_path'])
                    relative_path = path.relative_to(repo_path)
                    parts = relative_path.parts
                    
                    # Build nested dictionary structure
                    current = organized_results
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = result
            
            # Generate repository-level analysis
            repo_analysis = self._analyze_repository(results)
            
            return {
                'repository_path': str(repo_path),
                'analysis': repo_analysis,
                'files': organized_results
            }
            
        except Exception as e:
            logger.error(f"Error processing repository {repo_path}: {str(e)}")
            return {
                'repository_path': str(repo_path),
                'error': str(e)
            }
    
    def _analyze_repository(self, file_results: List[Dict]) -> Dict:
        """Generates repository-level analysis from individual file results."""
        analysis = {
            'total_files': len(file_results),
            'total_lines': 0,
            'languages': {},
            'dependencies': set(),
            'components': [],
            'sdk_usage': []
        }
        
        for result in file_results:
            if 'error' not in result:
                # Count lines
                analysis['total_lines'] += result['metadata']['num_lines']
                
                # Track languages
                file_type = result['metadata']['file_type']
                analysis['languages'][file_type] = analysis['languages'].get(file_type, 0) + 1
                
                # Collect dependencies
                if 'dependencies' in result['analysis']:
                    analysis['dependencies'].update(result['analysis']['dependencies'])
                
                # Track components
                if 'components' in result['analysis']:
                    analysis['components'].extend(result['analysis']['components'])
                
                # Collect SDK usage
                if 'sdk_usage' in result['analysis']:
                    analysis['sdk_usage'].extend(result['analysis']['sdk_usage'])
        
        # Convert sets to lists for JSON serialization
        analysis['dependencies'] = list(analysis['dependencies'])
        
        return analysis
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determines the programming language/type of a file."""
        suffix = file_path.suffix.lower()
        
        if suffix == '.py':
            return 'python'
        elif suffix in ['.js', '.jsx']:
            return 'javascript'
        elif suffix in ['.ts', '.tsx']:
            return 'typescript'
        else:
            return 'unknown' 