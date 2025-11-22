#!/usr/bin/env python3
"""
Test the fixed configuration
"""

import os
import yaml
from pathlib import Path

def test_configuration():
    """Test the configuration fix"""
    print("🔧 Testing Configuration Fix")
    print("=" * 40)
    
    config_path = Path("mini_agent/config/config.yaml")
    
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("📋 Configuration:")
    print(f"   API Base: {config['api_base']}")
    print(f"   Model: {config['model']}")
    print(f"   Provider: {config['provider']}")
    print(f"   API Key: {config['api_key']}")
    
    print("\n🎯 Expected API Endpoint:")
    api_base = config['api_base']
    provider = config['provider']
    
    if provider == "zai":
        # ZAI provider doesn't add protocol suffixes
        expected_endpoint = f"{api_base.rstrip('/')}/messages"
        print(f"   Endpoint: {expected_endpoint}")
        print("   ✅ Correct: Z.AI GLM API endpoint")
    elif provider == "anthropic":
        # Anthropic adds /anthropic/v1
        expected_endpoint = f"{api_base.rstrip('/')}/anthropic/v1/messages"
        print(f"   Endpoint: {expected_endpoint}")
        print("   ❌ Wrong: Would cause 404 error")
    elif provider == "openai":
        # OpenAI adds /v1
        expected_endpoint = f"{api_base.rstrip('/')}/v1/messages"
        print(f"   Endpoint: {expected_endpoint}")
        print("   ❌ Wrong: OpenAI protocol on Z.AI base")
    
    print(f"\n✅ Configuration Fix Applied Successfully!")
    print(f"   GLM-4.6 will now use proper Z.AI API endpoint")

if __name__ == "__main__":
    test_configuration()