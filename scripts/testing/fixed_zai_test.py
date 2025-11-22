#!/usr/bin/env python3
"""
Fixed Z.AI Integration Test
"""

import os
import sys
from pathlib import Path

# Set working directory to Mini-Agent
os.chdir("C:\\Users\\Jazeel-Home\\Mini-Agent")
print(f"Working directory: {os.getcwd()}")

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        print(f"📋 Loading environment from: {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
                    print(f"✅ Set {key}: {value[:20]}...")
    else:
        print(f"❌ .env file not found at: {env_file.absolute()}")

# Load environment
load_env_file()

# Add Mini-Agent to path
sys.path.insert(0, os.getcwd())

try:
    from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
    
    print("\n🧪 Testing Z.AI Integration")
    print("=" * 40)
    
    # Check API key
    api_key = get_zai_api_key()
    if api_key:
        print(f"✅ Z.AI API key loaded: {api_key[:20]}...")
        
        # Initialize client
        client = ZAIClient(api_key)
        print("✅ Z.AI client initialized")
        
        # Test simple web search
        import asyncio
        
        async def test_search():
            print("\n🔍 Testing web search...")
            try:
                result = await client.research_and_analyze(
                    query="GLM model capabilities",
                    depth="quick",
                    model_preference="glm-4.6"
                )
                
                if result.get("success"):
                    print("✅ Web search successful!")
                    print(f"Model: {result['model_used']}")
                    print(f"Analysis preview: {result['analysis'][:200]}...")
                    return True
                else:
                    print(f"❌ Search failed: {result.get('error')}")
                    return False
            except Exception as e:
                print(f"❌ Search exception: {e}")
                return False
        
        # Run test
        success = asyncio.run(test_search())
        
        if success:
            print("\n🎉 Z.AI integration is working correctly!")
            print("   • Native GLM web search is functional")
            print("   • API key is valid")
            print("   • Ready for production use")
            print("\n📝 Available tools:")
            print("   • zai_web_search - Native GLM web search")
            print("   • zai_web_reader - Web page reading")
        else:
            print("\n⚠️ Z.AI integration needs attention")
            
    else:
        print("❌ Z.AI API key not found in environment")
        print("   Check .env file and environment variables")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure all dependencies are installed")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
