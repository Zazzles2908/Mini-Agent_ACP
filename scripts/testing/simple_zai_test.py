#!/usr/bin/env python3
"""Simple sanity check for Z.AI web search."""

import asyncio
import os
from mini_agent.llm.zai_client import ZAIClient

async def simple_test():
    """Test basic Z.AI functionality."""
    print("🧪 Testing Z.AI Web Search...")
    
    client = ZAIClient(os.getenv('ZAI_API_KEY'))
    
    try:
        # Simple test
        result = await client.web_search_with_chat(
            "Hello, test Z.AI connection", 
            model_name='glm-4.6'
        )
        
        if result.get('success'):
            print("✅ Z.AI web search working!")
            print(f"Response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Z.AI web search failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Z.AI exception: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(simple_test())