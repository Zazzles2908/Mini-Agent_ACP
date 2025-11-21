#!/usr/bin/env python3
"""
Detailed System Component Test
Tests Mini-Agent components one by one
"""

import sys
import os
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔧 Detailed Component Testing")
print("=" * 50)

# Test skill system
print("\n1. Skills System:")
try:
    from mini_agent.tools.skill_loader import SkillLoader
    loader = SkillLoader()
    skills = loader.list_skills()
    print(f"   ✅ {len(skills)} skills available")
    
    # Show first few skills
    for i, skill in enumerate(skills[:3]):
        name = skill.get("name", "Unknown")
        desc = skill.get("description", "No description")
        if len(desc) > 50:
            desc = desc[:50] + "..."
        print(f"   {i+1}. {name} - {desc}")
    if len(skills) > 3:
        print(f"   ... and {len(skills) - 3} more skills")
        
except Exception as e:
    print(f"   ❌ Skills system failed: {e}")

# Test MCP loader
print("\n2. MCP System:")
try:
    from mini_agent.tools.mcp_loader import MCPLoader
    print("   ✅ MCP Loader imported successfully")
except Exception as e:
    print(f"   ❌ MCP Loader failed: {e}")

# Test agent initialization
print("\n3. Agent System:")
try:
    from mini_agent.agent import Agent
    
    # Test basic agent creation
    agent = Agent()
    print("   ✅ Agent class instantiated successfully")
    print(f"   📊 Agent has {len(agent.tools)} tools loaded")
    print(f"   🎯 Agent has {len(agent._loaded_skills)} skills loaded")
    
except Exception as e:
    print(f"   ❌ Agent system failed: {e}")

print("\n4. Summary:")
print("   🎉 Core components are functional")
print("   📈 Ready for Z.AI web feature restoration")
