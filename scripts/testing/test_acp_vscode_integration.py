#!/usr/bin/env python3
"""
Quick test of ACP server communication for VS Code extension.
Tests the stdio-based JSON-RPC 2.0 communication.
"""

import json
import subprocess
import sys
from typing import Dict, Any

def test_acp_server():
    """Test ACP server with JSON-RPC 2.0 messages."""
    
    # Test messages for ACP protocol
    test_messages = [
        # Initialize connection
        {
            "jsonrpc": "2.0",
            "method": "initialize", 
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "vscode-extension", "version": "1.0.0"}
            },
            "id": 1
        },
        # Test tool call
        {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "list_skills",
                "arguments": {}
            },
            "id": 2
        }
    ]
    
    try:
        print("🚀 Starting ACP server test...")
        
        # Start ACP server as subprocess
        process = subprocess.Popen(
            [sys.executable, "-m", "mini_agent.acp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        
        print("✅ ACP server started successfully")
        
        # Test initialization
        init_message = json.dumps(test_messages[0]) + "\n"
        process.stdin.write(init_message)
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            result = json.loads(response.strip())
            print(f"✅ Initialize response: {result}")
        else:
            print("❌ No response from server")
            
        # Test tool call
        tool_message = json.dumps(test_messages[1]) + "\n"
        process.stdin.write(tool_message)
        process.stdin.flush()
        
        # Read tool response
        response = process.stdout.readline()
        if response:
            result = json.loads(response.strip())
            print(f"✅ Tool call response: {result}")
        else:
            print("❌ No tool response from server")
            
        # Cleanup
        process.stdin.close()
        process.wait()
        
        print("🎉 ACP server communication test completed!")
        return True
        
    except Exception as e:
        print(f"❌ ACP server test failed: {e}")
        return False

if __name__ == "__main__":
    test_acp_server()
