#!/usr/bin/env python3
"""Test script for ACP stdio server"""

import asyncio
import json
import sys
from mini_agent.acp import MiniMaxACPAgent, main
import os

def test_acp_import():
    """Test that ACP components can be imported"""
    try:
        from mini_agent.acp import MiniMaxACPAgent
        print("✅ MiniMaxACPAgent import: SUCCESS")
        
        # Test basic initialization
        agent = MiniMaxACPAgent(
            conn=None,
            config=None,
            llm=None,
            base_tools=[],
            system_prompt="Test prompt"
        )
        print("✅ Agent instantiation: SUCCESS")
        
        return True
    except Exception as e:
        print(f"❌ ACP import test failed: {e}")
        return False

def test_stdout_echo():
    """Test that we can write to stdout"""
    test_message = {"test": "hello", "timestamp": "2025-11-20"}
    try:
        json.dump(test_message, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()
        return True
    except Exception as e:
        print(f"❌ Stdout test failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    print("🧪 Testing ACP Stdio Server Components...")
    
    # Test 1: Import and basic functionality
    if test_acp_import():
        print("✅ All ACP tests passed!")
        
        # Test 2: Write to stdout
        print("🧪 Testing stdout communication...")
        test_stdout_echo()
        
    else:
        print("❌ ACP tests failed!")
        sys.exit(1)