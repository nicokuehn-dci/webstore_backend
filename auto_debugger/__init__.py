"""
Auto Debugger Service
-------------------
Automated debugging and issue detection service for the WebStore application.
"""

__version__ = "1.0.0"
__author__ = "WebStore Development Team"

from .src.debugger import AutoDebugger
from .src.analyzers.code_analyzer import CodeAnalyzer
from .src.analyzers.error_detector import ErrorDetector
from .src.handlers.log_handler import LogHandler

__all__ = [
    'AutoDebugger',
    'CodeAnalyzer', 
    'ErrorDetector',
    'LogHandler'
]
