# 🤖 Agent Client Protocol & LLM Integration
## Mini-Agent Core Intelligence & Communication Layer

**Date**: November 25, 2025  
**Component**: Agent Client Protocol & LLM Integration  
**Status**: MiniMax-M2 Integration Operational

---

## 🎯 **AGENT CLIENT PROTOCOL OVERVIEW**

### **Protocol Architecture: Communication Bridge**

The Agent Client Protocol serves as the **communication bridge** between Mini-Agent and the underlying LLM (currently MiniMax-M2), handling prompt construction, tool selection, and response processing.

```
┌─────────────────────────────────────────────────────────────┐
│                   User Interface Layer                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Web UI    │ │    CLI      │ │   API       │            │
│  │ Interface   │ │ Interface   │ │ Interface   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Agent Execution Layer                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Agent     │ │   Tool      │ │   Skills    │            │
│  │   Class     │ │  System     │ │  System     │            │
│  │             │ │             │ │             │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent Client Protocol Layer                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Prompt    │ │   Tool      │ │  Response   │            │
│  │ Construction│ │   Selection │ │  Processing │            │
│  │             │ │             │ │             │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 LLM Integration Layer                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   MiniMax   │ │   OpenAI    │ │  Anthropic  │            │
│  │    -M2      │ │  Protocol   │ │   Protocol  │            │
│  │             │ │             │ │             │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 **CURRENT LLM CONFIGURATION**

### **MiniMax-M2 Integration**

**Primary LLM**: MiniMax-M2 via Anthropic Protocol  
**Provider**: Anthropic (with MiniMax-M2 model)  
**Protocol**: OpenAI SDK format compatibility

```python
# Current LLM Configuration (from config.yaml)
api_key: "${MINIMAX_API_KEY}"
api_base: "https://api.minimax.io"   # Global users (default)
model: "MiniMax-M2"
provider: "anthropic"  # FIXED: Restored working provider for MiniMax-M2
```

### **LLM Client Implementation**

**File**: `mini_agent/llm_client.py`

```python
class LLMClient:
    """LLM client for agent communication with multiple provider support"""
    
    def __init__(self, api_key: str, model: str, provider: str, api_base: str):
        self.api_key = api_key
        self.model = model
        self.provider = provider  # "anthropic" for MiniMax-M2
        self.api_base = api_base
        
        # Initialize appropriate client based on provider
        if provider == "anthropic":
            self.client = self._init_anthropic_client()
        elif provider == "openai":
            self.client = self._init_openai_client()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _init_anthropic_client(self):
        """Initialize Anthropic-compatible client (for MiniMax-M2)"""
        
        # Use Anthropic SDK format for MiniMax-M2
        return Anthropic(
            api_key=self.api_key,
            base_url=self.api_base  # Points to MiniMax endpoint
        )
    
    async def generate_response(
        self, 
        system_prompt: str, 
        messages: List[Dict], 
        max_tokens: int = None,
        temperature: float = None
    ) -> Dict:
        """Generate response using appropriate LLM"""
        
        try:
            if self.provider == "anthropic":
                return await self._generate_anthropic_response(
                    system_prompt, messages, max_tokens, temperature
                )
            elif self.provider == "openai":
                return await self._generate_openai_response(
                    system_prompt, messages, max_tokens, temperature
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
        except Exception as e:
            raise LLMClientError(f"LLM generation failed: {str(e)}")
    
    async def _generate_anthropic_response(
        self, 
        system_prompt: str, 
        messages: List[Dict], 
        max_tokens: int = None,
        temperature: float = None
    ) -> Dict:
        """Generate response using Anthropic protocol"""
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for message in messages:
            if message["role"] in ["user", "assistant"]:
                anthropic_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        # Generate response
        response = await self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=anthropic_messages,
            max_tokens=max_tokens or 2000,
            temperature=temperature or 0.7
        )
        
        return {
            "content": response.content[0].text,
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens
            },
            "finish_reason": response.stop_reason
        }
```

---

## 🔧 **AGENT CLASS ARCHITECTURE**

### **Core Agent Implementation**

**File**: `mini_agent/agent.py`

```python
class Agent:
    """Core agent class for Mini-Agent execution"""
    
    def __init__(
        self, 
        llm_client: LLMClient,
        system_prompt: str,
        tools: List[Tool],
        max_steps: int = 50,
        workspace_dir: str = "./workspace",
        token_limit: int = 200000
    ):
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.tools = tools
        self.max_steps = max_steps
        self.workspace_dir = Path(workspace_dir)
        self.token_limit = token_limit
        
        # Execution state
        self.messages = []
        self.current_step = 0
        self.completed_tasks = []
        self.failed_tasks = []
        
        # Tool management
        self.available_tools = self._organize_tools()
        self.tool_schemas = self._generate_tool_schemas()
    
    def _organize_tools(self) -> Dict[str, Tool]:
        """Organize tools by category for efficient access"""
        
        organized = {
            "file_tools": [],
            "bash_tools": [],
            "web_tools": [],
            "mcp_tools": [],
            "enhanced_tools": [],
            "meta_tools": []
        }
        
        for tool in self.tools:
            tool_name = tool.__class__.__name__
            
            if "File" in tool_name:
                organized["file_tools"].append(tool)
            elif "Bash" in tool_name:
                organized["bash_tools"].append(tool)
            elif "Web" in tool_name:
                organized["web_tools"].append(tool)
            elif "MCP" in tool_name or "MCPLoader" in tool_name:
                organized["mcp_tools"].append(tool)
            elif "Enhanced" in tool_name:
                organized["enhanced_tools"].append(tool)
            else:
                organized["meta_tools"].append(tool)
        
        return organized
    
    def _generate_tool_schemas(self) -> Dict:
        """Generate tool schemas for LLM communication"""
        
        schemas = {}
        
        for tool in self.tools:
            if hasattr(tool, 'name') and hasattr(tool, 'description') and hasattr(tool, 'parameters'):
                schemas[tool.name] = {
                    "description": tool.description,
                    "parameters": tool.parameters
                }
        
        return schemas
    
    async def run(self) -> str:
        """Main agent execution loop"""
        
        try:
            # Initialize execution
            await self._initialize_execution()
            
            # Main execution loop
            while self.current_step < self.max_steps:
                # Get next action from LLM
                action = await self._get_next_action()
                
                if not action:
                    break  # No more actions needed
                
                # Execute action
                result = await self._execute_action(action)
                
                # Process result
                await self._process_execution_result(result)
                
                # Check for completion
                if await self._check_task_completion():
                    break
            
            # Generate final summary
            final_summary = await self._generate_final_summary()
            return final_summary
            
        except Exception as e:
            error_summary = f"Agent execution failed: {str(e)}"
            await self._log_error(error_summary)
            return error_summary
    
    async def _get_next_action(self) -> Dict:
        """Get next action from LLM based on current state"""
        
        # Prepare context for LLM
        context = await self._prepare_execution_context()
        
        # Create prompt
        prompt = await self._create_execution_prompt(context)
        
        # Generate response
        response = await self.llm_client.generate_response(
            system_prompt=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ] + self.messages
        )
        
        # Parse action from response
        action = await self._parse_action_from_response(response["content"])
        
        return action
    
    async def _prepare_execution_context(self) -> Dict:
        """Prepare execution context for LLM decision making"""
        
        return {
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "available_tools": list(self.tool_schemas.keys()),
            "tool_descriptions": self.tool_schemas,
            "workspace_files": self._list_workspace_files(),
            "recent_execution_summary": await self._get_recent_execution_summary(),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks
        }
    
    async def _create_execution_prompt(self, context: Dict) -> str:
        """Create execution prompt for LLM"""
        
        prompt = f"""
Current Step: {context['current_step']}/{context['max_steps']}

Available Tools:
{self._format_tool_descriptions(context['tool_descriptions'])}

Recent Workspace Files:
{chr(10).join(context['workspace_files'][:10])}  # Limit to recent files

Recent Execution Summary:
{context['recent_execution_summary']}

Please determine the next action to complete the task.
Choose from available tools or indicate if the task is complete.
"""
        
        return prompt
    
    def _format_tool_descriptions(self, tool_schemas: Dict) -> str:
        """Format tool descriptions for prompt"""
        
        formatted = []
        for tool_name, schema in tool_schemas.items():
            formatted.append(f"- {tool_name}: {schema['description']}")
        
        return "\n".join(formatted)
    
    async def _parse_action_from_response(self, response_content: str) -> Dict:
        """Parse action from LLM response"""
        
        # Simple parsing - in production, this would be more sophisticated
        try:
            # Look for tool calls in response
            if "use_tool" in response_content.lower():
                # Extract tool name and parameters
                # This is a simplified implementation
                lines = response_content.split('\n')
                for line in lines:
                    if "tool:" in line.lower():
                        tool_name = line.split("tool:")[1].strip()
                        return {
                            "type": "tool_call",
                            "tool_name": tool_name,
                            "parameters": {}
                        }
            
            # Check for completion
            if "task complete" in response_content.lower() or "finished" in response_content.lower():
                return {
                    "type": "completion",
                    "message": "Task completed successfully"
                }
            
            # Default to no action
            return {"type": "none", "message": "No clear action identified"}
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"Failed to parse action: {str(e)}",
                "response_content": response_content
            }
```

---

## 🔄 **ENHANCED AGENT CLASS (UPGRADE INTEGRATION)**

### **Self-Aware Agent Implementation**

**Upgrade 3 Integration**: Enhanced Agent with self-awareness capabilities

```python
class SelfAwareAgent(Agent):
    """Enhanced agent with self-awareness and continuous improvement"""
    
    def __init__(self, llm_client, system_prompt, tools, max_steps=50, workspace_dir="./workspace", token_limit=200000):
        super().__init__(llm_client, system_prompt, tools, max_steps, workspace_dir, token_limit)
        
        # Initialize self-awareness components
        self.self_awareness_enabled = self._check_self_awareness_config()
        if self.self_awareness_enabled:
            self.performance_monitor = SelfAwarePerformanceMonitor()
            self.behavior_adapter = AdaptiveBehaviorEngine()
            self.meta_cognitive = MetaCognitiveEngine()
            self.improvement_loop = SelfImprovementLoop(
                performance_monitor=self.performance_monitor,
                behavior_adapter=self.behavior_adapter,
                meta_cognitive=self.meta_cognitive
            )
        
        # Performance tracking
        self.execution_history = []
        self.capability_assessment = {}
        self.learning_patterns = {}
    
    def _check_self_awareness_config(self) -> bool:
        """Check if self-awareness features are enabled"""
        config = get_config()
        return config.self_awareness.get("enabled", False)
    
    async def run(self) -> str:
        """Enhanced run method with self-awareness"""
        
        if not self.self_awareness_enabled:
            return await super().run()  # Use existing behavior
        
        # Pre-execution: Meta-cognitive planning
        task_context = await self._extract_current_task_context()
        execution_plan = await self.meta_cognitive.create_execution_plan(task_context)
        
        # Track planning phase
        await self.performance_monitor.record_planning_phase(execution_plan)
        
        try:
            # Enhanced execution with adaptation
            result = await self._execute_with_adaptation(execution_plan)
            
            # Post-execution: Learning and reflection
            await self._reflect_and_learn(result)
            
            return result
            
        except Exception as e:
            # Enhanced error handling with learning
            await self._learn_from_error(e, execution_plan)
            raise
    
    async def _execute_with_adaptation(self, execution_plan: Dict) -> str:
        """Execute task with behavioral adaptation"""
        
        adapted_plan = await self.behavior_adapter.adapt_execution_plan(
            execution_plan, await self._get_current_context()
        )
        
        # Track adaptation decisions
        await self.performance_monitor.record_adaptation_decisions(adapted_plan)
        
        # Execute adapted plan
        original_run = super().run  # Reference to original method
        result = await original_run()
        
        # Analyze execution effectiveness
        effectiveness = await self.behavior_adapter.analyze_execution_effectiveness(
            adapted_plan, result
        )
        
        await self.performance_monitor.record_execution_effectiveness(effectiveness)
        
        return result
    
    async def _reflect_and_learn(self, execution_result: str):
        """Post-execution reflection and learning"""
        
        # Meta-cognitive reflection
        reflection = await self.meta_cognitive.reflect_on_execution({
            "result": execution_result,
            "plan": execution_result,  # This would be the actual plan
            "steps_taken": self.current_step,
            "tools_used": await self._get_tools_used()
        })
        
        # Learning from execution
        learning_insights = await self.improvement_loop.integrated_learning_cycle(
            execution_result, reflection
        )
        
        # Update capability assessment
        await self._update_capability_assessment(learning_insights)
        
        # Store learning for future use
        await self._store_learning_patterns(learning_insights)
    
    async def _extract_current_task_context(self) -> str:
        """Extract current task context for self-awareness"""
        
        if not self.messages:
            return "No current task"
        
        # Find most recent user message
        for msg in reversed(self.messages):
            if msg.role == "user":
                return msg.content[:500]  # Truncate for analysis
        
        return "General interaction"
    
    async def _get_current_context(self) -> Dict:
        """Get current execution context"""
        
        return {
            "workspace_state": self._get_workspace_state(),
            "tool_effectiveness": await self._get_tool_effectiveness(),
            "session_progress": self.current_step / self.max_steps,
            "recent_failures": self.failed_tasks,
            "capability_assessment": self.capability_assessment
        }
    
    async def _get_tool_effectiveness(self) -> Dict:
        """Get current tool effectiveness metrics"""
        
        if not self.self_awareness_enabled:
            return {}
        
        return await self.performance_monitor.get_current_tool_effectiveness()
    
    async def _update_capability_assessment(self, learning_insights: Dict):
        """Update agent's capability assessment based on learning"""
        
        for capability, assessment in learning_insights.get("capability_updates", {}).items():
            if capability not in self.capability_assessment:
                self.capability_assessment[capability] = {}
            
            self.capability_assessment[capability].update(assessment)
        
        # Store updated assessment
        await self.performance_monitor.update_capability_assessment(self.capability_assessment)
```

---

## 🔗 **LLM CLIENT INTEGRATION PATTERNS**

### **Pattern 1: Multi-Provider Support**

```python
class UnifiedLLMClient:
    """Unified client supporting multiple LLM providers"""
    
    SUPPORTED_PROVIDERS = {
        "anthropic": {
            "client_class": AnthropicClient,
            "protocol": "anthropic",
            "models": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "MiniMax-M2"]
        },
        "openai": {
            "client_class": OpenAIClient,
            "protocol": "openai", 
            "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        }
    }
    
    @classmethod
    def create_client(cls, provider: str, model: str, api_key: str, api_base: str) -> "UnifiedLLMClient":
        """Create appropriate client based on provider"""
        
        if provider not in cls.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")
        
        provider_config = cls.SUPPORTED_PROVIDERS[provider]
        client_class = provider_config["client_class"]
        
        if model not in provider_config["models"]:
            raise ValueError(f"Unsupported model {model} for provider {provider}")
        
        return client_class(api_key, model, api_base)
```

### **Pattern 2: Tool-Enhanced Prompting**

```python
class ToolEnhancedPromptBuilder:
    """Build prompts with integrated tool information"""
    
    def __init__(self, agent: Agent):
        self.agent = agent
    
    async def build_execution_prompt(self, task_description: str) -> str:
        """Build execution prompt with tool enhancements"""
        
        # Base prompt structure
        base_prompt = f"""
Task: {task_description}

You are an AI agent with access to tools and capabilities.
Current step: {self.agent.current_step}/{self.agent.max_steps}

Available Tools:
{self._format_tools_for_prompt()}

Instructions:
1. Choose the most appropriate tool or action
2. Provide clear, step-by-step guidance
3. If the task is complete, say "Task completed: [summary]"

Available capabilities:
"""
        
        # Add tool capabilities
        tool_capabilities = await self._analyze_tool_capabilities()
        base_prompt += "\n".join(f"- {capability}" for capability in tool_capabilities)
        
        # Add context awareness
        if self.agent.self_awareness_enabled:
            context_info = await self._add_context_awareness()
            base_prompt += f"\n\nContext Awareness:\n{context_info}"
        
        return base_prompt
    
    async def _analyze_tool_capabilities(self) -> List[str]:
        """Analyze and list tool capabilities"""
        
        capabilities = []
        
        for tool_category, tools in self.agent.available_tools.items():
            for tool in tools:
                if hasattr(tool, 'description'):
                    # Parse capabilities from tool description
                    capabilities.extend(self._extract_capabilities_from_description(tool.description))
        
        return list(set(capabilities))  # Remove duplicates
    
    async def _add_context_awareness(self) -> str:
        """Add self-awareness context to prompt"""
        
        if not hasattr(self.agent, 'performance_monitor'):
            return "Self-awareness features disabled"
        
        # Get current performance context
        performance_context = await self.agent.performance_monitor.get_current_context()
        
        return f"""
- Most effective tools: {performance_context.get('effective_tools', [])}
- Recent performance: {performance_context.get('recent_performance', 'Unknown')}
- Capability strengths: {performance_context.get('strengths', [])}
- Areas for improvement: {performance_context.get('improvement_areas', [])}
"""
```

### **Pattern 3: Response Processing Enhancement**

```python
class EnhancedResponseProcessor:
    """Enhanced response processing with learning integration"""
    
    def __init__(self, agent: Agent):
        self.agent = agent
    
    async def process_llm_response(self, response: Dict) -> Dict:
        """Process LLM response with enhancement integration"""
        
        # Basic response processing
        processed_response = {
            "content": response["content"],
            "usage": response.get("usage", {}),
            "finish_reason": response.get("finish_reason", "unknown")
        }
        
        # Add enhancement if enabled
        if self.agent.self_awareness_enabled:
            # Analyze response for learning opportunities
            learning_analysis = await self._analyze_response_for_learning(response)
            processed_response["learning_analysis"] = learning_analysis
            
            # Enhance response based on performance history
            enhanced_response = await self._enhance_response_with_history(response)
            processed_response["enhanced_content"] = enhanced_response
        
        return processed_response
    
    async def _analyze_response_for_learning(self, response: Dict) -> Dict:
        """Analyze response for learning opportunities"""
        
        content = response["content"]
        
        analysis = {
            "complexity_score": self._calculate_complexity_score(content),
            "tool_suggestions": self._extract_tool_suggestions(content),
            "execution_strategy": self._identify_execution_strategy(content),
            "potential_improvements": self._suggest_improvements(content)
        }
        
        # Store analysis for learning
        if hasattr(self.agent, 'performance_monitor'):
            await self.agent.performance_monitor.record_response_analysis(analysis)
        
        return analysis
    
    async def _enhance_response_with_history(self, response: Dict) -> str:
        """Enhance response based on execution history"""
        
        # Get historical patterns
        patterns = await self._get_relevant_patterns(response["content"])
        
        if patterns:
            # Add contextual suggestions based on history
            enhancement = self._build_historical_enhancement(patterns)
            return f"{response['content']}\n\nContext: {enhancement}"
        
        return response["content"]
```

---

## 📊 **PROTOCOL PERFORMANCE & MONITORING**

### **Response Time Monitoring**

```python
class ProtocolPerformanceMonitor:
    """Monitor agent client protocol performance"""
    
    def __init__(self):
        self.metrics = {
            "llm_response_times": [],
            "prompt_building_times": [],
            "action_parsing_times": [],
            "execution_success_rates": []
        }
    
    async def measure_llm_performance(self, start_time: float, end_time: float, success: bool):
        """Measure LLM response performance"""
        
        response_time = end_time - start_time
        
        self.metrics["llm_response_times"].append(response_time)
        self.metrics["execution_success_rates"].append(1 if success else 0)
        
        # Calculate moving averages
        avg_response_time = sum(self.metrics["llm_response_times"]) / len(self.metrics["llm_response_times"])
        success_rate = sum(self.metrics["execution_success_rates"]) / len(self.metrics["execution_success_rates"])
        
        return {
            "current_response_time": response_time,
            "average_response_time": avg_response_time,
            "success_rate": success_rate,
            "total_requests": len(self.metrics["llm_response_times"])
        }
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for protocol"""
        
        if not self.metrics["llm_response_times"]:
            return {"status": "no_data"}
        
        response_times = self.metrics["llm_response_times"]
        
        return {
            "total_requests": len(response_times),
            "average_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "p95_response_time": self._calculate_percentile(response_times, 95),
            "success_rate": sum(self.metrics["execution_success_rates"]) / len(self.metrics["execution_success_rates"]),
            "error_rate": 1 - (sum(self.metrics["execution_success_rates"]) / len(self.metrics["execution_success_rates"]))
        }
```

### **Token Usage Tracking**

```python
class TokenUsageTracker:
    """Track token usage across agent execution"""
    
    def __init__(self, token_limit: int = 200000):
        self.token_limit = token_limit
        self.usage_history = []
        self.current_session_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    
    async def track_llm_usage(self, usage: Dict):
        """Track LLM token usage"""
        
        self.current_session_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
        self.current_session_usage["completion_tokens"] += usage.get("completion_tokens", 0)
        self.current_session_usage["total_tokens"] += usage.get("total_tokens", 0)
        
        # Store history for analysis
        self.usage_history.append({
            "timestamp": datetime.now().isoformat(),
            "usage": usage.copy(),
            "cumulative_usage": self.current_session_usage.copy()
        })
        
        # Check for potential overflow
        if self.current_session_usage["total_tokens"] > self.token_limit * 0.8:
            await self._trigger_token_management()
    
    async def _trigger_token_management(self):
        """Trigger token management when approaching limit"""
        
        # Suggest context summarization
        if self.current_session_usage["total_tokens"] > self.token_limit * 0.8:
            return {
                "action": "summarize_context",
                "reason": "Approaching token limit",
                "current_usage": self.current_session_usage["total_tokens"],
                "limit": self.token_limit
            }
        
        return None
    
    def get_usage_report(self) -> Dict:
        """Generate token usage report"""
        
        return {
            "session_summary": self.current_session_usage,
            "limit": self.token_limit,
            "usage_percentage": (self.current_session_usage["total_tokens"] / self.token_limit) * 100,
            "total_requests": len(self.usage_history),
            "average_tokens_per_request": (
                self.current_session_usage["total_tokens"] / max(len(self.usage_history), 1)
            ),
            "management_triggers": len([h for h in self.usage_history if h.get("management_action")])
        }
```

---

## 🚀 **INTEGRATION WITH UPGRADE SYSTEMS**

### **Upgrade 1: Memory Integration**

```python
class MemoryIntegratedAgent(SelfAwareAgent):
    """Agent with memory integration for better context"""
    
    async def prepare_execution_context(self) -> Dict:
        """Prepare context with memory integration"""
        
        base_context = await super()._get_current_context()
        
        # Add memory context if available
        if hasattr(self, 'memory_manager') and self.memory_manager:
            memory_context = await self.memory_manager.get_relevant_context(
                task_description=await self._extract_current_task(),
                project_context=await self.memory_manager.get_current_project_context()
            )
            base_context["memory_context"] = memory_context
        
        return base_context
    
    async def store_execution_learning(self, execution_data: Dict):
        """Store execution learning in memory system"""
        
        if hasattr(self, 'memory_manager') and self.memory_manager:
            await self.memory_manager.store_execution_pattern({
                "task_type": execution_data.get("task_type"),
                "tools_used": execution_data.get("tools_used"),
                "success": execution_data.get("success"),
                "performance_metrics": execution_data.get("performance"),
                "lessons_learned": execution_data.get("lessons")
            })
```

### **Upgrade 2: Web Intelligence Integration**

```python
class WebIntelligentAgent(MemoryIntegratedAgent):
    """Agent with web intelligence integration"""
    
    async def get_web_guidance(self, task_description: str) -> Dict:
        """Get web-based guidance for tasks"""
        
        if not hasattr(self, 'web_researcher') or not self.web_researcher:
            return {}
        
        # Get relevant web research
        web_guidance = await self.web_researcher.get_research_guidance(task_description)
        
        # Integrate with existing context
        current_context = await self.prepare_execution_context()
        current_context["web_guidance"] = web_guidance
        
        return current_context
    
    async def enhance_with_web_intelligence(self, response: str) -> str:
        """Enhance LLM response with web intelligence"""
        
        if not hasattr(self, 'web_researcher') or not self.web_researcher:
            return response
        
        # Extract potential research needs from response
        research_needs = await self._extract_research_needs(response)
        
        if research_needs:
            # Conduct research to enhance response
            research_results = await self.web_researcher.research_multiple_topics(research_needs)
            
            # Integrate research into response
            enhanced_response = await self._integrate_research_with_response(
                response, research_results
            )
            
            return enhanced_response
        
        return response
```

### **Upgrade 3: Complete Self-Aware Integration**

```python
class FullySelfAwareAgent(WebIntelligentAgent):
    """Fully integrated self-aware agent"""
    
    async def run(self) -> str:
        """Complete self-aware execution with all upgrades"""
        
        if not self.self_awareness_enabled:
            return await super().run()
        
        # Pre-execution: Meta-cognitive planning with all integrations
        task_context = await self._extract_current_task_context()
        
        # Get memory context
        memory_context = await self.get_memory_context(task_context) if hasattr(self, 'memory_manager') else {}
        
        # Get web guidance
        web_guidance = await self.get_web_guidance(task_context)
        
        # Create comprehensive execution plan
        comprehensive_plan = await self.meta_cognitive.create_comprehensive_plan({
            "task_context": task_context,
            "memory_context": memory_context,
            "web_guidance": web_guidance,
            "capability_assessment": self.capability_assessment,
            "learning_patterns": self.learning_patterns
        })
        
        # Execute with full adaptation
        result = await self._execute_with_full_adaptation(comprehensive_plan)
        
        # Complete learning cycle
        await self._complete_learning_cycle(result, comprehensive_plan)
        
        return result
    
    async def _complete_learning_cycle(self, result: str, plan: Dict):
        """Complete the full learning cycle across all systems"""
        
        # Memory learning
        if hasattr(self, 'memory_manager') and self.memory_manager:
            await self.memory_manager.integrate_execution_result(result, plan)
        
        # Web intelligence learning
        if hasattr(self, 'web_researcher') and self.web_researcher:
            await self.web_researcher.learn_from_execution(result, plan)
        
        # Self-awareness learning
        await self.improvement_loop.complete_integrated_learning_cycle(result, plan)
        
        # Update all capability assessments
        await self._update_all_capability_assessments(result, plan)
```

---

## 🎯 **SUCCESS CRITERIA & METRICS**

### **Protocol Success Metrics:**
- [ ] **LLM Integration**: Seamless MiniMax-M2 integration with proper prompting
- [ ] **Response Quality**: >90% response quality for standard tasks
- [ ] **Performance**: <5s average response time for complex reasoning
- [ ] **Reliability**: >99% uptime for LLM communication

### **Agent Success Metrics:**
- [ ] **Task Completion**: >85% task completion rate across diverse tasks
- [ ] **Tool Selection**: Intelligent tool selection based on context
- [ ] **Error Recovery**: Graceful handling of execution errors
- [ ] **Learning Integration**: Effective integration with all three upgrade systems

### **Enhancement Integration Success Metrics:**
- [ ] **Upgrade 1**: Memory integration improves context and learning
- [ ] **Upgrade 2**: Web intelligence enhances research and knowledge
- [ ] **Upgrade 3**: Self-awareness improves performance and adaptation
- [ ] **Cross-Integration**: All three upgrades work cohesively

### **Performance Success Metrics:**
- [ ] **Token Efficiency**: Optimal token usage within limits
- [ ] **Response Time**: Consistent performance under load
- [ ] **Scalability**: Maintains performance with increasing task complexity
- [ ] **Resource Usage**: Efficient CPU and memory utilization

---

**Bottom Line**: Agent Client Protocol provides the **intelligence foundation** that enables LLM communication, tool selection, and learning integration across all enhancement systems.

---

*Agent Client Protocol Documentation Complete: November 25, 2025*  
*Status: MiniMax-M2 Integration Operational with Enhancement Framework Ready*