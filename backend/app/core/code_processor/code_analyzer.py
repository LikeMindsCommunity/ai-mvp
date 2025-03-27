import ast
import logging
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """Analyzes code files to extract structure, dependencies, and patterns."""
    
    def __init__(self):
        self.import_patterns = {
            'react_native': [
                r'import\s+.*?react-native.*?',
                r'from\s+.*?react-native.*?import',
                r'require\(.*?react-native.*?\)'
            ],
            'react': [
                r'import\s+.*?react.*?',
                r'from\s+.*?react.*?import',
                r'require\(.*?react.*?\)'
            ],
            'sdk': [
                r'import\s+.*?likeminds.*?',
                r'from\s+.*?likeminds.*?import',
                r'require\(.*?likeminds.*?\)'
            ]
        }
        
    async def analyze_file(self, file_path: Path) -> Dict:
        """
        Analyzes a single code file and extracts relevant information.
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Dict containing analysis results including:
            - imports
            - dependencies
            - components
            - functions
            - classes
            - sdk_usage
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Basic file info
            analysis = {
                'file_path': str(file_path),
                'imports': [],
                'dependencies': set(),
                'components': [],
                'functions': [],
                'classes': [],
                'sdk_usage': [],
                'platform_type': self._detect_platform(content)
            }
            
            # Parse AST
            try:
                tree = ast.parse(content)
                analysis.update(self._analyze_ast(tree))
            except SyntaxError:
                # Handle non-Python files
                analysis.update(self._analyze_javascript(content))
            
            # Extract SDK usage
            analysis['sdk_usage'] = self._extract_sdk_usage(content)
            
            # Clean up sets to lists for JSON serialization
            analysis['dependencies'] = list(analysis['dependencies'])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {
                'file_path': str(file_path),
                'error': str(e)
            }
    
    def _analyze_ast(self, tree: ast.AST) -> Dict:
        """Analyzes Python AST to extract code information."""
        analysis = {
            'imports': [],
            'dependencies': set(),
            'components': [],
            'functions': [],
            'classes': []
        }
        
        for node in ast.walk(tree):
            # Extract imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        analysis['imports'].append(name.name)
                        analysis['dependencies'].add(name.name.split('.')[0])
                else:
                    if node.module:
                        analysis['imports'].append(node.module)
                        analysis['dependencies'].add(node.module.split('.')[0])
            
            # Extract classes
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'methods': [],
                    'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
                }
                
                # Check if it's likely a React/React Native component
                if 'Component' in str(node.bases) or any(d in ['component', 'Component'] for d in class_info['decorators']):
                    analysis['components'].append(class_info)
                else:
                    analysis['classes'].append(class_info)
            
            # Extract functions
            elif isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
                }
                analysis['functions'].append(func_info)
        
        return analysis
    
    def _analyze_javascript(self, content: str) -> Dict:
        """Analyzes JavaScript/TypeScript code using regex patterns."""
        analysis = {
            'imports': [],
            'dependencies': set(),
            'components': [],
            'functions': [],
            'classes': []
        }
        
        # Extract imports
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import\s+[\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                module = match.group(1)
                analysis['imports'].append(module)
                analysis['dependencies'].add(module.split('/')[0])
        
        # Extract React components
        component_patterns = [
            r'class\s+(\w+)\s+extends\s+(?:React\.)?Component',
            r'function\s+(\w+)\s*\([^)]*\)\s*{\s*return\s*<',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*<'
        ]
        
        for pattern in component_patterns:
            for match in re.finditer(pattern, content):
                component_name = match.group(1)
                analysis['components'].append({
                    'name': component_name,
                    'type': 'class' if 'class' in pattern else 'functional'
                })
        
        # Extract other functions
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                if not any(c['name'] == func_name for c in analysis['components']):
                    analysis['functions'].append({
                        'name': func_name
                    })
        
        return analysis
    
    def _detect_platform(self, content: str) -> str:
        """Detects the platform (React Native, React, Other) from the code."""
        for platform, patterns in self.import_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    return platform
        return 'unknown'
    
    def _extract_sdk_usage(self, content: str) -> List[Dict]:
        """Extracts SDK usage patterns from the code."""
        sdk_usages = []
        
        # Look for SDK imports
        sdk_import_matches = []
        for pattern in self.import_patterns['sdk']:
            sdk_import_matches.extend(re.finditer(pattern, content))
        
        # Look for SDK component usage
        sdk_component_pattern = r'<(LikeMinds\w+)[^>]*>'
        sdk_component_matches = re.finditer(sdk_component_pattern, content)
        
        # Look for SDK hook usage
        sdk_hook_pattern = r'use(LikeMinds\w+)'
        sdk_hook_matches = re.finditer(sdk_hook_pattern, content)
        
        # Process matches
        for match in sdk_import_matches:
            sdk_usages.append({
                'type': 'import',
                'value': match.group(0).strip()
            })
            
        for match in sdk_component_matches:
            sdk_usages.append({
                'type': 'component',
                'value': match.group(1)
            })
            
        for match in sdk_hook_matches:
            sdk_usages.append({
                'type': 'hook',
                'value': match.group(0)
            })
            
        return sdk_usages 