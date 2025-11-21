#!/usr/bin/env python3
"""Test script to verify full Mini-Agent system integration."""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mini_agent.llm.llm_wrapper import LLMClient
from mini_agent.schema import Message, LLMProvider

async def test_full_system():
    """Test the complete Mini-Agent system."""
    
    print("🧪 Testing Full Mini-Agent System...")
    
    # Check environment variables
    zai_api_key = os.getenv("ZAI_API_KEY")
    if not zai_api_key:
        print("❌ ZAI_API_KEY environment variable not found")
        return False
    
    print(f"✅ Z.AI API key found: {zai_api_key[:10]}...")
    
    # Initialize LLM client wrapper
    try:
        llm_client = LLMClient(
            api_key=zai_api_key,
            provider=LLMProvider.ZAI,
            model="glm-4.6"
        )
        print("✅ LLM wrapper initialized successfully")
    except Exception as e:
        print(f"❌ LLM wrapper initialization failed: {e}")
        return False
    
    # Test message generation through wrapper
    try:
        messages = [
            Message(
                role="user",
                content="Hello! Please tell me about GLM-4.6 and its capabilities."
            )
        ]
        
        print("🧪 Testing LLM wrapper with GLM-4.6...")
        result = await llm_client.generate(messages)
        
        if result.finish_reason == "stop":
            print("✅ LLM wrapper API call successful!")
            print(f"📝 Response: {result.content[:300]}...")
            return True
        else:
            print(f"❌ LLM wrapper API call failed: {result.content}")
            return False
            
    except Exception as e:
        print(f"❌ LLM wrapper test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting Full Mini-Agent System Test\n")
    
    success = await test_full_system()
    
    if success:
        print("\n🎉 Full Mini-Agent System Test PASSED!")
        print("✅ Complete GLM-4.6 integration working")
    else:
        print("\n💥 Full Mini-Agent System Test FAILED!")
        print("❌ System needs further troubleshooting")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)