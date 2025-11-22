#!/usr/bin/env python3
"""
System Health Check Script
Tests core Mini-Agent functionality and system components
"""

import sys
import os
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔍 Mini-Agent System Health Check")
print("=" * 50)

# Test environment variables
print("\n1. Environment Variables:")
zapi = os.environ.get('ZAI_API_KEY')
mapi = os.environ.get('MINIMAX_API_KEY')
print(f"   ZAI_API_KEY: {'✅ Available' if zapi else '❌ Missing'}")
print(f"   MINIMAX_API_KEY: {'✅ Available' if mapi else '❌ Missing'}")

# Test core imports
print("\n2. Core System Imports:")
try:
    from mini_agent.agent import Agent
    print("   ✅ Agent class imported")
except Exception as e:
    print(f"   ❌ Agent import failed: {e}")

try:
    from mini_agent.tools import get_tools
    tools = get_tools()
    print(f"   ✅ Tools system working: {len(tools)} tools available")
except Exception as e:
    print(f"   ❌ Tools system failed: {e}")

try:
    from mini_agent.skills import list_skills
    skills = list_skills()
    print(f"   ✅ Skills system working: {len(skills)} skills available")
except Exception as e:
    print(f"   ❌ Skills system failed: {e}")

print("\n3. System Summary:")
print("   📊 Basic functionality test complete")
print("   🎯 Ready for detailed component testing")
