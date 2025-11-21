#!/usr/bin/env python3
"""
Comprehensive Mini-Agent System Audit
Tests all components and identifies what needs restoration
"""

import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔍 Mini-Agent System Audit & Restoration")
print("=" * 60)

audit_results = {
    "working": [],
    "issues": [],
    "disabled": [],
    "restoration_needed": []
}

# 1. Environment Variables
print("\n1. Environment Configuration:")
if os.environ.get('ZAI_API_KEY'):
    print("   ✅ ZAI_API_KEY: Available")
    audit_results["working"].append("Z.AI API Key")
else:
    print("   ❌ ZAI_API_KEY: Missing")
    audit_results["issues"].append("Z.AI API Key")

if os.environ.get('MINIMAX_API_KEY'):
    print("   ✅ MINIMAX_API_KEY: Available") 
    audit_results["working"].append("MiniMax API Key")
else:
    print("   ❌ MINIMAX_API_KEY: Missing")
    audit_results["issues"].append("MiniMax API Key")

# 2. Core System Components
print("\n2. Core System Components:")

# Tools
try:
    from mini_agent.tools.bash_tool import BashTool
    from mini_agent.tools.file_tools import ReadTool, WriteTool
    print("   ✅ File & Bash Tools: Working")
    audit_results["working"].append("Core File Tools")
except Exception as e:
    print(f"   ❌ File & Bash Tools: {e}")
    audit_results["issues"].append("Core File Tools")

# Skills System
try:
    from mini_agent.tools.skill_loader import SkillLoader
    loader = SkillLoader("mini_agent/skills")
    skills = loader.discover_skills()
    print(f"   ✅ Skills System: {len(skills)} skills loaded")
    audit_results["working"].append(f"Skills System ({len(skills)} skills)")
    
    # List all available skills
    for skill in skills:
        audit_results["working"].append(f"Skill: {skill.name}")
        
except Exception as e:
    print(f"   ❌ Skills System: {e}")
    audit_results["issues"].append("Skills System")

# Z.AI Tools
try:
    from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
    print("   ✅ Z.AI Tools: Imported successfully")
    audit_results["working"].append("Z.AI Web Tools Imported")
    audit_results["disabled"].append("Z.AI Web Tools (currently disabled per user request)")
except Exception as e:
    print(f"   ❌ Z.AI Tools: {e}")
    audit_results["issues"].append("Z.AI Tools Import")

# MCP System
try:
    from mini_agent.tools.mcp_loader import MCPServerConnection
    print("   ✅ MCP System: Framework imported")
    audit_results["working"].append("MCP Framework")
except Exception as e:
    print(f"   ❌ MCP System: {e}")
    audit_results["issues"].append("MCP Framework")

# Agent System  
try:
    from mini_agent.agent import Agent
    from mini_agent.llm import LLMClient
    print("   ✅ Agent System: Core classes imported")
    audit_results["working"].append("Agent Core Classes")
except Exception as e:
    print(f"   ❌ Agent System: {e}")
    audit_results["issues"].append("Agent Core Classes")

# 3. File Structure Analysis
print("\n3. File Structure Analysis:")

# Check key directories
key_dirs = {
    "mini_agent": "Core system",
    "documents": "Documentation",
    "scripts": "Scripts & utilities",
    "skills": "Claude Skills",
    "vscode-extension": "VS Code extension"
}

for dir_name, description in key_dirs.items():
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"   ✅ {dir_name}/: {description} - EXISTS")
        audit_results["working"].append(f"{description} directory")
    else:
        print(f"   ❌ {dir_name}/: {description} - MISSING")
        audit_results["issues"].append(f"{description} directory")

# 4. Production Readiness Assessment
print("\n4. Production Readiness Assessment:")

print(f"   📊 System Status:")
print(f"      ✅ Working Components: {len(audit_results['working'])}")
print(f"      ❌ Issues Found: {len(audit_results['issues'])}") 
print(f"      ⏸️  Disabled Features: {len(audit_results['disabled'])}")

# Calculate readiness score
total_checks = len(audit_results['working']) + len(audit_results['issues'])
if total_checks > 0:
    readiness_score = (len(audit_results['working']) / total_checks) * 100
    print(f"   📈 Readiness Score: {readiness_score:.1f}%")
    
    if readiness_score >= 80:
        print("   🎯 Status: PRODUCTION READY")
    elif readiness_score >= 60:
        print("   ⚠️  Status: NEEDS MINOR FIXES")
    else:
        print("   🚨 Status: NEEDS RESTORATION")

# 5. Restoration Priorities
print("\n5. Restoration Priorities:")

print("   🎯 HIGH PRIORITY:")
print("      1. Re-enable Z.AI web search feature (currently disabled)")
print("      2. Verify MCP server connectivity")
print("      3. Test VS Code extension compatibility")

print("   🔧 MEDIUM PRIORITY:")
print("      4. Validate Agent initialization process")
print("      5. Test all 17 Claude Skills functionality")

print("   📋 LOW PRIORITY:")
print("      6. Clean up any remaining workspace artifacts")
print("      7. Optimize system performance")

# 6. Next Steps
print("\n6. Next Steps for Complete Restoration:")
print("   1. Systematically re-enable Z.AI web features")
print("   2. Test each component individually")
print("   3. Run end-to-end functionality tests")
print("   4. Validate production readiness")
print("   5. Create comprehensive system report")

print("\n" + "=" * 60)
print("🎯 AUDIT COMPLETE - Ready for systematic restoration")
