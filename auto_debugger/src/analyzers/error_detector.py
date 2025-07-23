"""
Error Detector
-------------
Detects and analyzes errors in Python code.
"""

import ast
import sys
import traceback
import re
from typing import Dict, List, Any, Optional


class ErrorDetector:
    """Detects various types of errors in Python code."""
    
    def __init__(self, config):
        self.config = config
    
    def check_syntax(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Check for syntax errors in the code."""
        errors = []
        
        try:
            ast.parse(content, filename=file_path)
        except SyntaxError as e:
            errors.append({
                'type': 'SYNTAX_ERROR',
                'message': str(e.msg),
                'file': file_path,
                'line': e.lineno or 0,
                'column': e.offset or 0,
                'severity': 'CRITICAL',
                'suggestion': self._get_syntax_error_suggestion(e)
            })
        except Exception as e:
            errors.append({
                'type': 'PARSE_ERROR',
                'message': f'Failed to parse file: {str(e)}',
                'file': file_path,
                'line': 0,
                'severity': 'HIGH'
            })
        
        return errors
    
    def _get_syntax_error_suggestion(self, error: SyntaxError) -> str:
        """Get a helpful suggestion for fixing syntax errors."""
        msg = error.msg.lower() if error.msg else ""
        
        if "invalid syntax" in msg:
            return "Check for missing colons, parentheses, or brackets"
        elif "unexpected eof" in msg:
            return "Check for unclosed parentheses, brackets, or quotes"
        elif "indentation" in msg:
            return "Check indentation - use 4 spaces per level"
        elif "unindent" in msg:
            return "Fix indentation to match outer indentation level"
        else:
            return "Review the syntax around the indicated line"
    
    def detect_runtime_errors(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """Detect potential runtime errors through static analysis."""
        errors = []
        
        try:
            tree = ast.parse(content, filename=file_path)
            
            # Check for common runtime error patterns
            errors.extend(self._check_undefined_variables(tree, file_path))
            errors.extend(self._check_attribute_errors(tree, file_path))
            errors.extend(self._check_import_errors(tree, file_path))
            errors.extend(self._check_type_errors(tree, file_path))
            
        except SyntaxError:
            pass  # Syntax errors are handled separately
        
        return errors
    
    def _check_undefined_variables(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for potentially undefined variables."""
        errors = []
        defined_names = set()
        used_names = []
        
        # Collect defined names
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    defined_names.add(name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    defined_names.add(name)
        
        # Check used names
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in defined_names and not self._is_builtin(node.id):
                    errors.append({
                        'type': 'UNDEFINED_VARIABLE',
                        'message': f'Variable "{node.id}" may be undefined',
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'MEDIUM'
                    })
        
        return errors
    
    def _check_attribute_errors(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for potential attribute errors."""
        errors = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                # Check for common attribute error patterns
                if isinstance(node.value, ast.Name):
                    # Check for None.attribute access
                    if node.value.id == 'None':
                        errors.append({
                            'type': 'ATTRIBUTE_ERROR',
                            'message': f'Accessing attribute "{node.attr}" on None',
                            'file': file_path,
                            'line': node.lineno,
                            'severity': 'HIGH'
                        })
        
        return errors
    
    def _check_import_errors(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for potential import errors."""
        errors = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Check for relative imports outside of packages
                if isinstance(node, ast.ImportFrom) and node.level > 0:
                    # This is a relative import
                    if not self._is_in_package(file_path):
                        errors.append({
                            'type': 'IMPORT_ERROR',
                            'message': 'Relative import used outside of package',
                            'file': file_path,
                            'line': node.lineno,
                            'severity': 'MEDIUM'
                        })
        
        return errors
    
    def _check_type_errors(self, tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
        """Check for potential type errors."""
        errors = []
        
        for node in ast.walk(tree):
            # Check for string + number operations
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    # This is a simplified check - real implementation would be more sophisticated
                    pass
        
        return errors
    
    def _is_builtin(self, name: str) -> bool:
        """Check if a name is a Python builtin."""
        return name in dir(__builtins__)
    
    def _is_in_package(self, file_path: str) -> bool:
        """Check if a file is part of a Python package."""
        import os
        directory = os.path.dirname(file_path)
        return os.path.exists(os.path.join(directory, '__init__.py'))
    
    def analyze_traceback(self, traceback_str: str) -> Dict[str, Any]:
        """Analyze an error traceback and provide insights."""
        analysis = {
            'error_type': 'UNKNOWN',
            'error_message': '',
            'file': '',
            'line': 0,
            'suggestions': [],
            'severity': 'HIGH'
        }
        
        try:
            lines = traceback_str.strip().split('\n')
            
            # Find the actual error line (usually the last line)
            for line in reversed(lines):
                if ':' in line and any(err in line for err in [
                    'Error', 'Exception', 'Warning'
                ]):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        analysis['error_type'] = parts[0].strip()
                        analysis['error_message'] = parts[1].strip()
                    break
            
            # Find file and line information
            for line in lines:
                if 'File "' in line and 'line' in line:
                    match = re.search(r'File "([^"]+)", line (\d+)', line)
                    if match:
                        analysis['file'] = match.group(1)
                        analysis['line'] = int(match.group(2))
                    break
            
            # Generate suggestions based on error type
            analysis['suggestions'] = self._get_error_suggestions(analysis['error_type'])
            
        except Exception:
            analysis['error_message'] = 'Failed to parse traceback'
        
        return analysis
    
    def _get_error_suggestions(self, error_type: str) -> List[str]:
        """Get suggestions for fixing common errors."""
        suggestions = {
            'NameError': [
                'Check if the variable is defined before use',
                'Check for typos in variable names',
                'Ensure proper import statements'
            ],
            'AttributeError': [
                'Check if the object has the requested attribute',
                'Ensure the object is not None',
                'Check for typos in attribute names'
            ],
            'ImportError': [
                'Check if the module is installed',
                'Verify the module path is correct',
                'Check for circular imports'
            ],
            'IndentationError': [
                'Use consistent indentation (4 spaces recommended)',
                'Check for mixing tabs and spaces',
                'Ensure proper nesting of code blocks'
            ],
            'SyntaxError': [
                'Check for missing colons, parentheses, or brackets',
                'Verify proper quote matching',
                'Check for invalid characters'
            ],
            'TypeError': [
                'Check argument types and counts',
                'Ensure operations are valid for the data types',
                'Check for None values where objects are expected'
            ]
        }
        
        return suggestions.get(error_type, ['Review the error message and context'])
