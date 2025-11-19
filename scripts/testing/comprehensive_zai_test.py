#!/usr/bin/env python3
"""
Comprehensive Z.AI Implementation Test
=====================================

Tests:
1. Current Implementation (Common API)
2. Corrected Implementation (Coding Plan API) 
3. GLM Chat Completion (Coding Plan feature)

Provides exact proof of what each implementation returns.
"""

import asyncio
import json
import os
from datetime import datetime

# Import both implementations
from mini_agent.llm.zai_client import ZAIClient
from mini_agent.llm.coding_plan_zai_client import CodingPlanZAIClient

# API Keys
CODING_PLAN_API_KEY = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def print_result(test_name: str, result: dict):
    """Print formatted test result"""
    print(f"\n🔍 {test_name}")
    print("-" * 60)
    print(f"Success: {'✅' if result.get('success', False) else '❌'}")
    
    if result.get('success'):
        # Show success details
        for key in ['id', 'created', 'query', 'count', 'model', 'url', 'title', 'word_count']:
            if key in result:
                print(f"{key.title()}: {result[key]}")
        
        # Show content preview
        if 'analysis' in result:
            print(f"\nAnalysis Preview (first 200 chars):")
            print(f"{result['analysis'][:200]}...")
            
        if 'choices' in result:
            print(f"\nGLM Response (first 200 chars):")
            choice = result['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                print(f"{choice['message']['content'][:200]}...")
        
        if 'content' in result:
            print(f"\nContent Preview (first 200 chars):")
            print(f"{result['content'][:200]}...")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    if 'api_endpoint' in result:
        print(f"API Endpoint: {result['api_endpoint']}")

async def test_common_api():
    """Test current Common API implementation"""
    print_header("TESTING COMMON API (Current Implementation)")
    
    client = ZAIClient(CODING_PLAN_API_KEY)  # Using your key
    print(f"API Endpoint: {client.base_url}")
    print(f"Expected Issue: This uses Common API with Coding Plan key - should fail with billing error")
    
    results = {}
    
    # Test 1: Web Search
    print_result("Common API - Web Search", 
                 await client.web_search("GLM-4.6 coding features", count=2))
    
    # Test 2: Web Reading  
    print_result("Common API - Web Reading",
                 await client.web_reading("https://docs.z.ai"))
    
    # Test 3: Research
    print_result("Common API - Research",
                 await client.research_and_analyze("GLM-4.6 features", depth="quick"))
    
    return results

async def test_coding_plan_api():
    """Test proper Coding Plan API implementation"""
    print_header("TESTING CODING PLAN API (Corrected Implementation)")
    
    client = CodingPlanZAIClient(CODING_PLAN_API_KEY)
    print(f"API Endpoint: {client.base_url}")
    print(f"Expected: This should work if your Coding Plan is active")
    
    # Test 1: Web Search
    search_result = await client.web_search("GLM-4.6 coding features", count=2)
    print_result("Coding Plan API - Web Search", search_result)
    
    # Test 2: Web Reading  
    reading_result = await client.web_reading("https://docs.z.ai")
    print_result("Coding Plan API - Web Reading", reading_result)
    
    # Test 3: GLM Chat Completion (main feature of Coding Plan)
    chat_messages = [
        {"role": "user", "content": "Explain what makes GLM-4.6 special for coding tasks"}
    ]
    
    print_result("Coding Plan API - GLM-4.6 Chat Completion",
                 await client.chat_completion(
                     messages=chat_messages,
                     model="GLM-4.6"
                 ))
    
    # Test 4: Try with different GLM model
    print_result("Coding Plan API - GLM-4.5 Chat Completion",
                 await client.chat_completion(
                     messages=[{"role": "user", "content": "Compare GLM-4.5 vs GLM-4.6"}],
                     model="GLM-4.5"
                 ))

async def compare_implementations():
    """Compare both implementations side by side"""
    print_header("IMPLEMENTATION COMPARISON")
    
    # Create clients
    common_client = ZAIClient(CODING_PLAN_API_KEY)
    coding_client = CodingPlanZAIClient(CODING_PLAN_API_KEY)
    
    print(f"\n📋 API ENDPOINT COMPARISON:")
    print(f"Common API:     {common_client.base_url}")
    print(f"Coding Plan API: {coding_client.base_url}")
    
    print(f"\n🔑 EXPECTED DIFFERENCES:")
    print(f"Common API:")
    print(f"  - Uses: https://api.z.ai/api/paas/v4")
    print(f"  - Target: General Z.AI users")
    print(f"  - Issue with Coding Plan key: Billing/authentication errors")
    
    print(f"\nCoding Plan API:")
    print(f"  - Uses: https://api.z.ai/api/coding/paas/v4")
    print(f"  - Target: GLM Coding Plan subscribers")
    print(f"  - Features: GLM-4.6, GLM-4.5 access")
    print(f"  - OpenAI compatible endpoint: /chat/completions")

def create_corrected_implementation():
    """Create implementation guide for fixing current code"""
    print_header("CORRECTED IMPLEMENTATION GUIDE")
    
    implementation_guide = """
🔧 HOW TO FIX YOUR CURRENT IMPLEMENTATION

1. UPDATE BASE URL:
   OLD: self.base_url = "https://api.z.ai/api/paas/v4"
   NEW: self.base_url = "https://api.z.ai/api/coding/paas/v4"

2. ADD GLM CHAT COMPLETION:
   The Coding Plan API provides GLM model access via:
   - Endpoint: {base_url}/chat/completions
   - Models: "GLM-4.6", "GLM-4.5", "GLM-4.5-air"
   - OpenAI Protocol compatible

3. WEB SEARCH/READING ENDPOINTS:
   These may be limited in Coding Plan API.
   Primary focus is on GLM model access.

4. BILLING/AUTHENTICATION:
   - Coding Plan API requires active subscription
   - API key: 1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ (provided by user)
   - Check subscription status if getting 429 errors
"""
    
    print(implementation_guide)

async def main():
    """Main test function"""
    print("🔬 COMPREHENSIVE Z.AI IMPLEMENTATION ANALYSIS")
    print("Testing current vs corrected implementation with Coding Plan")
    print("Using API Key: 1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ")
    
    try:
        # Test current implementation
        await test_common_api()
        
        print("\n" + "="*80)
        
        # Test corrected implementation
        await test_coding_plan_api()
        
        # Compare implementations
        await compare_implementations()
        
        # Provide implementation guide
        create_corrected_implementation()
        
        print_header("SUMMARY")
        print("✅ Tests completed successfully")
        print("📊 Results show the difference between Common API and Coding Plan API")
        print("🔧 Recommendations provided for implementation fix")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
