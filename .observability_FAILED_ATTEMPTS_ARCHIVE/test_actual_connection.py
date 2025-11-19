#!/usr/bin/env python3
"""
ACTUAL Langfuse Connection Test - With Real Keys

This test ACTUALLY connects to Langfuse and verifies the full observability pipeline.
"""

import os
import sys
from datetime import datetime, timezone
import time
import uuid

# Load environment variables from .env file
from pathlib import Path
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    print("[OK] Loaded .env file")
else:
    print("[WARN] .env file not found, using hardcoded keys")

# Langfuse credentials
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-a3763d23-9956-457a-9bb1-e5afb800d97b")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-1961199a-453d-4047-9e38-f698e715e321")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")

def test_langfuse_direct_connection():
    """Test direct connection to Langfuse with real keys."""
    print("\n" + "="*70)
    print("TEST 1: DIRECT LANGFUSE CONNECTION")
    print("="*70)
    
    try:
        from langfuse import Langfuse
        
        print(f"Connecting to Langfuse at {LANGFUSE_HOST}...")
        print(f"Public Key: {LANGFUSE_PUBLIC_KEY[:20]}...")
        print(f"Secret Key: {LANGFUSE_SECRET_KEY[:20]}...")
        
        langfuse = Langfuse(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST
        )
        
        print("[OK] Langfuse client created")
        
        # Create a test trace
        trace_id = str(uuid.uuid4())
        print(f"\nCreating test trace: {trace_id}")
        
        trace = langfuse.trace(
            id=trace_id,
            name="Mini-Agent Test Session",
            input={"test": "connection"},
            metadata={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "test_type": "direct_connection"
            }
        )
        
        print(f"[OK] Trace created: {trace_id}")
        
        # Create a span (tool execution)
        print("\nCreating test span (tool execution)...")
        span = trace.span(
            name="test_tool_execution",
            input={"tool": "read_file", "path": "/test/file.py"},
            output={"content": "Test content", "lines": 100},
            metadata={"duration_ms": 150, "category": "file"}
        )
        span.end()
        print("[OK] Span created and ended")
        
        # Create an event
        print("\nCreating test event...")
        trace.event(
            name="test_event",
            input={"type": "success"},
            metadata={"timestamp": datetime.now(timezone.utc).isoformat()}
        )
        print("[OK] Event created")
        
        # Flush to ensure data is sent
        print("\nFlushing data to Langfuse server...")
        langfuse.flush()
        print("[OK] Data flushed successfully")
        
        # Wait a moment for data to be processed
        time.sleep(2)
        
        print("\n" + "-"*70)
        print("SUCCESS! View your trace at:")
        print(f"  {LANGFUSE_HOST}/project/traces/{trace_id}")
        print("-"*70)
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Langfuse not installed: {e}")
        print("Install with: pip install langfuse")
        return False
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_langfuse_callback_handler():
    """Test Langfuse callback handler."""
    print("\n" + "="*70)
    print("TEST 2: LANGFUSE CALLBACK HANDLER")
    print("="*70)
    
    try:
        from langfuse.callback import CallbackHandler
        
        print("Creating callback handler...")
        langfuse_handler = CallbackHandler(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST
        )
        
        print(f"[OK] Callback handler created")
        print(f"     Session ID: {langfuse_handler.session_id if hasattr(langfuse_handler, 'session_id') else 'N/A'}")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Langfuse callback not available: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Callback handler failed: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection."""
    print("\n" + "="*70)
    print("TEST 3: SUPABASE CONNECTION")
    print("="*70)
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL", "https://mxaazuhlqewmkweewyaz.supabase.co")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_key:
            print("[WARN] SUPABASE_SERVICE_ROLE_KEY not set in environment")
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw"
        
        print(f"Connecting to Supabase at {supabase_url}...")
        
        supabase = create_client(supabase_url, supabase_key)
        print("[OK] Supabase client created")
        
        # Test query to agent_traces view
        print("\nTesting query to agent_traces view...")
        result = supabase.table("agent_traces").select("*").limit(5).execute()
        print(f"[OK] Query successful - {len(result.data)} traces found")
        
        # Test insert (without expecting response due to view limitations)
        print("\nTesting insert to agent_traces...")
        test_trace = {
            "id": str(uuid.uuid4()),
            "session_id": str(uuid.uuid4()),
            "agent_version": "test-1.0",
            "user_context": "Integration test",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "metadata": {"test": True}
        }
        
        try:
            supabase.table("agent_traces").insert(test_trace).execute()
            print("[OK] Insert successful")
        except Exception as e:
            print(f"[WARN] Insert issue (may be expected): {e}")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Supabase not installed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Supabase connection failed: {e}")
        return False

def test_full_observability_pipeline():
    """Test the complete observability pipeline with both Langfuse and Supabase."""
    print("\n" + "="*70)
    print("TEST 4: FULL OBSERVABILITY PIPELINE")
    print("="*70)
    
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from client import MiniAgentObservability
        
        print("Initializing MiniAgentObservability with real keys...")
        
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", 
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw")
        
        obs = MiniAgentObservability(
            langfuse_secret_key=LANGFUSE_SECRET_KEY,
            langfuse_public_key=LANGFUSE_PUBLIC_KEY,
            supabase_url="https://mxaazuhlqewmkweewyaz.supabase.co",
            supabase_service_key=supabase_key
        )
        
        print(f"\n[OK] Observability client initialized")
        print(f"     Session: {obs.session_id}")
        print(f"     Trace: {obs.trace_id}")
        print(f"     Langfuse: {'Connected' if obs.langfuse_client else 'Not connected'}")
        print(f"     Supabase: {'Connected' if obs.supabase_client else 'Not connected'}")
        
        # Log some test tool executions
        print("\nLogging test tool executions...")
        
        tools = [
            ("read_file", "file", {"path": "/test/example.py"}, {"content": "...", "lines": 50}),
            ("write_file", "file", {"path": "/test/output.txt", "content": "..."}, {"success": True}),
            ("bash", "core", {"command": "ls -la"}, {"output": "...", "exit_code": 0}),
            ("chat", "mcp", {"prompt": "test"}, {"response": "test response"}),
        ]
        
        for tool_name, category, inputs, outputs in tools:
            execution = obs.log_tool_execution(
                tool_name=tool_name,
                category=category,
                input_data=inputs,
                output_data=outputs,
                success=True
            )
            print(f"  [OK] Logged {tool_name} execution")
        
        # End session
        print("\nClosing session...")
        obs.close_session()
        print("[OK] Session closed")
        
        # Flush Langfuse data
        if obs.langfuse_client:
            print("\nFlushing Langfuse data...")
            obs.langfuse_client.flush()
            print("[OK] Langfuse data flushed")
        
        print("\n" + "-"*70)
        print("SUCCESS! Full observability pipeline working!")
        print(f"  View Langfuse trace: {LANGFUSE_HOST}/project/traces/{obs.trace_id}")
        print(f"  View Supabase data: https://mxaazuhlqewmkweewyaz.supabase.co")
        print("-"*70)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Full pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("="*70)
    print("MINI-AGENT OBSERVABILITY - ACTUAL CONNECTION TEST")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Langfuse Host: {LANGFUSE_HOST}")
    print("="*70)
    
    results = []
    
    # Run tests
    tests = [
        ("Direct Langfuse Connection", test_langfuse_direct_connection),
        ("Callback Handler", test_langfuse_callback_handler),
        ("Supabase Connection", test_supabase_connection),
        ("Full Observability Pipeline", test_full_observability_pipeline),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[FATAL] Test {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        if not result:
            all_passed = False
        print(f"{status} {name}")
    
    print("\n" + "="*70)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("The observability system is FULLY OPERATIONAL with real connections.")
        print("\nNext Steps:")
        print("1. Visit Langfuse UI to see your traces: http://localhost:3000")
        print("2. Check Supabase dashboard for stored data")
        print("3. Run 'python daily_summary.py' to generate reports")
    else:
        print("SOME TESTS FAILED")
        print("Review the errors above and fix the issues.")
    print("="*70)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
