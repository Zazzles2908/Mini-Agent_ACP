#!/usr/bin/env python3
"""Test Z.AI web search using the correct Anthropic base URL approach."""

import asyncio
import sys
import os

# Add the mini_agent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mini_agent'))

async def test_vsix_web_search():
    """Test web search using the Anthropic base URL approach for VSIX error research."""
    print("🔍 Testing Z.AI Anthropic Web Search for VSIX Error...")
    
    try:
        # Import the working client
        from llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key
        
        # Get API key
        api_key = get_zai_api_key()
        print(f"API Key available: {bool(api_key)}")
        
        if not api_key:
            print("❌ No Z.AI API key found")
            return
            
        # Initialize client with correct setup
        client = ClaudeZAIWebSearchClient(api_key)
        print(f"Client initialized - using Anthropic base URL approach")
        
        # Test web search for VSIX error information
        query = "VSIX extension package.json not found inside zip error cause solution proper directory structure"
        print(f"Searching for: {query}")
        
        # Perform web search using the working method
        search_blocks = await client.web_search_for_claude(
            query=query,
            count=5,
            search_engine="search-prime",
            recency_filter="noLimit"
        )
        
        print(f"✅ Web search completed! Found {len(search_blocks)} search result blocks")
        
        # Display results in a format that shows the research
        print("\n📊 VSIX Error Research Results:")
        print("=" * 60)
        
        for i, block in enumerate(search_blocks, 1):
            print(f"\n**Result {i}: {block.title}**")
            print(f"Source: {block.source}")
            print(f"Content Preview: {block.content[0]['text'][:150]}...")
            print(f"Citations Enabled: {block.citations.get('enabled', False)}")
            print("-" * 40)
            
        print(f"\n🎯 Summary: {len(search_blocks)} search result blocks generated for Claude citation")
        print("✅ Ready for Claude to cite naturally like web search!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_vsix_web_search())