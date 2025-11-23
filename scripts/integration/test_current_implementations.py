#!/usr/bin/env python3
"""
Real Z.AI Test - Using working implementations
"""

import asyncio
import os
import sys

sys.path.insert(0, '.')

async def test_current_working_implementations():
    """Test the existing working Z.AI implementations"""
    print("🚀 Testing Current Z.AI Implementations")
    print("=" * 45)
    
    # Test the working implementations we found
    implementations = [
        ('mini_agent.llm.zai_client', 'ZAIClient'),
        ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
    ]
    
    results = {}
    
    for module_path, class_name in implementations:
        print(f"\n🔍 Testing {class_name}...")
        try:
            # Import module
            module = __import__(module_path, fromlist=[class_name])
            client_class = getattr(module, class_name)
            
            print(f"   ✅ {class_name}: Import successful")
            
            # Test instantiation
            if class_name == 'ZAIClient':
                api_key = os.getenv('ZAI_API_KEY')
                if not api_key:
                    print(f"   ❌ No API key for {class_name}")
                    results[class_name] = {'import': 'success', 'instantiation': 'failed_no_key'}
                    continue
                    
                client = client_class(api_key)
                print(f"   ✅ {class_name}: Instantiation successful")
                
                # Test basic web search
                print(f"   Testing minimal web search...")
                search_result = await client.web_search(
                    query="Z.AI API test",
                    count=1
                )
                
                if search_result.get("success"):
                    print(f"   ✅ Web search: SUCCESS")
                    search_results = search_result.get("search_result", [])
                    print(f"   Results: {len(search_results)} found")
                    if search_results:
                        print(f"   First result: {search_results[0].get('title', 'N/A')[:50]}...")
                    results[class_name] = {'import': 'success', 'instantiation': 'success', 'search': 'working'}
                else:
                    print(f"   ❌ Web search: FAILED - {search_result.get('error', 'Unknown error')}")
                    results[class_name] = {'import': 'success', 'instantiation': 'success', 'search': 'failed'}
                    
            elif class_name == 'ZAIWebSearchTool':
                # This is the tool interface - test creation
                tool = client_class()
                print(f"   ✅ {class_name}: Instantiation successful")
                print(f"   Config available: {hasattr(tool, 'config')}")
                
                # This tool is designed to be used via agent system, not direct API
                results[class_name] = {'import': 'success', 'instantiation': 'success', 'note': 'tool_interface'}
                
        except Exception as e:
            print(f"   ❌ {class_name}: Failed - {e}")
            results[class_name] = {'import': 'failed', 'error': str(e)}
    
    return results

async def test_direct_api():
    """Test direct Z.AI API to understand the format"""
    print(f"\n🔍 Testing Direct Z.AI API Format")
    print("=" * 35)
    
    try:
        import aiohttp
        
        api_key = os.getenv('ZAI_API_KEY')
        if not api_key:
            print("❌ No API key for direct test")
            return False
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test the current working format (from zai_client.py)
        search_payload = {
            "search_engine": "search-prime",
            "search_query": "Z.AI API test",
            "count": 1,
            "search_recency_filter": "noLimit"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.z.ai/api/coding/paas/v4/web_search',
                headers=headers,
                json=search_payload,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ Direct API: Working (Status: {response.status})")
                    search_result = result.get('search_result', [])
                    print(f"   Results: {len(search_result)} found")
                    if search_result:
                        print(f"   First result: {search_result[0].get('title', 'N/A')[:50]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"   ❌ Direct API: Error {response.status}")
                    print(f"   Error: {error_text[:200]}...")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Direct API test failed: {e}")
        return False

async def main():
    """Main test execution"""
    print("🎯 Real Z.AI Implementation Testing")
    print("Testing existing working implementations vs direct API")
    print()
    
    # Test current implementations
    impl_results = await test_current_working_implementations()
    
    # Test direct API format
    direct_api_ok = await test_direct_api()
    
    print("\n" + "=" * 45)
    print("📊 Test Results Summary:")
    
    for class_name, result in impl_results.items():
        status = "✅ Working" if result.get('search') == 'working' else "❌ Issues"
        if result.get('instantiation') == 'success':
            status = "✅ Ready"
        print(f"   {class_name}: {status}")
        if result.get('search') == 'working':
            print(f"      - Import: Success")
            print(f"      - Instantiation: Success") 
            print(f"      - Web Search: Working")
        elif result.get('import') == 'success':
            print(f"      - Import: Success")
            print(f"      - Note: {result.get('note', 'Available')}")
        else:
            print(f"      - Failed: {result.get('error', 'Unknown')}")
    
    print(f"   Direct API: {'✅ Working' if direct_api_ok else '❌ Failed'}")
    
    # Determine status
    working_search = any(r.get('search') == 'working' for r in impl_results.values())
    
    print()
    if working_search and direct_api_ok:
        print("🎯 STATUS: Current implementations working!")
        print("   Ready for Phase 1 (Consolidation)")
    elif working_search:
        print("⚠️ STATUS: Working implementations found")
        print("   Ready for Phase 1 (Consolidation)")
    elif direct_api_ok:
        print("🔧 STATUS: Direct API works, implementations need fixes")
        print("   Fix implementations then proceed to consolidation")
    else:
        print("❌ STATUS: API connectivity issues")
    
    return working_search, direct_api_ok

if __name__ == "__main__":
    working, direct = asyncio.run(main())
    print(f"\n📄 Working implementations: {working}")
    print(f"📄 Direct API working: {direct}")