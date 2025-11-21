#!/usr/bin/env python3
"""
MCP Server Restoration Test
Tests MCP server connectivity and functionality
"""

import sys
import os
import asyncio
import json
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔧 MCP Server Restoration Test")
print("=" * 45)

async def test_mcp_configuration():
    """Test MCP configuration file."""
    print("\n1. MCP Configuration Test:")
    
    mcp_config_path = ".mcp.json"
    if os.path.exists(mcp_config_path):
        try:
            with open(mcp_config_path, 'r') as f:
                config = json.load(f)
            
            mcp_servers = config.get("mcpServers", {})
            print(f"   ✅ Found {len(mcp_servers)} MCP servers configured")
            
            for server_name, server_config in mcp_servers.items():
                command = server_config.get("command", "N/A")
                disabled = server_config.get("disabled", False)
                status = "🔴 Disabled" if disabled else "🟢 Enabled"
                print(f"   - {server_name}: {command} - {status}")
                
        except Exception as e:
            print(f"   ❌ Failed to read MCP config: {e}")
    else:
        print(f"   ⚠️  MCP config not found: {mcp_config_path}")

async def test_mcp_connection():
    """Test MCP server connections."""
    print("\n2. MCP Server Connection Test:")
    
    try:
        from mini_agent.tools.mcp_loader import load_mcp_tools_async
        
        print("   🔄 Loading MCP tools...")
        tools = await load_mcp_tools_async()
        
        print(f"   ✅ Loaded {len(tools)} MCP tools")
        
        # Show tool categories
        if tools:
            print("   📋 Available MCP tools:")
            for i, tool in enumerate(tools[:10]):  # Show first 10
                desc = tool.description[:50] + "..." if len(tool.description) > 50 else tool.description
                print(f"      {i+1}. {tool.name}: {desc}")
            if len(tools) > 10:
                print(f"      ... and {len(tools) - 10} more tools")
                
    except Exception as e:
        print(f"   ❌ MCP connection test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_vscode_integration():
    """Test VS Code extension files."""
    print("\n3. VS Code Extension Test:")
    
    vscode_dir = "vscode-extension"
    if os.path.exists(vscode_dir):
        print(f"   ✅ VS Code extension directory exists")
        
        # Check key files
        key_files = ["package.json", "extension.js", "chat_integration_extension.js"]
        for file_name in key_files:
            file_path = os.path.join(vscode_dir, file_name)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_name}: {size} bytes")
            else:
                print(f"   ❌ {file_name}: Missing")
    else:
        print(f"   ❌ VS Code extension directory not found")

async def main():
    await test_mcp_configuration()
    await test_mcp_connection()
    await test_vscode_integration()
    
    print("\n🎯 MCP RESTORATION TESTS COMPLETE")

if __name__ == "__main__":
    asyncio.run(main())
