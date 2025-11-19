#!/usr/bin/env python3
"""Simple test of basic server without Mini-Agent integration"""

import json
import sys

# Simple test without Mini-Agent imports
def test_basic_server():
    """Test the basic server structure"""
    print("🧪 Testing basic server structure...")
    
    try:
        # Test the JSON message handling directly
        from mini_agent_stdio_server import MiniAgentACPStdioServer
        
        server = MiniAgentACPStdioServer()
        print("✅ Server created")
        
        # Test initialize message
        import asyncio
        
        async def test_initialize():
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {}
            }
            
            response = await server.handle_message(init_message)
            print(f"✅ Initialize response: {response}")
            
            return response.get('result') is not None
        
        # Test without Mini-Agent integration
        success = asyncio.run(test_initialize())
        return success
        
    except Exception as e:
        print(f"❌ Basic server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_server()
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")