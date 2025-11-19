"""Quick test of mini-agent CLI startup."""
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Change to project directory so .env is found
import os
os.chdir(project_root)

print("Testing mini-agent CLI...")
print(f"Current directory: {Path.cwd()}")
print(f".env exists: {(Path.cwd() / '.env').exists()}")

# Test import
try:
    from mini_agent.cli import main
    print("✅ CLI module imported successfully")
except Exception as e:
    print(f"❌ Failed to import CLI: {e}")
    sys.exit(1)

# Test .env loading
from dotenv import load_dotenv
load_dotenv()
import os
zai_key = os.getenv("ZAI_API_KEY")
print(f"✅ ZAI_API_KEY loaded: {bool(zai_key)}")
if zai_key:
    print(f"   Preview: {zai_key[:30]}...")

print("\n✅ All imports and environment loading working!")
print("\nTo run mini-agent:")
print("1. cd C:\\Users\\Jazeel-Home\\Mini-Agent")
print("2. python -m mini_agent.cli --workspace .")
