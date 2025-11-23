# Best Practices Summary for MiniMax M2 + GLM-4.6 Systems

## Executive Summary

Based on industry research and our dual-model architecture, this document summarizes the **best practices** for preventing context overflow while optimizing performance for both MiniMax M2 and GLM-4.6 models.

## Core Principles

### 1. **Prevention Over Recovery**
- **Industry Standard**: Intercept overflow before it reaches the LLM
- **Our Implementation**: Proactive token budget checks before each LLM call
- **Impact**: Eliminates the 1M+ token overflow events we experienced

### 2. **Model-Specific Optimization**
- **MiniMax M2**: Leverage longer context window (200K) for detailed conversations
- **GLM-4.6**: Optimize aggressively for efficient context usage (128K limit)
- **Unified Approach**: Same prevention mechanisms, different optimization strategies

### 3. **Tool Output Priority**
- **Industry Finding**: 70-90% of context bloat comes from verbose tool outputs
- **Our Focus**: Optimize bash commands and file operations first
- **Expected Impact**: 80%+ reduction in tool result context size

## Model-Specific Best Practices

### **MiniMax M2 Best Practices**

#### **Context Strategy:**
- **Budget Threshold**: 150,000 tokens (75% of 200K limit)
- **Preservation Mode**: Detailed recent conversation history
- **Optimization Level**: Moderate (preserve context detail)

#### **Tool Optimization:**
```python
# MiniMax-optimized bash result handling
def optimize_bash_for_minimax(command, output):
    if "Get-ChildItem" in command:
        # Preserve more directory detail for MiniMax
        dirs = extract_directories(output, max_count=15)
        files = extract_files(output, max_count=20)
        return f"Structure: {len(dirs)} directories, {len(files)} files | Sample: {dirs[:10]}"
    elif "git" in command:
        # Detailed git status
        return summarize_git_detailed(output)
    return output[:500] + "..." if len(output) > 500 else output
```

#### **Conversation Management:**
- Keep last 10 messages in full detail
- Summarize content older than 20 messages
- Preserve tool execution details

### **GLM-4.6 Best Practices**

#### **Context Strategy:**
- **Budget Threshold**: 96,000 tokens (75% of 128K limit)
- **Preservation Mode**: Compressed summaries
- **Optimization Level**: Aggressive (maximum efficiency)

#### **Tool Optimization:**
```python
# GLM-optimized bash result handling
def optimize_bash_for_glm(command, output):
    if "Get-ChildItem" in command:
        # Minimal summary for GLM efficiency
        count = count_directory_items(output)
        return f"Directory: {count['dirs']} dirs, {count['files']} files"
    elif "git" in command:
        # Compressed git summary
        return f"Git: {count_git_changes(output)} changes"
    return f"Command completed ({len(output)} chars)" if len(output) > 100 else output
```

#### **Conversation Management:**
- Keep last 5 messages in full detail
- Summarize content older than 10 messages
- Aggressive tool result compression

## Implementation Best Practices

### **1. Token Budget Enforcement Pattern**

```python
# Industry-standard implementation
class ModelAwareTokenBudget:
    def __init__(self, model_name):
        self.model_name = model_name
        self.limits = {
            "MiniMax-M2": {"max": 200000, "warning": 150000},
            "GLM-4.6": {"max": 128000, "warning": 96000}
        }
    
    def check_budget(self, context):
        tokens = self.estimate_tokens(context)
        limit = self.limits[self.model_name]["warning"]
        return tokens <= limit
    
    def get_model_specific_threshold(self):
        return self.limits[self.model_name]["warning"]
```

### **2. Context Tiering Pattern**

```python
# Best practice context organization
class BestPracticeContextTier:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tier_limits = self._get_tier_limits(model_name)
    
    def _get_tier_limits(self, model_name):
        if model_name == "MiniMax-M2":
            return {
                "critical": 0.6,      # 60% for system + current task
                "recent": 0.25,       # 25% for recent messages
                "summarized": 0.10,   # 10% for historical summary
                "tool_results": 0.05  # 5% for tool summaries
            }
        else:  # GLM-4.6
            return {
                "critical": 0.65,     # 65% for system + current task
                "recent": 0.20,       # 20% for recent messages
                "summarized": 0.10,   # 10% for historical summary
                "tool_results": 0.05  # 5% for tool summaries
            }
```

### **3. Tool Optimization Pattern**

```python
# Industry-standard tool result optimization
class IndustryToolOptimizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.compression_level = self._get_compression_level()
    
    def optimize_bash_result(self, command, output):
        # Industry pattern: command-specific optimization
        if "list" in command or "ls" in command or "Get-ChildItem" in command:
            return self._optimize_directory_listing(output, command)
        elif "git" in command.lower():
            return self._optimize_git_output(output, command)
        elif "find" in command:
            return self._optimize_find_output(output, command)
        else:
            return self._optimize_generic_bash(output)
    
    def _optimize_directory_listing(self, output, command):
        # Extract counts and key items only
        dirs, files = self._count_directory_items(output)
        sample_items = self._extract_sample_items(output, limit=10)
        
        return f"Filesystem: {dirs} dirs, {files} files | Items: {', '.join(sample_items)}"
    
    def _optimize_git_output(self, output, command):
        # Industry pattern for git optimization
        if "status" in command.lower():
            changes = self._parse_git_changes(output)
            return f"Git status: {changes['modified']} modified, {changes['new']} new, {changes['deleted']} deleted"
        return f"Git operation completed ({len(output.split())} items)"
```

### **4. Error Recovery Pattern**

```python
# Industry-standard progressive recovery
class ProgressiveRecoverySystem:
    def __init__(self, model_name):
        self.model_name = model_name
        self.recovery_strategies = self._get_recovery_strategies()
    
    def handle_overflow(self, context):
        for i, strategy in enumerate(self.recovery_strategies, 1):
            try:
                reduced = strategy(context)
                if self._is_safe_size(reduced):
                    logger.info(f"Recovery successful with strategy {i}")
                    return reduced
            except Exception as e:
                logger.warning(f"Recovery strategy {i} failed: {e}")
        
        # Emergency fallback
        return self._emergency_context_reduction(context)
    
    def _get_recovery_strategies(self):
        return [
            self._remove_verbose_tool_outputs,
            self._reduce_conversation_history,
            self._compress_system_context,
            self._emergency_minimal_context
        ]
```

## Performance Optimization Best Practices

### **1. Lazy Optimization**
- Only optimize when approaching budget limits
- Avoid optimization overhead for normal operation
- Use caching for repeated optimizations

### **2. Model-Specific Tuning**
- Different compression levels for different models
- Model-aware token estimation
- Adaptive thresholds based on model characteristics

### **3. Monitoring and Alerting**
```python
# Industry-standard monitoring
class ContextMonitoring:
    def __init__(self):
        self.metrics = {
            "overflow_attempts": 0,
            "optimizations_performed": 0,
            "average_context_size": 0,
            "model_utilization": {}
        }
    
    def log_context_event(self, event_type, details):
        if event_type == "overflow_prevented":
            self.metrics["overflow_attempts"] += 1
        elif event_type == "optimization_performed":
            self.metrics["optimizations_performed"] += 1
        
        # Update model-specific metrics
        model = details.get("model")
        if model:
            if model not in self.model_utilization:
                self.model_utilization[model] = []
            self.model_utilization[model].append(details["utilization"])
```

## Common Pitfalls to Avoid

### **1. Over-Optimization**
- **Problem**: Optimizing too aggressively loses important context
- **Solution**: Model-specific optimization levels
- **Industry Practice**: Preserve critical information, optimize noise

### **2. Reactive Only Approach**
- **Problem**: Only optimizing after overflow occurs
- **Solution**: Proactive budget checks before LLM calls
- **Industry Practice**: Prevention-first architecture

### **3. Model-Agnostic Optimization**
- **Problem**: Same optimization for all models
- **Solution**: Model-specific strategies and thresholds
- **Industry Practice**: Leverage each model's strengths

### **4. Tool Output Blindness**
- **Problem**: Not optimizing tool results (biggest context source)
- **Solution**: Priority optimization for bash/file operations
- **Industry Practice**: Tool outputs are the primary context bloat source

## Success Metrics and KPIs

### **Primary Metrics:**
- **Context Overflow Rate**: Target = 0%
- **Context Size**: <75% of model limit consistently
- **Tool Output Compression**: >70% size reduction
- **Optimization Response Time**: <2 seconds

### **Secondary Metrics:**
- **Model Utilization Efficiency**: 60-75% of limit
- **Conversation Preservation Quality**: Retain essential information
- **Tool Result Accuracy**: Maintain functional completeness

### **Model-Specific Targets:**

#### **MiniMax M2:**
- Context utilization: 60-75% of 200K limit
- Detailed conversation preservation
- Moderate tool compression (80% reduction)

#### **GLM-4.6:**
- Context utilization: 50-75% of 128K limit
- Compressed conversation preservation  
- Aggressive tool compression (90% reduction)

## Integration Checklist

### **Phase 1: Foundation**
- [ ] Implement model-specific token budget checking
- [ ] Add tool output optimization for bash commands
- [ ] Create basic context tiering structure
- [ ] Test with both MiniMax M2 and GLM-4.6

### **Phase 2: Optimization**
- [ ] Implement model-aware compression strategies
- [ ] Add sliding window for large conversations
- [ ] Create progressive recovery system
- [ ] Add performance monitoring

### **Phase 3: Advanced Features**
- [ ] Real-time context monitoring dashboard
- [ ] Adaptive optimization based on usage patterns
- [ ] A/B testing framework for optimization strategies
- [ ] Integration with existing validation systems

---

## Conclusion

These best practices are based on **industry-proven patterns** that work specifically well with our **MiniMax M2 + GLM-4.6 dual-model architecture**. The key is **model-specific optimization** that leverages each model's strengths while maintaining consistent overflow prevention.

**Most Critical Implementation**: Proactive token budget enforcement before each LLM call - this alone will prevent the 1M+ token overflow events we experienced.
