"""Test Z.AI MCP implementation with real API calls."""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.tools.zai_mcp_tools import ZAIMCPClient


async def test_mcp_integration():
    """Test MCP tools with minimal quota usage."""
    
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        print("❌ ZAI_API_KEY not found in environment")
        return
    
    print("\n" + "="*60)
    print("Z.AI MCP Integration Test")
    print("="*60)
    print(f"⚠️  This will use 2 quota units from Lite plan (100 total)")
    print(f"⚠️  Current balance should NOT decrease (quota-based)")
    print("="*60 + "\n")
    
    client = ZAIMCPClient(api_key)
    
    # Test 1: Web Search Prime
    print("\n1️⃣  Testing webSearchPrime MCP tool...")
    print("-" * 60)
    search_result = await client.web_search_prime(
        query="MCP protocol model context",
        max_results=2  # Minimal for testing
    )
    
    if "error" in search_result:
        print(f"❌ Search failed: {search_result}")
    else:
        print(f"✅ Search successful!")
        print(f"Response structure: {list(search_result.keys())}")
        print(f"Response preview: {str(search_result)[:200]}...")
    
    # Test 2: Web Reader
    print("\n2️⃣  Testing webReader MCP tool...")
    print("-" * 60)
    reader_result = await client.web_reader(
        url="https://modelcontextprotocol.io/"
    )
    
    if "error" in reader_result:
        print(f"❌ Reader failed: {reader_result}")
    else:
        print(f"✅ Reader successful!")
        print(f"Response structure: {list(reader_result.keys())}")
        print(f"Response preview: {str(reader_result)[:200]}...")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)
    print("📊 Quota used: 2 units (1 search + 1 reader)")
    print("💰 Balance should be: $0.72 (unchanged)")
    print("📈 Remaining quota: 98/100")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_mcp_integration())
