"""
Z.AI Credit Protection Module - FIXED VERSION

This module provides hard protection against Z.AI credit consumption
by blocking all direct Z.AI tool and client usage when disabled in config.

FIXED: Now properly reads config to determine if Z.AI should be enabled.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Global protection flag - start with safe default (protected)
_ZAI_PROTECTION_ACTIVE = True

def is_zai_protected() -> bool:
    """Check if Z.AI credit protection is active"""
    global _ZAI_PROTECTION_ACTIVE
    return _ZAI_PROTECTION_ACTIVE

def get_config_zai_enabled() -> bool:
    """
    Get Z.AI enable status from config file.
    
    Returns:
        True if Z.AI is explicitly enabled in config, False otherwise (safe default)
    """
    try:
        # Import here to avoid circular dependencies
        import yaml
        
        # Try multiple config paths
        config_paths = [
            Path.cwd() / "mini_agent" / "config" / "config.yaml",
            Path.cwd() / "config.yaml",
            Path.home() / ".mini-agent" / "config.yaml"
        ]
        
        config_data = None
        config_path_used = None
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        config_path_used = config_path
                        break
                except Exception as e:
                    print(f"Warning: Failed to read config {config_path}: {e}")
                    continue
        
        if config_data is None:
            print("⚠️  No config file found - Z.AI protection active (safe default)")
            return False
            
        # Check Z.AI configuration
        tools_data = config_data.get('tools', {})
        search_enabled = tools_data.get('enable_zai_search', False)
        llm_enabled = tools_data.get('enable_zai_llm', False)
        
        zai_enabled = search_enabled or llm_enabled
        
        if zai_enabled:
            print(f"✅ Z.AI enabled in config ({config_path_used}) - Credits will be consumed")
        else:
            print(f"✅ Z.AI disabled in config ({config_path_used}) - Credit protection active")
            
        return zai_enabled
        
    except Exception as e:
        print(f"⚠️  Config check failed - Z.AI protection active (safe default): {e}")
        return False

def check_zai_protection() -> bool:
    """
    Check if Z.AI tools should be allowed based on config.
    
    Returns:
        True if Z.AI is enabled (credits will be consumed), False if protected
    """
    # Check config to determine if Z.AI should be enabled
    zai_enabled = get_config_zai_enabled()
    
    # Return True if Z.AI is enabled, False if protection is active
    return zai_enabled

def block_zai_usage(tool_name: str = "Unknown Z.AI Tool"):
    """
    Block Z.AI tool usage with clear error message.
    
    Args:
        tool_name: Name of the Z.AI tool that was attempted to be used
    """
    protection_status = "ACTIVE" if is_zai_protected() else "DISABLED"
    
    error_msg = f"""
🚫 Z.AI CREDIT PROTECTION BLOCKED

Tool: {tool_name}
Protection Status: {protection_status}

This Z.AI tool is disabled to protect your credits.
To enable Z.AI functionality:

1. Edit mini_agent/config/config.yaml
2. Set these values to true:
   enable_zai_search: true
   enable_zai_llm: true

⚠️  WARNING: Enabling Z.AI will consume credits from your account.

Current Status:
- MiniMax-M2: ✅ Active (300 prompts/5hrs quota)
- Z.AI Tools: ❌ Disabled (Credit Protected)
- Native Tools: ✅ Active (Unlimited)
"""
    
    print(error_msg)
    raise RuntimeError(f"Z.AI tool '{tool_name}' is disabled for credit protection")

# Initialize protection status on module import
try:
    if check_zai_protection():
        _ZAI_PROTECTION_ACTIVE = False
        print("✅ Z.AI tools enabled - Credit consumption active")
    else:
        _ZAI_PROTECTION_ACTIVE = True
        print("🔒 Z.AI Credit Protection: ACTIVE - All Z.AI tools blocked")
except Exception as e:
    # On any error, default to protection active (safe default)
    _ZAI_PROTECTION_ACTIVE = True
    print(f"🔒 Z.AI Credit Protection: ACTIVE (config error) - {e}")
