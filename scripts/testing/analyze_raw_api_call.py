#!/usr/bin/env python3
"""
Raw Z.AI API Call and Response Analysis
"""

import asyncio
import sys
import json
from pathlib import Path

# Add mini_agent to path
sys.path.insert(0, '.')

from mini_agent.llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key

async def analyze_raw_api_call():
    print("🔍 Z.AI API Call Analysis")
    print("=" * 60)
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ No API key found")
        return
    
    client = ClaudeZAIWebSearchClient(api_key)
    
    # Show the actual API call structure
    print(f"📡 API Configuration:")
    print(f"   Base URL: {client.base_url}")
    print(f"   Endpoint: {client.base_url}/web_search")
    print(f"   Headers: {json.dumps(client.headers, indent=2)}")
    
    # Show what payload would be sent
    test_payload = {
        "search_engine": "search-prime",
        "search_query": "site:docs.z.ai/devpack/tool/claude",
        "count": 10,
        "search_recency_filter": "noLimit",
    }
    
    print(f"\n📤 Request Payload:")
    print(json.dumps(test_payload, indent=2))
    
    # Make the actual call and show response structure
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{client.base_url}/web_search",
                headers=client.headers,
                json=test_payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                
                print(f"\n📥 Raw Response Status: {response.status}")
                print(f"📥 Response Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"\n📥 Raw Response JSON Structure:")
                    print(json.dumps(result, indent=2))
                    
                    # Extract just the search results
                    search_results = result.get("search_result", [])
                    print(f"\n🔍 Search Results Extracted: {len(search_results)} items")
                    
                    for i, item in enumerate(search_results, 1):
                        print(f"\n--- Raw Result {i} ---")
                        print(json.dumps(item, indent=2))
                        print(f"--- End Raw Result {i} ---")
                else:
                    error_text = await response.text()
                    print(f"\n❌ Error Response: {error_text}")
                    
    except Exception as e:
        print(f"❌ API Call Failed: {e}")

if __name__ == "__main__":
    import aiohttp
    asyncio.run(analyze_raw_api_call())