#!/usr/bin/env python3
"""Test Z.AI with Anthropic base URL for web search."""

import asyncio
import aiohttp
import os

async def test_zai_anthropic():
    """Test Z.AI with Anthropic base URL."""
    print("🔍 Testing Z.AI with Anthropic base URL...")
    
    # Get API key
    api_key = os.getenv('ZAI_API_KEY')
    print(f"API Key available: {bool(api_key)}")
    
    if not api_key:
        print("❌ No Z.AI API key found")
        return
        
    # Use Anthropic base URL
    base_url = "https://api.z.ai/api/anthropic"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-API-Key": api_key,  # Anthropic requires this header
        "anthropic-version": "2023-06-01",  # Required for web search
    }
    
    # Test web search via Anthropic endpoint
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "web_search_tool",
                        "web_search": {
                            "query": "VSIX extension package.json not found inside zip error cause solution"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"📡 Making request to: {base_url}")
            print(f"📡 Payload: {payload}")
            
            async with session.post(
                f"{base_url}/messages",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                
                response_text = await response.text()
                print(f"📊 Response Status: {response.status}")
                print(f"📊 Response Headers: {dict(response.headers)}")
                print(f"📊 Response Text: {response_text}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Web search via Anthropic working!")
                    print(f"Content length: {len(str(result))}")
                    
                    # Check if web search results are included
                    content = result.get('content', [])
                    for block in content:
                        if block.get('type') == 'web_search_results':
                            print(f"✅ Found web search results!")
                            results = block.get('results', [])
                            print(f"Results count: {len(results)}")
                            
                            # Print first result preview
                            if results:
                                first_result = results[0]
                                print(f"First result title: {first_result.get('title', 'N/A')}")
                                print(f"First result source: {first_result.get('url', 'N/A')}")
                            break
                else:
                    print(f"❌ Web search failed: {response.status}")
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zai_anthropic())