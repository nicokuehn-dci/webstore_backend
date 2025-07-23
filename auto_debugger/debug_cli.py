#!/usr/bin/env python3
"""
Auto Debugger CLI
----------------
Command-line interface for the auto debugger service.
"""

import argparse
import sys
import os

# Add parent directory to path to import auto_debugger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.debugger import AutoDebugger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Auto Debugger - Automated code analysis and debugging'
    )
    
    parser.add_argument(
        'command',
        choices=['scan', 'monitor', 'report', 'status'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--project-root',
        default=os.getcwd(),
        help='Project root directory (default: current directory)'
    )
    
    parser.add_argument(
        '--config',
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Monitoring interval in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--output',
        choices=['console', 'file', 'html'],
        default='console',
        help='Output format (default: console)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize debugger
        debugger = AutoDebugger(
            project_root=args.project_root,
            config_file=args.config
        )
        
        if args.command == 'scan':
            print("🔍 Running full project analysis...")
            results = debugger.run_full_analysis()
            
            if args.output == 'console':
                print_console_results(results)
            
            print(f"✅ Analysis complete. Found {len(results.get('errors', []))} errors and {len(results.get('warnings', []))} warnings.")
        
        elif args.command == 'monitor':
            print(f"👀 Starting continuous monitoring (interval: {args.interval}s)")
            print("Press Ctrl+C to stop...")
            
            debugger.start_monitoring(args.interval)
            
            try:
                # Keep the program running
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring...")
                debugger.stop_monitoring()
        
        elif args.command == 'report':
            print("📊 Generating latest report...")
            results = debugger.run_full_analysis()
            report_path = debugger.report_handler.get_latest_report()
            print(f"📄 Report generated: {report_path}")
        
        elif args.command == 'status':
            print("📈 Debugger Status:")
            stats = debugger.get_statistics()
            health = debugger.get_health_status()
            
            print(f"  Status: {health['status']}")
            print(f"  Monitoring: {'Active' if health['monitoring_active'] else 'Inactive'}")
            print(f"  Last Scan: {health['last_scan'] or 'Never'}")
            print(f"  Files Analyzed: {stats['files_analyzed']}")
            print(f"  Errors Detected: {stats['errors_detected']}")
            print(f"  Warnings Found: {stats['warnings_found']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def print_console_results(results):
    """Print analysis results to console."""
    errors = results.get('errors', [])
    warnings = results.get('warnings', [])
    performance_issues = results.get('performance_issues', [])
    
    if errors:
        print("\n🚨 ERRORS:")
        for error in errors[:10]:  # Show first 10 errors
            severity = error.get('severity', 'UNKNOWN')
            file_path = error.get('file', 'Unknown')
            line = error.get('line', 0)
            message = error.get('message', 'No message')
            
            print(f"  [{severity}] {file_path}:{line} - {message}")
        
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings[:5]:  # Show first 5 warnings
            file_path = warning.get('file', 'Unknown')
            line = warning.get('line', 0)
            message = warning.get('message', 'No message')
            
            print(f"  {file_path}:{line} - {message}")
        
        if len(warnings) > 5:
            print(f"  ... and {len(warnings) - 5} more warnings")
    
    if performance_issues:
        print("\n🚀 PERFORMANCE ISSUES:")
        for issue in performance_issues[:3]:  # Show first 3 performance issues
            file_path = issue.get('file', 'Unknown')
            line = issue.get('line', 0)
            message = issue.get('message', 'No message')
            
            print(f"  {file_path}:{line} - {message}")
        
        if len(performance_issues) > 3:
            print(f"  ... and {len(performance_issues) - 3} more performance issues")


if __name__ == '__main__':
    main()
