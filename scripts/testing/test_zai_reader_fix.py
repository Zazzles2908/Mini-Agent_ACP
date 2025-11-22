#!/usr/bin/env python3
"""Test script to verify Z.AI web reader fix for "Unknown Model" error."""

import asyncio
import sys
import os

# Add the mini_agent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mini_agent'))

# Import directly from the modules
from llm.zai_client import ZAIClient, get_zai_api_key

async def test_zai_web_reader_fix():
    """Test the fixed Z.AI web reader without model parameter."""
    
    # Get API key
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ ERROR: ZAI_API_KEY environment variable not found")
        return False
    
    print("✅ ZAI_API_KEY found")
    
    # Initialize client
    try:
        client = ZAIClient(api_key)
        print("✅ Z.AI client initialized successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize Z.AI client: {e}")
        return False
    
    # Test URL
    test_url = "https://agentclientprotocol.com/"
    
    print(f"\n🔍 Testing web reader with URL: {test_url}")
    print("📝 Testing without model parameter...")
    
    try:
        # Call web reading without model parameter
        result = await client.web_reading(
            url=test_url,
            format_type="markdown",
            include_images=True
        )
        
        if result.get("success"):
            print("✅ SUCCESS: Web reader fixed!")
            print(f"📄 Title: {result.get('title', 'N/A')}")
            print(f"📊 Content length: {result.get('word_count', 0)} words")
            print(f"⏰ Timestamp: {result.get('timestamp', 'N/A')}")
            
            # Show content preview
            content = result.get('content', '')
            if content:
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"\n📋 Content preview:\n{preview}")
            
            return True
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"❌ ERROR: Web reader failed - {error_msg}")
            
            # Check if it's still the model error
            if "Unknown Model" in error_msg:
                print("🔍 Issue: Still getting 'Unknown Model' error")
                print("💡 Suggestion: Check if /reader endpoint actually requires a model parameter")
            
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Exception during web reader test: {e}")
        return False

async def main():
    """Main test function."""
    print("🧪 Testing Z.AI Web Reader Fix")
    print("=" * 50)
    
    success = await test_zai_web_reader_fix()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Z.AI web reader is working correctly.")
    else:
        print("❌ Tests failed. Further investigation needed.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())