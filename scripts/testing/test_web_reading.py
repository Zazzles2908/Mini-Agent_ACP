#!/usr/bin/env python3
"""Test Z.AI web reading with fallback."""

import asyncio
import os
from mini_agent.llm.zai_client import ZAIClient

async def test_web_reading():
    """Test Z.AI web reading functionality."""
    print("🧪 Testing Z.AI Web Reading...")
    
    client = ZAIClient(os.getenv('ZAI_API_KEY'))
    
    try:
        # Test web reading with fallback
        result = await client.web_reading('https://agentclientprotocol.com/protocol/overview')
        
        if result.get('success'):
            print("✅ Z.AI web reading working!")
            print(f"Title: {result.get('title', 'No title')}")
            print(f"Content length: {result.get('word_count', 0)} words")
            print(f"Method: {result.get('metadata', {}).get('extraction_method', 'unknown')}")
            print(f"Content preview: {result.get('content', '')[:200]}...")
            return True
        else:
            print(f"❌ Z.AI web reading failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Z.AI exception: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_web_reading())