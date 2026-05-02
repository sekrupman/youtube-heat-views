#!/usr/bin/env python3
"""
YouTube Video Processor - Setup Script
Verifies all dependencies and configurations
"""

import sys
import subprocess
import os
import shutil
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")


def check_python():
    """Check Python version"""
    print("Python version: {}.{}.{}".format(*sys.version_info[:3]))
    if sys.version_info < (3, 9):
        print("Python 3.9+ required")
        return False
    return True


def check_module(module_name, pip_name=None):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        print(f"{module_name} installed")
        return True
    except ImportError:
        print(f"{module_name} not installed")
        if pip_name:
            print(f"  Run: pip install {pip_name}")
        return False

def check_command(command, name):
    path = shutil.which(command)
    if path:
        print(f"{name} found at: {path}")
        return True
    else:
        print(f"{name} not found in PATH")
        return False


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    os.makedirs("static", exist_ok=True)
    os.makedirs("clips", exist_ok=True)
    print("Directories created/verified")


def copy_static_files():
    """Copy static files to static directory"""
    print("\nCopying static files...")
    files = {
        "index.html": "static/index.html",
        "style.css": "static/style.css",
        "script.js": "static/script.js",
    }

    for src, dst in files.items():
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"Copied {src} to {dst}")
        elif os.path.exists(dst):
            print(f"{dst} already exists")


def main():
    print_header("YouTube Video Processor Setup")

    # Check Python
    print("1. Checking Python...")
    if not check_python():
        print("\nSetup failed. Please install Python 3.9+")
        return False

    # Check Python modules
    print("\n2. Checking Python modules...")
    modules = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
    ]

    missing = []
    for module, pip_name in modules:
        if not check_module(module, pip_name):
            missing.append(pip_name)

    if missing:
        print(f"\n Missing modules. Run:")
        print(f"  pip install {' '.join(missing)}")
        return False

    # Check system commands
    print("\n3. Checking system commands...")
    commands = [
        ("ffmpeg", "FFmpeg"),
        ("yt-dlp", "yt-dlp"),
    ]

    missing_commands = []
    for cmd, name in commands:
        if not check_command(cmd, name):
            missing_commands.append((cmd, name))

    if missing_commands:
        print("\n Some external tools are missing:")
        for cmd, name in missing_commands:
            if name == "FFmpeg":
                print(f"  - {name}: https://www.gyan.dev/ffmpeg/builds/")
            else:
                print(f"  - {name}: pip install {cmd}")

    # Create directories
    print("\n4. Setting up directories...")
    create_directories()

    # Copy static files
    print("\n5. Setting up static files...")
    copy_static_files()

    # Success
    print_header(" Setup Complete!")
    print(
        """
To start the server:
  python api.py

Then open your browser to:
  http://localhost:8000

For detailed documentation, see API_README.md
For quick start, see QUICKSTART.md
"""
    )

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
