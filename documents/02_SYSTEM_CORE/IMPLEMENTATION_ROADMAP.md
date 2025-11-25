# Implementation Roadmap: Missing Components Integration
## Detailed Technical Implementation Plan

**Document Purpose**: Step-by-step implementation guide for integrating the 10 missing components into the existing Mini-Agent system.

---

## Implementation Phases Overview

```
Phase 1: Foundation (Weeks 1-4)
├── Task Orchestration Layer
├── Session Lifecycle Management  
└── Error Recovery System

Phase 2: Quality & Security (Weeks 5-8)
├── Quality Assurance Framework
├── Security & Privacy Layer
└── Resource Monitoring System

Phase 3: Intelligence & Operations (Weeks 9-12)
├── Integration Governance
├── User Feedback Learning
├── Performance Analytics
└── Deployment Operations
```

---

## Phase 1: Foundation Components

### Week 1-2: Task Orchestration Layer

#### Step 1: Create Core Orchestration Infrastructure

**File: `mini_agent/orchestration/task_orchestrator.py`**
```python
"""Task Orchestration System for Mini-Agent"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path

from ..schema import Task, SubTask, TaskResult
from ..core.context_manager import ContextIsolationManager
from ..core.resource_manager import ResourceManager

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TaskExecutionPlan:
    task_id: str
    subtasks: List[SubTask]
    dependencies: Dict[str, List[str]]  # task_id -> dependencies
    resource_requirements: Dict[str, Any]
    estimated_duration: float
    parallel_groups: List[List[str]]  # Groups that can run in parallel

class TaskOrchestrator:
    """Main orchestration engine"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.task_graph = {}
        self.active_tasks = {}
        self.completed_tasks = {}
        self.resource_manager = ResourceManager(config.get('resources', {}))
        self.context_manager = ContextIsolationManager(config.get('context', {}))
        self.retry_manager = RetryManager()
        
    async def execute_complex_task(self, task: Task) -> TaskResult:
        """Execute a complex task by breaking it down"""
        logger.info(f"Starting orchestration for task: {task.id}")
        
        try:
            # Step 1: Decompose task
            subtasks = await self._decompose_task(task)
            
            # Step 2: Create execution plan
            execution_plan = await self._create_execution_plan(subtasks)
            
            # Step 3: Execute plan
            results = await self._execute_plan(execution_plan)
            
            # Step 4: Aggregate results
            final_result = await self._aggregate_results(results)
            
            logger.info(f"Task orchestration completed: {task.id}")
            return final_result
            
        except Exception as e:
            logger.error(f"Task orchestration failed: {task.id}, error: {e}")
            return TaskResult.error(task.id, str(e))
    
    async def _decompose_task(self, task: Task) -> List[SubTask]:
        """Break down complex task into subtasks"""
        logger.info(f"Decomposing task: {task.id}")
        
        # Use LLM to analyze and break down the task
        prompt = f"""
        Analyze this task and break it down into smaller, manageable subtasks:
        
        Task: {task.description}
        Requirements: {task.requirements}
        Context: {task.context}
        
        Break it down into:
        1. Parallelizable subtasks (can run simultaneously)
        2. Sequential subtasks (must run in order)
        3. Dependencies between subtasks
        4. Estimated complexity for each subtask
        
        Return as JSON with the following structure:
        {{
            "subtasks": [
                {{
                    "id": "unique_id",
                    "description": "what this subtask does",
                    "complexity": "low/medium/high",
                    "can_parallel": true/false,
                    "dependencies": ["other_task_id"]
                }}
            ]
        }}
        """
        
        # Call LLM for decomposition (using existing LLM client)
        # This is a placeholder - integrate with existing LLM client
        response = await self._call_llm_for_decomposition(prompt)
        
        subtasks = []
        for subtask_data in response['subtasks']:
            subtask = SubTask(
                id=subtask_data['id'],
                description=subtask_data['description'],
                complexity=subtask_data['complexity'],
                can_parallel=subtask_data['can_parallel'],
                dependencies=subtask_data['dependencies'],
                context=task.context  # Start with parent context
            )
            subtasks.append(subtask)
        
        logger.info(f"Decomposed task into {len(subtasks)} subtasks")
        return subtasks
    
    async def _create_execution_plan(self, subtasks: List[SubTask]) -> TaskExecutionPlan:
        """Create execution plan with dependencies"""
        logger.info("Creating execution plan")
        
        # Build dependency graph
        dependencies = {}
        for subtask in subtasks:
            dependencies[subtask.id] = subtask.dependencies
        
        # Group parallel tasks
        parallel_groups = self._identify_parallel_groups(subtasks)
        
        # Calculate resource requirements
        resource_requirements = await self._calculate_resource_requirements(subtasks)
        
        plan = TaskExecutionPlan(
            task_id=str(uuid.uuid4()),
            subtasks=subtasks,
            dependencies=dependencies,
            resource_requirements=resource_requirements,
            estimated_duration=self._estimate_duration(subtasks),
            parallel_groups=parallel_groups
        )
        
        logger.info(f"Execution plan created: {len(parallel_groups)} parallel groups")
        return plan
    
    async def _execute_plan(self, plan: TaskExecutionPlan) -> Dict[str, Any]:
        """Execute the plan with parallel processing"""
        logger.info("Executing task plan")
        
        results = {}
        executed = set()
        
        # Execute parallel groups sequentially, tasks within groups in parallel
        for group in plan.parallel_groups:
            # Wait for dependencies
            for task_id in group:
                await self._wait_for_dependencies(task_id, plan.dependencies, executed)
            
            # Execute group in parallel
            group_results = await asyncio.gather(*[
                self._execute_subtask(subtask_id, plan) for subtask_id in group
            ], return_exceptions=True)
            
            # Process results
            for i, subtask_id in enumerate(group):
                result = group_results[i]
                if isinstance(result, Exception):
                    logger.error(f"Subtask {subtask_id} failed: {result}")
                    results[subtask_id] = TaskResult.error(subtask_id, str(result))
                else:
                    results[subtask_id] = result
                    executed.add(subtask_id)
        
        return results
    
    async def _execute_subtask(self, subtask_id: str, plan: TaskExecutionPlan) -> TaskResult:
        """Execute a single subtask with isolated context"""
        # Find the subtask
        subtask = next(s for s in plan.subtasks if s.id == subtask_id)
        
        # Create isolated context
        context = await self.context_manager.create_isolated_context(subtask)
        
        # Allocate resources
        resources = await self.resource_manager.allocate(subtask)
        
        try:
            # Execute subtask using existing agent infrastructure
            result = await self._execute_subtask_with_agent(subtask, context, resources)
            return result
            
        except Exception as e:
            logger.error(f"Subtask execution failed: {subtask_id}, error: {e}")
            return TaskResult.error(subtask_id, str(e))
        finally:
            # Clean up context and resources
            await self.context_manager.cleanup_context(subtask_id)
            await self.resource_manager.release(subtask_id)
```

**File: `mini_agent/core/context_manager.py`**
```python
"""Context Isolation Manager for Task Orchestration"""

import asyncio
import logging
from typing import Dict, Any, Set
from dataclasses import dataclass
from ..core.context_overflow_prevention import MiniAgentContextManager

logger = logging.getLogger(__name__)

@dataclass
class TaskContext:
    task_id: str
    context_manager: MiniAgentContextManager
    active_entities: Set[str]  # Knowledge graph entities
    created_at: float
    token_count: int = 0

class ContextIsolationManager:
    """Manages isolated contexts for parallel task execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_contexts: Dict[str, TaskContext] = {}
        self.knowledge_graph_filter = KnowledgeGraphFilter()
        self.max_context_tokens = config.get('max_tokens_per_task', 80000)
        
    async def create_isolated_context(self, subtask) -> TaskContext:
        """Create isolated context for a subtask"""
        task_id = subtask.id
        
        # Create new context manager for this task
        context_manager = MiniAgentContextManager(f"task-{task_id}")
        
        # Filter knowledge graph to relevant entities
        relevant_entities = await self.knowledge_graph_filter.filter_relevant_entities(
            subtask.description, subtask.requirements
        )
        
        # Create task context
        task_context = TaskContext(
            task_id=task_id,
            context_manager=context_manager,
            active_entities=relevant_entities,
            created_at=asyncio.get_event_loop().time()
        )
        
        self.active_contexts[task_id] = task_context
        logger.info(f"Created isolated context for task: {task_id}")
        
        return task_context
    
    async def cleanup_context(self, task_id: str):
        """Clean up task context"""
        if task_id in self.active_contexts:
            del self.active_contexts[task_id]
            logger.info(f"Cleaned up context for task: {task_id}")
    
    async def get_context_summary(self, task_id: str) -> Dict[str, Any]:
        """Get summary of task context"""
        if task_id not in self.active_contexts:
            return {}
        
        context = self.active_contexts[task_id]
        return {
            'task_id': task_id,
            'token_count': context.token_count,
            'active_entities': len(context.active_entities),
            'created_at': context.created_at
        }

class KnowledgeGraphFilter:
    """Filters knowledge graph to relevant entities for tasks"""
    
    async def filter_relevant_entities(self, task_description: str, requirements: str) -> Set[str]:
        """Filter knowledge graph entities relevant to the task"""
        # This would integrate with the existing knowledge graph
        # For now, return a small subset based on keyword matching
        
        relevant_keywords = self._extract_keywords(task_description + " " + requirements)
        
        # Query knowledge graph for entities containing these keywords
        # This is a placeholder - integrate with existing knowledge graph
        relevant_entities = set()
        
        return relevant_entities
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract relevant keywords from text"""
        # Simple keyword extraction - could be enhanced with NLP
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = {word for word in words if len(word) > 2 and word not in stop_words}
        
        return keywords
```

**File: `mini_agent/core/resource_manager.py`**
```python
"""Resource Management System for Task Orchestration"""

import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ResourceType(Enum):
    CPU_CORES = "cpu_cores"
    MEMORY = "memory_mb"
    CONTEXT_TOKENS = "context_tokens"
    API_CALLS = "api_calls"

@dataclass
class ResourceAllocation:
    task_id: str
    cpu_cores: int
    memory_mb: int
    context_tokens: int
    api_calls_per_minute: int
    allocated_at: float

class ResourceManager:
    """Manages system resources for parallel task execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_cpu_cores = config.get('max_cpu_cores', 4)
        self.max_memory_mb = config.get('max_memory_mb', 8192)
        self.max_context_tokens = config.get('max_context_tokens', 200000)
        
        self.allocated_resources: Dict[str, ResourceAllocation] = {}
        self.available_resources = ResourceAllocation(
            task_id="system",
            cpu_cores=self.max_cpu_cores,
            memory_mb=self.max_memory_mb,
            context_tokens=self.max_context_tokens,
            api_calls_per_minute=100,
            allocated_at=0
        )
    
    async def allocate(self, subtask) -> ResourceAllocation:
        """Allocate resources for a subtask"""
        # Calculate resource requirements based on task complexity
        required_resources = self._calculate_requirements(subtask)
        
        # Check if resources are available
        if not self._can_allocate(required_resources):
            # Wait for resources to become available
            await self._wait_for_resources(required_resources)
        
        # Allocate resources
        allocation = ResourceAllocation(
            task_id=subtask.id,
            cpu_cores=required_resources['cpu_cores'],
            memory_mb=required_resources['memory_mb'],
            context_tokens=required_resources['context_tokens'],
            api_calls_per_minute=required_resources['api_calls_per_minute'],
            allocated_at=asyncio.get_event_loop().time()
        )
        
        self.allocated_resources[subtask.id] = allocation
        
        # Update available resources
        self.available_resources.cpu_cores -= allocation.cpu_cores
        self.available_resources.memory_mb -= allocation.memory_mb
        self.available_resources.context_tokens -= allocation.context_tokens
        
        logger.info(f"Allocated resources for task: {subtask.id}")
        return allocation
    
    async def release(self, task_id: str):
        """Release resources after task completion"""
        if task_id in self.allocated_resources:
            allocation = self.allocated_resources[task_id]
            
            # Return resources to available pool
            self.available_resources.cpu_cores += allocation.cpu_cores
            self.available_resources.memory_mb += allocation.memory_mb
            self.available_resources.context_tokens += allocation.context_tokens
            
            del self.allocated_resources[task_id]
            logger.info(f"Released resources for task: {task_id}")
    
    def _calculate_requirements(self, subtask) -> Dict[str, int]:
        """Calculate resource requirements for a subtask"""
        complexity_multipliers = {
            'low': 1,
            'medium': 2,
            'high': 4
        }
        
        base_requirements = {
            'cpu_cores': 1,
            'memory_mb': 512,
            'context_tokens': 20000,
            'api_calls_per_minute': 10
        }
        
        multiplier = complexity_multipliers.get(subtask.complexity, 1)
        
        return {
            key: int(value * multiplier)
            for key, value in base_requirements.items()
        }
    
    def _can_allocate(self, required: Dict[str, int]) -> bool:
        """Check if required resources are available"""
        return (
            self.available_resources.cpu_cores >= required['cpu_cores'] and
            self.available_resources.memory_mb >= required['memory_mb'] and
            self.available_resources.context_tokens >= required['context_tokens']
        )
    
    async def _wait_for_resources(self, required: Dict[str, int]):
        """Wait for required resources to become available"""
        while not self._can_allocate(required):
            # Release expired allocations
            await self._cleanup_expired_allocations()
            
            # Wait a bit before checking again
            await asyncio.sleep(1)
    
    async def _cleanup_expired_allocations(self):
        """Clean up expired resource allocations"""
        current_time = asyncio.get_event_loop().time()
        expired_tasks = []
        
        for task_id, allocation in self.allocated_resources.items():
            # Consider allocation expired if older than 1 hour
            if current_time - allocation.allocated_at > 3600:
                expired_tasks.append(task_id)
        
        for task_id in expired_tasks:
            await self.release(task_id)
```

#### Step 2: Integration with Existing Agent

**File: `mini_agent/agent.py` (Modifications)**
```python
"""Enhanced Agent with Task Orchestration"""

# Add orchestration import
from .orchestration.task_orchestrator import TaskOrchestrator

class Agent:
    def __init__(self, config: Dict[str, Any]):
        # Existing initialization...
        self.orchestrator = TaskOrchestrator(config.get('orchestration', {}))
        
    async def execute_task(self, task: Task) -> TaskResult:
        """Enhanced task execution with orchestration"""
        
        # Check if this is a complex task requiring orchestration
        if await self._is_complex_task(task):
            logger.info(f"Using task orchestration for complex task: {task.id}")
            return await self.orchestrator.execute_complex_task(task)
        else:
            logger.info(f"Using direct execution for simple task: {task.id}")
            return await self._execute_direct_task(task)
    
    async def _is_complex_task(self, task: Task) -> bool:
        """Determine if task requires orchestration"""
        complexity_indicators = [
            len(task.description) > 500,
            len(task.requirements) > 200,
            'complex' in task.description.lower(),
            'multiple' in task.description.lower(),
            'analysis' in task.description.lower() and 'data' in task.description.lower()
        ]
        
        # Also check context size
        context_tokens = await self._estimate_context_tokens(task)
        
        return sum(complexity_indicators) >= 2 or context_tokens > 50000
```

### Week 3-4: Session Lifecycle Management

#### Step 1: Session Registry and Cleanup

**File: `mini_agent/session/session_manager.py`**
```python
"""Session Lifecycle Management System"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class SessionState(Enum):
    ACTIVE = "active"           # Currently being used
    IDLE = "idle"              # No activity but not timed out
    STALE = "stale"            # Timed out, pending cleanup
    ARCHIVED = "archived"      # Moved to long-term storage
    DELETED = "deleted"        # Permanently removed

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: float
    last_activity: float
    state: SessionState
    context_size: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    ttl: Optional[float] = None  # Time to live in seconds

class SessionManager:
    """Manages session lifecycle and cleanup"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sessions: Dict[str, Session] = {}
        self.cleanup_policies = CleanupPolicyEngine(config.get('cleanup', {}))
        self.archive_manager = ArchiveManager(config.get('archive', {}))
        
        # Start background cleanup task
        asyncio.create_task(self._cleanup_loop())
    
    async def create_session(self, user_id: str, metadata: Dict[str, Any] = None) -> Session:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=time.time(),
            last_activity=time.time(),
            state=SessionState.ACTIVE,
            context_size=0,
            metadata=metadata or {},
            ttl=self._calculate_ttl(user_id)
        )
        
        self.sessions[session_id] = session
        
        logger.info(f"Created session: {session_id} for user: {user_id}")
        return session
    
    async def update_activity(self, session_id: str, context_size: int = 0):
        """Update session activity"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.last_activity = time.time()
            session.context_size = context_size
            
            # Reset TTL if user is active
            if session.state == SessionState.IDLE:
                session.state = SessionState.ACTIVE
                session.ttl = self._calculate_ttl(session.user_id)
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    async def cleanup_session(self, session_id: str):
        """Clean up a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            
            # Archive if needed
            if await self.cleanup_policies.should_archive(session):
                await self.archive_manager.archive_session(session)
            
            # Remove from active sessions
            del self.sessions[session_id]
            
            logger.info(f"Cleaned up session: {session_id}")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                current_time = time.time()
                sessions_to_cleanup = []
                
                for session_id, session in self.sessions.items():
                    # Check if session needs cleanup
                    if await self.cleanup_policies.should_cleanup(session):
                        sessions_to_cleanup.append(session_id)
                
                # Clean up sessions
                for session_id in sessions_to_cleanup:
                    await self.cleanup_session(session_id)
                
                # Sleep before next cleanup cycle
                await asyncio.sleep(self.config.get('cleanup_interval', 300))  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

class CleanupPolicyEngine:
    """Engine for determining cleanup policies"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.idle_timeout = config.get('idle_timeout', 3600)  # 1 hour
        self.max_context_size = config.get('max_context_size', 100000)  # tokens
        self.max_session_age = config.get('max_session_age', 86400)  # 24 hours
    
    async def should_cleanup(self, session: Session) -> bool:
        """Determine if session should be cleaned up"""
        current_time = time.time()
        
        # Check idle timeout
        if current_time - session.last_activity > self.idle_timeout:
            return True
        
        # Check context size
        if session.context_size > self.max_context_size:
            return True
        
        # Check max age
        if current_time - session.created_at > self.max_session_age:
            return True
        
        return False
    
    async def should_archive(self, session: Session) -> bool:
        """Determine if session should be archived"""
        return session.context_size > 10000  # Archive sessions with large contexts

class ArchiveManager:
    """Manages session archiving and retrieval"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.archive_dir = Path(config.get('archive_directory', './archive/sessions'))
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    async def archive_session(self, session: Session):
        """Archive a session"""
        archive_file = self.archive_dir / f"{session.session_id}.json"
        
        archive_data = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'created_at': session.created_at,
            'last_activity': session.last_activity,
            'metadata': session.metadata,
            'context_size': session.context_size,
            'archived_at': time.time()
        }
        
        with open(archive_file, 'w') as f:
            json.dump(archive_data, f, indent=2)
        
        logger.info(f"Archived session: {session.session_id}")
```

#### Step 2: Integration with Knowledge Graph

**File: `mini_agent/session/session_knowledge_graph.py`**
```python
"""Integration of Session Management with Knowledge Graph"""

class SessionKnowledgeGraphManager:
    """Manages knowledge graph entities per session"""
    
    def __init__(self, session_manager: SessionManager, knowledge_graph):
        self.session_manager = session_manager
        self.knowledge_graph = knowledge_graph
        self.session_entities: Dict[str, Set[str]] = {}  # session_id -> entity_ids
    
    async def get_session_entities(self, session_id: str) -> Set[str]:
        """Get knowledge graph entities for a session"""
        if session_id not in self.session_entities:
            self.session_entities[session_id] = set()
        return self.session_entities[session_id]
    
    async def add_entity_to_session(self, session_id: str, entity_id: str):
        """Add an entity to a session's context"""
        if session_id not in self.session_entities:
            self.session_entities[session_id] = set()
        
        self.session_entities[session_id].add(entity_id)
        
        # Update session context size
        session = await self.session_manager.get_session(session_id)
        if session:
            # Estimate tokens added by entity
            entity_tokens = await self._estimate_entity_tokens(entity_id)
            session.context_size += entity_tokens
    
    async def remove_entities_from_session(self, session_id: str, entity_ids: List[str]):
        """Remove entities from session context"""
        if session_id in self.session_entities:
            for entity_id in entity_ids:
                self.session_entities[session_id].discard(entity_id)
    
    async def cleanup_session_entities(self, session_id: str):
        """Remove all entities when cleaning up session"""
        if session_id in self.session_entities:
            entity_ids = list(self.session_entities[session_id])
            await self.remove_entities_from_session(session_id, entity_ids)
            del self.session_entities[session_id]
    
    async def _estimate_entity_tokens(self, entity_id: str) -> int:
        """Estimate token count for an entity"""
        # Get entity from knowledge graph
        entity = await self.knowledge_graph.get_entity(entity_id)
        if entity:
            # Rough estimation: 1 token per 4 characters
            total_chars = len(entity.name)
            for observation in entity.observations:
                total_chars += len(observation)
            return int(total_chars / 4)
        return 0
```

### Week 3-4: Error Recovery System

#### Step 1: Circuit Breaker and Retry Manager

**File: `mini_agent/recovery/error_recovery.py`**
```python
"""Error Recovery and Resilience System"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import time
from functools import wraps

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    TRANSIENT = "transient"      # Network, timeout, temporary
    PERSISTENT = "persistent"    # Auth, permission, data issues
    CATASTROPHIC = "catastrophic" # System overload, security breach

class RecoveryStrategy(Enum):
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    ESCALATE = "escalate"

@dataclass
class ErrorContext:
    error_type: ErrorType
    operation: str
    component: str
    timestamp: float
    metadata: Dict[str, Any]

@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    jitter: bool = True

class CircuitBreaker:
    """Circuit breaker for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if await self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e
    
    async def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        return time.time() - self.last_failure_time >= self.timeout
    
    async def _on_success(self):
        """Handle successful operation"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    async def _on_failure(self):
        """Handle failed operation"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

class RetryManager:
    """Manages retry logic with exponential backoff"""
    
    def __init__(self, default_config: RetryConfig):
        self.default_config = default_config
        self.retry_strategies = {
            ErrorType.TRANSIENT: RetryConfig(max_attempts=5, initial_delay=1.0),
            ErrorType.PERSISTENT: RetryConfig(max_attempts=2, initial_delay=5.0),
            ErrorType.CATASTROPHIC: RetryConfig(max_attempts=1, initial_delay=0.0)
        }
    
    async def execute_with_retry(self, func: Callable, error_context: ErrorContext, *args, **kwargs):
        """Execute function with retry logic"""
        retry_config = self.retry_strategies.get(error_context.error_type, self.default_config)
        
        last_exception = None
        
        for attempt in range(retry_config.max_attempts):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < retry_config.max_attempts - 1:
                    delay = self._calculate_delay(attempt, retry_config)
                    await asyncio.sleep(delay)
                    logger.warning(f"Retry attempt {attempt + 1} for {error_context.operation}: {e}")
                else:
                    logger.error(f"All retry attempts failed for {error_context.operation}: {e}")
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int, config: RetryConfig) -> float:
        """Calculate delay for retry attempt"""
        delay = config.initial_delay * (config.backoff_factor ** attempt)
        delay = min(delay, config.max_delay)
        
        # Add jitter to prevent thundering herd
        if config.jitter:
            delay *= (0.5 + (hash(str(attempt)) % 100) / 100)
        
        return delay

class FallbackHandler:
    """Handles fallback strategies for failed operations"""
    
    def __init__(self):
        self.fallback_strategies = {}
    
    def register_fallback(self, operation: str, fallback_func: Callable):
        """Register fallback function for an operation"""
        self.fallback_strategies[operation] = fallback_func
    
    async def handle_fallback(self, operation: str, error: Exception, context: Dict[str, Any]):
        """Execute fallback for failed operation"""
        if operation in self.fallback_strategies:
            logger.info(f"Executing fallback for operation: {operation}")
            return await self.fallback_strategies[operation](error, context)
        else:
            logger.warning(f"No fallback registered for operation: {operation}")
            return None

class ErrorRecoveryOrchestrator:
    """Orchestrates error recovery across the system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_manager = RetryManager(RetryConfig())
        self.fallback_handler = FallbackHandler()
        self.error_analyzer = ErrorAnalyzer()
        
        # Register common fallbacks
        self._register_default_fallbacks()
    
    def _register_default_fallbacks(self):
        """Register default fallback strategies"""
        
        async def web_search_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for web search failures"""
            # Return cached results or empty result
            logger.warning("Using fallback for web search")
            return {"error": "Search service temporarily unavailable", "fallback": True}
        
        async def api_call_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for API call failures"""
            # Try alternative endpoint or return cached data
            logger.warning("Using fallback for API call")
            return {"error": "API temporarily unavailable", "fallback": True}
        
        self.fallback_handler.register_fallback("web_search", web_search_fallback)
        self.fallback_handler.register_fallback("api_call", api_call_fallback)
    
    async def execute_with_recovery(self, operation: str, func: Callable, context: Dict[str, Any], *args, **kwargs):
        """Execute operation with full error recovery"""
        
        # Analyze potential error types
        expected_errors = await self.error_analyzer.analyze_operation(operation)
        
        # Create error context
        error_context = ErrorContext(
            error_type=expected_errors[0] if expected_errors else ErrorType.TRANSIENT,
            operation=operation,
            component=context.get('component', 'unknown'),
            timestamp=time.time(),
            metadata=context
        )
        
        # Get or create circuit breaker for this operation
        if operation not in self.circuit_breakers:
            self.circuit_breakers[operation] = CircuitBreaker(
                failure_threshold=self.config.get('failure_threshold', 5),
                timeout=self.config.get('circuit_timeout', 60)
            )
        
        circuit_breaker = self.circuit_breakers[operation]
        
        try:
            # Execute with circuit breaker protection
            async with circuit_breaker:
                # Execute with retry logic
                result = await self.retry_manager.execute_with_retry(
                    func, error_context, *args, **kwargs
                )
                return result
                
        except Exception as e:
            logger.error(f"Operation {operation} failed with all recovery attempts: {e}")
            
            # Try fallback
            fallback_result = await self.fallback_handler.handle_fallback(operation, e, context)
            
            if fallback_result is not None:
                return fallback_result
            else:
                # Re-raise original exception
                raise e

def with_error_recovery(operation: str, component: str = "unknown"):
    """Decorator for adding error recovery to functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # This would need access to the recovery orchestrator
            # In practice, this would be injected or accessed via a global instance
            recovery_orchestrator = get_recovery_orchestrator()  # Placeholder
            
            context = {'component': component}
            return await recovery_orchestrator.execute_with_recovery(
                operation, func, context, *args, **kwargs
            )
        return wrapper
    return decorator

class ErrorAnalyzer:
    """Analyzes operations to predict error types"""
    
    async def analyze_operation(self, operation: str) -> List[ErrorType]:
        """Analyze operation to predict likely error types"""
        error_patterns = {
            'web_search': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'api_call': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'file_access': [ErrorType.PERSISTENT, ErrorType.CATASTROPHIC],
            'database_query': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'llm_call': [ErrorType.TRANSIENT, ErrorType.CATASTROPHIC]
        }
        
        for pattern, error_types in error_patterns.items():
            if pattern in operation:
                return error_types
        
        return [ErrorType.TRANSIENT]  # Default to transient errors
```

This completes the implementation roadmap for the first phase. Each component is designed to integrate seamlessly with the existing Mini-Agent architecture while solving the specific problems identified.

The key improvements this phase provides:

1. **Task Orchestration**: Prevents context overflow by breaking complex tasks into manageable subtasks
2. **Session Management**: Prevents memory bloat by cleaning up stale sessions and their contexts
3. **Error Recovery**: Improves system reliability with circuit breakers, retries, and fallbacks

These foundational components will significantly improve the system's performance, reliability, and scalability while addressing the random context window loading issues.
