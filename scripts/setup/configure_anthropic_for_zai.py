#!/usr/bin/env python3
"""
Configure Z.AI for Mini-Agent using Anthropic-compatible endpoint
This sets up the environment variables for Z.AI integration with Claude Code
"""

import os
import sys
from pathlib import Path

def main():
    """Configure Z.AI integration through Anthropic endpoint"""
    
    # Z.AI API key from environment
    zai_api_key = os.getenv('ZAI_API_KEY')
    if not zai_api_key:
        print("❌ Error: ZAI_API_KEY not found in environment")
        print("Please set your Z.AI API key:")
        print("setx ZAI_API_KEY your_zai_api_key")
        return False
    
    # Set Anthropic-compatible environment variables for Z.AI
    os.environ['ANTHROPIC_AUTH_TOKEN'] = zai_api_key
    os.environ['ANTHROPIC_BASE_URL'] = 'https://api.z.ai/api/anthropic'
    
    # Model mapping for Z.AI coding plan
    model_mappings = {
        'ANTHROPIC_DEFAULT_OPUS_MODEL': 'GLM-4.6',
        'ANTHROPIC_DEFAULT_SONNET_MODEL': 'GLM-4.6', 
        'ANTHROPIC_DEFAULT_HAIKU_MODEL': 'GLM-4.5-Air'
    }
    
    print("✅ Z.AI Anthropic-compatible endpoint configured:")
    print(f"   ANTHROPIC_AUTH_TOKEN: {zai_api_key[:20]}...")
    print(f"   ANTHROPIC_BASE_URL: https://api.z.ai/api/anthropic")
    print("\n📋 Model mappings:")
    for env_var, model in model_mappings.items():
        os.environ[env_var] = model
        print(f"   {env_var}: {model}")
    
    print("\n💡 Benefits of this setup:")
    print("   • Uses coding plan credits (~120 prompts/5 hours)")
    print("   • Natural citations with Claude Code")
    print("   • Web search integration ready")
    print("   • No separate Z.AI API calls needed")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)