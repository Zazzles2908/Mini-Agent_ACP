#!/usr/bin/env python3
"""
Common types and enums shared across Mini-Agent components
=========================================================

This module contains shared type definitions that are used across multiple
components to avoid circular import issues.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from concurrent.futures import ThreadPoolExecutor

class ComplexityLevel(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

class SessionState(Enum):
    """Session lifecycle states"""
    ACTIVE = "active"           # Currently being used
    IDLE = "idle"              # No activity but not timed out
    STALE = "stale"            # Timed out, pending cleanup
    ARCHIVED = "archived"      # Moved to long-term storage
    DELETED = "deleted"        # Permanently removed

class CleanupReason(Enum):
    """Reasons for session cleanup"""
    IDLE_TIMEOUT = "idle_timeout"
    SIZE_LIMIT = "size_limit"
    AGE_LIMIT = "age_limit"
    MANUAL_DELETE = "manual_delete"
    SYSTEM_SHUTDOWN = "system_shutdown"
    ERROR_RECOVERY = "error_recovery"

class ErrorType(Enum):
    """Classification of error types for recovery strategies"""
    TRANSIENT = "transient"          # Network, timeout, temporary issues
    PERSISTENT = "persistent"        # Auth, permission, data issues
    CATASTROPHIC = "catastrophic"    # System overload, security breach
    BUSINESS_LOGIC = "business_logic" # Invalid data, missing requirements

class RecoveryStrategy(Enum):
    """Recovery strategy types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    ESCALATE = "escalate"
    IGNORE = "ignore"

class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, block requests
    HALF_OPEN = "half_open" # Testing recovery

class ResourceType(Enum):
    """Types of resources managed"""
    CPU_CORES = "cpu_cores"
    MEMORY_MB = "memory_mb"
    CONTEXT_TOKENS = "context_tokens"
    API_CALLS_PER_MINUTE = "api_calls_per_minute"

class ContextTier(Enum):
    """Context priority tiers for optimization"""
    CRITICAL = "critical"        # System prompt, current task
    RECENT = "recent"            # Recent conversation messages  
    SUMMARIZED = "summarized"    # Older content (intelligently summarized)
    TOOL_RESULTS = "tool"        # Tool execution results
    KNOWLEDGE = "knowledge"      # Knowledge graph entities

@dataclass
class SubTask:
    """Individual subtask for execution"""
    id: str
    description: str
    complexity: ComplexityLevel
    can_parallel: bool = True
    dependencies: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    estimated_duration: float = 60.0  # seconds
    max_retries: int = 2
    timeout: float = 300.0  # 5 minutes

@dataclass
class SubTaskResult:
    """Result from subtask execution"""
    subtask_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    retries_attempted: int = 0
    context_size: int = 0
    resource_usage: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskResult:
    """Final task result with orchestration metadata"""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    subtask_results: Dict[str, SubTaskResult] = field(default_factory=dict)
    execution_summary: Dict[str, Any] = field(default_factory=dict)
    total_duration: float = 0.0
    context_optimization: Dict[str, Any] = field(default_factory=dict)
