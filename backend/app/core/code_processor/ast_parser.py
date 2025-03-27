import ast
import logging
from typing import Dict, List, Optional, Set, Union
from pathlib import Path
import re
import json

logger = logging.getLogger(__name__)

class ASTParser:
    """Parses code into AST and extracts meaningful information."""
    
    def __init__(self):
        self.typescript_types = {
            'string', 'number', 'boolean', 'any', 'void', 'null', 'undefined',
            'object', 'array', 'function', 'symbol', 'bigint', 'never', 'unknown'
        }
    
    async def parse_file(self, file_path: Path, content: str) -> Dict:
        """
        Parses a code file and extracts detailed information.
        
        Args:
            file_path: Path to the code file
            content: Content of the code file
            
        Returns:
            Dict containing detailed code analysis
        """
        try:
            file_type = self._detect_file_type(file_path)
            
            if file_type == 'python':
                return await self._parse_python(content)
            else:
                return await self._parse_javascript(content, file_type == 'typescript')
                
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return {
                'error': str(e),
                'file_path': str(file_path)
            }
    
    async def _parse_python(self, content: str) -> Dict:
        """Parses Python code and extracts detailed information."""
        tree = ast.parse(content)
        
        analysis = {
            'imports': [],
            'classes': [],
            'functions': [],
            'variables': [],
            'decorators': set(),
            'docstrings': [],
            'type_annotations': set()
        }
        
        for node in ast.walk(tree):
            # Extract imports
            if isinstance(node, ast.Import):
                for name in node.names:
                    analysis['imports'].append({
                        'name': name.name,
                        'alias': name.asname
                    })
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for name in node.names:
                    analysis['imports'].append({
                        'name': f"{module}.{name.name}",
                        'alias': name.asname,
                        'from_import': True
                    })
            
            # Extract classes
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'bases': [self._get_name(base) for base in node.bases],
                    'decorators': [self._get_name(d) for d in node.decorator_list],
                    'methods': [],
                    'class_variables': [],
                    'docstring': ast.get_docstring(node)
                }
                
                # Add class decorators to global set
                analysis['decorators'].update(class_info['decorators'])
                
                # Process class body
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = self._extract_function_info(item)
                        class_info['methods'].append(method_info)
                    elif isinstance(item, ast.AnnAssign):
                        if isinstance(item.target, ast.Name):
                            class_info['class_variables'].append({
                                'name': item.target.id,
                                'type': self._get_annotation(item.annotation)
                            })
                
                analysis['classes'].append(class_info)
            
            # Extract standalone functions
            elif isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.Module):
                func_info = self._extract_function_info(node)
                analysis['functions'].append(func_info)
            
            # Extract module-level variables
            elif isinstance(node, ast.Assign) and isinstance(node.parent, ast.Module):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        analysis['variables'].append({
                            'name': target.id,
                            'value': self._get_value(node.value)
                        })
            
            # Extract type annotations
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.annotation, ast.Name):
                    analysis['type_annotations'].add(node.annotation.id)
                elif isinstance(node.annotation, ast.Subscript):
                    base = self._get_name(node.annotation.value)
                    analysis['type_annotations'].add(base)
        
        # Convert sets to lists for JSON serialization
        analysis['decorators'] = list(analysis['decorators'])
        analysis['type_annotations'] = list(analysis['type_annotations'])
        
        return analysis
    
    async def _parse_javascript(self, content: str, is_typescript: bool = False) -> Dict:
        """Parses JavaScript/TypeScript code and extracts detailed information."""
        analysis = {
            'imports': [],
            'exports': [],
            'classes': [],
            'functions': [],
            'variables': [],
            'interfaces': [] if is_typescript else None,
            'types': [] if is_typescript else None,
            'jsx_components': []
        }
        
        # Extract imports
        import_patterns = [
            (r'import\s+{([^}]+)}\s+from\s+[\'"]([^\'"]+)[\'"]', 'named'),
            (r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', 'default'),
            (r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', 'namespace')
        ]
        
        for pattern, import_type in import_patterns:
            for match in re.finditer(pattern, content):
                if import_type == 'named':
                    imports = [i.strip() for i in match.group(1).split(',')]
                    for imp in imports:
                        name_parts = imp.split(' as ')
                        analysis['imports'].append({
                            'name': name_parts[0].strip(),
                            'alias': name_parts[1].strip() if len(name_parts) > 1 else None,
                            'source': match.group(2),
                            'type': import_type
                        })
                else:
                    analysis['imports'].append({
                        'name': match.group(1),
                        'source': match.group(2),
                        'type': import_type
                    })
        
        # Extract exports
        export_patterns = [
            r'export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)',
            r'export\s+{([^}]+)}'
        ]
        
        for pattern in export_patterns:
            for match in re.finditer(pattern, content):
                if '{' in pattern:
                    exports = [e.strip() for e in match.group(1).split(',')]
                    analysis['exports'].extend(exports)
                else:
                    analysis['exports'].append(match.group(1))
        
        # Extract classes
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{([^}]+)}'
        for match in re.finditer(class_pattern, content):
            class_info = {
                'name': match.group(1),
                'extends': match.group(2),
                'methods': self._extract_js_methods(match.group(3))
            }
            analysis['classes'].append(class_info)
        
        # Extract functions
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*{([^}]+)}',
            r'const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)\s*{([^}]+)}'
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, content):
                func_info = {
                    'name': match.group(1),
                    'body': match.group(2).strip()
                }
                analysis['functions'].append(func_info)
        
        # Extract JSX components
        component_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*{\s*return\s*\(',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\('
        ]
        
        for pattern in component_patterns:
            for match in re.finditer(pattern, content):
                component_info = {
                    'name': match.group(1),
                    'type': 'functional'
                }
                analysis['jsx_components'].append(component_info)
        
        # Extract TypeScript specific information
        if is_typescript:
            # Extract interfaces
            interface_pattern = r'interface\s+(\w+)(?:\s+extends\s+(\w+))?\s*{([^}]+)}'
            for match in re.finditer(interface_pattern, content):
                interface_info = {
                    'name': match.group(1),
                    'extends': match.group(2),
                    'properties': self._extract_ts_properties(match.group(3))
                }
                analysis['interfaces'].append(interface_info)
            
            # Extract types
            type_pattern = r'type\s+(\w+)\s*=\s*([^;]+)'
            for match in re.finditer(type_pattern, content):
                type_info = {
                    'name': match.group(1),
                    'definition': match.group(2).strip()
                }
                analysis['types'].append(type_info)
        
        return analysis
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict:
        """Extracts detailed information from a function definition."""
        return {
            'name': node.name,
            'args': self._get_arguments(node.args),
            'returns': self._get_annotation(node.returns) if hasattr(node, 'returns') else None,
            'decorators': [self._get_name(d) for d in node.decorator_list],
            'docstring': ast.get_docstring(node),
            'is_async': isinstance(node, ast.AsyncFunctionDef)
        }
    
    def _get_arguments(self, args: ast.arguments) -> List[Dict]:
        """Extracts argument information from a function's arguments."""
        arguments = []
        
        # Process positional arguments
        for arg in args.args:
            arg_info = {
                'name': arg.arg,
                'type': self._get_annotation(arg.annotation) if hasattr(arg, 'annotation') else None
            }
            arguments.append(arg_info)
        
        # Process keyword arguments
        if args.kwarg:
            arguments.append({
                'name': args.kwarg.arg,
                'type': 'kwargs'
            })
        
        return arguments
    
    def _get_annotation(self, node: Optional[ast.AST]) -> Optional[str]:
        """Gets the string representation of a type annotation."""
        if node is None:
            return None
        
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_annotation(node.slice)}]"
        
        return None
    
    def _get_name(self, node: ast.AST) -> str:
        """Gets the string representation of a name node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
    
    def _get_value(self, node: ast.AST) -> str:
        """Gets the string representation of a value node."""
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.List):
            return f"[{', '.join(self._get_value(elt) for elt in node.elts)}]"
        elif isinstance(node, ast.Dict):
            keys = [self._get_value(k) for k in node.keys]
            values = [self._get_value(v) for v in node.values]
            return f"{{{', '.join(f'{k}: {v}' for k, v in zip(keys, values))}}}"
        return str(node)
    
    def _extract_js_methods(self, class_body: str) -> List[Dict]:
        """Extracts method information from a JavaScript class body."""
        methods = []
        method_pattern = r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*{([^}]+)}'
        
        for match in re.finditer(method_pattern, class_body):
            method_info = {
                'name': match.group(1),
                'is_async': bool(re.match(r'async\s+', match.group(0))),
                'body': match.group(2).strip()
            }
            methods.append(method_info)
        
        return methods
    
    def _extract_ts_properties(self, interface_body: str) -> List[Dict]:
        """Extracts property information from a TypeScript interface body."""
        properties = []
        property_pattern = r'(\w+)(?:\?)?:\s*([^;]+)'
        
        for match in re.finditer(property_pattern, interface_body):
            property_info = {
                'name': match.group(1),
                'type': match.group(2).strip(),
                'optional': '?' in match.group(0)
            }
            properties.append(property_info)
        
        return properties
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detects the type of code file based on extension."""
        suffix = file_path.suffix.lower()
        if suffix == '.py':
            return 'python'
        elif suffix in ['.ts', '.tsx']:
            return 'typescript'
        elif suffix in ['.js', '.jsx']:
            return 'javascript'
        else:
            return 'unknown' 