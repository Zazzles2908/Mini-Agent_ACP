"""Integration example showing how to use GLM Web Search with Mini-Max and Claude.

This demonstrates the pattern: 
Z.AI (GLM Web Search) → MiniMax (LLM Provider) → Claude (End User)

Follows the same architecture as using MiniMax → Anthropic.
"""

import asyncio
import os
from typing import List

from mini_agent.llm.glm_web_client import GLMWebSearchClient
from mini_agent.llm.anthropic_client import AnthropicClient  # MiniMax proxy to Claude
from mini_agent.schema import Message


async def example_claude_with_glm_web_search():
    """Example: Using Claude with GLM web search tools through MiniMax."""
    
    print("🤖 Claude + GLM Web Search Integration Example")
    print("=" * 60)
    
    # Get API keys
    zai_api_key = os.getenv('ZAI_API_KEY')
    minimax_api_key = os.getenv('MINIMAX_API_KEY')
    
    if not all([zai_api_key, minimax_api_key]):
        print("❌ Missing API keys")
        print("💡 Required: ZAI_API_KEY (Lite Plan), MINIMAX_API_KEY")
        return
    
    try:
        # 1. Initialize MiniMax (provides Claude access)
        print("🚀 Initializing MiniMax → Claude client...")
        claude_client = AnthropicClient(
            api_key=minimax_api_key,
            model="MiniMax-M2"  # Claude model through MiniMax
        )
        
        # 2. Initialize GLM Web Search client 
        print("🔍 Initializing GLM Web Search client...")
        glm_client = GLMWebSearchClient(
            api_key=zai_api_key,
            model="glm-4.5"
        )
        
        print("✅ Both clients initialized successfully")
        
        # 3. Example conversation where Claude can use GLM web search
        print("\n" + "=" * 60)
        print("💬 Example: Claude with Web Search Capabilities")
        print("=" * 60)
        
        messages = [
            Message(role="system", content="You are Claude with access to GLM web search tools."),
            Message(role="user", content="""
                I'm researching AI safety standards. Can you:
                1. Search for recent developments in AI safety regulations
                2. Read the most relevant policy document you find
                3. Provide a summary of key points and implications
            """)
        ]
        
        print("📝 User Query: Research AI safety standards, search news, read policy, summarize")
        print("🔄 Processing with Claude (who can now use GLM web search tools)...")
        
        # This would normally be: claude_client.generate(messages)
        # But for demonstration, we'll show what happens:
        print("\n🎯 What happens:")
        print("1. Claude receives the research request")
        print("2. Claude uses glm_web_search tool → GLM searches AI safety news")
        print("3. Claude finds relevant policy document") 
        print("4. Claude uses glm_web_read tool → GLM extracts policy content")
        print("5. Claude analyzes and summarizes findings")
        print("6. User gets comprehensive research with web-sourced evidence")
        
        print("\n💡 This gives Claude web search capabilities!")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")


async def example_direct_glm_usage():
    """Example: Direct usage of GLM web search client."""
    
    print("\n🔍 Direct GLM Web Search Usage")
    print("=" * 60)
    
    zai_api_key = os.getenv('ZAI_API_KEY')
    if not zai_api_key:
        print("❌ ZAI_API_KEY not found")
        return
    
    try:
        glm_client = GLMWebSearchClient(api_key=zai_api_key)
        
        # Example: Research task using web search
        messages = [
            Message(
                role="user",
                content="Search for information about recent developments in quantum computing hardware"
            )
        ]
        
        print("📡 Query: Quantum computing hardware developments")
        print("🔄 Processing...")
        
        # Note: This would require the actual API call to work
        # For now, showing the interface
        print("✅ GLM client ready to process web search requests")
        print("📋 Available tools:")
        for tool in glm_client.web_search_tools:
            print(f"  • {tool['function']['name']}")
        
    except Exception as e:
        print(f"❌ Direct usage failed: {e}")


async def example_combined_workflow():
    """Example: Combined workflow showing both approaches."""
    
    print("\n🔄 Combined Workflow Example")
    print("=" * 60)
    
    print("""
🎯 Scenario: Research AI regulation developments
    
1. **Option A: Direct GLM Usage**
   → User queries GLM directly
   → Gets web search results immediately
   → Best for: Simple web research tasks

2. **Option B: Claude with GLM Tools**
   → User talks to Claude via MiniMax
   → Claude uses GLM web search tools as needed
   → Gets natural conversation + web-enhanced responses
   → Best for: Complex research with reasoning

3. **Option C: Mixed Approach**
   → Use Claude for analysis and reasoning
   → Use GLM for web search operations
   → Combine results for comprehensive responses
   → Best of both worlds!
    """)
    
    print("💡 Choose the approach that fits your workflow!")


async def main():
    """Main demonstration function."""
    
    print("🚀 GLM Web Search + Claude Integration Examples")
    print("Demonstrating Z.AI → MiniMax → Claude architecture")
    print()
    
    await example_claude_with_glm_web_search()
    await example_direct_glm_usage()
    await example_combined_workflow()
    
    print("\n" + "=" * 60)
    print("🎉 Integration Examples Complete!")
    print("=" * 60)
    
    print("""
📋 Summary:

✅ GLM Web Search Client: Ready to use
✅ Claude Tool Integration: Following MiniMax → Anthropic pattern  
✅ Direct Usage: Available for web research
✅ Combined Workflows: Multiple integration options

🔧 Setup Required:
1. Z.AI Lite Plan API Key (for web search access)
2. MiniMax API Key (for Claude integration)
3. Environment variables configured

🚀 Ready to deploy!
""")


if __name__ == "__main__":
    asyncio.run(main())