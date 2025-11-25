#!/usr/bin/env python3
"""
Resource Management System for Task Orchestration
================================================

Manages system resources (CPU, memory, context tokens) for parallel task execution
to ensure optimal resource utilization and prevent system overload.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

import asyncio
import logging
import psutil
import time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum
from collections import defaultdict, deque

from ..core.common_types import ComplexityLevel, SubTask, ResourceType

logger = logging.getLogger(__name__)

@dataclass
class ResourceAllocation:
    """Resource allocation for a task"""
    task_id: str
    cpu_cores: int
    memory_mb: int
    context_tokens: int
    api_calls_per_minute: int
    allocated_at: float
    expires_at: Optional[float] = None  # Optional expiration time
    metadata: Dict[str, Any] = field(default_factory=dict)
    usage_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class SystemResources:
    """Current system resource status"""
    cpu_cores_available: int
    memory_mb_available: int
    context_tokens_available: int
    api_calls_available: int
    cpu_usage_percent: float
    memory_usage_percent: float
    timestamp: float

@dataclass
class ResourceRequest:
    """Request for resource allocation"""
    task_id: str
    requested_resources: Dict[ResourceType, int]
    priority: int = 1  # 1 = low, 5 = high
    max_wait_time: float = 300.0  # 5 minutes
    created_at: float = field(default_factory=time.time)

class ResourceManager:
    """Manages system resources for parallel task execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # System limits
        self.max_cpu_cores = config.get('max_cpu_cores', psutil.cpu_count())
        self.max_memory_mb = config.get('max_memory_mb', psutil.virtual_memory().total // (1024*1024))
        self.max_context_tokens = config.get('max_context_tokens', 200000)
        self.max_api_calls_per_minute = config.get('max_api_calls_per_minute', 100)
        
        # Resource pools
        self.available_resources = SystemResources(
            cpu_cores_available=self.max_cpu_cores,
            memory_mb_available=self.max_memory_mb,
            context_tokens_available=self.max_context_tokens,
            api_calls_available=self.max_api_calls_per_minute,
            cpu_usage_percent=0.0,
            memory_usage_percent=0.0,
            timestamp=time.time()
        )
        
        # Active allocations
        self.allocated_resources: Dict[str, ResourceAllocation] = {}
        
        # Resource requests queue
        self.resource_queue: deque = deque()
        
        # Usage statistics
        self.usage_statistics = {
            'total_allocations': 0,
            'successful_allocations': 0,
            'failed_allocations': 0,
            'average_allocation_time': 0.0,
            'peak_usage': {
                'cpu_cores': 0,
                'memory_mb': 0,
                'context_tokens': 0
            }
        }
        
        # Performance monitoring
        self.performance_monitor = ResourcePerformanceMonitor()
        
        # Start background monitoring and cleanup tasks
        asyncio.create_task(self._monitor_resources())
        asyncio.create_task(self._cleanup_expired_allocations())
        asyncio.create_task(self._process_resource_queue())
    
    async def allocate(self, subtask: SubTask) -> ResourceAllocation:
        """Allocate resources for a subtask"""
        task_id = subtask.id
        
        # Calculate resource requirements
        required_resources = self._calculate_requirements(subtask)
        
        # Create resource request
        request = ResourceRequest(
            task_id=task_id,
            requested_resources=required_resources
        )
        
        logger.info(f"Allocating resources for task {task_id}: {required_resources}")
        
        # Try immediate allocation
        allocation = await self._try_immediate_allocation(request)
        
        if allocation:
            self.usage_statistics['successful_allocations'] += 1
            logger.info(f"Immediately allocated resources for task {task_id}")
            return allocation
        
        # Queue request and wait
        self.resource_queue.append(request)
        allocation = await self._wait_for_allocation(request)
        
        if allocation:
            self.usage_statistics['successful_allocations'] += 1
            logger.info(f"Queued and allocated resources for task {task_id}")
        else:
            self.usage_statistics['failed_allocations'] += 1
            logger.error(f"Failed to allocate resources for task {task_id}")
        
        return allocation
    
    async def release(self, task_id: str):
        """Release resources after task completion"""
        if task_id in self.allocated_resources:
            allocation = self.allocated_resources[task_id]
            
            # Record final usage
            final_usage = self._record_allocation_usage(allocation)
            allocation.usage_history.append(final_usage)
            
            # Return resources to available pool
            self.available_resources.cpu_cores_available += allocation.cpu_cores
            self.available_resources.memory_mb_available += allocation.memory_mb
            self.available_resources.context_tokens_available += allocation.context_tokens
            self.available_resources.api_calls_available += allocation.api_calls_per_minute
            
            # Remove from allocated resources
            del self.allocated_resources[task_id]
            
            logger.info(f"Released resources for task {task_id}")
            
            # Update statistics
            self.usage_statistics['total_allocations'] += 1
            
            # Trigger resource queue processing
            await self._trigger_queue_processing()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current resource manager status"""
        
        # Calculate usage percentages
        cpu_usage_percent = ((self.max_cpu_cores - self.available_resources.cpu_cores_available) / self.max_cpu_cores) * 100
        memory_usage_percent = ((self.max_memory_mb - self.available_resources.memory_mb_available) / self.max_memory_mb) * 100
        context_usage_percent = ((self.max_context_tokens - self.available_resources.context_tokens_available) / self.max_context_tokens) * 100
        
        # Update available resources with current system usage
        self.available_resources.cpu_usage_percent = cpu_usage_percent
        self.available_resources.memory_usage_percent = memory_usage_percent
        self.available_resources.timestamp = time.time()
        
        return {
            'available_resources': {
                'cpu_cores': self.available_resources.cpu_cores_available,
                'memory_mb': self.available_resources.memory_mb_available,
                'context_tokens': self.available_resources.context_tokens_available,
                'api_calls_per_minute': self.available_resources.api_calls_available
            },
            'allocated_resources': len(self.allocated_resources),
            'resource_queue_size': len(self.resource_queue),
            'usage_percentages': {
                'cpu': cpu_usage_percent,
                'memory': memory_usage_percent,
                'context_tokens': context_usage_percent
            },
            'system_limits': {
                'max_cpu_cores': self.max_cpu_cores,
                'max_memory_mb': self.max_memory_mb,
                'max_context_tokens': self.max_context_tokens
            },
            'usage_statistics': self.usage_statistics,
            'performance_metrics': self.performance_monitor.get_metrics()
        }
    
    def _calculate_requirements(self, subtask: SubTask) -> Dict[ResourceType, int]:
        """Calculate resource requirements based on subtask complexity and estimated duration"""
        
        # Base requirements by complexity
        complexity_multipliers = {
            ComplexityLevel.SIMPLE: {
                ResourceType.CPU_CORES: 1,
                ResourceType.MEMORY_MB: 512,
                ResourceType.CONTEXT_TOKENS: 20000,
                ResourceType.API_CALLS_PER_MINUTE: 10
            },
            ComplexityLevel.MEDIUM: {
                ResourceType.CPU_CORES: 2,
                ResourceType.MEMORY_MB: 1024,
                ResourceType.CONTEXT_TOKENS: 40000,
                ResourceType.API_CALLS_PER_MINUTE: 20
            },
            ComplexityLevel.COMPLEX: {
                ResourceType.CPU_CORES: 3,
                ResourceType.MEMORY_MB: 2048,
                ResourceType.CONTEXT_TOKENS: 60000,
                ResourceType.API_CALLS_PER_MINUTE: 30
            },
            ComplexityLevel.VERY_COMPLEX: {
                ResourceType.CPU_CORES: 4,
                ResourceType.MEMORY_MB: 4096,
                ResourceType.CONTEXT_TOKENS: 80000,
                ResourceType.API_CALLS_PER_MINUTE: 50
            }
        }
        
        base_requirements = complexity_multipliers.get(subtask.complexity, complexity_multipliers[ComplexityLevel.MEDIUM])
        
        # Adjust based on estimated duration
        duration_multiplier = min(2.0, subtask.estimated_duration / 300)  # Cap at 2x for very long tasks
        
        adjusted_requirements = {}
        for resource_type, base_value in base_requirements.items():
            adjusted_requirements[resource_type] = int(base_value * duration_multiplier)
        
        # Ensure we don't exceed system limits
        adjusted_requirements[ResourceType.CPU_CORES] = min(
            adjusted_requirements[ResourceType.CPU_CORES], 
            self.max_cpu_cores
        )
        adjusted_requirements[ResourceType.MEMORY_MB] = min(
            adjusted_requirements[ResourceType.MEMORY_MB],
            self.max_memory_mb
        )
        
        return adjusted_requirements
    
    async def _try_immediate_allocation(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Try to allocate resources immediately"""
        
        # Check if resources are available
        if not self._can_allocate_immediately(request.requested_resources):
            return None
        
        # Allocate resources
        allocation = ResourceAllocation(
            task_id=request.task_id,
            cpu_cores=request.requested_resources[ResourceType.CPU_CORES],
            memory_mb=request.requested_resources[ResourceType.MEMORY_MB],
            context_tokens=request.requested_resources[ResourceType.CONTEXT_TOKENS],
            api_calls_per_minute=request.requested_resources[ResourceType.API_CALLS_PER_MINUTE],
            allocated_at=time.time(),
            expires_at=time.time() + 3600,  # 1 hour default expiration
            metadata={'allocation_type': 'immediate'}
        )
        
        # Deduct from available resources
        self.available_resources.cpu_cores_available -= allocation.cpu_cores
        self.available_resources.memory_mb_available -= allocation.memory_mb
        self.available_resources.context_tokens_available -= allocation.context_tokens
        self.available_resources.api_calls_available -= allocation.api_calls_per_minute
        
        # Store allocation
        self.allocated_resources[request.task_id] = allocation
        
        return allocation
    
    async def _wait_for_allocation(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Wait for resources to become available"""
        start_time = time.time()
        
        while time.time() - start_time < request.max_wait_time:
            # Check if resources are now available
            if self._can_allocate_immediately(request.requested_resources):
                return await self._try_immediate_allocation(request)
            
            # Clean up expired allocations
            await self._cleanup_expired_allocations()
            
            # Process queue to free up resources
            await self._process_resource_queue()
            
            # Wait before checking again
            await asyncio.sleep(1)
        
        logger.warning(f"Resource allocation timeout for task {request.task_id}")
        return None
    
    def _can_allocate_immediately(self, requested: Dict[ResourceType, int]) -> bool:
        """Check if resources can be allocated immediately"""
        return (
            self.available_resources.cpu_cores_available >= requested[ResourceType.CPU_CORES] and
            self.available_resources.memory_mb_available >= requested[ResourceType.MEMORY_MB] and
            self.available_resources.context_tokens_available >= requested[ResourceType.CONTEXT_TOKENS] and
            self.available_resources.api_calls_available >= requested[ResourceType.API_CALLS_PER_MINUTE]
        )
    
    async def _cleanup_expired_allocations(self):
        """Clean up expired resource allocations"""
        current_time = time.time()
        expired_tasks = []
        
        for task_id, allocation in self.allocated_resources.items():
            # Check expiration
            if allocation.expires_at and current_time > allocation.expires_at:
                expired_tasks.append(task_id)
            
            # Check for stuck allocations (no activity for 2 hours)
            elif allocation.usage_history:
                last_activity = allocation.usage_history[-1].get('timestamp', allocation.allocated_at)
                if current_time - last_activity > 7200:  # 2 hours
                    logger.warning(f"Releasing stuck allocation for task {task_id}")
                    expired_tasks.append(task_id)
        
        # Release expired allocations
        for task_id in expired_tasks:
            await self.release(task_id)
    
    async def _process_resource_queue(self):
        """Process queued resource requests"""
        if not self.resource_queue:
            return
        
        # Process requests in priority order
        queue_list = list(self.resource_queue)
        queue_list.sort(key=lambda x: x.priority, reverse=True)  # Higher priority first
        
        processed_requests = []
        
        for request in queue_list:
            if self._can_allocate_immediately(request.requested_resources):
                # Allocate immediately
                allocation = await self._try_immediate_allocation(request)
                if allocation:
                    processed_requests.append(request)
            elif time.time() - request.created_at > request.max_wait_time:
                # Remove timed-out requests
                processed_requests.append(request)
        
        # Remove processed requests from queue
        for request in processed_requests:
            try:
                self.resource_queue.remove(request)
            except ValueError:
                pass  # Already removed
    
    async def _monitor_resources(self):
        """Background task to monitor system resources"""
        while True:
            try:
                # Update system resource usage
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Record metrics
                self.performance_monitor.record_metric('cpu_usage', cpu_percent)
                self.performance_monitor.record_metric('memory_usage', memory.percent)
                
                # Check for resource alerts
                if cpu_percent > 80:
                    logger.warning(f"High CPU usage detected: {cpu_percent}%")
                
                if memory.percent > 85:
                    logger.warning(f"High memory usage detected: {memory.percent}%")
                
                # Clean up expired allocations periodically
                await self._cleanup_expired_allocations()
                
                # Process resource queue
                await self._process_resource_queue()
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying
    
    async def _trigger_queue_processing(self):
        """Trigger resource queue processing"""
        # This could be implemented with an asyncio.Event for more efficient signaling
        # For now, we just process on the next cycle
        pass
    
    def _record_allocation_usage(self, allocation: ResourceAllocation) -> Dict[str, Any]:
        """Record usage statistics for an allocation"""
        
        current_time = time.time()
        duration = current_time - allocation.allocated_at
        
        return {
            'timestamp': current_time,
            'duration': duration,
            'cpu_cores': allocation.cpu_cores,
            'memory_mb': allocation.memory_mb,
            'context_tokens': allocation.context_tokens,
            'api_calls': allocation.api_calls_per_minute
        }

class ResourcePerformanceMonitor:
    """Monitors and analyzes resource usage performance"""
    
    def __init__(self):
        self.metrics_history = deque(maxlen=1000)  # Keep last 1000 metrics
        self.performance_thresholds = {
            'cpu_usage_alert': 80.0,  # Alert at 80% CPU usage
            'memory_usage_alert': 85.0,  # Alert at 85% memory usage
            'context_usage_alert': 90.0,  # Alert at 90% context usage
            'allocation_failure_rate': 10.0,  # Alert if >10% allocation failures
            'average_wait_time_alert': 30.0  # Alert if average wait >30 seconds
        }
    
    def record_metric(self, metric_type: str, value: float, metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = {
            'timestamp': time.time(),
            'type': metric_type,
            'value': value,
            'metadata': metadata or {}
        }
        self.metrics_history.append(metric)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        if not self.metrics_history:
            return {}
        
        # Calculate recent metrics (last 100 entries)
        recent_metrics = list(self.metrics_history)[-100:]
        
        # Group by type
        metrics_by_type = defaultdict(list)
        for metric in recent_metrics:
            metrics_by_type[metric['type']].append(metric['value'])
        
        # Calculate aggregates
        aggregates = {}
        for metric_type, values in metrics_by_type.items():
            if values:
                aggregates[metric_type] = {
                    'current': values[-1],
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        
        # Check for alerts
        alerts = self._check_performance_alerts(aggregates)
        
        return {
            'aggregates': aggregates,
            'alerts': alerts,
            'history_size': len(self.metrics_history),
            'thresholds': self.performance_thresholds
        }
    
    def _check_performance_alerts(self, aggregates: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Check if any performance thresholds are exceeded"""
        alerts = []
        
        for metric_type, data in aggregates.items():
            threshold_key = f"{metric_type}_alert"
            if threshold_key in self.performance_thresholds:
                threshold = self.performance_thresholds[threshold_key]
                
                if data['current'] > threshold:
                    alerts.append({
                        'metric': metric_type,
                        'current_value': data['current'],
                        'threshold': threshold,
                        'severity': 'high' if data['current'] > threshold * 1.2 else 'medium',
                        'message': f"{metric_type} usage ({data['current']:.1f}%) exceeds threshold ({threshold}%)"
                    })
        
        return alerts
    
    def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Generate optimization suggestions based on performance data"""
        suggestions = []
        
        metrics = self.get_metrics()
        aggregates = metrics.get('aggregates', {})
        
        # CPU optimization suggestions
        if 'cpu_usage' in aggregates:
            cpu_avg = aggregates['cpu_usage']['average']
            if cpu_avg > 70:
                suggestions.append({
                    'type': 'cpu_optimization',
                    'priority': 'high',
                    'suggestion': 'Consider reducing parallel task count or optimizing CPU-intensive subtasks',
                    'impact': 'Reduce system load and improve responsiveness'
                })
        
        # Memory optimization suggestions
        if 'memory_usage' in aggregates:
            memory_avg = aggregates['memory_usage']['average']
            if memory_avg > 80:
                suggestions.append({
                    'type': 'memory_optimization',
                    'priority': 'high',
                    'suggestion': 'Implement more aggressive context cleanup or reduce context size limits',
                    'impact': 'Prevent memory exhaustion and system crashes'
                })
        
        # Allocation failure suggestions
        if 'allocation_failure_rate' in aggregates:
            failure_rate = aggregates['allocation_failure_rate']['current']
            if failure_rate > 5:
                suggestions.append({
                    'type': 'resource_optimization',
                    'priority': 'medium',
                    'suggestion': 'Increase system resource limits or optimize resource allocation strategy',
                    'impact': 'Reduce task queuing and improve throughput'
                })
        
        return suggestions

# Export main classes
__all__ = [
    'ResourceManager',
    'ResourceAllocation',
    'ResourceRequest',
    'SystemResources',
    'ResourceType',
    'ResourcePerformanceMonitor'
]
