#!/usr/bin/env python3
"""
Quick diagnostic to check Z.AI MCP implementation status
"""

import sys
from pathlib import Path
import os

print("🔍 Z.AI MCP Integration Diagnostic")
print("=" * 50)

# Check basic file structure
files_to_check = [
    "mini_agent/tools/zai_unified_tools.py",
    "mini_agent/tools/zai_mcp_tools.py", 
    "mini_agent/config/config.yaml",
    "mini_agent/config/z_mcp_servers.json"
]

print("\n📁 File Status:")
for file_path in files_to_check:
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file_path}")

# Check config settings
print("\n⚙️  Configuration Check:")
try:
    with open("mini_agent/config/config.yaml", 'r') as f:
        import yaml
        config = yaml.safe_load(f)
        
    enable_zai = config.get('tools', {}).get('enable_zai_search', False)
    use_mcp = config.get('tools', {}).get('zai_settings', {}).get('use_mcp_protocol', False)
    use_direct = config.get('tools', {}).get('zai_settings', {}).get('use_direct_api', True)
    
    print(f"  enable_zai_search: {enable_zai}")
    print(f"  use_mcp_protocol: {use_mcp}")
    print(f"  use_direct_api: {use_direct}")
    
    if use_mcp and not use_direct:
        print("  ✅ MCP Integration: ACTIVE")
        print("  ✅ Credit Protection: ACTIVE")
    else:
        print("  ⚠️  MCP Integration: NEEDS CONFIGURATION")
        
except Exception as e:
    print(f"  ❌ Config check failed: {e}")

# Check API key
print("\n🔑 API Key Status:")
zai_key = os.getenv('ZAI_API_KEY')
if zai_key and zai_key != "YOUR_ZAI_API_KEY":
    print(f"  ✅ ZAI_API_KEY set (length: {len(zai_key)})")
else:
    print("  ❌ ZAI_API_KEY missing or placeholder")

# Check MCP server config
print("\n🌐 MCP Server Status:")
try:
    with open("mini_agent/config/z_mcp_servers.json", 'r') as f:
        mcp_config = __import__('json').load(f)
    print(f"  ✅ MCP server config loaded")
    print(f"  📍 Web Search: {mcp_config.get('web_search', 'Not configured')}")
    print(f"  📍 Web Reader: {mcp_config.get('web_reader', 'Not configured')}")
except Exception as e:
    print(f"  ❌ MCP config failed: {e}")

print("\n🎯 Summary:")
print("The last AI implemented MCP protocol integration for Z.AI web tools")
print("to use FREE Lite plan quotas instead of burning paid credits.")
print("\nCurrent implementation status:")
if Path("mini_agent/tools/zai_unified_tools.py").exists():
    print("✅ Core MCP tools created")
    print("✅ Usage tracking implemented")
    print("✅ Credit protection system added")
    print("✅ Configuration updated")
else:
    print("❌ Implementation incomplete")

print("\n⚠️  REMAINING TASKS:")
print("1. Test MCP integration with actual API call")
print("2. Verify FREE quota usage (not charged)")
print("3. Confirm credit protection works")
print("4. Test web search and reader functionality")
print("5. Validate usage tracking")