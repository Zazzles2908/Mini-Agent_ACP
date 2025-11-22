#!/usr/bin/env python3
"""Debug script to trace Mini-Agent LLM client initialization."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mini_agent.llm.llm_wrapper import LLMClient
from mini_agent.schema import LLMProvider

def debug_llm_client():
    """Debug LLM client initialization to find the root cause."""
    
    print("🔍 Debugging LLM Client Initialization")
    print("=" * 50)
    
    # Check environment
    zai_api_key = os.getenv("ZAI_API_KEY")
    if zai_api_key:
        print(f"✅ ZAI_API_KEY: {zai_api_key[:10]}...")
    else:
        print("❌ ZAI_API_KEY: Missing")
        return
    
    # Check configuration
    config_file = Path("mini_agent/config/config.yaml")
    if config_file.exists():
        print("✅ config.yaml: Found")
        import yaml
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        print(f"   Provider: {config.get('provider')}")
        print(f"   Model: {config.get('model')}")
        print(f"   API Base: {config.get('api_base')}")
    else:
        print("❌ config.yaml: Missing")
        return
    
    print("\n🔧 Testing LLM Client Initialization...")
    
    try:
        # Try to initialize with configuration values
        client = LLMClient(
            api_key=zai_api_key,
            provider=LLMProvider.ZAI,
            model="glm-4.6"
        )
        
        print("✅ LLM Client initialized successfully")
        print(f"   Provider: {client.provider}")
        print(f"   API Base: {client.api_base}")
        print(f"   Model: {client.model}")
        print(f"   Client Type: {type(client._client)}")
        
        # Check if the correct client was instantiated
        from mini_agent.llm.glm_client import GLMClient
        if isinstance(client._client, GLMClient):
            print("✅ Correct client: GLMClient instantiated")
        else:
            print(f"❌ Wrong client: {type(client._client)} instantiated")
            
    except Exception as e:
        print(f"❌ LLM Client initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🧪 Testing API Call...")
    
    try:
        import asyncio
        from mini_agent.schema import Message
        
        async def test_api():
            messages = [Message(role="user", content="Hello")]
            result = await client.generate(messages)
            return result
        
        result = asyncio.run(test_api())
        
        print(f"✅ API Call successful")
        print(f"   Finish reason: {result.finish_reason}")
        print(f"   Response: {result.content[:100]}...")
        
    except Exception as e:
        print(f"❌ API Call failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_llm_client()