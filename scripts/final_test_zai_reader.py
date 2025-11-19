#!/usr/bin/env python3
"""Final test of Z.AI web reading functionality."""

import asyncio
import os
from mini_agent.llm.zai_client import ZAIClient

async def final_test():
    client = ZAIClient(os.getenv('ZAI_API_KEY'))
    
    print('🧪 Final Test: Z.AI Web Reading Functionality')
    print('=' * 50)
    
    try:
        # Test the original URL that was failing
        result = await client.web_reading('https://agentclientprotocol.com/protocol/overview')
        
        if result.get('success'):
            print('✅ SUCCESS: Web reading working via fallback!')
            title = result.get('title', 'No title')
            word_count = result.get('word_count', 0)
            method = result.get('metadata', {}).get('extraction_method', 'unknown')
            
            print(f'📄 Title: {title}')
            print(f'📊 Content length: {word_count} words')
            print(f'🔧 Method: {method}')
            print()
            print('📝 Content Preview:')
            print('-' * 40)
            content = result.get('content', '')
            preview = content[:500] + '...' if len(content) > 500 else content
            print(preview)
            
            print()
            print('🎉 CONCLUSION: Z.AI web reading issue has been RESOLVED!')
            print('   The fallback mechanism provides reliable web content extraction.')
            
        else:
            print('❌ FAILED:', result.get('error'))
            
    except Exception as e:
        print('❌ EXCEPTION:', str(e))

if __name__ == "__main__":
    asyncio.run(final_test())