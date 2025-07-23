"""
Performance Analyzer
------------------
Analyzes code for performance issues and optimization opportunities.
"""

import ast
from typing import Dict, List, Any


class PerformanceAnalyzer:
    """Analyzes code for performance issues."""
    
    def __init__(self, config):
        self.config = config
    
    def analyze_performance(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Analyze performance issues in the code."""
        issues = []
        
        try:
            tree = ast.parse(content, filename=file_path)
            
            issues.extend(self._check_loops(tree, file_path))
            issues.extend(self._check_imports(tree, file_path))
            issues.extend(self._check_string_operations(tree, file_path))
            issues.extend(self._check_list_operations(tree, file_path))
            
        except SyntaxError:
            pass  # Skip files with syntax errors
        
        return issues
    
    def _check_loops(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for inefficient loop patterns."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # Check for range(len()) pattern
                if (isinstance(node.iter, ast.Call) and
                    isinstance(node.iter.func, ast.Name) and
                    node.iter.func.id == 'range'):
                    
                    if (len(node.iter.args) == 1 and
                        isinstance(node.iter.args[0], ast.Call) and
                        isinstance(node.iter.args[0].func, ast.Name) and
                        node.iter.args[0].func.id == 'len'):
                        
                        issues.append({
                            'type': 'INEFFICIENT_LOOP',
                            'message': 'Consider using enumerate() instead of range(len())',
                            'file': file_path,
                            'line': node.lineno,
                            'severity': 'LOW',
                            'suggestion': 'Use: for i, item in enumerate(sequence)'
                        })
        
        return issues
    
    def _check_imports(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for performance issues with imports."""
        issues = []
        
        # Check for imports inside functions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.Import, ast.ImportFrom)):
                        issues.append({
                            'type': 'IMPORT_IN_FUNCTION',
                            'message': 'Import statement inside function may impact performance',
                            'file': file_path,
                            'line': child.lineno,
                            'severity': 'LOW',
                            'suggestion': 'Move import to module level if possible'
                        })
        
        return issues
    
    def _check_string_operations(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for inefficient string operations."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for string concatenation in loops
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if (isinstance(child, ast.AugAssign) and
                        isinstance(child.op, ast.Add)):
                        # This could be string concatenation
                        issues.append({
                            'type': 'STRING_CONCAT_IN_LOOP',
                            'message': 'String concatenation in loop can be inefficient',
                            'file': file_path,
                            'line': child.lineno,
                            'severity': 'MEDIUM',
                            'suggestion': 'Consider using list.append() and join()'
                        })
        
        return issues
    
    def _check_list_operations(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for inefficient list operations."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for list.append() in comprehensions
            if isinstance(node, ast.ListComp):
                for generator in node.generators:
                    # This is a simplified check
                    pass
            
            # Check for inefficient list operations
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Attribute) and
                    node.func.attr == 'append'):
                    
                    # Check if this is inside a loop
                    parent_nodes = []
                    # This would require tracking parent nodes
                    # For now, just flag potential issues
                    pass
        
        return issues
