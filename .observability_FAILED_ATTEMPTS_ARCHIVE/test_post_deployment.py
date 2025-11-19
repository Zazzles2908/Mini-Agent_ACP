#!/usr/bin/env python3
"""
Post-Schema Deployment Test
Run this AFTER deploying supabase-schema.sql in Supabase Dashboard
Tests the observability schema and tables are accessible
"""

import os
import sys
import json
from datetime import datetime

def test_observability_schema():
    """Test observability schema after deployment"""
    
    SUPABASE_URL = "https://mxaazuhlqewmkweewyaz.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxOTA1MjUsImV4cCI6MjA3Mzc2NjUyNX0.4UfuP40d5L72bp-WAXYTSOF8-P11eR3C5oEcr8dZHVI"
    
    print("TESTING OBSERVABILITY SCHEMA")
    print("=" * 50)
    print(f"Supabase URL: {SUPABASE_URL}")
    print(f"Test Time: {datetime.now()}")
    print()
    
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test 1: Check if observability schema exists
        print("Test 1: Schema Existence Check")
        try:
            # Query the information_schema to check for our schema
            response = supabase.rpc('has_schema', {'schema_name': 'mini_agent_observability'}).execute()
            
            if response.data:
                print("✅ Observability schema exists!")
            else:
                print("❌ Observability schema not found")
                print("   → Please deploy DEPLOY_SCHEMA.sql in Supabase Dashboard")
                return False
                
        except Exception as e:
            print(f"❌ Schema check failed: {e}")
            print("   → Please deploy DEPLOY_SCHEMA.sql in Supabase Dashboard")
            return False
        
        print()
        
        # Test 2: Check if tables exist
        print("Test 2: Table Existence Check")
        expected_tables = ['traces', 'tool_executions', 'performance_metrics', 'decisions']
        
        for table_name in expected_tables:
            try:
                # Try to select from the table (will be empty but should exist)
                response = supabase.table(f'mini_agent_observability.{table_name}').select('*').limit(1).execute()
                print(f"✅ Table '{table_name}' exists and accessible")
            except Exception as e:
                print(f"❌ Table '{table_name}' not found or inaccessible: {e}")
                return False
        
        print()
        
        # Test 3: Try inserting test data
        print("Test 3: Test Data Insertion")
        try:
            # Create a test trace
            trace_data = {
                'session_id': 'test_session_001',
                'agent_version': 'MiniMax-M2',
                'user_context': 'Test observability deployment',
                'metadata': {'test': True, 'phase': 'deployment_validation'}
            }
            
            response = supabase.table('mini_agent_observability.traces').insert(trace_data).execute()
            
            if response.data:
                trace_id = response.data[0]['id']
                print(f"✅ Test trace inserted successfully: {trace_id}")
                
                # Create a test tool execution
                tool_data = {
                    'trace_id': trace_id,
                    'tool_name': 'test_tool',
                    'category': 'test',
                    'input': {'test': 'data'},
                    'output': {'result': 'success'},
                    'start_time': datetime.now().isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration_ms': 150,
                    'success': True
                }
                
                response = supabase.table('mini_agent_observability.tool_executions').insert(tool_data).execute()
                
                if response.data:
                    print("✅ Test tool execution inserted successfully")
                    
                    # Add a performance metric
                    metric_data = {
                        'trace_id': trace_id,
                        'metric_type': 'latency',
                        'metric_value': 150.0,
                        'unit': 'ms'
                    }
                    
                    response = supabase.table('mini_agent_observability.performance_metrics').insert(metric_data).execute()
                    
                    if response.data:
                        print("✅ Test performance metric inserted successfully")
                        print("✅ All observability tables operational!")
                        return True
                    else:
                        print("❌ Failed to insert test performance metric")
                        return False
                else:
                    print("❌ Failed to insert test tool execution")
                    return False
            else:
                print("❌ Failed to insert test trace")
                return False
                
        except Exception as e:
            print(f"❌ Test data insertion failed: {e}")
            return False
        
    except ImportError:
        print("❌ Supabase client not installed")
        print("   → Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

def test_public_views():
    """Test public views after deployment"""
    
    SUPABASE_URL = "https://mxaazuhlqewmkweewyaz.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxOTA1MjUsImV4cCI6MjA3Mzc2NjUyNX0.4UfuP40d5L72bp-WAXYTSOF8-P11eR3C5oEcr8dZHVI"
    
    print("\nTesting Public Views")
    print("=" * 30)
    
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test public views
        expected_views = ['agent_traces', 'agent_tool_executions', 'agent_performance_metrics', 'agent_decisions']
        
        for view_name in expected_views:
            try:
                response = supabase.table(view_name).select('*').limit(1).execute()
                print(f"✅ Public view '{view_name}' accessible")
            except Exception as e:
                print(f"❌ Public view '{view_name}' not accessible: {e}")
                return False
        
        print("✅ All public views operational!")
        return True
        
    except Exception as e:
        print(f"❌ Public views test failed: {e}")
        return False

if __name__ == "__main__":
    print("OBSERVABILITY SCHEMA VALIDATION TEST")
    print("Run this AFTER deploying DEPLOY_SCHEMA.sql and DEPLOY_VIEWS.sql")
    print()
    
    schema_ok = test_observability_schema()
    views_ok = test_public_views()
    
    print("\nFINAL RESULTS")
    print("=" * 30)
    
    if schema_ok and views_ok:
        print("🎉 SUCCESS: Observability system ready for Mini-Agent integration!")
        print("✅ Schema deployed")
        print("✅ Tables operational")
        print("✅ Public views accessible")
        print("✅ Test data inserted")
        print("\n🚀 Ready to proceed to Phase 2: Mini-Agent Integration")
    else:
        print("❌ ISSUES DETECTED:")
        if not schema_ok:
            print("   - Schema deployment problems")
        if not views_ok:
            print("   - Public views problems")
        print("\n🔧 Fix issues before proceeding to Phase 2")
