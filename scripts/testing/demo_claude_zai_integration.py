#!/usr/bin/env python3
"""Demo script showing Claude Z.AI integration with search result blocks."""

import asyncio
import json
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key


async def demonstrate_claude_integration():
    """Demonstrate how Z.AI web search results format for Claude."""
    print("🚀 Claude Z.AI Web Search Integration Demo")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return
    
    client = ClaudeZAIWebSearchClient(api_key)
    
    print("🔍 Performing web search for 'Python web scraping 2024'...")
    
    # Perform search
    search_blocks = await client.web_search_for_claude(
        query="Python web scraping best practices 2024",
        count=3,
        search_engine="search-prime"
    )
    
    print(f"✅ Generated {len(search_blocks)} search result blocks")
    
    # Display formatted results
    print("\n📋 Claude Search Result Blocks:")
    print("=" * 60)
    
    for i, block in enumerate(search_blocks):
        print(f"\n🔗 Search Result Block {i+1}:")
        print(f"   Type: {block.type}")
        print(f"   Title: {block.title}")
        print(f"   Source: {block.source}")
        print(f"   Citations Enabled: {block.citations.get('enabled', False)}")
        print(f"   Content: {block.content[0]['text'][:150]}...")
    
    # Show how these would be passed to Claude
    print(f"\n🤖 How Claude Would Use These Results:")
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

# Claude automatically cites when using information:
# "According to the scraping guide at example.com, you should always..."
# [Citation automatically added by Claude]
""")
    
    # Show the complete JSON structure for tool result
    print("\n📄 Complete Tool Result JSON:")
    print("=" * 60)
    
    claude_tool_result = []
    for block in search_blocks:
        claude_tool_result.append({
            "type": block.type,
            "source": block.source,
            "title": block.title,
            "content": block.content,
            "citations": block.citations
        })
    
    print(json.dumps(claude_tool_result, indent=2))
    
    print(f"\n💡 Key Benefits:")
    print("✅ Natural citations - Claude cites like web search")
    print("✅ Structured format - Matches Claude's search_result schema")
    print("✅ Usage tracking - ~120 prompts every 5 hours")
    print("✅ Quality integration - Seamless Claude Code workflow")


async def demonstrate_research_workflow():
    """Demonstrate complete research workflow."""
    print(f"\n\n🔬 Research Workflow Demo")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        return
        
    client = ClaudeZAIWebSearchClient(api_key)
    
    # Comprehensive research
    research_result = await client.research_and_analyze_for_claude(
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
        
        # Show how this would integrate with Claude workflow
        print(f"\n🔄 Claude Workflow Integration:")
        print("1. User asks: 'Compare AI coding assistants'")
        print("2. Tool executes: claude_zai_web_search")
        print("3. Tool returns: search_result blocks")
        print("4. Claude cites: Automatically adds citations")
        print("5. User gets: Evidence-based response with sources")
        
    else:
        print(f"❌ Research failed: {research_result.get('error')}")


async def main():
    """Run the complete demonstration."""
    await demonstrate_claude_integration()
    await demonstrate_research_workflow()
    
    print(f"\n🎯 Summary:")
    print("The Z.AI integration enables Claude to cite web search results")
    print("naturally by formatting search results as search_result blocks.")
    print("This provides web search-quality citations for custom applications!")


if __name__ == "__main__":
    asyncio.run(main())
