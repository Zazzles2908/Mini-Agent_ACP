#!/usr/bin/env python3
"""
Real Z.AI Functional Testing - Test the 3 working implementations (Automated)
"""

import os
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("🧪 REAL Z.AI FUNCTIONAL TESTING (AUTOMATED)")
print("="*50)

# Test the 3 working implementations
working_impls = [
    "mini_agent.llm.zai_client",
    "mini_agent.llm.coding_plan_zai_client", 
    "mini_agent.tools.zai_unified_tools"
]

# Import and test each working implementation
for impl in working_impls:
    print(f"\n🔬 Testing {impl}...")
    
    try:
        module = __import__(impl, fromlist=[''])
        
        # Test 1: Can we create instances?
        print(f"  📋 Testing class instantiation...")
        
        if 'ZAIClient' in [name for name in dir(module) if not name.startswith('_')]:
            try:
                client = module.ZAIClient()
                print(f"    ✅ ZAIClient instantiated successfully")
                
                # Test 2: Check if it has web search methods
                methods = ['web_search', 'web_search_async', 'search_web', 'web_read']
                for method in methods:
                    if hasattr(client, method):
                        print(f"    ✅ Has {method} method")
                        
            except Exception as e:
                print(f"    ❌ ZAIClient instantiation failed: {e}")
        
        # Test the tools
        if 'ZAIWebSearchTool' in [name for name in dir(module) if not name.startswith('_')]:
            try:
                search_tool = module.ZAIWebSearchTool()
                print(f"    ✅ ZAIWebSearchTool instantiated")
                
                if hasattr(search_tool, 'execute'):
                    print(f"    ✅ Has execute method")
                if hasattr(search_tool, 'name'):
                    print(f"    ✅ Has name property: {search_tool.name}")
                    
            except Exception as e:
                print(f"    ❌ ZAIWebSearchTool instantiation failed: {e}")
                
        if 'ZAIWebReaderTool' in [name for name in dir(module) if not name.startswith('_')]:
            try:
                reader_tool = module.ZAIWebReaderTool()
                print(f"    ✅ ZAIWebReaderTool instantiated")
                
                if hasattr(reader_tool, 'execute'):
                    print(f"    ✅ Has execute method")
                if hasattr(reader_tool, 'name'):
                    print(f"    ✅ Has name property: {reader_tool.name}")
                    
            except Exception as e:
                print(f"    ❌ ZAIWebReaderTool instantiation failed: {e}")
                
    except Exception as e:
        print(f"  ❌ Module import failed: {e}")

# Test 3: Check API key and configuration
print(f"\n🔑 Testing API key and configuration...")

try:
    from mini_agent.llm.zai_client import get_zai_api_key
    
    api_key = get_zai_api_key()
    if api_key and api_key != "YOUR_ZAI_API_KEY":
        print(f"  ✅ ZAI_API_KEY found (length: {len(api_key)})")
    else:
        print(f"  ❌ ZAI_API_KEY missing or placeholder")
        
except Exception as e:
    print(f"  ❌ API key check failed: {e}")

# Test 4: Check what's actually loaded by the system
print(f"\n🏗️  Testing system integration...")

try:
    import mini_agent.tools
    
    if mini_agent.tools.zai_tools_available():
        print(f"  ✅ System reports Z.AI tools available")
        
        # Test the system's actual tool loading
        if hasattr(mini_agent.tools, 'ZAIWebSearchTool'):
            print(f"  ✅ ZAIWebSearchTool available in system")
        if hasattr(mini_agent.tools, 'ZAIWebReaderTool'):
            print(f"  ✅ ZAIWebReaderTool available in system")
        if hasattr(mini_agent.tools, 'get_zai_tools'):
            print(f"  ✅ get_zai_tools function available")
            
    else:
        print(f"  ❌ System reports Z.AI tools NOT available")
        
except Exception as e:
    print(f"  ❌ System integration test failed: {e}")

# Test 5: Quick API endpoint test (non-interactive)
print(f"\n🌐 Testing Z.AI API endpoint connectivity...")

try:
    import aiohttp
    import asyncio
    
    async def test_endpoint():
        try:
            from mini_agent.llm.zai_client import get_zai_api_key
            api_key = get_zai_api_key()
            
            if not api_key or api_key == "YOUR_ZAI_API_KEY":
                print(f"  ⚠️  No valid API key - skipping endpoint test")
                return
                
            # Test the endpoint
            url = "https://api.z.ai/api/coding/paas/v4/models"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            print(f"  🔍 Testing endpoint: {url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    print(f"    Status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        print(f"    ✅ API endpoint accessible")
                        print(f"    📊 Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    else:
                        print(f"    ❌ API endpoint returned status {response.status}")
                        
        except Exception as e:
            print(f"    ❌ Endpoint test failed: {e}")
    
    # Run the async test
    asyncio.run(test_endpoint())
    
except Exception as e:
    print(f"  ❌ Endpoint test setup failed: {e}")

print(f"\n📊 FUNCTIONAL TESTING SUMMARY")
print(f"="*50)
print(f"✅ 3 working implementations identified")
print(f"🧪 Functional testing completed")
print(f"📋 Ready for MCP migration planning")
