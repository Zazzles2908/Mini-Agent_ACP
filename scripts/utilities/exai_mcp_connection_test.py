#!/usr/bin/env python3
"""
EXAI-MCP Server Connection Test
Connect to the actual running EXAI-MCP server
"""

import sys
import os
import json
sys.path.insert(0, '.')

print("🔗 EXAI-MCP SERVER CONNECTION TEST")
print("=" * 45)

# Check what ports EXAI-MCP is using
import subprocess
result = subprocess.run(["docker", "ps", "--format", "{{.Names}}\\t{{.Ports}}"], capture_output=True, text=True)
print("\n1. EXAI-MCP Container Ports:")
for line in result.stdout.split('\n')[1:]:
    if 'exai' in line.lower():
        print(f"   {line}")

# Test the health endpoint
print("\n2. EXAI-MCP Health Check:")
try:
    import requests
    response = requests.get("http://localhost:3002/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Health check: {data}")
    else:
        print(f"   ❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Health check error: {e}")

# Check if we can connect to the WebSocket endpoint
print("\n3. EXAI-MCP WebSocket Test:")
try:
    import websockets
    import asyncio
    
    async def test_websocket():
        try:
            uri = "ws://localhost:3010"
            print(f"   🔗 Connecting to {uri}")
            
            async with websockets.connect(uri) as websocket:
                print("   ✅ WebSocket connection established")
                
                # Send a basic MCP initialization message
                init_msg = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "test-client",
                            "version": "1.0.0"
                        }
                    }
                }
                
                await websocket.send(json.dumps(init_msg))
                response = await websocket.recv()
                print(f"   📨 Received: {response[:200]}...")
                
                # Try to list tools
                tools_msg = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }
                
                await websocket.send(json.dumps(tools_msg))
                tools_response = await websocket.recv()
                tools_data = json.loads(tools_response)
                
                if "result" in tools_data and "tools" in tools_data["result"]:
                    tools = tools_data["result"]["tools"]
                    print(f"   ✅ Found {len(tools)} EXAI-MCP tools:")
                    for i, tool in enumerate(tools[:10]):  # Show first 10
                        print(f"      {i+1}. {tool.get('name', 'Unknown')}: {tool.get('description', '')[:60]}...")
                    if len(tools) > 10:
                        print(f"      ... and {len(tools) - 10} more tools")
                else:
                    print(f"   ❌ No tools found: {tools_data}")
                
        except Exception as e:
            print(f"   ❌ WebSocket error: {e}")
    
    asyncio.run(test_websocket())
    
except ImportError:
    print("   ❌ websockets package not available")
except Exception as e:
    print(f"   ❌ WebSocket test failed: {e}")

print("\n4. What EXAI-MCP Should Provide:")
print("   Based on your system, EXAI-MCP should have:")
print("   - Advanced file operations")
print("   - Code analysis and debugging")
print("   - Project management tools")
print("   - Web scraping capabilities")
print("   - API integrations")
print("   - Custom development tools")
