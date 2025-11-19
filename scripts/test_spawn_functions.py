#!/usr/bin/env python3
"""Test the correct way to use ACP with spawn functions"""

import acp
import asyncio

async def test_spawn_functions():
    """Test the spawn functions that might be the correct approach"""
    
    print("🧪 Testing ACP spawn functions...")
    
    try:
        # Test spawn_agent_process
        print("📦 Testing spawn_agent_process...")
        
        # Create a simple agent implementation
        class SimpleAgent:
            async def initialize(self, params):
                return {
                    'protocolVersion': acp.PROTOCOL_VERSION,
                    'agentCapabilities': {'loadSession': False},
                    'agentInfo': {
                        'name': 'test-agent',
                        'title': 'Test Agent',
                        'version': '1.0.0'
                    }
                }
            
            async def newSession(self, params):
                return {'sessionId': 'test-session'}
            
            async def prompt(self, params):
                return {
                    'content': [
                        {
                            'type': 'text',
                            'text': f"Echo: {params.get('prompt', 'No prompt')}"
                        }
                    ]
                }
            
            async def cancel(self, params):
                return {'cancelled': True}
            
            async def loadSession(self, params):
                return {'sessionLoaded': False}
            
            async def setSessionMode(self, params):
                return {'modeSet': True}
            
            async def setSessionModel(self, params):
                return {'modelSet': True}
        
        agent = SimpleAgent()
        print("✅ Simple agent created")
        
        # Test spawn_stdio_connection
        print("📦 Testing spawn_stdio_connection...")
        
        try:
            connection = await acp.spawn_stdio_connection(agent)
            print("✅ spawn_stdio_connection worked!")
            print(f"Connection type: {type(connection)}")
        except Exception as e:
            print(f"⚠️ spawn_stdio_connection failed: {e}")
        
        # Test spawn_agent_process
        print("📦 Testing spawn_agent_process...")
        
        try:
            await acp.spawn_agent_process(agent)
            print("✅ spawn_agent_process worked!")
        except Exception as e:
            print(f"⚠️ spawn_agent_process failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Spawn functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_spawn_functions())
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")