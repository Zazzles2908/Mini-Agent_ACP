#!/usr/bin/env python3
"""
ACTUAL System Reality Check
Test what actually works vs what I assumed worked
"""

import sys
import os
import json
import subprocess
sys.path.insert(0, '.')

print("🚨 ACTUAL SYSTEM REALITY CHECK")
print("=" * 50)

# 1. Check what's actually available vs what I claimed
print("\n1. MCP SERVER REALITY:")
print("   What EXAI should provide vs what it actually provides:")

# Check the actual EXAI-MCP container logs
print("\n2. EXAI-MCP Container Status:")
result = subprocess.run(["docker", "ps", "--format", "{{.Names}}\\t{{.Status}}"], capture_output=True, text=True)
for line in result.stdout.split('\n')[1:]:
    if 'exai' in line.lower():
        print(f"   Container: {line}")

# Check what port the stdio MCP server actually uses
print("\n3. EXAI-MCP Stdio Service:")
result = subprocess.run(["docker", "port", "exai-mcp-stdio"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"   MCP Stdio ports: {result.stdout.strip()}")
else:
    print(f"   ❌ No stdio MCP container found")

# 2. Z.AI API Reality Check
print("\n4. Z.AI API REALITY CHECK:")

# Test if the key actually works for web search
from start_mini_agent import load_environment
load_environment()

try:
    import asyncio
    from mini_agent.llm.zai_client import ZAIClient
    
    async def test_real_zai():
        client = ZAIClient(os.environ.get('ZAI_API_KEY'))
        
        # Test 1: Can we even make the API call?
        print("   Testing Z.AI web search API...")
        try:
            result = await client.web_search(query="test", count=1)
            print(f"   Raw response: {result}")
            
            if not result.get("success"):
                print(f"   ❌ Z.AI web search FAILED: {result.get('error')}")
            else:
                print(f"   ✅ Z.AI web search working")
        except Exception as e:
            print(f"   ❌ Z.AI web search ERROR: {e}")
        
        # Test 2: Can we use GLM Chat with the key?
        print("   Testing GLM Chat with key...")
        try:
            result = await client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="GLM-4.6"
            )
            if result.get("success"):
                print(f"   ✅ GLM Chat working (have MiniMax access)")
            else:
                print(f"   ❌ GLM Chat failed: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ GLM Chat ERROR: {e}")
    
    asyncio.run(test_real_zai())
    
except Exception as e:
    print(f"   ❌ Z.AI client test failed: {e}")

# 3. Dependency Check
print("\n5. DEPENDENCY ISSUES:")
try:
    import aiohttp
    print("   ✅ aiohttp: Available")
except ImportError:
    print("   ❌ aiohttp: MISSING")

try:
    import openai
    print("   ✅ openai SDK: Available")
except ImportError:
    print("   ❌ openai SDK: MISSING (need to install)")

# 4. What the user actually has
print("\n6. USER'S ACTUAL SYSTEM:")
print("   Based on your requirements:")
print("   - EXAI-MCP server: Running (but may not be connecting properly)")
print("   - Z.AI key: May be MiniMax/GLM, not Z.AI")
print("   - Web search: Probably not available")
print("   - Dependencies: Need to verify aiohttp and openai SDK")

print("\n❌ MY PREVIOUS ASSESSMENTS WERE INCORRECT")
print("🎯 NEED TO:")
print("   1. Test EXAI-MCP stdio connection properly")
print("   2. Verify what your ZAI_API_KEY actually provides")
print("   3. Fix dependency issues")
print("   4. Stop making false assumptions")
