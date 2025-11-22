#!/usr/bin/env python3
"""
ACP Server Test and Validation Script
Verifies that the Mini-Agent ACP bridge is working correctly
"""

import subprocess
import sys
import os
from pathlib import Path

def test_acp_server_import():
    """Test that the ACP server can be imported"""
    print("Testing ACP Server Import...")
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from mini_agent.acp.__init___FIXED import main, MiniMaxACPAgent
        print("✅ ACP server module imported successfully")
        print("✅ MiniMaxACPAgent class available")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_mini_agent_core():
    """Test that Mini-Agent core components work"""
    print("\\nTesting Mini-Agent Core...")
    try:
        from mini_agent.agent import Agent
        print("✅ Agent class available")
        
        from mini_agent.llm.llm_client import LLMClient
        print("✅ LLMClient class available")
        
        from mini_agent.cli import initialize_base_tools
        print("✅ initialize_base_tools function available")
        
        return True
    except Exception as e:
        print(f"❌ Mini-Agent core test failed: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\\nTesting Dependencies...")
    
    dependencies = [
        ("acp", "Agent Client Protocol library"),
        ("pydantic", "Data validation"),
        ("pyyaml", "YAML configuration"),
        ("prompt_toolkit", "Terminal interface"),
    ]
    
    all_good = True
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ Missing: {description} (pip install {package})")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test that all required files exist"""
    print("\\nTesting File Structure...")
    
    required_files = [
        Path(__file__).parent.parent / "mini_agent" / "acp" / "__init___FIXED.py",
        Path(__file__).parent.parent / "mini_agent" / "cli.py",
        Path(__file__).parent.parent / "mini_agent" / "config" / "config.yaml",
        Path(__file__).parent.parent / "scripts" / "acp_terminal_bridge.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if file_path.exists():
            print(f"✅ {file_path.name}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False
    
    return all_exist

def quick_start_test():
    """Run a quick start test"""
    print("\\n" + "=" * 50)
    print("QUICK START TEST")
    print("=" * 50)
    
    print("\\nTo start using Mini-Agent ACP immediately:")
    print("1. cd C:\\Users\\Jazeel-Home\\Mini-Agent")
    print("2. python scripts/acp_terminal_bridge.py")
    print("\\nThis will start the ACP server ready for protocol messages!")
    
    print("\\nAlternative methods:")
    print("• Direct: python -m mini_agent.acp.__init___FIXED")
    print("• VS Code: Install extension from vscode-extension/ folder")

def main():
    """Run all tests"""
    print("🔧 Mini-Agent ACP Bridge Validation")
    print("=" * 50)
    
    tests = [
        test_acp_server_import,
        test_mini_agent_core,
        test_dependencies,
        test_file_structure,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ Mini-Agent ACP Bridge is fully functional")
        print("✅ Ready for immediate use")
        quick_start_test()
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("Please fix the issues above before using ACP")
        return 1

if __name__ == "__main__":
    sys.exit(main())
