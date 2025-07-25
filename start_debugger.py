#!/usr/bin/env python3
"""
Auto Debugger Launcher
---------------------
Convenient entry point to start the auto debugger service.

Usage:
    python start_debugger.py [options]

Examples:
    python start_debugger.py                    # Run one-time scan
    python start_debugger.py --monitor          # Start continuous monitoring
    python start_debugger.py --scan             # Quick scan only
    python start_debugger.py --report           # Generate report
    python start_debugger.py --status           # Show status
    python start_debugger.py --view-log         # View latest log file
    python start_debugger.py --help             # Show help
"""

import argparse
import sys
import os
import time
from datetime import datetime

# Add the auto_debugger to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'auto_debugger'))

try:
    from auto_debugger.src.debugger import AutoDebugger
except ImportError as e:
    print(f"❌ Error importing auto debugger: {e}")
    print("Make sure the auto_debugger directory exists and is properly configured.")
    sys.exit(1)


def display_log_with_pagination(log_path: str, lines_per_page: int = 50):
    """Display log file content with pagination."""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        current_line = 0
        
        while current_line < total_lines:
            # Clear screen for better viewing
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Show current page
            end_line = min(current_line + lines_per_page, total_lines)
            for i in range(current_line, end_line):
                print(lines[i], end='')
            
            # Show pagination info
            print(f"\n--- Page {current_line // lines_per_page + 1} of {(total_lines - 1) // lines_per_page + 1} ---")
            print(f"Lines {current_line + 1}-{end_line} of {total_lines}")
            
            # Get user input for navigation
            if end_line >= total_lines:
                print("\n✅ End of log file. Press Enter to exit...")
                input()
                break
            else:
                print("\nPress Enter for next page, 'q' to quit, 'b' for beginning:")
                choice = input().strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'b':
                    current_line = 0
                else:
                    current_line = end_line
                    
    except Exception as e:
        print(f"❌ Error reading log file: {e}")


def print_banner():
    """Print a nice banner for the debugger."""
    print("=" * 60)
    print("🔍 WebStore Auto Debugger Service")
    print("=" * 60)
    print("Automated code analysis and debugging for your WebStore app")
    print()


def print_results_summary(results):
    """Print a summary of analysis results."""
    errors = results.get('errors', [])
    warnings = results.get('warnings', [])
    performance_issues = results.get('performance_issues', [])
    summary = results.get('summary', {})
    
    print("\n📊 Analysis Results Summary:")
    print("-" * 40)
    print(f"📁 Files Analyzed: {summary.get('total_files', 0)}")
    print(f"🚨 Errors Found: {len(errors)}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print(f"🚀 Performance Issues: {len(performance_issues)}")
    print(f"🔥 Critical Issues: {summary.get('critical_issues', 0)}")
    print(f"⚡ High Priority: {summary.get('high_priority_issues', 0)}")
    
    # Show top errors
    if errors:
        print("\n🚨 Top Critical Errors:")
        for i, error in enumerate(errors[:3], 1):
            file_path = error.get('file', 'Unknown')
            line = error.get('line', 0)
            message = error.get('message', 'No message')
            severity = error.get('severity', 'UNKNOWN')
            
            # Shorten file path for display
            if len(file_path) > 50:
                file_path = "..." + file_path[-47:]
            
            print(f"  {i}. [{severity}] {file_path}:{line}")
            print(f"     {message}")
    
    # Show recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        print("\n💡 Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            priority = rec.get('priority', 'MEDIUM')
            category = rec.get('category', 'General')
            message = rec.get('message', '')
            
            print(f"  {i}. [{priority}] {category}: {message}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='WebStore Auto Debugger - Automated code analysis',
        epilog='For more details, see auto_debugger/README.md'
    )
    
    # Command options
    parser.add_argument(
        '--scan', '-s',
        action='store_true',
        help='Run a one-time code analysis scan'
    )
    
    parser.add_argument(
        '--monitor', '-m',
        action='store_true',
        help='Start continuous monitoring'
    )
    
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help='Generate and show latest report'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show debugger status and statistics'
    )
    
    parser.add_argument(
        '--view-log',
        action='store_true',
        help='View the latest human-readable log file'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=30,
        help='Monitoring interval in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress detailed output'
    )
    
    parser.add_argument(
        '--project-root',
        default=os.path.dirname(os.path.abspath(__file__)),
        help='Project root directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # If no specific command, default to scan
    if not any([args.scan, args.monitor, args.report, args.status, args.view_log]):
        args.scan = True
    
    if not args.quiet:
        print_banner()
    
    try:
        # Initialize the debugger
        if not args.quiet:
            print(f"🔧 Initializing debugger for project: {args.project_root}")
        
        debugger = AutoDebugger(
            project_root=args.project_root,
            config_file=args.config
        )
        
        if args.status:
            # Show status
            stats = debugger.get_statistics()
            health = debugger.get_health_status()
            
            print("📈 Debugger Status:")
            print(f"  🔄 Status: {health['status']}")
            print(f"  👀 Monitoring: {'Active' if health['monitoring_active'] else 'Inactive'}")
            print(f"  📅 Last Scan: {health['last_scan'] or 'Never'}")
            print(f"  📁 Files Analyzed: {stats['files_analyzed']}")
            print(f"  🚨 Errors Detected: {stats['errors_detected']}")
            print(f"  ⚠️  Warnings Found: {stats['warnings_found']}")
            
            if stats['start_time']:
                uptime = datetime.now() - stats['start_time']
                print(f"  ⏱️  Uptime: {uptime}")
        
        elif args.view_log:
            # View the latest human-readable log file
            print("📝 Finding latest log file...")
            reports_dir = 'auto_debugger/reports'
            if os.path.exists(reports_dir):
                log_files = [f for f in os.listdir(reports_dir) if f.startswith('debug_log_') and f.endswith('.txt')]
                if log_files:
                    log_files.sort(reverse=True)  # Most recent first
                    latest_log = os.path.join(reports_dir, log_files[0])
                    
                    print(f"📄 Latest log file: {latest_log}")
                    print("🔍 Use pagination to navigate through the log:")
                    print("=" * 60)
                    
                    # Use pagination for better readability
                    display_log_with_pagination(latest_log)
                else:
                    print("❌ No log files found. Run a scan first with --scan")
            else:
                print("❌ Reports directory not found. Run a scan first with --scan")
        
        elif args.report:
            # Generate and show report
            print("📊 Generating comprehensive report...")
            results = debugger.run_full_analysis()
            
            report_path = debugger.report_handler.get_latest_report()
            print(f"📄 Report saved to: {report_path}")
            
            # Try to find HTML report
            html_report = report_path.replace('.json', '.html')
            if os.path.exists(html_report):
                print(f"🌐 HTML Report: {html_report}")
            
            if not args.quiet:
                print_results_summary(results)
        
        elif args.monitor:
            # Start continuous monitoring
            print(f"👀 Starting continuous monitoring...")
            print(f"⏰ Scan Interval: {args.interval} seconds")
            print("📊 Monitoring WebStore project for code issues...")
            print("🛑 Press Ctrl+C to stop monitoring")
            print()
            
            debugger.start_monitoring(args.interval)
            
            try:
                # Keep the program running and show periodic updates
                start_time = time.time()
                while True:
                    time.sleep(10)  # Update every 10 seconds
                    
                    # Show periodic status (every minute)
                    if int(time.time() - start_time) % 60 == 0:
                        stats = debugger.get_statistics()
                        uptime = int(time.time() - start_time)
                        print(f"⏱️  Monitoring for {uptime}s | "
                              f"Errors: {stats['errors_detected']} | "
                              f"Warnings: {stats['warnings_found']}")
            
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring...")
                debugger.stop_monitoring()
                print("✅ Auto debugger stopped successfully")
        
        elif args.scan:
            # Run one-time scan
            print("🔍 Running comprehensive code analysis...")
            print("📂 Scanning Python files in the project...")
            
            start_time = time.time()
            results = debugger.run_full_analysis()
            elapsed = time.time() - start_time
            
            print(f"✅ Analysis completed in {elapsed:.2f} seconds")
            
            if not args.quiet:
                print_results_summary(results)
            
            # Quick summary
            errors = len(results.get('errors', []))
            warnings = len(results.get('warnings', []))
            
            if errors == 0 and warnings == 0:
                print("\n🎉 Great! No issues found in your code!")
            elif errors == 0:
                print(f"\n✅ No critical errors found, but {warnings} warnings to review")
            else:
                print(f"\n⚠️  Found {errors} errors and {warnings} warnings that need attention")
            
            # Show where to find detailed results
            report_path = debugger.report_handler.get_latest_report()
            if report_path and os.path.exists(report_path):
                print(f"📄 Detailed report: {report_path}")
                
                # Show readable log file
                log_path = report_path.replace('.json', '.txt').replace('debug_report_', 'debug_log_')
                if os.path.exists(log_path):
                    print(f"📝 Human-readable log: {log_path}")
                    print(f"💡 Tip: Open the log file to see warnings organized by severity and date")
                
                # Show HTML report if available
                html_path = report_path.replace('.json', '.html')
                if os.path.exists(html_path):
                    print(f"🌐 HTML report: {html_path}")
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if not args.quiet:
            import traceback
            print("\nFull error details:")
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
