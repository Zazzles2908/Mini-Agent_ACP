#!/usr/bin/env python3
"""
Simple Production System Test
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_config_basics():
    """Test basic configuration functionality"""
    print("🧪 TESTING PRODUCTION CONFIGURATION SYSTEM")
    print("=" * 45)
    
    try:
        from mini_agent.config import get_config
        
        # Load configuration
        config = get_config()
        print("✅ Configuration loaded successfully")
        
        # Test basic values
        app_name = config.get("app.name")
        llm_provider = config.get("llm.provider")
        max_tokens = config.get("llm.max_tokens")
        
        print(f"   📱 App name: {app_name}")
        print(f"   🤖 LLM provider: {llm_provider}")
        print(f"   🔢 Max tokens: {max_tokens}")
        
        # Test environment override
        print("\n2. Testing environment variable override...")
        os.environ['MINIMAX_API_KEY'] = 'test_key_12345'
        os.environ['MINIMAX_DEBUG'] = 'true'
        
        # Reset and reload
        from mini_agent.config import reset_config
        reset_config()
        config = get_config()
        
        api_key = config.get('MINIMAX_API_KEY')
        debug = config.get('MINIMAX_DEBUG')
        
        if api_key:
            print(f"   🔑 API key (env): {api_key[:10]}...")
        else:
            print("   ⚠️  API key (env): None")
            
        print(f"   🔧 Debug (env): {debug}")
        
        # Health check
        print("\n3. Running health check...")
        health = config.health_check()
        print(f"   🏥 Health status: {health['status']}")
        print(f"   📁 Config loaded: {health['config_loaded']}")
        
        if health.get('errors'):
            print(f"   ❌ Errors: {health['errors']}")
        
        if health.get('warnings'):
            print(f"   ⚠️  Warnings: {health['warnings']}")
        
        print("\n✅ CONFIGURATION SYSTEM WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_factory():
    """Test agent factory (basic)"""
    print("\n🤖 TESTING AGENT FACTORY")
    print("=" * 25)
    
    try:
        from mini_agent.agent_factory import AgentFactory
        
        factory = AgentFactory()
        print("✅ AgentFactory initialized successfully")
        
        # Just test that it can be created
        info = factory.get_agent_info.__doc__
        if info:
            print("   📚 Factory methods available")
        
        print("✅ AGENT FACTORY WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Agent factory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_tools():
    """Test MCP tools loading"""
    print("\n🔌 TESTING MCP TOOLS LOADING")
    print("=" * 32)
    
    try:
        import asyncio
        from mini_agent.tools.mcp_loader import load_mcp_tools_async
        
        # Test MCP loading
        async def test_mcp():
            tools = await load_mcp_tools_async('mini_agent/config/.mcp.json')
            return len(tools)
        
        tool_count = asyncio.run(test_mcp())
        print(f"✅ MCP tools loaded: {tool_count} tools")
        return True
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 PRODUCTION SYSTEM VALIDATION")
    print("=" * 40)
    
    results = []
    
    # Test configuration
    results.append(test_config_basics())
    
    # Test agent factory
    results.append(test_agent_factory())
    
    # Test MCP tools
    results.append(test_mcp_tools())
    
    print("\n" + "=" * 40)
    print("📊 FINAL RESULTS")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Production system is functional")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("⚠️  Some issues need to be resolved")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
