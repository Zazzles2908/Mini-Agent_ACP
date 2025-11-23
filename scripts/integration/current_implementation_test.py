#!/usr/bin/env python3
"""
Test Current Z.AI Implementation
Tests the actual working implementations we found
"""

print("🔍 Testing Current Z.AI Implementation")
print("=" * 40)

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Test 1: Check config and credit protection
print("1. Config & Credit Protection Test:")
try:
    from mini_agent.config.config import Config
    config = Config()
    
    print(f"   Z.AI Search Enabled: {config.tools.enable_zai_search}")
    print(f"   Z.AI API Key Present: {bool(config.zai_api_key)}")
    
    # Test credit protection
    try:
        from mini_agent.utils.credit_protection import check_zai_protection
        protection_status = check_zai_protection()
        print(f"   Credit Protection Status: {protection_status}")
        print(f"   Protection Logic: {'Blocked' if protection_status else 'Allowed'}")
    except Exception as e:
        print(f"   ⚠️ Credit Protection: {e}")
        
except Exception as e:
    print(f"   ❌ Config error: {e}")

print()

# Test 2: Import working implementations
print("2. Implementation Import Test:")
implementations = [
    ('mini_agent.llm.zai_client', 'ZAIClient'),
    ('mini_agent.llm.coding_plan_zai_client', 'CodingPlanZAIClient'),  
    ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
]

working_implementations = []

for module_path, class_name in implementations:
    try:
        module = __import__(module_path, fromlist=[class_name])
        client_class = getattr(module, class_name)
        print(f"   ✅ {class_name}: Import successful")
        
        # Check methods
        methods = [m for m in dir(client_class) if not m.startswith('_') and callable(getattr(client_class, m, None))]
        print(f"      Methods: {len(methods)} public methods")
        
        working_implementations.append((class_name, module_path, methods))
        
    except Exception as e:
        print(f"   ❌ {class_name}: {e}")

print()

# Test 3: Try basic instantiation
print("3. Instance Creation Test:")
for class_name, module_path, methods in working_implementations:
    try:
        if class_name == 'ZAIWebSearchTool':
            # This should work with current config
            module = __import__(module_path, fromlist=[class_name])
            tool_class = getattr(module, class_name)
            tool = tool_class()
            print(f"   ✅ {class_name}: Instance created successfully")
            
            # Check if it has config
            has_config = hasattr(tool, 'config')
            print(f"      Has config: {has_config}")
            
            if has_config:
                print(f"      Config type: {type(tool.config)}")
                
        elif class_name == 'ZAIClient':
            from mini_agent.config.config import Config
            config = Config()
            module = __import__(module_path, fromlist=[class_name])
            client_class = getattr(module, class_name)
            client = client_class(config.zai_api_key)
            print(f"   ✅ {class_name}: Instance created successfully")
            print(f"      Base URL: {getattr(client, 'base_url', 'N/A')}")
            
    except Exception as e:
        print(f"   ❌ {class_name}: {e}")

print()

# Test 4: Check for duplicate methods
print("4. Method Analysis:")
print(f"   Found {len(working_implementations)} working implementations")
for class_name, module_path, methods in working_implementations:
    print(f"   {class_name}:")
    print(f"      Module: {module_path}")
    print(f"      Public methods: {len(methods)}")
    if len(methods) > 5:
        print(f"      First 5 methods: {methods[:5]}")
    if len(methods) > 10:
        print(f"      Too many methods - possible duplication")

print()
print("=" * 40)
print("📊 Current State Summary:")
print(f"   Working Implementations: {len(working_implementations)}/3")
print(f"   Z.AI Search Config: {config.tools.enable_zai_search if 'config' in locals() else 'Unknown'}")
print(f"   Credit Protection: {'Active' if 'protection_status' in locals() and protection_status else 'Inactive'}")

# Check for duplicated methods
if any(len(methods) > 10 for _, _, methods in working_implementations):
    print(f"   ⚠️ DETECTED: Possible method duplication in Z.AI implementations")
    print(f"   🔧 NEEDS: Consolidation of duplicate methods")

print()
print("🎯 Ready for Phase 1 (Consolidation) if:")
print("   1. At least 2 implementations working")
print("   2. No critical configuration issues") 
print("   3. Method duplication identified for cleanup")