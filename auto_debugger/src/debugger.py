"""
Main Auto Debugger Service
-------------------------
Central debugging service that coordinates all debugging activities.
"""

import os
import sys
import traceback
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

from .analyzers.code_analyzer import CodeAnalyzer
from .analyzers.error_detector import ErrorDetector
from .analyzers.performance_analyzer import PerformanceAnalyzer
from .handlers.log_handler import LogHandler
from .handlers.report_handler import ReportHandler
from .utils.config import DebugConfig
from .utils.file_scanner import FileScanner


class AutoDebugger:
    """
    Automated debugging service for the WebStore application.
    Provides real-time error detection, code analysis, and performance monitoring.
    """
    
    def __init__(self, project_root: str = None, config_file: str = None):
        """Initialize the auto debugger service."""
        self.project_root = project_root or os.getcwd()
        self.config = DebugConfig(config_file)
        self.is_running = False
        self.monitoring_thread = None
        
        # Initialize components
        self.log_handler = LogHandler(self.config)
        self.code_analyzer = CodeAnalyzer(self.config)
        self.error_detector = ErrorDetector(self.config)
        self.performance_analyzer = PerformanceAnalyzer(self.config)
        self.report_handler = ReportHandler(self.config)
        self.file_scanner = FileScanner(self.project_root)
        
        # Statistics
        self.stats = {
            'errors_detected': 0,
            'warnings_found': 0,
            'files_analyzed': 0,
            'performance_issues': 0,
            'start_time': None,
            'last_scan': None
        }
        
        self.log_handler.info("AutoDebugger initialized")
    
    def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring of the project."""
        if self.is_running:
            self.log_handler.warning("Debugger is already running")
            return
            
        self.is_running = True
        self.stats['start_time'] = datetime.now()
        
        self.log_handler.info(f"Starting continuous monitoring (interval: {interval}s)")
        
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        if not self.is_running:
            return
            
        self.is_running = False
        self.log_handler.info("Stopping continuous monitoring")
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
    
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop that runs in a separate thread."""
        while self.is_running:
            try:
                self.run_full_analysis()
                time.sleep(interval)
            except Exception as e:
                self.log_handler.error(f"Error in monitoring loop: {e}")
                self.log_handler.debug(traceback.format_exc())
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """Run a complete analysis of the project."""
        self.log_handler.info("Starting full project analysis")
        start_time = time.time()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'errors': [],
            'warnings': [],
            'performance_issues': [],
            'code_quality': {},
            'summary': {}
        }
        
        try:
            # Get all Python files
            python_files = self.file_scanner.get_python_files()
            self.stats['files_analyzed'] = len(python_files)
            
            # Analyze each file
            for file_path in python_files:
                file_results = self._analyze_file(file_path)
                
                results['errors'].extend(file_results.get('errors', []))
                results['warnings'].extend(file_results.get('warnings', []))
                results['performance_issues'].extend(file_results.get('performance_issues', []))
            
            # Run project-wide analysis
            results['code_quality'] = self.code_analyzer.analyze_project_structure(self.project_root)
            
            # Update statistics
            self.stats['errors_detected'] = len(results['errors'])
            self.stats['warnings_found'] = len(results['warnings'])
            self.stats['performance_issues'] = len(results['performance_issues'])
            self.stats['last_scan'] = datetime.now()
            
            # Generate summary
            results['summary'] = self._generate_summary(results)
            
            # Generate report
            self.report_handler.generate_report(results)
            
            elapsed_time = time.time() - start_time
            self.log_handler.info(f"Full analysis completed in {elapsed_time:.2f}s")
            
        except Exception as e:
            self.log_handler.error(f"Error during full analysis: {e}")
            self.log_handler.debug(traceback.format_exc())
            results['errors'].append({
                'type': 'DEBUGGER_ERROR',
                'message': str(e),
                'file': 'auto_debugger',
                'severity': 'HIGH'
            })
        
        return results
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file for issues."""
        results = {
            'file': file_path,
            'errors': [],
            'warnings': [],
            'performance_issues': []
        }
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Run different analyzers
            syntax_errors = self.error_detector.check_syntax(file_path, content)
            code_issues = self.code_analyzer.analyze_code_quality(file_path, content)
            performance_issues = self.performance_analyzer.analyze_performance(file_path, content)
            
            results['errors'].extend(syntax_errors)
            results['warnings'].extend(code_issues)
            results['performance_issues'].extend(performance_issues)
            
        except Exception as e:
            self.log_handler.error(f"Error analyzing file {file_path}: {e}")
            results['errors'].append({
                'type': 'FILE_ANALYSIS_ERROR',
                'message': f"Failed to analyze file: {e}",
                'file': file_path,
                'line': 0,
                'severity': 'MEDIUM'
            })
        
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of analysis results."""
        summary = {
            'total_files': self.stats['files_analyzed'],
            'total_errors': len(results['errors']),
            'total_warnings': len(results['warnings']),
            'total_performance_issues': len(results['performance_issues']),
            'critical_issues': 0,
            'high_priority_issues': 0,
            'recommendations': []
        }
        
        # Count severity levels
        for error in results['errors']:
            if error.get('severity') == 'CRITICAL':
                summary['critical_issues'] += 1
            elif error.get('severity') == 'HIGH':
                summary['high_priority_issues'] += 1
        
        # Generate recommendations
        if summary['critical_issues'] > 0:
            summary['recommendations'].append("Address critical errors immediately")
        if summary['total_performance_issues'] > 5:
            summary['recommendations'].append("Consider performance optimization")
        if summary['total_warnings'] > 20:
            summary['recommendations'].append("Review and fix code quality warnings")
        
        return summary
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current debugging statistics."""
        stats = self.stats.copy()
        if stats['start_time']:
            stats['uptime'] = str(datetime.now() - stats['start_time'])
        return stats
    
    def analyze_specific_error(self, error_traceback: str) -> Dict[str, Any]:
        """Analyze a specific error traceback."""
        return self.error_detector.analyze_traceback(error_traceback)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status of the project."""
        return {
            'status': 'HEALTHY' if self.stats['errors_detected'] == 0 else 'ISSUES_DETECTED',
            'last_scan': self.stats['last_scan'].isoformat() if self.stats['last_scan'] else None,
            'monitoring_active': self.is_running,
            'critical_issues': self.stats['errors_detected'],
            'warnings': self.stats['warnings_found']
        }
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_monitoring()
