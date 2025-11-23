"""
CORRECTED Context Overflow Prevention - Updated for 200K Token Limit
===================================================================

Both MiniMax-M2 and GLM-4.6 now have 200K token context windows!
This makes our implementation much more powerful and simplified.
"""

class CorrectedTokenBudgetManager:
    """Updated token budget manager for 200K context windows"""
    
    def __init__(self, model_name: str, max_tokens: int = 200000):
        self.model_name = model_name
        self.max_tokens = max_tokens  # 200K for both models
        
        # Conservative thresholds for safety
        self.warning_threshold = int(max_tokens * 0.60)  # 120K (60%)
        self.safe_threshold = int(max_tokens * 0.75)     # 150K (75%)
        self.overflow_threshold = int(max_tokens * 0.95) # 190K (95%)
        
        self.current_tokens = 0
    
    def check_budget_before_llm(self, context) -> bool:
        """Check if context will fit within 200K budget"""
        try:
            # Estimate tokens (improved calculation)
            estimated_tokens = self._estimate_tokens_accurate(context)
            
            print(f"{Colors.BRIGHT_CYAN}[BUDGET] Context check: {estimated_tokens:,}/{self.max_tokens:,} tokens ({estimated_tokens/self.max_tokens:.1%}){Colors.RESET}")
            
            # Multiple warning levels
            if estimated_tokens > self.overflow_threshold:
                print(f"{Colors.BRIGHT_RED}[CRITICAL] Overflow risk: {estimated_tokens}/{self.max_tokens}{Colors.RESET}")
                return False
            elif estimated_tokens > self.safe_threshold:
                print(f"{Colors.BRIGHT_YELLOW}[WARNING] Approaching limit: {estimated_tokens}/{self.safe_threshold}{Colors.RESET}")
                return True  # Allow but warn
            else:
                print(f"{Colors.BRIGHT_GREEN}[SAFE] Well within limits: {estimated_tokens}/{self.safe_threshold}{Colors.RESET}")
                return True
                
        except Exception as e:
            print(f"{Colors.BRIGHT_YELLOW}[BUDGET] Check failed: {e} - proceeding cautiously{Colors.RESET}")
            return True
    
    def _estimate_tokens_accurate(self, context) -> int:
        """More accurate token estimation"""
        total_tokens = 0
        
        for msg in context:
            if hasattr(msg, 'content') and msg.content:
                # Basic content estimation
                content_tokens = len(str(msg.content)) // 4
                total_tokens += content_tokens
                
                # Add overhead for thinking, tool calls, metadata
                if hasattr(msg, 'thinking') and msg.thinking:
                    total_tokens += len(str(msg.thinking)) // 4
                
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    total_tokens += len(str(msg.tool_calls)) // 4
                
                # Message overhead (role, metadata, etc.)
                total_tokens += 10  # Rough estimate per message
        
        return total_tokens

class UnifiedContextOptimizer:
    """Context optimizer for 200K token windows - both models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.max_context = 200000  # Unified limit
        
        # Model-specific optimization strategies (same limit, different approach)
        if "glm" in model_name.lower():
            # GLM-4.6: Enhanced coding performance + tool use
            self.strategy = {
                "preserve_detail": "high",
                "tool_optimization": "aggressive", 
                "coding_focus": True,
                "tool_integration": True
            }
        else:
            # MiniMax-M2: Agentic capabilities + streaming
            self.strategy = {
                "preserve_detail": "medium",
                "tool_optimization": "balanced",
                "agentic_focus": True,
                "streaming_optimization": True
            }
    
    def optimize_tool_result(self, tool_name: str, result_content: str) -> str:
        """Optimize tool results with 200K context awareness"""
        
        # For 200K context, we can be more generous with preservation
        if self.strategy["tool_optimization"] == "aggressive":
            # GLM-4.6: More aggressive optimization
            return self._optimize_aggressive(tool_name, result_content)
        else:
            # MiniMax-M2: Balanced optimization
            return self._optimize_balanced(tool_name, result_content)
    
    def _optimize_aggressive(self, tool_name: str, content: str) -> str:
        """GLM-4.6 aggressive optimization"""
        if tool_name == "bash":
            return self._optimize_bash_glm(content)
        elif "file" in tool_name.lower():
            return self._optimize_file_glm(content)
        else:
            return self._optimize_generic_glm(content)
    
    def _optimize_balanced(self, tool_name: str, content: str) -> str:
        """MiniMax-M2 balanced optimization"""
        if tool_name == "bash":
            return self._optimize_bash_minimax(content)
        elif "file" in tool_name.lower():
            return self._optimize_file_minimax(content)
        else:
            return self._optimize_generic_minimax(content)
    
    def _optimize_bash_glm(self, content: str) -> str:
        """GLM-4.6 optimized bash handling"""
        if "Get-ChildItem" in content:
            lines = content.split('\n')
            dirs = [l for l in lines if l.strip().startswith('d---')]
            files = [l for l in lines if l.strip().startswith('-a---')]
            
            # More aggressive compression for GLM
            return f"Filesystem: {len(dirs)} dirs, {len(files)} files"
        
        elif "git" in content.lower():
            if "status" in content.lower():
                changes = self._count_git_changes(content)
                return f"Git: {changes['modified']} mod, {changes['new']} new"
            return "Git operation completed"
        
        return f"Command completed ({len(content.split())} items)"
    
    def _optimize_bash_minimax(self, content: str) -> str:
        """MiniMax-M2 balanced bash handling"""
        if "Get-ChildItem" in content:
            lines = content.split('\n')
            dirs = [l for l in lines if l.strip().startswith('d---')]
            files = [l for l in lines if l.strip().startswith('-a---')]
            
            # Preserve more detail for MiniMax
            dir_names = [l.split()[-1] for l in dirs[:8]]
            sample = ', '.join(dir_names)
            
            return f"Directory structure: {len(dirs)} directories, {len(files)} files | Items: {sample}"
        
        elif "git" in content.lower():
            if "status" in content.lower():
                changes = self._count_git_changes(content)
                return f"Git status: {changes['modified']} modified, {changes['new']} new, {changes['deleted']} deleted files"
            return "Git operation completed successfully"
        
        return content[:400] + "..." if len(content) > 400 else content
    
    def _count_git_changes(self, content: str) -> dict:
        """Count git status changes"""
        return {
            'modified': content.count('modified:'),
            'new': content.count('new file:'),
            'deleted': content.count('deleted:')
        }

class ContextTierManager:
    """Updated tier manager for 200K context windows"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.max_context = 200000
        
        # Updated tier allocations for 200K context
        self.tier_allocations = {
            'critical': 0.60,      # 120K - System + current task
            'recent': 0.25,        # 50K - Recent conversation
            'tool_results': 0.10,  # 20K - Tool summaries
            'historical': 0.05     # 10K - Historical summaries
        }
        
        self.tiers = {
            'critical': [],
            'recent': [],
            'tool_results': [],
            'historical': []
        }
    
    def get_optimal_context(self) -> list:
        """Get optimized context within 200K limit"""
        context = []
        
        # Critical content (system prompt + current task)
        context.extend(self.tiers['critical'])
        
        # Recent conversation (more generous with 200K)
        recent_count = 8 if "glm" in self.model_name.lower() else 6
        recent = self.tiers['recent'][-recent_count:] if len(self.tiers['recent']) > recent_count else self.tiers['recent']
        context.extend(recent)
        
        # Tool results (optimized summaries)
        tool_results = self.tiers['tool_results']
        context.extend(tool_results[-5:] if tool_results else [])
        
        # Historical content (latest summaries)
        if self.tiers['historical']:
            context.append(self.tiers['historical'][-1])
        
        return context

# Updated Agent integration for 200K contexts
class UpdatedAgentIntegration:
    """How to integrate with existing agent.py using 200K limits"""
    
    def __init__(self, llm_client, existing_agent):
        self.llm = llm_client
        self.agent = existing_agent
        self.optimizer = UnifiedContextOptimizer(self._get_model_name())
        self.budget = CorrectedTokenBudgetManager(self._get_model_name())
        self.tier_manager = ContextTierManager(self._get_model_name())
    
    def _get_model_name(self) -> str:
        """Detect model name"""
        model_info = getattr(self.llm, 'model', 'unknown')
        if 'glm' in str(model_info).lower():
            return 'GLM-4.6'
        elif 'minimax' in str(model_info).lower():
            return 'MiniMax-M2'
        else:
            return 'unknown'
    
    def enhanced_run_method(self):
        """Enhanced run method with 200K context management"""
        
        # Check budget before LLM call
        if not self.budget.check_budget_before_llm(self.agent.messages):
            print(f"{Colors.BRIGHT_YELLOW}[OPTIMIZE] Context optimization needed{Colors.RESET}")
            self._apply_context_optimization()
        
        # Continue with existing agent logic
        # The existing agent.run() method remains largely unchanged
        pass
    
    def _apply_context_optimization(self):
        """Apply context optimization for 200K limit"""
        print(f"{Colors.BRIGHT_CYAN}[200K OPTIMIZE] Applying 200K context optimization{Colors.RESET}")
        
        # Strategy 1: Optimize tool outputs (most impact)
        self._optimize_tool_outputs()
        
        # Strategy 2: Compress conversation if needed
        if len(self.agent.messages) > 15:
            self._compress_conversation_history()
        
        print(f"{Colors.BRIGHT_GREEN}[200K OPTIMIZE] Context optimization complete{Colors.RESET}")
    
    def _optimize_tool_outputs(self):
        """Optimize tool outputs with 200K awareness"""
        optimized_messages = []
        
        for msg in self.agent.messages:
            if msg.role == "tool":
                # Apply model-specific optimization
                optimized_content = self.optimizer.optimize_tool_result(msg.name, msg.content)
                msg.content = optimized_content
            optimized_messages.append(msg)
        
        self.agent.messages = optimized_messages

# Usage with existing agent.py
def integrate_with_existing_agent(agent_instance):
    """Integrate 200K optimization with existing agent"""
    
    # Get model name
    model_name = "GLM-4.6" if hasattr(agent_instance.llm, 'model') and 'glm' in str(agent_instance.llm.model).lower() else "MiniMax-M2"
    
    # Add token budget management
    agent_instance.token_budget = CorrectedTokenBudgetManager(model_name)
    
    # Add context optimizer
    agent_instance.context_optimizer = UnifiedContextOptimizer(model_name)
    
    # Add tier manager
    agent_instance.context_tiers = ContextTierManager(model_name)
    
    # Modify the run method (minimal changes needed)
    original_run = agent_instance.run
    
    async def enhanced_run():
        # Add pre-LLM budget check
        if hasattr(agent_instance, 'token_budget'):
            current_context = agent_instance.messages
            if not agent_instance.token_budget.check_budget_before_llm(current_context):
                print(f"{Colors.BRIGHT_YELLOW}[200K] Context optimization needed{Colors.RESET}")
                # Apply optimization before proceeding
                agent_instance._apply_200k_optimization()
        
        # Continue with original run method
        return await original_run()
    
    agent_instance.run = enhanced_run
    return agent_instance

# Example usage:
"""
# With 200K context limits, our overflow problem is significantly reduced:

CONTEXT_COMPARISON = {
    'Previous Limit': 80000,
    'Current Models': 200000,  # Both MiniMax-M2 and GLM-4.6
    'Improvement': '2.5x larger context window',
    'Our Overflow': 1005262,  # Still exceeds even 200K
    'Solution': 'Proactive optimization before hitting 200K'
}

print(f"With 200K limits: {CONTEXT_COMPARISON['Our Overflow']/200000:.1f}x overflow still possible")
print(f"Target: Keep context <150K (75% of 200K) for safety")
print(f"Result: Prevent the 1M+ token overflow events")
"""
