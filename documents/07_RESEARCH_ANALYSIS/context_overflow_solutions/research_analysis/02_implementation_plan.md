# Context Overflow Prevention - Implementation Plan

## Priority 1: Immediate Protection (Implement First)

### 1.1 Token Budget Enforcement System

Add this to the main execution loop to prevent overflow:

```python
# In main execution engine
class TokenBudgetManager:
    def __init__(self, max_tokens=80000, warning_threshold=0.8):
        self.max_tokens = max_tokens
        self.warning_threshold = warning_threshold
        self.current_tokens = 0
        self.interventions = 0
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars = 1 token)"""
        return len(text) // 4
    
    def check_budget_before_llm(self, prompt: str) -> bool:
        """Check if next LLM call will exceed budget"""
        estimated_tokens = self.estimate_tokens(prompt)
        projected_total = self.current_tokens + estimated_tokens
        
        if projected_total > self.max_tokens:
            self.intervene_before_overflow()
            return False
        elif projected_total > self.max_tokens * self.warning_threshold:
            logger.warning(f"Token warning: {projected_total}/{self.max_tokens}")
        
        return True
    
    def intervene_before_overflow(self):
        """Emergency context reduction before overflow"""
        self.interventions += 1
        
        # Strategy 1: Remove verbose tool outputs
        self.summarize_recent_tool_outputs()
        
        # Strategy 2: Reduce conversation history  
        self.truncate_conversation_history()
        
        # Strategy 3: Compress system context
        self.optimize_system_context()
        
        logger.info(f"Context intervention #{self.interventions} completed")
```

### 1.2 Smart Tool Output Summarization

Replace verbose bash outputs with intelligent summaries:

```python
# Enhanced bash tool with automatic summarization
class OptimizedBashTool:
    def __init__(self):
        self.summarizer = BashOutputSummarizer()
    
    def execute(self, command: str, **kwargs):
        result = self._execute_bash(command, **kwargs)
        
        # Apply smart summarization based on command type
        if 'Get-ChildItem' in command and '-Recurse' in command:
            return self.summarizer.summarize_directory_listing(command, result.output)
        elif 'git' in command.lower():
            return self.summarizer.summarize_git_output(command, result.output)
        else:
            return self.summarizer.summarize_generic_output(command, result.output)

class BashOutputSummarizer:
    def summarize_directory_listing(self, command, output):
        lines = [l for l in output.split('\n') if l.strip()]
        
        # Count directories and files
        dirs = [l for l in lines if l.startswith('d---')]
        files = [l for l in lines if l.startswith('-a---')]
        
        # Extract only directory names (first 10)
        dir_names = [l.split()[-1] for l in dirs[:10]]
        
        summary = {
            'command': command,
            'summary': f"Directory structure: {len(dirs)} directories, {len(files)} files",
            'sample_directories': dir_names,
            'total_counts': f"{len(dirs)} dirs, {len(files)} files",
            'note': f"{'...' if len(dirs) > 10 else ''}"
        }
        
        return summary  # Much smaller than full listing
    
    def summarize_git_output(self, command, output):
        # Extract key information from git commands
        if 'status' in command.lower():
            lines = [l for l in output.split('\n') if l.strip() and not l.startswith('#')]
            modified = [l for l in lines if 'modified:' in l]
            added = [l for l in lines if 'new file:' in l]
            
            return {
                'command': command,
                'modified_files': len(modified),
                'new_files': len(added),
                'summary': f"Git status: {len(modified)} modified, {len(added)} new files"
            }
        
        # Generic git command summary
        return {
            'command': command,
            'output_lines': len(output.split('\n')),
            'summary': f"Git operation completed ({len(output.split('\n'))} lines output)"
        }
```

### 1.3 Context Tiering System

Separate critical vs. non-critical context:

```python
class ContextTierManager:
    def __init__(self):
        self.tiers = {
            'critical': [],    # System prompt, current task
            'recent': [],      # Last 5-10 messages
            'summarized': [],  # Older messages (summarized)
            'tool_results': [] # Tool outputs (summarized)
        }
    
    def add_content(self, content: str, tier: str, metadata: dict = None):
        """Add content to appropriate tier"""
        
        # Tier 1: Critical content (system prompt, current task)
        if tier == 'critical':
            self.tiers['critical'] = [content]
        
        # Tier 2: Recent conversation (last 10 messages)
        elif tier == 'recent':
            self.tiers['recent'].append({
                'content': content,
                'metadata': metadata or {}
            })
            # Keep only last 10
            if len(self.tiers['recent']) > 10:
                self.tiers['recent'].pop(0)
        
        # Tier 3: Tool results (always summarized)
        elif tier == 'tool_results':
            if len(content) > 500:  # Summarize large tool outputs
                summary = self._summarize_content(content, max_tokens=100)
                self.tiers['tool_results'].append(summary)
            else:
                self.tiers['tool_results'].append(content)
            
            # Keep only last 5 tool results
            if len(self.tiers['tool_results']) > 5:
                self.tiers['tool_results'].pop(0)
    
    def get_llm_context(self) -> str:
        """Compose optimized context for LLM"""
        context_parts = []
        
        # Always include critical content
        context_parts.extend(self.tiers['critical'])
        
        # Recent messages (full content)
        context_parts.extend([item['content'] for item in self.tiers['recent'][-5:]])
        
        # Summarized historical content
        if self.tiers['summarized']:
            context_parts.append(self.tiers['summarized'][-1])  # Latest summary
        
        # Summarized tool results only
        context_parts.extend(self.tiers['tool_results'])
        
        return '\n\n'.join(context_parts)
```

## Priority 2: Recovery Mechanisms (Implement Second)

### 2.1 Emergency Context Reduction

```python
class ContextRecoverySystem:
    def __init__(self, max_tokens=80000):
        self.max_tokens = max_tokens
        self.recovery_strategies = [
            self._remove_verbose_tool_outputs,
            self._reduce_conversation_history,
            self._compress_system_context,
            self._emergency_reset
        ]
    
    def handle_overflow(self, current_context: str) -> str:
        """Progressive context reduction strategies"""
        
        for strategy in self.recovery_strategies:
            try:
                reduced = strategy(current_context)
                
                if self._estimate_tokens(reduced) < self.max_tokens:
                    logger.info(f"Recovery successful using {strategy.__name__}")
                    return reduced
                    
            except Exception as e:
                logger.warning(f"Recovery strategy {strategy.__name__} failed: {e}")
        
        # Final fallback
        return self._emergency_reset(current_context)
    
    def _remove_verbose_tool_outputs(self, context: str):
        """Remove detailed tool outputs, keep summaries"""
        lines = context.split('\n')
        cleaned_lines = []
        in_tool_output = False
        
        for line in lines:
            # Detect tool output sections
            if '---bash output---' in line or '---file content---' in line:
                in_tool_output = True
                continue
            elif '---end tool output---' in line:
                in_tool_output = False
                continue
            
            if not in_tool_output:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _reduce_conversation_history(self, context: str):
        """Keep only essential conversation elements"""
        # This would parse conversation structure and keep only recent/highlight messages
        return context  # Simplified implementation
    
    def _emergency_reset(self, context: str) -> str:
        """Emergency mode: minimal context for basic functionality"""
        # Keep only system prompt and last user message
        lines = context.split('\n')
        essential_lines = []
        
        for line in lines:
            if line.startswith('System:') or line.startswith('User:'):
                essential_lines.append(line)
                if len(essential_lines) > 3:  # System + last 2 user messages
                    break
        
        return '\n'.join(essential_lines)
```

### 2.2 Proactive Summarization

```python
class ProactiveSummarizer:
    def __init__(self, token_threshold=50000):
        self.token_threshold = token_threshold
        self.last_summary_token_count = 0
    
    def should_summarize(self, current_tokens: int) -> bool:
        """Determine if proactive summarization is needed"""
        
        # Token-based trigger
        if current_tokens > self.token_threshold:
            return True
        
        # Only summarize if we've added significant new content
        if current_tokens - self.last_summary_token_count > 10000:
            return True
        
        return False
    
    def create_smart_summary(self, context_segments: List[dict]) -> str:
        """Create intelligent summaries based on content type"""
        
        # Group content by type
        tool_outputs = [s for s in context_segments if s.get('type') == 'tool_output']
        conversations = [s for s in context_segments if s.get('type') == 'conversation']
        file_operations = [s for s in context_segments if s.get('type') == 'file_operation']
        
        summary_parts = []
        
        # Summarize tool operations
        if tool_outputs:
            tool_summary = self._summarize_tool_operations(tool_outputs)
            summary_parts.append(f"Tool Operations: {tool_summary}")
        
        # Summarize conversation flow
        if conversations:
            conv_summary = self._summarize_conversations(conversations)
            summary_parts.append(f"Conversation: {conv_summary}")
        
        # Summarize file operations
        if file_operations:
            file_summary = self._summarize_file_operations(file_operations)
            summary_parts.append(f"File Operations: {file_summary}")
        
        return " | ".join(summary_parts)
    
    def _summarize_tool_operations(self, operations: List[dict]) -> str:
        """Summarize multiple tool operations"""
        bash_count = sum(1 for op in operations if op.get('tool') == 'bash')
        file_count = sum(1 for op in operations if op.get('tool') in ['read', 'write', 'edit'])
        
        return f"{bash_count} bash commands, {file_count} file operations"
    
    def _summarize_conversations(self, conversations: List[dict]) -> str:
        """Summarize conversation topics"""
        topics = [conv.get('topic', 'general') for conv in conversations]
        unique_topics = list(set(topics))
        
        return f"Discussion topics: {', '.join(unique_topics)}"
```

## Implementation Steps

### Step 1: Token Budget Enforcement (Day 1)
1. Add `TokenBudgetManager` class to main execution
2. Integrate token checking before each LLM call
3. Add basic context reduction triggers

### Step 2: Tool Output Optimization (Day 2)
1. Replace verbose bash tool with `OptimizedBashTool`
2. Implement command-specific summarization
3. Add file operation optimization

### Step 3: Context Tiering (Day 3)
1. Implement `ContextTierManager`
2. Update content routing to use tiers
3. Test tier-based context composition

### Step 4: Recovery Systems (Day 4)
1. Add `ContextRecoverySystem`
2. Implement emergency reduction strategies
3. Add proactive summarization triggers

### Step 5: Testing and Validation (Day 5)
1. Load test with large contexts
2. Validate overflow prevention
3. Confirm recovery mechanisms work

## Success Criteria

- ✅ **Zero context overflow errors** in testing
- ✅ **Context size consistently below 80,000 tokens**
- ✅ **Tool output optimized by 70%+**
- ✅ **Recovery mechanisms work within 2 seconds**
- ✅ **User experience unchanged** (same functionality, better reliability)

---

*This implementation plan provides concrete steps to prevent the context overflow that caused the LLM failures.*