#!/usr/bin/env python3
"""
Simple Z.AI Connectivity Test
Tests basic API connectivity before MCP testing
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mini_agent.config.config import Config

def test_zai_api_connectivity():
    """Test basic Z.AI API connectivity"""
    print("🔍 Testing Z.AI API Connectivity...")
    
    try:
        config = Config()
        
        # Check API key
        if not config.zai_api_key:
            print("❌ Z.AI API Key: Missing")
            return False
        
        print(f"✅ Z.AI API Key: Present (length: {len(config.zai_api_key)})")
        
        # Test basic endpoint
        import requests
        
        headers = {
            'Authorization': f'Bearer {config.zai_api_key}',
            'Content-Type': 'application/json'
        }
        
        # Simple test endpoint
        test_url = 'https://api.z.ai/api/coding/paas/v4/models'
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Z.AI API: Working (Status: {response.status_code})")
                models = response.json()
                print(f"   Available models: {len(models.get('data', []))}")
                return True
            else:
                print(f"❌ Z.AI API: Error (Status: {response.status_code})")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Z.AI API: Connection failed - {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Z.AI Test: Exception - {str(e)}")
        return False

def test_current_implementations():
    """Test current working implementations"""
    print("\n🔍 Testing Current Implementations...")
    
    implementations = [
        ('mini_agent.llm.zai_client', 'ZAIClient'),
        ('mini_agent.llm.coding_plan_zai_client', 'CodingPlanZAIClient'),
        ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
    ]
    
    results = {}
    
    for module_path, class_name in implementations:
        try:
            print(f"   Testing {class_name}...")
            module = __import__(module_path, fromlist=[class_name])
            client_class = getattr(module, class_name)
            
            # Test class attributes
            if hasattr(client_class, '__init__'):
                print(f"   ✅ {class_name}: Import and class access successful")
                results[f'{module_path}_{class_name}'] = {
                    'status': 'working',
                    'has_init': True,
                    'class_methods': [method for method in dir(client_class) if not method.startswith('_')][:5]
                }
            else:
                print(f"   ⚠️ {class_name}: Import successful but no __init__")
                results[f'{module_path}_{class_name}'] = {
                    'status': 'imported_no_init',
                    'methods': [method for method in dir(client_class) if not method.startswith('_')][:5]
                }
                
        except Exception as e:
            print(f"   ❌ {class_name}: Failed - {str(e)}")
            results[f'{module_path}_{class_name}'] = {
                'status': 'failed',
                'error': str(e)
            }
    
    return results

def main():
    """Main test execution"""
    print("🚀 Z.AI System Health Check")
    print("=" * 40)
    
    # Test basic connectivity
    api_working = test_zai_api_connectivity()
    
    # Test implementations
    implementations = test_current_implementations()
    
    print("\n" + "=" * 40)
    print("📊 Summary:")
    print(f"   • Z.AI API: {'✅ Working' if api_working else '❌ Failed'}")
    
    working_impls = [name for name, result in implementations.items() if result['status'] == 'working']
    print(f"   • Working Implementations: {len(working_impls)}/3")
    for impl in working_impls:
        print(f"     - {impl.split('.')[-1]}")
    
    if api_working and working_impls:
        print(f"\n🎯 Status: READY for Phase 1 Consolidation")
        print(f"   • API connectivity confirmed")
        print(f"   • {len(working_impls)} implementation(s) operational")
    elif api_working:
        print(f"\n⚠️ Status: API working but implementations need fixing")
    else:
        print(f"\n❌ Status: Z.AI connectivity issues")
    
    # Save detailed results
    import json
    results = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'api_connectivity': api_working,
        'implementations': implementations,
        'ready_for_consolidation': api_working and len(working_impls) >= 2
    }
    
    with open('ZAI_HEALTH_CHECK.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: ZAI_HEALTH_CHECK.json")

if __name__ == "__main__":
    main()