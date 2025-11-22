#!/usr/bin/env python3
"""
Z.AI Functional Test (Async Corrected)
Tests actual Z.AI web search and reader functionality with proper async handling
"""

import sys
import os
import asyncio
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🧪 Z.AI Functionality Test (Async)")
print("=" * 40)

async def test_zai_web_search():
    """Test Z.AI web search functionality."""
    print("\n1. Testing Z.AI Web Search:")
    try:
        from mini_agent.tools.zai_tools import ZAIWebSearchTool
        
        tool = ZAIWebSearchTool()
        
        # Test with a simple search query
        query = "Python programming tutorial"
        print(f"   🔍 Searching for: '{query}'")
        
        result = await tool.execute(query=query)
        
        if result.success:
            print("   ✅ Web search completed successfully")
            print(f"   📝 Result preview: {result.content[:200]}...")
        else:
            print(f"   ❌ Web search failed: {result.error}")
            
    except Exception as e:
        print(f"   ❌ Web search test failed: {e}")

async def test_zai_web_reader():
    """Test Z.AI web reader functionality."""
    print("\n2. Testing Z.AI Web Reader:")
    try:
        from mini_agent.tools.zai_tools import ZAIWebReaderTool
        
        tool = ZAIWebReaderTool()
        
        # Test with a reliable URL
        test_url = "https://python.org"
        print(f"   📖 Reading content from: {test_url}")
        
        result = await tool.execute(url=test_url)
        
        if result.success:
            print("   ✅ Web reader completed successfully")
            print(f"   📝 Content preview: {result.content[:200]}...")
        else:
            print(f"   ❌ Web reader failed: {result.error}")
            
    except Exception as e:
        print(f"   ❌ Web reader test failed: {e}")

async def main():
    """Main test runner."""
    await test_zai_web_search()
    await test_zai_web_reader()
    
    print("\n🎯 Z.AI FUNCTIONALITY TEST COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
