#!/usr/bin/env python3
"""
Mini-Agent Launcher with Environment Variable Support

This script ensures that Mini-Agent has access to the required environment variables
when running in environments that don't automatically load .env files.
"""

import os
import sys
import subprocess

def load_environment():
    """Load environment variables from .env file if it exists."""
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"📝 Loading environment variables from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")

def main():
    """Main entry point."""
    # Load environment variables
    load_environment()
    
    # Get the path to the UV Python executable
    uv_python = r"C:\Users\Jazeel-Home\AppData\Roaming\uv\tools\mini-agent\Scripts\python.exe"
    
    # Check if UV Python exists
    if not os.path.exists(uv_python):
        print(f"❌ UV Python not found at: {uv_python}")
        print("Trying regular Python...")
        python_exe = sys.executable
    else:
        python_exe = uv_python
    
    print(f"🚀 Starting Mini-Agent with Python: {python_exe}")
    
    # Run mini-agent using the appropriate Python executable
    try:
        result = subprocess.run([
            python_exe, "-m", "mini_agent.cli"
        ] + sys.argv[1:],  # Pass through any additional arguments
        cwd=os.getcwd(),
        env=os.environ.copy()  # Ensure environment variables are available
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n👋 Mini-Agent terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting Mini-Agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()