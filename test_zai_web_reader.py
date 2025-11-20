#!/usr/bin/env python3
"""Test script to verify Z.AI web reader functionality and identify the error."""

import asyncio
import sys
import os

# Add the mini_agent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mini_agent'))

async def test_zai_reader():
    """Test Z.AI web reader to identify the error."""
    print("🔍 Testing Z.AI Web Reader...")
    
    try:
        # Import the tool directly
        from tools.zai_tools import ZAIWebReaderTool
        
        # Initialize tool
        tool = ZAIWebReaderTool()
        print(f"Tool available: {tool.available}")
        
        if not tool.available:
            print("❌ Tool not available - ZAI_API_KEY missing or client initialization failed")
            return
            
        # Test with the problematic URL
        test_url = "https://stackoverflow.com/questions/60598883/error-extension-package-json-not-found-inside-zip-when-repackaging-and-insta"
        print(f"Testing URL: {test_url}")
        
        result = await tool.execute(url=test_url)
        
        print("✅ Z.AI Web Reader Test Result:")
        print(f"Success: {result.success}")
        print(f"Content length: {len(result.content) if result.success else 0}")
        
        if result.success:
            print("✅ Web reader working correctly")
        else:
            print(f"❌ Error: {result.error}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zai_reader())