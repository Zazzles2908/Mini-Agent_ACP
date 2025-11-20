#!/usr/bin/env python3
"""Debug environment variable loading"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=== Environment Variable Debug ===")
print(f"Current working directory: {Path.cwd()}")
print(f".env file path: {Path.cwd() / '.env'}")
print(f".env file exists: {(Path.cwd() / '.env').exists()}")

# Try loading .env
env_file = Path.cwd() / ".env"
if env_file.exists():
    load_dotenv(env_file, override=False)
    print("✅ .env file loaded successfully")
else:
    print("❌ .env file not found")

print(f"MINIMAX_API_KEY from env: {os.getenv('MINIMAX_API_KEY') is not None}")
print(f"ZAI_API_KEY from env: {os.getenv('ZAI_API_KEY') is not None}")

if os.getenv('MINIMAX_API_KEY'):
    print(f"MINIMAX_API_KEY length: {len(os.getenv('MINIMAX_API_KEY'))}")
    print(f"MINIMAX_API_KEY starts with: {os.getenv('MINIMAX_API_KEY')[:20]}...")

# Test config loading
print("\n=== Testing Config Loading ===")
try:
    from mini_agent.config import Config
    config = Config.load()
    print("✅ Config loaded successfully")
    print(f"API Key loaded: {config.llm.api_key is not None}")
    print(f"API Base: {config.llm.api_base}")
    print(f"Provider: {config.llm.provider}")
except Exception as e:
    print(f"❌ Config loading failed: {e}")
    import traceback
    traceback.print_exc()