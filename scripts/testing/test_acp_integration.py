#!/usr/bin/env python3
"""Comprehensive ACP (Agent Client Protocol) integration test."""

import asyncio
import os
import sys
from pathlib import Path

# Add mini_agent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

async def test_acp_availability():
    """Test ACP package availability."""
    print("🔍 Testing ACP package availability...")
    
    try:
        import acp
        print(f"✅ ACP package available (version: {getattr(acp, '__version__', 'unknown')})")
        
        # Test key ACP imports
        from acp import AgentSideConnection, stdio_streams, PROTOCOL_VERSION
        print(f"✅ ACP core imports successful (Protocol version: {PROTOCOL_VERSION})")
        
        return True
    except ImportError as e:
        print(f"❌ ACP package import failed: {e}")
        return False

async def test_mini_agent_acp():
    """Test Mini-Agent ACP integration."""
    print("🔍 Testing Mini-Agent ACP integration...")
    
    try:
        # Test import
        from mini_agent.acp import MiniMaxACPAgent
        print("✅ Mini-Agent ACP module imports successfully")
        
        # Test basic instantiation parameters
        agent = MiniMaxACPAgent(
            conn=None,
            config=None,
            llm=None,
            base_tools=[],
            system_prompt="Test system prompt"
        )
        print("✅ Mini-MaxACPAgent instantiates successfully")
        
        return True
    except Exception as e:
        print(f"❌ Mini-Agent ACP integration failed: {e}")
        return False

async def test_vscode_extension():
    """Test VS Code extension configuration."""
    print("🔍 Testing VS Code extension configuration...")
    
    try:
        # Check package.json
        package_path = Path(__file__).parent.parent.parent / "vscode-extension" / "package.json"
        if not package_path.exists():
            print("❌ VS Code extension package.json not found")
            return False
        
        import json
        with open(package_path) as f:
            package_data = json.load(f)
        
        # Check required fields
        required_fields = ["name", "main", "contributes"]
        for field in required_fields:
            if field not in package_data:
                print(f"❌ Missing required field in package.json: {field}")
                return False
        
        print("✅ VS Code extension package.json is properly configured")
        print(f"  - Extension name: {package_data.get('name')}")
        print(f"  - Main file: {package_data.get('main')}")
        print(f"  - Commands: {len(package_data.get('contributes', {}).get('commands', []))}")
        
        return True
    except Exception as e:
        print(f"❌ VS Code extension test failed: {e}")
        return False

async def test_zai_integration():
    """Test Z.AI integration with ACP."""
    print("🔍 Testing Z.AI integration...")
    
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        # Test basic instantiation
        client = ZAIClient(os.getenv('ZAI_API_KEY'))
        print("✅ Z.AI client instantiates successfully")
        
        return True
    except Exception as e:
        print(f"❌ Z.AI integration test failed: {e}")
        return False

async def main():
    """Run all ACP integration tests."""
    print("🚀 Starting Mini-Agent ACP Integration Tests\n")
    
    tests = [
        ("ACP Package Availability", test_acp_availability),
        ("Mini-Agent ACP Integration", test_mini_agent_acp),
        ("VS Code Extension", test_vscode_extension),
        ("Z.AI Integration", test_zai_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"TEST: {test_name}")
        print('='*50)
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
        
        print()  # Add spacing between tests
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Mini-Agent ACP integration is ready.")
    else:
        print("⚠️  Some tests failed. Please check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())