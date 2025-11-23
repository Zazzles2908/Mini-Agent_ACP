"""
Concrete Integration Guide: Current System → Robust System
==========================================================

This guide shows exactly how to modify the existing agent.py to integrate
context overflow prevention without breaking current functionality.
"""

# ===========================================
# PHASE 1: MINIMAL CHANGES (Low Risk)
# ===========================================

# Step 1: Add token budget manager to Agent class
class Agent:
    def __init__(self, ...):
        # ... existing code ...
        
        # NEW: Add token budget enforcement
        self.token_budget = TokenBudgetManager(max_tokens=80000, warning_threshold=0.8)
        
    # Step 2: Add pre-LLM call token check
    async def run(self) -> str:
        # ... existing setup code ...
        
        while step < self.max_steps:
            # NEW: Check token budget BEFORE making LLM call
            current_context = self._get_full_context()
            if not self.token_budget.check_budget_before_llm(current_context):
                # NEW: Emergency context optimization
                print(f"{Colors.BRIGHT_YELLOW}[OPTIMIZE] Context optimization needed{Colors.RESET}")
                self._emergency_context_optimization()
                current_context = self._get_optimized_context()
            
            # NEW: Use optimized context for LLM call
            try:
                response = await self.llm.generate(messages=current_context, tools=tool_list)
                # Update actual token usage
                self.token_budget.update_actual_tokens(self._estimate_tokens())
            except Exception as e:
                # Handle LLM errors (including overflow)
                return self._handle_llm_error(e, step)

# Step 3: Add context optimization methods
def _get_full_context(self) -> list[Message]:
    """Get current full context before optimization"""
    return self.messages

def _emergency_context_optimization(self):
    """Emergency optimization when token budget exceeded"""
    # Remove verbose tool outputs, keep summaries
    self._optimize_tool_outputs()
    
    # Remove old conversation history, keep summaries
    self._compress_conversation_history()
    
    print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Context optimized{Colors.RESET}")

def _optimize_tool_outputs(self):
    """Remove verbose tool outputs, add summaries instead"""
    optimized_messages = []
    tool_summaries = []
    
    for msg in self.messages:
        if msg.role == "tool":
            # Optimize tool result
            optimized_tool = self._optimize_single_tool_result(msg)
            if optimized_tool:
                tool_summaries.append(optimized_tool)
        else:
            optimized_messages.append(msg)
    
    # Add summarized tool results
    if tool_summaries:
        summary_msg = Message(
            role="user", 
            content=f"[Tool Results Summary]: {len(tool_summaries)} tools executed - {', '.join(tool_summaries)}"
        )
        optimized_messages.append(summary_msg)
    
    self.messages = optimized_messages

def _optimize_single_tool_result(self, tool_msg: Message) -> str:
    """Optimize a single tool result"""
    content = tool_msg.content
    
    # Extract command from name and content
    if tool_msg.name == "bash":
        # Parse bash command and optimize output
        if "Get-ChildItem" in content and "-Recurse" in content:
            return self._summarize_directory_listing(content)
        elif "git" in content.lower():
            return self._summarize_git_output(content)
        else:
            return "bash command executed"
    
    elif "file" in tool_msg.name.lower():
        # File operations - extract key info only
        return f"file operation completed: {tool_msg.name}"
    
    else:
        return f"{tool_msg.name} tool executed"

def _summarize_directory_listing(self, content: str) -> str:
    """Summarize directory listing results"""
    lines = content.split('\n')
    dirs = [l for l in lines if l.strip() and l.startswith('d---')]
    files = [l for l in lines if l.strip() and l.startswith('-a---')]
    
    dir_names = [l.split()[-1] for l in dirs[:5]]  # First 5 dirs only
    return f"{len(dirs)} dirs, {len(files)} files ({', '.join(dir_names)})"

def _compress_conversation_history(self):
    """Compress old conversation messages"""
    if len(self.messages) > 20:  # If too many messages
        # Keep first message (system), last 5 messages, and middle summary
        system_msg = self.messages[0]
        recent_messages = self.messages[-5:]
        middle_summary = self._create_conversation_summary(self.messages[1:-5])
        
        self.messages = [system_msg, middle_summary] + recent_messages

# ===========================================
# PHASE 2: TOOL INTEGRATION (Medium Risk)
# ===========================================

# Step 4: Modify tool execution to add optimization
async def run(self) -> str:
    # ... existing loop ...
    
    # Execute tool calls (EXISTING)
    for tool_call in response.tool_calls:
        # ... existing tool execution ...
        
        # NEW: Optimize result before adding to context
        optimized_result = self._optimize_tool_result_for_context(function_name, result)
        
        tool_msg = Message(
            role="tool",
            content=optimized_result,  # Use optimized result
            tool_call_id=tool_call_id,
            name=function_name,
        )
        self.messages.append(tool_msg)

def _optimize_tool_result_for_context(self, tool_name: str, result: ToolResult) -> str:
    """Optimize tool result before adding to context"""
    if not result.success:
        return f"Error: {result.error}"  # Short error messages
    
    # Bash tool optimization
    if tool_name == "bash":
        return self._optimize_bash_result(result.content)
    
    # File tool optimization
    elif "file" in tool_name.lower():
        return self._optimize_file_result(result.content)
    
    # Default optimization
    else:
        return self._truncate_for_context(result.content)

def _optimize_bash_result(self, content: str) -> str:
    """Optimize bash command results"""
    lines = content.split('\n')
    
    # Directory listing optimization
    if any('Get-ChildItem' in line for line in lines):
        dirs = [l for l in lines if l.strip().startswith('d---')]
        files = [l for l in lines if l.strip().startswith('-a---')]
        
        dir_names = [l.split()[-1] for l in dirs[:10]]  # First 10 only
        return f"Directory: {len(dirs)} dirs, {len(files)} files | Dirs: {', '.join(dir_names)}"
    
    # Git command optimization
    elif any('git' in line.lower() for line in lines):
        if 'status' in content.lower():
            modified = content.count('modified:')
            new_files = content.count('new file:')
            return f"Git status: {modified} modified, {new_files} new files"
        else:
            return "Git operation completed"
    
    # Generic bash optimization
    else:
        if len(content) > 200:
            return content[:200] + "..."  # Truncate
        return content

def _optimize_file_result(self, content: str) -> str:
    """Optimize file operation results"""
    if len(content) > 300:
        return f"File operation completed ({len(content)} chars)"
    return content

def _truncate_for_context(self, content: str, max_chars: int = 200) -> str:
    """Generic truncation for context"""
    if len(content) > max_chars:
        return content[:max_chars] + "..."
    return content

# ===========================================
# PHASE 3: CONTEXT TIERING (Higher Risk)
# ===========================================

# Step 5: Implement context tiering system
class Agent:
    def __init__(self, ...):
        # ... existing code ...
        
        # NEW: Context tiering system
        self.context_tiers = {
            'critical': [],    # System prompt
            'recent': [],      # Last 5 messages
            'summarized': [],  # Older content (summarized)
            'tool_results': [] # Tool results (optimized)
        }
        
        # Add system message to critical tier
        self.context_tiers['critical'].append(self.messages[0])
        
    def _get_optimized_context(self) -> list[Message]:
        """Get context composed from tiers with size limits"""
        context = []
        
        # Critical content (system prompt) - always included
        context.extend(self.context_tiers['critical'])
        
        # Recent messages (last 3)
        recent = self.context_tiers['recent'][-3:]
        context.extend(recent)
        
        # Summarized content (latest only)
        if self.context_tiers['summarized']:
            context.extend(self.context_tiers['summarized'][-1:])
        
        # Tool results (optimized summaries)
        tool_summary = self.context_tiers['tool_results']
        if tool_summary:
            context.extend(tool_summary[-2:])  # Last 2 tool summaries
        
        return context
    
    def _route_message_to_tier(self, msg: Message):
        """Route new messages to appropriate tier"""
        if msg.role == "user":
            # Add to recent tier
            self.context_tiers['recent'].append(msg)
            
            # Limit recent tier to 5 messages
            if len(self.context_tiers['recent']) > 5:
                old_msg = self.context_tiers['recent'].pop(0)
                # Move to summarized tier
                self.context_tiers['summarized'].append(old_msg)
        
        elif msg.role == "tool":
            # Add to tool results tier
            self.context_tiers['tool_results'].append(msg)
            
            # Limit tool results to 3 items
            if len(self.context_tiers['tool_results']) > 3:
                self.context_tiers['tool_results'].pop(0)

# ===========================================
# PHASE 4: PROACTIVE OPTIMIZATION (Full System)
# ===========================================

# Step 6: Add proactive optimization before LLM calls
class Agent:
    async def run(self) -> str:
        while step < self.max_steps:
            # PROACTIVE: Check if next LLM call will overflow
            if self._will_next_llm_call_overflow():
                self._proactive_context_optimization()
            
            # Use optimized context
            context = self._get_optimized_context()
            
            # Make LLM call with safe context
            try:
                response = await self.llm.generate(messages=context, tools=tool_list)
            except Exception as e:
                # Handle any remaining LLM errors
                return self._handle_llm_error(e, step)
            
            # Route assistant response to tiers
            assistant_msg = Message(...)
            self._route_message_to_tier(assistant_msg)
            
            # Execute tools with optimization
            for tool_call in response.tool_calls:
                result = await tool.execute(**arguments)
                optimized_result = self._optimize_tool_result(tool_call.function.name, result)
                
                tool_msg = Message(...)
                self._route_message_to_tier(tool_msg)
    
    def _will_next_llm_call_overflow(self) -> bool:
        """Predict if next LLM call will overflow token limit"""
        estimated_tokens = 0
        
        # Count all context tiers
        for tier_messages in self.context_tiers.values():
            for msg in tier_messages:
                estimated_tokens += self._estimate_message_tokens(msg)
        
        # Add estimated cost of next response (rough calculation)
        estimated_tokens += 1000  # Conservative estimate for next response
        
        # Check if this will exceed limit
        return estimated_tokens > self.token_limit * 0.9  # 90% threshold
    
    def _proactive_context_optimization(self):
        """Optimize context before overflow occurs"""
        print(f"{Colors.BRIGHT_YELLOW}[PROACTIVE] Optimizing context to prevent overflow{Colors.RESET}")
        
        # Strategy 1: Compress tool results
        self._compress_tool_results()
        
        # Strategy 2: Reduce recent conversation
        self._reduce_recent_conversation()
        
        # Strategy 3: Merge summarized content
        self._merge_summarized_content()
        
        print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Proactive optimization complete{Colors.RESET}")

# ===========================================
# IMPLEMENTATION PRIORITIES
# ===========================================

"""
PHASE 1 (Immediate - Low Risk):
✅ Add token_budget manager
✅ Add pre-LLM call checks
✅ Add emergency optimization
✅ Basic tool output truncation

PHASE 2 (Tool Integration - Medium Risk):
✅ Modify tool execution with optimization
✅ Add bash command summarization
✅ Add file operation optimization

PHASE 3 (Context Tiering - Higher Risk):
✅ Implement tier routing
✅ Replace flat message list with tiers
✅ Add tier-based context composition

PHASE 4 (Full System - Highest Risk):
✅ Proactive overflow prevention
✅ Advanced optimization strategies
✅ Full context management system
"""

# ===========================================
# BACKWARD COMPATIBILITY NOTES
# ===========================================

"""
To maintain backward compatibility:

1. Keep existing method signatures
2. Add new methods with different names
3. Preserve existing error handling patterns
4. Maintain same output formats
5. Add feature flags for gradual rollout

Example backward-compatible approach:

class Agent:
    async def run(self) -> str:
        # Keep existing interface
        # Internally use new optimized system
        context = self._get_full_context()  # Backward compatible
        if self.enable_optimization:  # Feature flag
            context = self._get_optimized_context()
        
        return await self._run_with_context(context)
"""
