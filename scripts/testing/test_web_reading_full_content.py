#!/usr/bin/env python3
"""
Test Web Reading to Get Full Page Content
"""

import asyncio
import sys
from pathlib import Path

# Add mini_agent to path
sys.path.insert(0, '.')

from mini_agent.llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key

async def test_web_reading():
    print("📖 Testing Z.AI Web Reading - Get Full Page Content")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    client = ClaudeZAIWebSearchClient(api_key)
    
    # Test reading the actual Claude documentation page
    urls_to_test = [
        "https://docs.z.ai/devpack/tool/claude",
        "https://docs.z.ai/devpack/tool/claude-for-ide"
    ]
    
    for url in urls_to_test:
        print(f"\n🔍 Reading: {url}")
        print("-" * 50)
        
        try:
            result = await client.web_reading(
                url=url,
                format_type="markdown",  # or "text", "html"
                include_images=True
            )
            
            if result.get('success'):
                print(f"✅ Successfully read page!")
                print(f"📋 Title: {result.get('title', 'N/A')}")
                print(f"📊 Word count: {result.get('word_count', 0)}")
                print(f"⏰ Timestamp: {result.get('timestamp', 'N/A')}")
                
                # Show first 500 characters of content
                content = result.get('content', '')
                print(f"\n📄 FULL CONTENT PREVIEW (first 500 chars):")
                print("=" * 40)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("=" * 40)
                
            else:
                print(f"❌ Failed to read page")
                print(f"Error: {result.get('error', 'Unknown error')}")
                
                # Try fallback search if reading fails
                print(f"\n🔄 Trying search fallback...")
                search_result = await client.web_search_for_claude(
                    query=f"content of {url}",
                    count=3,
                    search_engine="search-prime"
                )
                
                if search_result:
                    print(f"✅ Search fallback returned {len(search_result)} results")
                    for i, block in enumerate(search_result, 1):
                        print(f"  {i}. {block.title}")
                        print(f"     Content preview: {block.content[0]['text'][:100]}...")
                        
        except Exception as e:
            print(f"❌ Exception reading page: {e}")
    
    # Also test the combined search + read functionality
    print(f"\n" + "=" * 60)
    print("🔍 Testing Combined Search + Read")
    print("=" * 60)
    
    try:
        # First search for the documentation
        search_result = await client.web_search_for_claude(
            query="Z.AI DevPack Claude Code integration setup steps",
            count=5,
            search_engine="search-prime"
        )
        
        print(f"✅ Search found {len(search_result)} results")
        
        # Then try to read the most relevant result
        if search_result:
            first_result = search_result[0]
            print(f"\n📖 Now reading full content of: {first_result.source}")
            
            read_result = await client.web_reading(
                url=first_result.source,
                format_type="markdown",
                include_images=True
            )
            
            if read_result.get('success'):
                print(f"✅ Full content retrieved!")
                print(f"Title: {read_result.get('title')}")
                print(f"Word count: {read_result.get('word_count')}")
                
                # Show a substantial preview of the content
                content = read_result.get('content', '')
                preview_length = 800
                print(f"\n📄 SUBSTANTIAL CONTENT PREVIEW ({preview_length} chars):")
                print("=" * 60)
                print(content[:preview_length] + "\n... [CONTINUES]" if len(content) > preview_length else content)
                print("=" * 60)
                
    except Exception as e:
        print(f"❌ Combined test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_web_reading())