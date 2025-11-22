#!/usr/bin/env python3
"""Test script to verify GLM-4.6 integration with Z.AI API."""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mini_agent.llm.glm_client import GLMClient
from mini_agent.schema import Message

async def test_glm_client():
    """Test the GLM client with real API calls."""
    
    print("🔧 Testing GLM-4.6 Integration...")
    
    # Check environment variables
    zai_api_key = os.getenv("ZAI_API_KEY")
    if not zai_api_key:
        print("❌ ZAI_API_KEY environment variable not found")
        return False
    
    print(f"✅ Z.AI API key found: {zai_api_key[:10]}...")
    
    # Initialize GLM client
    try:
        glm_client = GLMClient(
            api_key=zai_api_key,
            model="glm-4.6"
        )
        print("✅ GLM client initialized successfully")
    except Exception as e:
        print(f"❌ GLM client initialization failed: {e}")
        return False
    
    # Test basic message generation
    try:
        messages = [
            Message(
                role="user",
                content="Hello! Can you tell me what you are?"
            )
        ]
        
        print("🧪 Testing GLM-4.6 API call...")
        result = await glm_client.generate(messages)
        
        if result.finish_reason == "stop":
            print("✅ GLM-4.6 API call successful!")
            print(f"📝 Response: {result.content[:200]}...")
            return True
        else:
            print(f"❌ GLM-4.6 API call failed: {result.content}")
            return False
            
    except Exception as e:
        print(f"❌ GLM-4.6 API test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting GLM-4.6 Integration Test\n")
    
    success = await test_glm_client()
    
    if success:
        print("\n🎉 GLM-4.6 Integration Test PASSED!")
        print("✅ Mini-Agent can now use GLM-4.6 for reasoning and actions")
    else:
        print("\n💥 GLM-4.6 Integration Test FAILED!")
        print("❌ Mini-Agent will need troubleshooting")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)