import aiohttp
import asyncio
import os
import sys
sys.path.insert(0, '.')

async def search():
    from mini_agent.llm.zai_client import ZAIClient
    
    api_key = os.getenv('ZAI_API_KEY')
    client = ZAIClient(api_key)
    
    # Search for Claude Code Z.AI configuration
    result = await client.web_search('z.ai Claude Code ANTHROPIC_BASE_URL web search MCP integration', count=5)
    
    if result.get('success'):
        print('=== Search Results ===')
        for item in result.get('search_result', []):
            title = item.get('title', '')
            link = item.get('link', '')
            content = item.get('content', '')
            print(f"Title: {title}")
            print(f"URL: {link}")
            print(f"Content: {content[:300]}...")
            print('---')
    else:
        print('Error:', result)

asyncio.run(search())
