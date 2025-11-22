#!/usr/bin/env python3
"""
Z.AI Web Reader Fix Test
Tests web reading with corrected parameters
"""

import sys
import os
import asyncio
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔧 Z.AI Web Reader Fix Test")
print("=" * 40)

async def test_web_reader_direct():
    """Test web reader with minimal parameters."""
    print("\n1. Testing Z.AI Web Reader (Direct):")
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        client = ZAIClient(os.environ.get('ZAI_API_KEY'))
        
        # Test with minimal parameters
        test_url = "https://httpbin.org/html"
        print(f"   📖 Reading: {test_url}")
        
        result = await client.web_reading(
            url=test_url,
            format_type="text",
            include_images=False
        )
        
        if result.get("success"):
            print("   ✅ Web reader works!")
            print(f"   📝 Content length: {len(result.get('content', ''))} chars")
        else:
            print(f"   ❌ Web reader failed: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ Web reader test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_web_search():
    """Test simple web search."""
    print("\n2. Testing Z.AI Web Search (Simple):")
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        client = ZAIClient(os.environ.get('ZAI_API_KEY'))
        
        # Test simple search
        query = "Python"
        print(f"   🔍 Searching: '{query}'")
        
        result = await client.web_search(query=query, count=3)
        
        if result.get("success"):
            print("   ✅ Web search works!")
            print(f"   📝 Results: {len(result.get('search_result', []))} found")
        else:
            print(f"   ❌ Web search failed: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ Web search test failed: {e}")

async def main():
    await test_web_reader_direct()
    await test_simple_web_search()
    print("\n🎯 Z.AI FUNCTIONALITY TESTS COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
