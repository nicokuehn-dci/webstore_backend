"""
Code Analyzer
------------
Analyzes code quality, structure, and potential issues.
"""

import ast
import os
import re
from typing import Dict, List, Any
from pathlib import Path


class CodeAnalyzer:
    """Analyzes code quality and structure."""
    
    def __init__(self, config):
        self.config = config
        self.max_line_length = config.get('max_line_length', 88)
        self.max_complexity = config.get('max_complexity', 10)
    
    def analyze_code_quality(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Analyze code quality of a single file."""
        issues = []
        
        try:
            # Parse the AST
            tree = ast.parse(content, filename=file_path)
            
            # Check various code quality metrics
            issues.extend(self._check_line_length(content, file_path))
            issues.extend(self._check_complexity(tree, file_path))
            issues.extend(self._check_imports(tree, file_path))
            issues.extend(self._check_docstrings(tree, file_path))
            issues.extend(self._check_naming_conventions(tree, file_path))
            
        except SyntaxError as e:
            issues.append({
                'type': 'SYNTAX_ERROR',
                'message': str(e),
                'file': file_path,
                'line': e.lineno,
                'severity': 'HIGH'
            })
        
        return issues
    
    def _check_line_length(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Check for lines that are too long."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > self.max_line_length:
                issues.append({
                    'type': 'LINE_TOO_LONG',
                    'message': f'Line too long ({len(line)} > {self.max_line_length} characters)',
                    'file': file_path,
                    'line': i,
                    'severity': 'LOW'
                })
        
        return issues
    
    def _check_complexity(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check cyclomatic complexity of functions."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._calculate_complexity(node)
                if complexity > self.max_complexity:
                    issues.append({
                        'type': 'HIGH_COMPLEXITY',
                        'message': f'Function "{node.name}" has high complexity ({complexity})',
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'MEDIUM'
                    })
        
        return issues
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _check_imports(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check import statements for issues."""
        issues = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append((f"{module}.{alias.name}", node.lineno))
        
        # Check for unused imports (basic check)
        # This is a simplified version - a real implementation would be more sophisticated
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
        
        return issues
    
    def _check_docstrings(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for missing docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    node_type = 'function' if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else 'class'
                    issues.append({
                        'type': 'MISSING_DOCSTRING',
                        'message': f'{node_type.capitalize()} "{node.name}" is missing a docstring',
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'LOW'
                    })
        
        return issues
    
    def _check_naming_conventions(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check naming conventions (PEP 8)."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not self._is_snake_case(node.name):
                    issues.append({
                        'type': 'NAMING_CONVENTION',
                        'message': f'Function "{node.name}" should use snake_case',
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'LOW'
                    })
            elif isinstance(node, ast.ClassDef):
                if not self._is_pascal_case(node.name):
                    issues.append({
                        'type': 'NAMING_CONVENTION',
                        'message': f'Class "{node.name}" should use PascalCase',
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'LOW'
                    })
        
        return issues
    
    def _is_snake_case(self, name: str) -> bool:
        """Check if a name follows snake_case convention."""
        return re.match(r'^[a-z_][a-z0-9_]*$', name) is not None
    
    def _is_pascal_case(self, name: str) -> bool:
        """Check if a name follows PascalCase convention."""
        return re.match(r'^[A-Z][a-zA-Z0-9]*$', name) is not None
    
    def analyze_project_structure(self, project_root: str) -> Dict[str, Any]:
        """Analyze overall project structure."""
        structure_info = {
            'total_files': 0,
            'total_lines': 0,
            'packages': [],
            'missing_init_files': [],
            'large_files': [],
            'duplicate_code': []
        }
        
        for root, dirs, files in os.walk(project_root):
            # Skip virtual environment and cache directories
            dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
            
            python_files = [f for f in files if f.endswith('.py')]
            structure_info['total_files'] += len(python_files)
            
            # Check for missing __init__.py files
            if python_files and '__init__.py' not in files and root != project_root:
                rel_path = os.path.relpath(root, project_root)
                structure_info['missing_init_files'].append(rel_path)
            
            # Count lines and check for large files
            for file in python_files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        structure_info['total_lines'] += lines
                        
                        if lines > 500:  # Flag files with more than 500 lines
                            structure_info['large_files'].append({
                                'file': os.path.relpath(file_path, project_root),
                                'lines': lines
                            })
                except Exception:
                    pass  # Skip files that can't be read
        
        return structure_info
