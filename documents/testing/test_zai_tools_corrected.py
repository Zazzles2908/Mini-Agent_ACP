#!/usr/bin/env python3
"""Test script for Z.AI tools functionality."""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool

async def test_zai_tools():
    """Test both Z.AI web search and web reader tools."""
    
    print("=" * 60)
    print("Z.AI TOOLS FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Check environment
    print(f"ZAI_API_KEY present: {'Yes' if os.getenv('ZAI_API_KEY') else 'No'}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Test Web Search Tool
    print("=== Testing Z.AI Web Search Tool ===")
    try:
        search_tool = ZAIWebSearchTool()
        print(f"Tool available: {search_tool.available}")
        
        if search_tool.available:
            print("Executing web search...")
            result = await search_tool.execute(
                query="Mini-Agent AI assistant capabilities and features 2025",
                depth="quick",
                model="auto"
            )
            
            print(f"Search Success: {result.success}")
            print(f"Content Length: {len(result.content)}")
            
            if result.success:
                print("✅ Web search tool is working correctly")
            else:
                print(f"❌ Web search failed: {result.error}")
        else:
            print("❌ Web search tool not available (no API key or initialization failed)")
            
    except Exception as e:
        print(f"❌ Web search test error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test Web Reader Tool
    print("=== Testing Z.AI Web Reader Tool ===")
    try:
        reader_tool = ZAIWebReaderTool()
        print(f"Tool available: {reader_tool.available}")
        
        if reader_tool.available:
            print("Executing web reading...")
            result = await reader_tool.execute(
                url="https://httpbin.org/html",
                format="markdown",
                include_images=True
            )
            
            print(f"Reader Success: {result.success}")
            print(f"Content Length: {len(result.content)}")
            
            if result.success:
                print("✅ Web reader tool is working correctly")
            else:
                print(f"❌ Web reader failed: {result.error}")
        else:
            print("❌ Web reader tool not available (no API key or initialization failed)")
            
    except Exception as e:
        print(f"❌ Web reader test error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_zai_tools())