#!/usr/bin/env python3
"""
Task Orchestration Package
========================

Package for task orchestration capabilities that prevent context overflow
by breaking complex tasks into manageable subtasks with parallel execution.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

from .task_orchestrator import (
    TaskOrchestrator,
    TaskDecompositionEngine,
    ExecutionPlanner,
    SubTaskExecutor,
    TaskExecutionPlan,
    SubTaskResult,
    TaskResult,
    SubTask,
    ContextIsolationManager,
    ComplexityLevel,
    TaskStatus
)

__all__ = [
    'TaskOrchestrator',
    'TaskDecompositionEngine',
    'ExecutionPlanner', 
    'SubTaskExecutor',
    'TaskExecutionPlan',
    'SubTaskResult',
    'TaskResult',
    'SubTask',
    'ContextIsolationManager',
    'ComplexityLevel',
    'TaskStatus'
]

__version__ = '1.0.0'
__author__ = 'Mini-Agent Enhancement Project'
