#!/usr/bin/env python3
"""
Final Test: Corrected Z.AI Implementation
==========================================

Tests the corrected implementation using Coding Plan API.
"""

import asyncio
import os
from datetime import datetime

# Import corrected implementation
from mini_agent.llm.zai_client import ZAIClient

# API Key
CODING_PLAN_API_KEY = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

def print_result(title: str, result: dict):
    """Print formatted result"""
    print(f"\n🔍 {title}")
    print("-" * 50)
    print(f"Success: {'✅' if result.get('success', False) else '❌'}")
    
    if result.get('success'):
        # Show details
        for key in ['model', 'content', 'analysis', 'word_count', 'id']:
            if key in result:
                content = result[key]
                if key == 'content' and len(content) > 300:
                    print(f"{key.title()}: {content[:300]}...")
                else:
                    print(f"{key.title()}: {content}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    if 'api_endpoint' in result:
        print(f"API Endpoint: {result['api_endpoint']}")

async def test_corrected_implementation():
    """Test the corrected implementation"""
    print("🚀 TESTING CORRECTED Z.AI IMPLEMENTATION")
    print("=" * 60)
    
    # Create client with Coding Plan API
    client = ZAIClient(CODING_PLAN_API_KEY, use_coding_plan=True)
    print(f"Using Coding Plan API: {client.base_url}")
    
    # Test 1: GLM Chat Completion (main feature)
    print_result("GLM-4.6 Chat Completion", 
                 await client.chat_completion(
                     messages=[{"role": "user", "content": "Explain what GLM-4.6 is best for"}],
                     model="GLM-4.6"
                 ))
    
    # Test 2: GLM Research and Analysis
    print_result("GLM-4.6 Research Analysis",
                 await client.gl_research_and_analyze(
                     query="Benefits of GLM-4.6 for coding tasks",
                     model="GLM-4.6"
                 ))
    
    # Test 3: Try GLM-4.5
    print_result("GLM-4.5 Chat Completion",
                 await client.chat_completion(
                     messages=[{"role": "user", "content": "Compare GLM-4.5 vs GLM-4.6"}],
                     model="GLM-4.5"
                 ))
    
    # Test 4: Web Search (expected to fail based on previous tests)
    print_result("Web Search (for comparison)",
                 await client.web_search("GLM-4.6 coding", count=2))
    
    print(f"\n✅ CORRECTED IMPLEMENTATION TEST COMPLETED")

async def main():
    try:
        await test_corrected_implementation()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
