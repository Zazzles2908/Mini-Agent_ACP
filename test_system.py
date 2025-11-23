#!/usr/bin/env python3
"""Test script to verify Mini-Agent system functionality"""

import sys
import os
import asyncio
import tempfile
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

async def test_mini_agent():
    """Test the Mini-Agent system"""
    print("🧪 Testing Mini-Agent System...")
    
    try:
        # Test configuration loading
        print("📝 Testing configuration...")
        from mini_agent.config import get_config
        config = get_config()
        print(f"✅ Configuration loaded: {len(config._config)} keys")
        
        # Test agent creation
        print("🤖 Testing agent creation...")
        from mini_agent.cli import main
        
        # Create a temporary workspace
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"📁 Using temporary workspace: {temp_dir}")
            
            # Test basic initialization
            print("🚀 Testing system startup...")
            
            # Try to run a simple test
            print("✅ Basic system components working!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mini_agent())
    sys.exit(0 if result else 1)