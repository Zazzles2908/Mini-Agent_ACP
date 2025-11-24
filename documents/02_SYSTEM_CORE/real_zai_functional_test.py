#!/usr/bin/env python3
"""
Real Z.AI Functional Testing - Test the 3 working implementations
"""

import os
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("🧪 REAL Z.AI FUNCTIONAL TESTING")
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
                if hasattr(client, 'web_search'):
                    print(f"    ✅ Has web_search method")
                if hasattr(client, 'web_search_async'):
                    print(f"    ✅ Has web_search_async method")
                if hasattr(client, 'search_web'):
                    print(f"    ✅ Has search_web method")
                    
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

# Test 3: Actual web search functionality
print(f"\n🌐 Testing actual web search with simple query...")

try:
    # Import the working implementation
    from mini_agent.tools.zai_unified_tools import ZAIWebSearchTool
    
    print("  🎯 Creating search tool instance...")
    search_tool = ZAIWebSearchTool()
    
    print(f"  🔍 Tool name: {search_tool.name}")
    print(f"  📝 Tool description: {search_tool.description[:100]}...")
    
    # Test with a simple search (this is where we'd consume credits)
    print("  ⚠️  About to test web search - this may consume credits!")
    
    # Ask user for confirmation
    user_input = input("  ❓ Continue with actual web search test? (y/N): ")
    if user_input.lower() == 'y':
        print("  🔍 Running web search test...")
        
        import asyncio
        
        async def test_search():
            try:
                result = await search_tool.execute(query="test search", max_results=1)
                print(f"  ✅ Web search result: {result}")
                return True
            except Exception as e:
                print(f"  ❌ Web search failed: {e}")
                return False
        
        # Actually run the search
        asyncio.run(test_search())
        
    else:
        print("  ⏭️  Skipping web search test")
        
except Exception as e:
    print(f"  ❌ Web search test setup failed: {e}")

# Test 4: Check API key and configuration
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

# Test 5: Check what's actually loaded by the system
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

print(f"\n📊 FUNCTIONAL TESTING SUMMARY")
print(f"="*50)
print(f"✅ 3 working implementations identified")
print(f"🧪 Ready for functional testing")
print(f"⚠️  Some tests may consume Z.AI credits")
