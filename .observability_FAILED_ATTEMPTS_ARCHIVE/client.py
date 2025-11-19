#!/usr/bin/env python3
"""
Mini-Agent Observability Client
Provides unified interface for logging agent activities to both Langfuse and Supabase
"""

import os
import time
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import asyncio

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

@dataclass
class ToolExecution:
    """Data structure for tool execution logging"""
    id: str
    tool_name: str
    category: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    start_time: datetime
    end_time: datetime
    duration_ms: int
    success: bool
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'tool_name': self.tool_name,
            'category': self.category,
            'input': self.input_data,
            'output': self.output_data,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_ms': self.duration_ms,
            'success': self.success,
            'error_message': self.error_message
        }

@dataclass
class SessionTrace:
    """Data structure for agent session logging"""
    id: str
    session_id: str
    agent_version: str
    user_context: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'agent_version': self.agent_version,
            'user_context': self.user_context,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'metadata': self.metadata
        }

class MiniAgentObservability:
    """
    Unified observability client for Mini-Agent
    Logs to both Langfuse and Supabase observability schema
    """
    
    def __init__(self, 
                 langfuse_secret_key: Optional[str] = None,
                 langfuse_public_key: Optional[str] = None,
                 supabase_url: str = "https://mxaazuhlqewmkweewyaz.supabase.co",
                 supabase_service_key: Optional[str] = None):
        
        self.session_id = str(uuid.uuid4())
        self.agent_version = "MiniMax-M2"
        self.start_time = datetime.now(timezone.utc)
        
        # Initialize Langfuse client
        self.langfuse_client = None
        if LANGFUSE_AVAILABLE and langfuse_secret_key and langfuse_public_key:
            try:
                self.langfuse_client = langfuse.Langfuse(
                    secret_key=langfuse_secret_key,
                    public_key=langfuse_public_key
                )
                print("Langfuse client initialized")
            except Exception as e:
                print(f"⚠️  Langfuse initialization failed: {e}")
        
        # Initialize Supabase client
        self.supabase_client = None
        if SUPABASE_AVAILABLE and supabase_url and supabase_service_key:
            try:
                self.supabase_client = create_client(supabase_url, supabase_service_key)
                print("Supabase client initialized")
            except Exception as e:
                print(f"⚠️  Supabase initialization failed: {e}")
        
        # Create session trace
        self.trace_id = str(uuid.uuid4())
        self._create_session_trace()
        
        print(f"Target Mini-Agent Observability initialized")
        print(f"   Session ID: {self.session_id}")
        print(f"   Trace ID: {self.trace_id}")
    
    def _create_session_trace(self):
        """Create session trace in both Langfuse and Supabase"""
        
        # Create Langfuse trace
        if self.langfuse_client:
            try:
                trace = self.langfuse_client.trace(
                    id=self.trace_id,
                    name="Mini-Agent Session",
                    input={"session_id": self.session_id},
                    metadata={
                        "agent_version": self.agent_version,
                        "start_time": self.start_time.isoformat()
                    }
                )
                print(f"[OK] Langfuse trace created: {self.trace_id}")
            except Exception as e:
                print(f"[WARN] Langfuse trace creation failed: {e}")
        
        # Create Supabase trace
        if self.supabase_client:
            try:
                trace_data = {
                    'id': self.trace_id,
                    'session_id': self.session_id,
                    'agent_version': self.agent_version,
                    'user_context': 'Mini-Agent Observability System',
                    'started_at': self.start_time.isoformat(),
                    'metadata': {
                        'client_version': '1.0.0',
                        'capabilities': ['langfuse', 'supabase']
                    }
                }
                
                try:
                    # Insert without expecting response data (views may not support RETURNING)
                    self.supabase_client.table('agent_traces').insert(trace_data).execute()
                    print("[OK] Supabase trace created successfully")
                except Exception as supabase_error:
                    print(f"[WARN] Supabase trace creation issue: {supabase_error}")
                    
            except Exception as e:
                print(f"[WARN] Supabase trace creation failed: {e}")
    
    def log_tool_execution(self, 
                          tool_name: str, 
                          category: str,
                          input_data: Dict[str, Any],
                          output_data: Dict[str, Any],
                          success: bool = True,
                          error_message: Optional[str] = None,
                          start_time: Optional[datetime] = None) -> ToolExecution:
        """
        Log a tool execution to both Langfuse and Supabase
        """
        if start_time is None:
            start_time = datetime.now(timezone.utc)
        
        end_time = datetime.now(timezone.utc)
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        execution = ToolExecution(
            id=str(uuid.uuid4()),
            tool_name=tool_name,
            category=category,
            input_data=input_data,
            output_data=output_data,
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message
        )
        
        # Log to Langfuse
        if self.langfuse_client:
            try:
                span = self.langfuse_client.span(
                    trace_id=self.trace_id,
                    name=tool_name,
                    input=input_data,
                    output=output_data,
                    metadata={
                        'category': category,
                        'duration_ms': duration_ms,
                        'success': success,
                        'error_message': error_message
                    }
                )
                print(f"[OK] Langfuse span logged: {tool_name}")
            except Exception as e:
                print(f"[WARN] Langfuse logging failed: {e}")
        
        # Log to Supabase
        if self.supabase_client:
            try:
                execution_data = {
                    'id': execution.id,  # Add the ID!
                    'trace_id': self.trace_id,
                    'tool_name': tool_name,
                    'category': category,
                    'input': input_data,
                    'output': output_data,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_ms': duration_ms,
                    'success': success,
                    'error_message': error_message
                }
                
                try:
                    # Insert without expecting response data
                    self.supabase_client.table('agent_tool_executions').insert(execution_data).execute()
                    print(f"[OK] Supabase tool execution logged: {tool_name}")
                except Exception as supabase_error:
                    print(f"[WARN] Supabase tool execution issue: {supabase_error}")
                    
            except Exception as e:
                print(f"[WARN] Supabase logging failed: {e}")
        
        return execution
    
    def log_performance_metric(self, 
                              metric_type: str,
                              value: float,
                              unit: str,
                              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Log a performance metric
        """
        success = True
        
        # Log to Langfuse
        if self.langfuse_client:
            try:
                self.langfuse_client.score(
                    trace_id=self.trace_id,
                    name=metric_type,
                    value=value,
                    metadata=metadata or {}
                )
                print(f"[OK] Langfuse metric logged: {metric_type} = {value} {unit}")
            except Exception as e:
                print(f"[WARN] Langfuse metric logging failed: {e}")
                success = False
        
        # Log to Supabase
        if self.supabase_client:
            try:
                metric_id = str(uuid.uuid4())  # Generate ID
                metric_data = {
                    'id': metric_id,
                    'trace_id': self.trace_id,
                    'metric_type': metric_type,
                    'metric_value': value,
                    'unit': unit
                }
                
                try:
                    # Insert without expecting response data
                    self.supabase_client.table('agent_performance_metrics').insert(metric_data).execute()
                    print(f"[OK] Supabase metric logged: {metric_type} = {value} {unit}")
                except Exception as supabase_error:
                    print(f"[WARN] Supabase metric issue: {supabase_error}")
                    success = False
                    
            except Exception as e:
                print(f"[WARN] Supabase metric logging failed: {e}")
                success = False
        
        return success
    
    def log_agent_decision(self,
                          decision_type: str,
                          considered_options: List[str],
                          selected_option: str,
                          reasoning: str,
                          confidence_score: Optional[float] = None) -> bool:
        """
        Log an agent decision for transparency
        """
        success = True
        
        # Log to Langfuse as event (update_trace doesn't exist)
        if self.langfuse_client:
            try:
                self.langfuse_client.event(
                    trace_id=self.trace_id,
                    name=f"decision_{decision_type}",
                    input={
                        'considered_options': considered_options,
                        'selected_option': selected_option
                    },
                    output={'reasoning': reasoning},
                    metadata={
                        'decision_type': decision_type,
                        'confidence': confidence_score
                    }
                )
                print(f"[OK] Langfuse decision logged: {decision_type}")
            except Exception as e:
                print(f"[WARN] Langfuse decision logging failed: {e}")
                success = False
        
        # Log to Supabase
        if self.supabase_client:
            try:
                decision_id = str(uuid.uuid4())  # Generate ID
                decision_data = {
                    'id': decision_id,
                    'trace_id': self.trace_id,
                    'decision_type': decision_type,
                    'considered_options': considered_options,
                    'selected_option': selected_option,
                    'reasoning': reasoning,
                    'confidence_score': confidence_score
                }
                
                try:
                    # Insert without expecting response data
                    self.supabase_client.table('agent_decisions').insert(decision_data).execute()
                    print(f"[OK] Supabase decision logged: {decision_type}")
                except Exception as supabase_error:
                    print(f"[WARN] Supabase decision issue: {supabase_error}")
                    success = False
                    
            except Exception as e:
                print(f"⚠️  Supabase decision logging failed: {e}")
                success = False
        
        return success
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of current session
        """
        duration = datetime.now(timezone.utc) - self.start_time
        
        return {
            'session_id': self.session_id,
            'trace_id': self.trace_id,
            'agent_version': self.agent_version,
            'start_time': self.start_time.isoformat(),
            'duration_minutes': duration.total_seconds() / 60,
            'langfuse_available': self.langfuse_client is not None,
            'supabase_available': self.supabase_client is not None
        }
    
    def close_session(self):
        """Close the observability session"""
        
        end_time = datetime.now(timezone.utc)
        
        # Update Langfuse trace - just flush, no update needed
        if self.langfuse_client:
            try:
                self.langfuse_client.flush()
                print(f"[OK] Langfuse session flushed: {self.trace_id}")
            except Exception as e:
                print(f"[WARN] Langfuse session close failed: {e}")
        
        # Update Supabase trace
        if self.supabase_client:
            try:
                response = self.supabase_client.table('agent_traces').update({
                    'ended_at': end_time.isoformat()
                }).eq('id', self.trace_id).execute()
                print(f"[OK] Supabase session closed: {self.trace_id}")
            except Exception as e:
                print(f"[WARN] Supabase session close failed: {e}")

# Example usage
if __name__ == "__main__":
    print("Mini-Agent Observability Client Test")
    print("=" * 50)
    
    # Initialize client (will work with available credentials)
    client = MiniAgentObservability()
    
    # Test tool execution logging
    print("\nTesting tool execution logging...")
    execution = client.log_tool_execution(
        tool_name="test_file_read",
        category="file",
        input_data={"path": "/test/file.txt", "mode": "r"},
        output_data={"content": "test content", "lines": 1},
        success=True
    )
    
    # Test performance metric
    print("\nTesting performance metric...")
    client.log_performance_metric(
        metric_type="latency",
        value=execution.duration_ms,
        unit="ms"
    )
    
    # Test agent decision
    print("\nTesting agent decision...")
    client.log_agent_decision(
        decision_type="tool_selection",
        considered_options=["file.read", "bash.cat", "smart_file_query"],
        selected_option="file.read",
        reasoning="File operation is most appropriate for reading local files",
        confidence_score=0.95
    )
    
    # Get session summary
    print("\nSession Summary:")
    summary = client.get_session_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Close session
    print("\nClosing session...")
    client.close_session()
    print("✅ Test completed!")
