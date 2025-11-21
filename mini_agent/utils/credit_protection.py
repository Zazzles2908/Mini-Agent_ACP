"""
Z.AI Credit Protection Module

This module provides hard protection against Z.AI credit consumption
by blocking all direct Z.AI tool and client usage when disabled in config.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Global protection flag
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
        # Add project root to path if not already there
        project_root = Path(__file__).parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
            
        # Try to load config
        from mini_agent.config import Config
        
        config_path = Config.get_default_config_path()
        if not config_path.exists():
            print("⚠️  No config file found - Z.AI protection active (safe default)")
            return False
            
        config = Config.from_yaml(config_path)
        
        # Check both Z.AI flags - both must be True to enable
        search_enabled = getattr(config.tools, 'enable_zai_search', False)
        llm_enabled = getattr(config.tools, 'enable_zai_llm', False)
        
        zai_enabled = search_enabled or llm_enabled
        
        if zai_enabled:
            print("⚠️  Z.AI enabled in config - Credits will be consumed")
        else:
            print("✅ Z.AI disabled in config - Credit protection active")
            
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
    # Always start with protection active (safe default)
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

# Global check on module import
if check_zai_protection():
    _ZAI_PROTECTION_ACTIVE = False
else:
    _ZAI_PROTECTION_ACTIVE = True
    print("🔒 Z.AI Credit Protection: ACTIVE - All Z.AI tools blocked")
