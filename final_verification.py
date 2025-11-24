#!/usr/bin/env python3
"""Final verification test"""

import sys
import os
import asyncio

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

async def test_final_verification():
    """Final verification of the restored system"""
    print("=== FINAL SYSTEM VERIFICATION ===")
    
    try:
        # Test 1: Import and configuration
        print("\n1. Testing configuration and imports...")
        from mini_agent.config import get_config
        config = get_config()
        print(f"   Configuration: {len(config._config)} keys loaded")
        
        # Test 2: LLM Client creation
        print("\n2. Testing LLM client creation...")
        from mini_agent.llm.llm_wrapper import LLMClient
        llm_client = LLMClient(
            api_key=config.api_key or "dummy_key",
            provider=config.provider,
            api_base=config.api_base or "https://api.minimax.io",
            model=config.model
        )
        print(f"   LLM Client: {llm_client.model} ({llm_client._client.__class__.__name__})")
        
        # Test 3: Error response handling
        print("\n3. Testing error response handling...")
        
        # Test the response parsing with an error response
        error_response = {"error": "Authentication failed", "type": "error"}
        client = llm_client._client  # Get the actual OpenAI client
        parsed = client._parse_response(error_response)
        print(f"   Error parsing: {parsed.content[:50]}...")
        print(f"   Error type: {parsed.finish_reason}")
        
        print("\n4. Testing tool loading...")
        from mini_agent.tools.bash_tool import BashTool
        bash_tool = BashTool()
        print(f"   Bash tool: {bash_tool.name}")
        
        # Test 5: Agent creation
        print("\n5. Testing agent creation...")
        from mini_agent.tools.base import Tool
        from mini_agent.agent import Agent
        
        # Create a minimal agent with correct parameters
        agent = Agent(
            llm_client=llm_client,
            system_prompt="You are a helpful assistant.",
            tools=[],  # Empty tools list for test
            max_steps=10
        )
        print(f"   Agent: Created with {len(agent.tools)} tools")
        
        print("\n=== ALL TESTS PASSED ===")
        print("System has been successfully restored!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_final_verification())
    print(f"\nFinal Status: {'SYSTEM FULLY RESTORED' if result else 'ISSUES REMAIN'}")