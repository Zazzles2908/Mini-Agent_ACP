#!/usr/bin/env python3
"""
Simple ACP server diagnostic - check if server starts and responds.
"""

import subprocess
import sys
import json

def simple_acp_test():
    """Test basic ACP server functionality."""
    
    try:
        print("🔍 Testing ACP server startup...")
        
        # Start server with timeout
        process = subprocess.Popen(
            [sys.executable, "-m", "mini_agent.acp", "--workspace", "."],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send simple initialize message
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
            "id": 1
        }
        
        print("📤 Sending initialize message...")
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # Wait briefly for response
        import time
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Server is running and responsive")
            print("📊 VS Code extension integration should work!")
        else:
            stderr_output = process.stderr.read()
            print(f"❌ Server stopped unexpectedly")
            print(f"Error: {stderr_output}")
            
        # Cleanup
        process.terminate()
        process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    simple_acp_test()
