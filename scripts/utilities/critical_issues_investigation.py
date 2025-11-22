#!/usr/bin/env python3
"""
Critical System Issues Investigation
Deep dive into what's actually working vs what's just responding
"""

import sys
import os
import subprocess
sys.path.insert(0, '.')

print("🔍 CRITICAL ISSUES INVESTIGATION")
print("=" * 50)

# 1. Check actual Z.AI web search functionality
print("\n1. Z.AI Web Search REALITY CHECK:")
try:
    import asyncio
    from start_mini_agent import load_environment
    load_environment()
    
    async def real_web_search_test():
        from mini_agent.llm.zai_client import ZAIClient
        
        client = ZAIClient(os.environ.get('ZAI_API_KEY'))
        
        # Test with a specific, verifiable query
        result = await client.web_search(
            query="What is the capital of France?",
            count=3
        )
        
        print(f"   Raw API response: {result}")
        
        if result.get("success"):
            results = result.get("search_result", [])
            print(f"   ✅ Search completed, {len(results)} results")
            for i, item in enumerate(results):
                print(f"   Result {i+1}: {item.get('title', 'No title')[:50]}...")
        else:
            print(f"   ❌ Search failed: {result.get('error')}")
    
    asyncio.run(real_web_search_test())
    
except Exception as e:
    print(f"   ❌ Z.AI test failed: {e}")

# 2. Check dependencies
print("\n2. Dependency Check:")
try:
    import aiohttp
    print("   ✅ aiohttp available")
except ImportError:
    print("   ❌ aiohttp MISSING - installing now...")
    subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp"])

# 3. Find the actual working MCP server
print("\n3. Original MCP Server Investigation:")
print("   Looking for EXAI-MCP server (the working one)...")

# Check for docker containers
result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
if result.returncode == 0:
    print("   Docker containers:")
    for line in result.stdout.split('\n')[1:]:
        if 'exai' in line.lower():
            print(f"   ✅ Found EXAI container: {line}")
else:
    print("   ❌ Docker not accessible or no containers running")

# Check for existing MCP configuration
print("\n4. Original MCP Configuration:")
mcp_configs = [
    ".mcp.json",
    "mcp.json", 
    "mini_agent/acp/.mcp.json",
    "mcp_config.json"
]

for config in mcp_configs:
    if os.path.exists(config):
        print(f"   ✅ Found: {config}")
        with open(config, 'r') as f:
            content = f.read()
            if 'exai' in content.lower():
                print("   ✅ Contains EXAI configuration!")
    else:
        print(f"   ❌ Missing: {config}")

print("\n🚨 ISSUES IDENTIFIED:")
print("   1. aiohttp dependency missing")
print("   2. Z.AI web search may not actually work") 
print("   3. Connecting to wrong MCP servers (generic instead of EXAI)")
print("   4. Need to verify Z.AI key capabilities")
