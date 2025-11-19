#!/usr/bin/env python3
"""Verify Supabase data integrity"""

import os
from supabase import create_client
from pathlib import Path

# Load env
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

supabase = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_SERVICE_ROLE_KEY']
)

print("="*70)
print("SUPABASE DATA VERIFICATION")
print("="*70)

# Check traces
traces = supabase.table('agent_traces').select('*').limit(10).execute()
print(f"\nAgent Traces: {len(traces.data)} found")
for trace in traces.data[:5]:
    print(f"  - {trace['session_id'][:8]}... ({trace['agent_version']}) - {trace.get('status', 'active')}")

# Check tool executions
tools = supabase.table('agent_tool_executions').select('*').limit(10).execute()
print(f"\nTool Executions: {len(tools.data)} found")
for tool in tools.data[:5]:
    status = "OK" if tool['success'] else "FAIL"
    print(f"  - {tool['tool_name']} ({tool['category']}): {status} [{tool['duration_ms']}ms]")

# Check performance metrics
metrics = supabase.table('agent_performance_metrics').select('*').limit(10).execute()
print(f"\nPerformance Metrics: {len(metrics.data)} found")
for metric in metrics.data[:5]:
    print(f"  - {metric['metric_type']}: {metric['metric_value']} {metric['unit']}")

# Check decisions
decisions = supabase.table('agent_decisions').select('*').limit(10).execute()
print(f"\nAgent Decisions: {len(decisions.data)} found")
for decision in decisions.data[:5]:
    print(f"  - {decision['decision_type']}: {decision['selected_option']}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
