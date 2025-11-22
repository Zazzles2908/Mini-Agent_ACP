#!/usr/bin/env python3

# Test script to verify imports work
print("Testing mini-agent imports...")

try:
    import sys
    sys.path.insert(0, '/workspace')
    
    print("Step 1: Importing schema...")
    from mini_agent.schema import LLMProvider, Message, LLMResponse
    print("✓ Schema imports successful")
    
    print("Step 2: Creating a test message...")
    test_msg = Message(role="user", content="Hello")
    print(f"✓ Message created: {test_msg}")
    
    print("Step 3: Testing LLMResponse...")
    test_response = LLMResponse(content="Hello!", finish_reason="stop")
    print(f"✓ LLMResponse created: {test_response}")
    
    print("Step 4: Importing other modules...")
    from mini_agent.llm import LLMClient
    from mini_agent.agent import Agent
    from mini_agent import Config
    print("✓ All modules imported successfully")
    
    print("\n🎉 SUCCESS! All import errors have been fixed!")
    print("The mini-agent should now work correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    print("\nThere may still be an issue that needs to be resolved.")