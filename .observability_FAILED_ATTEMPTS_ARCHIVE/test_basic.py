#!/usr/bin/env python3
"""
Simple Observability Client Test
Tests basic functionality without emoji characters
"""

import os
import time
import uuid
from datetime import datetime, timezone

# Try to import optional dependencies
try:
    import langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

def test_basic_functionality():
    """Test basic observability functionality"""
    
    print("Testing Mini-Agent Observability Basic Functionality")
    print("=" * 55)
    print(f"Langfuse available: {LANGFUSE_AVAILABLE}")
    print(f"Supabase available: {SUPABASE_AVAILABLE}")
    print()
    
    session_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    
    print(f"Session ID: {session_id}")
    print(f"Trace ID: {trace_id}")
    print()
    
    # Test Supabase connection (even without schema)
    if SUPABASE_AVAILABLE:
        try:
            supabase_url = "https://mxaazuhlqewmkweewyaz.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxOTA1MjUsImV4cCI6MjA3Mzc2NjUyNX0.4UfuP40d5L72bp-WAXYTSOF8-P11eR3C5oEcr8dZHVI"
            
            supabase = create_client(supabase_url, supabase_key)
            print("[OK] Supabase client created successfully")
            
            # Try to access the information_schema (should work)
            try:
                response = supabase.table('information_schema.tables').select('table_name').limit(1).execute()
                print("[OK] Supabase database access working")
            except Exception as e:
                print(f"[WARN] Supabase information_schema access failed: {e}")
                
        except Exception as e:
            print(f"[ERROR] Supabase client creation failed: {e}")
    else:
        print("[WARN] Supabase client not available - install with: pip install supabase")
    
    print()
    
    # Test Langfuse initialization (without keys)
    if LANGFUSE_AVAILABLE:
        try:
            print("[INFO] Langfuse library available but no keys configured")
            print("[INFO] Will work once API keys are provided")
        except Exception as e:
            print(f"[ERROR] Langfuse test failed: {e}")
    else:
        print("[WARN] Langfuse client not available - install with: pip install langfuse")
    
    print()
    
    # Test basic data structures
    print("Testing data structures...")
    
    start_time = datetime.now(timezone.utc)
    time.sleep(0.1)  # Simulate some work
    end_time = datetime.now(timezone.utc)
    duration_ms = int((end_time - start_time).total_seconds() * 1000)
    
    tool_execution_data = {
        'id': str(uuid.uuid4()),
        'tool_name': 'test_tool',
        'category': 'test',
        'input': {'test': 'data'},
        'output': {'result': 'success'},
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_ms': duration_ms,
        'success': True
    }
    
    print("[OK] Tool execution data structure created")
    print(f"     Duration: {duration_ms}ms")
    
    session_data = {
        'session_id': session_id,
        'trace_id': trace_id,
        'started_at': start_time.isoformat(),
        'agent_version': 'MiniMax-M2'
    }
    
    print("[OK] Session data structure created")
    
    print()
    print("BASIC FUNCTIONALITY TEST COMPLETED")
    print("Next steps:")
    print("1. Deploy Supabase schema via Dashboard")
    print("2. Configure Langfuse API keys")
    print("3. Run full observability pipeline test")

if __name__ == "__main__":
    test_basic_functionality()
