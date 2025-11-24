#!/usr/bin/env python3
"""
Quick Z.AI Health Check
Simple connectivity test without timeouts
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_config():
    """Test configuration loading"""
    try:
        from mini_agent.config.config import Config
        config = Config()
        
        print("✅ Config import successful")
        print(f"   Z.AI API Key present: {bool(config.zai_api_key)}")
        if config.zai_api_key:
            print(f"   API Key length: {len(config.zai_api_key)}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_imports():
    """Test importing Z.AI implementations"""
    print("\n🔍 Testing Z.AI Implementation Imports...")
    
    tests = [
        ('mini_agent.llm.zai_client', 'ZAIClient'),
        ('mini_agent.llm.coding_plan_zai_client', 'CodingPlanZAIClient'),
        ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
    ]
    
    results = {}
    
    for module_path, class_name in tests:
        try:
            module = __import__(module_path, fromlist=[class_name])
            client_class = getattr(module, class_name)
            
            print(f"✅ {class_name}: Import OK")
            
            # Check if class has methods
            methods = [m for m in dir(client_class) if not m.startswith('_') and callable(getattr(client_class, m, None))]
            print(f"   Public methods: {len(methods)}")
            
            results[f'{class_name}'] = {
                'import': 'success',
                'methods_count': len(methods),
                'methods': methods[:3]  # First 3 methods
            }
            
        except Exception as e:
            print(f"❌ {class_name}: {e}")
            results[f'{class_name}'] = {
                'import': 'failed',
                'error': str(e)
            }
    
    return results

def main():
    """Quick health check"""
    print("🚀 Quick Z.AI Health Check")
    print("=" * 30)
    
    # Test config
    config_ok = test_config()
    
    # Test imports
    import_results = test_imports()
    
    print("\n" + "=" * 30)
    print("📊 Results:")
    print(f"   Config: {'✅' if config_ok else '❌'}")
    
    working_count = sum(1 for r in import_results.values() if r['import'] == 'success')
    print(f"   Imports: {working_count}/3 working")
    
    for name, result in import_results.items():
        status = "✅" if result['import'] == 'success' else "❌"
        print(f"     {status} {name}")
    
    # Quick recommendation
    if config_ok and working_count >= 2:
        print(f"\n🎯 READY for consolidation")
    elif config_ok:
        print(f"\n⚠️ Partial readiness - fix imports")
    else:
        print(f"\n❌ Config issues - fix first")
    
    return config_ok, import_results

if __name__ == "__main__":
    main()