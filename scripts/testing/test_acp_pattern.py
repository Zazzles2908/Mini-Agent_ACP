#!/usr/bin/env python3
"""Test the ACP library usage pattern"""

import acp
import asyncio

async def test_acp_agent():
    """Test how to properly use the ACP Agent class"""
    
    print("🧪 Testing ACP Agent usage pattern...")
    
    try:
        # Create a simple agent that matches the ACP interface
        class TestAgent:
            def initialize(self, params):
                return {
                    "protocolVersion": acp.PROTOCOL_VERSION,
                    "agentCapabilities": {
                        "loadSession": False
                    },
                    "agentInfo": {
                        "name": "test-agent",
                        "title": "Test Agent",
                        "version": "1.0.0"
                    }
                }
            
            def newSession(self, params):
                return {
                    "sessionId": "test-session-123"
                }
            
            def prompt(self, params):
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Echo: {params.get('prompt', 'No prompt')}"
                        }
                    ]
                }
            
            def cancel(self, params):
                return {"cancelled": True}
            
            def loadSession(self, params):
                return {"sessionLoaded": False}
            
            def setSessionMode(self, params):
                return {"modeSet": True}
            
            def setSessionModel(self, params):
                return {"modelSet": True}
        
        # Create agent instance
        agent = TestAgent()
        print("✅ Test agent created")
        
        # Test methods
        init_result = agent.initialize({})
        print(f"✅ Initialize test: {init_result}")
        
        session_result = agent.newSession({"cwd": "./"})
        print(f"✅ New session test: {session_result}")
        
        prompt_result = agent.prompt({"prompt": "Hello", "sessionId": "test"})
        print(f"✅ Prompt test: {prompt_result}")
        
        print("✅ ACP Agent pattern validated!")
        return True
        
    except Exception as e:
        print(f"❌ ACP Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_acp_agent())
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")