#!/usr/bin/env python3
"""
Mini-Agent Package Launcher
This script properly sets up the Python path to allow relative imports
"""

import sys
import os

# Add the project directory to Python path
project_dir = r"C:\Users\Jazeel-Home\Mini-Agent"
sys.path.insert(0, project_dir)
sys.path.insert(0, os.path.join(project_dir, "mini_agent"))

# Set working directory
os.chdir(project_dir)

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("📝 Loaded environment from: .env")
except ImportError:
    pass

if __name__ == "__main__":
    try:
        # Import and run the CLI
        from mini_agent.cli import main
        main()
    except Exception as e:
        print(f"Error starting Mini-Agent: {e}")
        input("Press Enter to exit...")