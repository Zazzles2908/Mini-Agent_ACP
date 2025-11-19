#!/usr/bin/env python3
"""
Test Z.AI Coding Plan API functionality
Tests web search, web reading, and chat completion capabilities
"""

import asyncio
import os
import json
from datetime import datetime

# Set API key environment variable for testing
os.environ["ZAI_API_KEY"] = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

# Import the ZAI client
from mini_agent.llm.zai_client import ZAIClient

async def test_web_search():
    """Test web search functionality"""
    print("🔍 Testing Web Search...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        result = await client.web_search(
            query="latest AI developments 2024",
            count=3,
            search_engine="search_std"
        )
        
        print(f"Web Search Result:")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Results Count: {result.get('count', 0)}")
            print(f"API Endpoint: {client.base_url}")
            print(f"First Result Title: {result.get('search_result', [{}])[0].get('title', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Web Search Exception: {e}")
        print("-" * 80)

async def test_web_reading():
    """Test web reading functionality"""
    print("📖 Testing Web Reading...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        result = await client.web_reading(
            url="https://www.example.com",
            format_type="markdown",
            include_images=True
        )
        
        print(f"Web Reading Result:")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Word Count: {result.get('word_count', 0)}")
            print(f"API Endpoint: {client.base_url}")
            print(f"Content Preview: {str(result.get('content', ''))[:200]}...")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Web Reading Exception: {e}")
        print("-" * 80)

async def test_chat_completion():
    """Test GLM chat completion"""
    print("🤖 Testing GLM Chat Completion...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        messages = [
            {"role": "user", "content": "What are the benefits of using Z.AI's GLM models?"}
        ]
        
        result = await client.chat_completion(
            messages=messages,
            model="GLM-4.6",
            temperature=0.7
        )
        
        print(f"Chat Completion Result:")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Model Used: {result.get('model', 'N/A')}")
            print(f"API Endpoint: {result.get('api_endpoint', 'N/A')}")
            print(f"Usage: {result.get('usage', {})}")
            print(f"Content Preview: {str(result.get('content', ''))[:200]}...")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"API Endpoint: {result.get('api_endpoint', 'N/A')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Chat Completion Exception: {e}")
        print("-" * 80)

async def test_common_api_endpoints():
    """Test with Common API instead of Coding Plan API"""
    print("🔄 Testing Common API (for comparison)...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=False)
    
    try:
        # Test web search with Common API
        result = await client.web_search(
            query="AI developments",
            count=2,
            search_engine="search_std"
        )
        
        print(f"Common API Web Search:")
        print(f"Success: {result.get('success', False)}")
        print(f"API Endpoint: {client.base_url}")
        if result.get('success'):
            print(f"Results: {result.get('count', 0)}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Common API Exception: {e}")
        print("-" * 80)

async def main():
    """Run all tests"""
    print(f"🧪 Z.AI Coding Plan API Test Suite")
    print(f"⏰ Test Time: {datetime.now().isoformat()}")
    print(f"🔑 API Key: 1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ")
    print("=" * 80)
    
    # Test GLM Chat (should work with Coding Plan)
    await test_chat_completion()
    
    # Test Web Search with Coding Plan (might fail)
    await test_web_search()
    
    # Test Web Reading with Coding Plan (might fail)
    await test_web_reading()
    
    # Test Common API for comparison
    await test_common_api_endpoints()
    
    print("✅ Test Suite Complete")

if __name__ == "__main__":
    asyncio.run(main())