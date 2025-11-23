#!/usr/bin/env python3
"""
Real Z.AI Implementation Audit - Test what's actually operational
"""

import os
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("🔍 REAL Z.AI IMPLEMENTATION AUDIT")
print("="*50)

# Test 1: Import ALL 12 Z.AI implementations
print("\n📋 Testing imports for all 12 implementations...")

zai_files = [
    "mini_agent.llm.zai_client",
    "mini_agent.llm.claude_zai_client", 
    "mini_agent.llm.extended_claude_zai_client",
    "mini_agent.llm.coding_plan_zai_client",
    "mini_agent.tools.zai_unified_tools",
    "mini_agent.tools.claude_zai_tools",
    "mini_agent.tools.zai_web_tools", 
    "mini_agent.tools.zai_direct_api_tools",
    "mini_agent.tools.zai_direct_web_tools",
    "mini_agent.tools.zai_openai_tools",
    "mini_agent.tools.zai_openai_web_tools",
    "mini_agent.tools.zai_corrected_tools"
]

results = {
    "SUCCESS": [],
    "FAILED": []
}

for zai_file in zai_files:
    try:
        print(f"  Testing: {zai_file}")
        module = __import__(zai_file, fromlist=[''])
        print(f"    ✅ SUCCESS: {zai_file}")
        results["SUCCESS"].append(zai_file)
        
        # Check if it has specific classes
        if hasattr(module, 'ZAIClient'):
            print(f"      - Found ZAIClient")
        if hasattr(module, 'ZAIWebSearchTool'):
            print(f"      - Found ZAIWebSearchTool")
        if hasattr(module, 'ZAIWebReaderTool'): 
            print(f"      - Found ZAIWebReaderTool")
            
    except Exception as e:
        print(f"    ❌ FAILED: {zai_file} - {str(e)[:100]}")
        results["FAILED"].append(zai_file)

# Test 2: Check what the system ACTUALLY loads
print(f"\n🧠 Testing actual system loading...")

try:
    # This simulates what the system actually does
    print("  Loading mini_agent.tools...")
    import mini_agent.tools
    tools_available = mini_agent.tools.zai_tools_available()
    print(f"    Z.AI Tools Available: {tools_available}")
    
    print("  Loading mini_agent.llm...")
    import mini_agent.llm
    print(f"    Available LLM classes: {[cls for cls in dir(mini_agent.llm) if not cls.startswith('_')]}")
    
except Exception as e:
    print(f"    ❌ System loading failed: {e}")

# Test 3: Check credit protection behavior
print(f"\n💳 Testing credit protection logic...")

try:
    from mini_agent.utils.credit_protection import check_zai_protection
    protection_status = check_zai_protection()
    print(f"    Credit Protection Status: {protection_status}")
    print(f"    Type: {type(protection_status)}")
    
except Exception as e:
    print(f"    ❌ Credit protection check failed: {e}")

# Test 4: Configuration check
print(f"\n⚙️  Testing configuration...")

config_file = project_root / "mini_agent" / "config" / "config.yaml"
if config_file.exists():
    print(f"    ✅ Config file exists: {config_file}")
else:
    print(f"    ❌ Config file missing: {config_file}")

env_file = project_root / ".env"
if env_file.exists():
    print(f"    ✅ .env file exists: {env_file}")
    # Check for ZAI_API_KEY
    with open(env_file, 'r') as f:
        env_content = f.read()
        if 'ZAI_API_KEY' in env_content:
            print(f"    ✅ ZAI_API_KEY found in .env")
        else:
            print(f"    ⚠️  ZAI_API_KEY missing from .env")
else:
    print(f"    ❌ .env file missing: {env_file}")

# Summary
print(f"\n📊 AUDIT SUMMARY")
print(f"="*50)
print(f"✅ Successfully imported: {len(results['SUCCESS'])}/12")
print(f"❌ Failed imports: {len(results['FAILED'])}/12")

if results['SUCCESS']:
    print(f"\n📋 WORKING IMPLEMENTATIONS:")
    for item in results['SUCCESS']:
        print(f"  - {item}")

if results['FAILED']:
    print(f"\n❌ BROKEN IMPLEMENTATIONS:")
    for item in results['FAILED']:
        print(f"  - {item}")

print(f"\n🎯 CONCLUSION: Only {len(results['SUCCESS'])} of 12 implementations are actually working!")
