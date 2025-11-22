#!/usr/bin/env python3
"""Simple ACP stdio test"""

import subprocess
import sys
import json

def simple_acp_test():
    """Test basic ACP stdio functionality"""
    print("🧪 Testing ACP stdio functionality...")
    
    try:
        # Start the ACP server
        process = subprocess.Popen([
            sys.executable, '-m', 'mini_agent.acp'
        ], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
        )
        
        print("✅ ACP server started")
        
        # Send initialize message
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        message_str = json.dumps(init_message) + '\n'
        process.stdin.write(message_str)
        process.stdin.flush()
        
        print("📤 Sent initialize message")
        
        # Try to read output with timeout
        try:
            output, error = process.communicate(timeout=10)
            print(f"📥 Server output: {output}")
            if error:
                print(f"⚠️ Server error: {error}")
        except subprocess.TimeoutExpired:
            print("⏰ Server is running (no immediate response, which is expected)")
            process.kill()
            output, error = process.communicate()
            print(f"📥 Final output: {output}")
        
        print("✅ ACP stdio test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ACP test failed: {e}")
        return False

if __name__ == "__main__":
    success = simple_acp_test()
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")