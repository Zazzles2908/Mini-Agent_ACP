#!/usr/bin/env python3
"""Test corrected Z.AI implementation with proper API usage."""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool

async def test_corrected_implementation():
    """Test the corrected Z.AI implementation."""
    
    print("=" * 80)
    print("CORRECTED Z.AI IMPLEMENTATION TEST")
    print("=" * 80)
    
    # Check environment
    print(f"ZAI_API_KEY present: {'Yes' if os.getenv('ZAI_API_KEY') else 'No'}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Test Web Search Tool with corrected model
    print("=== Testing Z.AI Web Search Tool (GLM-4.5) ===")
    try:
        search_tool = ZAIWebSearchTool()
        print(f"Tool available: {search_tool.available}")
        
        if search_tool.available:
            print("Executing web search with GLM-4.5...")
            result = await search_tool.execute(
                query="Z.AI API correct implementation best practices",
                depth="comprehensive",
                model="glm-4.5"
            )
            
            print(f"Search Success: {result.success}")
            print(f"Content Length: {len(result.content)}")
            
            if result.success:
                print("✅ Web search tool is working correctly with GLM-4.5")
                # Check if model description is improved
                if "GLM-4.5" in result.content:
                    print("✅ Model description correctly shows GLM-4.5")
            else:
                print(f"❌ Web search failed: {result.error}")
        else:
            print("❌ Web search tool not available")
            
    except Exception as e:
        print(f"❌ Web search test error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test Web Reader Tool with corrected implementation
    print("=== Testing Z.AI Web Reader Tool (/reader endpoint) ===")
    try:
        reader_tool = ZAIWebReaderTool()
        print(f"Tool available: {reader_tool.available}")
        
        if reader_tool.available:
            print("Executing web reading with correct /reader endpoint...")
            result = await reader_tool.execute(
                url="https://httpbin.org/json",
                format="markdown",
                include_images=True
            )
            
            print(f"Reader Success: {result.success}")
            print(f"Content Length: {len(result.content)}")
            
            if result.success:
                print("✅ Web reader tool is working correctly with /reader endpoint")
            else:
                print(f"❌ Web reader failed: {result.error}")
                # Note: May fall back to search if direct reader fails
                if "search fallback" in result.get("metadata", {}).get("extraction_method", ""):
                    print("ℹ️  Using search fallback (acceptable if /reader endpoint unavailable)")
        else:
            print("❌ Web reader tool not available")
            
    except Exception as e:
        print(f"❌ Web reader test error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("CORRECTED IMPLEMENTATION TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_corrected_implementation())