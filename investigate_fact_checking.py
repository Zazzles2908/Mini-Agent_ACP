#!/usr/bin/env python3
"""
Fact-Checking System Investigation Script
Investigates why fact-checking tools are not operational
"""

import json
import os
import sys

def investigate_zai_config():
    """Investigate Z.AI configuration issues"""
    print("=== Z.AI Configuration Investigation ===")
    
    # Check ZAI_API_KEY
    zai_key = os.environ.get('ZAI_API_KEY')
    print(f"ZAI_API_KEY exists: {'ZAI_API_KEY' in os.environ}")
    
    if zai_key:
        print(f"ZAI_API_KEY length: {len(zai_key)}")
        print(f"ZAI_API_KEY starts with: {zai_key[:10]}...")
        
        # Check for Bearer token format (should NOT have Bearer)
        if zai_key.startswith('Bearer '):
            print("❌ ERROR: ZAI_API_KEY starts with 'Bearer' (should be raw key)")
            print("Expected format: abc123def456...")
            print(f"Found format: Bearer {zai_key[7:17]}...")
            return False
        else:
            print("✅ ZAI_API_KEY appears to be in correct format")
            return True
    else:
        print("❌ ERROR: ZAI_API_KEY not found in environment")
        return False

def investigate_mcp_config():
    """Investigate MCP configuration issues"""
    print("\n=== MCP Configuration Investigation ===")
    
    try:
        with open('mini_agent/config/.mcp.json', 'r') as f:
            mcp_config = json.load(f)
        
        print("✅ MCP config file found and loaded")
        
        # Check for Z.AI servers
        zai_servers = {}
        for server_name, server_config in mcp_config.get('mcpServers', {}).items():
            if 'z.ai' in server_config.get('url', '').lower() or 'zai' in server_name.lower():
                zai_servers[server_name] = server_config
        
        print(f"Found {len(zai_servers)} Z.AI servers in MCP config:")
        for name, config in zai_servers.items():
            url = config.get('url', 'No URL')
            headers = config.get('headers', {})
            print(f"  - {name}:")
            print(f"    URL: {url}")
            print(f"    Headers: {list(headers.keys())}")
            if 'Authorization' in headers:
                auth = headers['Authorization']
                print(f"    Auth format: {auth[:20]}...")
        
        # Check for required headers
        for name, config in zai_servers.items():
            headers = config.get('headers', {})
            if 'Accept' not in headers:
                print(f"❌ WARNING: {name} missing Accept header")
            if 'Authorization' not in headers:
                print(f"❌ ERROR: {name} missing Authorization header")
            else:
                auth_value = headers['Authorization']
                if not auth_value.startswith('Bearer '):
                    print(f"❌ ERROR: {name} Authorization header should start with 'Bearer '")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to read MCP config: {e}")
        return False

def test_zai_connectivity():
    """Test basic Z.AI connectivity"""
    print("\n=== Z.AI Connectivity Test ===")
    
    import aiohttp
    import asyncio
    
    zai_key = os.environ.get('ZAI_API_KEY')
    if not zai_key:
        print("❌ Cannot test connectivity - no ZAI_API_KEY")
        return False
    
    async def test_endpoint(url, name):
        """Test a single Z.AI endpoint"""
        headers = {
            "Authorization": f"Bearer {zai_key}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
        
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=test_request,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    print(f"✅ {name} responded with status {response.status}")
                    print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    if response.status == 200:
                        data = await response.json()
                        if 'result' in data and 'tools' in data['result']:
                            tool_count = len(data['result']['tools'])
                            print(f"   Found {tool_count} tools")
                        else:
                            print(f"   Unexpected response format")
                    return response.status == 200
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            return False
    
    # Test both Z.AI endpoints
    endpoints = [
        ("https://api.z.ai/api/mcp/web_search_prime/mcp", "Web Search Prime"),
        ("https://api.z.ai/api/mcp/web_reader/mcp", "Web Reader")
    ]
    
    async def run_tests():
        results = []
        for url, name in endpoints:
            success = await test_endpoint(url, name)
            results.append(success)
        return results
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(run_tests())
        loop.close()
        
        if all(results):
            print("✅ All Z.AI endpoints are accessible")
            return True
        else:
            print(f"❌ Some Z.AI endpoints failed: {results}")
            return False
    except Exception as e:
        print(f"❌ Error testing connectivity: {e}")
        return False

def check_fact_checking_tools():
    """Check what fact-checking tools are available"""
    print("\n=== Available Fact-Checking Tools ===")
    
    # Check for specific fact-checking tools
    fact_checking_tools = [
        'minimax_analyze_code',
        'minimax_review_code', 
        'get_skill',
        'webSearchPrime',
        'webReader',
        'zai_web_search'
    ]
    
    available_tools = []
    
    # Test minimax tools that might have fact-checking
    try:
        import types
        # Check if minimax functions are available
        functions_to_test = [
            ('minimax_analyze_code', 'Code analysis with fact-checking'),
            ('minimax_review_code', 'Code review with comprehensive analysis')
        ]
        
        for func_name, description in functions_to_test:
            if hasattr(sys.modules.get('__main__', types.ModuleType('__main__')), func_name):
                print(f"✅ {func_name}: {description}")
                available_tools.append(func_name)
            else:
                print(f"❓ {func_name}: Not directly importable")
                
    except Exception as e:
        print(f"❓ Error checking minimax tools: {e}")
    
    print(f"\nFound {len(available_tools)} functional fact-checking tools")
    return available_tools

def main():
    """Main investigation function"""
    print("🔍 FACT-CHECKING SYSTEM INVESTIGATION")
    print("=" * 50)
    
    zai_ok = investigate_zai_config()
    mcp_ok = investigate_mcp_config()
    
    if zai_ok:
        connectivity_ok = test_zai_connectivity()
    else:
        connectivity_ok = False
    
    tools = check_fact_checking_tools()
    
    print("\n" + "=" * 50)
    print("📊 INVESTIGATION SUMMARY")
    print("=" * 50)
    
    print(f"Z.AI Configuration: {'✅ OK' if zai_ok else '❌ ISSUES'}")
    print(f"MCP Configuration: {'✅ OK' if mcp_ok else '❌ ISSUES'}")  
    print(f"Z.AI Connectivity: {'✅ OK' if connectivity_ok else '❌ FAILED'}")
    print(f"Fact-Checking Tools: {len(tools)} available")
    
    if not zai_ok:
        print("\n🚨 ROOT CAUSE: Z.AI API Key Issues")
        print("Fix: Ensure ZAI_API_KEY is set and in correct format (no 'Bearer' prefix)")
    elif not connectivity_ok:
        print("\n🚨 ROOT CAUSE: Z.AI Endpoint Connectivity Issues") 
        print("Fix: Check network connectivity and Z.AI service status")
    elif len(tools) == 0:
        print("\n🚨 ROOT CAUSE: No Fact-Checking Tools Available")
        print("Fix: Enable MiniMax tools or find alternative fact-checking methods")
    else:
        print("\n✅ SYSTEM APPEARS FUNCTIONAL")
        print("If fact-checking isn't working, may be a different issue")

if __name__ == "__main__":
    main()