#!/usr/bin/env python3
"""
Post-Schema Deployment Validation
Tests the observability schema after successful deployment
"""

import os
import sys
import json
from datetime import datetime

def test_observability_schema():
    """Test observability schema after deployment"""
    
    SUPABASE_URL = "https://mxaazuhlqewmkweewyaz.supabase.co"
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw"
    
    print("TESTING OBSERVABILITY SCHEMA")
    print("=" * 50)
    print(f"Supabase URL: {SUPABASE_URL}")
    print(f"Test Time: {datetime.now()}")
    print()
    
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("[OK] Supabase client created with service key")
        
        # Test 1: Check if tables exist by trying to query them
        print("\nTest 1: Table Existence Check")
        expected_tables = ['traces', 'tool_executions', 'performance_metrics', 'decisions']
        
        for table_name in expected_tables:
            try:
                # Try to select from the table (should work if it exists)
                response = supabase.table(f'mini_agent_observability.{table_name}').select('*').limit(1).execute()
                print(f"[OK] Table 'mini_agent_observability.{table_name}' exists and accessible")
            except Exception as e:
                print(f"[ERROR] Table 'mini_agent_observability.{table_name}' not accessible: {e}")
                return False
        
        print()
        
        # Test 2: Check public views
        print("Test 2: Public Views Check")
        expected_views = ['agent_traces', 'agent_tool_executions', 'agent_performance_metrics', 'agent_decisions']
        
        for view_name in expected_views:
            try:
                response = supabase.table(view_name).select('*').limit(1).execute()
                print(f"[OK] Public view '{view_name}' accessible")
            except Exception as e:
                print(f"[ERROR] Public view '{view_name}' not accessible: {e}")
                return False
        
        print()
        
        # Test 3: Try inserting test data
        print("Test 3: Test Data Insertion")
        try:
            # Create a test trace
            trace_data = {
                'session_id': 'deployment_test_session',
                'agent_version': 'MiniMax-M2',
                'user_context': 'Testing schema deployment',
                'metadata': {'test': True, 'phase': 'validation'}
            }
            
            response = supabase.table('mini_agent_observability.traces').insert(trace_data).execute()
            
            if response.data:
                trace_id = response.data[0]['id']
                print(f"[OK] Test trace inserted successfully: {trace_id}")
                
                # Create a test tool execution
                tool_data = {
                    'trace_id': trace_id,
                    'tool_name': 'schema_validation',
                    'category': 'validation',
                    'input': {'test': 'data'},
                    'output': {'result': 'success'},
                    'start_time': datetime.now().isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration_ms': 150,
                    'success': True
                }
                
                response = supabase.table('mini_agent_observability.tool_executions').insert(tool_data).execute()
                
                if response.data:
                    print("[OK] Test tool execution inserted successfully")
                    
                    # Add a performance metric
                    metric_data = {
                        'trace_id': trace_id,
                        'metric_type': 'validation_latency',
                        'metric_value': 150.0,
                        'unit': 'ms'
                    }
                    
                    response = supabase.table('mini_agent_observability.performance_metrics').insert(metric_data).execute()
                    
                    if response.data:
                        print("[OK] Test performance metric inserted successfully")
                        
                        # Add a decision log
                        decision_data = {
                            'trace_id': trace_id,
                            'decision_type': 'schema_validation',
                            'considered_options': ['schema_exists', 'schema_missing'],
                            'selected_option': 'schema_exists',
                            'reasoning': 'All tables and views accessible',
                            'confidence_score': 1.0
                        }
                        
                        response = supabase.table('mini_agent_observability.decisions').insert(decision_data).execute()
                        
                        if response.data:
                            print("[OK] Test decision log inserted successfully")
                            print("[OK] ALL SCHEMA TESTS PASSED!")
                            return True
                        else:
                            print("[ERROR] Failed to insert test decision log")
                            return False
                    else:
                        print("[ERROR] Failed to insert test performance metric")
                        return False
                else:
                    print("[ERROR] Failed to insert test tool execution")
                    return False
            else:
                print("[ERROR] Failed to insert test trace")
                return False
                
        except Exception as e:
            print(f"[ERROR] Test data insertion failed: {e}")
            return False
        
    except ImportError:
        print("[ERROR] Supabase client not installed")
        print("   Run: pip install supabase")
        return False
    except Exception as e:
        print(f"[ERROR] Critical error: {e}")
        return False

def test_observability_client_with_schema():
    """Test observability client with deployed schema"""
    
    print("\n" + "=" * 50)
    print("TESTING OBSERVABILITY CLIENT WITH SCHEMA")
    print("=" * 50)
    
    try:
        from client import MiniAgentObservability
        
        # Initialize client with service key
        client = MiniAgentObservability(
            supabase_service_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw"
        )
        
        print("[OK] Client initialized successfully")
        
        # Test tool execution logging
        print("\nTesting tool execution logging...")
        execution = client.log_tool_execution(
            tool_name="post_deployment_test",
            category="validation",
            input_data={"test": "post_deployment"},
            output_data={"status": "success", "schema": "operational"},
            success=True
        )
        
        print(f"[OK] Tool execution logged: {execution.tool_name}")
        
        # Test performance metric
        print("\nTesting performance metric...")
        metric_success = client.log_performance_metric(
            metric_type="post_deployment_test",
            value=execution.duration_ms,
            unit="ms"
        )
        
        if metric_success:
            print("[OK] Performance metric logged")
        else:
            print("[ERROR] Performance metric logging failed")
        
        # Test agent decision
        print("\nTesting agent decision...")
        decision_success = client.log_agent_decision(
            decision_type="deployment_verification",
            considered_options=["schema_missing", "schema_partial", "schema_complete"],
            selected_option="schema_complete",
            reasoning="All observability schema components deployed successfully",
            confidence_score=1.0
        )
        
        if decision_success:
            print("[OK] Agent decision logged")
        else:
            print("[ERROR] Agent decision logging failed")
        
        # Get session summary
        print("\nSession Summary:")
        summary = client.get_session_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # Close session
        print("\nClosing session...")
        client.close_session()
        print("[OK] Session closed successfully")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Client test failed: {e}")
        return False

if __name__ == "__main__":
    print("OBSERVABILITY SCHEMA VALIDATION")
    print("=" * 60)
    print("Testing after successful schema deployment")
    print()
    
    # Test schema directly
    schema_ok = test_observability_schema()
    
    # Test with observability client
    client_ok = test_observability_client_with_schema()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if schema_ok and client_ok:
        print("[SUCCESS] Schema deployment validation COMPLETE!")
        print("[OK] All observability tables operational")
        print("[OK] All public views accessible") 
        print("[OK] Test data inserted successfully")
        print("[OK] Observability client working with schema")
        print("\n[CONGRATULATIONS] Mini-Agent Observability System is FULLY OPERATIONAL!")
    else:
        print("[ERROR] Issues detected:")
        if not schema_ok:
            print("   - Schema validation failed")
        if not client_ok:
            print("   - Client integration failed")
        print("\n[ACTION] Fix issues before proceeding")
