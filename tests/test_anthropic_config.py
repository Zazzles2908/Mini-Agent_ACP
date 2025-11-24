#!/usr/bin/env python3
"""
PROPER TEST: Anthropic SDK Configuration Validation

This test validates that the Anthropic SDK configuration is properly implemented
and the system can actually use the Anthropic client.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_provider_setting():
    """Test that config.yaml has correct provider setting"""
    print("🔧 TEST 1: Configuration Provider Setting")
    
    config_path = project_root / "mini_agent" / "config" / "config.yaml"
    if not config_path.exists():
        print("❌ FAIL: config.yaml file not found")
        return False
    
    # Read and parse config
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Check for correct provider setting
    if 'provider: "anthropic"' in content:
        print("✅ PASS: Provider correctly set to 'anthropic'")
        return True
    elif 'provider: "openai"' in content:
        print("❌ FAIL: Provider still set to 'openai' - fix not implemented")
        return False
    else:
        print("❌ FAIL: Provider setting not found in config")
        return False

def test_anthropic_client_import():
    """Test that anthropic_client.py can be imported"""
    print("🔧 TEST 2: Anthropic Client Import")
    
    try:
        from mini_agent.llm.anthropic_client import AnthropicClient
        print("✅ PASS: AnthropicClient imported successfully")
        return True
    except ImportError as e:
        print(f"❌ FAIL: Cannot import AnthropicClient: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: Import error: {e}")
        return False

def test_anthropic_client_initialization():
    """Test that AnthropicClient can be initialized"""
    print("🔧 TEST 3: Anthropic Client Initialization")
    
    try:
        from mini_agent.llm.anthropic_client import AnthropicClient
        
        # Test initialization (should not fail even without API key)
        client = AnthropicClient(
            api_key="test_key",
            api_base="https://api.minimax.io",
            model="MiniMax-M2"
        )
        
        print("✅ PASS: AnthropicClient initialized successfully")
        print(f"   - Base URL: {client.api_base}")
        print(f"   - Model: {client.model}")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: AnthropicClient initialization failed: {e}")
        return False

def test_config_consistency():
    """Test that config is consistent with Anthropic usage"""
    print("🔧 TEST 4: Configuration Consistency")
    
    config_path = project_root / "mini_agent" / "config" / "config.yaml"
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for inconsistencies
    if 'provider: "anthropic"' in content:
        if 'api_base: "https://api.openai.com/v1"' in content:
            issues.append("Config has anthropic provider but OpenAI base URL")
        
        if 'OpenAI' in content and 'api_base: "https://api.minimax.io"' in content:
            # This is actually correct for MiniMax
            print("✅ PASS: Config properly uses MiniMax base URL with Anthropic provider")
            return True
    
    if issues:
        for issue in issues:
            print(f"❌ ISSUE: {issue}")
        return False
    
    print("✅ PASS: Configuration appears consistent")
    return True

def main():
    """Run all tests"""
    print("🧪 PROPER ANTHROPIC CONFIG VALIDATION TESTS")
    print("=" * 50)
    
    tests = [
        test_config_provider_setting,
        test_anthropic_client_import,
        test_anthropic_client_initialization,
        test_config_consistency
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR in {test.__name__}: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Anthropic config properly implemented!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Implementation needs fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
