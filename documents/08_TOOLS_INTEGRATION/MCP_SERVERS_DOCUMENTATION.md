# 🔌 MCP Servers Architecture & Integration
## Mini-Agent Model Context Protocol (MCP) Infrastructure

**Date**: November 25, 2025  
**Component**: MCP Servers for External Service Integration  
**Status**: 6 Servers Operational (1 Pending Database Migration)

---

## 🎯 **MCP ARCHITECTURE OVERVIEW**

### **MCP Protocol in Mini-Agent**

**Model Context Protocol (MCP)** is the communication standard that allows Mini-Agent to interact with external services and tools through a unified interface.

```
┌─────────────────────────────────────────────────────────────┐
│                    Mini-Agent Agent                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Tool      │ │  Enhanced   │ │    Base     │            │
│  │ Classes     │ │   Tools     │ │    Tools    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 MCP Client Layer                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ HTTP Client │ │ SSE Handler │ │  Protocol   │            │
│  │             │ │             │ │   Parser    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                MCP Servers (6 Total)                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Memory    │ │     Git     │ │    Z.AI     │            │
│  │   (Local)   │ │   (Local)   │ │  (Remote)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ MiniMax     │ │ Supabase    │ │   Custom    │            │
│  │   (Local)   │ │  (Local)    │ │   (Local)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 **CURRENT MCP SERVER INVENTORY**

### **6 MCP Servers Configured and Ready**

| Server | Type | Status | Tools | Purpose |
|--------|------|--------|-------|---------|
| **memory** | Local | ✅ Operational | 9 tools | Knowledge graph memory |
| **git** | Local | ✅ Operational | 12 tools | Version control |
| **zai-web-search** | Remote | ✅ Operational | 1 tool | FREE web search |
| **zai-web-reader** | Remote | ✅ Operational | 1 tool | FREE web content extraction |
| **minimax-coding-plan** | Local | ✅ Operational | 4 tools | AI coding assistance |
| **supabase-admin** | Local | ⏳ Pending Migration | 4 tools | Database operations |

**Total Tools Available**: **31 MCP tools** across all servers

---

## ⚙️ **MCP CONFIGURATION**

### **Configuration File**: `mini_agent/config/.mcp.json`

```json
{
  "mcpServers": {
    "memory": {
      "description": "Memory - Knowledge graph memory system (long-term memory based on graph database)",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "disabled": false
    },
    "git": {
      "description": "Git - Git repository operations and version control", 
      "command": "python",
      "args": ["-m", "mcp_server_git"],
      "env": {},
      "disabled": false
    },
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
      "description": "MiniMax Coding Plan - AI coding assistance with web_search and understand_image tools",
      "command": "python",
      "args": ["scripts/mcp_servers/minimax_coding_plan_mcp_server.py"],
      "env": {
        "MINIMAX_API_KEY": "${MINIMAX_API_KEY}",
        "MINIMAX_API_BASE": "https://api.minimax.io"
      },
      "disabled": false
    },
    "supabase-admin": {
      "description": "Supabase Admin MCP - Full database control for Mini-Agent's long-term memory and project storage",
      "command": "python",
      "args": ["scripts/mcp_servers/supabase_admin_mcp_server.py"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_SERVICE_KEY": "${SUPABASE_SERVICE_KEY}",
        "SUPABASE_ADMIN_TOKEN": "${SUPABASE_ADMIN_TOKEN}"
      },
      "disabled": false
    }
  }
}
```

---

## 🔍 **INDIVIDUAL MCP SERVER DETAILS**

### **1. Memory MCP Server**
**Type**: Local (npm package)  
**Status**: ✅ Operational  
**Purpose**: Knowledge graph memory system

**Implementation:**
```bash
# Command: npx -y @modelcontextprotocol/server-memory
# Tools: 9 knowledge graph operations
```

**Available Tools:**
- `create_node` - Create knowledge graph nodes
- `get_node` - Retrieve knowledge graph nodes  
- `update_node` - Update existing nodes
- `delete_node` - Remove nodes from graph
- `create_relation` - Create node relationships
- `get_related_nodes` - Find connected nodes
- `search_nodes` - Query nodes by content
- `create_session` - Create memory sessions
- `get_session` - Retrieve session data

**Integration with Upgrades:**
- **Upgrade 1**: Cross-session knowledge building
- **Upgrade 2**: Web research knowledge integration
- **Upgrade 3**: Learning pattern storage

### **2. Git MCP Server**
**Type**: Local (Python module)  
**Status**: ✅ Operational  
**Purpose**: Git repository operations and version control

**Implementation:**
```bash
# Command: python -m mcp_server_git
# Tools: 12 version control operations
```

**Available Tools:**
- `git_status` - Repository status
- `git_diff` - Show file changes
- `git_log` - Commit history
- `git_branch` - Branch management
- `git_checkout` - Switch branches
- `git_add` - Stage changes
- `git_commit` - Create commits
- `git_reset` - Reset changes
- `git_show` - Show commit details
- `git_create_branch` - Create new branches
- `git_merge` - Merge branches
- `git_push` - Push to remote

**Integration with Upgrades:**
- **Upgrade 1**: Project versioning and backup
- **Upgrade 3**: Development pattern analysis

### **3. Z.AI Web Search MCP Server**
**Type**: Remote (HTTP/SSE)  
**Status**: ✅ Operational  
**Purpose**: FREE web search (100 searches/day quota)

**Implementation:**
```json
{
  "command": "remote",
  "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
  "headers": {
    "Authorization": "Bearer ${ZAI_API_KEY}"
  },
  "timeout": 30,
  "retry": {"max_retries": 3, "initial_delay": 1.0}
}
```

**Available Tools:**
- `web_search_prime` - Comprehensive web search

**Features:**
- **FREE Quota**: 100 searches per month
- **SSE Protocol**: Server-sent events for real-time responses
- **Credit Protection**: Automatic quota monitoring
- **Intelligent Fallback**: Graceful degradation when quota exhausted

**Integration with Upgrades:**
- **Upgrade 2**: Research orchestration
- **Upgrade 3**: Research pattern learning

### **4. Z.AI Web Reader MCP Server**
**Type**: Remote (HTTP/SSE)  
**Status**: ✅ Operational  
**Purpose**: FREE web content extraction (100 reads/day quota)

**Implementation:**
```json
{
  "command": "remote", 
  "url": "https://api.z.ai/api/mcp/web_reader_prime/mcp",
  "headers": {
    "Authorization": "Bearer ${ZAI_API_KEY}"
  },
  "timeout": 45,
  "retry": {"max_retries": 3, "initial_delay": 2.0}
}
```

**Available Tools:**
- `web_reader_prime` - Extract content from web pages

**Features:**
- **FREE Quota**: 100 reads per month
- **SSE Protocol**: Real-time content extraction
- **Content Parsing**: Extract readable text from web pages
- **Source Validation**: Basic content verification

**Integration with Upgrades:**
- **Upgrade 2**: Content extraction and validation
- **Upgrade 3**: Reading pattern analysis

### **5. MiniMax Coding Plan MCP Server**
**Type**: Local (Python script)  
**Status**: ✅ Operational  
**Purpose**: AI coding assistance and development planning

**Implementation:**
```python
# File: scripts/mcp_servers/minimax_coding_plan_mcp_server.py (400+ lines)
# Command: python scripts/mcp_servers/minimax_coding_plan_mcp_server.py
# Environment: MiniMax API integration
```

**Available Tools:**
- `coding_plan` - Generate development plans
- `code_review` - Review code for improvements
- `architecture_design` - System architecture planning
- `technical_research` - Research technical solutions

**Features:**
- **MiniMax Integration**: Uses MiniMax-M2 for AI assistance
- **Development Planning**: Structured approach to coding tasks
- **Architecture Design**: System design capabilities
- **Code Review**: Quality assessment and suggestions

**Integration with Upgrades:**
- **All Upgrades**: General AI assistance for implementation

### **6. Supabase Admin MCP Server**
**Type**: Local (Python script)  
**Status**: ⏳ Pending Database Migration  
**Purpose**: Full database control for Mini-Agent memory and storage

**Implementation:**
```python
# File: scripts/mcp_servers/supabase_admin_mcp_server.py (400+ lines)
# Command: python scripts/mcp_servers/supabase_admin_mcp_server.py
# Database: 6 tables in PostgreSQL
```

**Available Tools:**
- `execute_sql` - Raw SQL execution with admin access
- `table_operation` - CRUD operations (select, insert, update, delete, upsert)
- `project_memory` - Project-level context management
- `session_memory` - Conversation history management

**Features:**
- **Database Schema**: 6 tables designed for Mini-Agent
- **Admin Access**: Full database control
- **CRUD Operations**: Standard database operations
- **Context Management**: Project and session context

**Integration with Upgrades:**
- **Upgrade 1**: Memory enhancement and project context
- **Upgrade 2**: Knowledge graph and research storage
- **Upgrade 3**: Performance analytics and learning storage

---

## 🔧 **MCP CLIENT ARCHITECTURE**

### **HTTP Client Implementation**

**File**: `mini_agent/tools/http_mcp_client.py`

**Key Features:**
- **SSE Support**: Handles Server-Sent Events for real-time responses
- **Error Handling**: Comprehensive retry logic and error recovery
- **Protocol Detection**: Automatically detects SSE vs JSON responses
- **Timeout Management**: Configurable timeouts per server
- **Authentication**: Automatic header injection for remote servers

**Critical Enhancement - SSE Protocol Fix:**
```python
def _parse_sse_response(self, response_text: str) -> Dict[str, Any]:
    """Parse Server-Sent Events response from Z.AI MCP servers"""
    lines = response_text.strip().split('\n')
    data_lines = [line for line in lines if line.startswith('data: ')]
    
    for line in data_lines:
        json_data = line[6:]  # Remove 'data: ' prefix
        
        # Handle end-of-stream marker
        if json_data.strip() == '[DONE]':
            continue
            
        try:
            parsed = json.loads(json_data)
            # Extract result or content from SSE message
            if 'result' in parsed:
                return parsed['result']
            elif 'content' in parsed:
                return parsed['content']
            else:
                return parsed
        except json.JSONDecodeError:
            continue
    
    return {"error": "No valid SSE data found"}
```

**Usage Pattern:**
```python
# Tool implementation
async def execute(self, query: str):
    # Call MCP server
    result = await self.mcp_client.call_tool("zai-web-search", {
        "query": query,
        "max_results": 5
    })
    
    # Process response
    if result.success:
        return self.format_search_results(result.data)
    else:
        raise ToolError(f"Search failed: {result.error}")
```

---

## 🔌 **MCP SERVER INTEGRATION PATTERNS**

### **Pattern 1: Direct Tool Integration**

**Example**: Z.AI Web Search Integration
```python
class ZAIWebTool(Tool):
    def __init__(self):
        self.mcp_client = MCPServerClient()
        
    async def execute(self, query: str, max_results: int = 5):
        result = await self.mcp_client.call_tool("zai-web-search", {
            "query": query,
            "max_results": max_results
        })
        return result.data
```

### **Pattern 2: Enhanced Tool Integration**

**Example**: Enhanced Memory Integration
```python
class EnhancedMemoryTool(Tool):
    def __init__(self, config: Config):
        self.config = config
        self.mcp_client = MCPServerClient()
        
    async def execute(self, operation: str, data: Dict):
        # Use Supabase Admin MCP server
        result = await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": operation,
            "table_name": "mini_agent_memory",
            "data": data
        })
        
        # Enhanced processing
        if self.config.memory.get("pattern_learning", False):
            await self._record_pattern(result, operation)
            
        return result.data
```

### **Pattern 3: Multi-Server Orchestration**

**Example**: Web Research with Memory Integration
```python
class WebResearchOrchestrator:
    def __init__(self):
        self.mcp_client = MCPServerClient()
        
    async def research_with_memory(self, query: str):
        # 1. Search web using Z.AI
        web_results = await self.mcp_client.call_tool("zai-web-search", {
            "query": query
        })
        
        # 2. Extract content using Z.AI Reader
        extracted_content = await self.mcp_client.call_tool("zai-web-reader", {
            "urls": [result["url"] for result in web_results["results"]]
        })
        
        # 3. Store in knowledge base using Supabase
        await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": "insert",
            "table_name": "mini_agent_knowledge",
            "data": {
                "entity_type": "research_topic",
                "content": extracted_content,
                "query": query
            }
        })
        
        return {"web_results": web_results, "knowledge_stored": True}
```

---

## 🚨 **MCP CONNECTION ISSUES & RESOLUTION**

### **Common Issues Identified & Resolved**

#### **Issue 1: Z.AI SSE Protocol Parsing**
**Problem**: MCP servers returning SSE format instead of JSON  
**Status**: ✅ **RESOLVED**  
**Solution**: Enhanced `_parse_sse_response()` method in HTTP client

```python
# Before: Response parsing failed
if response.headers.get('content-type') == 'text/event-stream':
    # Now properly handles SSE format
    return self._parse_sse_response(response_text)

# After: SSE parsing works correctly
data: {'choices': [{'message': {'content': 'Search results...'}]}}
```

#### **Issue 2: Authentication Header Configuration**
**Problem**: Missing or incorrect authorization headers  
**Status**: ✅ **RESOLVED**  
**Solution**: Automated header injection from environment variables

```json
{
  "headers": {
    "Authorization": "Bearer ${ZAI_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
  }
}
```

#### **Issue 3: Connection Timeout Management**
**Problem**: Long-running operations timing out  
**Status**: ✅ **RESOLVED**  
**Solution**: Per-server timeout configuration and retry logic

```json
{
  "timeout": 30,
  "retry": {
    "max_retries": 3,
    "initial_delay": 1.0
  }
}
```

---

## 📊 **MCP SERVER MONITORING**

### **Health Check System**

**Connection Testing:**
```python
async def check_mcp_server_health(server_name: str):
    """Test individual MCP server connectivity"""
    
    try:
        result = await mcp_client.call_tool(server_name, {
            "health_check": True
        })
        return {
            "server": server_name,
            "status": "healthy",
            "response_time": result.response_time,
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "server": server_name,
            "status": "unhealthy", 
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }
```

**Multi-Server Health Report:**
```python
async def get_all_mcp_health():
    """Get health status for all configured MCP servers"""
    
    servers = ["memory", "git", "zai-web-search", "zai-web-reader", 
               "minimax-coding-plan", "supabase-admin"]
    
    health_report = {}
    for server in servers:
        health_report[server] = await check_mcp_server_health(server)
    
    return {
        "overall_status": "operational" if all(
            h["status"] == "healthy" for h in health_report.values()
        ) else "degraded",
        "servers": health_report,
        "timestamp": datetime.now().isoformat()
    }
```

### **Performance Monitoring**

**Response Time Tracking:**
```python
class MCPPerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    async def track_request(self, server: str, operation: str, duration: float):
        """Track MCP request performance"""
        
        if server not in self.metrics:
            self.metrics[server] = {}
        
        if operation not in self.metrics[server]:
            self.metrics[server][operation] = []
        
        self.metrics[server][operation].append({
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
        
        # Alert on slow operations
        if duration > 10.0:  # 10 second threshold
            self._alert_slow_operation(server, operation, duration)
    
    def get_performance_summary(self):
        """Generate performance summary report"""
        
        summary = {}
        for server, operations in self.metrics.items():
            server_summary = {}
            for operation, requests in operations.items():
                durations = [r["duration"] for r in requests]
                server_summary[operation] = {
                    "avg_response_time": sum(durations) / len(durations),
                    "max_response_time": max(durations),
                    "min_response_time": min(durations),
                    "total_requests": len(durations)
                }
            summary[server] = server_summary
        
        return summary
```

---

## 🔄 **MCP SERVER LIFECYCLE MANAGEMENT**

### **Server Startup & Shutdown**

**Startup Process:**
```python
async def start_mcp_servers():
    """Initialize all configured MCP servers"""
    
    servers = load_mcp_config()
    
    for server_name, server_config in servers.items():
        try:
            if server_config["command"] == "remote":
                # Remote servers (Z.AI) don't need startup
                continue
            
            # Start local servers
            process = await start_local_mcp_server(server_name, server_config)
            server_processes[server_name] = process
            
            # Health check
            await asyncio.sleep(2)  # Wait for startup
            health = await check_mcp_server_health(server_name)
            
            if health["status"] == "healthy":
                print(f"✅ {server_name} MCP server started successfully")
            else:
                print(f"⚠️ {server_name} MCP server started but health check failed")
                
        except Exception as e:
            print(f"❌ Failed to start {server_name} MCP server: {e}")
```

**Graceful Shutdown:**
```python
async def shutdown_mcp_servers():
    """Gracefully shutdown all MCP servers"""
    
    for server_name, process in server_processes.items():
        try:
            print(f"🔄 Shutting down {server_name} MCP server...")
            
            # Send SIGTERM for graceful shutdown
            process.terminate()
            await asyncio.sleep(2)
            
            # Force kill if still running
            if not process.exited:
                process.kill()
                await process.wait()
            
            print(f"✅ {server_name} MCP server shut down successfully")
            
        except Exception as e:
            print(f"❌ Error shutting down {server_name}: {e}")
```

---

## 🛠️ **MCP SERVER DEVELOPMENT**

### **Creating Custom MCP Servers**

**Template for New MCP Server:**
```python
#!/usr/bin/env python3
"""
Custom MCP Server Template
"""

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, CallToolResult
import asyncio

app = Server("custom-mcp-server")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    
    return [
        Tool(
            name="custom_operation",
            description="Perform custom operation",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "First parameter"},
                    "param2": {"type": "integer", "description": "Second parameter"}
                },
                "required": ["param1"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool execution"""
    
    try:
        if name == "custom_operation":
            result = await custom_operation(
                arguments["param1"], 
                arguments.get("param2", 0)
            )
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Custom operation result: {result}"
                    }
                ]
            )
        else:
            return CallToolResult(
                isError=True,
                content=[{
                    "type": "text", 
                    "text": f"Unknown tool: {name}"
                }]
            )
            
    except Exception as e:
        return CallToolResult(
            isError=True,
            content=[{
                "type": "text",
                "text": f"Error executing {name}: {str(e)}"
            }]
        )

async def custom_operation(param1: str, param2: int):
    """Custom operation implementation"""
    
    # Your custom logic here
    await asyncio.sleep(0.1)  # Simulate work
    
    return f"Processed {param1} with value {param2}"

if __name__ == "__main__":
    import mcp.server.stdio
    import sys
    
    asyncio.run(mcp.server.stdio.run(
        app, 
        InitializationOptions(
            server_name="custom-mcp-server",
            server_version="1.0.0",
            capabilities=app.get_capabilities(
                notification_options=None,
                experimental_capabilities={}
            )
        )
    ))
```

**Configuration for Custom Server:**
```json
{
  "custom-mcp-server": {
    "description": "Custom MCP server for specific functionality",
    "command": "python",
    "args": ["path/to/custom_mcp_server.py"],
    "env": {
      "CUSTOM_CONFIG": "value"
    },
    "disabled": false
  }
}
```

---

## 📈 **MCP USAGE ANALYTICS**

### **Tool Usage Tracking**

**Usage Statistics:**
```python
async def track_mcp_usage():
    """Track usage statistics across all MCP servers"""
    
    usage_stats = {}
    
    for server_name in get_configured_servers():
        try:
            # Get usage from MCP server
            stats = await get_mcp_usage_stats(server_name)
            usage_stats[server_name] = stats
        except Exception as e:
            usage_stats[server_name] = {"error": str(e)}
    
    return {
        "total_servers": len(usage_stats),
        "operational_servers": sum(
            1 for stats in usage_stats.values() 
            if "error" not in stats
        ),
        "server_details": usage_stats,
        "timestamp": datetime.now().isoformat()
    }

# Usage patterns analysis
async def analyze_usage_patterns():
    """Analyze usage patterns for optimization"""
    
    patterns = {
        "most_used_servers": await get_most_used_servers(),
        "peak_usage_hours": await get_peak_usage_hours(),
        "average_response_times": await get_average_response_times(),
        "error_rates": await get_error_rates()
    }
    
    return patterns
```

---

## 🎯 **SUCCESS CRITERIA & METRICS**

### **Infrastructure Success Metrics:**
- [ ] **100% MCP Server Availability**: All 6 servers operational
- [ ] **<100ms Response Time**: Average across all MCP tools
- [ ] **99.9% Uptime**: Consistent server availability
- [ ] **Error Rate <1%**: Successful operation percentage

### **Integration Success Metrics:**
- [ ] **Enhancement Integration**: All 3 upgrades use MCP servers effectively
- [ ] **Cross-Server Orchestration**: Multiple servers work together seamlessly
- [ ] **Performance Optimization**: MCP usage enhances overall system performance
- [ ] **Reliability**: MCP failures don't break agent functionality

### **Development Success Metrics:**
- [ ] **Easy Extension**: New MCP servers can be added easily
- [ ] **Clear Documentation**: All servers well-documented
- [ ] **Health Monitoring**: Proactive issue detection and resolution
- [ ] **Resource Efficiency**: Optimal resource usage across servers

---

**Bottom Line**: MCP infrastructure provides the **extensibility foundation** for Mini-Agent enhancements while maintaining **reliability** and **performance**.

---

*MCP Servers Documentation Complete: November 25, 2025*  
*Status: 6 Servers Configured - 5 Operational, 1 Pending Database Migration*