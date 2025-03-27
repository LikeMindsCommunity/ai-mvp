import ast
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class CodeChunker:
    """Breaks down code files into meaningful chunks for embedding."""
    
    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size
        self.comment_patterns = {
            'python': {
                'single': r'#.*?$',
                'multi': r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
            },
            'javascript': {
                'single': r'//.*?$',
                'multi': r'/\*[\s\S]*?\*/'
            }
        }
    
    async def chunk_file(self, file_path: Path, content: str) -> List[Dict]:
        """
        Chunks a code file into meaningful segments.
        
        Args:
            file_path: Path to the code file
            content: Content of the code file
            
        Returns:
            List of chunks with metadata
        """
        try:
            file_type = self._detect_file_type(file_path)
            chunks = []
            
            # Extract comments first
            comments = self._extract_comments(content, file_type)
            
            # Try parsing as Python first
            try:
                tree = ast.parse(content)
                chunks.extend(self._chunk_python_ast(tree, content))
            except SyntaxError:
                # If not Python, use regex-based chunking for JavaScript/TypeScript
                chunks.extend(self._chunk_javascript(content))
            
            # Add comment chunks
            chunks.extend(self._create_comment_chunks(comments))
            
            # Add metadata to chunks
            for chunk in chunks:
                chunk.update({
                    'file_path': str(file_path),
                    'file_type': file_type
                })
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking file {file_path}: {str(e)}")
            return [{
                'file_path': str(file_path),
                'error': str(e),
                'content': content[:self.max_chunk_size]
            }]
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detects the type of code file based on extension."""
        suffix = file_path.suffix.lower()
        if suffix in ['.py']:
            return 'python'
        elif suffix in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript'
        else:
            return 'unknown'
    
    def _extract_comments(self, content: str, file_type: str) -> List[str]:
        """Extracts comments from code content."""
        comments = []
        patterns = self.comment_patterns.get(file_type, self.comment_patterns['python'])
        
        # Extract single-line comments
        single_line = re.finditer(patterns['single'], content, re.MULTILINE)
        comments.extend(match.group(0) for match in single_line)
        
        # Extract multi-line comments
        multi_line = re.finditer(patterns['multi'], content, re.MULTILINE)
        comments.extend(match.group(0) for match in multi_line)
        
        return comments
    
    def _chunk_python_ast(self, tree: ast.AST, content: str) -> List[Dict]:
        """Creates chunks from Python AST nodes."""
        chunks = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                # Get the source code for this node
                start_line = node.lineno
                end_line = self._get_node_end_line(node)
                
                # Extract the lines
                lines = content.split('\n')[start_line-1:end_line]
                chunk_content = '\n'.join(lines)
                
                # Create chunk with metadata
                chunk = {
                    'type': 'class' if isinstance(node, ast.ClassDef) else 'function',
                    'name': node.name,
                    'content': chunk_content,
                    'start_line': start_line,
                    'end_line': end_line
                }
                
                # Split if too large
                if len(chunk_content) > self.max_chunk_size:
                    sub_chunks = self._split_large_chunk(chunk)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(chunk)
        
        return chunks
    
    def _chunk_javascript(self, content: str) -> List[Dict]:
        """Creates chunks from JavaScript/TypeScript code using regex patterns."""
        chunks = []
        
        # Patterns for different code constructs
        patterns = {
            'class': r'class\s+(\w+)[\s\S]*?{[\s\S]*?}(?=\s*(?:export|class|function|const|let|var|$))',
            'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))[\s\S]*?{[\s\S]*?}(?=\s*(?:export|class|function|const|let|var|$))',
            'component': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))[\s\S]*?{[\s\S]*?return\s*\([\s\S]*?\)[\s\S]*?}(?=\s*(?:export|class|function|const|let|var|$))'
        }
        
        for chunk_type, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            
            for match in matches:
                chunk_content = match.group(0)
                name = next(n for n in match.groups() if n is not None)
                
                chunk = {
                    'type': chunk_type,
                    'name': name,
                    'content': chunk_content,
                    'start_line': content[:match.start()].count('\n') + 1,
                    'end_line': content[:match.end()].count('\n') + 1
                }
                
                if len(chunk_content) > self.max_chunk_size:
                    sub_chunks = self._split_large_chunk(chunk)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(chunk)
        
        return chunks
    
    def _create_comment_chunks(self, comments: List[str]) -> List[Dict]:
        """Creates chunks from extracted comments."""
        chunks = []
        current_chunk = []
        current_size = 0
        
        for comment in comments:
            if current_size + len(comment) > self.max_chunk_size:
                if current_chunk:
                    chunks.append({
                        'type': 'comment',
                        'content': '\n'.join(current_chunk)
                    })
                current_chunk = [comment]
                current_size = len(comment)
            else:
                current_chunk.append(comment)
                current_size += len(comment)
        
        if current_chunk:
            chunks.append({
                'type': 'comment',
                'content': '\n'.join(current_chunk)
            })
        
        return chunks
    
    def _split_large_chunk(self, chunk: Dict) -> List[Dict]:
        """Splits a large chunk into smaller ones."""
        content = chunk['content']
        chunks = []
        
        # Split by lines first
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        chunk_index = 1
        
        for line in lines:
            if current_size + len(line) > self.max_chunk_size:
                if current_chunk:
                    chunks.append({
                        **chunk,
                        'content': '\n'.join(current_chunk),
                        'part': chunk_index
                    })
                    chunk_index += 1
                current_chunk = [line]
                current_size = len(line)
            else:
                current_chunk.append(line)
                current_size += len(line)
        
        if current_chunk:
            chunks.append({
                **chunk,
                'content': '\n'.join(current_chunk),
                'part': chunk_index
            })
        
        return chunks
    
    def _get_node_end_line(self, node: ast.AST) -> int:
        """Gets the end line number of an AST node."""
        if hasattr(node, 'end_lineno'):
            return node.end_lineno
        
        # Fallback: find the max line number of all child nodes
        max_line = node.lineno
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                max_line = max(max_line, child.lineno)
            if hasattr(child, 'end_lineno'):
                max_line = max(max_line, child.end_lineno)
        
        return max_line 