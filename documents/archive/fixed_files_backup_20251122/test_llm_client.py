#!/usr/bin/env python3
"""
Test LLM Client initialization and API call
This will help identify if the issue is with API calls or just config loading
"""

import os
import sys
import traceback
from pathlib import Path

# Add the current directory to Python path so we can import mini_agent
sys.path.insert(0, str(Path.cwd() / "mini_agent"))

def test_llm_client():
    """Test LLM client initialization and API call"""
    print("=== Testing LLM Client ===")
    
    try:
        # Import mini_agent components
        from mini_agent.config import Config
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        print("✅ Imported mini_agent components successfully")
        
        # Load configuration
        print("\n📝 Loading configuration...")
        config = Config.load()
        print("✅ Configuration loaded successfully")
        
        # Display config details for debugging
        print(f"API Key loaded: {bool(config.llm.api_key)}")
        print(f"API Base: {config.llm.api_base}")
        print(f"Model: {config.llm.model}")
        print(f"Provider: {config.llm.provider}")
        print(f"API Key length: {len(config.llm.api_key) if config.llm.api_key else 0}")
        print(f"API Key starts with: {config.llm.api_key[:20] if config.llm.api_key else 'None'}...")
        
        # Initialize LLM client
        print("\n🔧 Initializing LLM client...")
        provider = LLMProvider.ANTHROPIC if config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI
        print(f"Using provider: {provider}")
        
        llm_client = LLMClient(
            api_key=config.llm.api_key,
            provider=provider,
            api_base=config.llm.api_base,
            model=config.llm.model,
        )
        print("✅ LLM client initialized successfully")
        
        # Test a simple API call
        print("\n🧪 Testing API call...")
        from mini_agent.schema import Message
        
        test_messages = [
            Message(role="user", content="Say 'Hello, MiniMax!' if you can hear me.")
        ]
        
        print("Sending test message...")
        response = llm_client.chat(test_messages)
        
        print("✅ API call successful!")
        print(f"Response: {response.content}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False
        
    except Exception as e:
        print(f"❌ Error during LLM client test: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Mini-Agent LLM Client Test")
    print("=" * 50)
    
    success = test_llm_client()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 LLM Client test PASSED - API calls are working!")
        print("The issue is likely elsewhere (maybe in your enhanced server code)")
    else:
        print("💥 LLM Client test FAILED - Found the root cause!")
        print("The API authentication/configuration is still broken")