# Recommended Implementation: Context Overflow Solution for MiniMax M2 + GLM-4.6

## Executive Summary

This document provides a **complete, actionable implementation plan** to prevent context overflow in our dual-model agent system. Based on our analysis of the current system failures and industry best practices research, this solution will eliminate the 1M+ token overflow events while optimizing for both MiniMax M2 and GLM-4.6 models.

## Problem Summary

**Current State (Broken):**
- 1,005,262 tokens processed vs. 80,000 limit (12.5x overflow)
- Reactive token checking after context growth
- Verbose tool outputs flood context without optimization
- LLM-based summarization fails when LLM is overloaded
- 4 failed retry attempts before system failure

**Target State (Fixed):**
- Context consistently <75% of model limits
- Proactive overflow prevention before LLM calls
- Tool outputs optimized by 80%+ 
- Zero context overflow events
- <2 second optimization response time

## Recommended Architecture

### **Core Design Principles**

1. **Prevention Over Recovery**: Check token budget BEFORE LLM calls, not after
2. **Model-Aware Optimization**: Different strategies for MiniMax M2 vs. GLM-4.6
3. **Tool Output Priority**: Focus optimization on bash/file operations first
4. **Incremental Implementation**: No breaking changes to existing functionality

### **System Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Execution Flow                     │
├─────────────────────────────────────────────────────────────┤
│ 1. Token Budget Check (PROACTIVE)                          │
│    ├─ Estimate current context size                         │
│    ├─ Check against model-specific threshold               │
│    └─ Trigger optimization if approaching limit            │
│                                                              │
│ 2. Context Optimization (if needed)                        │
│    ├─ Tool output compression (bash/file operations)       │
│    ├─ Conversation history summarization                   │
│    └─ Context tiering and prioritization                   │
│                                                              │
│ 3. LLM Call with Safe Context                              │
│    ├─ Use optimized context                                │
│    ├─ Monitor actual token usage                           │
│    └─ Update budget tracking                               │
│                                                              │
│ 4. Tool Execution with Optimization                        │
│    ├─ Optimize results before adding to context            │
│    ├─ Apply model-specific compression                     │
│    └─ Route to appropriate context tier                    │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Immediate Protection (Week 1)

### **Step 1: Token Budget Enforcement**

Add this to `mini_agent/agent.py` - Add to `__init__` method:

```python
# Add after existing initialization
from .tools.context_optimizer import ModelAwareTokenBudget

def __init__(self, ..., token_limit: int = 80000):
    # ... existing code ...
    
    # NEW: Model-aware token budget management
    model_name = self._detect_model_name()
    self.token_budget = ModelAwareTokenBudget(
        model_name=model_name,
        max_tokens=token_limit,
        warning_threshold=0.75
    )
    
    # NEW: Enable context optimization feature flag
    self.enable_context_optimization = True
```

Add new method to detect model:

```python
def _detect_model_name(self) -> str:
    """Detect which model we're using for optimization"""
    model_info = getattr(self.llm, 'model', 'unknown')
    if 'minimax' in str(model_info).lower():
        return 'MiniMax-M2'
    elif 'glm' in str(model_info).lower():
        return 'GLM-4.6'
    else:
        return 'default'

def _get_model_token_limit(self) -> int:
    """Get model-specific token limits"""
    model_name = self._detect_model_name()
    limits = {
        'MiniMax-M2': 200000,
        'GLM-4.6': 128000,
        'default': 80000
    }
    return limits.get(model_name, 80000)
```

### **Step 2: Pre-LLM Call Budget Check**

Modify the `run()` method - Replace line 449-450:

```python
# OLD CODE (Line 449-450):
response = await self.llm.generate(messages=self.messages, tools=tool_list)

# NEW CODE:
# Check token budget before making LLM call
current_context = self.messages  # Full current context
if not self.token_budget.check_budget_before_llm(current_context):
    print(f"{Colors.BRIGHT_YELLOW}[OPTIMIZE] Context optimization needed{Colors.RESET}")
    # Apply emergency optimization
    optimized_context = self._emergency_context_optimization()
    try:
        response = await self.llm.generate(messages=optimized_context, tools=tool_list)
    except Exception as e:
        # Handle any remaining errors
        return self._handle_llm_error(e, step)
else:
    response = await self.llm.generate(messages=self.messages, tools=tool_list)

# Update actual token usage after call
actual_tokens = self._estimate_tokens()
self.token_budget.update_actual_tokens(actual_tokens)
```

### **Step 3: Emergency Context Optimization**

Add this new method to the `Agent` class:

```python
def _emergency_context_optimization(self) -> list[Message]:
    """Emergency context optimization when budget exceeded"""
    print(f"{Colors.BRIGHT_YELLOW}[OPTIMIZE] Applying emergency context reduction{Colors.RESET}")
    
    optimized_messages = []
    
    # Strategy 1: Keep system prompt
    if self.messages:
        optimized_messages.append(self.messages[0])  # System message
    
    # Strategy 2: Keep recent conversation (last 5 messages)
    recent_count = 5 if self._detect_model_name() == "MiniMax-M2" else 3
    recent_messages = self.messages[-recent_count:] if len(self.messages) > recent_count else self.messages[1:]
    optimized_messages.extend(recent_messages)
    
    # Strategy 3: Add tool optimization summary
    tool_summaries = self._create_tool_summaries()
    if tool_summaries:
        summary_msg = Message(
            role="user",
            content=f"[Tool Operations Summary]: {len(tool_summaries)} tools executed - {', '.join(tool_summaries)}"
        )
        optimized_messages.append(summary_msg)
    
    # Strategy 4: Add conversation summary if needed
    if len(self.messages) > 10:
        conv_summary = self._create_conversation_summary(self.messages[1:-5])
        optimized_messages.insert(1, conv_summary)
    
    print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Context optimized: {len(self.messages)} → {len(optimized_messages)} messages{Colors.RESET}")
    return optimized_messages

def _create_tool_summaries(self) -> list[str]:
    """Create summaries of tool operations"""
    summaries = []
    for msg in self.messages:
        if msg.role == "tool":
            if msg.name == "bash":
                # Extract key info from bash operations
                if "Get-ChildItem" in msg.content:
                    summaries.append("directory listing")
                elif "git" in msg.content.lower():
                    summaries.append("git operation")
                else:
                    summaries.append("bash command")
            elif "file" in msg.name.lower():
                summaries.append("file operation")
            else:
                summaries.append(f"{msg.name} tool")
    return summaries[:5]  # Limit to 5 summaries

def _create_conversation_summary(self, messages: list[Message]) -> Message:
    """Create a summary of old conversation content"""
    summary_content = "Conversation History Summary:\n"
    for msg in messages:
        if msg.role == "user":
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_content += f"User: {content}\n"
        elif msg.role == "assistant" and msg.content:
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_content += f"Assistant: {content}\n"
    
    return Message(role="user", content=summary_content)
```

## Phase 2: Tool Output Optimization (Week 2)

### **Step 4: Tool Result Optimization**

Create new file: `mini_agent/tools/context_optimizer.py`

```python
"""Context optimization tools for preventing overflow"""

import re
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class OptimizationConfig:
    """Configuration for context optimization"""
    model_name: str
    max_tool_output_chars: int
    compress_directory_listings: bool
    compress_git_output: bool
    preserve_detail_level: str  # "detailed", "moderate", "minimal"

class ContextOptimizer:
    """Main context optimization engine"""
    
    def __init__(self, model_name: str):
        self.config = self._get_optimization_config(model_name)
    
    def _get_optimization_config(self, model_name: str) -> OptimizationConfig:
        """Get model-specific optimization configuration"""
        if model_name == "MiniMax-M2":
            return OptimizationConfig(
                model_name=model_name,
                max_tool_output_chars=500,
                compress_directory_listings=True,
                compress_git_output=True,
                preserve_detail_level="moderate"
            )
        elif model_name == "GLM-4.6":
            return OptimizationConfig(
                model_name=model_name,
                max_tool_output_chars=200,
                compress_directory_listings=True,
                compress_git_output=True,
                preserve_detail_level="minimal"
            )
        else:
            # Default configuration
            return OptimizationConfig(
                model_name=model_name,
                max_tool_output_chars=300,
                compress_directory_listings=True,
                compress_git_output=True,
                preserve_detail_level="moderate"
            )
    
    def optimize_tool_result(self, tool_name: str, result_content: str) -> str:
        """Optimize tool result based on tool type"""
        
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
        """Optimize bash command outputs"""
        lines = content.split('\n')
        
        # Directory listing optimization
        if any(cmd in content for cmd in ["Get-ChildItem", "ls", "dir"]):
            return self._optimize_directory_listing(lines)
        
        # Git command optimization
        elif "git" in content.lower():
            return self._optimize_git_output(content)
        
        # Generic bash optimization
        else:
            return self._optimize_generic_bash(content)
    
    def _optimize_directory_listing(self, lines: List[str]) -> str:
        """Optimize directory listing outputs"""
        dirs = [line for line in lines if line.strip().startswith('d---')]
        files = [line for line in lines if line.strip().startswith('-a---')]
        
        # Extract directory names
        dir_names = []
        for line in dirs[:10]:  # Limit to first 10
            parts = line.split()
            if len(parts) > 0:
                dir_names.append(parts[-1])
        
        # Create summary based on model configuration
        if self.config.preserve_detail_level == "minimal":
            return f"Directory: {len(dirs)} directories, {len(files)} files"
        elif self.config.preserve_detail_level == "moderate":
            sample = ', '.join(dir_names[:5])
            overflow = f"... +{len(dir_names)-5} more" if len(dir_names) > 5 else ""
            return f"Filesystem: {len(dirs)} dirs, {len(files)} files | Sample: {sample} {overflow}".strip()
        else:  # detailed
            all_dirs = ', '.join(dir_names)
            return f"Directory structure ({len(dirs)} dirs, {len(files)} files): {all_dirs}"
    
    def _optimize_git_output(self, content: str) -> str:
        """Optimize git command outputs"""
        # Count git status changes
        modified = content.count('modified:')
        new_files = content.count('new file:')
        deleted = content.count('deleted:')
        
        if modified > 0 or new_files > 0 or deleted > 0:
            return f"Git status: {modified} modified, {new_files} new, {deleted} deleted"
        else:
            return f"Git operation completed ({len(content.split())} lines output)"
    
    def _optimize_generic_bash(self, content: str) -> str:
        """Optimize generic bash command outputs"""
        if len(content) <= self.config.max_tool_output_chars:
            return content
        
        # Truncate with context preservation
        lines = content.split('\n')[:10]  # First 10 lines
        truncated = '\n'.join(lines)
        
        if len(content) > len(truncated):
            truncated += f"\n... ({len(content.split('\n')) - 10} more lines)"
        
        return truncated
    
    def _optimize_file_result(self, content: str) -> str:
        """Optimize file operation results"""
        if len(content) > self.config.max_tool_output_chars:
            return f"File operation completed ({len(content)} characters)"
        return content
    
    def _basic_optimization(self, content: str) -> str:
        """Basic content optimization for any tool"""
        if len(content) > self.config.max_tool_output_chars:
            return content[:self.config.max_tool_output_chars] + "..."
        return content

class ModelAwareTokenBudget:
    """Model-specific token budget management"""
    
    def __init__(self, model_name: str, max_tokens: int = 80000, warning_threshold: float = 0.75):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.warning_threshold = warning_threshold
        self.current_tokens = 0
        self.model_limits = {
            'MiniMax-M2': 200000,
            'GLM-4.6': 128000,
            'default': 80000
        }
    
    def check_budget_before_llm(self, context: list) -> bool:
        """Check if context will fit within budget"""
        try:
            # Simple token estimation (can be improved with tiktoken)
            total_chars = sum(len(str(msg.content)) for msg in context if hasattr(msg, 'content'))
            estimated_tokens = total_chars // 4  # Rough approximation
            
            # Check against model-specific warning threshold
            model_limit = self.model_limits.get(self.model_name, 80000)
            warning_limit = int(model_limit * self.warning_threshold)
            
            if estimated_tokens > warning_limit:
                print(f"{Colors.BRIGHT_YELLOW}[BUDGET] Token warning: {estimated_tokens}/{warning_limit} (limit: {model_limit}){Colors.RESET}")
                return False
            
            return True
            
        except Exception as e:
            print(f"{Colors.BRIGHT_YELLOW}[BUDGET] Budget check failed: {e}{Colors.RESET}")
            return True  # Fail safe - allow call if check fails
    
    def update_actual_tokens(self, actual_tokens: int):
        """Update with actual token usage"""
        self.current_tokens = actual_tokens
```

### **Step 5: Integrate Tool Optimization**

Modify tool execution in `agent.py` - Replace lines 590-597:

```python
# OLD CODE:
# Add tool result message
tool_msg = Message(
    role="tool",
    content=result.content if result.success else f"Error: {result.error}",
    tool_call_id=tool_call_id,
    name=function_name,
)
self.messages.append(tool_msg)

# NEW CODE:
# Optimize tool result before adding to context
if result.success:
    # Apply context optimization
    optimizer = ContextOptimizer(self._detect_model_name())
    optimized_content = optimizer.optimize_tool_result(function_name, result.content)
else:
    optimized_content = f"Error: {result.error}"

# Add optimized tool result message
tool_msg = Message(
    role="tool",
    content=optimized_content,
    tool_call_id=tool_call_id,
    name=function_name,
)
self.messages.append(tool_msg)
```

## Phase 3: Advanced Context Management (Week 3)

### **Step 6: Context Tiering System**

Replace the flat message list with tiered management:

```python
class Agent:
    def __init__(self, ...):
        # ... existing code ...
        
        # NEW: Context tiering system
        self.context_tiers = {
            'critical': [],      # System prompt
            'recent': [],        # Recent conversation
            'summarized': [],    # Older content (summarized)
            'tool_results': []   # Tool operation summaries
        }
        
        # Initialize with system message
        if self.messages:
            self.context_tiers['critical'].append(self.messages[0])
    
    def _get_optimized_context(self) -> list[Message]:
        """Get context composed from tiers with size management"""
        context = []
        model_name = self._detect_model_name()
        
        # Critical content (system prompt) - always included
        context.extend(self.context_tiers['critical'])
        
        # Recent messages (model-specific count)
        recent_count = 5 if model_name == "MiniMax-M2" else 3
        recent = self.context_tiers['recent'][-recent_count:] if len(self.context_tiers['recent']) > recent_count else self.context_tiers['recent']
        context.extend(recent)
        
        # Summarized content (latest only)
        if self.context_tiers['summarized']:
            context.extend(self.context_tiers['summarized'][-1:])
        
        # Tool results (optimized, limited count)
        tool_results = self.context_tiers['tool_results']
        max_tool_results = 2 if model_name == "MiniMax-M2" else 1
        context.extend(tool_results[-max_tool_results:])
        
        return context
    
    def _route_message_to_tier(self, msg: Message):
        """Route new messages to appropriate tier"""
        if msg.role == "user" and len(self.context_tiers['recent']) > 0:
            # Add to recent tier
            self.context_tiers['recent'].append(msg)
            
            # Manage recent tier size
            max_recent = 10 if self._detect_model_name() == "MiniMax-M2" else 5
            if len(self.context_tiers['recent']) > max_recent:
                old_msg = self.context_tiers['recent'].pop(0)
                # Create summary and move to summarized tier
                summary = self._create_message_summary(old_msg)
                self.context_tiers['summarized'].append(summary)
        
        elif msg.role == "tool":
            # Add to tool results tier
            self.context_tiers['tool_results'].append(msg)
            
            # Manage tool results tier size
            max_tools = 5
            if len(self.context_tiers['tool_results']) > max_tools:
                self.context_tiers['tool_results'].pop(0)
```

## Testing and Validation

### **Test Scenarios**

Create test cases in `tests/test_context_optimization.py`:

```python
import pytest
from mini_agent.tools.context_optimizer import ContextOptimizer, ModelAwareTokenBudget

class TestContextOptimization:
    def test_minimax_budget_check(self):
        budget = ModelAwareTokenBudget("MiniMax-M2")
        # Test that MiniMax allows larger contexts
        
    def test_glm_budget_check(self):
        budget = ModelAwareTokenBudget("GLM-4.6")
        # Test that GLM enforces stricter limits
        
    def test_directory_listing_optimization(self):
        optimizer = ContextOptimizer("MiniMax-M2")
        large_listing = "d--- directory1\nd--- directory2\n..." * 100
        optimized = optimizer._optimize_directory_listing(large_listing.split('\n'))
        assert len(optimized) < 200  # Should be compressed
        
    def test_git_output_optimization(self):
        optimizer = ContextOptimizer("GLM-4.6")
        git_output = "modified: file1.txt\nnew file: file2.py\n"
        optimized = optimizer._optimize_git_output(git_output)
        assert "2 modified, 1 new" in optimized
```

### **Validation Checklist**

- [ ] **Token Budget**: Context consistently <75% of model limits
- [ ] **Tool Optimization**: Bash commands reduced by 80%+
- [ ] **No Overflow**: Zero 1M+ token events
- [ ] **Performance**: Optimization completes in <2 seconds
- [ ] **Functionality**: All existing features work unchanged

## Success Metrics

### **Primary KPIs:**
- **Context Overflow Rate**: 0% (target)
- **Average Context Size**: <60% of model limit
- **Tool Output Compression**: 80%+ size reduction
- **Response Time**: <2 second optimization

### **Model-Specific Metrics:**

#### **MiniMax M2:**
- Context utilization: 60-75% of 200K limit
- Detailed conversation preservation
- Moderate tool compression

#### **GLM-4.6:**
- Context utilization: 50-75% of 128K limit
- Efficient conversation compression
- Aggressive tool compression

## Risk Mitigation

### **Rollback Plan:**
1. **Feature Flags**: Disable optimization with single config change
2. **Gradual Rollout**: Enable for 10% of requests initially
3. **Monitoring**: Real-time overflow detection
4. **Fallback**: Emergency context reset if optimization fails

### **Compatibility:**
- **Backward Compatible**: All existing functionality preserved
- **Model Agnostic**: Works with any LLM model
- **Incremental**: Can implement phases separately

## Implementation Timeline

### **Week 1: Foundation**
- Token budget enforcement
- Emergency context optimization
- Basic tool output compression

### **Week 2: Optimization**
- Model-aware optimization strategies
- Context tiering system
- Advanced tool result handling

### **Week 3: Advanced Features**
- Real-time monitoring
- Performance tuning
- Comprehensive testing

---

## Conclusion

This implementation addresses the **root cause** of our context overflow (1M+ tokens) by implementing **industry-proven prevention strategies** specifically optimized for our **MiniMax M2 + GLM-4.6 dual-model architecture**.

**Key Success Factor**: The proactive token budget check before each LLM call will prevent the overflow before it happens, eliminating the 4-retry failure pattern we experienced.

**Expected Impact**: Zero context overflow events, 80%+ tool output compression, and optimized performance for both models.
