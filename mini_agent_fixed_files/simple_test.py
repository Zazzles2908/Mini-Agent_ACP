#!/usr/bin/env python3

print("Starting simple import test...")

try:
    print("Importing mini_agent...")
    from mini_agent.schema import LLMProvider, Message, LLMResponse
    print("✓ Schema imports successful")
    
    print("Importing LLMClient...")
    from mini_agent.llm import LLMClient
    print("✓ LLMClient import successful")
    
    print("Importing Agent...")
    from mini_agent.agent import Agent
    print("✓ Agent import successful")
    
    print("Importing mini_agent package...")
    import mini_agent
    print("✓ Mini-Agent package import successful")
    
    print("\n🎉 ALL IMPORTS SUCCESSFUL! The import errors have been fixed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()