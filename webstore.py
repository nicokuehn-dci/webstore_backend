#!/usr/bin/env python3
"""
WebStore App - Main Entry Point
------------------------------
A command-line interface for managing products and users in a web store.
Features an interactive menu system with arrow key navigation and colored UI.

Usage:
    ./webstore.py

Authors:
    Nico Kuehn <nico.kuehn@dci.education>
    Alexandra Adamchyk <alexandra.adamchyk@dci.education>
    Abdul Rahman Dahhan <abdul.dahhan@dci.education>

Contributors:
    - Added enhanced cart functionality with tax and discount system
    - Improved virtual environment handling
    - Added full-featured product management system
    - Implemented hierarchical menu navigation
    - Enhanced user authentication system

Date: May 27, 2025
License: MIT License
"""

import os
import sys
import subprocess

# Define version
VERSION = "1.0.0"

def setup_venv_and_dependencies():
    """Setup virtual environment and install dependencies."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # First, ensure virtual environment exists
    venv_path = os.path.join(current_dir, 'venv')
    # Use correct path for Windows vs Unix
    if os.name == 'nt':  # Windows
        venv_python = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Unix/Linux/macOS
        venv_python = os.path.join(venv_path, 'bin', 'python')
    
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            sys.exit(1)
    
    # Check and activate virtual environment
    if os.path.exists(venv_python) and sys.executable != venv_python and not os.environ.get('VENV_PYTHON_RUNNING'):
        print("Activating virtual environment...")
        os.environ['VENV_PYTHON_RUNNING'] = '1'
        # Use subprocess instead of os.execv to handle paths with spaces
        try:
            subprocess.run([venv_python] + sys.argv, check=True)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"Error running with virtual environment: {e}")
            sys.exit(1)
    
    # Ensure pip is up to date in the virtual environment
    try:
        subprocess.run([venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading pip: {e}")
        sys.exit(1)
    
    # Check if requirements.txt exists and install dependencies
    requirements_file = os.path.join(current_dir, 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            print("Checking dependencies in virtual environment...")
            # Get list of installed packages
            result = subprocess.run([venv_python, '-m', 'pip', 'freeze'], capture_output=True, text=True)
            installed_packages = {line.split('==')[0].lower() for line in result.stdout.splitlines()}
            
            # Read requirements
            with open(requirements_file, 'r') as f:
                required_packages = {line.split('==')[0].lower() for line in f.readlines() if line.strip() and not line.startswith('#')}
            
            # Find missing packages
            missing_packages = required_packages - installed_packages
            if missing_packages:
                print(f"Installing missing dependencies in virtual environment: {', '.join(missing_packages)}")
                subprocess.run([venv_python, '-m', 'pip', 'install', '-r', requirements_file], check=True)
                print("Dependencies installed successfully in virtual environment.")
            else:
                print("All dependencies are already installed in virtual environment.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error checking dependencies: {e}")
            sys.exit(1)
    else:
        print("Warning: requirements.txt not found!")

# Setup virtual environment and install dependencies before importing any third-party modules
setup_venv_and_dependencies()

# Now we can safely import our dependencies
import time
from blessed import Terminal

from src.utils.setup import check_python_version, setup_environment
from src.controllers.main_controller import MainController

def parse_args():
    """Parse command line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print(f"""
WebStore App - Interactive CLI Menu System v{VERSION}
Usage:
  {sys.argv[0]} [options]

Options:
  -h, --help     Show this help message and exit
  -v, --version  Show version and exit
  --init         Initialize repository with requirements.txt and .gitignore
  --debug        Start with auto debugger monitoring
  --debug-scan   Run a one-time debug scan

Example:
  {sys.argv[0]}              Start the application
  {sys.argv[0]} --init       Initialize repository files
  {sys.argv[0]} --debug      Start with debugging enabled
""")
            sys.exit(0)
        elif sys.argv[1] in ['-v', '--version']:
            print(f"WebStore App v{VERSION}")
            sys.exit(0)
        elif sys.argv[1] == '--init':
            print("Repository files already initialized.")
            sys.exit(0)
        elif sys.argv[1] == '--debug':
            # Start with auto debugger monitoring
            try:
                from auto_debugger.src.debugger import AutoDebugger
                debugger = AutoDebugger()
                print("🔍 Starting auto debugger monitoring...")
                debugger.start_monitoring(interval=30)
                print("✅ Auto debugger is now monitoring your code!")
            except ImportError:
                print("⚠️ Auto debugger not available")
        elif sys.argv[1] == '--debug-scan':
            # Run one-time debug scan
            try:
                from auto_debugger.src.debugger import AutoDebugger
                debugger = AutoDebugger()
                print("🔍 Running debug scan...")
                results = debugger.run_full_analysis()
                errors = len(results.get('errors', []))
                warnings = len(results.get('warnings', []))
                print(f"✅ Scan complete: {errors} errors, {warnings} warnings")
                if errors > 0:
                    print("📊 Check auto_debugger/reports/ for detailed results")
                sys.exit(0)
            except ImportError:
                print("⚠️ Auto debugger not available")
                sys.exit(1)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print(f"Use '{sys.argv[0]} --help' for usage information.")
            sys.exit(1)

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check Python version
    check_python_version()
    
    # Parse command-line arguments
    parse_args()
    
    # Setup environment (venv should already be activated)
    setup_environment()
    
    # Initialize terminal
    term = Terminal()
    print(term.clear)
    # Title with orange background and black text
    print(term.move(0, 2) + term.center(term.black_on_orange(term.bold(f" WebStore App v{VERSION} "))))
    print()
    print(term.center(term.orange(term.bold("Interactive CLI Menu System"))))
    print(term.center(term.orange("-------------------------")))
    print()
    # Display credits as a watermark
    print(term.center(term.orange("Developed by:")))
    print(term.center(term.orange("Nico Kuehn · Alexandra Adamchyk · Abdul Rahman Dahhan")))
    print()
    print(term.center("Starting application..."))
    print()
    
    # Show loading progress bar (5 seconds)
    width = term.width
    bar_width = 40
    left_padding = (width - bar_width) // 2
    sleep_time = 5.0 / bar_width  # Distribute 5 seconds across all steps
    print()
    for i in range(bar_width + 1):
        progress = '$' * i + ' ' * (bar_width - i)
        percentage = int((i / bar_width) * 100)
        print(term.move_up(1) + ' ' * left_padding + f'[{progress}] {percentage}%')
        time.sleep(sleep_time)  # Adjusted delay for 5 second total
    print()
    
    # Check if git is initialized
    if not os.path.exists(os.path.join(current_dir, '.git')):
        print(term.center(term.yellow("Git repository not initialized.")))
        print(term.center(term.yellow("Run 'git init' to create a new repository.")))
        print()
    
    input(term.center("Press Enter to continue..."))
    
    # Initialize and run the main controller
    controller = MainController()
    controller.run()

if __name__ == "__main__":
    main()

# blah blah blah