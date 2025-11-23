#!/usr/bin/env python3
"""
Real MCP Integration Test - Phase 2b
Tests the unified MCP client without config dependencies
"""

import asyncio
import json
import os
import sys

# Add current directory to path
sys.path.insert(0, '.')

async def test_mcp_connectivity():
    """Test MCP server connectivity directly"""
    print("🚀 Testing MCP Server Connectivity")
    print("=" * 40)
    
    # Get API key from environment or config
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ ZAI_API_KEY not found in environment")
        print("📋 Testing connectivity without authentication...")
        
        # Test basic connectivity
        import urllib.request
        import ssl
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # Test basic connection
            req = urllib.request.Request('https://api.z.ai')
            with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
                print(f"   ✅ Z.AI API reachable: {response.status}")
                return True
        except Exception as e:
            print(f"   ❌ Z.AI API unreachable: {e}")
            return False
    
    print(f"✅ Z.AI API Key: Present (length: {len(api_key)})")
    
    # Test MCP endpoint connectivity
    try:
        import aiohttp
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test MCP web search endpoint
        test_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "web_search_prime",
            "params": {
                "query": "test MCP connectivity",
                "count": 1,
                "search_engine": "search-prime",
                "recency_filter": "noLimit"
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.z.ai/api/mcp/web_search_prime/mcp',
                headers=headers,
                json=test_payload,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ MCP Web Search: Working (Status: {response.status})")
                    print(f"   Response size: {len(str(result))} bytes")
                    return True
                else:
                    error_text = await response.text()
                    print(f"   ❌ MCP Web Search: Error {response.status}")
                    print(f"   Error: {error_text[:200]}...")
                    return False
                    
    except Exception as e:
        print(f"   ❌ MCP Test failed: {e}")
        return False

async def test_unified_client_direct():
    """Test unified client with direct API access"""
    print("\n🔍 Testing Unified MCP Client")
    print("=" * 40)
    
    try:
        # Import the unified client directly
        from mini_agent.integrations.unified_zai_mcp_client import UnifiedZAIMCPClient
        
        api_key = os.getenv('ZAI_API_KEY')
        if not api_key:
            print("❌ No API key available for testing")
            return False
        
        # Create client
        client = UnifiedZAIMCPClient(api_key)
        print("✅ Unified MCP Client created")
        
        # Test with minimal search
        print("   Testing minimal search...")
        result = await client.web_search_mcp(
            query="Z.AI MCP configuration",
            count=1
        )
        
        if result["success"]:
            print(f"   ✅ Minimal search: SUCCESS")
            results = result.get("search_result", [])
            print(f"   Results count: {len(results)}")
            if results:
                print(f"   First result: {results[0].get('title', 'N/A')[:50]}...")
            return True
        else:
            print(f"   ❌ Minimal search: FAILED")
            print(f"   Error: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Unified client test failed: {e}")
        return False

async def main():
    """Main test execution"""
    print("🎯 Phase 2b: Real MCP Integration Testing")
    print("Testing Z.AI MCP server connectivity and unified client")
    print()
    
    # Test 1: Basic connectivity
    connectivity_ok = await test_mcp_connectivity()
    
    # Test 2: Unified client (if connectivity works)
    if connectivity_ok:
        unified_ok = await test_unified_client_direct()
        print("\n" + "=" * 40)
        print("📊 Final Results:")
        print(f"   MCP Connectivity: {'✅' if connectivity_ok else '❌'}")
        print(f"   Unified Client: {'✅' if unified_ok else '❌'}")
        
        if connectivity_ok and unified_ok:
            print(f"\n🎯 STATUS: Ready for Phase 1 (Consolidation)")
            print(f"   MCP integration is working!")
        elif connectivity_ok:
            print(f"\n⚠️ STATUS: MCP works but unified client needs fixes")
        else:
            print(f"\n❌ STATUS: MCP connectivity issues")
    else:
        print("\n" + "=" * 40)
        print("❌ MCP connectivity failed - cannot proceed with integration")
    
    # Save test results
    test_results = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "mcp_connectivity": connectivity_ok,
        "unified_client": await test_unified_client_direct() if connectivity_ok else False,
        "ready_for_consolidation": connectivity_ok
    }
    
    with open('MCP_INTEGRATION_TEST_RESULTS.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📄 Results saved to: MCP_INTEGRATION_TEST_RESULTS.json")

if __name__ == "__main__":
    asyncio.run(main())