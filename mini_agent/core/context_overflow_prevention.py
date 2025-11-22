"""
Context Overflow Prevention Integration for Mini-Agent
======================================================

This module provides context overflow prevention for MiniMax-M2
by integrating the optimized prevention system into our agent.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ContextTier(Enum):
    """Context priority tiers for optimization"""
    CRITICAL = "critical"        # System prompt, current task
    RECENT = "recent"            # Recent conversation messages  
    SUMMARIZED = "summarized"    # Older content (intelligently summarized)
    TOOL_RESULTS = "tool"        # Tool execution results


@dataclass
class ContextSegment:
    """Context segment with metadata for optimization"""
    content: str
    tier: ContextTier
    tokens: int
    source: str
    timestamp: float
    metadata: Dict[str, Any] = None


class MiniAgentContextManager:
    """
    Context overflow prevention manager for Mini-Agent
    Integrates with existing agent token estimation and summarization
    """
    
    def __init__(self, model_name: str = "MiniMax-M2"):
        self.model_name = model_name
        self.max_tokens = 200000  # MiniMax-M2 supports 200K
        
        # Conservative safety thresholds
        self.warning_threshold = int(self.max_tokens * 0.60)    # 120K (60%)
        self.safe_threshold = int(self.max_tokens * 0.75)       # 150K (75%)
        self.overflow_threshold = int(self.max_tokens * 0.95)   # 190K (95%)
        
        self.current_tokens = 0
        self.optimization_count = 0
        
        # Model-specific strategy
        self.strategy = {
            "name": "MiniMax-M2",
            "optimization_level": "balanced", 
            "preserve_detail": "moderate",
            "tool_focus": "agentic_capabilities"
        }

    def check_token_budget_before_llm(self, messages: List[Dict]) -> bool:
        """
        Check token budget before making LLM call
        
        Args:
            messages: Current message context
            
        Returns:
            True if budget is healthy, False if optimization needed
        """
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            # Fallback estimation if tiktoken unavailable
            return self._estimate_tokens_fallback(messages) < self.safe_threshold
        
        total_tokens = 0
        for msg in messages:
            # Count content
            if isinstance(msg.get('content'), str):
                total_tokens += len(encoding.encode(msg['content']))
            elif isinstance(msg.get('content'), list):
                for block in msg['content']:
                    if isinstance(block, dict):
                        total_tokens += len(encoding.encode(str(block)))
            
            # Add metadata overhead
            total_tokens += 4
        
        self.current_tokens = total_tokens
        
        # Check thresholds
        if total_tokens > self.overflow_threshold:
            logger.warning(f"CRITICAL: Token budget exceeded ({total_tokens}/{self.max_tokens})")
            return False
        elif total_tokens > self.safe_threshold:
            logger.warning(f"Token budget approaching limit ({total_tokens}/{self.max_tokens})")
            return True  # Still OK but needs monitoring
        else:
            logger.info(f"Token budget healthy ({total_tokens}/{self.max_tokens})")
            return True

    def _estimate_tokens_fallback(self, messages: List[Dict]) -> int:
        """Fallback token estimation"""
        total_chars = 0
        for msg in messages:
            content = msg.get('content', '')
            if isinstance(content, str):
                total_chars += len(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        total_chars += len(str(block))
        return int(total_chars / 2.5)  # Rough estimation

    def get_optimization_recommendations(self) -> List[str]:
        """Get recommendations for context optimization"""
        recommendations = []
        
        if self.current_tokens > self.safe_threshold:
            recommendations.append("Consider summarizing older messages")
            recommendations.append("Archive less relevant tool results")
            recommendations.append("Clean up verbose thinking content")
        
        if self.current_tokens > self.warning_threshold:
            recommendations.append("Monitor context growth carefully")
            recommendations.append("Prepare for proactive summarization")
        
        return recommendations

    def should_emergency_optimize(self) -> bool:
        """Check if emergency optimization is needed"""
        return self.current_tokens > self.safe_threshold

    def get_status_report(self) -> Dict[str, Any]:
        """Get current context status for monitoring"""
        return {
            "current_tokens": self.current_tokens,
            "max_tokens": self.max_tokens,
            "usage_percentage": (self.current_tokens / self.max_tokens) * 100,
            "optimization_count": self.optimization_count,
            "thresholds": {
                "warning": self.warning_threshold,
                "safe": self.safe_threshold, 
                "overflow": self.overflow_threshold
            },
            "recommendations": self.get_optimization_recommendations(),
            "needs_optimization": self.should_emergency_optimize()
        }


# Global context manager instance (integrates with agent.py)
_context_manager = None

def get_context_manager() -> MiniAgentContextManager:
    """Get global context manager instance"""
    global _context_manager
    if _context_manager is None:
        _context_manager = MiniAgentContextManager()
    return _context_manager

def reset_context_manager():
    """Reset context manager for new agent session"""
    global _context_manager
    _context_manager = None
