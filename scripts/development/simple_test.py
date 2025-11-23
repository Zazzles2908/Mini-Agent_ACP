#!/usr/bin/env python3
"""Simple test of config fix"""

def test_simple():
    try:
        # Test OpenAI client import
        from mini_agent.llm.openai_client import OpenAIClient
        
        # Test initialization
        client = OpenAIClient(
            api_key="test_key",
            api_base="https://api.minimax.io/v1",
            model="MiniMax-M2"
        )
        
        print("✅ SUCCESS: OpenAI client initializes")
        print(f"   Base: {client.api_base}")
        print(f"   Model: {client.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if test_simple():
        print("\n🎉 Configuration appears to be fixed!")
    else:
        print("\n💥 Still has issues")
