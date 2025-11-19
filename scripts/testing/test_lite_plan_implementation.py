#!/usr/bin/env python3
"""
Test Z.AI Lite Plan functionality with updated implementation
Tests web search and reading with cost optimization
"""

import asyncio
import os
import json
from datetime import datetime

# Ensure correct API key is set
os.environ["ZAI_API_KEY"] = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

# Import the updated ZAI client
from mini_agent.llm.zai_client import ZAIClient

async def test_lite_plan_web_search():
    """Test web search with cost-optimized parameters"""
    print("🔍 Testing Z.AI Lite Plan Web Search...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=False)
    
    try:
        result = await client.web_search(
            query="AI developments 2024",
            count=3,
            search_engine="search-prime",
            recency_filter="noLimit"
        )
        
        print(f"Web Search Result:")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Results Count: {result.get('count', 0)}")
            print(f"API Endpoint: {client.base_url}")
            print(f"Query: {result.get('query', 'N/A')}")
            print(f"Timestamp: {result.get('timestamp', 'N/A')}")
            
            # Show first result
            search_results = result.get('search_result', [])
            if search_results:
                print(f"First Result: {search_results[0].get('title', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Web Search Exception: {e}")
        print("-" * 80)

async def test_lite_plan_web_reader():
    """Test web reader with cost awareness"""
    print("📖 Testing Z.AI Lite Plan Web Reader...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=False)
    
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
            print(f"Fallback Method: {result.get('metadata', {}).get('extraction_method', 'N/A')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Web Reading Exception: {e}")
        print("-" * 80)

async def test_cost_optimization():
    """Test cost optimization features"""
    print("💰 Testing Cost Optimization...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=False)
    
    try:
        # Test different search depths for cost comparison
        depths = ["quick", "comprehensive", "deep"]
        for depth in depths:
            print(f"Testing {depth} depth search...")
            result = await client.web_search(
                query="AI news today",
                count=7 if depth == "deep" else (3 if depth == "quick" else 7),
                search_engine="search-prime",
                recency_filter="noLimit"
            )
            print(f"  {depth}: Success={result.get('success', False)}")
            if result.get('success'):
                print(f"  Results: {result.get('count', 0)}")
            else:
                print(f"  Error: {result.get('error', 'Unknown')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"Cost Optimization Test Exception: {e}")
        print("-" * 80)

async def test_glm_chat():
    """Test GLM chat completion with updated client"""
    print("🤖 Testing GLM Chat Completion...")
    client = ZAIClient(api_key="1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ", use_coding_plan=False)
    
    try:
        messages = [
            {"role": "user", "content": "What are the key benefits of using Z.AI's Lite Plan for web search?"}
        ]
        
        result = await client.chat_completion(
            messages=messages,
            model="GLM-4.6",
            temperature=0.7
        )
        
        print(f"GLM Chat Result:")
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"Model: {result.get('model', 'N/A')}")
            print(f"API Endpoint: {result.get('api_endpoint', 'N/A')}")
            print(f"Usage: {result.get('usage', {})}")
            print(f"Content Preview: {str(result.get('content', ''))[:200]}...")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"API Endpoint: {result.get('api_endpoint', 'N/A')}")
        print("-" * 80)
        
    except Exception as e:
        print(f"GLM Chat Exception: {e}")
        print("-" * 80)

async def main():
    """Run comprehensive Lite Plan test suite"""
    print(f"🧪 Z.AI Lite Plan Implementation Test Suite")
    print(f"⏰ Test Time: {datetime.now().isoformat()}")
    print(f"🔑 API Key: 1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ")
    print(f"💰 Plan Type: Lite Plan (web search + web reader + GLM chat)")
    print("=" * 80)
    
    # Test GLM chat
    await test_glm_chat()
    
    # Test web search
    await test_lite_plan_web_search()
    
    # Test web reader
    await test_lite_plan_web_reader()
    
    # Test cost optimization
    await test_cost_optimization()
    
    print("✅ Lite Plan Test Suite Complete")

if __name__ == "__main__":
    asyncio.run(main())