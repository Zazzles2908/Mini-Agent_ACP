#!/usr/bin/env python3
"""
Session Lifecycle Management System
==================================

Manages session creation, lifecycle, cleanup, and archival to prevent memory bloat
and ensure efficient resource utilization across the system.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

import asyncio
import json
import logging
import sqlite3
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

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

@dataclass
class Session:
    """Session entity with metadata"""
    session_id: str
    user_id: str
    created_at: float
    last_activity: float
    state: SessionState
    context_size: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    ttl: Optional[float] = None  # Time to live in seconds
    tags: Set[str] = field(default_factory=set)
    
    # Activity tracking
    activity_count: int = 0
    context_updates: int = 0
    errors_count: int = 0
    
    # Resource usage
    peak_context_size: int = 0
    total_operations: int = 0
    api_calls_made: int = 0

@dataclass
class CleanupAction:
    """Cleanup action to be performed"""
    session_id: str
    reason: CleanupReason
    priority: int  # 1=low, 5=high
    scheduled_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class SessionDatabase:
    """SQLite database for session persistence"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_activity REAL NOT NULL,
                    state TEXT NOT NULL,
                    context_size INTEGER NOT NULL DEFAULT 0,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    ttl REAL,
                    tags TEXT NOT NULL DEFAULT '',
                    activity_count INTEGER NOT NULL DEFAULT 0,
                    context_updates INTEGER NOT NULL DEFAULT 0,
                    errors_count INTEGER NOT NULL DEFAULT 0,
                    peak_context_size INTEGER NOT NULL DEFAULT 0,
                    total_operations INTEGER NOT NULL DEFAULT 0,
                    api_calls_made INTEGER NOT NULL DEFAULT 0,
                    created_at_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id 
                ON sessions(user_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_state 
                ON sessions(state)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_last_activity 
                ON sessions(last_activity)
            """)
            
            conn.commit()
    
    def save_session(self, session: Session):
        """Save session to database"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sessions (
                    session_id, user_id, created_at, last_activity, state,
                    context_size, metadata, ttl, tags, activity_count,
                    context_updates, errors_count, peak_context_size,
                    total_operations, api_calls_made
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.user_id,
                session.created_at,
                session.last_activity,
                session.state.value,
                session.context_size,
                json.dumps(session.metadata),
                session.ttl,
                ','.join(session.tags),
                session.activity_count,
                session.context_updates,
                session.errors_count,
                session.peak_context_size,
                session.total_operations,
                session.api_calls_made
            ))
            conn.commit()
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """Load session from database"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("""
                SELECT * FROM sessions WHERE session_id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_session(row)
            return None
    
    def load_sessions_by_user(self, user_id: str) -> List[Session]:
        """Load all sessions for a user"""
        sessions = []
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("""
                SELECT * FROM sessions WHERE user_id = ? ORDER BY last_activity DESC
            """, (user_id,))
            
            for row in cursor.fetchall():
                sessions.append(self._row_to_session(row))
        
        return sessions
    
    def load_sessions_by_state(self, state: SessionState) -> List[Session]:
        """Load sessions by state"""
        sessions = []
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("""
                SELECT * FROM sessions WHERE state = ? ORDER BY last_activity
            """, (state.value,))
            
            for row in cursor.fetchall():
                sessions.append(self._row_to_session(row))
        
        return sessions
    
    def cleanup_sessions(self, session_ids: List[str]):
        """Remove sessions from database"""
        if not session_ids:
            return
            
        with sqlite3.connect(str(self.db_path)) as conn:
            placeholders = ','.join(['?' for _ in session_ids])
            conn.execute(f"""
                DELETE FROM sessions WHERE session_id IN ({placeholders})
            """, session_ids)
            conn.commit()
    
    def _row_to_session(self, row) -> Session:
        """Convert database row to Session object"""
        return Session(
            session_id=row[0],
            user_id=row[1],
            created_at=row[2],
            last_activity=row[3],
            state=SessionState(row[4]),
            context_size=row[5],
            metadata=json.loads(row[6]) if row[6] else {},
            ttl=row[7],
            tags=set(row[8].split(',')) if row[8] else set(),
            activity_count=row[9],
            context_updates=row[10],
            errors_count=row[11],
            peak_context_size=row[12],
            total_operations=row[13],
            api_calls_made=row[14]
        )

class CleanupPolicyEngine:
    """Determines cleanup policies and actions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.policies = self._initialize_policies()
    
    def _initialize_policies(self) -> Dict[str, Any]:
        """Initialize cleanup policies"""
        return {
            'idle_timeout': self.config.get('idle_timeout', 3600),  # 1 hour
            'max_context_size': self.config.get('max_context_size', 100000),  # tokens
            'max_session_age': self.config.get('max_session_age', 86400),  # 24 hours
            'max_context_updates': self.config.get('max_context_updates', 1000),
            'max_errors': self.config.get('max_errors', 10),
            'archive_threshold': self.config.get('archive_threshold', 10000),  # Archive sessions > 10K tokens
            'emergency_cleanup_threshold': self.config.get('emergency_cleanup_threshold', 0.9)  # 90% memory usage
        }
    
    async def should_cleanup(self, session: Session) -> Tuple[bool, Optional[CleanupReason]]:
        """Determine if session should be cleaned up"""
        current_time = time.time()
        
        # Check idle timeout
        if current_time - session.last_activity > self.policies['idle_timeout']:
            return True, CleanupReason.IDLE_TIMEOUT
        
        # Check context size limit
        if session.context_size > self.policies['max_context_size']:
            return True, CleanupReason.SIZE_LIMIT
        
        # Check session age limit
        if current_time - session.created_at > self.policies['max_session_age']:
            return True, CleanupReason.AGE_LIMIT
        
        # Check excessive errors
        if session.errors_count > self.policies['max_errors']:
            return True, CleanupReason.ERROR_RECOVERY
        
        return False, None
    
    async def should_archive(self, session: Session) -> bool:
        """Determine if session should be archived instead of deleted"""
        # Archive sessions with substantial content or long lifetime
        return (
            session.context_size > self.policies['archive_threshold'] or
            session.total_operations > 100 or
            session.created_at < time.time() - 3600  # Older than 1 hour
        )
    
    async def calculate_priority(self, session: Session, reason: CleanupReason) -> int:
        """Calculate cleanup priority (1=low, 5=high)"""
        if reason == CleanupReason.ERROR_RECOVERY:
            return 5  # High priority
        elif reason == CleanupReason.SIZE_LIMIT:
            return 4  # High priority
        elif reason == CleanupReason.AGE_LIMIT:
            return 3  # Medium priority
        elif reason == CleanupReason.IDLE_TIMEOUT:
            return 2  # Low priority
        else:
            return 1  # Lowest priority

class SessionLifecycleManager:
    """Main session lifecycle management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize components
        self.session_db = SessionDatabase(config.get('database_path', './data/sessions.db'))
        self.cleanup_policies = CleanupPolicyEngine(config)
        self.archive_manager = ArchiveManager(config.get('archive', {}))
        
        # In-memory session cache
        self.active_sessions: Dict[str, Session] = {}
        self.cleanup_queue: List[CleanupAction] = []
        
        # Statistics
        self.statistics = {
            'sessions_created': 0,
            'sessions_archived': 0,
            'sessions_deleted': 0,
            'total_context_tokens_processed': 0,
            'average_session_lifetime': 0.0,
            'cleanup_actions_performed': 0
        }
        
        # Start background tasks
        asyncio.create_task(self._cleanup_loop())
        asyncio.create_task(self._archive_loop())
        asyncio.create_task(self._maintenance_loop())
        
        logger.info("Session lifecycle manager initialized")
    
    async def create_session(self, user_id: str, metadata: Dict[str, Any] = None, ttl: float = None) -> Session:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        current_time = time.time()
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=current_time,
            last_activity=current_time,
            state=SessionState.ACTIVE,
            context_size=0,
            metadata=metadata or {},
            ttl=ttl,
            tags=set(metadata.get('tags', [])) if metadata else set()
        )
        
        # Cache and persist
        self.active_sessions[session_id] = session
        self.session_db.save_session(session)
        
        # Update statistics
        self.statistics['sessions_created'] += 1
        
        logger.info(f"Created session: {session_id} for user: {user_id}")
        return session
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        # Check cache first
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Load from database
        session = self.session_db.load_session(session_id)
        if session:
            # Cache active sessions
            if session.state in [SessionState.ACTIVE, SessionState.IDLE]:
                self.active_sessions[session_id] = session
        
        return session
    
    async def update_activity(self, session_id: str, context_size: int = 0, context_update: bool = False):
        """Update session activity"""
        session = await self.get_session(session_id)
        if not session:
            logger.warning(f"Session not found for activity update: {session_id}")
            return
        
        current_time = time.time()
        
        # Update activity
        session.last_activity = current_time
        session.activity_count += 1
        session.total_operations += 1
        
        # Update context size
        if context_size > 0:
            session.context_size = context_size
            session.context_updates += 1
            session.peak_context_size = max(session.peak_context_size, context_size)
            self.statistics['total_context_tokens_processed'] += context_size
        
        # Update state
        if session.state == SessionState.IDLE:
            session.state = SessionState.ACTIVE
        
        # Persist changes
        self.session_db.save_session(session)
        
        logger.debug(f"Updated activity for session: {session_id}")
    
    async def add_session_error(self, session_id: str, error_info: Dict[str, Any]):
        """Add error information to session"""
        session = await self.get_session(session_id)
        if not session:
            return
        
        session.errors_count += 1
        
        # Add error details to metadata
        if 'errors' not in session.metadata:
            session.metadata['errors'] = []
        
        session.metadata['errors'].append({
            'timestamp': time.time(),
            'error': error_info.get('error', 'Unknown error'),
            'component': error_info.get('component', 'unknown'),
            'operation': error_info.get('operation', 'unknown')
        })
        
        # Keep only recent errors (last 10)
        if len(session.metadata['errors']) > 10:
            session.metadata['errors'] = session.metadata['errors'][-10:]
        
        self.session_db.save_session(session)
    
    async def cleanup_session(self, session_id: str, reason: CleanupReason, priority: int = 1):
        """Schedule session for cleanup"""
        current_time = time.time()
        
        cleanup_action = CleanupAction(
            session_id=session_id,
            reason=reason,
            priority=priority,
            scheduled_at=current_time,
            metadata={'reason': reason.value}
        )
        
        self.cleanup_queue.append(cleanup_action)
        
        # Sort queue by priority (higher priority first)
        self.cleanup_queue.sort(key=lambda x: x.priority, reverse=True)
        
        logger.debug(f"Scheduled cleanup for session {session_id}: {reason.value} (priority {priority})")
    
    async def delete_session(self, session_id: str, reason: CleanupReason = CleanupReason.MANUAL_DELETE):
        """Permanently delete session"""
        session = await self.get_session(session_id)
        if not session:
            return
        
        # Archive if needed
        if await self.cleanup_policies.should_archive(session):
            await self.archive_manager.archive_session(session)
            session.state = SessionState.ARCHIVED
        else:
            session.state = SessionState.DELETED
        
        # Remove from active sessions
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        # Update statistics
        if session.state == SessionState.ARCHIVED:
            self.statistics['sessions_archived'] += 1
        else:
            self.statistics['sessions_deleted'] += 1
        
        logger.info(f"Deleted session: {session_id} (reason: {reason.value})")
    
    async def get_session_statistics(self, user_id: str = None) -> Dict[str, Any]:
        """Get session statistics"""
        if user_id:
            user_sessions = self.session_db.load_sessions_by_user(user_id)
        else:
            # Load all sessions
            all_sessions = []
            for state in SessionState:
                all_sessions.extend(self.session_db.load_sessions_by_state(state))
            user_sessions = all_sessions
        
        if not user_sessions:
            return {'message': 'No sessions found'}
        
        # Calculate statistics
        total_sessions = len(user_sessions)
        active_sessions = len([s for s in user_sessions if s.state == SessionState.ACTIVE])
        idle_sessions = len([s for s in user_sessions if s.state == SessionState.IDLE])
        archived_sessions = len([s for s in user_sessions if s.state == SessionState.ARCHIVED])
        
        # Calculate averages
        avg_lifetime = sum(time.time() - s.created_at for s in user_sessions) / total_sessions
        avg_context_size = sum(s.context_size for s in user_sessions) / total_sessions
        avg_operations = sum(s.total_operations for s in user_sessions) / total_sessions
        
        # Current system state
        current_memory_usage = await self._get_current_memory_usage()
        
        return {
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'idle_sessions': idle_sessions,
            'archived_sessions': archived_sessions,
            'average_session_lifetime_hours': avg_lifetime / 3600,
            'average_context_size': avg_context_size,
            'average_operations_per_session': avg_operations,
            'current_memory_usage_percent': current_memory_usage,
            'system_statistics': self.statistics,
            'cleanup_queue_size': len(self.cleanup_queue)
        }
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                # Process cleanup queue
                if self.cleanup_queue:
                    action = self.cleanup_queue.pop(0)
                    
                    session = await self.get_session(action.session_id)
                    if session:
                        await self.delete_session(action.session_id, action.reason)
                        self.statistics['cleanup_actions_performed'] += 1
                
                # Check for sessions that need cleanup
                await self._check_sessions_for_cleanup()
                
                # Sleep before next cycle
                await asyncio.sleep(self.config.get('cleanup_interval', 300))  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _check_sessions_for_cleanup(self):
        """Check all sessions for cleanup criteria"""
        sessions_to_cleanup = []
        
        # Check active sessions
        for session in list(self.active_sessions.values()):
            should_cleanup, reason = await self.cleanup_policies.should_cleanup(session)
            if should_cleanup:
                priority = await self.cleanup_policies.calculate_priority(session, reason)
                sessions_to_cleanup.append((session.session_id, reason, priority))
        
        # Schedule cleanups
        for session_id, reason, priority in sessions_to_cleanup:
            await self.cleanup_session(session_id, reason, priority)
    
    async def _archive_loop(self):
        """Background archiving loop"""
        while True:
            try:
                # Archive old active sessions
                for session in list(self.active_sessions.values()):
                    if await self.cleanup_policies.should_archive(session):
                        await self.archive_manager.archive_session(session)
                        session.state = SessionState.ARCHIVED
                        del self.active_sessions[session.session_id]
                        self.statistics['sessions_archived'] += 1
                
                await asyncio.sleep(1800)  # Archive every 30 minutes
                
            except Exception as e:
                logger.error(f"Error in archive loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _maintenance_loop(self):
        """Background maintenance loop"""
        while True:
            try:
                # Emergency cleanup if memory usage is too high
                memory_usage = await self._get_current_memory_usage()
                emergency_threshold = self.cleanup_policies.policies['emergency_cleanup_threshold']
                
                if memory_usage > emergency_threshold:
                    logger.warning(f"High memory usage ({memory_usage:.1%}), triggering emergency cleanup")
                    
                    # Clean up oldest idle sessions first
                    idle_sessions = sorted(
                        [s for s in self.active_sessions.values() if s.state == SessionState.IDLE],
                        key=lambda x: x.last_activity
                    )
                    
                    for session in idle_sessions[:10]:  # Clean up 10 oldest
                        await self.cleanup_session(session.session_id, CleanupReason.ERROR_RECOVERY, 5)
                
                await asyncio.sleep(600)  # Check every 10 minutes
                
            except Exception as e:
                logger.error(f"Error in maintenance loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _get_current_memory_usage(self) -> float:
        """Get current system memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return memory.percent / 100.0
        except ImportError:
            # Fallback if psutil not available
            return 0.5  # Assume 50% usage

class ArchiveManager:
    """Manages session archiving and retrieval"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.archive_dir = Path(config.get('archive_directory', './archive/sessions'))
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Archive statistics
        self.archive_stats = {
            'sessions_archived': 0,
            'total_archived_size_mb': 0,
            'oldest_archive_age_days': 0
        }
    
    async def archive_session(self, session: Session):
        """Archive a session to long-term storage"""
        archive_file = self.archive_dir / f"{session.session_id}.json"
        
        archive_data = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'created_at': session.created_at,
            'last_activity': session.last_activity,
            'metadata': session.metadata,
            'context_size': session.context_size,
            'activity_count': session.activity_count,
            'total_operations': session.total_operations,
            'archived_at': time.time(),
            'session_summary': self._generate_session_summary(session)
        }
        
        with open(archive_file, 'w') as f:
            json.dump(archive_data, f, indent=2)
        
        # Update statistics
        file_size_mb = archive_file.stat().st_size / (1024 * 1024)
        self.archive_stats['sessions_archived'] += 1
        self.archive_stats['total_archived_size_mb'] += file_size_mb
        
        logger.info(f"Archived session: {session.session_id} ({file_size_mb:.2f} MB)")
    
    def _generate_session_summary(self, session: Session) -> str:
        """Generate summary of session activity"""
        lifetime_hours = (time.time() - session.created_at) / 3600
        
        summary_parts = [
            f"Session lasted {lifetime_hours:.1f} hours",
            f"Context size: {session.context_size:,} tokens",
            f"Total operations: {session.total_operations}",
            f"Activity count: {session.activity_count}",
            f"Errors encountered: {session.errors_count}"
        ]
        
        if session.metadata.get('project_type'):
            summary_parts.append(f"Project type: {session.metadata['project_type']}")
        
        return "; ".join(summary_parts)
    
    def get_archive_statistics(self) -> Dict[str, Any]:
        """Get archive statistics"""
        return self.archive_stats.copy()

# Export main classes
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
