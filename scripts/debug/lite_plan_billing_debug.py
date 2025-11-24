#!/usr/bin/env python3
"""
Lite Plan Implementation Debug
Investigate why Lite plan calls are billing additional money instead of using included quotas
"""

import asyncio
import os
import sys

sys.path.insert(0, '.')

async def debug_lite_plan_implementation():
    """Debug why Lite plan API calls are billing instead of using included quotas"""
    print("🔍 Lite Plan Implementation Debug")
    print("=" * 45)
    
    # Review what we're actually calling
    api_calls_made = [
        {
            "endpoint": "https://api.z.ai/api/coding/paas/v4/web_search",
            "method": "POST",
            "purpose": "Web search using direct API",
            "expected": "Use Lite plan included quotas"
        },
        {
            "endpoint": "https://api.z.ai/api/coding/paas/v4/models", 
            "method": "GET",
            "purpose": "List available models",
            "expected": "Check plan eligibility"
        }
    ]
    
    print("📊 API Calls Made During Testing:")
    for i, call in enumerate(api_calls_made, 1):
        print(f"   {i}. {call['method']} {call['endpoint']}")
        print(f"      Purpose: {call['purpose']}")
        print(f"      Expected: {call['expected']}")
        print()
    
    # Possible problems in our implementation
    print("🛠️ Possible Implementation Issues:")
    
    implementation_problems = [
        {
            "issue": "Wrong API Endpoint",
            "description": "Using /web_search instead of /lite_plan/web_search",
            "solution": "Check if Lite plan has dedicated endpoints"
        },
        {
            "issue": "Missing Plan Identification",
            "description": "Not identifying requests as Lite plan usage",
            "solution": "Add plan-specific headers or parameters"
        },
        {
            "issue": "Using Paid Features",
            "description": "API parameters triggering paid add-ons",
            "solution": "Strip out advanced parameters"
        },
        {
            "issue": "Authentication Issue",
            "description": "Not properly authenticating as Lite plan user",
            "solution": "Verify API key has Lite plan permissions"
        },
        {
            "issue": "Credit Protection Interference",
            "description": "Credit protection systems using paid endpoints",
            "solution": "Disable credit protection during testing"
        }
    ]
    
    for i, problem in enumerate(implementation_problems, 1):
        print(f"   {i}. {problem['issue']}")
        print(f"      Problem: {problem['description']}")
        print(f"      Solution: {problem['solution']}")
        print()
    
    # Check what we should be doing for Lite plan
    print("🎯 What Lite Plan Calls Should Look Like:")
    print("   Endpoint: Likely /lite_plan/ or /free/ prefix")
    print("   Headers: Plan identification parameters")
    print("   Parameters: No premium features")
    print("   Authentication: Same API key, different usage tracking")
    
    return implementation_problems

async def check_lite_plan_specific_endpoints():
    """Check if Lite plan has specific endpoints we should use"""
    print(f"\n🌐 Lite Plan Endpoint Investigation")
    print("=" * 40)
    
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ No API key available")
        return False
    
    # Common Lite plan endpoint patterns
    lite_endpoints_to_test = [
        "https://api.z.ai/api/lite/web_search",
        "https://api.z.ai/api/free/web_search", 
        "https://api.z.ai/api/plan/lite/web_search",
        "https://api.z.ai/api/lite_plan/web_search"
    ]
    
    try:
        import aiohttp
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        test_payload = {
            "query": "test",
            "count": 1
        }
        
        for endpoint in lite_endpoints_to_test:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        endpoint,
                        headers=headers,
                        json=test_payload,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        
                        if response.status == 200:
                            print(f"   ✅ Found working endpoint: {endpoint}")
                            print(f"      Status: {response.status}")
                            return True
                        elif response.status == 404:
                            print(f"   ❌ Not found: {endpoint}")
                        elif response.status == 401:
                            print(f"   🔒 Auth error: {endpoint}")
                        else:
                            print(f"   ⚠️ Other error ({response.status}): {endpoint}")
                            
            except Exception as e:
                print(f"   ❌ Failed: {endpoint} - {str(e)[:50]}...")
        
        print(f"\n💡 None of the Lite plan endpoints worked")
        print(f"   This suggests Lite plan uses the same endpoints")
        print(f"   But with different parameters or headers")
        
        return False
        
    except Exception as e:
        print(f"❌ Endpoint testing failed: {e}")
        return False

async def analyze_current_implementation():
    """Analyze what's wrong with current implementation"""
    print(f"\n🔧 Current Implementation Analysis")
    print("=" * 35)
    
    # Check the actual implementation code
    print("📋 What Our Implementation Currently Does:")
    print("   1. Uses standard /coding/paas/v4/web_search endpoint")
    print("   2. Uses search-engine and search-query parameters")
    print("   3. No special Lite plan identification")
    print("   4. Standard headers and authentication")
    
    print(f"\n❓ What We Should Be Checking:")
    print("   1. Are we missing plan-specific parameters?")
    print("   2. Should we use different endpoints?")
    print("   3. Are we missing plan identification headers?")
    print("   4. Is our API key properly configured for Lite plan?")
    
    # The real issue - we don't know how Lite plan billing works
    print(f"\n🚨 The Real Issue:")
    print(f"   We don't understand Z.AI's Lite plan billing mechanism")
    print(f"   We need to find Z.AI's official Lite plan API documentation")
    print(f"   The implementation might require specific parameters or endpoints")
    
    return True

async def main():
    """Debug Lite plan implementation"""
    print("🚨 CRITICAL: Lite Plan Billing Issue")
    print("Paid subscriptions should NOT consume additional credits!")
    print()
    
    # Analyze implementation problems
    problems = await debug_lite_plan_implementation()
    
    # Check for Lite plan specific endpoints
    await check_lite_plan_specific_endpoints()
    
    # Analyze current implementation
    await analyze_current_implementation()
    
    print("\n" + "=" * 45)
    print("🎯 Root Cause Analysis:")
    print("   1. Our API calls are billing additional credits")
    print("   2. Should be using included Lite plan quotas") 
    print("   3. Implementation missing Lite plan specific logic")
    print("   4. Need Z.AI's official Lite plan API documentation")
    
    print(f"\n🔧 Immediate Actions Needed:")
    print("   1. Find Z.AI Lite plan API documentation")
    print("   2. Identify correct endpoints and parameters")
    print("   3. Fix authentication for Lite plan usage")
    print("   4. Test with corrected implementation")
    
    print(f"\n⚠️ STOP ALL TESTING until fixed!")
    print(f"   Each test call is consuming paid credits")
    print(f"   Need to understand proper Lite plan usage")

if __name__ == "__main__":
    asyncio.run(main())