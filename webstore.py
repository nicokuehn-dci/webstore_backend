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
import logging
from pathlib import Path

# Enhanced imports for new functionality
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    import watchdog
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

# Define version and configuration
VERSION = "1.0.0"
APP_NAME = "WebStore"

def setup_logging():
    """Setup enhanced logging with loguru if available."""
    if LOGURU_AVAILABLE:
        # Configure loguru for enhanced logging
        logger.remove()  # Remove default handler
        logger.add(
            "logs/webstore.log",
            rotation="10 MB",
            retention="7 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
        )
        logger.add(
            sys.stderr,
            level="WARNING",
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        logger.info(f"Enhanced logging initialized for {APP_NAME} v{VERSION}")
        return logger
    else:
        # Fallback to standard logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/webstore.log'),
                logging.StreamHandler(sys.stderr)
            ]
        )
        return logging.getLogger(__name__)

def load_environment():
    """Load environment variables from .env file if available."""
    if DOTENV_AVAILABLE:
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
            return True
    return False

def get_system_info():
    """Get system information for monitoring."""
    info = {
        'python_version': sys.version,
        'platform': sys.platform,
        'cwd': os.getcwd()
    }
    
    if PSUTIL_AVAILABLE:
        try:
            info.update({
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'disk_usage': psutil.disk_usage('.').percent
            })
        except:
            pass  # Ignore errors in system info gathering
    
    return info

def create_directories():
    """Create necessary directories for the application."""
    directories = ['logs', 'reports', 'backups', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

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
{APP_NAME} - Interactive CLI Menu System v{VERSION}
Usage:
  {sys.argv[0]} [options]

Options:
  -h, --help     Show this help message and exit
  -v, --version  Show version and exit
  --init         Initialize repository with requirements.txt and .gitignore
  --debug        Start with auto debugger monitoring
  --debug-scan   Run a one-time debug scan
  --demo         Demonstrate enhanced features
  --system-status Show system status

Example:
  {sys.argv[0]}              Start the application
  {sys.argv[0]} --init       Initialize repository files
  {sys.argv[0]} --debug      Start with debugging enabled
""")
            sys.exit(0)
        elif sys.argv[1] in ['-v', '--version']:
            print(f"{APP_NAME} v{VERSION}")
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
        elif sys.argv[1] == '--demo':
            # Demonstrate enhanced features
            try:
                from src.utils.enhanced_utils import demo_all_features
                demo_all_features()
                sys.exit(0)
            except ImportError as e:
                print(f"⚠️ Enhanced features demo not available: {e}")
                sys.exit(1)
        elif sys.argv[1] == '--system-status':
            # Show system status
            try:
                from src.utils.enhanced_utils import DisplayHelper
                DisplayHelper.show_system_status()
                sys.exit(0)
            except ImportError:
                print("⚠️ System monitoring not available")
                sys.exit(1)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print(f"Use '{sys.argv[0]} --help' for usage information.")
            sys.exit(1)

def enhanced_startup_display():
    """Enhanced startup display using rich if available."""
    if RICH_AVAILABLE:
        console = Console()
        
        # Clear screen and show startup
        console.clear()
        
        # Create a fancy panel for the app title
        title_text = Text(f"{APP_NAME} v{VERSION}", style="bold magenta")
        subtitle_text = Text("Interactive CLI Menu System", style="cyan")
        credits_text = Text("Developed by: Nico Kuehn · Alexandra Adamchyk · Abdul Rahman Dahhan", style="dim")
        
        panel = Panel.fit(
            f"{title_text}\n{subtitle_text}\n\n{credits_text}",
            title="🛍️ Welcome to WebStore",
            border_style="blue"
        )
        console.print(panel, justify="center")
        
        # Show system info if available
        if PSUTIL_AVAILABLE:
            system_info = get_system_info()
            console.print(f"\n💻 System: Python {system_info.get('python_version', 'Unknown').split()[0]}", style="dim")
            console.print(f"📁 Directory: {system_info.get('cwd', 'Unknown')}", style="dim")
        
        # Enhanced progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Initializing WebStore...", total=100)
            
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.05)  # 5 second total loading
        
        console.print("\n✅ [green]Initialization complete![/green]")
        console.print("Press Enter to continue...", style="dim")
        
    else:
        # Fallback to original blessed display
        fallback_startup_display()

def fallback_startup_display():
    """Fallback startup display using blessed."""
    term = Terminal()
    print(term.clear)
    # Title with orange background and black text
    print(term.move(0, 2) + term.center(term.black_on_orange(term.bold(f" {APP_NAME} v{VERSION} "))))
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

def check_git_status():
    """Check git repository status."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    git_dir = os.path.join(current_dir, '.git')
    
    if not os.path.exists(git_dir):
        if RICH_AVAILABLE:
            console = Console()
            console.print("⚠️ [yellow]Git repository not initialized.[/yellow]")
            console.print("[dim]Run 'git init' to create a new repository.[/dim]")
        else:
            term = Terminal()
            print(term.center(term.yellow("Git repository not initialized.")))
            print(term.center(term.yellow("Run 'git init' to create a new repository.")))
        print()
        return False
    return True
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
    """Enhanced main function with new dependencies integration."""
    # Initialize logging first
    app_logger = setup_logging()
    
    # Load environment variables
    env_loaded = load_environment()
    if env_loaded and LOGURU_AVAILABLE:
        app_logger.info("Environment variables loaded from .env file")
    
    # Create necessary directories
    create_directories()
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Log system information
    system_info = get_system_info()
    if LOGURU_AVAILABLE:
        app_logger.info(f"Starting {APP_NAME} v{VERSION}")
        app_logger.info(f"System info: {system_info}")
    
    # Check Python version
    check_python_version()
    
    # Parse command-line arguments
    parse_args()
    
    # Setup environment (venv should already be activated)
    setup_environment()
    
    # Enhanced startup display
    enhanced_startup_display()
    
    # Check git status
    check_git_status()
    
    input("Press Enter to continue...")
    
    # Initialize and run the main controller
    try:
        if LOGURU_AVAILABLE:
            app_logger.info("Initializing main controller")
        
        controller = MainController()
        
        if LOGURU_AVAILABLE:
            app_logger.info("Starting main application loop")
        
        controller.run()
        
    except KeyboardInterrupt:
        if LOGURU_AVAILABLE:
            app_logger.info("Application terminated by user")
        print("\n👋 Goodbye! Thanks for using WebStore!")
    except Exception as e:
        if LOGURU_AVAILABLE:
            app_logger.error(f"Application error: {e}")
        else:
            print(f"Error: {e}")
        raise
    finally:
        if LOGURU_AVAILABLE:
            app_logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()

# blah blah blah