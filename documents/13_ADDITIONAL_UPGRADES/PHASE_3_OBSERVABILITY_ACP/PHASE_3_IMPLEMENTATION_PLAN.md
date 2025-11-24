# Phase 3: Observability & Editor Integration - Implementation Plan

## 🎯 Executive Summary

**Status**: ⏸️ PAUSED - Awaiting Phase 1 & 2 Completion  
**Goal**: Integrate Langfuse for LLM observability/tracing and implement Agent Client Protocol (ACP) for Zed editor integration.

**Vision**: Transform Mini-Agent into a production-ready, multi-editor AI system with comprehensive monitoring, cost tracking, and performance analytics.

---

## 📋 Phase 3 Overview

**Status**: PAUSED  
**Priority**: Medium  
**Estimated Time**: 5-6 hours  
**Dependencies**: 
- 🔄 Phase 1 Complete (Web Search Architecture)
- 🔄 Phase 2 Complete (Supabase Integration)
- Langfuse account (cloud or self-hosted)
- Zed editor installed for testing

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Mini-Agent                               │
│               (Core Agent System)                           │
└───────────┬─────────────────────────────┬───────────────────┘
            │                             │
            ▼                             ▼
┌───────────────────────────┐  ┌──────────────────────────┐
│   Langfuse Integration    │  │   ACP Implementation     │
│   (Observability Layer)   │  │   (Editor Integration)   │
├───────────────────────────┤  ├──────────────────────────┤
│                           │  │                          │
│ • Trace all LLM calls     │  │ • Zed editor support     │
│ • Monitor token usage     │  │ • JetBrains compatible   │
│ • Track costs             │  │ • VS Code bridge         │
│ • Performance metrics     │  │ • Multi-editor protocol  │
│ • Error tracking          │  │ • Tool visibility        │
│ • User analytics          │  │ • Context sync           │
│                           │  │                          │
└───────────────────────────┘  └──────────────────────────┘
            │                             │
            ▼                             ▼
┌───────────────────────────────────────────────────────────┐
│              Langfuse Dashboard                           │
│  • Real-time traces    • Cost analysis                    │
│  • Performance graphs  • User sessions                    │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 Part A: Langfuse Integration

### **What is Langfuse?**

Langfuse is an open-source LLM observability platform providing:
- **Trace Collection**: Capture every LLM call with full context
- **Cost Tracking**: Monitor token usage and API costs
- **Performance Analytics**: Response times, error rates, success metrics
- **Session Management**: Group related traces by user/project
- **Prompt Management**: Version control for prompts
- **User Feedback**: Collect ratings and feedback on responses

### **Why Langfuse for Mini-Agent?**

| Feature | Benefit |
|---------|---------|
| **Open Source** | Self-host or use cloud, no vendor lock-in |
| **Python SDK** | Easy integration with Mini-Agent |
| **Real-time Monitoring** | Live dashboard for production usage |
| **Cost Optimization** | Identify expensive operations |
| **Debugging** | Trace failures back to specific calls |
| **Analytics** | Understand usage patterns |

---

### **Implementation Steps for Langfuse**

#### **Step 1: Setup Langfuse** ⏱️ 30 minutes

**Option A: Cloud (Easiest)**
```bash
# 1. Sign up at https://langfuse.com
# 2. Create new project
# 3. Get API keys (Public Key + Secret Key + Host URL)
```

**Option B: Self-Hosted (Full Control)**
```bash
# Docker Compose setup
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker-compose up -d

# Access at http://localhost:3000
```

**Environment Variables**:
```bash
# Add to .env
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com  # or http://localhost:3000
```

---

#### **Step 2: Install Langfuse SDK** ⏱️ 10 minutes

```bash
uv pip install langfuse
```

---

#### **Step 3: Create Langfuse Wrapper** ⏱️ 60 minutes

**File to Create**: `mini_agent/observability/langfuse_tracer.py`

```python
"""
Langfuse Integration for Mini-Agent
Provides comprehensive LLM observability and tracing.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from functools import wraps
import logging

from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

logger = logging.getLogger(__name__)

class LangfuseTracer:
    """
    Langfuse tracing wrapper for Mini-Agent.
    
    Automatically traces:
    - LLM API calls
    - Tool executions
    - Agent steps
    - Session context
    """
    
    def __init__(self):
        """Initialize Langfuse client."""
        self.enabled = False
        
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        
        if public_key and secret_key:
            try:
                self.client = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=host
                )
                self.enabled = True
                logger.info("Langfuse tracing enabled")
            except Exception as e:
                logger.warning(f"Langfuse initialization failed: {e}")
                self.client = None
        else:
            logger.info("Langfuse not configured (missing API keys)")
            self.client = None
    
    def create_trace(self, name: str, user_id: Optional[str] = None,
                     session_id: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None):
        """Create new trace for tracking execution."""
        if not self.enabled:
            return None
        
        try:
            trace = self.client.trace(
                name=name,
                user_id=user_id,
                session_id=session_id,
                metadata=metadata or {},
                timestamp=datetime.now()
            )
            return trace
        except Exception as e:
            logger.error(f"Failed to create trace: {e}")
            return None
    
    def create_generation(self, trace_id: str, name: str, model: str,
                         input_text: str, output_text: str,
                         usage: Optional[Dict[str, int]] = None,
                         metadata: Optional[Dict[str, Any]] = None):
        """Track LLM generation."""
        if not self.enabled:
            return
        
        try:
            self.client.generation(
                trace_id=trace_id,
                name=name,
                model=model,
                input=input_text,
                output=output_text,
                usage=usage or {},
                metadata=metadata or {},
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Failed to create generation: {e}")
    
    def create_span(self, trace_id: str, name: str, input_data: Any,
                   output_data: Any, metadata: Optional[Dict[str, Any]] = None):
        """Track tool execution or agent step."""
        if not self.enabled:
            return
        
        try:
            self.client.span(
                trace_id=trace_id,
                name=name,
                input=input_data,
                output=output_data,
                metadata=metadata or {},
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Failed to create span: {e}")
    
    def score_generation(self, trace_id: str, name: str, value: float,
                        comment: Optional[str] = None):
        """Add score/feedback to generation."""
        if not self.enabled:
            return
        
        try:
            self.client.score(
                trace_id=trace_id,
                name=name,
                value=value,
                comment=comment
            )
        except Exception as e:
            logger.error(f"Failed to add score: {e}")
    
    def flush(self):
        """Flush pending traces."""
        if self.enabled:
            self.client.flush()

# Global tracer instance
_tracer = None

def get_tracer() -> LangfuseTracer:
    """Get global Langfuse tracer instance."""
    global _tracer
    if _tracer is None:
        _tracer = LangfuseTracer()
    return _tracer

def trace_llm_call(func):
    """Decorator to trace LLM API calls."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tracer = get_tracer()
        
        if not tracer.enabled:
            return await func(*args, **kwargs)
        
        # Extract relevant info
        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        input_text = str(messages)
        
        # Create trace
        trace = tracer.create_trace(
            name=f"llm_call_{func.__name__}",
            metadata={"function": func.__name__, "model": model}
        )
        
        try:
            # Execute function
            result = await func(*args, **kwargs)
            
            # Track generation
            output_text = str(result.get("content", "")) if isinstance(result, dict) else str(result)
            usage = result.get("usage", {}) if isinstance(result, dict) else {}
            
            tracer.create_generation(
                trace_id=trace.id if trace else "unknown",
                name=func.__name__,
                model=model,
                input_text=input_text,
                output_text=output_text,
                usage=usage
            )
            
            return result
            
        except Exception as e:
            # Track error
            logger.error(f"LLM call failed: {e}")
            raise
        finally:
            tracer.flush()
    
    return wrapper

def trace_tool_execution(func):
    """Decorator to trace tool executions."""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        tracer = get_tracer()
        
        if not tracer.enabled:
            return await func(self, *args, **kwargs)
        
        # Create span for tool execution
        tool_name = self.name if hasattr(self, 'name') else func.__name__
        
        trace = tracer.create_trace(
            name=f"tool_{tool_name}",
            metadata={"tool": tool_name, "function": func.__name__}
        )
        
        try:
            result = await func(self, *args, **kwargs)
            
            tracer.create_span(
                trace_id=trace.id if trace else "unknown",
                name=tool_name,
                input_data={"args": args, "kwargs": kwargs},
                output_data={"result": str(result)[:500]},  # Truncate for readability
                metadata={"success": getattr(result, 'success', True)}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise
        finally:
            tracer.flush()
    
    return wrapper
```

---

#### **Step 4: Integrate with Agent** ⏱️ 45 minutes

**File to Modify**: `mini_agent/agent.py`

```python
from mini_agent.observability.langfuse_tracer import get_tracer, trace_llm_call

class Agent:
    def __init__(self, ...):
        # ... existing initialization ...
        
        # Initialize Langfuse tracer
        self.tracer = get_tracer()
        
        if self.tracer.enabled:
            logger.info("Langfuse observability enabled")
    
    @trace_llm_call
    async def _call_llm(self, messages: List[Dict[str, str]], **kwargs):
        """Call LLM with automatic tracing."""
        # Existing LLM call logic
        response = await self.client.create_completion(
            messages=messages,
            model=self.config.model,
            **kwargs
        )
        return response
    
    async def run(self, user_message: str):
        """Run agent with full observability."""
        
        # Create trace for entire agent run
        trace = self.tracer.create_trace(
            name="agent_run",
            session_id=self.session_id if hasattr(self, 'session_id') else None,
            metadata={
                "workspace": str(self.workspace_dir),
                "max_steps": self.max_steps
            }
        )
        
        try:
            # ... existing agent logic with LLM calls (automatically traced) ...
            
            result = await self._execute_agent_loop(user_message)
            
            return result
            
        finally:
            self.tracer.flush()
```

---

#### **Step 5: Dashboard & Analytics** ⏱️ 30 minutes

**Usage Examples**:

```python
# View traces in Langfuse dashboard
# 1. Navigate to https://cloud.langfuse.com (or your self-hosted URL)
# 2. Select your project
# 3. View traces in real-time

# Analyze costs
# - Go to "Analytics" tab
# - View token usage by model
# - Calculate costs based on provider pricing

# Monitor performance
# - Check average response times
# - Identify slow operations
# - Track error rates

# Session analysis
# - Group traces by session_id
# - View conversation flows
# - Analyze multi-turn interactions
```

---

## 🔌 Part B: Agent Client Protocol (ACP) Integration

### **What is ACP?**

Agent Client Protocol (ACP) is an open standard developed by Zed Industries that enables AI coding agents to integrate seamlessly with code editors.

**Key Features**:
- **Editor Agnostic**: Works with Zed, JetBrains, VS Code (via adapters)
- **Rich Context**: Access to editor state, file contents, selections
- **Tool Protocol**: Expose agent capabilities to editors
- **Bi-directional**: Editor can call agent, agent can modify editor
- **Open Standard**: No vendor lock-in, community-driven

### **Why ACP for Mini-Agent?**

| Feature | Benefit |
|---------|---------|
| **Multi-Editor Support** | One agent, multiple editors |
| **Deep Integration** | Direct access to editor state |
| **Standard Protocol** | Future-proof, widely adopted |
| **Tool Visibility** | Editors can discover agent capabilities |
| **Context Sync** | Editor and agent share state |

---

### **Implementation Steps for ACP**

#### **Step 1: Install ACP SDK** ⏱️ 10 minutes

```bash
uv pip install acpex  # Python ACP implementation
```

---

#### **Step 2: Create ACP Server** ⏱️ 90 minutes

**File to Create**: `mini_agent/editor_integration/acp_server.py`

```python
"""
Agent Client Protocol Server for Mini-Agent
Enables integration with Zed and other ACP-compatible editors.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional

from acpex import ACPServer, Tool, Resource, Context

logger = logging.getLogger(__name__)

class MiniAgentACPServer:
    """
    ACP server exposing Mini-Agent capabilities to editors.
    
    Provides:
    - Tool discovery (list available agent tools)
    - Tool execution (run tools from editor)
    - Context sharing (sync editor state with agent)
    - File operations (read/write from agent)
    """
    
    def __init__(self, agent):
        """Initialize ACP server with Mini-Agent instance."""
        self.agent = agent
        self.server = ACPServer(
            name="mini-agent",
            version="1.0.0",
            description="Mini-Agent: Comprehensive AI agent with 39+ tools"
        )
        
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """Register Mini-Agent tools as ACP tools."""
        
        # Register each Mini-Agent tool
        for tool in self.agent.tools:
            acp_tool = Tool(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters,
                handler=self._create_tool_handler(tool)
            )
            self.server.register_tool(acp_tool)
        
        logger.info(f"Registered {len(self.agent.tools)} tools with ACP server")
    
    def _create_tool_handler(self, tool):
        """Create async handler for tool execution."""
        async def handler(params: Dict[str, Any], context: Context) -> Dict[str, Any]:
            """Execute Mini-Agent tool and return result."""
            try:
                # Execute tool
                result = await tool.execute(**params)
                
                return {
                    "success": result.success,
                    "content": result.content,
                    "error": result.error,
                    "metadata": getattr(result, 'metadata', {})
                }
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                return {
                    "success": False,
                    "content": "",
                    "error": str(e)
                }
        
        return handler
    
    def _register_resources(self):
        """Register agent resources (files, context, etc.)."""
        
        # Workspace files resource
        workspace_resource = Resource(
            uri="workspace://",
            description="Access to workspace files",
            handler=self._workspace_resource_handler
        )
        self.server.register_resource(workspace_resource)
        
        # Agent context resource
        context_resource = Resource(
            uri="context://",
            description="Current agent context and state",
            handler=self._context_resource_handler
        )
        self.server.register_resource(context_resource)
    
    async def _workspace_resource_handler(self, uri: str) -> Dict[str, Any]:
        """Handle workspace resource requests."""
        # Parse URI to get file path
        file_path = uri.replace("workspace://", "")
        
        try:
            # Read file using agent's file tools
            content = await self.agent.read_file(file_path)
            
            return {
                "uri": uri,
                "content": content,
                "content_type": "text/plain"
            }
        except Exception as e:
            return {
                "uri": uri,
                "error": str(e)
            }
    
    async def _context_resource_handler(self, uri: str) -> Dict[str, Any]:
        """Handle agent context requests."""
        return {
            "uri": uri,
            "content": {
                "workspace": str(self.agent.workspace_dir),
                "session_id": getattr(self.agent, 'session_id', None),
                "step_count": getattr(self.agent, 'step_count', 0),
                "tools_available": len(self.agent.tools)
            },
            "content_type": "application/json"
        }
    
    async def start(self, host: str = "localhost", port: int = 8765):
        """Start ACP server."""
        logger.info(f"Starting ACP server on {host}:{port}")
        await self.server.serve(host=host, port=port)
    
    async def stop(self):
        """Stop ACP server."""
        await self.server.shutdown()
        logger.info("ACP server stopped")
```

---

#### **Step 3: Zed Editor Configuration** ⏱️ 20 minutes

**File to Create**: `~/.config/zed/agents/mini-agent.json`

```json
{
  "name": "Mini-Agent",
  "description": "Comprehensive AI agent with 39+ specialized tools",
  "connection": {
    "type": "websocket",
    "url": "ws://localhost:8765"
  },
  "capabilities": [
    "file_operations",
    "web_search",
    "code_analysis",
    "database_operations",
    "memory_management"
  ],
  "settings": {
    "auto_start": true,
    "log_level": "info"
  }
}
```

**Zed Settings** (`~/.config/zed/settings.json`):

```json
{
  "agents": {
    "enabled": true,
    "default_agent": "Mini-Agent",
    "agents": [
      "mini-agent"
    ]
  }
}
```

---

#### **Step 4: Launch Integration** ⏱️ 30 minutes

**File to Create**: `scripts/launch_with_acp.py`

```python
"""
Launch Mini-Agent with ACP server for editor integration.
"""

import asyncio
import logging
from mini_agent.cli import create_agent
from mini_agent.editor_integration.acp_server import MiniAgentACPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Launch Mini-Agent with ACP server."""
    
    # Create agent instance
    logger.info("Initializing Mini-Agent...")
    agent = await create_agent()
    
    # Create ACP server
    logger.info("Starting ACP server...")
    acp_server = MiniAgentACPServer(agent)
    
    # Start server
    await acp_server.start(host="localhost", port=8765)
    
    logger.info("Mini-Agent ACP server running. Open Zed editor to connect.")
    logger.info("Press Ctrl+C to stop.")
    
    try:
        # Keep running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await acp_server.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

**Usage**:
```bash
# Start Mini-Agent with ACP
python scripts/launch_with_acp.py

# Open Zed editor
# Mini-Agent will appear in agents panel
# Use CMD+K to invoke Mini-Agent in any file
```

---

## 📊 Success Criteria

### **Phase 3 Complete When:**

**Langfuse Integration**:
- ✅ Langfuse client initialized and connected
- ✅ All LLM calls automatically traced
- ✅ Tool executions tracked with spans
- ✅ Dashboard showing real-time traces
- ✅ Cost analytics available
- ✅ Performance metrics tracked
- ✅ Session grouping working

**ACP Integration**:
- ✅ ACP server running and connectable
- ✅ All Mini-Agent tools exposed via ACP
- ✅ Zed editor can discover and call tools
- ✅ Context sharing working
- ✅ File operations accessible
- ✅ Multi-editor compatibility tested

---

## 🚀 Future Enhancements (Post-Phase 3)

1. **Langfuse Advanced Features**:
   - Prompt management and versioning
   - A/B testing for different approaches
   - User feedback collection
   - Automated cost optimization

2. **ACP Expansion**:
   - JetBrains IDE support
   - VS Code bridge adapter
   - Custom editor extensions
   - Real-time collaboration

3. **Integration**:
   - Langfuse + Supabase (store traces in database)
   - ACP + Memory (sync editor state to memory)
   - Multi-agent orchestration via ACP

---

## 📚 References

- [Langfuse Documentation](https://langfuse.com/docs)
- [Agent Client Protocol Specification](https://zed.dev/acp)
- [Zed Editor](https://zed.dev)
- [ACPex Python Library](https://github.com/acpex/acpex-python)

---

*Last Updated: November 24, 2025*
*Status: PAUSED - Awaiting Phase 1 & 2 completion*
