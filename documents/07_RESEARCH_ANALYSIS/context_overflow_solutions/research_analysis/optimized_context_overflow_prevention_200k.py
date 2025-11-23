"""
Optimized Context Overflow Prevention - 200K Context Windows
============================================================

Updated implementation for both MiniMax-M2 and GLM-4.6 with 200K context windows.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


# ANSI colors for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_BLUE = "\033[94m"


class ContextTier(Enum):
    """Context priority tiers for 200K optimization"""
    CRITICAL = "critical"        # System prompt, current task
    RECENT = "recent"            # Recent conversation messages
    SUMMARIZED = "summarized"    # Older content (intelligently summarized)
    TOOL_RESULTS = "tool"        # Tool execution results (optimized)


@dataclass
class ContextSegment:
    """Context segment with metadata for 200K optimization"""
    content: str
    tier: ContextTier
    tokens: int
    source: str
    timestamp: float
    metadata: Dict[str, Any] = None


class OptimizedTokenBudgetManager:
    """
    Proactive token budget manager for 200K context windows
    Implements industry-standard prevention over recovery approach
    """
    
    def __init__(self, model_name: str = "MiniMax-M2"):
        self.model_name = model_name
        self.max_tokens = 200000  # Both models support 200K
        
        # Conservative thresholds for safety
        self.warning_threshold = int(self.max_tokens * 0.60)    # 120K (60%)
        self.safe_threshold = int(self.max_tokens * 0.75)       # 150K (75%)
        self.overflow_threshold = int(self.max_tokens * 0.95)   # 190K (95%)
        
        self.current_tokens = 0
        self.optimization_count = 0
        
        # Model-specific optimization strategies
        if "glm" in model_name.lower():
            self.strategy = {
                "name": "GLM-4.6",
                "optimization_level": "aggressive",
                "preserve_detail": "compressed",
                "tool_focus": "coding_performance"
            }
        else:
            self.strategy = {
                "name": "MiniMax-M2", 
                "optimization_level": "balanced",
                "preserve_detail": "moderate",
                "tool_focus": "agentic_capabilities"
            }
    
    def check_budget_before_llm(self, context: List) -> bool:
        """
        Proactive token budget check BEFORE LLM call
        This is the critical prevention vs recovery strategy
        """
        try:
            estimated_tokens = self._estimate_tokens_accurate(context)
            utilization = estimated_tokens / self.max_tokens
            
            # Log current status with colors
            print(f"{Colors.BRIGHT_CYAN}[200K BUDGET] Model: {self.strategy['name']} | "
                  f"Context: {estimated_tokens:,}/{self.max_tokens:,} tokens ({utilization:.1%}){Colors.RESET}")
            
            # Multiple warning levels
            if estimated_tokens > self.overflow_threshold:
                print(f"{Colors.BRIGHT_RED}[CRITICAL] Overflow risk: {estimated_tokens:,}/{self.overflow_threshold:,} tokens{Colors.RESET}")
                self.optimization_count += 1
                return False
                
            elif estimated_tokens > self.safe_threshold:
                print(f"{Colors.BRIGHT_YELLOW}[WARNING] Approaching limit: {estimated_tokens:,}/{self.safe_threshold:,} tokens{Colors.RESET}")
                print(f"{Colors.DIM}  Recommended: Context optimization{Colors.RESET}")
                return True  # Allow but warn
                
            else:
                print(f"{Colors.BRIGHT_GREEN}[SAFE] Well within limits: {estimated_tokens:,}/{self.safe_threshold:,} tokens{Colors.RESET}")
                return True
                
        except Exception as e:
            print(f"{Colors.BRIGHT_YELLOW}[BUDGET] Check failed: {e} - proceeding cautiously{Colors.RESET}")
            return True  # Fail safe - allow call if check fails
    
    def _estimate_tokens_accurate(self, context: List) -> int:
        """More accurate token estimation for 200K contexts"""
        total_tokens = 0
        
        for msg in context:
            if hasattr(msg, 'content') and msg.content:
                # Content estimation
                content_tokens = self._estimate_content_tokens(msg.content)
                total_tokens += content_tokens
                
                # Thinking overhead
                if hasattr(msg, 'thinking') and msg.thinking:
                    total_tokens += self._estimate_content_tokens(msg.thinking)
                
                # Tool calls overhead
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    total_tokens += self._estimate_content_tokens(str(msg.tool_calls))
                
                # Message metadata overhead
                total_tokens += 8  # Rough estimate per message
        
        return total_tokens
    
    def _estimate_content_tokens(self, content) -> int:
        """Estimate tokens for content"""
        content_str = str(content)
        
        # For large content, use rough estimation
        if len(content_str) > 1000:
            # Rough estimation: 4 characters ≈ 1 token
            return len(content_str) // 4
        
        # For smaller content, try to use more accurate counting
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(content_str))
        except:
            # Fallback to rough estimation
            return len(content_str) // 4
    
    def update_actual_tokens(self, actual_tokens: int):
        """Update with actual token usage from LLM response"""
        self.current_tokens = max(self.current_tokens, actual_tokens)
        
        # Log if actual usage exceeded estimate
        if actual_tokens > self.estimate_tokens():
            print(f"{Colors.DIM}[BUDGET] Actual usage: {actual_tokens:,} tokens (estimate was conservative){Colors.RESET}")
    
    def get_optimization_strategies(self) -> List[str]:
        """Get model-specific optimization strategies"""
        strategies = [
            "remove_verbose_tool_outputs",
            "compress_conversation_history", 
            "summarize_older_content",
            "emergency_context_reduction"
        ]
        
        # GLM-4.6: Focus on coding and tool performance
        if self.strategy["optimization_level"] == "aggressive":
            strategies.insert(0, "aggressive_tool_compression")
            strategies.insert(1, "code_focused_optimization")
        
        return strategies


class AdvancedContextOptimizer:
    """
    Context optimizer specifically designed for 200K token windows
    Implements model-aware optimization strategies
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        
        # Model-specific optimization configuration
        if "glm" in model_name.lower():
            self.config = {
                "max_tool_output_chars": 300,        # Aggressive compression
                "preserve_directory_samples": 5,     # Minimal samples
                "git_detail_level": "compressed",    # Compressed git info
                "conversation_preservation": 6,      # Last 6 messages
                "optimization_priority": "aggressive"
            }
        else:  # MiniMax-M2
            self.config = {
                "max_tool_output_chars": 600,        # Balanced compression
                "preserve_directory_samples": 12,    # More samples
                "git_detail_level": "detailed",      # Detailed git info
                "conversation_preservation": 8,      # Last 8 messages
                "optimization_priority": "balanced"
            }
    
    def optimize_tool_result(self, tool_name: str, result_content: str) -> str:
        """Optimize tool results based on tool type and model"""
        
        # Bash command optimization
        if tool_name == "bash":
            return self._optimize_bash_result(result_content)
        
        # File operation optimization
        elif "file" in tool_name.lower():
            return self._optimize_file_result(result_content)
        
        # Other tools - basic optimization
        else:
            return self._basic_optimization(result_content)
    
    def _optimize_bash_result(self, content: str) -> str:
        """Optimize bash command outputs with 200K awareness"""
        lines = content.split('\n')
        
        # Directory listing optimization (most common tool output)
        if any(cmd in content for cmd in ["Get-ChildItem", "ls", "dir"]):
            return self._optimize_directory_listing_200k(lines)
        
        # Git command optimization
        elif "git" in content.lower():
            return self._optimize_git_output_200k(content)
        
        # Generic bash optimization
        else:
            return self._optimize_generic_bash_200k(content)
    
    def _optimize_directory_listing_200k(self, lines: List[str]) -> str:
        """Optimize directory listings for 200K context windows"""
        dirs = [line for line in lines if line.strip().startswith('d---')]
        files = [line for line in lines if line.strip().startswith('-a---')]
        
        # Extract directory names based on model strategy
        sample_limit = self.config["preserve_directory_samples"]
        dir_names = []
        
        for line in dirs[:sample_limit]:
            parts = line.split()
            if len(parts) > 0:
                dir_names.append(parts[-1])
        
        # Create optimized summary
        if self.config["optimization_priority"] == "aggressive":
            # GLM-4.6: Minimal compression
            return f"Filesystem: {len(dirs)} directories, {len(files)} files"
        else:
            # MiniMax-M2: Moderate detail
            sample_text = ', '.join(dir_names)
            overflow_note = f"... +{len(dir_names)-sample_limit} more" if len(dir_names) > sample_limit else ""
            
            return f"Directory: {len(dirs)} dirs, {len(files)} files | Sample: {sample_text} {overflow_note}".strip()
    
    def _optimize_git_output_200k(self, content: str) -> str:
        """Optimize git outputs for 200K context windows"""
        # Count git status changes
        modified = content.count('modified:')
        new_files = content.count('new file:')
        deleted = content.count('deleted:')
        
        if self.config["git_detail_level"] == "detailed":
            # MiniMax-M2: More detailed git info
            return f"Git status: {modified} modified, {new_files} new, {deleted} deleted files"
        else:
            # GLM-4.6: Compressed git info
            return f"Git: {modified} mod, {new_files} new, {deleted} del"
    
    def _optimize_generic_bash_200k(self, content: str) -> str:
        """Optimize generic bash outputs for 200K contexts"""
        max_chars = self.config["max_tool_output_chars"]
        
        if len(content) <= max_chars:
            return content
        
        # Truncate with context preservation
        lines = content.split('\n')
        preserved_lines = []
        
        for line in lines:
            if len('\n'.join(preserved_lines + [line])) > max_chars:
                break
            preserved_lines.append(line)
        
        truncated = '\n'.join(preserved_lines)
        if len(content) > len(truncated):
            truncated += f"\n... ({len(lines) - len(preserved_lines)} more lines)"
        
        return truncated
    
    def _optimize_file_result(self, content: str) -> str:
        """Optimize file operation results"""
        max_chars = self.config["max_tool_output_chars"]
        
        if len(content) > max_chars:
            return f"File operation completed ({len(content)} characters)"
        return content
    
    def _basic_optimization(self, content: str) -> str:
        """Basic content optimization for any tool"""
        max_chars = self.config["max_tool_output_chars"]
        
        if len(content) > max_chars:
            return content[:max_chars] + "..."
        return content


class ContextTierManager200K:
    """
    Context tiering system optimized for 200K token windows
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.max_context = 200000
        
        # Tier allocations optimized for 200K windows
        self.tier_allocations = {
            'critical': 0.60,      # 120K - System prompt + current task
            'recent': 0.25,        # 50K - Recent conversation
            'tool_results': 0.10,  # 20K - Optimized tool results
            'historical': 0.05     # 10K - Historical summaries
        }
        
        self.tiers = {
            'critical': [],
            'recent': [],
            'tool_results': [],
            'historical': []
        }
        
        # Model-specific tier management
        if "glm" in model_name.lower():
            self.tier_config = {
                "recent_preservation": 6,        # Keep last 6 messages
                "tool_result_limit": 3,          # Keep last 3 tool results
                "optimization_level": "aggressive"
            }
        else:  # MiniMax-M2
            self.tier_config = {
                "recent_preservation": 8,        # Keep last 8 messages
                "tool_result_limit": 4,          # Keep last 4 tool results
                "optimization_level": "balanced"
            }
    
    def add_context_segment(self, content: str, tier: ContextTier, source: str, metadata: Dict = None):
        """Add content to appropriate tier with 200K optimization"""
        
        estimated_tokens = len(content) // 4  # Rough estimation
        
        # Route to appropriate tier
        if tier == ContextTier.CRITICAL:
            # Critical content replaces existing
            self.tiers[tier] = [content]
        
        elif tier == ContextTier.RECENT:
            # Recent conversation with limit
            self.tiers[tier].append(content)
            
            # Manage tier size
            max_recent = self.tier_config["recent_preservation"]
            if len(self.tiers[tier]) > max_recent:
                old_content = self.tiers[tier].pop(0)
                # Move to historical tier
                self._create_and_add_summary(old_content, ContextTier.SUMMARIZED)
        
        elif tier == ContextTier.TOOL_RESULTS:
            # Tool results always optimized and limited
            optimized_content = self._optimize_tool_content(content, source)
            self.tiers[tier].append(optimized_content)
            
            # Manage tier size
            max_tools = self.tier_config["tool_result_limit"]
            if len(self.tiers[tier]) > max_tools:
                self.tiers[tier].pop(0)
        
        elif tier == ContextTier.SUMMARIZED:
            # Historical content always summarized
            self.tiers[tier].append(content)
            # Keep only latest summary
            if len(self.tiers[tier]) > 1:
                self.tiers[tier].pop(0)
    
    def _optimize_tool_content(self, content: str, source: str) -> str:
        """Optimize tool content before adding to tier"""
        optimizer = AdvancedContextOptimizer(self.model_name)
        
        if "bash" in source.lower():
            return optimizer._optimize_bash_result(content)
        elif "file" in source.lower():
            return optimizer._optimize_file_result(content)
        else:
            return optimizer._basic_optimization(content)
    
    def _create_and_add_summary(self, content: str, target_tier: ContextTier):
        """Create summary and add to target tier"""
        summary = f"[Summary] {content[:200]}..." if len(content) > 200 else content
        self.tiers[target_tier.value].append(summary)
    
    def get_optimized_context_200k(self) -> List[str]:
        """Get context optimized for 200K token windows"""
        context_parts = []
        
        # Critical content (system prompt + current task)
        context_parts.extend(self.tiers['critical'])
        
        # Recent conversation (model-specific count)
        recent_count = self.tier_config["recent_preservation"]
        recent = self.tiers['recent'][-recent_count:] if len(self.tiers['recent']) > recent_count else self.tiers['recent']
        context_parts.extend(recent)
        
        # Tool results (optimized, limited)
        tool_results = self.tiers['tool_results']
        context_parts.extend(tool_results)
        
        # Historical content (latest summary only)
        if self.tiers['historical']:
            context_parts.append(self.tiers['historical'][-1])
        
        return context_parts


# Integration helper for existing agent.py
def integrate_200k_optimization(agent_instance):
    """Integrate 200K optimization with existing agent"""
    
    # Detect model
    model_name = "MiniMax-M2"  # Default
    if hasattr(agent_instance.llm, 'model'):
        model_str = str(agent_instance.llm.model).lower()
        if 'glm' in model_str:
            model_name = "GLM-4.6"
        elif 'minimax' in model_str:
            model_name = "MiniMax-M2"
    
    # Add optimization components
    agent_instance.token_budget = OptimizedTokenBudgetManager(model_name)
    agent_instance.context_optimizer = AdvancedContextOptimizer(model_name)
    agent_instance.context_tiers = ContextTierManager200K(model_name)
    
    # Add 200K-specific methods
    agent_instance._emergency_context_optimization_200k = lambda: _emergency_optimization_200k(agent_instance)
    agent_instance._optimize_tool_result_200k = lambda tool_name, content: agent_instance.context_optimizer.optimize_tool_result(tool_name, content)
    
    print(f"{Colors.BRIGHT_GREEN}[200K OPTIMIZE] Integrated {model_name} optimization with 200K context windows{Colors.RESET}")
    
    return agent_instance


def _emergency_optimization_200k(agent_instance):
    """Emergency context optimization for 200K limits"""
    print(f"{Colors.BRIGHT_YELLOW}[200K EMERGENCY] Applying emergency context optimization{Colors.RESET}")
    
    optimized_messages = []
    
    # Strategy 1: Keep system message
    if agent_instance.messages:
        optimized_messages.append(agent_instance.messages[0])
    
    # Strategy 2: Keep recent messages (more generous with 200K)
    recent_count = 6 if "glm" in str(agent_instance.llm.model).lower() else 8
    recent = agent_instance.messages[-recent_count:] if len(agent_instance.messages) > recent_count else agent_instance.messages[1:]
    optimized_messages.extend(recent)
    
    # Strategy 3: Optimize tool results
    tool_summaries = []
    for msg in agent_instance.messages:
        if msg.role == "tool":
            optimized_content = agent_instance.context_optimizer.optimize_tool_result(msg.name, msg.content)
            tool_summaries.append(f"{msg.name}: {optimized_content}")
    
    if tool_summaries:
        summary_msg = f"[Tool Results Summary]: {len(tool_summaries)} tools - {', '.join(tool_summaries[:3])}"
        optimized_messages.append(summary_msg)
    
    agent_instance.messages = optimized_messages
    print(f"{Colors.BRIGHT_GREEN}[200K EMERGENCY] Context optimized: {len(agent_instance.messages)} messages{Colors.RESET}")


# Example usage demonstration
if __name__ == "__main__":
    # Test the optimization system
    budget_manager = OptimizedTokenBudgetManager("MiniMax-M2")
    optimizer = AdvancedContextOptimizer("MiniMax-M2")
    tier_manager = ContextTierManager200K("MiniMax-M2")
    
    print(f"200K Token Budget Manager initialized for {budget_manager.strategy['name']}")
    print(f"Context limits: {budget_manager.max_tokens:,} tokens")
    print(f"Safe threshold: {budget_manager.safe_threshold:,} tokens")
    print(f"Optimization strategy: {budget_manager.strategy['optimization_level']}")
