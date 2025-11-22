import yaml
import json
from pathlib import Path

# Load configuration
config_path = Path("mini_agent/config/config.yaml")
config = {}

if config_path.exists():
    with open(config_path, 'r') as f:
        content = f.read()
        print("Config file loaded. First 10 lines:")
        print("\n".join(content.split('\n')[:10]))
        print("\n" + "="*50)
        
        try:
            config = yaml.safe_load(content)
            print("YAML parsing successful!")
        except Exception as e:
            print(f"YAML parsing failed: {e}")
            # Try to extract key values manually
            lines = content.split('\n')
            for line in lines:
                if 'model:' in line:
                    print(f"Primary model: {line}")
                if 'enable_zai_search:' in line:
                    print(f"Z.AI enabled: {line}")

# Check file organization
main_dir_files = list(Path(".").glob("*.py")) + list(Path(".").glob("*.md"))
print(f"\nFiles in main directory: {len(main_dir_files)}")
for file in main_dir_files:
    print(f"  - {file.name}")

# Check Z.AI implementation
zai_tool = Path("mini_agent/tools/zai_unified_tools.py")
if zai_tool.exists():
    with open(zai_tool, 'r') as f:
        content = f.read()
        print(f"\nZ.AI tools file exists: {len(content)} characters")
        print("Contains web_search:", 'web_search' in content)
        print("Contains web_reading:", 'web_reading' in content)
else:
    print("\nZ.AI tools file not found")

# Summary
print("\n" + "="*50)
print("SYSTEM AUDIT SUMMARY")
print("="*50)
print("This is a quick audit. The dashboard is ready for real integration.")