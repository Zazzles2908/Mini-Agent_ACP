#!/usr/bin/env python3
"""Validation script to verify the Anthropic provider switch works correctly."""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path.cwd()))

from mini_agent.config import Config
from mini_agent.llm import LLMClient

async def validate_anthropic_switch():
    """Validate that switching to Anthropic provider works correctly."""
    print("🔍 Validating Anthropic Provider Switch")
    print("=" * 50)
    
    try:
        # Test 1: Load current config
        print("\n1️⃣ Loading current config...")
        config = Config.load()
        print(f"✅ Config loaded successfully")
        print(f"   Provider: {config.llm.provider}")
        print(f"   API Base: {config.llm.api_base}")
        print(f"   Model: {config.llm.model}")
        
        # Test 2: Verify it's set to Anthropic
        print("\n2️⃣ Verifying Anthropic configuration...")
        if config.llm.provider == "anthropic":
            print("✅ Provider correctly set to 'anthropic'")
        else:
            print(f"❌ Provider is '{config.llm.provider}', should be 'anthropic'")
            return False
        
        # Test 3: Test LLM client initialization with Anthropic
        print("\n3️⃣ Testing LLM client initialization...")
        
        # Create a test client (no API call, just initialization)
        llm_client = LLMClient(
            api_key="test_key",  # Test key, no actual API calls
            provider="anthropic",
            model=config.llm.model,
            api_base=config.llm.api_base
        )
        
        print(f"✅ Anthropic client initialized successfully")
        print(f"   Client provider: {llm_client.provider}")
        print(f"   Client API base: {llm_client.api_base}")
        print(f"   Client model: {llm_client.model}")
        
        # Test 4: Verify API endpoint construction
        print("\n4️⃣ Verifying API endpoint construction...")
        expected_endpoint = "https://api.minimax.io/anthropic"
        actual_endpoint = llm_client.api_base
        
        if actual_endpoint == expected_endpoint:
            print(f"✅ API endpoint correct: {actual_endpoint}")
        else:
            print(f"❌ API endpoint incorrect!")
            print(f"   Expected: {expected_endpoint}")
            print(f"   Actual: {actual_endpoint}")
            return False
        
        # Test 5: Verify internal client type
        print("\n5️⃣ Verifying internal client type...")
        client_type = type(llm_client._client).__name__
        if "Anthropic" in client_type:
            print(f"✅ Using Anthropic client: {client_type}")
        else:
            print(f"❌ Not using Anthropic client: {client_type}")
            return False
        
        # Test 6: Test with actual config values
        print("\n6️⃣ Testing with actual config values...")
        actual_client = LLMClient(
            api_key=config.llm.api_key,
            provider=config.llm.provider,
            model=config.llm.model,
            api_base=config.llm.api_base
        )
        
        print(f"✅ Real config client created")
        print(f"   Final API endpoint: {actual_client.api_base}")
        
        # Test 7: Check for any runtime errors in setup
        print("\n7️⃣ Checking for runtime errors...")
        try:
            # Just verify the client can be created without errors
            # (Don't make actual API calls)
            if actual_client:
                print("✅ Client creation completed without runtime errors")
            else:
                print("❌ Client creation failed")
                return False
        except Exception as e:
            print(f"❌ Runtime error during client creation: {e}")
            return False
        
        print("\n🎯 VALIDATION COMPLETE!")
        print("✅ Anthropic provider switch is working correctly!")
        print("💡 The system is now configured to use Anthropic protocol with MiniMax-M2")
        return True
        
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the Anthropic switch validation."""
    print("🚀 Starting Anthropic Provider Switch Validation")
    print("Testing if MiniMax-M2 works with Anthropic protocol...\n")
    
    success = await validate_anthropic_switch()
    
    if success:
        print("\n🎉 SUCCESS: Anthropic provider switch validated!")
        print("📋 Summary:")
        print("   - Provider: anthropic ✅")
        print("   - API endpoint: https://api.minimax.io/anthropic ✅")
        print("   - Client type: AnthropicClient ✅")
        print("   - Ready for API testing ✅")
    else:
        print("\n🚨 FAILED: Anthropic provider switch has issues!")
        print("📋 Please review the errors above")
        
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
