#!/usr/bin/env python3
"""Direct test of ACP stdio server communication"""

import asyncio
import json
import sys
from mini_agent.acp import main

async def test_acp_stdio():
    """Test ACP server with JSON-RPC messages"""
    
    # Create test initialization message
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    print("🧪 Testing ACP Stdio Communication...")
    print(f"📤 Sending: {json.dumps(init_message, indent=2)}")
    
    try:
        # Redirect stdin to our test message
        test_input = json.dumps(init_message) + "\n"
        
        # Capture stdout to see the response
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        captured_output = io.StringIO()
        captured_errors = io.StringIO()
        
        # Simulate stdin by providing test input
        original_stdin = sys.stdin
        sys.stdin = io.StringIO(test_input)
        
        try:
            with redirect_stdout(captured_output), redirect_stderr(captured_errors):
                # Run the ACP main function
                await main()
        finally:
            sys.stdin = original_stdin
        
        output = captured_output.getvalue()
        errors = captured_errors.getvalue()
        
        print(f"📥 Received response:")
        if output:
            print(output)
        if errors:
            print(f"Errors: {errors}")
            
        print("✅ ACP stdio communication test completed!")
        
    except Exception as e:
        print(f"❌ ACP stdio test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_acp_stdio())