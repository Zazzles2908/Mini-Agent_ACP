#!/usr/bin/env python3
"""Test Z.AI client directly - minimal test."""

import asyncio
import aiohttp
import json
import os

async def test_zai_simple():
    """Simple direct test of Z.AI API."""
    print("🔍 Testing Z.AI API directly...")
    
    # Get API key
    api_key = os.getenv('ZAI_API_KEY')
    print(f"API Key available: {bool(api_key)}")
    
    if not api_key:
        print("❌ No Z.AI API key found")
        return
        
    # Test the web search endpoint directly
    base_url = "https://api.z.ai/api/coding/paas/v4"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
    }
    
    # Test web search
    payload = {
        "search_engine": "search-prime",
        "search_query": "VSIX extension package.json not found error cause solution",
        "count": 5,
        "search_recency_filter": "noLimit"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"📡 Making request to: {base_url}/web_search")
            
            async with session.post(
                f"{base_url}/web_search",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                response_text = await response.text()
                print(f"📊 Response Status: {response.status}")
                print(f"📊 Response Headers: {dict(response.headers)}")
                print(f"📊 Response Text: {response_text}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Web search working!")
                    print(f"Results count: {len(result.get('search_result', []))}")
                else:
                    print(f"❌ Web search failed: {response.status}")
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    # Test web reader separately
    print("\n🔍 Testing Z.AI Web Reader...")
    
    reader_payload = {
        "url": "https://stackoverflow.com/questions/60598883/error-extension-package-json-not-found-inside-zip-when-repackaging-and-insta",
        "return_format": "text",
        "retain_images": False
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"📡 Making request to: {base_url}/reader")
            
            async with session.post(
                f"{base_url}/reader",
                headers=headers,
                json=reader_payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                response_text = await response.text()
                print(f"📊 Reader Response Status: {response.status}")
                print(f"📊 Reader Response Text: {response_text}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Web reader working!")
                    print(f"Content length: {len(result.get('content', ''))}")
                else:
                    print(f"❌ Web reader failed: {response.status}")
                    try:
                        error_data = json.loads(response_text)
                        print(f"❌ Error details: {error_data}")
                    except:
                        print(f"❌ Could not parse error response")
                        
    except Exception as e:
        print(f"❌ Reader Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zai_simple())