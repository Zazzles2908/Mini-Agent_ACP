"""
Context Overflow Prevention System
===================================

This module implements concrete solutions to prevent the context overflow
that caused LLM API failures with 1M+ tokens in 80K token limit environment.
"""

import time
import logging
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ContextTier(Enum):
    """Context priority tiers for smart management"""
    CRITICAL = "critical"      # System prompt, current task
    RECENT = "recent"          # Last 5 messages
    SUMMARIZED = "summarized"  # Older messages (summarized)
    TOOL_RESULTS = "tool"      # Tool outputs (always summarized)


@dataclass
class ContextSegment:
    """Represents a chunk of context with metadata"""
    content: str
    tier: ContextTier
    tokens: int
    source: str
    timestamp: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TokenBudgetManager:
    """
    Enforces token budgets to prevent LLM context overflow
    """
    
    def __init__(self, max_tokens: int = 80000, warning_threshold: float = 0.8):
        self.max_tokens = max_tokens
        self.warning_threshold = warning_threshold
        self.current_tokens = 0
        self.interventions = 0
        self.token_history: List[Dict] = []
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation - 4 characters ≈ 1 token"""
        return max(1, len(text) // 4)
    
    def check_budget_before_llm(self, context: str) -> bool:
        """Check if next LLM call will exceed budget"""
        estimated_tokens = self.estimate_tokens(context)
        projected_total = self.current_tokens + estimated_tokens
        
        # Log token usage
        self.token_history.append({
            'timestamp': time.time(),
            'projected_tokens': projected_total,
            'available_tokens': self.max_tokens - projected_total,
            'utilization': projected_total / self.max_tokens
        })
        
        if projected_total > self.max_tokens:
            logger.error(f"Token budget exceeded: {projected_total}/{self.max_tokens}")
            return False
        elif projected_total > self.max_tokens * self.warning_threshold:
            logger.warning(f"Token warning: {projected_total}/{self.max_tokens} ({projected_total/self.max_tokens:.1%})")
        
        self.current_tokens = projected_total
        return True
    
    def update_actual_tokens(self, actual_tokens: int):
        """Update with actual LLM token count"""
        self.current_tokens = max(self.current_tokens, actual_tokens)
        
        if self.current_tokens > self.max_tokens:
            logger.warning(f"Actual usage exceeds estimated: {actual_tokens}")
    
    def reset_budget(self):
        """Reset token budget (for new sessions or tasks)"""
        self.current_tokens = 0
        self.interventions = 0
        logger.info("Token budget reset")


class BashOutputSummarizer:
    """
    Intelligent summarization for bash command outputs
    """
    
    @staticmethod
    def summarize_directory_listing(command: str, output: str) -> Dict[str, Any]:
        """Optimize Get-ChildItem directory listings"""
        lines = [l.strip() for l in output.split('\n') if l.strip()]
        
        # Count directories and files
        dirs = [l for l in lines if l.startswith('d---')]
        files = [l for l in lines if l.startswith('-a---')]
        
        # Extract directory names only (sample of first 10)
        dir_names = []
        for line in dirs[:10]:
            parts = line.split()
            if len(parts) > 0:
                dir_names.append(parts[-1])
        
        # Create intelligent summary
        summary = {
            'original_command': command,
            'command_summary': 'Directory structure analysis',
            'total_directories': len(dirs),
            'total_files': len(files),
            'sample_directories': dir_names,
            'overflow_note': f"... and {max(0, len(dirs) - 10)} more directories" if len(dirs) > 10 else "",
            'compressed_output': f"Found {len(dirs)} directories, {len(files)} files",
            'token_reduction': f"~{len(output)} chars → ~{len(str(summary))} chars"
        }
        
        logger.info(f"Bash summarization: {len(output)} chars → ~{len(str(summary))} chars")
        return summary
    
    @staticmethod
    def summarize_git_output(command: str, output: str) -> Dict[str, Any]:
        """Optimize git command outputs"""
        lines = [l.strip() for l in output.split('\n') if l.strip() and not l.startswith('#')]
        
        # Parse git status
        if 'status' in command.lower():
            modified = [l for l in lines if 'modified:' in l]
            added = [l for l in lines if 'new file:' in l]
            deleted = [l for l in lines if 'deleted:' in l]
            
            return {
                'original_command': command,
                'command_summary': 'Git status analysis',
                'modified_files': len(modified),
                'new_files': len(added),
                'deleted_files': len(deleted),
                'total_changes': len(modified) + len(added) + len(deleted),
                'compressed_output': f"Git: {len(modified)} modified, {len(added)} new, {len(deleted)} deleted"
            }
        
        # Generic git command
        return {
            'original_command': command,
            'command_summary': 'Git operation',
            'output_lines': len(lines),
            'compressed_output': f"Git operation completed ({len(lines)} lines)"
        }
    
    @staticmethod
    def summarize_generic_output(command: str, output: str, max_tokens: int = 200) -> Dict[str, Any]:
        """Generic bash output summarization"""
        lines = [l.strip() for l in output.split('\n') if l.strip()]
        compressed_lines = lines[:10]  # First 10 lines only
        
        return {
            'original_command': command,
            'command_summary': 'Command execution',
            'total_lines': len(lines),
            'compressed_lines': compressed_lines,
            'truncated_note': f"... and {max(0, len(lines) - 10)} more lines" if len(lines) > 10 else "",
            'compressed_output': f"Command completed: {len(lines)} lines output"
        }


class ContextTierManager:
    """
    Manages context in priority tiers for optimal token usage
    """
    
    def __init__(self, max_context_tokens: int = 80000):
        self.max_context_tokens = max_context_tokens
        self.tiers = {
            ContextTier.CRITICAL: [],
            ContextTier.RECENT: [],
            ContextTier.SUMMARIZED: [],
            ContextTier.TOOL_RESULTS: []
        }
        self.summarizer = BashOutputSummarizer()
    
    def add_context_segment(self, content: str, tier: ContextTier, source: str, metadata: Dict = None):
        """Add content to appropriate tier with token tracking"""
        
        # Estimate tokens upfront
        estimated_tokens = len(content) // 4
        segment = ContextSegment(
            content=content,
            tier=tier,
            tokens=estimated_tokens,
            source=source,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        # Route to appropriate tier
        if tier == ContextTier.CRITICAL:
            # Critical content replaces existing (system prompt, current task)
            self.tiers[tier] = [segment]
        
        elif tier == ContextTier.RECENT:
            # Recent conversation - keep last 5 items
            self.tiers[tier].append(segment)
            if len(self.tiers[tier]) > 5:
                self.tiers[tier].pop(0)
        
        elif tier == ContextTier.TOOL_RESULTS:
            # Tool results - always summarized and limited
            summarized_content = self._summarize_content(content, tier, source)
            summarized_segment = ContextSegment(
                content=summarized_content,
                tier=tier,
                tokens=len(summarized_content) // 4,
                source=source,
                timestamp=time.time(),
                metadata={'original_size': len(content), 'summarized': True}
            )
            self.tiers[tier].append(summarized_segment)
            
            # Keep only last 3 tool results to save space
            if len(self.tiers[tier]) > 3:
                self.tiers[tier].pop(0)
        
        elif tier == ContextTier.SUMMARIZED:
            # Historical content - always summarized
            self.tiers[tier].append(segment)
            # Keep only latest summary
            if len(self.tiers[tier]) > 1:
                self.tiers[tier].pop(0)
    
    def _summarize_content(self, content: str, tier: ContextTier, source: str) -> str:
        """Smart content summarization based on tier and source"""
        
        # Bash command optimization
        if 'bash' in source.lower():
            return self._summarize_bash_content(content, source)
        
        # File content optimization
        elif 'file' in source.lower():
            return self._summarize_file_content(content, source)
        
        # Generic content
        else:
            return self._summarize_generic_content(content, max_tokens=100)
    
    def _summarize_bash_content(self, content: str, source: str) -> str:
        """Summarize bash command outputs"""
        
        # Extract command and output from tool result format
        lines = content.split('\n')
        command_line = None
        output_lines = []
        
        for line in lines:
            if line.strip().startswith('Command:') or 'Get-ChildItem' in line:
                command_line = line
            elif line.strip() and not line.startswith('---'):
                output_lines.append(line)
        
        command = command_line or source
        output = '\n'.join(output_lines)
        
        # Apply intelligent summarization
        if 'Get-ChildItem' in command and '-Recurse' in command:
            return str(self.summarizer.summarize_directory_listing(command, output))
        elif 'git' in command.lower():
            return str(self.summarizer.summarize_git_output(command, output))
        else:
            return str(self.summarizer.summarize_generic_output(command, output))
    
    def _summarize_file_content(self, content: str, source: str) -> str:
        """Summarize file read operations"""
        if len(content) > 1000:
            # For large files, provide metadata only
            return f"File: {source} | Size: {len(content)} chars | Preview: {content[:200]}..."
        else:
            return f"File: {source} | Content: {content}"
    
    def _summarize_generic_content(self, content: str, max_tokens: int = 100) -> str:
        """Generic content summarization"""
        if len(content) > max_tokens * 4:  # Rough token estimate
            return content[:max_tokens * 4] + "..."  # Truncate with ellipsis
        return content
    
    def get_optimized_context(self) -> str:
        """Compose context within token limits"""
        context_parts = []
        total_tokens = 0
        
        # Always include critical content
        for segment in self.tiers[ContextTier.CRITICAL]:
            if total_tokens + segment.tokens < self.max_context_tokens * 0.6:  # 60% for critical
                context_parts.append(segment.content)
                total_tokens += segment.tokens
        
        # Add recent conversation (last 3 items)
        for segment in self.tiers[ContextTier.RECENT][-3:]:
            if total_tokens + segment.tokens < self.max_context_tokens * 0.85:  # 85% total for recent
                context_parts.append(segment.content)
                total_tokens += segment.tokens
        
        # Add summarized historical content
        if self.tiers[ContextTier.SUMMARIZED]:
            latest_summary = self.tiers[ContextTier.SUMMARIZED][-1]
            if total_tokens + latest_summary.tokens < self.max_context_tokens * 0.95:  # 95% total
                context_parts.append(f"[Historical Summary] {latest_summary.content}")
                total_tokens += latest_summary.tokens
        
        # Add tool result summaries (most compact)
        for segment in self.tiers[ContextTier.TOOL_RESULTS]:
            if total_tokens + segment.tokens < self.max_context_tokens:
                context_parts.append(f"[Tool] {segment.content}")
                total_tokens += segment.tokens
            else:
                break  # Stop if we're approaching limit
        
        logger.info(f"Context optimization: {total_tokens} tokens ({total_tokens/self.max_context_tokens:.1%} of limit)")
        return '\n\n'.join(context_parts)
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get current context state for monitoring"""
        tier_counts = {tier.value: len(segments) for tier, segments in self.tiers.items()}
        total_segments = sum(tier_counts.values())
        
        return {
            'total_segments': total_segments,
            'tier_breakdown': tier_counts,
            'estimated_tokens': self._estimate_total_tokens(),
            'optimization_ratio': self._estimate_total_tokens() / self.max_context_tokens
        }
    
    def _estimate_total_tokens(self) -> int:
        """Estimate total tokens across all tiers"""
        return sum(segment.tokens for segments in self.tiers.values() for segment in segments)


class ContextRecoverySystem:
    """
    Emergency context reduction when overflow is detected
    """
    
    def __init__(self, max_tokens: int = 80000):
        self.max_tokens = max_tokens
        self.recovery_strategies = [
            self._remove_verbose_tool_outputs,
            self._reduce_conversation_history,
            self._compress_system_context,
            self._emergency_minimal_context
        ]
    
    def handle_overflow(self, context: str) -> str:
        """Progressive context reduction with recovery strategies"""
        
        logger.warning(f"Context overflow detected. Current context: ~{len(context)} chars")
        
        for i, strategy in enumerate(self.recovery_strategies, 1):
            try:
                reduced_context = strategy(context)
                estimated_tokens = len(reduced_context) // 4
                
                if estimated_tokens < self.max_tokens:
                    logger.info(f"Recovery successful with strategy {i}: {strategy.__name__}")
                    logger.info(f"Context reduced: ~{len(context)} → ~{len(reduced_context)} chars")
                    return reduced_context
                    
            except Exception as e:
                logger.warning(f"Recovery strategy {i} ({strategy.__name__}) failed: {e}")
        
        # Final emergency fallback
        logger.warning("All recovery strategies failed, using emergency minimal context")
        return self._emergency_minimal_context(context)
    
    def _remove_verbose_tool_outputs(self, context: str) -> str:
        """Remove verbose tool outputs, keep summaries only"""
        lines = context.split('\n')
        cleaned_lines = []
        skip_section = False
        
        for line in lines:
            # Detect tool output markers
            if '---bash output---' in line or '---file content---' in line:
                skip_section = True
                cleaned_lines.append("[Tool output summarized]")
                continue
            elif '---end tool output---' in line:
                skip_section = False
                continue
            
            if not skip_section:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _reduce_conversation_history(self, context: str) -> str:
        """Keep only recent conversation highlights"""
        lines = context.split('\n')
        essential_lines = []
        
        for line in lines:
            # Keep system prompts and recent user messages
            if (line.startswith('System:') or 
                line.startswith('User:') or 
                line.startswith('Assistant:')):
                essential_lines.append(line)
                
                # Stop after collecting a few recent messages
                if len([l for l in essential_lines if l.startswith('User:')]) >= 3:
                    break
        
        return '\n'.join(essential_lines)
    
    def _compress_system_context(self, context: str) -> str:
        """Compress system-level context"""
        lines = context.split('\n')
        compressed_lines = []
        
        for line in lines:
            if line.startswith('System:'):
                # Keep only essential system info
                if any(keyword in line for keyword in ['role', 'primary', 'context']):
                    compressed_lines.append(line)
            else:
                compressed_lines.append(line)
        
        return '\n'.join(compressed_lines)
    
    def _emergency_minimal_context(self, context: str) -> str:
        """Emergency mode: absolute minimum context for basic functionality"""
        lines = context.split('\n')
        minimal_lines = []
        
        # Keep only the last few messages
        message_count = 0
        for line in reversed(lines):
            if line.strip() and (line.startswith('User:') or line.startswith('Assistant:')):
                minimal_lines.insert(0, line)
                message_count += 1
                if message_count >= 2:  # Just last exchange
                    break
        
        # Add minimal system context if available
        for line in lines:
            if line.startswith('System:') and 'role' in line.lower():
                minimal_lines.insert(0, line)
                break
        
        logger.warning(f"Emergency context: {len(minimal_lines)} lines")
        return '\n'.join(minimal_lines)


# Integration functions for existing system
def create_context_overflow_protection():
    """Create complete context overflow protection system"""
    return {
        'token_budget': TokenBudgetManager(),
        'tier_manager': ContextTierManager(),
        'recovery_system': ContextRecoverySystem(),
        'summarizer': BashOutputSummarizer()
    }


def optimize_bash_command_result(command: str, output: str) -> Dict[str, Any]:
    """Standalone function to optimize bash command results"""
    summarizer = BashOutputSummarizer()
    
    if 'Get-ChildItem' in command and '-Recurse' in command:
        return summarizer.summarize_directory_listing(command, output)
    elif 'git' in command.lower():
        return summarizer.summarize_git_output(command, output)
    else:
        return summarizer.summarize_generic_output(command, output)


# Example usage patterns
if __name__ == "__main__":
    # Initialize protection system
    protection = create_context_overflow_protection()
    
    # Example: Optimize a bash command result
    command = "Get-ChildItem -Path . -Recurse"
    output = "Directory: C:\\Users\\Jazeel-Home\\Mini-Agent\n\nd----- 18/11/2025 8:29 AM .venv\nd----- 21/11/2025 11:00 PM .vscode\nd----- 22/11/2025 8:00 PM docs\n[... hundreds more lines ...]"
    
    optimized_result = optimize_bash_command_result(command, output)
    print("Original size:", len(output))
    print("Optimized result:", optimized_result)
    
    # Example: Add content to tier manager
    protection['tier_manager'].add_context_segment(
        content="User: List files in current directory",
        tier=ContextTier.RECENT,
        source="conversation"
    )
    
    # Get optimized context for LLM
    optimized_context = protection['tier_manager'].get_optimized_context()
    print("Optimized context size:", len(optimized_context), "chars")
    
    # Check token budget
    can_proceed = protection['token_budget'].check_budget_before_llm(optimized_context)
    print("Can proceed with LLM call:", can_proceed)
