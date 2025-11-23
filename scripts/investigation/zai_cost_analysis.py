#!/usr/bin/env python3
"""
Z.AI Cost Structure Investigation
Investigate why 1 cent was consumed when Lite plan should have free quotas
"""

import asyncio
import os
import sys

sys.path.insert(0, '.')

async def investigate_zai_cost_structure():
    """Investigate Z.AI cost structure and quota usage"""
    print("🔍 Z.AI Cost Structure Investigation")
    print("=" * 45)
    
    # Check what we found earlier about Lite plan
    lite_plan_info = {
        "web_searches": 100,
        "web_readers": 100, 
        "glm_prompts": "120 every 5 hours",
        "cost": "FREE with Lite plan"
    }
    
    print(f"Lite Plan Expected Quotas:")
    print(f"   Web Searches: {lite_plan_info['web_searches']}")
    print(f"   Web Readers: {lite_plan_info['web_readers']}")
    print(f"   GLM Prompts: {lite_plan_info['glm_prompts']}")
    print(f"   Cost: {lite_plan_info['cost']}")
    
    # Test what actually got called
    print(f"\nWhat We Tested During Phase 2:")
    
    test_calls = [
        "ZAIClient.web_search() - 1 call",
        "Direct API web_search - 1 call", 
        "Consolidated client tests - 2-3 calls",
        "Total estimated calls: ~5 web searches"
    ]
    
    for call in test_calls:
        print(f"   • {call}")
    
    # Analyze the 1 cent consumption
    print(f"\n💰 Cost Analysis:")
    print(f"   Expected: $0 (using free Lite plan quotas)")
    print(f"   Actual: 1 cent consumed")
    print(f"   Calls made: ~5 web searches")
    print(f"   Expected quota usage: 5/100 searches")
    
    # Possible explanations
    print(f"\n🤔 Possible Explanations:")
    explanations = [
        "1. Lite plan quotas are NOT actually free - they still cost money",
        "2. Lite plan has hidden costs beyond the advertised free quotas", 
        "3. Free quotas only apply to specific endpoints/features",
        "4. API calls made during testing triggered billable features",
        "5. Background processes or credit protection used billable calls"
    ]
    
    for i, explanation in enumerate(explanations, 1):
        print(f"   {i}. {explanation}")
    
    # Check what Z.AI API was actually called
    print(f"\n🔍 API Endpoints Called:")
    endpoints_called = [
        "POST https://api.z.ai/api/coding/paas/v4/web_search",
        "Headers: Authorization Bearer [API_KEY], Content-Type: application/json",
        "Payload: search_engine, search_query, count, search_recency_filter"
    ]
    
    for endpoint in endpoints_called:
        print(f"   • {endpoint}")
    
    # Verification needed
    print(f"\n❓ Verification Needed:")
    verification_items = [
        "Check Z.AI dashboard for exact quota usage",
        "Verify if web searches consume from 100 free quota or bill separately",
        "Confirm which Lite plan features are actually free",
        "Check if billing was from API calls or other Z.AI services"
    ]
    
    for item in verification_items:
        print(f"   • {item}")
    
    return {
        "expected_cost": 0,
        "actual_cost": 0.01,
        "calls_made": 5,
        "explanations": explanations,
        "verification_needed": verification_items
    }

async def check_zai_dashboard_access():
    """Check if we can access Z.AI dashboard info"""
    print(f"\n🌐 Z.AI Dashboard Information")
    print("=" * 35)
    
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ No Z.AI API key available")
        return False
    
    try:
        import aiohttp
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Try to get account information
        async with aiohttp.ClientSession() as session:
            # Test if we can get account info
            async with session.get(
                'https://api.z.ai/api/coding/paas/v4/models',
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                if response.status == 200:
                    print("✅ API connectivity confirmed")
                    models = await response.json()
                    print(f"   Available models: {len(models.get('data', []))}")
                    return True
                else:
                    print(f"❌ API error: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Dashboard check failed: {e}")
        return False

async def main():
    """Main investigation"""
    print("💰 Z.AI Cost Consumption Analysis")
    print("Understanding the 1 cent spent during Phase 2 testing")
    print()
    
    # Investigate cost structure
    cost_info = await investigate_zai_cost_structure()
    
    # Check dashboard access
    dashboard_ok = await check_zai_dashboard_access()
    
    print("\n" + "=" * 45)
    print("📊 Cost Analysis Summary:")
    print(f"   Expected: ${cost_info['expected_cost']} (free quotas)")
    print(f"   Actual: ${cost_info['actual_cost']} (real money)")
    print(f"   Gap: ${cost_info['actual_cost'] - cost_info['expected_cost']}")
    
    print(f"\n🎯 Key Questions:")
    print(f"   1. Should Lite plan web searches be completely free?")
    print(f"   2. Did we accidentally trigger paid features?")
    print(f"   3. Is the 1 cent from quota overage or base costs?")
    
    print(f"\n📋 Recommendations:")
    print(f"   1. Check Z.AI dashboard for exact quota status")
    print(f"   2. Verify Lite plan cost structure")
    print(f"   3. Consider using MCP for quota tracking")
    print(f"   4. Implement stricter cost controls for testing")
    
    return cost_info

if __name__ == "__main__":
    result = asyncio.run(main())