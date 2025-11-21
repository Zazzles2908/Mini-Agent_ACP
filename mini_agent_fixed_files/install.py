#!/usr/bin/env python3
"""
Quick installation script for mini-agent fixed files
"""

import os
import shutil
import sys

def main():
    print("🚀 Mini-Agent Fixed Files Installer")
    print("=" * 40)
    
    # Get current directory
    current_dir = os.getcwd()
    fixed_files_dir = os.path.join(current_dir, "mini_agent_fixed_files")
    mini_agent_dir = os.path.join(current_dir, "mini_agent")
    
    print(f"Current directory: {current_dir}")
    print(f"Fixed files location: {fixed_files_dir}")
    
    # Check if fixed files exist
    if not os.path.exists(fixed_files_dir):
        print("❌ Error: mini_agent_fixed_files directory not found!")
        print("Please ensure you're running this script from the correct location.")
        sys.exit(1)
    
    # Check if mini_agent folder exists
    if os.path.exists(mini_agent_dir):
        backup_dir = os.path.join(current_dir, f"mini_agent_backup_{int(time.time())}")
        print(f"📦 Creating backup: {backup_dir}")
        shutil.move(mini_agent_dir, backup_dir)
        print("✅ Backup created")
    
    # Copy new files
    print("📁 Installing fixed mini_agent files...")
    shutil.copytree(os.path.join(fixed_files_dir, "mini_agent"), mini_agent_dir)
    print("✅ mini_agent files installed")
    
    # Install pydantic
    print("📦 Installing pydantic...")
    os.system("pip install pydantic")
    print("✅ Pydantic installed")
    
    # Run test
    print("🧪 Running import test...")
    os.system("python test_imports.py")
    
    print("\n🎉 Installation complete!")
    print("\nNext steps:")
    print("1. Test your mini-agent: python test_llm_client.py")
    print("2. Restore skills folder from GitHub if needed")
    print("3. Configure your API keys")

if __name__ == "__main__":
    import time
    main()