#!/usr/bin/env python3
"""Simple system check for Mini-Agent."""

import os
from pathlib import Path

def main():
    print("🔍 Mini-Agent System Check")
    print("=" * 30)
    
    # Check environment
    zai_api_key = os.getenv("ZAI_API_KEY")
    if zai_api_key:
        print(f"✅ ZAI_API_KEY: {zai_api_key[:10]}...")
    else:
        print("❌ ZAI_API_KEY: Missing")
    
    # Check venv
    if Path(".venv").exists():
        print("✅ Virtual Environment: Available")
    else:
        print("❌ Virtual Environment: Missing")
    
    # Check config
    config_file = Path("mini_agent/config/config.yaml")
    if config_file.exists():
        print("✅ Configuration: Found")
    else:
        print("❌ Configuration: Missing")
    
    print("=" * 30)
    print("🧪 Quick GLM Test...")
    
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        
        from mini_agent.llm.glm_client import GLMClient
        from mini_agent.schema import Message
        
        import asyncio
        
        async def test_glm():
            client = GLMClient(api_key=zai_api_key, model="glm-4.6")
            result = await client.generate([Message(role="user", content="Hello")])
            return result.finish_reason == "stop"
        
        success = asyncio.run(test_glm())
        if success:
            print("✅ GLM-4.6: Working")
        else:
            print("❌ GLM-4.6: Failed")
            
    except Exception as e:
        print(f"❌ GLM-4.6: Error - {e}")
    
    print("=" * 30)
    print("System check complete!")

if __name__ == "__main__":
    main()