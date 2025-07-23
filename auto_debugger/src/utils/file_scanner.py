"""
File Scanner
-----------
Scans project files for analysis.
"""

import os
from typing import List


class FileScanner:
    """Scans and filters project files."""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.excluded_dirs = {'venv', '__pycache__', '.git', 'node_modules', '.mypy_cache'}
        self.python_extensions = {'.py'}
    
    def get_python_files(self) -> List[str]:
        """Get all Python files in the project."""
        python_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove excluded directories from search
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            # Find Python files
            for file in files:
                if any(file.endswith(ext) for ext in self.python_extensions):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)
        
        return python_files
    
    def get_modified_files(self, since_timestamp: float) -> List[str]:
        """Get files modified since a specific timestamp."""
        modified_files = []
        
        for file_path in self.get_python_files():
            try:
                mtime = os.path.getmtime(file_path)
                if mtime > since_timestamp:
                    modified_files.append(file_path)
            except OSError:
                pass  # Skip files that can't be accessed
        
        return modified_files
    
    def is_excluded(self, file_path: str) -> bool:
        """Check if a file should be excluded from analysis."""
        path_parts = file_path.split(os.sep)
        return any(part in self.excluded_dirs for part in path_parts)
    
    def get_project_structure(self) -> dict:
        """Get a summary of the project structure."""
        structure = {
            'total_files': 0,
            'python_files': 0,
            'directories': 0,
            'largest_file': {'path': '', 'size': 0},
            'file_types': {}
        }
        
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            structure['directories'] += len(dirs)
            structure['total_files'] += len(files)
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Count by extension
                _, ext = os.path.splitext(file)
                ext = ext.lower()
                structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
                
                # Track Python files
                if ext == '.py':
                    structure['python_files'] += 1
                
                # Track largest file
                try:
                    size = os.path.getsize(file_path)
                    if size > structure['largest_file']['size']:
                        structure['largest_file'] = {
                            'path': os.path.relpath(file_path, self.project_root),
                            'size': size
                        }
                except OSError:
                    pass
        
        return structure
