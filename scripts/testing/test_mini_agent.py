#!/usr/bin/env python3
"""Test script to verify complete Mini-Agent functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mini_agent.agent import Agent
from mini_agent.schema import Message

async def test_mini_agent():
    """Test the Mini-Agent directly."""
    
    print("🧪 Testing Complete Mini-Agent...")
    
    # Check environment variables
    zai_api_key = os.getenv("ZAI_API_KEY")
    if not zai_api_key:
        print("❌ ZAI_API_KEY environment variable not found")
        return False
    
    print(f"✅ Z.AI API key found: {zai_api_key[:10]}...")
    
    try:
        # Initialize Mini-Agent
        agent = Agent()
        print("✅ Mini-Agent initialized successfully")
        
        # Test with a simple message
        messages = [
            Message(
                role="user",
                content="Hello! Please respond with a brief greeting."
            )
        ]
        
        print("🧪 Testing Mini-Agent response...")
        result = await agent.process_message(messages[0])
        
        if result:
            print("✅ Mini-Agent responded successfully!")
            print(f"📝 Response: {str(result.content)[:200]}...")
            return True
        else:
            print("❌ Mini-Agent did not respond")
            return False
            
    except Exception as e:
        print(f"❌ Mini-Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🚀 Starting Complete Mini-Agent Test\n")
    
    success = await test_mini_agent()
    
    if success:
        print("\n🎉 Complete Mini-Agent Test PASSED!")
        print("✅ Mini-Agent is ready for full use")
    else:
        print("\n💥 Complete Mini-Agent Test FAILED!")
        print("❌ Mini-Agent needs further setup")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)