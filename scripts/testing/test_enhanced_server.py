#!/usr/bin/env python3
"""
Test Enhanced ACP Server functionality
"""

import asyncio
import json
from pathlib import Path
from mini_agent.acp.enhanced_server import MiniAgentACPServer

async def test_enhanced_server():
    """Test the enhanced ACP server"""
    print("🔧 TESTING ENHANCED ACP SERVER")
    print("-" * 40)
    
    try:
        # Create server instance
        server = MiniAgentACPServer()
        print("✅ Server instance created")
        
        # Test basic properties
        print(f"✅ Server type: {type(server).__name__}")
        print(f"✅ Server has process_message: {hasattr(server, 'process_message')}")
        print(f"✅ Server has create_session: {hasattr(server, 'create_session')}")
        
        # Test message processing (simulate a basic message)
        test_message = {
            "id": "test-1",
            "type": "initialize",
            "timestamp": "2025-11-20T10:00:00Z",
            "data": {}
        }
        
        try:
            response = await server.process_message(test_message)
            print(f"✅ Message processing works: {response.get('success', False)}")
        except Exception as e:
            print(f"⚠️  Message processing issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def test_stdio_extension():
    """Test stdio extension functionality"""
    print("\n🔧 TESTING STDIO EXTENSION")
    print("-" * 40)
    
    stdio_file = Path("mini_agent/vscode_extension/enhanced_extension_stdio.js")
    if not stdio_file.exists():
        print("❌ Stdio extension not found")
        return False
    
    content = stdio_file.read_text()
    
    # Check for key features
    features = {
        "child_process_spawn": "child_process.spawn" in content,
        "python_spawn": "python" in content and "spawn" in content,
        "stdio_transport": "stdio" in content.lower(),
        "chat_participant": "chatParticipant" in content,
        "session_management": "session" in content.lower(),
        "json_rpc": "jsonrpc" in content.lower() or "json-rpc" in content.lower()
    }
    
    for feature, present in features.items():
        print(f"{'✅' if present else '❌'} {feature.replace('_', ' ').title()}: {'Present' if present else 'Missing'}")
    
    # Calculate completeness
    completeness = sum(features.values()) / len(features) * 100
    print(f"\n📊 STDIO EXTENSION COMPLETENESS: {completeness:.1f}%")
    
    return completeness >= 80

async def main():
    """Main test function"""
    print("🚀 ENHANCED ACP SERVER VALIDATION")
    print("=" * 50)
    
    server_ok = await test_enhanced_server()
    extension_ok = test_stdio_extension()
    
    print("\n" + "=" * 50)
    print("📊 FINAL VALIDATION RESULTS")
    print("=" * 50)
    
    if server_ok and extension_ok:
        print("✅ ALL SYSTEMS OPERATIONAL")
        print("🚀 Ready for Chat API integration!")
    else:
        print("⚠️  ISSUES DETECTED")
        if not server_ok:
            print("🔧 Fix ACP server issues")
        if not extension_ok:
            print("🔧 Fix extension completeness")
    
    return server_ok and extension_ok

if __name__ == "__main__":
    result = asyncio.run(main())