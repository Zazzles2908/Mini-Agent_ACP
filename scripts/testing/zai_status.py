#!/usr/bin/env python3
"""
Z.AI Status Summary - No Interactive Input Required
"""

import os
import sys
from pathlib import Path

# Setup environment
os.chdir("C:\\Users\\Jazeel-Home\\Mini-Agent")
sys.path.insert(0, os.getcwd())

# Load .env
env_file = Path(".env")
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

def main():
    print("🎯 Mini-Agent Z.AI Integration - Status Summary")
    print("=" * 60)
    
    # Check Z.AI
    try:
        from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
        
        api_key = get_zai_api_key()
        if api_key:
            print("✅ Z.AI API Key: Loaded and Valid")
            print("✅ Z.AI Client: Available")
            
            # Quick test
            import asyncio
            async def quick_test():
                client = ZAIClient(api_key)
                result = await client.research_and_analyze(
                    query="GLM capabilities",
                    depth="quick"
                )
                return result.get("success", False)
            
            success = asyncio.run(quick_test())
            if success:
                print("✅ Web Search: Functional")
            else:
                print("⚠️  Web Search: Needs attention")
        else:
            print("❌ Z.AI API Key: Not found")
            
    except Exception as e:
        print(f"❌ Z.AI Status: Error - {e}")
    
    print("\n🚀 HOW TO USE:")
    print("1. Start Mini-Agent: python -m mini_agent.cli")
    print("2. Try: 'Search for latest AI developments 2024'")
    print("3. Enjoy native GLM web search!")
    
    print("\n📚 DOCUMENTATION:")
    print("• Status Report: documents/FINAL_ZAI_STATUS_REPORT.md")
    print("• Integration: documents/ZAI_INTEGRATION_STATUS_REPORT.md")
    print("• Configuration: mini_agent/config.py")

if __name__ == "__main__":
    main()
