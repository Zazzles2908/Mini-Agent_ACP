#!/usr/bin/env python3
"""Test the production Mini-Agent stdio server"""

import subprocess
import json
import time

def test_production_server():
    """Test the production ACP server with Mini-Agent integration"""
    print("🧪 Testing Production Mini-Agent ACP Server...")
    
    try:
        # Start the production server
        process = subprocess.Popen([
            'python', 'mini_agent_stdio_server.py'
        ], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
        )
        
        print("✅ Production server started")
        
        # Test 1: Initialize
        print("📤 Test 1: Initialize...")
        
        init_message = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        process.stdin.write(json.dumps(init_message) + '\n')
        process.stdin.flush()
        
        time.sleep(2)
        
        # Check stderr for initialization logs
        stderr_output = process.stderr.read()
        print(f"📊 Server logs: {stderr_output[-500:]}")  # Last 500 chars
        
        # Read response
        output_line = process.stdout.readline()
        if output_line:
            response = json.loads(output_line.strip())
            print(f"✅ Initialize response: {response}")
            
            if response.get('result', {}).get('agentInfo', {}).get('name') == 'mini-agent':
                print("✅ Initialize test passed!")
            else:
                print("❌ Initialize test failed!")
                return False
        else:
            print("❌ No response!")
            return False
        
        # Test 2: Create session
        print("📤 Test 2: New session...")
        
        session_message = {"jsonrpc": "2.0", "id": 2, "method": "newSession", "params": {"cwd": "./"}}
        process.stdin.write(json.dumps(session_message) + '\n')
        process.stdin.flush()
        
        time.sleep(1)
        
        session_output = process.stdout.readline()
        if session_output:
            session_response = json.loads(session_output.strip())
            session_id = session_response.get('result', {}).get('sessionId')
            print(f"✅ Session created: {session_id}")
        else:
            print("❌ No session response!")
            session_id = None
        
        # Test 3: Simple prompt
        if session_id:
            print("📤 Test 3: Send prompt...")
            
            prompt_message = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "prompt",
                "params": {"sessionId": session_id, "prompt": "Hello!"}
            }
            process.stdin.write(json.dumps(prompt_message) + '\n')
            process.stdin.flush()
            
            time.sleep(3)
            
            prompt_output = process.stdout.readline()
            if prompt_output:
                prompt_response = json.loads(prompt_output.strip())
                content = prompt_response.get('result', {}).get('content', [])
                if content:
                    print(f"✅ Got response: {content[0]['text'][:100]}...")
                else:
                    print("⚠️ No content in response")
            else:
                print("⚠️ No prompt response")
        
        # Cleanup
        process.terminate()
        process.wait(timeout=5)
        
        print("✅ Production server test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Production test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_production_server()
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")