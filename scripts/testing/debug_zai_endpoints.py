#!/usr/bin/env python3
"""Debug script for Z.AI endpoint testing."""

import asyncio
import os
import sys
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.llm.minimax_zai_client import MiniMax-M2ZAIWebSearchClient, get_zai_api_key


async def debug_zai_endpoint():
    """Debug the Z.AI endpoint to see what's happening."""
    print("🔧 Debugging Z.AI Endpoint...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    print(f"✅ Client initialized with endpoint: {client.base_url}")
    
    # Test with minimal parameters
    try:
        import aiohttp
        
        payload = {
            "search_engine": "search-prime",
            "search_query": "Python programming",
            "count": 2,
            "search_recency_filter": "noLimit"
        }
        
        print(f"🔍 Testing search with payload: {json.dumps(payload, indent=2)}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{client.base_url}/web_search",
                headers=client.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                
                print(f"📊 Response Status: {response.status}")
                print(f"📊 Response Headers: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"📊 Response Body: {response_text[:500]}...")
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        print(f"✅ JSON parsed successfully")
                        print(f"✅ Result keys: {list(result.keys())}")
                        search_results = result.get("search_result", [])
                        print(f"✅ Search results count: {len(search_results)}")
                        return True
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON decode failed: {e}")
                        return False
                else:
                    print(f"❌ API returned error status: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False


async def test_basic_glm_chat():
    """Test if the basic GLM chat works to verify API key is valid."""
    print("\n🧪 Testing GLM Chat (Coding Plan)...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
    
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    try:
        import aiohttp
        
        payload = {
            "model": "glm-4.6",
            "messages": [
                {"role": "user", "content": "Hello, can you confirm you're working?"}
            ]
        }
        
        print(f"🔍 Testing GLM chat with endpoint: {client.base_url}/chat/completions")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{client.base_url}/chat/completions",
                headers=client.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                
                print(f"📊 Chat Response Status: {response.status}")
                
                response_text = await response.text()
                print(f"📊 Chat Response: {response_text[:300]}...")
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        print(f"✅ GLM chat successful")
                        return True
                    except json.JSONDecodeError:
                        print(f"❌ Chat JSON decode failed")
                        return False
                else:
                    print(f"❌ Chat API error: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Chat test exception: {e}")
        return False


async def test_different_endpoints():
    """Test different possible endpoints for web search."""
    print("\n🔍 Testing Different Endpoints...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
    
    # Try different possible endpoints
    endpoints = [
        "https://api.z.ai/api/coding/paas/v4",  # Current client default
        "https://api.z.ai/api/paas/v4",         # Common API
        "https://api.z.ai/api/anthropic",       # Anthropic endpoint
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        
        try:
            import aiohttp
            
            payload = {
                "search_engine": "search-prime",
                "search_query": "Python",
                "count": 1,
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{endpoint}/web_search",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    
                    print(f"   Status: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        if result.get("search_result"):
                            print(f"   ✅ SUCCESS with {endpoint}")
                            print(f"   Results: {len(result.get('search_result', []))}")
                            return endpoint
                        else:
                            print(f"   ❌ No search results")
                    else:
                        print(f"   ❌ Error: {response.status}")
                        response_text = await response.text()
                        print(f"   Response: {response_text[:100]}...")
                        
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n❌ No working endpoints found")
    return None


if __name__ == "__main__":
    asyncio.run(debug_zai_endpoint())
    asyncio.run(test_basic_glm_chat())
    working_endpoint = asyncio.run(test_different_endpoints())
    
    if working_endpoint:
        print(f"\n🎉 Found working endpoint: {working_endpoint}")
    else:
        print(f"\n⚠️ No working endpoints found - check API key permissions")
