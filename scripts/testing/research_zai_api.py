#!/usr/bin/env python3
"""Research Z.AI API documentation to fix implementation."""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.tools.zai_tools import ZAIWebSearchTool

async def research_zai_api():
    """Research Z.AI API documentation to understand correct implementation."""
    
    print("=" * 80)
    print("Z.AI API RESEARCH FOR CORRECT IMPLEMENTATION")
    print("=" * 80)
    
    search_tool = ZAIWebSearchTool()
    
    if not search_tool.available:
        print("❌ Z.AI search tool not available")
        return
    
    # Research Z.AI API documentation
    print("\n🔍 Researching Z.AI API documentation...")
    result = await search_tool.execute(
        query="Z.AI API documentation web reader endpoint reader API specification GLM models",
        depth="deep"
    )
    
    if result.success:
        print("✅ Web search successful")
        print("\nContent from search results:")
        print("-" * 50)
        print(result.content)
        print("-" * 50)
    else:
        print(f"❌ Web search failed: {result.error}")
    
    # Research GLM model specifications
    print("\n🔍 Researching GLM model specifications...")
    result2 = await search_tool.execute(
        query="GLM-4.5 GLM-4.6 model specification Z.AI API model selection",
        depth="comprehensive"
    )
    
    if result2.success:
        print("✅ GLM model search successful")
        print("\nGLM model information:")
        print("-" * 50)
        print(result2.content[:500] + "..." if len(result2.content) > 500 else result2.content)
        print("-" * 50)
    else:
        print(f"❌ GLM model search failed: {result2.error}")

if __name__ == "__main__":
    asyncio.run(research_zai_api())