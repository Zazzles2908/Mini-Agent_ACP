"""Test environment variable loading."""
import os
from pathlib import Path

# Check if python-dotenv is available
try:
    from dotenv import load_dotenv
    has_dotenv = True
except ImportError:
    has_dotenv = False
    print("⚠️  python-dotenv not installed")

print("\n" + "="*50)
print("ENVIRONMENT VARIABLE TEST")
print("="*50 + "\n")

# Check .env file
env_path = Path(".env")
print(f"1. .env file exists: {env_path.exists()}")

if env_path.exists():
    with open(env_path) as f:
        content = f.read()
        print(f"2. .env content length: {len(content)} bytes")
        if "ZAI_API_KEY" in content:
            print("3. ZAI_API_KEY found in .env file ✅")
        else:
            print("3. ZAI_API_KEY NOT found in .env file ❌")

# Try loading with dotenv
if has_dotenv:
    print("\n4. Loading with python-dotenv:")
    load_dotenv(env_path)
    key = os.getenv("ZAI_API_KEY")
    if key:
        print(f"   ✅ ZAI_API_KEY loaded: {key[:30]}...")
    else:
        print("   ❌ ZAI_API_KEY not loaded")
else:
    print("\n4. python-dotenv not available")
    print("   Install with: pip install python-dotenv")

# Check direct environment
print("\n5. Direct environment check:")
key = os.environ.get("ZAI_API_KEY")
if key:
    print(f"   ✅ ZAI_API_KEY in environment: {key[:30]}...")
else:
    print("   ❌ ZAI_API_KEY not in environment")

print("\n" + "="*50)

# Solution
if not has_dotenv:
    print("\n💡 SOLUTION:")
    print("   Install python-dotenv:")
    print("   pip install python-dotenv")
    print("\n   OR set environment variable directly:")
    print("   $env:ZAI_API_KEY = '7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe'")
