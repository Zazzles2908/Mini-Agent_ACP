#!/usr/bin/env python3
"""Mini-Agent setup and verification script."""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking Mini-Agent environment...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Check API keys
        with open(env_file) as f:
            env_content = f.read()
            if "ZAI_API_KEY" in env_content:
                print("✅ ZAI_API_KEY found")
            else:
                print("❌ ZAI_API_KEY missing")
                
            if "MINIMAX_API_KEY" in env_content:
                print("✅ MINIMAX_API_KEY found")
            else:
                print("❌ MINIMAX_API_KEY missing")
    else:
        print("❌ .env file not found")
    
    # Check Python environment
    print(f"🐍 Python version: {sys.version}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not in virtual environment - consider using venv")
    
    # Check installed packages
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True)
        if "aiohttp" in result.stdout:
            print("✅ Core dependencies installed")
        else:
            print("❌ Core dependencies missing")
    except Exception as e:
        print(f"❌ Error checking packages: {e}")
    
    print("\n" + "="*50)

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directory structure...")
    
    directories = [
        "documents",
        "documents/technical", 
        "documents/user_guides",
        "scripts",
        "tests"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"✅ {directory}/")

def show_usage():
    """Show usage instructions."""
    print("""
🚀 Mini-Agent Setup Complete!

Next steps:

1. **Activate the agent:**
   ```bash
   python -m mini_agent
   ```

2. **Run tests:**
   ```bash
   python scripts/test_zai_reader.py
   ```

3. **Install VS Code extension:**
   ```bash
   code --install-extension mini_agent/vscode_extension/
   ```

4. **Start ACP server:**
   ```bash
   python -m mini_agent.acp
   ```

Environment variables needed in .env:
- ZAI_API_KEY: Your Z.AI API key
- MINIMAX_API_KEY: Your MiniMax API key

🎯 Quick Commands:
- /help - Show available commands
- /clear - Clear conversation
- /stats - Show session statistics
- /exit - Exit the agent
""")

def main():
    """Main setup function."""
    print("="*50)
    print("🛠️  Mini-Agent Setup Script")
    print("="*50)
    
    check_environment()
    create_directories()
    show_usage()

if __name__ == "__main__":
    main()