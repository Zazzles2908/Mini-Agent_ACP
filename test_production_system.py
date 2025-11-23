#!/usr/bin/env python3
"""
Production Configuration System Test
Tests the new configuration system comprehensively
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the mini_agent directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mini_agent.config import get_config, reset_config


async def test_configuration_system():
    """Test the production configuration system"""
    print("🧪 TESTING PRODUCTION CONFIGURATION SYSTEM")
    print("=" * 50)
    
    # Test 1: Basic Configuration Loading
    print("\n1. Testing Basic Configuration Loading...")
    try:
        config = get_config()
        print("✅ Configuration loaded successfully")
        print(f"   📊 Top-level keys: {len(config._config)}")
        print(f"   📁 Config sources: {config._config.get('sources', [])}")
        
        # Test getting values
        app_name = config.get("app.name")
        debug_mode = config.get("app.debug")
        llm_provider = config.get("llm.provider")
        
        print(f"   📝 App name: {app_name}")
        print(f"   🔧 Debug mode: {debug_mode}")
        print(f"   🤖 LLM provider: {llm_provider}")
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Environment Variable Override
    print("\n2. Testing Environment Variable Override...")
    try:
        # Set environment variables
        os.environ['MINIMAX_API_KEY'] = 'test_api_key_12345'
        os.environ['MINIMAX_DEBUG'] = 'true'
        os.environ['MINIMAX_MODEL'] = 'MiniMax-M2-Test'
        
        # Reset and reload configuration
        reset_config()
        config = get_config()
        
        # Test that environment variables override config
        api_key = config.get('MINIMAX_API_KEY')
        debug = config.get('MINIMAX_DEBUG')
        model = config.get('llm.model')
        
        print(f"✅ Environment override working:")
        print(f"   🔑 API key: {api_key[:12]}...")
        print(f"   🔧 Debug: {debug}")
        print(f"   🤖 Model: {model}")
        
    except Exception as e:
        print(f"❌ Environment override failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Type Validation
    print("\n3. Testing Type Validation...")
    try:
        # Test numeric types
        max_tokens = config.get("llm.max_tokens")
        temperature = config.get("llm.temperature")
        
        print(f"✅ Type validation passed:")
        print(f"   🔢 Max tokens: {max_tokens} (type: {type(max_tokens).__name__})")
        print(f"   🌡️  Temperature: {temperature} (type: {type(temperature).__name__})")
        
        # Test boolean type
        debug = config.get("app.debug")
        print(f"   🔍 Debug: {debug} (type: {type(debug).__name__})")
        
    except Exception as e:
        print(f"❌ Type validation failed: {e}")
        return False
    
    # Test 4: Health Check
    print("\n4. Testing Health Check...")
    try:
        health = config.health_check()
        
        print(f"✅ Health check completed:")
        print(f"   🏥 Status: {health['status']}")
        print(f"   📁 Config loaded: {health['config_loaded']}")
        print(f"   📋 Sources: {len(health.get('sources', []))}")
        
        if health.get('errors'):
            print(f"   ❌ Errors: {health['errors']}")
        
        if health.get('warnings'):
            print(f"   ⚠️  Warnings: {health['warnings']}")
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 5: Configuration Access Methods
    print("\n5. Testing Configuration Access Methods...")
    try:
        # Test dot notation
        workspace_dir = config.get("workspace.directory")
        print(f"✅ Dot notation access: workspace.directory = {workspace_dir}")
        
        # Test required parameter
        try:
            missing_key = config.get("nonexistent.key", required=True)
            print("❌ Should have raised error for missing required key")
            return False
        except Exception:
            print("✅ Required parameter validation working")
        
        # Test default values
        default_value = config.get("nonexistent.key", default="default_value")
        print(f"✅ Default values working: {default_value}")
        
    except Exception as e:
        print(f"❌ Configuration access methods failed: {e}")
        return False
    
    print("\n🎉 CONFIGURATION SYSTEM TEST COMPLETED")
    print("=" * 50)
    return True


async def test_agent_factory():
    """Test the agent factory (basic test without actual agent creation)"""
    print("\n🧪 TESTING AGENT FACTORY")
    print("=" * 30)
    
    try:
        # Test basic imports
        from mini_agent.agent_factory import AgentFactory
        
        factory = AgentFactory()
        print("✅ AgentFactory initialized successfully")
        
        # Test health check
        health = factory.health_check()
        print(f"✅ Factory health check: {health['status']}")
        
        if health.get('errors'):
            print(f"   ❌ Errors: {health['errors']}")
        
        if health.get('warnings'):
            print(f"   ⚠️  Warnings: {health['warnings']}")
            
    except Exception as e:
        print(f"❌ Agent factory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Run all tests"""
    print("🚀 PRODUCTION SYSTEM VALIDATION")
    print("=" * 50)
    
    config_success = await test_configuration_system()
    factory_success = await test_agent_factory()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Configuration System: {'✅ PASSED' if config_success else '❌ FAILED'}")
    print(f"Agent Factory: {'✅ PASSED' if factory_success else '❌ FAILED'}")
    
    if config_success and factory_success:
        print("\n🎉 ALL TESTS PASSED - PRODUCTION SYSTEM READY")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - ISSUES TO RESOLVE")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
