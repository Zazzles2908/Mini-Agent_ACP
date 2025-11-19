#!/usr/bin/env python3
"""
Simple Z.AI Web Search Evidence Test
"""

import asyncio
import os
from mini_agent.llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key

async def test_web_search():
    print("🔍 Z.AI Web Search Raw Evidence Test")
    print("=" * 50)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API Key: {api_key[:20]}...{api_key[-10:]}")
    
    client = ClaudeZAIWebSearchClient(api_key)
    print(f"🌐 Base URL: {client.base_url}")
    
    try:
        print("\n🧪 Testing web search...")
        result = await client.web_search_for_claude(
            query="Python web scraping libraries",
            count=3,
            search_engine="search-prime"
        )
        
        print(f"✅ Search completed! Got {len(result)} results")
        if result:
            print(f"First result: {result[0].source}")
            print(f"Title: {result[0].title}")
            print(f"Content length: {len(result[0].content[0]['text'])}")
        
        print("\n🧪 Testing research...")
        research = await client.research_and_analyze_for_claude(
            query="AI coding assistants",
            depth="quick"
        )
        
        print(f"✅ Research completed!")
        print(f"Success: {research.get('success')}")
        print(f"Sources: {research.get('source_count')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_web_search())