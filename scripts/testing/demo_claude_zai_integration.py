#!/usr/bin/env python3
"""Demo script showing MiniMax-M2 Z.AI integration with search result blocks."""

import asyncio
import json
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.llm.minimax_zai_client import MiniMax-M2ZAIWebSearchClient, get_zai_api_key


async def demonstrate_minimax_integration():
    """Demonstrate how Z.AI web search results format for MiniMax-M2."""
    print("🚀 MiniMax-M2 Z.AI Web Search Integration Demo")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return
    
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    print("🔍 Performing web search for 'Python web scraping 2024'...")
    
    # Perform search
    search_blocks = await client.web_search_for_minimax(
        query="Python web scraping best practices 2024",
        count=3,
        search_engine="search-prime"
    )
    
    print(f"✅ Generated {len(search_blocks)} search result blocks")
    
    # Display formatted results
    print("\n📋 MiniMax-M2 Search Result Blocks:")
    print("=" * 60)
    
    for i, block in enumerate(search_blocks):
        print(f"\n🔗 Search Result Block {i+1}:")
        print(f"   Type: {block.type}")
        print(f"   Title: {block.title}")
        print(f"   Source: {block.source}")
        print(f"   Citations Enabled: {block.citations.get('enabled', False)}")
        print(f"   Content: {block.content[0]['text'][:150]}...")
    
    # Show how these would be passed to MiniMax-M2
    print(f"\n🤖 How MiniMax-M2 Would Use These Results:")
    print("=" * 60)
    
    print("""
# Tool Execution Results Format:
tool_result = [
    {
        "type": "search_result",
        "source": "https://example.com/scraping-guide",
        "title": "Python Web Scraping Best Practices",
        "content": [{"type": "text", "text": "Content about web scraping..."}],
        "citations": {"enabled": True}
    },
    # ... more search result blocks
]

# MiniMax-M2 automatically cites when using information:
# "According to the scraping guide at example.com, you should always..."
# [Citation automatically added by MiniMax-M2]
""")
    
    # Show the complete JSON structure for tool result
    print("\n📄 Complete Tool Result JSON:")
    print("=" * 60)
    
    minimax_tool_result = []
    for block in search_blocks:
        minimax_tool_result.append({
            "type": block.type,
            "source": block.source,
            "title": block.title,
            "content": block.content,
            "citations": block.citations
        })
    
    print(json.dumps(minimax_tool_result, indent=2))
    
    print(f"\n💡 Key Benefits:")
    print("✅ Natural citations - MiniMax-M2 cites like web search")
    print("✅ Structured format - Matches MiniMax-M2's search_result schema")
    print("✅ Usage tracking - ~120 prompts every 5 hours")
    print("✅ Quality integration - Seamless MiniMax-M2 Code workflow")


async def demonstrate_research_workflow():
    """Demonstrate complete research workflow."""
    print(f"\n\n🔬 Research Workflow Demo")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        return
        
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    # Comprehensive research
    research_result = await client.research_and_analyze_for_minimax(
        query="AI coding assistants comparison 2024",
        depth="comprehensive",
        search_engine="search-prime"
    )
    
    if research_result.get("success"):
        print("✅ Research completed successfully")
        print(f"   Query: {research_result['query']}")
        print(f"   Depth: {research_result['depth']}")
        print(f"   Sources: {research_result['source_count']}")
        print(f"   Integration: {research_result['integration_type']}")
        
        # Show how this would integrate with MiniMax-M2 workflow
        print(f"\n🔄 MiniMax-M2 Workflow Integration:")
        print("1. User asks: 'Compare AI coding assistants'")
        print("2. Tool executes: minimax_zai_web_search")
        print("3. Tool returns: search_result blocks")
        print("4. MiniMax-M2 cites: Automatically adds citations")
        print("5. User gets: Evidence-based response with sources")
        
    else:
        print(f"❌ Research failed: {research_result.get('error')}")


async def main():
    """Run the complete demonstration."""
    await demonstrate_minimax_integration()
    await demonstrate_research_workflow()
    
    print(f"\n🎯 Summary:")
    print("The Z.AI integration enables MiniMax-M2 to cite web search results")
    print("naturally by formatting search results as search_result blocks.")
    print("This provides web search-quality citations for custom applications!")


if __name__ == "__main__":
    asyncio.run(main())
