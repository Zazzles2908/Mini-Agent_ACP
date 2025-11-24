#!/usr/bin/env python3
"""
Basic Z.AI Test - Check current state without network calls
"""

print("🔍 Basic Z.AI State Check")
print("=" * 25)

# 1. Check if config file exists and is readable
print("1. Config Check:")
try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    
    from mini_agent.config.config import Config
    config = Config()
    
    print("   ✅ Config imported successfully")
    print(f"   Z.AI API Key: {'Present' if config.zai_api_key else 'Missing'}")
    print(f"   Z.AI Search Enabled: {getattr(config.tools.zai_settings, 'enable_zai_search', 'Not found')}")
    
except Exception as e:
    print(f"   ❌ Config error: {e}")
    print("   This indicates a fundamental issue with the config system")

print()

# 2. Check current implementations
print("2. Implementation Status:")
implementations = [
    ('mini_agent.llm.zai_client', 'ZAIClient'),
    ('mini_agent.llm.coding_plan_zai_client', 'CodingPlanZAIClient'),
    ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
]

for module_path, class_name in implementations:
    try:
        module = __import__(module_path, fromlist=[class_name])
        client_class = getattr(module, class_name)
        print(f"   ✅ {class_name}: Available")
        
        # Quick method check
        methods = [m for m in dir(client_class) if not m.startswith('_') and callable(getattr(client_class, m, None))]
        print(f"      Methods: {len(methods)} public methods")
        
    except Exception as e:
        print(f"   ❌ {class_name}: {e}")

print()

# 3. Check if we can create instances (basic check)
print("3. Instance Creation Test:")
try:
    from mini_agent.tools.zai_unified_tools import ZAIWebSearchTool
    tool = ZAIWebSearchTool()
    print("   ✅ ZAIWebSearchTool: Can be instantiated")
    print(f"   Tool config: {hasattr(tool, 'config')}")
    
except Exception as e:
    print(f"   ❌ ZAIWebSearchTool: {e}")

print()

# 4. Simple network test
print("4. Network Connectivity Test:")
try:
    import urllib.request
    import ssl
    
    # Create SSL context that doesn't verify certificates (for testing)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Test a simple HTTPS connection
    req = urllib.request.Request('https://api.z.ai/api/coding/paas/v4/models')
    
    with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
        if response.status == 200:
            print("   ✅ Z.AI API: HTTPS connection works")
            data = response.read()[:100]  # First 100 bytes
            print(f"   Response size: {len(data)} bytes")
        else:
            print(f"   ⚠️ Z.AI API: HTTP {response.status}")
            
except Exception as e:
    print(f"   ❌ Z.AI API: {e}")

print()
print("=" * 25)
print("📋 Summary:")
print("If all checks pass, the system is ready for Phase 1 consolidation")
print("If any fail, we need to fix the fundamental issue first")