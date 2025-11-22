#!/usr/bin/env python3
"""Test script to check Z.AI tools functionality."""

import asyncio
import os
import sys
import logging

# Add the mini_agent module to the path
sys.path.insert(0, '.')

try:
    from llm.zai_client import ZAIClient
    from tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

async def test_zai_functionality():
    """Test Z.AI tools functionality."""
    print("Testing Z.AI Web Search and Reading Tools")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ ZAI_API_KEY environment variable not set")
        print("   Web search and reading will not work without a valid API key")
        api_key = "dummy-key-for-structure-test"
    else:
        print("✅ ZAI_API_KEY environment variable found")
    
    try:
        # Initialize client and tools
        print("\n1. Initializing Z.AI Client...")
        client = ZAIClient(api_key)
        print("✅ Z.AI Client initialized successfully")
        
        print("\n2. Initializing Web Search Tool...")
        search_tool = ZAIWebSearchTool()
        print(f"   Search tool available: {search_tool.available}")
        
        print("\n3. Initializing Web Reader Tool...")
        reader_tool = ZAIWebReaderTool()
        print(f"   Reader tool available: {reader_tool.available}")
        
        # Check tool parameters
        print("\n4. Checking Tool Parameters...")
        print("   Search Tool Parameters:")
        search_params = search_tool.parameters
        for param, details in search_params['properties'].items():
            required = " (required)" if param in search_params.get('required', []) else ""
            print(f"     - {param}: {details.get('type', 'unknown')}{required}")
        
        print("\n   Reader Tool Parameters:")
        reader_params = reader_tool.parameters
        for param, details in reader_params['properties'].items():
            required = " (required)" if param in reader_params.get('required', []) else ""
            print(f"     - {param}: {details.get('type', 'unknown')}{required}")
        
        # Test method signatures
        print("\n5. Testing Method Signatures...")
        import inspect
        
        search_sig = inspect.signature(search_tool.execute)
        print(f"   Search tool execute signature: {search_sig}")
        
        reader_sig = inspect.signature(reader_tool.execute)
        print(f"   Reader tool execute signature: {reader_sig}")
        
        print("\n✅ All tools initialized successfully!")
        print("\nNote: Actual API calls require valid ZAI_API_KEY")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = asyncio.run(test_zai_functionality())
    sys.exit(0 if result else 1)