#!/usr/bin/env python3
"""Detailed investigation of Z.AI reader endpoint."""

import asyncio
import aiohttp
import os
import json
from mini_agent.llm.zai_client import ZAIClient

async def investigate_reader_api():
    """Deep investigation of Z.AI reader API."""
    api_key = os.getenv('ZAI_API_KEY')
    client = ZAIClient(api_key)
    
    print("=== Z.AI Reader API Investigation ===\n")
    
    # Test 1: Verify API key and endpoint accessibility
    print("1. Testing API key and endpoint accessibility...")
    try:
        async with aiohttp.ClientSession() as session:
            # Test chat endpoint first
            chat_payload = {
                'model': 'glm-4.6',
                'messages': [{'role': 'user', 'content': 'test'}],
                'stream': False
            }
            
            async with session.post(
                f'{client.base_url}/chat/completions',
                headers=client.headers,
                json=chat_payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                print(f"Chat endpoint status: {response.status}")
                if response.status == 200:
                    print("✅ Chat endpoint working")
                else:
                    print(f"❌ Chat endpoint failed: {await response.text()}")
                    
    except Exception as e:
        print(f"❌ Chat endpoint exception: {e}")
    
    # Test 2: Try different reader endpoint approaches
    print("\n2. Testing different reader endpoint approaches...")
    
    # Try GET request instead of POST
    try:
        print("  Testing GET request...")
        async with aiohttp.ClientSession() as session:
            params = {'url': 'https://agentclientprotocol.com/protocol/overview'}
            async with session.get(
                f'{client.base_url}/reader',
                headers=client.headers,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                print(f"    GET status: {response.status}")
                if response.status != 400:
                    result = await response.text()
                    print(f"    GET result: {result[:200]}...")
                    
    except Exception as e:
        print(f"    GET exception: {e}")
    
    # Test 3: Try with different payload structures
    print("\n3. Testing different payload structures...")
    
    payload_variations = [
        # Basic structure
        {
            'model': 'glm-4.6',
            'url': 'https://agentclientprotocol.com/protocol/overview'
        },
        # With additional parameters
        {
            'model': 'glm-4.6',
            'url': 'https://agentclientprotocol.com/protocol/overview',
            'format': 'markdown',
            'timeout': 30
        },
        # Alternative structure
        {
            'target_url': 'https://agentclientprotocol.com/protocol/overview',
            'model': 'glm-4.6'
        },
        # Minimal structure
        {
            'url': 'https://agentclientprotocol.com/protocol/overview'
        }
    ]
    
    for i, payload in enumerate(payload_variations, 1):
        try:
            print(f"  Testing payload variation {i}: {json.dumps(payload, indent=2)}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{client.base_url}/reader',
                    headers=client.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        print(f"    ✅ SUCCESS with payload {i}")
                        result = await response.json()
                        print(f"    Response keys: {list(result.keys())}")
                        break
                    else:
                        error_text = await response.text()
                        print(f"    ❌ Payload {i} failed: {error_text[:100]}")
                        
        except Exception as e:
            print(f"    ❌ Payload {i} exception: {str(e)}")
    
    # Test 4: Check if reader endpoint exists at all
    print("\n4. Checking available endpoints...")
    try:
        async with aiohttp.ClientSession() as session:
            # Try to get API documentation or info
            async with session.get(
                f'{client.base_url}/models',
                headers=client.headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                print(f"    /models endpoint status: {response.status}")
                if response.status == 200:
                    models_result = await response.json()
                    print(f"    Available models: {json.dumps(models_result, indent=2)}")
                    
    except Exception as e:
        print(f"    /models endpoint exception: {e}")
    
    # Test 5: Try different base URLs
    print("\n5. Testing different base URLs...")
    alternative_urls = [
        "https://api.z.ai/api/paas/v4",
        "https://api.z-ai.com/api/paas/v4", 
        "https://z-ai.com/api/paas/v4",
        "https://api.z.ai/v1"
    ]
    
    for alt_url in alternative_urls:
        try:
            print(f"  Testing {alt_url}/reader...")
            async with aiohttp.ClientSession() as session:
                payload = {
                    'url': 'https://agentclientprotocol.com/protocol/overview'
                }
                
                async with session.post(
                    f'{alt_url}/reader',
                    headers=client.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    print(f"    {alt_url}/reader status: {response.status}")
                    if response.status != 400:
                        result = await response.text()
                        print(f"    {alt_url}/reader result: {result[:100]}...")
                        
        except Exception as e:
            print(f"    {alt_url}/reader exception: {e}")

if __name__ == "__main__":
    asyncio.run(investigate_reader_api())