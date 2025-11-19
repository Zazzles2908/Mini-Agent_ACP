"""
Verification script to check Mini-Agent Intelligence System setup
"""

import os
from pathlib import Path

def verify_intelligence_system():
    """Verify that the intelligence system is properly set up"""
    
    print("Mini-Agent Intelligence System Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Expected file structure
    expected_files = [
        "ai_agent_config.json",
        "self_awareness.py",
        "intelligent_decisions.py", 
        "real_time_monitor.py",
        "native_glm_integration.py",
        "mini_agent_intelligence.py",
        "test_native_glm.py",
        "README.md",
        ".env",
        "SYSTEM_CONFIG_ISSUE.md"
    ]
    
    print(f"\nChecking file structure...")
    
    found_files = []
    missing_files = []
    
    for file_name in expected_files:
        file_path = Path(file_name)
        if file_path.exists():
            found_files.append(file_name)
            print(f"   OK Found: {file_name}")
        else:
            missing_files.append(file_name)
            print(f"   ERROR Missing: {file_name}")
    
    # Check environment setup
    print(f"\nChecking environment setup...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("   OK .env file exists")
        with open(env_file, "r") as f:
            env_content = f.read()
            if "ZAI_API_KEY=" in env_content:
                print("   OK ZAI_API_KEY configuration found")
            else:
                print("   WARNING ZAI_API_KEY not found in .env")
    else:
        print("   ERROR .env file missing")
    
    # Check configuration
    config_file = Path("ai_agent_config.json")
    if config_file.exists():
        print("   OK Configuration file exists")
        import json
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                if config.get("model_config", {}).get("min_glm_model") == "glm4.5":
                    print("   OK GLM 4.5 minimum configured")
                else:
                    print("   WARNING GLM configuration issue")
        except:
            print("   ERROR Cannot parse configuration file")
    else:
        print("   ERROR Configuration file missing")
    
    # Summary
    print(f"\nVerification Summary:")
    print(f"   Files found: {len(found_files)}/{len(expected_files)}")
    print(f"   Files missing: {len(missing_files)}")
    
    if len(missing_files) == 0:
        print(f"\n✅ SYSTEM READY FOR USE!")
        print(f"\nNext steps:")
        print(f"1. Update .env with your API key if needed")
        print(f"2. Run: python test_native_glm.py")
        print(f"3. Integrate into main agent code")
    else:
        print(f"\n❌ SETUP INCOMPLETE")
        print(f"Missing files: {', '.join(missing_files)}")
    
    return {
        "ready": len(missing_files) == 0,
        "found_files": found_files,
        "missing_files": missing_files
    }

if __name__ == "__main__":
    result = verify_intelligence_system()