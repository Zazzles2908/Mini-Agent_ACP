#!/usr/bin/env python3
"""Test Z.AI reader with correct model names from API."""

import asyncio
import aiohttp
import os
from mini_agent.llm.zai_client import ZAIClient

async def test_with_correct_models():
    """Test Z.AI reader with the correct model names from /models endpoint."""
    api_key = os.getenv('ZAI_API_KEY')
    client = ZAIClient(api_key)
    
    print("=== Testing Z.AI Reader with Correct Model Names ===\n")
    
    # First get the correct model names
    correct_models = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{client.base_url}/models',
                headers=client.headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    models_data = await response.json()
                    for model in models_data.get('data', []):
                        correct_models.append(model['id'])
                    print(f"Available models from API: {correct_models}")
                else:
                    print(f"Failed to get models: {response.status}")
                    return
                    
    except Exception as e:
        print(f"Exception getting models: {e}")
        return
    
    print("\nTesting reader with each correct model...")
    
    # Test each correct model
    for model in correct_models:
        print(f"\n🧪 Testing reader with model: {model}")
        
        # Test 1: Basic reader call
        try:
            payload = {
                'model': model,
                'url': 'https://agentclientprotocol.com/protocol/overview'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{client.base_url}/reader',
                    headers=client.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ SUCCESS with {model}!")
                        print(f"   Title: {result.get('title', 'No title')}")
                        print(f"   Content length: {len(result.get('content', ''))}")
                        print(f"   First 200 chars: {result.get('content', '')[:200]}...")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ {model} failed: {error_text[:100]}")
                        
        except Exception as e:
            print(f"❌ {model} exception: {str(e)}")
    
    print("\n❌ No model worked. Trying alternative approaches...")
    
    # Try without model parameter one more time
    try:
        print("\n🧪 Testing reader without model parameter...")
        payload = {
            'url': 'https://agentclientprotocol.com/protocol/overview'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{client.base_url}/reader',
                headers=client.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ SUCCESS without model parameter!")
                    print(f"   Title: {result.get('title', 'No title')}")
                    print(f"   Content length: {len(result.get('content', ''))}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed without model: {error_text}")
                    
    except Exception as e:
        print(f"❌ Exception without model: {str(e)}")
    
    print("\n❌ All tests failed. Reader endpoint may not be available.")
    return False

if __name__ == "__main__":
    asyncio.run(test_with_correct_models())