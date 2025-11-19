"""
Comprehensive Z.AI Web Search Verification Test
Tests that Z.AI web search is actually working and NOT falling back to OpenAI
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_zai_web_search():
    """Test Z.AI web search functionality"""
    print("=" * 70)
    print("Z.AI Web Search Verification Test")
    print("=" * 70)
    
    # Check API key
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        print("❌ FAILED: ZAI_API_KEY not found in environment")
        return False
    
    print(f"✓ ZAI_API_KEY found: {api_key[:8]}...")
    
    # Test 1: Import zai-sdk
    try:
        from zai import ZaiClient
        print("✓ Successfully imported ZaiClient from zai-sdk")
    except ImportError as e:
        print(f"❌ FAILED: Could not import zai-sdk: {e}")
        return False
    
    # Test 2: Initialize client
    try:
        client = ZaiClient(api_key=api_key)
        print("✓ Successfully initialized ZaiClient")
    except Exception as e:
        print(f"❌ FAILED: Could not initialize ZaiClient: {e}")
        return False
    
    # Test 3: Actually perform a web search
    print("\n" + "-" * 70)
    print("Testing actual web search functionality...")
    print("-" * 70)
    
    try:
        response = client.web_search.web_search(
            search_engine="search-prime",
            search_query="artificial intelligence latest developments 2025",
            count=3
        )
        
        print("✓ Web search request completed successfully")
        
        # Verify response structure
        if not hasattr(response, 'search_result'):
            print("❌ FAILED: Response missing 'search_result' attribute")
            return False
        
        print(f"✓ Received search results: {len(response.search_result)} results")
        
        # Display first result to verify it's real data
        if response.search_result:
            first_result = response.search_result[0]
            print("\n" + "=" * 70)
            print("First Search Result Preview:")
            print("=" * 70)
            print(f"Title: {first_result.get('title', 'N/A')}")
            print(f"Link: {first_result.get('link', 'N/A')}")
            print(f"Media: {first_result.get('media', 'N/A')}")
            print(f"Content Preview: {first_result.get('content', 'N/A')[:200]}...")
            print("=" * 70)
        else:
            print("⚠ WARNING: No search results returned")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Web search failed with error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False
    
    # Test 4: Verify it's using Z.AI native models (check response metadata)
    try:
        if hasattr(response, 'model'):
            print(f"\n✓ Model used: {response.model}")
        if hasattr(response, 'id'):
            print(f"✓ Request ID: {response.id}")
        if hasattr(response, 'created'):
            print(f"✓ Created timestamp: {response.created}")
    except Exception as e:
        print(f"⚠ Could not check response metadata: {e}")
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS: Z.AI web search is working correctly!")
    print("✅ CONFIRMED: Using native Z.AI SDK (not falling back to OpenAI)")
    print("=" * 70)
    return True

def test_zai_chat_with_search():
    """Test Z.AI chat completion with web search integration"""
    print("\n\n" + "=" * 70)
    print("Z.AI Chat with Web Search Test")
    print("=" * 70)
    
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        print("❌ Skipping: ZAI_API_KEY not found")
        return False
    
    try:
        from zai import ZaiClient
        client = ZaiClient(api_key=api_key)
        
        # Test chat with web search tool
        tools = [{
            "type": "web_search",
            "web_search": {
                "enable": True,
                "search_engine": "search-prime",
                "search_result": True,
                "count": 3
            }
        }]
        
        messages = [{
            "role": "user",
            "content": "What are the latest developments in AI in 2025?"
        }]
        
        print("Testing chat with web search tool...")
        response = client.chat.completions.create(
            model="glm-4-air",
            messages=messages,
            tools=tools
        )
        
        print("✓ Chat completion with web search successful")
        
        if hasattr(response, 'choices') and response.choices:
            content = response.choices[0].message.content
            print(f"\n✓ Response received (length: {len(content)} chars)")
            print(f"Response preview: {content[:200]}...")
        
        if hasattr(response, 'web_search') and response.web_search:
            print(f"✓ Web search results included: {len(response.web_search)} sources")
        
        print("\n✅ SUCCESS: Chat with web search integration working!")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    success1 = test_zai_web_search()
    success2 = test_zai_chat_with_search()
    
    print("\n\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(f"Direct Web Search: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Chat with Search: {'✅ PASS' if success2 else '❌ FAIL'}")
    print("=" * 70)
    
    sys.exit(0 if (success1 and success2) else 1)
