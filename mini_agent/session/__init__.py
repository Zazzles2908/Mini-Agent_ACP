#!/usr/bin/env python3
"""
Session Management Package
=========================

Package for session lifecycle management that prevents memory bloat
and ensures efficient resource utilization across the system.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

from .session_manager import (
    SessionLifecycleManager,
    Session,
    SessionState,
    CleanupReason,
    CleanupAction,
    SessionDatabase,
    CleanupPolicyEngine,
    ArchiveManager
)

__all__ = [
    'SessionLifecycleManager',
    'Session',
    'SessionState',
    'CleanupReason', 
    'CleanupAction',
    'SessionDatabase',
    'CleanupPolicyEngine',
    'ArchiveManager'
]

__version__ = '1.0.0'
__author__ = 'Mini-Agent Enhancement Project'
