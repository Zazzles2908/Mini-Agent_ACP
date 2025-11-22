#!/usr/bin/env python3
"""
Test script to verify authentication and import fixes
"""

import sys
import os
from pathlib import Path

def test_dotenv_loading():
    """Test .env file loading"""
    print("🔍 Testing .env file loading...")
    
    from dotenv import load_dotenv
    env_file = Path.cwd() / ".env"
    
    if env_file.exists():
        load_dotenv(env_file, override=False)
        print(f"✅ .env file loaded from: {env_file}")
        
        minimax_key = os.getenv('MINIMAX_API_KEY')
        zai_key = os.getenv('ZAI_API_KEY')
        
        if minimax_key:
            print(f"✅ MINIMAX_API_KEY found ({len(minimax_key)} characters)")
        else:
            print("❌ MINIMAX_API_KEY not found")
            return False
            
        if zai_key:
            print(f"✅ ZAI_API_KEY found ({len(zai_key)} characters)")
        else:
            print("❌ ZAI_API_KEY not found")
            return False
    else:
        print("❌ .env file not found")
        return False
    
    return True

def test_config_loading():
    """Test configuration loading with environment substitution"""
    print("\n🔍 Testing configuration loading...")
    
    try:
        from mini_agent.config import Config
        config = Config.load()
        
        print("✅ Configuration loaded successfully")
        print(f"   API Base: {config.llm.api_base}")
        print(f"   Model: {config.llm.model}")
        print(f"   Provider: {config.llm.provider}")
        
        # Check if API key was substituted
        api_key = config.llm.api_key
        if api_key.startswith('${'):
            print(f"❌ API key not substituted: {api_key}")
            return False
        else:
            print(f"✅ API key properly substituted ({len(api_key)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_client():
    """Test LLM client initialization"""
    print("\n🔍 Testing LLM client initialization...")
    
    try:
        from mini_agent.config import Config
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        config = Config.load()
        
        provider = LLMProvider.ANTHROPIC if config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI
        
        llm_client = LLMClient(
            api_key=config.llm.api_key,
            provider=provider,
            api_base=config.llm.api_base,
            model=config.llm.model,
        )
        
        print("✅ LLM client initialized successfully")
        print(f"   Provider: {provider}")
        print(f"   API Base: {config.llm.api_base}")
        print(f"   Model: {config.llm.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM client initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_zai_client():
    """Test ZAI client imports"""
    print("\n🔍 Testing ZAI client imports...")
    
    try:
        from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
        
        # Check aiohttp availability
        import mini_agent.llm.zai_client as zai_module
        aiohttp_available = zai_module.AIOHTTP_AVAILABLE
        
        print("✅ ZAI client imports successfully")
        print(f"   aiohttp available: {aiohttp_available}")
        
        if aiohttp_available:
            # Test ZAI client instantiation
            zai_api_key = get_zai_api_key()
            if zai_api_key:
                zai_client = ZAIClient(zai_api_key)
                print("✅ ZAI client instantiated successfully")
                print(f"   Available models: {list(zai_client.models.keys())}")
            else:
                print("⚠️  ZAI_API_KEY not found in environment")
        else:
            print("⚠️  aiohttp not available - ZAI tools will not work")
        
        return True
        
    except Exception as e:
        print(f"❌ ZAI client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔧 Mini-Agent Authentication & Import Fix Verification")
    print("=" * 60)
    
    tests = [
        ("Environment Loading", test_dotenv_loading),
        ("Configuration Loading", test_config_loading),
        ("LLM Client", test_llm_client),
        ("ZAI Client", test_zai_client),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational! Authentication and import issues resolved.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
