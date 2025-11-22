#!/usr/bin/env python3
"""
Quick Z.AI Web Search Enabler
============================
Simple script to enable/disable Z.AI web search functionality.
Addresses user's "snippet only" problem.
"""

import yaml
import os
from pathlib import Path

def enable_zai_web_search():
    """Enable Z.AI web search in config"""
    config_path = Path("mini_agent/config/config.yaml")
    
    # Read current config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Enable web search
    config['tools']['enable_zai_search'] = True
    config['tools']['enable_zai_llm'] = True
    
    # Save updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print("✅ Z.AI web search ENABLED")
    print("   ⚠️  This will consume ~120 prompts/5hrs from coding plan")
    print("   🔄 You may need to restart the agent for changes to take effect")

def disable_zai_web_search():
    """Disable Z.AI web search in config (safety mode)"""
    config_path = Path("mini_agent/config/config.yaml")
    
    # Read current config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Disable web search
    config['tools']['enable_zai_search'] = False
    config['tools']['enable_zai_llm'] = False
    
    # Save updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print("✅ Z.AI web search DISABLED (credit protection active)")

def check_status():
    """Check current Z.AI status"""
    config_path = Path("mini_agent/config/config.yaml")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    search_enabled = config.get('tools', {}).get('enable_zai_search', False)
    llm_enabled = config.get('tools', {}).get('enable_zai_llm', False)
    
    print(f"🔍 Z.AI Search Status: {'ENABLED' if search_enabled else 'DISABLED'}")
    print(f"🤖 Z.AI LLM Status: {'ENABLED' if llm_enabled else 'DISABLED'}")
    
    if search_enabled:
        print("   ✅ Full web search results should be available")
        print("   ⚠️  Monitor coding plan usage (~120 prompts/5hrs)")
    else:
        print("   ❌ Only snippets/limited results will be shown")
        print("   💡 Run this script with 'enable' to fix snippet problem")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python zai_web_toggle.py [enable|disable|status]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "enable":
        enable_zai_web_search()
    elif command == "disable":
        disable_zai_web_search()
    elif command == "status":
        check_status()
    else:
        print("Invalid command. Use: enable, disable, or status")