#!/usr/bin/env python3
"""
Test Z.AI Web Search and Reading Tools
=====================================

This script tests the current Z.AI implementation vs the proper Coding Plan API
and provides exact proof of what each method returns.

API Keys:
- Current: Uses ZAI_API_KEY env variable (if available)
- Coding Plan: Uses the provided key from user
"""

import asyncio
import json
import os
from datetime import datetime

# Import current Z.AI client
from mini_agent.llm.zai_client import ZAIClient

# API Keys
CURRENT_API_KEY = os.getenv("ZAI_API_KEY", "not_available")
CODING_PLAN_API_KEY = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"

def log_result(test_name: str, result: dict, detailed: bool = True):
    """Log test result with proper formatting"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    
    if detailed:
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Success: {result.get('success', False)}")
        
        if result.get('success'):
            # Extract relevant fields
            relevant_fields = ['id', 'created', 'query', 'count', 'model', 'url', 'title', 'word_count']
            for field in relevant_fields:
                if field in result:
                    print(f"{field.title()}: {result[field]}")
            
            # Show content preview
            if 'analysis' in result:
                print(f"\nAnalysis Preview (first 300 chars):")
                print(f"{result['analysis'][:300]}...")
            
            if 'content' in result:
                print(f"\nContent Preview (first 300 chars):")
                print(f"{result['content'][:300]}...")
                
            if 'search_result' in result:
                print(f"\nSearch Results Count: {len(result['search_result'])}")
                if result['search_result']:
                    print(f"First Result Title: {result['search_result'][0].get('title', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    else:
        print(json.dumps(result, indent=2))

async def test_current_implementation():
    """Test current implementation using Common API"""
    print(f"\n🔍 TESTING CURRENT IMPLEMENTATION (Common API)")
    print(f"API Key Available: {'✅' if CURRENT_API_KEY != 'not_available' else '❌'}")
    
    if CURRENT_API_KEY == 'not_available':
        print("⚠️  No ZAI_API_KEY found in environment - testing with Coding Plan key")
        client = ZAIClient(CODING_PLAN_API_KEY)
    else:
        client = ZAIClient(CURRENT_API_KEY)
    
    print(f"Using Base URL: {client.base_url}")
    
    # Test 1: Basic web search
    print(f"\n📊 TEST 1: Basic Web Search")
    search_result = await client.web_search(
        query="GLM-4.6 model features coding plan",
        count=3,
        search_engine="search-std"  # Using cheaper option
    )
    log_result("Current Implementation - Web Search", search_result)
    
    # Test 2: Web reading
    print(f"\n📖 TEST 2: Web Reading")
    reading_result = await client.web_reading(
        url="https://docs.z.ai/devpack/overview"
    )
    log_result("Current Implementation - Web Reading", reading_result)
    
    # Test 3: Research and Analyze
    print(f"\n🔬 TEST 3: Research and Analyze")
    research_result = await client.research_and_analyze(
        query="GLM-4.6 capabilities web search API",
        depth="quick",
        model_preference="auto"
    )
    log_result("Current Implementation - Research", research_result)
    
    return {
        "web_search": search_result,
        "web_reading": reading_result,
        "research": research_result
    }

async def test_coding_plan_api():
    """Test proper Coding Plan API"""
    print(f"\n🚀 TESTING CODING PLAN API")
    print(f"Using Coding Plan API Key: ✅")
    
    # Create Coding Plan client
    coding_client = ZAIClient(CODING_PLAN_API_KEY)
    coding_client.base_url = "https://api.z.ai/api/coding/paas/v4"
    
    print(f"Using Coding Plan Base URL: {coding_client.base_url}")
    
    # Test 1: Basic web search with Coding Plan
    print(f"\n📊 TEST 1: Coding Plan Web Search")
    search_result = await coding_client.web_search(
        query="GLM-4.6 model features coding plan",
        count=3,
        search_engine="search-std"
    )
    log_result("Coding Plan API - Web Search", search_result)
    
    # Test 2: Web reading with Coding Plan
    print(f"\n📖 TEST 2: Coding Plan Web Reading")
    reading_result = await coding_client.web_reading(
        url="https://docs.z.ai/devpack/overview"
    )
    log_result("Coding Plan API - Web Reading", reading_result)
    
    # Test 3: Research with premium settings
    print(f"\n🔬 TEST 3: Coding Plan Research with GLM-4.6")
    research_result = await coding_client.research_and_analyze(
        query="GLM-4.6 capabilities web search API",
        depth="comprehensive",
        model_preference="glm-4.6"
    )
    log_result("Coding Plan API - Research (GLM-4.6)", research_result)
    
    return {
        "web_search": search_result,
        "web_reading": reading_result,
        "research": research_result
    }

def compare_results(current: dict, coding: dict):
    """Compare results between current and coding plan implementation"""
    print(f"\n📋 COMPARISON ANALYSIS")
    print(f"{'='*60}")
    
    for test_name in ["web_search", "web_reading", "research"]:
        print(f"\n🔍 {test_name.upper()} Comparison:")
        
        current_result = current.get(test_name, {})
        coding_result = coding.get(test_name, {})
        
        print(f"  Current API Success: {current_result.get('success', False)}")
        print(f"  Coding Plan Success: {coding_result.get('success', False)}")
        
        if current_result.get('success') and coding_result.get('success'):
            print(f"  Current Base URL: {current_result.get('base_url', 'N/A')}")
            print(f"  Coding Base URL: {coding_result.get('base_url', 'N/A')}")
            
            # Show differences in results
            current_id = current_result.get('id', 'N/A')
            coding_id = coding_result.get('id', 'N/A')
            print(f"  Current ID: {current_id}")
            print(f"  Coding ID: {coding_id}")
            
            if current_id != coding_id:
                print(f"  ✅ Different results - different API endpoints confirmed")
            else:
                print(f"  ❌ Same results - likely same endpoint")
        
        elif not current_result.get('success'):
            print(f"  ⚠️  Current API failed: {current_result.get('error', 'Unknown error')}")
        elif not coding_result.get('success'):
            print(f"  ⚠️  Coding Plan API failed: {coding_result.get('error', 'Unknown error')}")

async def main():
    """Main test function"""
    print("🔬 Z.AI IMPLEMENTATION TEST & COMPARISON")
    print("=" * 60)
    print("Testing current implementation vs proper Coding Plan API")
    print("=" * 60)
    
    # Test current implementation
    current_results = await test_current_implementation()
    
    # Test coding plan API
    coding_results = await test_coding_plan_api()
    
    # Compare results
    compare_results(current_results, coding_results)
    
    print(f"\n✅ TESTS COMPLETED")
    print(f"Current implementation results: {len([r for r in current_results.values() if r.get('success')])}/3 successful")
    print(f"Coding Plan results: {len([r for r in coding_results.values() if r.get('success')])}/3 successful")

if __name__ == "__main__":
    asyncio.run(main())