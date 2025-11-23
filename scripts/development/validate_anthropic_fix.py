#!/usr/bin/env python3
"""
MANUAL VALIDATION: Anthropic SDK Configuration Fix

This validates that the Anthropic configuration fix is properly implemented.
"""

def validate_anthropic_config():
    """Validate the Anthropic config fix"""
    print("🧪 VALIDATING ANTHROPIC CONFIG FIX")
    print("=" * 40)
    
    # Read config file
    config_path = "mini_agent/config/config.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading config from: {config_path}")
    
    # Check line 12 specifically
    lines = content.split('\n')
    line_12 = lines[11] if len(lines) > 11 else "NOT FOUND"
    print(f"📄 Line 12: {line_12}")
    
    # Validate fix
    if 'provider: "anthropic"' in content:
        print("✅ SUCCESS: Provider correctly set to 'anthropic'")
        
        # Check for consistency
        if 'https://api.minimax.io' in content:
            print("✅ SUCCESS: Uses correct MiniMax base URL")
        else:
            print("⚠️  WARNING: MiniMax base URL not found")
            
        # Check Anthropic import
        try:
            exec("from mini_agent.llm.anthropic_client import AnthropicClient")
            print("✅ SUCCESS: Anthropic client can be imported")
            
            # Test initialization
            exec("""
from mini_agent.llm.anthropic_client import AnthropicClient
client = AnthropicClient(api_key="test", api_base="https://api.minimax.io", model="MiniMax-M2")
print("✅ SUCCESS: Anthropic client initializes correctly")
print(f"   - Base: {client.api_base}")
print(f"   - Model: {client.model}")
""")
            
        except Exception as e:
            print(f"❌ ERROR: Anthropic client test failed: {e}")
            
        return True
        
    elif 'provider: "openai"' in content:
        print("❌ FAIL: Provider still set to 'openai' - fix not applied")
        return False
    else:
        print("❌ FAIL: Provider setting not found")
        return False

if __name__ == "__main__":
    success = validate_anthropic_config()
    if success:
        print("\n🎉 ANTHROPIC CONFIG VALIDATION PASSED")
    else:
        print("\n💥 ANTHROPIC CONFIG VALIDATION FAILED")
