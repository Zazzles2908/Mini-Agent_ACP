#!/usr/bin/env python3
"""Find the correct way to use the ACP library"""

import acp
import asyncio

async def test_acp_library():
    """Test different ways to use the ACP library"""
    
    print("🧪 Testing ACP library usage patterns...")
    
    try:
        # Check what's available in stdio module
        print("📦 Available in acp.stdio:", dir(acp.stdio))
        
        # Check what's in spawn functions
        print("📦 Available in spawn functions:")
        if hasattr(acp, 'spawn_agent_process'):
            print("spawn_agent_process available")
        if hasattr(acp, 'spawn_stdio_connection'):
            print("spawn_stdio_connection available")
        if hasattr(acp, 'spawn_stdio_transport'):
            print("spawn_stdio_transport available")
            
        # Test creating an Agent instance
        print("\n🧪 Testing Agent instantiation...")
        agent = acp.Agent()
        print("✅ Agent instance created")
        print("📋 Agent methods:", [m for m in dir(agent) if not m.startswith('_')])
        
        # Check if there are any example usages
        print("\n📖 Checking ACP examples...")
        
        return True
        
    except Exception as e:
        print(f"❌ ACP library test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_acp_library())
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")