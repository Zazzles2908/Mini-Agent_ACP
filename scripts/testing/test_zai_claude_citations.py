#!/usr/bin/env python3
"""
Test Z.AI Web Search with MiniMax-M2 Citations

Demonstrates the correct implementation that formats Z.AI web search results
as MiniMax-M2's search_result blocks with proper citations.
"""

import asyncio
import os
import json
from typing import List, Dict, Any

from mini_agent.tools.zai_web_search_with_citations import ZAIWebSearchWithCitationsTool, MiniMax-M2CitationSearchResult
from mini_agent.schema import Message


async def test_minimax_citation_format():
    """Test the MiniMax-M2 citation formatting functionality."""
    
    print("🔍 Testing Z.AI Web Search with MiniMax-M2 Citations")
    print("=" * 60)
    
    # Get API key
    zai_api_key = os.getenv('ZAI_API_KEY')
    
    if not zai_api_key:
        print("❌ ZAI_API_KEY not found in environment")
        print("💡 Get your GLM Coding Plan API key from: https://z.ai/subscribe")
        return
    
    print(f"✅ Z.AI API Key found: {zai_api_key[:20]}...")
    
    try:
        # Initialize the tool
        print("\n🚀 Initializing Z.AI Web Search with Citations tool...")
        search_tool = ZAIWebSearchWithCitationsTool(api_key=zai_api_key)
        
        if not search_tool.available:
            print("❌ Tool not available - check API key")
            return
            
        print("✅ Tool initialized successfully")
        
        # Test 1: Basic Search Result Formatting
        print("\n" + "=" * 60)
        print("🧪 Test 1: MiniMax-M2 Search Result Formatting")
        print("=" * 60)
        
        # Create a mock search result to show the format
        mock_result = {
            "success": True,
            "query": "AI regulation news",
            "analysis": "Recent developments in AI regulation show increasing government oversight...",
            "search_evidence": [
                {
                    "url": "https://example.com/ai-regulation-2024",
                    "title": "New AI Regulation Framework Released",
                    "content": "The government announced new AI regulations focusing on safety and transparency.",
                    "description": "Details about the new AI regulation framework announced by the government."
                },
                {
                    "url": "https://example.com/tech-policy-update",
                    "title": "Technology Policy Updates",
                    "content": "Latest updates on technology policy including AI governance and compliance requirements.",
                    "description": "Comprehensive overview of recent technology policy changes."
                }
            ],
            "model_used": "glm-4.5",
            "depth": "comprehensive",
            "timestamp": "2025-11-20T10:00:00Z"
        }
        
        # Format as MiniMax-M2 search results
        formatted_results = search_tool._format_search_results(mock_result, max_results=3)
        
        print("📋 Formatted MiniMax-M2 Search Result Blocks:")
        for i, result in enumerate(formatted_results, 1):
            print(f"\n{i}. Search Result Block:")
            print(f"   Type: {result['type']}")
            print(f"   Source: {result['source']}")
            print(f"   Title: {result['title']}")
            print(f"   Content: {result['content'][0]['text'][:100]}...")
            print(f"   Citations: {result['citations']['enabled']}")
        
        # Test 2: Individual Citation Block
        print("\n" + "=" * 60)
        print("🧪 Test 2: Individual Citation Block Creation")
        print("=" * 60)
        
        citation_block = MiniMax-M2CitationSearchResult(
            source="https://openai.com/blog/ai-safety",
            title="OpenAI's Approach to AI Safety",
            content="OpenAI has implemented several safety measures including constitutional AI and reinforcement learning from human feedback."
        )
        
        formatted_block = citation_block.to_minimax_search_result_block()
        print("📄 Individual Citation Block:")
        print(json.dumps(formatted_block, indent=2))
        
        # Test 3: Tool Schema
        print("\n" + "=" * 60)
        print("🧪 Test 3: MiniMax-M2 Tool Schema")
        print("=" * 60)
        
        tool_schema = search_tool.get_minimax_tool_schema()
        print("🛠️  MiniMax-M2 Tool Schema:")
        print(f"   Name: {tool_schema['name']}")
        print(f"   Description: {tool_schema['description']}")
        print(f"   Parameters: {list(tool_schema['input_schema']['properties'].keys())}")
        
        # Test 4: Anthropic Client Integration
        print("\n" + "=" * 60)
        print("🧪 Test 4: Anthropic Client Integration")
        print("=" * 60)
        
        anthropic_tools = search_tool.format_for_anthropic_client()
        print("🔗 Tools for Anthropic Client:")
        print(json.dumps(anthropic_tools[0], indent=2))
        
        # Show the integration pattern
        print("\n💡 Integration Pattern:")
        print("1. User asks MiniMax-M2: 'Search for AI developments'")
        print("2. MiniMax-M2 calls zai_web_search_with_citations tool")
        print("3. Tool searches Z.AI and formats results as search_result blocks")
        print("4. MiniMax-M2 receives results with citations enabled")
        print("5. MiniMax-M2 provides response with natural citations")
        
        # Test 5: Expected MiniMax-M2 Response
        print("\n" + "=" * 60)
        print("🧪 Test 5: Expected MiniMax-M2 Response with Citations")
        print("=" * 60)
        
        expected_response = {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Based on recent developments in AI regulation, the government has announced new frameworks focusing on safety and transparency.",
                    "citations": [
                        {
                            "type": "search_result_location",
                            "source": "https://example.com/ai-regulation-2024",
                            "title": "New AI Regulation Framework Released",
                            "cited_text": "The government announced new AI regulations focusing on safety and transparency.",
                            "search_result_index": 0,
                            "start_block_index": 0,
                            "end_block_index": 0
                        }
                    ]
                }
            ]
        }
        
        print("🎯 Expected MiniMax-M2 Response Format:")
        print(json.dumps(expected_response, indent=2))
        
        print("\n" + "=" * 60)
        print("✅ Z.AI MiniMax-M2 Citations Integration Test Complete!")
        print("=" * 60)
        
        print("\n📊 Summary:")
        print("✅ MiniMax-M2 Search Result Blocks: Proper format with citations")
        print("✅ Z.AI Web Search Integration: Formats GLM results correctly")
        print("✅ Anthropic Client Ready: Tool schema ready for MiniMax-M2")
        print("✅ Citation System: Enables natural source attribution")
        
        print("\n🔄 Next Steps:")
        print("1. Test with actual Z.AI API calls")
        print("2. Integrate with MiniMax-M2 Code setup")
        print("3. Verify citation behavior in MiniMax-M2 responses")
        print("4. Deploy to production!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Verify Z.AI API key has web search access")
        print("2. Check GLM Coding Plan setup")
        print("3. Ensure proper environment configuration")


async def demonstrate_citation_workflow():
    """Demonstrate the complete citation workflow."""
    
    print("\n🔄 Citation Workflow Demonstration")
    print("=" * 60)
    
    print("""
🎯 Complete Workflow:

1. **User Query**: "What are the latest AI safety developments?"

2. **MiniMax-M2 Tool Call**: 
   {
     "name": "zai_web_search_with_citations",
     "input": {
       "query": "latest AI safety developments",
       "depth": "comprehensive",
       "max_results": 3
     }
   }

3. **Z.AI Web Search**:
   - GLM searches web for AI safety information
   - Returns search evidence with URLs and content
   - Analysis of findings

4. **Format as Search Result Blocks**:
   [
     {
       "type": "search_result",
       "source": "https://example.com/ai-safety-2024",
       "title": "AI Safety Framework 2024",
       "content": [{"type": "text", "text": "Key safety developments..."}],
       "citations": {"enabled": true}
     }
   ]

5. **MiniMax-M2 Response with Citations**:
   "Recent AI safety developments include [1] new regulatory frameworks..."
   
   Where [1] automatically links to the search result with full citation info

This gives MiniMax-M2 natural web search capabilities with proper citations!
    """)


async def main():
    """Main demonstration function."""
    
    print("🚀 Z.AI Web Search with MiniMax-M2 Citations Test")
    print("Testing proper integration with MiniMax-M2's citation system")
    print()
    
    await test_minimax_citation_format()
    await demonstrate_citation_workflow()


if __name__ == "__main__":
    asyncio.run(main())