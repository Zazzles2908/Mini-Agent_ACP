# Phase 1: Web Search Architecture Optimization - Implementation Plan

## 🎯 Executive Summary

**Goal**: Fix web search architecture to align with Mini-Agent's design patterns by properly implementing Z.AI MCP servers and integrating MiniMax Coding Plan MCP with web_search and understand_image capabilities.

**Current Issues:**
1. ❌ Z.AI MCP protocol mismatch (SSE vs JSON-RPC) causing fallback to Direct API
2. ❌ Duplicate web search functionality (MCP + Direct API in same tool)
3. ❌ MiniMax Coding Plan MCP not fully integrated
4. ❌ Inefficient quota usage due to fallback behavior

**Target Architecture:**
```
Mini-Agent
├── Z.AI MCP Servers (Remote HTTP)
│   ├── web-search-prime → webSearchPrime tool
│   └── web-reader → webReader tool
├── MiniMax Coding Plan MCP (Local)
│   ├── web_search → Web search capability
│   └── understand_image → Vision analysis
└── Unified web search experience (single workflow)
```

---

## 📋 Phase 1 Overview

**Status**: Ready for Implementation  
**Priority**: High  
**Estimated Time**: 2-3 hours  
**Dependencies**: ZAI_API_KEY, MINIMAX_API_KEY, MiniMax Coding Plan subscription

---

## 🔍 Current State Analysis

### **Problem 1: Z.AI MCP Protocol Mismatch**

**Current Implementation** (`mini_agent/tools/http_mcp_client.py`):
```python
async with session.post(
    self.mcp_search_endpoint,
    headers=headers,
    json=mcp_request,
    timeout=aiohttp.ClientTimeout(total=30)
) as response:
    if response.status == 200:
        result = await response.json()  # ❌ Assumes JSON response
```

**Actual Z.AI Behavior**:
- Returns `200` status code
- Content-Type: `text/event-stream` (Server-Sent Events)
- Not standard JSON-RPC format

**Error Result**:
```
Error: MCP search failed: 200, message='Attempt to decode JSON with unexpected mimetype: ''
```

**Root Cause**: Z.AI MCP endpoints use SSE streaming instead of single JSON responses.

---

### **Problem 2: Duplicate Functionality**

**Current Tool Architecture** (`mini_agent/tools/zai_web_tool.py`):
```python
class ZAIWebTool(Tool):
    async def _try_mcp_search(self, query: str, max_results: int):
        # Try MCP protocol first
        
    async def _try_direct_search(self, query: str, max_results: int):
        # Fallback to Direct API
```

**Issues:**
- Two complete implementations of web search in one tool
- Automatic fallback masks protocol issues
- Users don't know which method is being used
- Inefficient quota tracking

---

### **Problem 3: MiniMax Coding Plan MCP Underutilized**

**Current Configuration** (`mini_agent/config/.mcp.json`):
```json
{
  "minimax-coding-plan": {
    "description": "MiniMax Coding Plan - AI-powered coding assistance...",
    "command": "python",
    "args": ["scripts/mcp_servers/minimax_coding_plan_mcp_server.py"],
    "disabled": false
  }
}
```

**Available but Not Exposed**:
- ✅ Server configured and running
- ❌ `web_search` tool capability not documented
- ❌ `understand_image` tool capability not documented
- ❌ Not integrated with web search workflow

**According to MiniMax Documentation**:
- Global Host: `https://api.minimax.io`
- Available Tools:
  - `web_search`: Performs web searches, returns organic results
  - `understand_image`: Analyzes images with AI, extracts information

---

## 🛠️ Solution Architecture

### **Target State: Clean Hybrid MCP Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                       Mini-Agent                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │         Web Search Orchestration Layer           │      │
│  │  (Intelligent routing based on use case)         │      │
│  └──────────────────┬───────────────────────────────┘      │
│                     │                                       │
│         ┌───────────┴───────────┐                          │
│         ▼                       ▼                          │
│  ┌─────────────┐         ┌─────────────┐                  │
│  │ Z.AI MCP    │         │ MiniMax MCP │                  │
│  │ (Remote)    │         │ (Local)     │                  │
│  ├─────────────┤         ├─────────────┤                  │
│  │ webSearch   │         │ web_search  │                  │
│  │ webReader   │         │ understand_ │                  │
│  │             │         │   image     │                  │
│  └─────────────┘         └─────────────┘                  │
│       SSE                     JSON-RPC                     │
│   (100 searches)           (Coding Plan)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Implementation Steps

### **Step 1: Fix Z.AI MCP SSE Protocol** ⏱️ 45 minutes

**Task**: Update HTTP MCP client to handle Server-Sent Events properly.

**File to Modify**: `mini_agent/tools/http_mcp_client.py`

**Changes Required**:

1. **Add SSE parsing capability**:
```python
async def _parse_sse_response(self, response):
    """Parse Server-Sent Events response from Z.AI MCP endpoint."""
    messages = []
    async for line in response.content:
        line = line.decode('utf-8').strip()
        if line.startswith('data: '):
            try:
                data = json.loads(line[6:])  # Remove 'data: ' prefix
                messages.append(data)
            except json.JSONDecodeError:
                continue
    return messages
```

2. **Update request handling**:
```python
async with session.post(
    self.url,
    headers=headers,
    json=request_data,
    timeout=aiohttp.ClientTimeout(total=self.timeout)
) as response:
    if response.status == 200:
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        
        if 'text/event-stream' in content_type:
            # Parse SSE response
            messages = await self._parse_sse_response(response)
            return self._format_sse_result(messages)
        else:
            # Standard JSON response
            result = await response.json()
            return result
```

3. **Add result formatting**:
```python
def _format_sse_result(self, messages):
    """Format SSE messages into tool result."""
    # Extract actual search results from SSE stream
    for msg in messages:
        if 'result' in msg:
            return msg['result']
    return messages[-1] if messages else {}
```

**Testing**:
```python
# Test Z.AI MCP with SSE handling
await http_client.call_tool("webSearchPrime", {"query": "test", "max_results": 3})
```

**Expected Result**: ✅ Z.AI MCP search works without falling back to Direct API

---

### **Step 2: Remove Direct API Fallback** ⏱️ 30 minutes

**Task**: Simplify ZAI web tool to use MCP only.

**File to Modify**: `mini_agent/tools/zai_web_tool.py`

**Changes Required**:

1. **Remove Direct API methods**:
```python
# DELETE: async def _try_direct_search(...)
# DELETE: self.direct_base_url = "..."
# DELETE: self.direct_available = None
```

2. **Simplify execute logic**:
```python
async def execute(self, **kwargs) -> ToolResult:
    """Execute web search using Z.AI MCP protocol only."""
    
    if not self.available:
        return ToolResult(
            success=False,
            content="",
            error="Z.AI web tool not available - no API key configured"
        )
    
    query = kwargs.get("query", "")
    max_results = kwargs.get("max_results", 3)
    include_reader = kwargs.get("include_reader", False)
    
    # Use MCP search (no fallback)
    search_result = await self._try_mcp_search(query, max_results)
    
    if not search_result.get("success"):
        return ToolResult(
            success=False,
            content="",
            error=search_result.get("error", "MCP search failed")
        )
    
    # Handle reader if requested
    if include_reader:
        reader_result = await self._try_mcp_reader(...)
    
    return self._format_response(search_result, reader_result)
```

3. **Update tool description**:
```python
@property
def description(self) -> str:
    return (
        "Z.AI web search using MCP protocol with FREE quotas (100 searches + 100 readers). "
        "Provides detailed search results with source citations. "
        "Use for: research, fact-checking, current information needs."
    )
```

**Testing**:
```python
# Test simplified tool
result = await zai_tool.execute(query="Mini-Agent architecture", max_results=3)
assert result.success == True
assert "Method: MCP" in result.content
```

**Expected Result**: ✅ Single, clean web search implementation using MCP only

---

### **Step 3: Document MiniMax Coding Plan MCP Tools** ⏱️ 20 minutes

**Task**: Create comprehensive documentation for MiniMax MCP capabilities.

**File to Create**: `documents/13_ADDITIONAL_UPGRADES/PHASE_1_WEB_SEARCH/MINIMAX_CODING_PLAN_MCP.md`

**Content** (see separate file for full documentation)

**Key Points to Document**:
- Global API host: `https://api.minimax.io`
- Available tools: `web_search`, `understand_image`
- Usage examples and parameters
- Integration with Mini-Agent workflow
- Quota and cost information

---

### **Step 4: Update MCP Configuration** ⏱️ 15 minutes

**Task**: Enhance MCP server descriptions and ensure proper environment variables.

**File to Modify**: `mini_agent/config/.mcp.json`

**Changes Required**:

```json
{
  "mcpServers": {
    "zai-web-search": {
      "description": "Z.AI Web Search - FREE web search using MCP protocol (100 searches/day quota)",
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {
        "Authorization": "Bearer ${ZAI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
      },
      "timeout": 30,
      "retry": {
        "max_retries": 3,
        "initial_delay": 1.0
      },
      "disabled": false
    },
    "zai-web-reader": {
      "description": "Z.AI Web Reader - FREE web content extraction using MCP protocol (100 reads/day quota)",
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_reader_prime/mcp",
      "headers": {
        "Authorization": "Bearer ${ZAI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
      },
      "timeout": 45,
      "retry": {
        "max_retries": 3,
        "initial_delay": 2.0
      },
      "disabled": false
    },
    "minimax-coding-plan": {
      "description": "MiniMax Coding Plan MCP - AI coding assistance with web_search and understand_image tools",
      "command": "python",
      "args": ["scripts/mcp_servers/minimax_coding_plan_mcp_server.py"],
      "env": {
        "MINIMAX_API_KEY": "${MINIMAX_API_KEY}",
        "MINIMAX_API_BASE": "https://api.minimax.io"
      },
      "disabled": false
    }
  }
}
```

**Testing**:
```bash
# Verify configuration loads
python -c "import json; print(json.load(open('mini_agent/config/.mcp.json'))['mcpServers'].keys())"
```

---

### **Step 5: Create Web Search Orchestration** ⏱️ 30 minutes

**Task**: Build intelligent routing layer that chooses appropriate search tool.

**File to Create**: `mini_agent/tools/web_search_orchestrator.py`

**Implementation**:

```python
"""Web Search Orchestration Layer
Routes search requests to appropriate MCP server based on use case.
"""

from typing import Any, Dict
from .base import Tool, ToolResult

class WebSearchOrchestrator(Tool):
    """
    Intelligent web search routing between Z.AI and MiniMax MCPs.
    
    Routing Logic:
    - General web search → Z.AI MCP (FREE quota, optimized for search)
    - Coding-related search → MiniMax Coding Plan MCP (specialized for dev)
    - Image understanding → MiniMax Coding Plan MCP (understand_image)
    """
    
    def __init__(self, zai_tool, minimax_tool):
        self.zai_tool = zai_tool
        self.minimax_tool = minimax_tool
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return (
            "Intelligent web search with automatic routing: "
            "Uses Z.AI MCP for general searches (FREE 100/day quota), "
            "or MiniMax Coding Plan MCP for coding-specific searches. "
            "Supports image understanding via understand_image tool."
        )
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["general", "coding", "image"],
                    "default": "general",
                    "description": "Type of search: general, coding, or image"
                },
                "max_results": {
                    "type": "integer",
                    "default": 3,
                    "description": "Maximum results (1-5)"
                },
                "image_url": {
                    "type": "string",
                    "description": "Image URL (required for image search type)"
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, **kwargs) -> ToolResult:
        """Route search to appropriate MCP server."""
        
        search_type = kwargs.get("search_type", "general")
        query = kwargs.get("query", "")
        
        if not query:
            return ToolResult(
                success=False,
                content="",
                error="Query parameter required"
            )
        
        # Route based on search type
        if search_type == "image":
            return await self._handle_image_search(kwargs)
        elif search_type == "coding":
            return await self._handle_coding_search(kwargs)
        else:
            return await self._handle_general_search(kwargs)
    
    async def _handle_general_search(self, kwargs) -> ToolResult:
        """Use Z.AI MCP for general web search."""
        return await self.zai_tool.execute(**kwargs)
    
    async def _handle_coding_search(self, kwargs) -> ToolResult:
        """Use MiniMax Coding Plan MCP for coding searches."""
        # Call minimax web_search tool
        result = await self.minimax_tool.call_tool(
            "web_search",
            {"query": kwargs.get("query")}
        )
        return self._format_minimax_result(result)
    
    async def _handle_image_search(self, kwargs) -> ToolResult:
        """Use MiniMax understand_image tool."""
        image_url = kwargs.get("image_url")
        if not image_url:
            return ToolResult(
                success=False,
                content="",
                error="image_url required for image search type"
            )
        
        result = await self.minimax_tool.call_tool(
            "understand_image",
            {
                "image_url": image_url,
                "prompt": kwargs.get("query")
            }
        )
        return self._format_minimax_result(result)
    
    def _format_minimax_result(self, result) -> ToolResult:
        """Format MiniMax MCP result."""
        # Extract content from MCP response
        content_parts = []
        for item in result.content:
            if hasattr(item, 'text'):
                content_parts.append(item.text)
        
        return ToolResult(
            success=not result.isError if hasattr(result, 'isError') else True,
            content='\n'.join(content_parts),
            metadata={"source": "minimax_coding_plan"}
        )
```

**Testing**:
```python
# Test routing logic
orchestrator = WebSearchOrchestrator(zai_tool, minimax_tool)

# General search → Z.AI
result1 = await orchestrator.execute(query="latest news", search_type="general")

# Coding search → MiniMax
result2 = await orchestrator.execute(query="React hooks", search_type="coding")

# Image search → MiniMax
result3 = await orchestrator.execute(
    query="What's in this image?",
    search_type="image",
    image_url="https://example.com/image.jpg"
)
```

---

### **Step 6: Integration Testing** ⏱️ 30 minutes

**Task**: Comprehensive testing of new web search architecture.

**Test Script** (`tests/test_phase1_web_search.py`):

```python
"""Phase 1 Web Search Architecture Tests"""

import asyncio
import pytest
from mini_agent.tools.http_mcp_client import HTTPMCPClient
from mini_agent.tools.zai_web_tool import ZAIWebTool
from mini_agent.tools.web_search_orchestrator import WebSearchOrchestrator

@pytest.mark.asyncio
async def test_zai_mcp_sse_handling():
    """Test Z.AI MCP Server-Sent Events handling."""
    client = HTTPMCPClient({
        "name": "zai-web-search",
        "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('ZAI_API_KEY')}"},
        "timeout": 30
    })
    
    result = await client.call_tool("webSearchPrime", {
        "query": "Mini-Agent architecture",
        "max_results": 3
    })
    
    assert result is not None
    assert "error" not in result
    print("✅ Z.AI MCP SSE handling works")

@pytest.mark.asyncio
async def test_zai_tool_no_fallback():
    """Test ZAI tool uses MCP only (no Direct API fallback)."""
    tool = ZAIWebTool()
    
    result = await tool.execute(query="test search", max_results=2)
    
    assert result.success == True
    assert "Method: MCP" in result.content or "mcp" in result.content.lower()
    assert "Direct API" not in result.content
    print("✅ ZAI tool uses MCP only")

@pytest.mark.asyncio
async def test_minimax_web_search():
    """Test MiniMax Coding Plan web_search tool."""
    # Load MCP connection
    from mini_agent.tools.mcp_loader import load_mcp_tools_async
    tools = await load_mcp_tools_async()
    
    minimax_tools = [t for t in tools if "minimax" in t.name.lower()]
    web_search = next((t for t in minimax_tools if "web_search" in t.name), None)
    
    assert web_search is not None, "MiniMax web_search tool not found"
    
    result = await web_search.execute(query="Python async programming")
    assert result.success == True
    print("✅ MiniMax web_search works")

@pytest.mark.asyncio
async def test_orchestrator_routing():
    """Test web search orchestrator routing logic."""
    zai_tool = ZAIWebTool()
    # minimax_tool = ... (get from MCP loader)
    
    orchestrator = WebSearchOrchestrator(zai_tool, minimax_tool)
    
    # Test general search routing
    result1 = await orchestrator.execute(
        query="news today",
        search_type="general"
    )
    assert result1.success == True
    
    # Test coding search routing
    result2 = await orchestrator.execute(
        query="React best practices",
        search_type="coding"
    )
    assert result2.success == True
    
    print("✅ Orchestrator routing works")

if __name__ == "__main__":
    asyncio.run(test_zai_mcp_sse_handling())
    asyncio.run(test_zai_tool_no_fallback())
    asyncio.run(test_minimax_web_search())
    asyncio.run(test_orchestrator_routing())
    print("\n🎉 All Phase 1 tests passed!")
```

**Run Tests**:
```bash
pytest tests/test_phase1_web_search.py -v
```

---

## 📊 Success Criteria

### **Phase 1 Complete When:**

- ✅ Z.AI MCP handles SSE protocol correctly (no JSON decode errors)
- ✅ No fallback to Direct API (MCP-only implementation)
- ✅ MiniMax Coding Plan MCP web_search and understand_image documented
- ✅ Web search orchestrator routes queries intelligently
- ✅ All tests passing
- ✅ Documentation updated
- ✅ Zero duplicate functionality

### **Metrics to Track:**

| Metric | Target | Actual |
|--------|--------|--------|
| Z.AI MCP Success Rate | >95% | ___ |
| MiniMax MCP Availability | 100% | ___ |
| Average Search Time | <5s | ___ |
| Quota Usage Accuracy | 100% | ___ |
| Zero Fallbacks to Direct API | Yes | ___ |

---

## 🚨 Rollback Plan

If Phase 1 implementation fails:

1. **Revert to previous state**:
```bash
git checkout HEAD~1 mini_agent/tools/http_mcp_client.py
git checkout HEAD~1 mini_agent/tools/zai_web_tool.py
```

2. **Disable new orchestrator**:
```python
# In mini_agent/cli.py
# tools.append(WebSearchOrchestrator(...))  # Comment out
```

3. **Keep existing fallback behavior** until issues resolved

---

## 📝 Next Steps After Phase 1

Once Phase 1 is complete:
1. Update `documents/01_OVERVIEW/AGENT_HANDOFF.md`
2. Begin Phase 2 (Supabase integration)
3. Monitor web search usage patterns
4. Gather user feedback on search quality

---

## 📚 References

- [Z.AI MCP Documentation](https://docs.z.ai/devpack/mcp/search-mcp-server)
- [MiniMax Coding Plan MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

---

*Last Updated: November 24, 2025*
