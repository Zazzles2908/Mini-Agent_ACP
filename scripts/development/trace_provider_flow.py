#!/usr/bin/env python3
"""Trace the actual provider switching interconnection flow to find the real break."""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path.cwd()))

def trace_provider_flow():
    """Trace how provider setting flows through the system."""
    print("🔍 Tracing Actual Provider Switching Interconnection Flow")
    print("=" * 70)
    
    try:
        # Step 1: Load config.yaml
        print("\n1️⃣ STEP 1: Loading config.yaml...")
        from mini_agent.config import Config
        config = Config.load()
        
        print(f"   ✅ Config loaded successfully")
        print(f"   📋 Raw config.yaml provider: {config.llm.provider}")
        print(f"   📋 Config type: {type(config.llm.provider)}")
        print(f"   📋 API base: {config.llm.api_base}")
        print(f"   📋 Model: {config.llm.model}")
        
        # Step 2: Trace to CLI provider conversion
        print(f"\n2️⃣ STEP 2: CLI provider conversion...")
        
        # This is what cli.py does
        config_provider = config.llm.provider.lower()
        cli_provider = "LLMProvider.ANTHROPIC" if config_provider == "anthropic" else "LLMProvider.OPENAI"
        
        print(f"   📋 Config provider: {config.llm.provider}")
        print(f"   📋 CLI resolution: {config_provider} -> {cli_provider}")
        
        # Step 3: Test LLMClient initialization
        print(f"\n3️⃣ STEP 3: LLMClient initialization...")
        
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        # Test with actual enum from CLI
        provider_enum = LLMProvider.ANTHROPIC if config_provider == "anthropic" else LLMProvider.OPENAI
        
        print(f"   📋 Provider enum: {provider_enum}")
        print(f"   📋 Provider value: {provider_enum.value}")
        
        # Initialize LLMClient
        llm_client = LLMClient(
            api_key=config.llm.api_key,
            provider=provider_enum,
            api_base=config.llm.api_base,
            model=config.llm.model,
        )
        
        print(f"   ✅ LLMClient created successfully")
        print(f"   📋 Client type: {type(llm_client._client).__name__}")
        print(f"   📋 Client provider: {llm_client.provider}")
        print(f"   📋 API endpoint: {llm_client.api_base}")
        
        # Step 4: Verify the client selection
        print(f"\n4️⃣ STEP 4: Client selection verification...")
        
        if config.llm.provider.lower() == "anthropic":
            expected_client = "AnthropicClient"
            expected_api = f"{config.llm.api_base.rstrip('/')}/anthropic"
        else:
            expected_client = "OpenAIClient"
            expected_api = f"{config.llm.api_base.rstrip('/')}/v1"
            
        actual_client = type(llm_client._client).__name__
        
        print(f"   📋 Expected: {expected_client}")
        print(f"   📋 Actual: {actual_client}")
        print(f"   📋 API expected: {expected_api}")
        print(f"   📋 API actual: {llm_client.api_base}")
        
        if actual_client == expected_client and llm_client.api_base == expected_api:
            print(f"   ✅ Provider switching working correctly!")
            return True
        else:
            print(f"   ❌ Provider switching broken!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error in provider flow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_import_impact():
    """Test if schema imports are actually affecting the flow."""
    print(f"\n🔍 SCHEMA IMPORT IMPACT ANALYSIS")
    print("=" * 50)
    
    try:
        # Test if schema imports work
        from mini_agent.schema import LLMProvider, Message, LLMResponse
        print(f"   ✅ Schema imports working")
        print(f"   📋 LLMProvider: {LLMProvider}")
        
        # Test if different files can import consistently
        from mini_agent.config import Config
        from mini_agent.llm import LLMClient
        
        print(f"   ✅ All imports consistent")
        return True
        
    except Exception as e:
        print(f"   ❌ Schema import issue: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Provider Flow Interconnection Analysis")
    
    # Test the actual flow
    flow_success = trace_provider_flow()
    
    # Test schema import impact
    import_success = test_schema_import_impact()
    
    print(f"\n📋 ANALYSIS RESULTS:")
    print(f"   Provider Flow: {'✅ Working' if flow_success else '❌ Broken'}")
    print(f"   Schema Imports: {'✅ Working' if import_success else '❌ Broken'}")
    
    if flow_success:
        print(f"\n🎯 CONCLUSION: Provider switching flow is working!")
        print(f"💡 The issue might be in authentication, not interconnection")
    else:
        print(f"\n🔍 CONCLUSION: Found the break in provider switching flow!")
        
    sys.exit(0 if flow_success else 1)
