"""
Log Handler
----------
Handles logging for the auto debugger service.
"""

import logging
import os
from datetime import datetime
from typing import Any


class LogHandler:
    """Handles logging for the debugger service."""
    
    def __init__(self, config):
        self.config = config
        self.log_level = config.get('log_level', 'INFO')
        self.log_file = config.get('log_file', 'auto_debugger/logs/debugger.log')
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('auto_debugger')
        self.logger.setLevel(getattr(logging, self.log_level.upper()))
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.log_level.upper()))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def log_analysis_result(self, result: dict):
        """Log analysis results."""
        timestamp = result.get('timestamp', datetime.now().isoformat())
        errors = len(result.get('errors', []))
        warnings = len(result.get('warnings', []))
        
        self.info(f"Analysis completed at {timestamp}: {errors} errors, {warnings} warnings")
        
        # Log critical errors
        for error in result.get('errors', []):
            if error.get('severity') == 'CRITICAL':
                self.error(f"CRITICAL: {error.get('message')} in {error.get('file')}:{error.get('line')}")
    
    def get_log_file_path(self) -> str:
        """Get the path to the log file."""
        return self.log_file
