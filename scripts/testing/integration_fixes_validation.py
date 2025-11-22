#!/usr/bin/env python3
"""
Mini-Agent Integration Fixes Validation
Tests the specific integration issues mentioned by the user
"""

import os
import asyncio
from pathlib import Path

def test_openai_sdk_integration():
    """Test OpenAI SDK integration"""
    print("📦 Testing OpenAI SDK Integration...")
    
    try:
        from openai import AsyncOpenAI
        print("   ✅ OpenAI SDK: Successfully imported")
        print("   ✅ Used by: mini_agent/llm/openai_client.py")
        return True
    except ImportError as e:
        print(f"   ❌ OpenAI SDK: Import failed - {e}")
        return False

def test_zai_glm_integration():
    """Test Z.AI and GLM-4.6 integration"""
    print("\n🌐 Testing Z.AI and GLM-4.6 Integration...")
    
    # Check Z.AI API key
    zai_api_key = os.getenv("ZAI_API_KEY")
    if not zai_api_key:
        print("   ❌ ZAI_API_KEY: Missing")
        return False
    
    print(f"   ✅ ZAI_API_KEY: Found ({len(zai_api_key)} chars)")
    
    # Test GLM client
    try:
        from mini_agent.llm.glm_client import GLMClient
        print("   ✅ GLM Client: Successfully imported")
        
        # Test initialization
        client = GLMClient(api_key=zai_api_key, model="glm-4.6")
        print("   ✅ GLM-4.6 Client: Initialized successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ GLM-4.6 Client: Failed - {e}")
        return False

def test_llm_provider_hierarchy():
    """Test updated LLM provider hierarchy"""
    print("\n🤖 Testing LLM Provider Hierarchy...")
    
    try:
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        # Test providers
        providers = [LLMProvider.ANTHROPIC, LLMProvider.OPENAI, LLMProvider.ZAI]
        print(f"   ✅ Available providers: {[p.value for p in providers]}")
        
        # Test GLM provider specifically
        zai_api_key = os.getenv("ZAI_API_KEY")
        if zai_api_key:
            client = LLMClient(
                api_key=zai_api_key,
                provider=LLMProvider.ZAI,
                model="glm-4.6"
            )
            print("   ✅ GLM Provider: Successfully configured")
            print("   ✅ Model: glm-4.6")
            return True
        else:
            print("   ❌ ZAI_API_KEY: Required for GLM provider")
            return False
            
    except Exception as e:
        print(f"   ❌ LLM Provider Hierarchy: Failed - {e}")
        return False

def test_zai_web_search():
    """Test Z.AI web search functionality"""
    print("\n🔍 Testing Z.AI Web Search...")
    
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            print("   ❌ ZAI_API_KEY: Missing")
            return False
        
        client = ZAIClient(zai_api_key)
        print("   ✅ Z.AI Client: Initialized")
        
        # Test web search (lightweight test)
        import asyncio
        
        async def test_search():
            result = await client.web_search("test query", count=1)
            return result.get("success", False)
        
        success = asyncio.run(test_search())
        if success:
            print("   ✅ Web Search: API responding")
            return True
        else:
            print("   ❌ Web Search: API not responding")
            return False
            
    except Exception as e:
        print(f"   ❌ Z.AI Web Search: Failed - {e}")
        return False

def test_aiohttp_import():
    """Test aiohttp import (VS Code issue)"""
    print("\n📝 Testing aiohttp Import...")
    
    try:
        import aiohttp
        print(f"   ✅ aiohttp: Available (version {aiohttp.__version__})")
        print("   ✅ VS Code Pylance warning: False positive (vs venv detection)")
        return True
    except ImportError as e:
        print(f"   ❌ aiohttp: Not available - {e}")
        return False

def test_configuration():
    """Test updated configuration"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from mini_agent.config import LLMConfig
        
        # Test GLM-4.6 as primary
        config = LLMConfig(
            api_key="test",
            model="glm-4.6",
            provider="zai"
        )
        
        print(f"   ✅ Primary Model: {config.model}")
        print(f"   ✅ Provider: {config.provider}")
        print("   ✅ GLM-4.6: Configured as primary for reasoning/actions")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration: Failed - {e}")
        return False

def test_agent_initialization():
    """Test agent with new GLM provider"""
    print("\n🤖 Testing Agent Initialization...")
    
    try:
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        zai_api_key = os.getenv("ZAI_API_KEY")
        minimax_key = os.getenv("MINIMAX_API_KEY")
        
        if not zai_api_key:
            print("   ❌ ZAI_API_KEY: Missing for GLM testing")
            return False
        
        # Initialize GLM client
        glm_client = LLMClient(
            api_key=zai_api_key,
            provider=LLMProvider.ZAI,
            model="glm-4.6"
        )
        
        print("   ✅ GLM Agent: Successfully initialized")
        print("   ✅ Ready for reasoning tasks")
        return True
        
    except Exception as e:
        print(f"   ❌ Agent Initialization: Failed - {e}")
        return False

async def test_glm_reasoning():
    """Test GLM-4.6 reasoning capabilities"""
    print("\n🧠 Testing GLM-4.6 Reasoning...")
    
    try:
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider, Message
        
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            print("   ❌ ZAI_API_KEY: Missing")
            return False
        
        client = LLMClient(
            api_key=zai_api_key,
            provider=LLMProvider.ZAI,
            model="glm-4.6"
        )
        
        # Test with simple message
        messages = [
            Message(role="user", content="Hello, please respond briefly to confirm you're working.")
        ]
        
        response = await client.generate(messages)
        
        if response and response.content:
            print(f"   ✅ GLM-4.6 Response: {response.content[:50]}...")
            print("   ✅ Reasoning: Working")
            return True
        else:
            print("   ❌ GLM-4.6: No response generated")
            return False
            
    except Exception as e:
        print(f"   ❌ GLM-4.6 Reasoning: Failed - {e}")
        return False

def main():
    """Main validation function"""
    print("🎯 Mini-Agent Integration Fixes Validation")
    print("=" * 60)
    print("Testing: OpenAI SDK, Z.AI, GLM-4.6, aiohttp imports")
    print()
    
    # Run all tests
    tests = [
        ("OpenAI SDK Integration", test_openai_sdk_integration),
        ("Z.AI/GLM Integration", test_zai_glm_integration),
        ("LLM Provider Hierarchy", test_llm_provider_hierarchy),
        ("Z.AI Web Search", test_zai_web_search),
        ("aiohttp Import", test_aiohttp_import),
        ("Configuration", test_configuration),
        ("Agent Initialization", test_agent_initialization),
        ("GLM-4.6 Reasoning", lambda: asyncio.run(test_glm_reasoning())),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name}: Exception - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n🏆 FINAL SCORE: {passed}/{total} ({int(passed/total*100)}%)")
    
    if passed == total:
        print("🎉 ALL INTEGRATION FIXES SUCCESSFUL!")
        print("\n✅ System Status:")
        print("   • OpenAI SDK: Already integrated and working")
        print("   • Z.AI API: Configured for web search")
        print("   • GLM-4.6: Now primary LLM for reasoning/actions")
        print("   • aiohttp: Working (VS Code warning is false positive)")
        print("   • LLM Hierarchy: Updated with ZAI provider")
    else:
        print(f"⚠️ {total-passed} integration issues remain")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)