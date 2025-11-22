#!/usr/bin/env python3
"""
Direct Z.AI Web Search Test for docs.z.ai/devpack/tool/minimax
"""

import asyncio
import sys
from pathlib import Path

# Add mini_agent to path
sys.path.insert(0, '.')

from mini_agent.llm.minimax_zai_client import MiniMax-M2ZAIWebSearchClient, get_zai_api_key

async def search_devpack_minimax():
    print("🔍 Searching for docs.z.ai/devpack/tool/minimax")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    # Search for the specific URL
    try:
        result = await client.web_search_for_minimax(
            query="site:docs.z.ai/devpack/tool/minimax",
            count=10,
            search_engine="search-prime"
        )
        
        print(f"✅ Search completed! Found {len(result)} results")
        print(f"\n📋 RAW SEARCH RESULTS:")
        print("=" * 60)
        
        for i, block in enumerate(result, 1):
            print(f"\n--- RESULT {i} ---")
            print(f"Type: {block.type}")
            print(f"Source: {block.source}")
            print(f"Title: {block.title}")
            print(f"Content: {block.content[0]['text']}")
            print(f"Citations: {block.citations}")
            print(f"--- END RESULT {i} ---")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")
        print(f"Exception type: {type(e).__name__}")
    
    # Also try a broader search
    print(f"\n" + "=" * 60)
    print("🔍 BROADER SEARCH: Z.AI DevPack MiniMax-M2 integration")
    print("=" * 60)
    
    try:
        result2 = await client.web_search_for_minimax(
            query="Z.AI DevPack MiniMax-M2 integration tool configuration",
            count=5,
            search_engine="search-prime"
        )
        
        print(f"✅ Broader search completed! Found {len(result2)} results")
        
        for i, block in enumerate(result2, 1):
            print(f"\n--- BROADER RESULT {i} ---")
            print(f"Source: {block.source}")
            print(f"Title: {block.title}")
            print(f"Content preview: {block.content[0]['text'][:200]}...")
            print(f"--- END BROADER RESULT {i} ---")
            
    except Exception as e:
        print(f"❌ Broader search failed: {e}")

if __name__ == "__main__":
    asyncio.run(search_devpack_minimax())