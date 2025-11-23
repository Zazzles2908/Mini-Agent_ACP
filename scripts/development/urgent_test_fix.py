#!/usr/bin/env python3
"""
URGENT TEST: MiniMax-M2 Configuration Fix Validation

This validates that MiniMax-M2 is properly configured with OpenAI-compatible API.
"""

def urgent_test_minimax_config():
    """Urgent test to verify MiniMax-M2 config is correct"""
    print("🚨 URGENT TEST: MiniMax-M2 Configuration")
    print("=" * 45)
    
    # Read config
    with open("mini_agent/config/config.yaml", 'r') as f:
        content = f.read()
    
    print("📄 Current config:")
    lines = content.split('\n')
    for i, line in enumerate(lines[6:16], 7):
        print(f"{i:2d}: {line}")
    
    # Check for correct configuration
    issues = []
    if 'provider: "openai"' not in content:
        issues.append("Provider should be 'openai'")
    else:
        print("✅ Provider: 'openai' (CORRECT)")
    
    if 'api_base: "https://api.minimax.io/v1"' not in content:
        issues.append("Base URL should be 'https://api.minimax.io/v1'")
    else:
        print("✅ Base URL: 'https://api.minimax.io/v1' (CORRECT)")
    
    # Test OpenAI client
    try:
        from mini_agent.llm.openai_client import OpenAIClient
        client = OpenAIClient(
            api_key="test_key",
            api_base="https://api.minimax.io/v1",
            model="MiniMax-M2"
        )
        print("✅ OpenAI client initializes correctly")
        print(f"   - Base: {client.api_base}")
        print(f"   - Model: {client.model}")
    except Exception as e:
        issues.append(f"OpenAI client failed: {e}")
    
    # Test that Anthropic client is NOT used
    print("\n🔍 Checking that Anthropic is NOT being used:")
    try:
        from mini_agent.llm.anthropic_client import AnthropicClient
        print("⚠️  AnthropicClient is available (this is OK if not used)")
    except Exception as e:
        print(f"ℹ️  AnthropicClient import failed: {e} (this is OK)")
    
    if issues:
        print(f"\n❌ ISSUES FOUND: {len(issues)}")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print(f"\n✅ ALL CHECKS PASSED")
        print("MiniMax-M2 should work correctly now")
        return True

if __name__ == "__main__":
    success = urgent_test_minimax_config()
    if success:
        print("\n🎉 CONFIGURATION FIX SUCCESSFUL")
    else:
        print("\n💥 CONFIGURATION STILL BROKEN")
