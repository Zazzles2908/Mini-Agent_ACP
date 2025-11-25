#!/usr/bin/env python3
"""
Task Orchestration System for Mini-Agent
========================================

This module provides task orchestration capabilities to prevent context overflow
by breaking complex tasks into manageable subtasks that can run in parallel
with isolated contexts.

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

from ..schema import Message
from ..core.common_types import (
    ComplexityLevel, TaskStatus, SubTask, SubTaskResult, TaskResult
)
from ..core.context_overflow_prevention import get_context_manager
from ..core.resource_manager import ResourceManager
from ..core.error_recovery import ErrorRecoveryOrchestrator

logger = logging.getLogger(__name__)

@dataclass
class TaskExecutionPlan:
    """Plan for executing complex tasks with subtasks"""
    task_id: str
    original_task: str
    subtasks: List[SubTask]
    dependencies: Dict[str, List[str]]
    parallel_groups: List[List[str]]
    resource_requirements: Dict[str, Any]
    estimated_total_duration: float
    execution_strategy: str  # "parallel", "sequential", or "hybrid"
    risk_assessment: Dict[str, Any]
    created_at: float = field(default_factory=time.time)

class TaskDecompositionEngine:
    """Analyzes and decomposes complex tasks using LLM"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.decomposition_patterns = self._load_patterns()
    
    async def decompose_task(self, task: str, context: Dict[str, Any] = None) -> List[SubTask]:
        """Decompose a complex task into subtasks"""
        logger.info(f"Decomposing task: {task[:100]}...")
        
        # Analyze task complexity
        complexity = await self._analyze_complexity(task, context)
        
        # Use LLM to generate subtask breakdown
        subtask_specs = await self._llm_decomposition(task, complexity, context)
        
        # Convert to SubTask objects
        subtasks = []
        for spec in subtask_specs:
            subtask = SubTask(
                id=spec.get('id', str(uuid.uuid4())),
                description=spec['description'],
                complexity=self._parse_complexity(spec['complexity']),
                can_parallel=spec.get('can_parallel', True),
                dependencies=spec.get('dependencies', []),
                context=spec.get('context', {}),
                estimated_duration=spec.get('estimated_duration', 60.0),
                max_retries=spec.get('max_retries', 2),
                timeout=spec.get('timeout', 300.0)
            )
            subtasks.append(subtask)
        
        # Post-process for dependency resolution
        subtasks = await self._resolve_dependencies(subtasks)
        
        logger.info(f"Decomposed into {len(subtasks)} subtasks")
        return subtasks
    
    async def _analyze_complexity(self, task: str, context: Dict[str, Any]) -> ComplexityLevel:
        """Analyze task complexity based on various factors"""
        complexity_score = 0
        
        # Length-based indicators
        if len(task) > 1000:
            complexity_score += 2
        elif len(task) > 500:
            complexity_score += 1
        
        # Keyword indicators
        complex_keywords = [
            'analysis', 'comprehensive', 'complete', 'full', 'integrate', 
            'multiple', 'system', 'architecture', 'optimization', 'deployment'
        ]
        
        for keyword in complex_keywords:
            if keyword.lower() in task.lower():
                complexity_score += 1
        
        # Context indicators
        if context:
            if 'existing_codebase' in context:
                complexity_score += 1
            if 'large_dataset' in context:
                complexity_score += 2
            if 'performance_critical' in context:
                complexity_score += 1
        
        # Convert to complexity level
        if complexity_score >= 5:
            return ComplexityLevel.VERY_COMPLEX
        elif complexity_score >= 3:
            return ComplexityLevel.COMPLEX
        elif complexity_score >= 1:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.SIMPLE
    
    async def _llm_decomposition(self, task: str, complexity: ComplexityLevel, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use LLM to generate detailed task breakdown"""
        
        prompt = f"""
        You are a task decomposition expert. Break down this task into specific, actionable subtasks:
        
        Original Task: {task}
        Complexity Level: {complexity.value}
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Requirements for decomposition:
        1. Create specific, actionable subtasks (no vague descriptions)
        2. Ensure subtasks can be executed independently when possible
        3. Identify which subtasks can run in parallel vs must be sequential
        4. Estimate realistic durations (in seconds)
        5. Set appropriate complexity levels for each subtask
        6. Specify dependencies between subtasks clearly
        
        Return JSON in this format:
        {{
            "subtasks": [
                {{
                    "id": "unique_subtask_id",
                    "description": "Specific, actionable description",
                    "complexity": "simple|medium|complex|very_complex",
                    "can_parallel": true/false,
                    "dependencies": ["other_subtask_id"],
                    "estimated_duration": 120,
                    "max_retries": 2,
                    "timeout": 300,
                    "context": {{"focus": "relevant information for this subtask"}}
                }}
            ]
        }}
        """
        
        try:
            response = await self.llm_client.chat([
                Message(role="user", content=prompt)
            ])
            
            # Parse JSON response
            content = response.content
            if isinstance(content, dict):
                return content.get('subtasks', [])
            else:
                # Try to extract JSON from text response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return parsed.get('subtasks', [])
                
            logger.warning("Failed to parse LLM decomposition response")
            return self._fallback_decomposition(task, complexity)
            
        except Exception as e:
            logger.error(f"LLM decomposition failed: {e}")
            return self._fallback_decomposition(task, complexity)
    
    def _fallback_decomposition(self, task: str, complexity: ComplexityLevel) -> List[Dict[str, Any]]:
        """Fallback decomposition when LLM fails"""
        # Simple rule-based decomposition based on common patterns
        
        if 'analysis' in task.lower():
            return [
                {
                    'id': 'data_preparation',
                    'description': 'Prepare and clean data for analysis',
                    'complexity': 'medium',
                    'can_parallel': False,
                    'dependencies': [],
                    'estimated_duration': 300,
                    'context': {'focus': 'data handling and preprocessing'}
                },
                {
                    'id': 'analysis_execution',
                    'description': 'Perform the main analysis',
                    'complexity': complexity.value,
                    'can_parallel': True,
                    'dependencies': ['data_preparation'],
                    'estimated_duration': 600,
                    'context': {'focus': 'analysis techniques and methodologies'}
                },
                {
                    'id': 'results_interpretation',
                    'description': 'Interpret and document analysis results',
                    'complexity': 'medium',
                    'can_parallel': False,
                    'dependencies': ['analysis_execution'],
                    'estimated_duration': 300,
                    'context': {'focus': 'results interpretation and documentation'}
                }
            ]
        
        elif 'development' in task.lower() or 'build' in task.lower():
            return [
                {
                    'id': 'requirements_analysis',
                    'description': 'Analyze requirements and create technical specification',
                    'complexity': 'medium',
                    'can_parallel': False,
                    'dependencies': [],
                    'estimated_duration': 400,
                    'context': {'focus': 'requirements and technical design'}
                },
                {
                    'id': 'implementation',
                    'description': 'Implement the core functionality',
                    'complexity': complexity.value,
                    'can_parallel': True,
                    'dependencies': ['requirements_analysis'],
                    'estimated_duration': 1200,
                    'context': {'focus': 'implementation and coding'}
                },
                {
                    'id': 'testing_validation',
                    'description': 'Test and validate the implementation',
                    'complexity': 'medium',
                    'can_parallel': False,
                    'dependencies': ['implementation'],
                    'estimated_duration': 600,
                    'context': {'focus': 'testing and quality assurance'}
                },
                {
                    'id': 'documentation',
                    'description': 'Create comprehensive documentation',
                    'complexity': 'simple',
                    'can_parallel': True,
                    'dependencies': ['implementation'],
                    'estimated_duration': 300,
                    'context': {'focus': 'documentation and user guides'}
                }
            ]
        
        else:
            # Generic fallback
            return [
                {
                    'id': 'task_analysis',
                    'description': 'Analyze task requirements and approach',
                    'complexity': 'simple',
                    'can_parallel': False,
                    'dependencies': [],
                    'estimated_duration': 200,
                    'context': {'focus': 'task understanding and planning'}
                },
                {
                    'id': 'task_execution',
                    'description': 'Execute the main task components',
                    'complexity': complexity.value,
                    'can_parallel': True,
                    'dependencies': ['task_analysis'],
                    'estimated_duration': 800,
                    'context': {'focus': 'task execution and implementation'}
                },
                {
                    'id': 'task_completion',
                    'description': 'Finalize and document task completion',
                    'complexity': 'simple',
                    'can_parallel': False,
                    'dependencies': ['task_execution'],
                    'estimated_duration': 150,
                    'context': {'focus': 'completion and documentation'}
                }
            ]
    
    def _parse_complexity(self, complexity_str: str) -> ComplexityLevel:
        """Parse complexity string to enum"""
        mapping = {
            'simple': ComplexityLevel.SIMPLE,
            'medium': ComplexityLevel.MEDIUM,
            'complex': ComplexityLevel.COMPLEX,
            'very_complex': ComplexityLevel.VERY_COMPLEX
        }
        return mapping.get(complexity_str.lower(), ComplexityLevel.MEDIUM)
    
    async def _resolve_dependencies(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Resolve and validate subtask dependencies"""
        subtask_map = {st.id: st for st in subtasks}
        
        # Validate dependencies exist
        for subtask in subtasks:
            resolved_deps = []
            for dep_id in subtask.dependencies:
                if dep_id in subtask_map:
                    resolved_deps.append(dep_id)
                else:
                    logger.warning(f"Dependency {dep_id} not found for subtask {subtask.id}")
            subtask.dependencies = resolved_deps
        
        # Detect circular dependencies
        await self._check_circular_dependencies(subtasks)
        
        return subtasks
    
    async def _check_circular_dependencies(self, subtasks: List[SubTask]):
        """Check for circular dependencies"""
        def has_cycle(subtask_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            visited.add(subtask_id)
            rec_stack.add(subtask_id)
            
            subtask = next((st for st in subtasks if st.id == subtask_id), None)
            if subtask:
                for dep_id in subtask.dependencies:
                    if dep_id not in visited:
                        if has_cycle(dep_id, visited, rec_stack):
                            return True
                    elif dep_id in rec_stack:
                        return True
            
            rec_stack.remove(subtask_id)
            return False
        
        visited = set()
        for subtask in subtasks:
            if subtask.id not in visited:
                if has_cycle(subtask.id, visited, set()):
                    raise ValueError(f"Circular dependency detected involving subtask {subtask.id}")
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load decomposition patterns and heuristics"""
        return {
            'common_patterns': {
                'analysis_workflow': ['data_preparation', 'analysis_execution', 'results_interpretation'],
                'development_workflow': ['requirements_analysis', 'implementation', 'testing_validation', 'documentation'],
                'integration_workflow': ['setup', 'integration', 'validation', 'deployment']
            },
            'complexity_mapping': {
                ComplexityLevel.SIMPLE: {'max_duration': 300, 'max_retries': 1},
                ComplexityLevel.MEDIUM: {'max_duration': 600, 'max_retries': 2},
                ComplexityLevel.COMPLEX: {'max_duration': 1200, 'max_retries': 3},
                ComplexityLevel.VERY_COMPLEX: {'max_duration': 1800, 'max_retries': 3}
            }
        }

class ExecutionPlanner:
    """Plans task execution strategy and resource allocation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_parallel_tasks = config.get('max_parallel_tasks', 3)
        self.resource_manager = ResourceManager(config.get('resources', {}))
    
    async def create_execution_plan(self, subtasks: List[SubTask]) -> TaskExecutionPlan:
        """Create optimized execution plan"""
        logger.info(f"Creating execution plan for {len(subtasks)} subtasks")
        
        # Build dependency graph
        dependencies = self._build_dependency_graph(subtasks)
        
        # Identify parallel execution groups
        parallel_groups = self._identify_parallel_groups(subtasks, dependencies)
        
        # Calculate resource requirements
        resource_requirements = await self._calculate_resource_requirements(subtasks)
        
        # Estimate total duration
        estimated_duration = self._estimate_total_duration(subtasks, parallel_groups)
        
        # Assess execution risks
        risk_assessment = self._assess_execution_risks(subtasks, parallel_groups)
        
        # Determine optimal execution strategy
        strategy = self._determine_execution_strategy(subtasks, parallel_groups)
        
        plan = TaskExecutionPlan(
            task_id=str(uuid.uuid4()),
            original_task="Complex task requiring orchestration",
            subtasks=subtasks,
            dependencies=dependencies,
            parallel_groups=parallel_groups,
            resource_requirements=resource_requirements,
            estimated_total_duration=estimated_duration,
            execution_strategy=strategy,
            risk_assessment=risk_assessment
        )
        
        logger.info(f"Execution plan created: {strategy} strategy, {len(parallel_groups)} groups")
        return plan
    
    def _build_dependency_graph(self, subtasks: List[SubTask]) -> Dict[str, List[str]]:
        """Build dependency graph from subtasks"""
        dependencies = {}
        for subtask in subtasks:
            dependencies[subtask.id] = subtask.dependencies
        return dependencies
    
    def _identify_parallel_groups(self, subtasks: List[SubTask], dependencies: Dict[str, List[str]]) -> List[List[str]]:
        """Identify which subtasks can run in parallel"""
        
        # Topological sort to find execution order
        in_degree = {subtask.id: 0 for subtask in subtasks}
        for deps in dependencies.values():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        groups = []
        available_tasks = [task_id for task_id, degree in in_degree.items() if degree == 0]
        
        while available_tasks:
            # Take tasks that can run in parallel (no dependencies)
            current_group = []
            new_available = []
            
            for task_id in available_tasks:
                if self._can_run_in_parallel(task_id, current_group, subtasks):
                    current_group.append(task_id)
                else:
                    new_available.append(task_id)
            
            if current_group:
                groups.append(current_group)
            
            # Update available tasks based on dependencies
            available_tasks = new_available
            for task_id in current_group:
                for subtask in subtasks:
                    if task_id in subtask.dependencies:
                        in_degree[subtask.id] -= 1
                        if in_degree[subtask.id] == 0 and subtask.id not in available_tasks:
                            available_tasks.append(subtask.id)
        
        return groups
    
    def _can_run_in_parallel(self, task_id: str, current_group: List[str], subtasks: List[SubTask]) -> bool:
        """Check if task can run in parallel with current group"""
        task = next((st for st in subtasks if st.id == task_id), None)
        if not task or not task.can_parallel:
            return False
        
        # Check if task has dependencies on tasks in current group
        for group_task in current_group:
            if group_task in task.dependencies:
                return False
        
        return True
    
    async def _calculate_resource_requirements(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """Calculate total resource requirements"""
        total_cpu = 0
        total_memory = 0
        total_context = 0
        
        for subtask in subtasks:
            # Estimate resources based on complexity
            complexity_multipliers = {
                ComplexityLevel.SIMPLE: {'cpu': 1, 'memory': 512, 'context': 20000},
                ComplexityLevel.MEDIUM: {'cpu': 2, 'memory': 1024, 'context': 40000},
                ComplexityLevel.COMPLEX: {'cpu': 3, 'memory': 2048, 'context': 60000},
                ComplexityLevel.VERY_COMPLEX: {'cpu': 4, 'memory': 4096, 'context': 80000}
            }
            
            multipliers = complexity_multipliers.get(subtask.complexity, complexity_multipliers[ComplexityLevel.MEDIUM])
            total_cpu += multipliers['cpu']
            total_memory += multipliers['memory']
            total_context += multipliers['context']
        
        return {
            'total_cpu_cores': total_cpu,
            'total_memory_mb': total_memory,
            'total_context_tokens': total_context,
            'max_parallel_groups': len(self._identify_parallel_groups(subtasks, self._build_dependency_graph(subtasks)))
        }
    
    def _estimate_total_duration(self, subtasks: List[SubTask], parallel_groups: List[List[str]]) -> float:
        """Estimate total execution time"""
        total_time = 0
        
        for group in parallel_groups:
            # For parallel groups, take the maximum duration of tasks in the group
            group_duration = max(
                next((st.estimated_duration for st in subtasks if st.id == task_id), 0)
                for task_id in group
            )
            total_time += group_duration
        
        return total_time
    
    def _assess_execution_risks(self, subtasks: List[SubTask], parallel_groups: List[List[str]]) -> Dict[str, Any]:
        """Assess risks associated with execution plan"""
        
        risks = []
        
        # Check for very long-running tasks
        long_tasks = [st for st in subtasks if st.estimated_duration > 900]  # > 15 minutes
        if long_tasks:
            risks.append({
                'type': 'long_running_task',
                'severity': 'medium',
                'description': f"{len(long_tasks)} tasks may take > 15 minutes",
                'mitigation': 'Consider breaking down long tasks further'
            })
        
        # Check for high dependency count
        high_dependency_tasks = [st for st in subtasks if len(st.dependencies) > 3]
        if high_dependency_tasks:
            risks.append({
                'type': 'high_dependency_count',
                'severity': 'low',
                'description': f"{len(high_dependency_tasks)} tasks have > 3 dependencies",
                'mitigation': 'Consider reducing dependencies or creating intermediate tasks'
            })
        
        # Check for potential resource contention
        total_parallel_groups = len(parallel_groups)
        if total_parallel_groups > 10:
            risks.append({
                'type': 'high_parallelism',
                'severity': 'medium',
                'description': f"High parallelism ({total_parallel_groups} groups) may cause resource contention",
                'mitigation': 'Consider sequential execution for some tasks'
            })
        
        return {
            'risk_level': 'low' if len(risks) == 0 else 'medium' if len(risks) <= 2 else 'high',
            'risks': risks,
            'overall_score': max(0, 100 - len(risks) * 20)
        }
    
    def _determine_execution_strategy(self, subtasks: List[SubTask], parallel_groups: List[List[str]]) -> str:
        """Determine optimal execution strategy"""
        
        # Calculate parallelism ratio
        total_tasks = len(subtasks)
        parallel_tasks = sum(len(group) for group in parallel_groups)
        parallelism_ratio = parallel_tasks / total_tasks if total_tasks > 0 else 0
        
        # Consider resource constraints
        estimated_resources = self._calculate_resource_requirements(subtasks)
        system_resources = self.resource_manager.available_resources
        
        # Determine strategy based on factors
        if parallelism_ratio > 0.7 and estimated_resources['total_cpu_cores'] <= system_resources.cpu_cores:
            return "parallel"
        elif parallelism_ratio < 0.3 or estimated_resources['total_cpu_cores'] > system_resources.cpu_cores * 1.5:
            return "sequential"
        else:
            return "hybrid"

class SubTaskExecutor:
    """Executes individual subtasks with context isolation"""
    
    def __init__(self, agent_instance, context_manager, resource_manager, error_recovery):
        self.agent = agent_instance
        self.context_manager = context_manager
        self.resource_manager = resource_manager
        self.error_recovery = error_recovery
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def execute_subtask(self, subtask: SubTask, parent_context: Dict[str, Any]) -> SubTaskResult:
        """Execute a single subtask with isolated context"""
        start_time = time.time()
        retries = 0
        
        logger.info(f"Executing subtask: {subtask.id} - {subtask.description}")
        
        while retries <= subtask.max_retries:
            try:
                # Create isolated context for this subtask
                context = await self._create_isolated_context(subtask, parent_context)
                
                # Allocate resources
                resources = await self.resource_manager.allocate(subtask)
                
                try:
                    # Execute with timeout and error recovery
                    result = await asyncio.wait_for(
                        self._execute_with_recovery(subtask, context, resources),
                        timeout=subtask.timeout
                    )
                    
                    duration = time.time() - start_time
                    
                    logger.info(f"Subtask {subtask.id} completed successfully in {duration:.1f}s")
                    
                    return SubTaskResult(
                        subtask_id=subtask.id,
                        status=TaskStatus.COMPLETED,
                        result=result,
                        duration=duration,
                        retries_attempted=retries,
                        context_size=context.get('token_count', 0),
                        resource_usage=resources.__dict__
                    )
                    
                finally:
                    # Clean up context and resources
                    await self.context_manager.cleanup_context(subtask.id)
                    await self.resource_manager.release(subtask.id)
                    
            except asyncio.TimeoutError:
                retries += 1
                if retries > subtask.max_retries:
                    duration = time.time() - start_time
                    logger.error(f"Subtask {subtask.id} timed out after {retries} retries")
                    return SubTaskResult(
                        subtask_id=subtask.id,
                        status=TaskStatus.TIMEOUT,
                        error=f"Task timed out after {retries} retries",
                        duration=duration,
                        retries_attempted=retries
                    )
                else:
                    logger.warning(f"Subtask {subtask.id} timed out, retrying ({retries}/{subtask.max_retries})")
                    
            except Exception as e:
                retries += 1
                if retries > subtask.max_retries:
                    duration = time.time() - start_time
                    logger.error(f"Subtask {subtask.id} failed after {retries} retries: {e}")
                    return SubTaskResult(
                        subtask_id=subtask.id,
                        status=TaskStatus.FAILED,
                        error=str(e),
                        duration=duration,
                        retries_attempted=retries
                    )
                else:
                    logger.warning(f"Subtask {subtask.id} failed, retrying ({retries}/{subtask.max_retries}): {e}")
        
        # Should not reach here
        return SubTaskResult(
            subtask_id=subtask.id,
            status=TaskStatus.FAILED,
            error="Maximum retries exceeded",
            duration=time.time() - start_time,
            retries_attempted=subtask.max_retries
        )
    
    async def _create_isolated_context(self, subtask: SubTask, parent_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create isolated context for subtask"""
        return await self.context_manager.create_isolated_context(subtask, parent_context)
    
    async def _execute_with_recovery(self, subtask: SubTask, context: Dict[str, Any], resources) -> Any:
        """Execute subtask with error recovery"""
        
        # Use error recovery orchestrator
        return await self.error_recovery.execute_with_recovery(
            operation=f"subtask_{subtask.id}",
            func=self._execute_subtask_logic,
            context={'subtask': subtask, 'context': context, 'resources': resources},
            subtask=subtask,
            context_data=context,
            resources=resources
        )
    
    async def _execute_subtask_logic(self, subtask: SubTask, context_data: Dict[str, Any], resources) -> Any:
        """Execute the actual subtask logic"""
        
        # Create a focused task for the agent
        focused_task = {
            'id': subtask.id,
            'description': subtask.description,
            'context': context_data,
            'complexity': subtask.complexity.value,
            'estimated_duration': subtask.estimated_duration
        }
        
        # Execute using the agent (this integrates with existing Mini-Agent infrastructure)
        result = await self.agent.execute_task_with_context(focused_task, context_data)
        
        return result

class TaskOrchestrator:
    """Main orchestration engine for complex tasks"""
    
    def __init__(self, config: Dict[str, Any], llm_client, agent_instance):
        self.config = config
        self.llm_client = llm_client
        self.agent = agent_instance
        
        # Initialize components
        self.decomposition_engine = TaskDecompositionEngine(llm_client)
        self.execution_planner = ExecutionPlanner(config)
        self.subtask_executor = None  # Will be initialized after other components
        
        # Initialize managers
        self.context_manager = ContextIsolationManager(config.get('context', {}))
        self.resource_manager = ResourceManager(config.get('resources', {}))
        self.error_recovery = ErrorRecoveryOrchestrator(config.get('error_recovery', {}))
        
        # Complete executor initialization
        self.subtask_executor = SubTaskExecutor(agent_instance, self.context_manager, self.resource_manager, self.error_recovery)
        
        # Task registry for tracking
        self.active_tasks: Dict[str, TaskExecutionPlan] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
    
    async def execute_complex_task(self, task: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute a complex task using orchestration"""
        task_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(f"Starting orchestration for complex task: {task_id}")
        
        try:
            # Step 1: Analyze and decompose task
            subtasks = await self.decomposition_engine.decompose_task(task, context)
            
            if not subtasks:
                raise ValueError("Task decomposition failed - no subtasks generated")
            
            # Step 2: Create execution plan
            execution_plan = await self.execution_planner.create_execution_plan(subtasks)
            execution_plan.task_id = task_id
            execution_plan.original_task = task
            
            self.active_tasks[task_id] = execution_plan
            
            # Step 3: Execute plan
            subtask_results = await self._execute_plan(execution_plan)
            
            # Step 4: Aggregate results
            final_result = await self._aggregate_results(task_id, execution_plan, subtask_results)
            
            # Step 5: Generate execution summary
            execution_summary = await self._generate_execution_summary(execution_plan, final_result)
            final_result.execution_summary = execution_summary
            
            # Store completed task
            self.completed_tasks[task_id] = final_result
            
            duration = time.time() - start_time
            logger.info(f"Complex task orchestration completed in {duration:.1f}s: {task_id}")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Task orchestration failed: {task_id}, error: {e}")
            duration = time.time() - start_time
            
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error=str(e),
                total_duration=duration
            )
        
        finally:
            # Clean up active task
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
    
    async def _execute_plan(self, plan: TaskExecutionPlan) -> Dict[str, SubTaskResult]:
        """Execute the orchestration plan"""
        logger.info(f"Executing plan with {len(plan.parallel_groups)} parallel groups")
        
        subtask_results = {}
        completed_subtasks = set()
        
        # Execute parallel groups sequentially, tasks within groups in parallel
        for group_idx, group in enumerate(plan.parallel_groups):
            logger.info(f"Executing group {group_idx + 1}/{len(plan.parallel_groups)}: {group}")
            
            # Wait for dependencies
            for subtask_id in group:
                await self._wait_for_dependencies(subtask_id, plan.dependencies, completed_subtasks)
            
            # Execute group tasks in parallel
            group_tasks = []
            for subtask_id in group:
                subtask = next(st for st in plan.subtasks if st.id == subtask_id)
                task = asyncio.create_task(
                    self.subtask_executor.execute_subtask(subtask, plan.subtasks[0].context)
                )
                group_tasks.append((subtask_id, task))
            
            # Wait for group completion
            for subtask_id, task in group_tasks:
                try:
                    result = await task
                    subtask_results[subtask_id] = result
                    
                    if result.status == TaskStatus.COMPLETED:
                        completed_subtasks.add(subtask_id)
                    else:
                        logger.warning(f"Subtask {subtask_id} completed with status: {result.status}")
                        
                except Exception as e:
                    logger.error(f"Group task {subtask_id} failed: {e}")
                    subtask_results[subtask_id] = SubTaskResult(
                        subtask_id=subtask_id,
                        status=TaskStatus.FAILED,
                        error=str(e)
                    )
        
        return subtask_results
    
    async def _wait_for_dependencies(self, subtask_id: str, dependencies: Dict[str, List[str]], completed: Set[str]):
        """Wait for subtask dependencies to complete"""
        deps = dependencies.get(subtask_id, [])
        
        for dep_id in deps:
            if dep_id not in completed:
                logger.debug(f"Waiting for dependency {dep_id} before executing {subtask_id}")
                # In a more sophisticated implementation, this could use events/signals
                # For now, we'll just wait a bit and check again
                await asyncio.sleep(0.1)
                if dep_id not in completed:
                    # This is a simplified dependency wait - in practice, you'd want
                    # proper dependency tracking and notification
                    pass
    
    async def _aggregate_results(self, task_id: str, plan: TaskExecutionPlan, subtask_results: Dict[str, SubTaskResult]) -> TaskResult:
        """Aggregate subtask results into final result"""
        
        # Determine overall status
        all_completed = all(
            result.status == TaskStatus.COMPLETED 
            for result in subtask_results.values()
        )
        
        overall_status = TaskStatus.COMPLETED if all_completed else TaskStatus.FAILED
        
        # Aggregate results
        aggregated_result = {
            'task_id': task_id,
            'subtasks_executed': len(subtask_results),
            'successful_subtasks': len([r for r in subtask_results.values() if r.status == TaskStatus.COMPLETED]),
            'failed_subtasks': len([r for r in subtask_results.values() if r.status == TaskStatus.FAILED]),
            'total_duration': sum(r.duration for r in subtask_results.values()),
            'context_optimization': await self._calculate_context_optimization(subtask_results)
        }
        
        # Include individual subtask results
        for subtask_id, result in subtask_results.items():
            aggregated_result[f'subtask_{subtask_id}'] = {
                'status': result.status.value,
                'result': result.result,
                'error': result.error,
                'duration': result.duration,
                'retries': result.retries_attempted
            }
        
        return TaskResult(
            task_id=task_id,
            status=overall_status,
            result=aggregated_result,
            subtask_results=subtask_results
        )
    
    async def _calculate_context_optimization(self, subtask_results: Dict[str, SubTaskResult]) -> Dict[str, Any]:
        """Calculate context optimization metrics"""
        
        successful_tasks = [r for r in subtask_results.values() if r.status == TaskStatus.COMPLETED]
        
        if not successful_tasks:
            return {'optimization_achieved': False, 'reason': 'No successful tasks'}
        
        total_context_used = sum(r.context_size for r in successful_tasks)
        estimated_single_context = total_context_used * 2  # Rough estimate of what single execution would use
        
        optimization_achieved = total_context_used < estimated_single_context
        reduction_percentage = ((estimated_single_context - total_context_used) / estimated_single_context) * 100 if estimated_single_context > 0 else 0
        
        return {
            'optimization_achieved': optimization_achieved,
            'context_reduction_percentage': reduction_percentage,
            'total_context_tokens': total_context_used,
            'estimated_single_context_tokens': estimated_single_context,
            'tokens_saved': estimated_single_context - total_context_used
        }
    
    async def _generate_execution_summary(self, plan: TaskExecutionPlan, result: TaskResult) -> Dict[str, Any]:
        """Generate comprehensive execution summary"""
        
        successful_subtasks = len([r for r in result.subtask_results.values() if r.status == TaskStatus.COMPLETED])
        total_subtasks = len(plan.subtasks)
        
        return {
            'execution_strategy': plan.execution_strategy,
            'total_subtasks': total_subtasks,
            'successful_subtasks': successful_subtasks,
            'failed_subtasks': total_subtasks - successful_subtasks,
            'success_rate': (successful_subtasks / total_subtasks) * 100 if total_subtasks > 0 else 0,
            'parallel_groups_executed': len(plan.parallel_groups),
            'estimated_duration': plan.estimated_total_duration,
            'actual_duration': result.total_duration,
            'duration_accuracy': abs(result.total_duration - plan.estimated_total_duration) / plan.estimated_total_duration * 100,
            'risk_assessment': plan.risk_assessment,
            'resource_utilization': await self._calculate_resource_utilization(result.subtask_results),
            'performance_metrics': await self._calculate_performance_metrics(plan, result)
        }
    
    async def _calculate_resource_utilization(self, subtask_results: Dict[str, SubTaskResult]) -> Dict[str, Any]:
        """Calculate resource utilization metrics"""
        
        if not subtask_results:
            return {}
        
        total_cpu_used = sum(r.resource_usage.get('cpu_cores', 0) for r in subtask_results.values() if r.resource_usage)
        total_memory_used = sum(r.resource_usage.get('memory_mb', 0) for r in subtask_results.values() if r.resource_usage)
        
        return {
            'total_cpu_cores_utilized': total_cpu_used,
            'total_memory_mb_utilized': total_memory_used,
            'average_cpu_per_subtask': total_cpu_used / len(subtask_results) if subtask_results else 0,
            'average_memory_per_subtask': total_memory_used / len(subtask_results) if subtask_results else 0
        }
    
    async def _calculate_performance_metrics(self, plan: TaskExecutionPlan, result: TaskResult) -> Dict[str, Any]:
        """Calculate performance metrics"""
        
        successful_results = [r for r in result.subtask_results.values() if r.status == TaskStatus.COMPLETED]
        
        if not successful_results:
            return {}
        
        durations = [r.duration for r in successful_results]
        retries = sum(r.retries_attempted for r in successful_results)
        
        return {
            'average_subtask_duration': sum(durations) / len(durations),
            'fastest_subtask_duration': min(durations),
            'slowest_subtask_duration': max(durations),
            'total_retries_attempted': retries,
            'efficiency_score': len(successful_results) / (len(successful_results) + retries) * 100,
            'parallel_efficiency': len(plan.parallel_groups) / len(plan.subtasks) * 100
        }
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        return {
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'context_manager_active': hasattr(self.context_manager, 'active_contexts'),
            'resource_manager_status': self.resource_manager.get_status() if hasattr(self.resource_manager, 'get_status') else 'unknown',
            'error_recovery_enabled': self.error_recovery is not None
        }

class ContextIsolationManager:
    """Manages context isolation for subtasks"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_contexts: Dict[str, Dict[str, Any]] = {}
        self.knowledge_graph_filter = KnowledgeGraphFilter()
    
    async def create_isolated_context(self, subtask: SubTask, parent_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create isolated context for subtask"""
        task_id = subtask.id
        
        # Create minimal context focused on subtask
        isolated_context = {
            'task_id': task_id,
            'subtask_description': subtask.description,
            'complexity': subtask.complexity.value,
            'parent_context_summary': self._summarize_context(parent_context),
            'relevant_entities': await self._get_relevant_entities(subtask),
            'focused_instructions': self._generate_focused_instructions(subtask),
            'token_count': 0,
            'created_at': time.time()
        }
        
        # Store active context
        self.active_contexts[task_id] = isolated_context
        
        logger.debug(f"Created isolated context for subtask: {task_id}")
        return isolated_context
    
    async def cleanup_context(self, task_id: str):
        """Clean up subtask context"""
        if task_id in self.active_contexts:
            del self.active_contexts[task_id]
            logger.debug(f"Cleaned up context for subtask: {task_id}")
    
    def _summarize_context(self, context: Dict[str, Any]) -> str:
        """Summarize parent context for subtask"""
        if not context:
            return "No parent context"
        
        # Extract key information
        key_elements = []
        
        if 'project_type' in context:
            key_elements.append(f"Project: {context['project_type']}")
        if 'requirements' in context:
            key_elements.append(f"Requirements: {str(context['requirements'])[:100]}")
        if 'constraints' in context:
            key_elements.append(f"Constraints: {str(context['constraints'])[:100]}")
        
        return "; ".join(key_elements) if key_elements else str(context)[:200]
    
    async def _get_relevant_entities(self, subtask: SubTask) -> List[str]:
        """Get relevant knowledge graph entities for subtask"""
        return await self.knowledge_graph_filter.filter_entities(subtask.description, subtask.complexity)
    
    def _generate_focused_instructions(self, subtask: SubTask) -> str:
        """Generate focused instructions for subtask execution"""
        return f"""
        Execute the following subtask with focused attention:
        
        Subtask: {subtask.description}
        Complexity: {subtask.complexity.value}
        Timeout: {subtask.timeout} seconds
        
        Focus on:
        1. Specific requirements for this subtask
        2. Relevant patterns and best practices
        3. Quality and completeness
        4. Integration points with other subtasks
        
        Avoid:
        1. Unnecessary exploration
        2. Overly detailed analysis
        3. Scope creep beyond this subtask
        """

class KnowledgeGraphFilter:
    """Filters knowledge graph entities for task relevance"""
    
    async def filter_entities(self, task_description: str, complexity: ComplexityLevel) -> List[str]:
        """Filter entities relevant to the task"""
        # This is a simplified implementation
        # In practice, this would integrate with the actual knowledge graph
        
        # Extract keywords from task description
        keywords = self._extract_keywords(task_description)
        
        # Map keywords to entity types (simplified)
        entity_mapping = {
            'analysis': ['Data Analysis Patterns', 'Statistical Methods'],
            'development': ['Software Architecture', 'Code Patterns'],
            'api': ['API Design', 'RESTful Patterns'],
            'database': ['Database Design', 'SQL Patterns'],
            'authentication': ['Security Patterns', 'Auth Methods'],
            'performance': ['Optimization Techniques', 'Performance Patterns'],
            'testing': ['Testing Strategies', 'Quality Assurance'],
            'deployment': ['DevOps Patterns', 'Infrastructure']
        }
        
        relevant_entities = []
        for keyword in keywords:
            if keyword in entity_mapping:
                relevant_entities.extend(entity_mapping[keyword])
        
        # Remove duplicates and limit to reasonable number
        return list(set(relevant_entities))[:10]  # Max 10 entities per subtask
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        import re
        
        # Convert to lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Keep relevant technical terms
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        return keywords

# Export main classes
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
