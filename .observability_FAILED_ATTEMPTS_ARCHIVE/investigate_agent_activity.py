#!/usr/bin/env python3
"""
Investigation: Check if current agent is sending data to observability system
"""

from supabase import create_client
from datetime import datetime, timezone, timedelta
import os
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

print('='*70)
print('INVESTIGATING AGENT ACTIVITY IN OBSERVABILITY SYSTEM')
print('='*70)
print(f'Current Time: {datetime.now(timezone.utc).isoformat()}')
print()

# Get all traces sorted by most recent
all_traces = supabase.table('agent_traces').select('*').order('started_at', desc=True).limit(20).execute()

print(f'Total Traces in Database: {len(all_traces.data)}')
print()

if all_traces.data:
    print('LAST 10 TRACES (Most Recent First):')
    print('-'*70)
    for i, trace in enumerate(all_traces.data[:10], 1):
        started = trace['started_at']
        session_id = trace['session_id']
        agent_ver = trace['agent_version']
        context = trace.get('user_context', 'N/A')
        
        # Calculate age
        from dateutil import parser as date_parser
        trace_time = date_parser.isoparse(started)
        now = datetime.now(timezone.utc)
        age = now - trace_time
        
        if age.total_seconds() < 3600:
            age_str = f'{int(age.total_seconds() / 60)} minutes ago'
        elif age.total_seconds() < 86400:
            age_str = f'{int(age.total_seconds() / 3600)} hours ago'
        else:
            age_str = f'{int(age.total_seconds() / 86400)} days ago'
        
        print(f'{i}. {started} ({age_str})')
        print(f'   Session: {session_id}')
        print(f'   Agent: {agent_ver}')
        print(f'   Context: {context[:50]}...' if len(context) > 50 else f'   Context: {context}')
        print()

print('='*70)
print('ACTIVITY ANALYSIS:')
print('='*70)
print()

# Categorize traces
mini_agent_traces = [t for t in all_traces.data if t['agent_version'] == 'MiniMax-M2']
test_traces = [t for t in all_traces.data if t['agent_version'] == 'test-1.0']
other_traces = [t for t in all_traces.data if t['agent_version'] not in ['MiniMax-M2', 'test-1.0']]

print(f'MiniMax-M2 Agent Traces: {len(mini_agent_traces)}')
print(f'Test/Development Traces: {len(test_traces)}')
print(f'Other Traces: {len(other_traces)}')
print()

# Check for recent activity
now = datetime.now(timezone.utc)
recent_cutoff = now - timedelta(minutes=10)

recent_activity = []
for trace in all_traces.data:
    from dateutil import parser as date_parser
    trace_time = date_parser.isoparse(trace['started_at'])
    if trace_time > recent_cutoff:
        recent_activity.append(trace)

if recent_activity:
    print(f'\nRECENT ACTIVITY (Last 10 minutes): {len(recent_activity)} trace(s)')
    for trace in recent_activity:
        print(f'  - {trace["started_at"]} | {trace["agent_version"]} | Session: {trace["session_id"][:16]}...')
else:
    print('\nNO RECENT ACTIVITY in last 10 minutes')

# Check for tool executions
print()
print('='*70)
print('CHECKING TOOL EXECUTIONS:')
print('='*70)
print()

all_tools = supabase.table('agent_tool_executions').select('*').order('start_time', desc=True).limit(20).execute()
print(f'Total Tool Executions: {len(all_tools.data)}')

if all_tools.data:
    print('\nLast 10 Tool Executions:')
    for i, tool in enumerate(all_tools.data[:10], 1):
        start = tool['start_time']
        name = tool['tool_name']
        cat = tool['category']
        success = 'OK' if tool['success'] else 'FAIL'
        print(f'{i}. {start} | {name} ({cat}): {success}')

print()
print('='*70)
print('CONCLUSION:')
print('='*70)
print()

if recent_activity:
    print('STATUS: Agent activity detected in last 10 minutes')
    print('ACTION: Data IS flowing to observability system')
else:
    if mini_agent_traces:
        latest = mini_agent_traces[0]
        from dateutil import parser as date_parser
        trace_time = date_parser.isoparse(latest['started_at'])
        age = now - trace_time
        
        print(f'STATUS: No recent activity (latest was {int(age.total_seconds() / 60)} minutes ago)')
        print('ACTION: Observability client exists but NOT currently active')
        print()
        print('POSSIBLE REASONS:')
        print('  1. The other agent is not using the observability client')
        print('  2. The observability client needs to be imported/initialized')
        print('  3. The agent is running but not logging to observability')
    else:
        print('STATUS: No MiniMax-M2 agent traces found')
        print('ACTION: Observability system has been tested but not integrated into active agent')

print()
print('='*70)
