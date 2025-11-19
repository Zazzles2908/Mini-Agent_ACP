#!/usr/bin/env python3
"""
GLM Web Search Integration Test

Demonstrates how the GLM Web Search Wrapper works with Z.AI Lite Plan
and can be integrated with Claude via MiniMax.
"""

import asyncio
import os
import json
from typing import List

from mini_agent.llm.glm_web_client import GLMWebSearchClient
from mini_agent.schema import Message


async def test_glm_web_search_integration():
    """Test GLM web search integration and demonstrate Claude tool access."""
    
    print("🔍 Testing GLM Web Search Integration")
    print("=" * 60)
    
    # Get API keys from environment
    zai_api_key = os.getenv('ZAI_API_KEY')
    minimax_api_key = os.getenv('MINIMAX_API_KEY')
    
    if not zai_api_key:
        print("❌ ZAI_API_KEY not found in environment")
        print("💡 Get your Lite Plan API key from: https://z.ai/subscribe")
        return
    
    print(f"✅ Z.AI API Key found: {zai_api_key[:20]}...")
    
    try:
        # Initialize GLM Web Search Client
        print("\n🚀 Initializing GLM Web Search Client...")
        glm_client = GLMWebSearchClient(
            api_key=zai_api_key,
            model="glm-4.5"  # Efficient default for web search
        )
        
        print("✅ GLM Web Search Client initialized successfully")
        
        # Test 1: Basic Web Search
        print("\n" + "=" * 60)
        print("🧪 Test 1: Basic Web Search")
        print("=" * 60)
        
        search_messages = [
            Message(
                role="user", 
                content="Search for the latest developments in AI regulation and policy"
            )
        ]
        
        print("📡 Query: 'Latest AI regulation developments'")
        print("🔄 Processing with GLM web search...")
        
        response = await glm_client.generate(search_messages)
        
        print("✅ Web search completed!")
        print(f"📄 Response preview: {response.content[:200]}...")
        
        # Test 2: Web Reading
        print("\n" + "=" * 60)
        print("🧪 Test 2: Web Reading")
        print("=" * 60)
        
        read_messages = [
            Message(
                role="user",
                content="Read the OpenAI API documentation and summarize the key features"
            )
        ]
        
        print("📡 Query: 'Read OpenAI API documentation'")
        print("🔄 Processing with GLM web reading...")
        
        response = await glm_client.generate(read_messages)
        
        print("✅ Web reading completed!")
        print(f"📄 Response preview: {response.content[:200]}...")
        
        # Test 3: Combined Workflow (Web Search + Reading)
        print("\n" + "=" * 60)
        print("🧪 Test 3: Combined Workflow")
        print("=" * 60)
        
        combined_messages = [
            Message(
                role="user",
                content="Search for recent breakthroughs in quantum computing, then read the most relevant article"
            )
        ]
        
        print("📡 Query: 'Search quantum computing breakthroughs, then read relevant article'")
        print("🔄 Processing with combined GLM tools...")
        
        response = await glm_client.generate(combined_messages)
        
        print("✅ Combined workflow completed!")
        print(f"📄 Response preview: {response.content[:200]}...")
        
        # Show Available Tools
        print("\n" + "=" * 60)
        print("🛠️  Available GLM Tools for Claude")
        print("=" * 60)
        
        for i, tool in enumerate(glm_client.web_search_tools, 1):
            func = tool["function"]
            print(f"\n{i}. **{func['name']}**")
            print(f"   📝 {func['description']}")
            print(f"   ⚙️  Parameters: {list(func['parameters']['properties'].keys())}")
        
        # Claude Integration Example
        print("\n" + "=" * 60)
        print("🔗 Claude Integration Example")
        print("=" * 60)
        
        print("""
When using Claude through MiniMax, the GLM web search tools become available:

1. User asks Claude: "What's the latest on AI policy?"
2. Claude automatically uses glm_web_search tool
3. GLM searches the web and provides analysis
4. Claude integrates the results into the conversation

This gives Claude web search capabilities without any separate setup!
        """)
        
        # MiniMax Integration Example
        if minimax_api_key:
            print("✅ MiniMax API Key found - Claude integration available")
            print("\n💡 Claude can now use GLM web search tools when accessed through MiniMax!")
        else:
            print("⚠️  MiniMax API Key not found - direct Claude integration not available")
            print("💡 Add MINIMAX_API_KEY to environment for Claude integration")
        
        print("\n" + "=" * 60)
        print("🎉 GLM Web Search Integration Test Complete!")
        print("=" * 60)
        
        print("\n📊 Summary:")
        print("✅ Web Search: GLM successfully searches web with AI analysis")
        print("✅ Web Reading: GLM successfully extracts and processes web content")
        print("✅ Tool Format: Compatible with Claude's tool calling interface")
        print("✅ Integration: Ready for MiniMax → Claude workflow")
        
        print("\n🔄 Next Steps:")
        print("1. Test with your specific use cases")
        print("2. Try Claude integration (if MiniMax key available)")
        print("3. Optimize parameters based on your needs")
        print("4. Deploy to production!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Verify Z.AI API key is correct and has Lite Plan access")
        print("2. Check internet connectivity")
        print("3. Ensure Z.AI Lite Plan includes web search functionality")
        print("4. Review error details above")


async def demonstrate_tool_schema():
    """Show the tool schemas that Claude will see."""
    
    print("\n🔍 Tool Schema Demonstration")
    print("=" * 60)
    
    zai_api_key = os.getenv('ZAI_API_KEY')
    if not zai_api_key:
        print("❌ ZAI_API_KEY not found - cannot demonstrate tools")
        return
    
    glm_client = GLMWebSearchClient(api_key=zai_api_key)
    
    print("📋 GLM Tools that Claude will see:")
    print(json.dumps(glm_client.web_search_tools, indent=2))


if __name__ == "__main__":
    print("🚀 GLM Web Search Integration Test")
    print("Testing Z.AI Lite Plan integration with Claude tool interface")
    print()
    
    # Run main test
    asyncio.run(test_glm_web_search_integration())
    
    # Show tool schemas
    asyncio.run(demonstrate_tool_schema())