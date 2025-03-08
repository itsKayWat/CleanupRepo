#!/usr/bin/env python3
import sys
import subprocess
import platform

def install_requirements():
    """Install all required packages for CleanupRepo."""
    # CleanupRepo uses only standard library modules
    print("CleanupRepo uses only Python standard library modules. No additional packages required!")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("WARNING: CleanupRepo is designed for Python 3.6+. You're running Python {}.{}.{}".format(
            python_version.major, python_version.minor, python_version.micro))
    else:
        print("Python version check passed: {}.{}.{}".format(
            python_version.major, python_version.minor, python_version.micro))

    print("\nSetup complete! CleanupRepo is ready to use.")

if __name__ == "__main__":
    install_requirements()