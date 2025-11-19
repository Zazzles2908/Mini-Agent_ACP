#!/usr/bin/env python3
"""Install Mini-Agent dependencies."""

import subprocess
import sys
import os

def install_requirements():
    """Install all required dependencies."""
    print("🚀 Installing Mini-Agent dependencies...")
    
    # Install from requirements.txt
    try:
        print("📦 Installing from requirements.txt...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Successfully installed all dependencies!")
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False
    
    # Verify key imports
    print("\n🔍 Verifying key imports...")
    imports_to_check = [
        "aiohttp",
        "anthropic", 
        "openai",
        "requests",
        "pydantic",
        "pyyaml"
    ]
    
    all_good = True
    for module in imports_to_check:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False
    
    if all_good:
        print("\n🎉 All dependencies installed successfully!")
        return True
    else:
        print("\n⚠️  Some imports failed. Check the errors above.")
        return False

if __name__ == "__main__":
    install_requirements()