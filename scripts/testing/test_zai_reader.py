#!/usr/bin/env python3
"""Test Z.AI reader endpoint functionality."""

import asyncio
import aiohttp
import os
from mini_agent.llm.zai_client import ZAIClient

async def test_zai_reader():
    """Test Z.AI reader with different models."""
    api_key = os.getenv('ZAI_API_KEY')
    client = ZAIClient(api_key)
    
    print("Testing Z.AI reader endpoint functionality...")
    
    # First test which models work for chat
    working_chat_models = []
    test_models = ['glm-4.6', 'glm-4.5', 'glm-4-air']
    
    for model in test_models:
        try:
            chat_payload = {
                'model': model,
                'messages': [{'role': 'user', 'content': 'Hi'}],
                'stream': False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{client.base_url}/chat/completions',
                    headers=client.headers,
                    json=chat_payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        working_chat_models.append(model)
                        print(f'✅ Chat works with: {model}')
                    else:
                        print(f'❌ Chat fails with {model}: {response.status}')
                        
        except Exception as e:
            print(f'❌ Chat exception with {model}: {str(e)}')
    
    print(f'\nWorking chat models: {working_chat_models}')
    
    # Now test reader with working models
    for model in working_chat_models:
        try:
            print(f'\nTesting reader with model: {model}')
            reader_payload = {
                'model': model,
                'url': 'https://agentclientprotocol.com/protocol/overview',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{client.base_url}/reader',
                    headers=client.headers,
                    json=reader_payload,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as response:
                    if response.status == 200:
                        print(f'✅ SUCCESS: Reader works with {model}')
                        result = await response.json()
                        content = result.get('content', '')
                        title = result.get('title', 'No title')
                        print(f'Title: {title}')
                        print(f'Content length: {len(content)}')
                        print(f'First 200 chars: {content[:200]}...')
                        return True
                    else:
                        error_text = await response.text()
                        print(f'❌ Reader fails with {model}: {error_text[:100]}')
                        
        except Exception as e:
            print(f'❌ Reader exception with {model}: {str(e)}')
    
    print('\n❌ No working model found for reader endpoint')
    
    # Try without model parameter
    try:
        print('\nTrying reader without model parameter...')
        reader_payload = {
            'url': 'https://agentclientprotocol.com/protocol/overview',
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{client.base_url}/reader',
                headers=client.headers,
                json=reader_payload,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                if response.status == 200:
                    print('✅ SUCCESS: Reader works without model parameter')
                    result = await response.json()
                    print(f'Result keys: {list(result.keys())}')
                    return True
                else:
                    error_text = await response.text()
                    print(f'❌ Reader fails without model: {error_text[:100]}')
                    
    except Exception as e:
        print(f'❌ Reader exception without model: {str(e)}')
    
    return False

if __name__ == "__main__":
    asyncio.run(test_zai_reader())