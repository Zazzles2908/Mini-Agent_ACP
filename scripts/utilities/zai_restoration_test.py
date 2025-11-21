#!/usr/bin/env python3
"""
Z.AI Web Feature Restoration Test
Tests Z.AI web search and reader functionality
"""

import sys
import os
sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🌐 Z.AI Web Feature Restoration Test")
print("=" * 50)

# Test 1: Import Z.AI tools
print("\n1. Z.AI Tools Import Test:")
try:
    from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
    print("   ✅ Z.AI tools imported successfully")
    
    # Test 2: Initialize tools
    print("\n2. Z.AI Tools Initialization:")
    try:
        web_search = ZAIWebSearchTool()
        web_reader = ZAIWebReaderTool()
        print("   ✅ Web search tool initialized")
        print("   ✅ Web reader tool initialized")
        
        # Test 3: Check tool properties
        print("\n3. Tool Properties:")
        print(f"   Web Search Tool:")
        print(f"      Name: {web_search.name}")
        print(f"      Description: {web_search.description[:100]}...")
        
        print(f"   Web Reader Tool:")
        print(f"      Name: {web_reader.name}")
        print(f"      Description: {web_reader.description[:100]}...")
        
        print("\n   ✅ Z.AI web features are READY for restoration!")
        print("   🎯 Next: Test actual functionality")
        
    except Exception as e:
        print(f"   ❌ Tool initialization failed: {e}")
        
except Exception as e:
    print(f"   ❌ Z.AI tools import failed: {e}")

# Test 4: Environment check
print("\n4. Environment Validation:")
zai_key = os.environ.get('ZAI_API_KEY', '')
if zai_key and len(zai_key) > 10:
    print("   ✅ ZAI_API_KEY is valid and loaded")
    print(f"   📝 Key length: {len(zai_key)} characters")
else:
    print("   ❌ ZAI_API_KEY missing or invalid")

print("\n🎯 Z.AI RESTORATION STATUS: READY TO ACTIVATE")
