#!/usr/bin/env python3
"""Final system audit for Mini-Agent with GLM-4.6 integration."""

import asyncio
import os
import sys
from pathlib import Path
import importlib.util

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Check environment setup."""
    print("🔧 Environment Check...")
    
    # Python venv
    if Path(".venv").exists():
        print("✅ Python virtual environment (.venv) exists")
    else:
        print("❌ Python virtual environment (.venv) missing")
        return False
    
    # Package manager
    if Path(".venv/Scripts/uv.exe").exists() or Path(".venv/bin/uv").exists():
        print("✅ uv package manager available")
    else:
        print("❌ uv package manager missing")
        return False
    
    # API keys
    zai_api_key = os.getenv("ZAI_API_KEY")
    if zai_api_key:
        print(f"✅ ZAI_API_KEY found: {zai_api_key[:10]}...")
    else:
        print("❌ ZAI_API_KEY environment variable missing")
        return False
    
    return True

def check_dependencies():
    """Check required dependencies."""
    print("\n📦 Dependencies Check...")
    
    required_packages = [
        "aiohttp",
        "anthropic", 
        "openai",
        "pydantic",
        "pyyaml",
        "httpx",
        "requests"
    ]
    
    all_good = True
    for package in required_packages:
        try:
            spec = importlib.util.find_spec(package)
            if spec:
                print(f"✅ {package} available")
            else:
                print(f"❌ {package} missing")
                all_good = False
        except Exception:
            print(f"❌ {package} check failed")
            all_good = False
    
    return all_good

async def check_glm_integration():
    """Check GLM-4.6 integration."""
    print("\n🧠 GLM-4.6 Integration Check...")
    
    try:
        from mini_agent.llm.glm_client import GLMClient
        from mini_agent.schema import Message
        
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            return False
        
        # Initialize client
        glm_client = GLMClient(
            api_key=zai_api_key,
            model="glm-4.6"
        )
        print("✅ GLMClient initialized")
        
        # Test API call
        messages = [Message(role="user", content="Say hello")]
        result = await glm_client.generate(messages)
        
        if result.finish_reason == "stop" and result.content:
            print("✅ GLM-4.6 API call successful")
            print(f"   Response: {result.content[:100]}...")
            return True
        else:
            print("❌ GLM-4.6 API call failed")
            return False
            
    except Exception as e:
        print(f"❌ GLM integration check failed: {e}")
        return False

async def check_llm_wrapper():
    """Check LLM wrapper integration."""
    print("\n🔗 LLM Wrapper Check...")
    
    try:
        from mini_agent.llm.llm_wrapper import LLMClient
        from mini_agent.schema import Message, LLMProvider
        
        zai_api_key = os.getenv("ZAI_API_KEY")
        if not zai_api_key:
            return False
        
        # Initialize wrapper
        llm_client = LLMClient(
            api_key=zai_api_key,
            provider=LLMProvider.ZAI,
            model="glm-4.6"
        )
        print("✅ LLM wrapper initialized")
        
        # Test through wrapper
        messages = [Message(role="user", content="What is GLM?")]
        result = await llm_client.generate(messages)
        
        if result.finish_reason == "stop" and result.content:
            print("✅ LLM wrapper API call successful")
            print(f"   Response: {result.content[:100]}...")
            return True
        else:
            print("❌ LLM wrapper API call failed")
            return False
            
    except Exception as e:
        print(f"❌ LLM wrapper check failed: {e}")
        return False

def check_configuration():
    """Check configuration files."""
    print("\n⚙️ Configuration Check...")
    
    config_file = Path("mini_agent/config/config.yaml")
    if config_file.exists():
        print("✅ config.yaml exists")
    else:
        print("❌ config.yaml missing")
        return False
    
    try:
        import yaml
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check key settings
        if config.get('provider') == 'zai':
            print("✅ Provider set to 'zai'")
        else:
            print(f"❌ Provider is '{config.get('provider')}', should be 'zai'")
            return False
            
        if config.get('model') == 'glm-4.6':
            print("✅ Model set to 'glm-4.6'")
        else:
            print(f"❌ Model is '{config.get('model')}', should be 'glm-4.6'")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

async def main():
    """Main audit function."""
    print("🚀 Mini-Agent System Audit")
    print("=" * 50)
    
    checks = [
        ("Environment", check_environment()),
        ("Dependencies", check_dependencies()),
        ("GLM Integration", await check_glm_integration()),
        ("LLM Wrapper", await check_llm_wrapper()),
        ("Configuration", check_configuration())
    ]
    
    print("\n" + "=" * 50)
    print("📊 AUDIT RESULTS")
    print("=" * 50)
    
    passed = 0
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:15} {status}")
        if result:
            passed += 1
    
    total = len(checks)
    percentage = (passed / total) * 100
    
    print(f"\nOverall Score: {passed}/{total} ({percentage:.1f}%)")
    
    if percentage >= 100:
        print("\n🎉 EXCELLENT! System is production ready!")
        print("✅ Mini-Agent with GLM-4.6 is fully functional")
    elif percentage >= 80:
        print("\n👍 GOOD! Minor issues detected")
        print("⚠️ System mostly functional, minor setup needed")
    else:
        print("\n⚠️ ISSUES DETECTED! Major problems need fixing")
        print("❌ System not ready for production use")
    
    return percentage >= 80

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)