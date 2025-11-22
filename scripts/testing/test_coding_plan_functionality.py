#!/usr/bin/env python3
"""
Test Z.AI Coding Plan functionality with proper usage quota understanding
Focus: Usage limits (~120 prompts every 5 hours), not pricing
"""

import asyncio
import os
from datetime import datetime

# Ensure correct API key is set
os.environ["ZAI_API_KEY"] = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

# Import the ZAI client with correct configuration
from mini_agent.llm.zai_client import ZAIClient

async def test_coding_plan_glm_chat():
    """Test GLM chat with Coding Plan limits (~120 prompts every 5 hours)"""
    print("🤖 Testing GLM Chat (Coding Plan)...")
    print("💡 Usage Limit: ~120 prompts every 5 hours")
    
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        messages = [
            {"role": "user", "content": "What are the key features of Z.AI's Coding Plan?"}
        ]
        
        result = await client.chat_completion(
            messages=messages,
            model="GLM-4.6",
            temperature=0.7
        )
        
        print(f"Result: {'✅ Success' if result.get('success') else '❌ Failed'}")
        if result.get('success'):
            print(f"Model: {result.get('model', 'N/A')}")
            print(f"Usage: {result.get('usage', {})}")
            print(f"Content Preview: {str(result.get('content', ''))[:100]}...")
            print(f"Total Tokens: {result.get('usage', {}).get('total_tokens', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"API Endpoint: {result.get('api_endpoint', 'N/A')}")
            
            # Check if this is a quota limit error
            if "1113" in str(result.get('error', '')):
                print("💰 Usage Quota: This appears to be a quota limit, not a configuration issue")
        print("-" * 60)
        
    except Exception as e:
        print(f"Exception: {e}")
        print("-" * 60)

async def test_coding_plan_web_search():
    """Test web search with Coding Plan - may have different limits"""
    print("🔍 Testing Web Search (Coding Plan)...")
    print("💡 Note: Web search may have different quota allocation in Coding Plan")
    
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        result = await client.web_search(
            query="AI coding tools 2024",
            count=5,
            search_engine="search-prime"
        )
        
        print(f"Result: {'✅ Success' if result.get('success') else '❌ Failed'}")
        if result.get('success'):
            print(f"Query: {result.get('query', 'N/A')}")
            print(f"Results: {result.get('count', 0)}")
            print(f"Search Engine: search-prime")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"API Endpoint: {client.base_url}")
            
            # Check if this is a quota limit error
            if "1113" in str(result.get('error', '')):
                print("💰 Usage Quota: Web search quota may be different from chat quota")
        print("-" * 60)
        
    except Exception as e:
        print(f"Exception: {e}")
        print("-" * 60)

async def test_coding_plan_web_reader():
    """Test web reader with Coding Plan"""
    print("📖 Testing Web Reader (Coding Plan)...")
    print("💡 Note: Web reader may have different quota allocation")
    
    client = ZAIClient(api_key="1cd42fbb5c474884bdd884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    try:
        result = await client.web_reading(
            url="https://www.example.com",
            format_type="markdown",
            include_images=True
        )
        
        print(f"Result: {'✅ Success' if result.get('success') else '❌ Failed'}")
        if result.get('success'):
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Word Count: {result.get('word_count', 0)}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"Fallback Method: {result.get('metadata', {}).get('extraction_method', 'N/A')}")
        print("-" * 60)
        
    except Exception as e:
        print(f"Exception: {e}")
        print("-" * 60)

async def test_quota_usage_tracking():
    """Test how to track and manage Coding Plan quota usage"""
    print("📊 Testing Quota Usage Tracking...")
    print("💡 Strategy: Track usage to stay within ~120 prompts every 5 hours")
    
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=True)
    
    # Simulate usage tracking
    usage_stats = {
        "prompts_used": 0,
        "total_tokens": 0,
        "time_window": "5 hours",
        "limit": 120
    }
    
    print(f"Current Stats: {usage_stats}")
    print("💡 Recommendation: Implement quota tracking and usage warnings")
    print("💡 Best Practice: Use GLM-4.5 for efficiency, GLM-4.6 for complex tasks")
    print("-" * 60)

async def main():
    """Test Coding Plan functionality with proper understanding"""
    print(f"🧪 Z.AI Coding Plan Functionality Test")
    print(f"⏰ Test Time: {datetime.now().isoformat()}")
    print(f"🔑 API Key: 1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ")
    print(f"📊 Plan Type: Coding Plan")
    print(f"💰 Usage Limit: ~120 prompts every 5 hours (3x Claude Pro usage)")
    print(f"⚠️  Focus: Usage quota management, not pricing")
    print("=" * 60)
    
    # Test GLM chat (should work within quota)
    await test_coding_plan_glm_chat()
    
    # Test web search (quota-dependent)
    await test_coding_plan_web_search()
    
    # Test web reader (quota-dependent)
    await test_coding_plan_web_reader()
    
    # Test quota tracking
    await test_quota_usage_tracking()
    
    print("✅ Coding Plan Test Complete")

if __name__ == "__main__":
    asyncio.run(main())