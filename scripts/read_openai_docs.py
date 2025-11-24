import aiohttp
import asyncio
import os
import sys
sys.path.insert(0, '.')

async def read_openai_docs():
    url = 'https://docs.z.ai/guides/develop/openai/python'
    
    headers = {
        'Authorization': f"Bearer {os.getenv('ZAI_API_KEY')}",
        'Content-Type': 'application/json'
    }
    
    payload = {
        'url': url,
        'format_type': 'text'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://api.z.ai/api/coding/paas/v4/reader',
            headers=headers,
            json=payload
        ) as response:
            result = await response.json()
            if 'content' in result:
                print(result['content'][:3000])
            else:
                print('Full result:', result)

asyncio.run(read_openai_docs())
