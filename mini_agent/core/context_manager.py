#!/usr/bin/env python3
"""
Context Isolation Manager for Task Orchestration
===============================================

Manages isolated contexts for parallel task execution to prevent context overflow
and ensure each subtask has appropriate context boundaries.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Set, Optional
from enum import Enum

from .context_overflow_prevention import MiniAgentContextManager
from ..tools.note_tool import SessionNoteTool

logger = logging.getLogger(__name__)

class ContextTier(Enum):
    """Context priority tiers for optimization"""
    CRITICAL = "critical"        # System prompt, current task
    RECENT = "recent"            # Recent conversation messages  
    SUMMARIZED = "summarized"    # Older content (intelligently summarized)
    TOOL_RESULTS = "tool"        # Tool execution results
    KNOWLEDGE = "knowledge"      # Knowledge graph entities

@dataclass
class TaskContext:
    """Isolated context for a specific task"""
    task_id: str
    context_manager: MiniAgentContextManager
    active_entities: Set[str]
    created_at: float
    token_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    tier_distribution: Dict[str, int] = field(default_factory=dict)  # tier -> token count

@dataclass
class ContextAllocation:
    """Resource allocation for task context"""
    task_id: str
    max_tokens: int
    reserved_tokens: int = 0
    allocated_at: float = field(default_factory=time.time)
    usage_history: List[Dict[str, Any]] = field(default_factory=list)

class ContextIsolationManager:
    """Manages isolated contexts for parallel task execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_contexts: Dict[str, TaskContext] = {}
        self.knowledge_graph = self._initialize_knowledge_graph()
        self.context_allocations: Dict[str, ContextAllocation] = {}
        
        # Configuration
        self.max_context_tokens = config.get('max_tokens_per_task', 80000)
        self.context_cleanup_interval = config.get('cleanup_interval', 300)  # 5 minutes
        self.knowledge_graph_filter = KnowledgeGraphFilter()
        
        # Start background cleanup task
        asyncio.create_task(self._cleanup_loop())
    
    async def create_isolated_context(self, subtask, parent_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create isolated context for a subtask"""
        task_id = subtask.id
        
        # Create context allocation
        allocation = await self._allocate_context_resources(subtask)
        
        # Create isolated context manager
        context_manager = MiniAgentContextManager(f"task-{task_id}")
        
        # Filter knowledge graph to relevant entities
        relevant_entities = await self.knowledge_graph_filter.filter_relevant_entities(
            subtask.description, subtask.requirements if hasattr(subtask, 'requirements') else []
        )
        
        # Create task context
        task_context = TaskContext(
            task_id=task_id,
            context_manager=context_manager,
            active_entities=relevant_entities,
            created_at=asyncio.get_event_loop().time(),
            token_count=0,
            metadata={
                'subtask_description': subtask.description,
                'complexity': subtask.complexity.value,
                'allocation': allocation
            },
            tier_distribution={
                ContextTier.CRITICAL.value: 0,
                ContextTier.RECENT.value: 0,
                ContextTier.SUMMARIZED.value: 0,
                ContextTier.TOOL_RESULTS.value: 0,
                ContextTier.KNOWLEDGE.value: len(relevant_entities) * 50  # Estimate
            }
        )
        
        self.active_contexts[task_id] = task_context
        self.context_allocations[task_id] = allocation
        
        # Load relevant content into context
        await self._load_context_content(task_context, parent_context)
        
        logger.info(f"Created isolated context for task: {task_id} (max {allocation.max_tokens} tokens)")
        
        return await self._serialize_context(task_context)
    
    async def update_context_activity(self, task_id: str, context_updates: Dict[str, Any]):
        """Update context activity and token usage"""
        if task_id not in self.active_contexts:
            logger.warning(f"Context not found for task: {task_id}")
            return
        
        context = self.active_contexts[task_id]
        
        # Update token count
        if 'token_count' in context_updates:
            context.token_count = context_updates['token_count']
        
        # Update tier distribution
        if 'tier_distribution' in context_updates:
            context.tier_distribution.update(context_updates['tier_distribution'])
        
        # Record usage
        allocation = self.context_allocations.get(task_id)
        if allocation:
            allocation.usage_history.append({
                'timestamp': time.time(),
                'token_count': context.token_count,
                'tier_distribution': context.tier_distribution.copy()
            })
            
            # Keep only recent usage history
            if len(allocation.usage_history) > 100:
                allocation.usage_history = allocation.usage_history[-50:]
    
    async def cleanup_context(self, task_id: str):
        """Clean up task context"""
        if task_id in self.active_contexts:
            context = self.active_contexts[task_id]
            
            # Save context summary if needed
            if context.token_count > 1000:  # Save only substantial contexts
                await self._save_context_summary(context)
            
            # Remove from active contexts
            del self.active_contexts[task_id]
            
            # Remove allocation
            if task_id in self.context_allocations:
                del self.context_allocations[task_id]
            
            logger.info(f"Cleaned up context for task: {task_id}")
    
    async def get_context_status(self) -> Dict[str, Any]:
        """Get status of all active contexts"""
        total_tokens = sum(ctx.token_count for ctx in self.active_contexts.values())
        total_allocations = sum(alloc.max_tokens for alloc in self.context_allocations.values())
        
        return {
            'active_contexts': len(self.active_contexts),
            'total_context_tokens': total_tokens,
            'total_allocated_tokens': total_allocations,
            'utilization_percentage': (total_tokens / total_allocations * 100) if total_allocations > 0 else 0,
            'contexts': {
                task_id: {
                    'token_count': ctx.token_count,
                    'max_tokens': self.context_allocations[task_id].max_tokens,
                    'created_at': ctx.created_at,
                    'tier_distribution': ctx.tier_distribution,
                    'active_entities': len(ctx.active_entities)
                }
                for task_id, ctx in self.active_contexts.items()
            }
        }
    
    async def _allocate_context_resources(self, subtask) -> ContextAllocation:
        """Allocate context resources based on subtask complexity"""
        
        # Base allocation by complexity
        complexity_allocations = {
            'simple': 20000,
            'medium': 40000, 
            'complex': 60000,
            'very_complex': 80000
        }
        
        base_allocation = complexity_allocations.get(subtask.complexity.value, 40000)
        
        # Adjust based on estimated duration (longer tasks need more context)
        duration_multiplier = min(2.0, subtask.estimated_duration / 300)  # Cap at 2x for very long tasks
        
        max_tokens = int(base_allocation * duration_multiplier)
        max_tokens = min(max_tokens, self.max_context_tokens)  # Don't exceed global limit
        
        return ContextAllocation(
            task_id=subtask.id,
            max_tokens=max_tokens,
            reserved_tokens=int(max_tokens * 0.1)  # Reserve 10% for overhead
        )
    
    async def _load_context_content(self, context: TaskContext, parent_context: Dict[str, Any]):
        """Load relevant content into task context"""
        
        # Load system-critical content
        critical_tokens = await self._load_critical_content(context)
        context.tier_distribution[ContextTier.CRITICAL.value] = critical_tokens
        
        # Load parent context summary
        recent_tokens = await self._load_parent_context_summary(context, parent_context)
        context.tier_distribution[ContextTier.RECENT.value] = recent_tokens
        
        # Load knowledge graph entities
        knowledge_tokens = await self._load_knowledge_entities(context)
        context.tier_distribution[ContextTier.KNOWLEDGE.value] = knowledge_tokens
        
        # Estimate total
        context.token_count = sum(context.tier_distribution.values())
        
        logger.debug(f"Loaded context content for {context.task_id}: {context.token_count} tokens")
    
    async def _load_critical_content(self, context: TaskContext) -> int:
        """Load critical system content"""
        # Load essential system prompts, configuration, etc.
        # This is a simplified implementation
        
        system_content = [
            "You are Mini-Agent, a versatile AI assistant.",
            "Focus on the specific subtask assigned to you.",
            "Maintain context boundaries and avoid scope creep.",
            "Use appropriate tools and follow best practices."
        ]
        
        content = "\n".join(system_content)
        
        # Estimate token count (rough calculation)
        estimated_tokens = len(content) // 4
        
        return estimated_tokens
    
    async def _load_parent_context_summary(self, context: TaskContext, parent_context: Dict[str, Any]) -> int:
        """Load summarized parent context"""
        if not parent_context:
            return 0
        
        # Extract key information from parent context
        summary_elements = []
        
        if 'project_type' in parent_context:
            summary_elements.append(f"Project Type: {parent_context['project_type']}")
        
        if 'requirements' in parent_context:
            req_summary = str(parent_context['requirements'])[:200]
            summary_elements.append(f"Requirements: {req_summary}")
        
        if 'constraints' in parent_context:
            constraint_summary = str(parent_context['constraints'])[:200]
            summary_elements.append(f"Constraints: {constraint_summary}")
        
        # Create summary
        summary = "; ".join(summary_elements)
        
        if summary:
            # Add to context manager
            context.context_manager.add_content(summary, ContextTier.RECENT)
        
        # Estimate tokens
        return len(summary) // 4 if summary else 0
    
    async def _load_knowledge_entities(self, context: TaskContext) -> int:
        """Load relevant knowledge graph entities"""
        total_tokens = 0
        
        for entity_id in context.active_entities:
            try:
                # Get entity from knowledge graph
                entity_data = await self.knowledge_graph.get_entity(entity_id)
                
                if entity_data:
                    # Format entity content
                    entity_content = f"Entity: {entity_data.get('name', entity_id)}\n"
                    entity_content += f"Type: {entity_data.get('type', 'unknown')}\n"
                    
                    # Add observations (limit to avoid bloat)
                    observations = entity_data.get('observations', [])[:5]  # Max 5 observations
                    for obs in observations:
                        entity_content += f"- {obs}\n"
                    
                    # Add to context manager
                    context.context_manager.add_content(entity_content, ContextTier.KNOWLEDGE)
                    
                    total_tokens += len(entity_content) // 4
                    
            except Exception as e:
                logger.warning(f"Failed to load entity {entity_id}: {e}")
        
        return total_tokens
    
    async def _save_context_summary(self, context: TaskContext):
        """Save context summary for future reference"""
        summary = {
            'task_id': context.task_id,
            'created_at': context.created_at,
            'final_token_count': context.token_count,
            'tier_distribution': context.tier_distribution,
            'active_entities': list(context.active_entities),
            'summary': f"Task context with {context.token_count} tokens across {len(context.tier_distribution)} tiers"
        }
        
        # This could be saved to a summary database or file
        logger.info(f"Saved context summary for task: {context.task_id}")
    
    async def _serialize_context(self, context: TaskContext) -> Dict[str, Any]:
        """Serialize context for use in task execution"""
        return {
            'task_id': context.task_id,
            'max_tokens': self.context_allocations[context.task_id].max_tokens,
            'current_tokens': context.token_count,
            'tier_distribution': context.tier_distribution,
            'active_entities': list(context.active_entities),
            'created_at': context.created_at,
            'metadata': context.metadata,
            'context_manager': context.context_manager  # This would need serialization in practice
        }
    
    def _initialize_knowledge_graph(self):
        """Initialize knowledge graph interface"""
        # This would integrate with the actual knowledge graph system
        # For now, return a mock interface
        return MockKnowledgeGraph()
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                current_time = time.time()
                
                # Find contexts to cleanup
                contexts_to_cleanup = []
                
                for task_id, context in self.active_contexts.items():
                    # Check if context is stale (no activity for 30 minutes)
                    if current_time - context.created_at > 1800:  # 30 minutes
                        contexts_to_cleanup.append(task_id)
                
                # Cleanup stale contexts
                for task_id in contexts_to_cleanup:
                    await self.cleanup_context(task_id)
                
                # Sleep before next cleanup cycle
                await asyncio.sleep(self.context_cleanup_interval)
                
            except Exception as e:
                logger.error(f"Error in context cleanup loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

class KnowledgeGraphFilter:
    """Filters knowledge graph to relevant entities for tasks"""
    
    def __init__(self):
        self.keyword_mapping = {
            'analysis': ['Data Analysis', 'Statistics', 'Machine Learning', 'Pattern Recognition'],
            'development': ['Software Architecture', 'Code Patterns', 'API Design', 'Database Design'],
            'authentication': ['Security Patterns', 'Authentication', 'Authorization', 'Session Management'],
            'performance': ['Optimization', 'Caching', 'Scalability', 'Performance Monitoring'],
            'testing': ['Testing Strategies', 'Quality Assurance', 'Test Automation', 'Unit Testing'],
            'deployment': ['DevOps', 'CI/CD', 'Infrastructure', 'Cloud Deployment'],
            'api': ['REST API', 'GraphQL', 'API Design', 'Web Services'],
            'database': ['SQL', 'Database Design', 'Data Modeling', 'Query Optimization'],
            'frontend': ['User Interface', 'JavaScript', 'CSS', 'Web Development'],
            'backend': ['Server Architecture', 'Microservices', 'API Development', 'Data Processing']
        }
    
    async def filter_relevant_entities(self, task_description: str, requirements: List[str] = None) -> Set[str]:
        """Filter knowledge graph entities relevant to the task"""
        
        # Combine task description and requirements
        full_text = task_description
        if requirements:
            full_text += " " + " ".join(requirements)
        
        # Extract keywords
        keywords = self._extract_keywords(full_text.lower())
        
        # Find relevant entities
        relevant_entities = set()
        
        for keyword in keywords:
            if keyword in self.keyword_mapping:
                relevant_entities.update(self.keyword_mapping[keyword])
        
        # Add generic entities based on context
        if 'web' in full_text.lower() or 'http' in full_text.lower():
            relevant_entities.update(['Web Development', 'HTTP', 'REST API'])
        
        if 'data' in full_text.lower():
            relevant_entities.update(['Data Analysis', 'Database Design', 'Data Processing'])
        
        if 'user' in full_text.lower() or 'interface' in full_text.lower():
            relevant_entities.update(['User Interface', 'User Experience', 'Frontend Development'])
        
        # Limit to reasonable number
        return list(relevant_entities)[:10]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        import re
        
        # Extract words and filter
        words = re.findall(r'\b\w{3,}\b', text)
        
        # Filter out common words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'will', 'with',
            'from', 'have', 'they', 'know', 'want', 'been', 'good', 'much', 'some',
            'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make',
            'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were', 'what'
        }
        
        keywords = [word for word in words if word not in stop_words]
        
        return keywords

class MockKnowledgeGraph:
    """Mock knowledge graph for development"""
    
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity data (mock implementation)"""
        
        # Mock entity data
        mock_entities = {
            'Data Analysis': {
                'name': 'Data Analysis',
                'type': 'Methodology',
                'observations': [
                    'Systematic examination of data to extract insights',
                    'Involves statistical techniques and visualization',
                    'Essential for evidence-based decision making',
                    'Requires clean, well-structured data'
                ]
            },
            'Software Architecture': {
                'name': 'Software Architecture',
                'type': 'Design Pattern',
                'observations': [
                    'Fundamental organization of software systems',
                    'Defines components, relationships, and interactions',
                    'Influences scalability, maintainability, and performance',
                    'Should consider both functional and non-functional requirements'
                ]
            },
            'Security Patterns': {
                'name': 'Security Patterns',
                'type': 'Best Practice',
                'observations': [
                    'Proven solutions to common security problems',
                    'Include authentication, authorization, and data protection',
                    'Essential for building secure applications',
                    'Should be implemented consistently across the system'
                ]
            }
        }
        
        return mock_entities.get(entity_id)

# Export main classes
__all__ = [
    'ContextIsolationManager',
    'TaskContext', 
    'ContextAllocation',
    'ContextTier',
    'KnowledgeGraphFilter'
]
