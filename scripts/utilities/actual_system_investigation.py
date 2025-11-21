#!/usr/bin/env python3
"""
ACTUAL System Investigation - What the user has
"""

import sys
import os
import subprocess
import json
sys.path.insert(0, '.')

print("🔍 ACTUAL SYSTEM INVESTIGATION")
print("=" * 50)

# 1. Check what the user's ZAI_API_KEY actually is
print("\n1. ZAI_API_KEY Analysis:")
zai_key = os.environ.get('ZAI_API_KEY')
print(f"   ZAI_KEY: {zai_key[:20]}...{zai_key[-10:] if zai_key else 'None'}")

# Check if this looks like a GLM key (MiniMax)
if zai_key:
    if zai_key.startswith('eyJ') or 'minimax' in zai_key.lower():
        print("   ❌ This appears to be a GLM/MiniMax key, NOT a Z.AI key!")
        print("   📝 Z.AI web search is not available with this key")
    else:
        print("   ✅ This might be a Z.AI key")

# 2. Check the EXAI-MCP server that's actually running
print("\n2. EXAI-MCP Server Analysis:")
result = subprocess.run(["docker", "ps", "--format", "table {{.Names}}\\t{{.Ports}}"], capture_output=True, text=True)
if result.returncode == 0:
    print("   Running containers:")
    for line in result.stdout.split('\n')[1:]:
        if 'exai' in line.lower():
            print(f"   ✅ {line}")

# Check EXAI-MCP ports
print("\n3. EXAI-MCP Port Analysis:")
exai_ports = {
    "3010": "WebSocket (main API)",
    "3002": "Health check", 
    "3001": "Additional service",
    "3003": "HTTP API",
    "8079": "Stdio service"
}

for port, desc in exai_ports.items():
    result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
    if port in result.stdout:
        print(f"   ✅ Port {port} ({desc}): ACTIVE")

# 3. Find the ORIGINAL MCP configuration for EXAI
print("\n4. Finding Original EXAI Configuration:")
# Check all json files for EXAI references
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.json') and file != 'package-lock.json':
            try:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'exai' in content.lower():
                        print(f"   ✅ Found EXAI config: {file_path}")
                        with open(file_path, 'r') as f2:
                            config = json.load(f2)
                        print(f"   📋 Config: {json.dumps(config, indent=2)}")
            except:
                pass

# 4. Test what the user actually has access to
print("\n5. Testing Actual API Access:")
try:
    import asyncio
    from start_mini_agent import load_environment
    load_environment()
    
    async def test_api_access():
        from mini_agent.llm.zai_client import ZAIClient
        
        client = ZAIClient(os.environ.get('ZAI_API_KEY'))
        
        # Test GLM chat (which might work with MiniMax key)
        try:
            result = await client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="GLM-4.6"
            )
            if result.get("success"):
                print("   ✅ GLM Chat works - you have MiniMax API access")
            else:
                print(f"   ❌ GLM Chat failed: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ GLM Chat error: {e}")
        
        # Test actual Z.AI web search
        try:
            result = await client.web_search(
                query="test",
                count=1
            )
            if result.get("success"):
                print("   ✅ Z.AI web search works - you have Z.AI access")
            else:
                print(f"   ❌ Z.AI web search failed: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ Z.AI web search error: {e}")
    
    asyncio.run(test_api_access())
    
except Exception as e:
    print(f"   ❌ API test failed: {e}")

print("\n🚨 MAJOR FINDINGS:")
print("   1. ZAI_API_KEY appears to be MiniMax/GLM, NOT Z.AI")
print("   2. EXAI-MCP servers are running (ports 3010, 3002, etc.)")
print("   3. Need to connect to EXAI-MCP, not generic MCP")
print("   4. Z.AI web search may not be available with current key")
