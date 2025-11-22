#!/usr/bin/env python3
"""
Debug Z.AI Credit Protection Logic
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def debug_credit_protection():
    """Debug the credit protection logic"""
    print("🔍 Debugging Z.AI Credit Protection...")
    
    try:
        from mini_agent.utils.credit_protection import (
            check_zai_protection, 
            get_config_zai_enabled, 
            is_zai_protected
        )
        
        print("🔍 Step 1: Config Check")
        config_enabled = get_config_zai_enabled()
        print(f"   Config Z.AI Enabled: {config_enabled}")
        
        print("🔍 Step 2: Protection Check")
        protection_allowed = check_zai_protection()
        print(f"   Check Z.AI Protection: {protection_allowed}")
        
        print("🔍 Step 3: Global Protection Status")
        protection_active = is_zai_protected()
        print(f"   Global Protection Active: {protection_active}")
        
        print("🔍 Step 4: Environment Variables")
        zai_key = os.getenv('ZAI_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        print(f"   ZAI_API_KEY: {'Set' if zai_key else 'Not Set'}")
        print(f"   OPENAI_API_KEY: {'Set' if openai_key else 'Not Set'}")
        
        print("\n📊 RESULT:")
        if config_enabled and protection_allowed:
            print("✅ Z.AI should be ENABLED")
        elif config_enabled and not protection_allowed:
            print("❌ Protection blocking despite config enabled")
        elif not config_enabled and protection_allowed:
            print("⚠️  Config disabled but protection allowing")
        else:
            print("✅ Z.AI properly disabled")
            
        return config_enabled, protection_allowed
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        return False, False

def main():
    """Main debug function"""
    print("🚀 Z.AI Credit Protection Debug")
    print("=" * 50)
    
    config_enabled, protection_allowed = debug_credit_protection()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print(f"   Config Enabled: {config_enabled}")
    print(f"   Protection Allowing: {protection_allowed}")
    
    return config_enabled, protection_allowed

if __name__ == "__main__":
    main()