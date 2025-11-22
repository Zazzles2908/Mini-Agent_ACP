"""
MAIN DIRECTORY FIX GUIDELINES
============================
This file documents the correct file organization to prevent main directory clutter.

RULES TO ALWAYS FOLLOW:
1. NEVER create .py scripts in main directory - use scripts/utilities/
2. NEVER create .md files in main directory - use documents/
3. NEVER create .yaml files in main directory - use mini_agent/config/
4. ALWAYS check if files belong in existing subdirectories first

CORRECT LOCATIONS:
- Python scripts: scripts/utilities/
- Documentation: documents/
- Configuration: mini_agent/config/
- Core code: mini_agent/
- Testing: tests/

EXAMPLES OF INCORRECT (Will NOT do this):
- ❌ create "fix_script.py" in main directory
- ❌ create "README" in main directory  
- ❌ create "config.yaml" in main directory

EXAMPLES OF CORRECT (Will do this):
- ✅ scripts/utilities/system_reality_checker.py
- ✅ documents/system_reality_report.md
- ✅ mini_agent/config/custom_settings.yaml

CONSTRAINT: Every new file must have a proper subdirectory home.
"""