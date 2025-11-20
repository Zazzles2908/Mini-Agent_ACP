#!/usr/bin/env python3
"""Direct test of Z.AI web reader functionality."""

import asyncio
import os
import sys
import logging

# Set up logging to see the actual errors
logging.basicConfig(level=logging.DEBUG)

async def test_zai_direct():
    """Test Z.AI client directly to identify the error."""
    print("🔍 Testing Z.AI Web Reader directly...")
    
    # Import the Z.AI client
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mini_agent'))
    
    from llm.zai_client import ZAIClient, get_zai_api_key
    
    # Get API key
    api_key = get_zai_api_key()
    print(f"API Key available: {bool(api_key)}")
    
    if not api_key:
        print("❌ No Z.AI API key found in environment")
        return
        
    # Initialize client
    client = ZAIClient(api_key=api_key, use_coding_plan=True)
    print(f"Client initialized with base URL: {client.base_url}")
    
    # Test web reading
    test_url = "https://stackoverflow.com/questions/60598883/error-extension-package-json-not-found-inside-zip-when-repackaging-and-insta"
    print(f"Testing URL: {test_url}")
    
    try:
        result = await client.web_reading(
            url=test_url,
            format_type="text",
            include_images=False
        )
        
        print("\n📊 Test Result:")
        print(f"Success: {result.get('success', False)}")
        
        if result.get('success'):
            print("✅ Z.AI Web Reader working correctly")
            print(f"Content preview: {result.get('content', '')[:200]}...")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            # If it failed, test the alternative approach
            print("\n🔄 Testing web search fallback...")
            search_result = await client.web_search(
                query="VSIX extension package.json not found error cause solution",
                count=5
            )
            print(f"Search success: {search_result.get('success', False)}")
            
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zai_direct())