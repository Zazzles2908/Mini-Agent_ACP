#!/usr/bin/env python3
"""Test the simple ACP stdio server"""

import subprocess
import json
import time
import threading
from queue import Queue

def test_simple_acp_server():
    """Test the simple ACP stdio server"""
    print("🧪 Testing Simple ACP stdio server...")
    
    try:
        # Start the simple ACP server
        process = subprocess.Popen([
            'python', 'simple_acp_stdio_server.py'
        ], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
        )
        
        print("✅ Simple ACP server started")
        
        # Test 1: Send initialization message
        print("📤 Test 1: Sending initialize message...")
        
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        message_str = json.dumps(init_message) + '\n'
        process.stdin.write(message_str)
        process.stdin.flush()
        
        # Wait for response
        time.sleep(1)
        
        # Read response
        output_line = process.stdout.readline()
        if output_line:
            response = json.loads(output_line.strip())
            print(f"✅ Initialize response: {response}")
            
            # Verify response structure
            if response.get('id') == 1 and response.get('result'):
                print("✅ Initialize test passed!")
            else:
                print("❌ Initialize test failed!")
                return False
        else:
            print("❌ No response received!")
            return False
        
        # Test 2: Create session
        print("📤 Test 2: Creating new session...")
        
        session_message = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "newSession",
            "params": {"cwd": "./"}
        }
        
        session_str = json.dumps(session_message) + '\n'
        process.stdin.write(session_str)
        process.stdin.flush()
        
        time.sleep(1)
        
        session_output = process.stdout.readline()
        if session_output:
            session_response = json.loads(session_output.strip())
            print(f"✅ Session response: {session_response}")
            
            session_id = session_response.get('result', {}).get('sessionId')
            if session_id:
                print(f"✅ Session created with ID: {session_id}")
            else:
                print("❌ Session creation failed!")
                return False
        else:
            print("❌ No session response!")
            return False
        
        # Test 3: Send prompt
        print("📤 Test 3: Sending prompt...")
        
        prompt_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "prompt", 
            "params": {
                "sessionId": session_id,
                "prompt": "Hello, can you help me with Python?"
            }
        }
        
        prompt_str = json.dumps(prompt_message) + '\n'
        process.stdin.write(prompt_str)
        process.stdin.flush()
        
        time.sleep(1)
        
        prompt_output = process.stdout.readline()
        if prompt_output:
            prompt_response = json.loads(prompt_output.strip())
            print(f"✅ Prompt response: {prompt_response}")
            
            content = prompt_response.get('result', {}).get('content', [])
            if content and content[0].get('text'):
                print(f"✅ Got response: {content[0]['text'][:50]}...")
            else:
                print("❌ No content in prompt response!")
                return False
        else:
            print("❌ No prompt response!")
            return False
        
        # Cleanup
        process.terminate()
        process.wait(timeout=5)
        
        print("✅ Simple ACP server test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Simple ACP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_acp_server()
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")