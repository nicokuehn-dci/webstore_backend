"""
Setup Utilities
-------------
Functions for setting up the application environment.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("This script requires Python 3.6 or higher.")
        sys.exit(1)

def setup_environment():
    """Setup required files and virtual environment"""
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    requirements_file = os.path.join(current_dir, 'requirements.txt')
    gitignore_file = os.path.join(current_dir, '.gitignore')
    
    # Create requirements.txt if needed
    if not os.path.exists(requirements_file):
        print("requirements.txt not found. Creating it...")
        with open(requirements_file, 'w') as f:
            f.write("blessed==1.21.0\nwcwidth==0.2.13\n")
        print("requirements.txt created successfully.")
    
    # Create .gitignore if needed
    if not os.path.exists(gitignore_file):
        print(".gitignore not found. Creating it...")
        with open(gitignore_file, 'w') as f:
            f.write("""# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.venv/
env/
ENV/
.env

# IDE specific files
.idea/
.vscode/
*.swp

# OS specific files
.DS_Store
Thumbs.db

# Application specific
*.log
*.sqlite3
""")
        print(".gitignore created successfully.")
    
    # Setup virtual environment
    venv_dir = os.path.join(current_dir, 'venv')  # Using 'venv' folder (not '.venv')
    venv_bin = os.path.join(venv_dir, 'bin')
    venv_python = os.path.join(venv_bin, 'python')
    
    # Check for alternate venv location
    alt_venv_dir = os.path.join(current_dir, '.venv')
    if os.path.exists(alt_venv_dir) and not os.path.exists(venv_dir):
        print("Found '.venv' directory instead of 'venv'. Using the existing environment.")
        venv_dir = alt_venv_dir
        venv_bin = os.path.join(venv_dir, 'bin')
        venv_python = os.path.join(venv_bin, 'python')
    
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
    
    # Install requirements
    if os.path.exists(requirements_file):
        print("Installing requirements from requirements.txt...")
        try:
            subprocess.check_call([os.path.join(venv_bin, 'pip'), 'install', '-r', requirements_file])
        except Exception as e:
            print(f"Warning: Failed to install requirements: {e}")
            print("Continuing with available packages...")
    
    # Restart script with venv Python if we're not already using it
    # Add a guard to prevent endless loops
    if sys.executable != venv_python and not os.environ.get('VENV_PYTHON_RUNNING'):
        os.environ['VENV_PYTHON_RUNNING'] = '1'
        try:
            # Check if the venv Python exists before trying to use it
            if os.path.exists(venv_python):
                os.execv(venv_python, [venv_python] + sys.argv)
            else:
                print(f"Warning: Virtual environment Python not found at {venv_python}")
                print("Continuing with system Python...")
        except FileNotFoundError:
            print(f"Warning: Could not find Python in virtual environment at {venv_python}")
            print("Continuing with system Python...")
