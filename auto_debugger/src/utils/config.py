"""
Configuration Manager
-------------------
Manages configuration for the auto debugger.
"""

import json
import os
from typing import Dict, Any


class DebugConfig:
    """Manages debugger configuration."""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or 'auto_debugger/config/debug_config.json'
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Return default configuration
        default_config = {
            'log_level': 'INFO',
            'log_file': 'auto_debugger/logs/debugger.log',
            'reports_dir': 'auto_debugger/reports',
            'max_line_length': 88,
            'max_complexity': 10,
            'scan_interval': 30,
            'excluded_dirs': ['venv', '__pycache__', '.git', 'node_modules'],
            'file_extensions': ['.py'],
            'monitoring': {
                'enabled': True,
                'interval': 30,
                'auto_fix': False
            },
            'analysis': {
                'syntax_check': True,
                'code_quality': True,
                'performance': True,
                'security': False
            },
            'reporting': {
                'generate_html': True,
                'keep_reports': 10,
                'email_alerts': False
            }
        }
        
        # Save default config
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config_data: Dict[str, Any]):
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value):
        """Set configuration value."""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config_data)
    
    def reload(self):
        """Reload configuration from file."""
        self.config_data = self._load_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data."""
        return self.config_data.copy()
