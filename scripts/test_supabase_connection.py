#!/usr/bin/env python3
"""
Test Supabase Connection and Verify Setup
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("🧪 Testing Supabase Connection...")
print("=" * 50)

# Check environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

print(f"\n1️⃣ Environment Variables:")
print(f"   SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
print(f"   SUPABASE_SERVICE_KEY: {'✅ Set' if supabase_key else '❌ Missing'}")

if not supabase_url or not supabase_key:
    print("\n❌ Missing required environment variables!")
    print("Add them to your .env file:")
    print("  SUPABASE_URL=https://your-project.supabase.co")
    print("  SUPABASE_SERVICE_KEY=your_service_role_key")
    sys.exit(1)

print(f"\n2️⃣ Supabase Configuration:")
print(f"   URL: {supabase_url}")
print(f"   Key: {supabase_key[:20]}...")

# Try to import supabase
try:
    from supabase import create_client, Client
    print("\n3️⃣ Supabase Python Client: ✅ Installed")
except ImportError:
    print("\n3️⃣ Supabase Python Client: ❌ Not installed")
    print("   Run: uv pip install supabase")
    sys.exit(1)

# Connect to Supabase
print("\n4️⃣ Connecting to Supabase...")
try:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("   ✅ Connection established")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    sys.exit(1)

# Test basic operations
print("\n5️⃣ Testing Database Operations...")

# Try to list tables (might fail if RPC doesn't exist yet)
try:
    # First test: Check if we can access any table
    # This will help us understand if our connection has proper permissions
    result = supabase.table("mini_agent_projects").select("*").limit(1).execute()
    print("   ✅ Can query mini_agent_projects table")
    print(f"   📊 Existing rows: {len(result.data)}")
except Exception as e:
    error_str = str(e)
    if "relation" in error_str and "does not exist" in error_str:
        print("   ⚠️ mini_agent_projects table doesn't exist yet")
        print("   📝 Run the migration SQL to create tables:")
        print("      migrations/001_mini_agent_memory_schema.sql")
    else:
        print(f"   ⚠️ Query test: {e}")

# Try to insert a test project
print("\n6️⃣ Testing Insert Operation...")
try:
    test_data = {
        "project_id": "test_connection_check",
        "context": {"test": True, "purpose": "connection_verification"},
        "metadata": {"created_by": "test_supabase_connection.py"}
    }
    
    # Try to upsert (insert or update)
    result = supabase.table("mini_agent_projects").upsert(test_data).execute()
    print("   ✅ Insert/Upsert successful")
    print(f"   📊 Result: {result.data}")
    
    # Clean up test data
    supabase.table("mini_agent_projects").delete().eq("project_id", "test_connection_check").execute()
    print("   🧹 Test data cleaned up")
    
except Exception as e:
    error_str = str(e)
    if "relation" in error_str and "does not exist" in error_str:
        print("   ⚠️ Table doesn't exist - need to run migration first")
    else:
        print(f"   ⚠️ Insert test: {e}")

print("\n" + "=" * 50)
print("🎉 SUPABASE CONNECTION TEST COMPLETE")
print("=" * 50)
print("\n📝 Next Steps:")
print("1. If tables don't exist, run the migration SQL in Supabase Dashboard:")
print("   - Go to: https://supabase.com/dashboard/project/mxaazuhlqewmkweewyaz/sql")
print("   - Copy and run: migrations/001_mini_agent_memory_schema.sql")
print("")
print("2. After migration, the MCP server will have full access to:")
print("   - mini_agent_projects (project context)")
print("   - mini_agent_sessions (conversation history)")
print("   - mini_agent_knowledge (knowledge graph)")
print("   - mini_agent_tool_logs (analytics)")
print("   - mini_agent_user_prefs (settings)")
print("   - mini_agent_system_state (health)")
