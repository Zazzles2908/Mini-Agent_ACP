# MCP Refactoring Plan - Z.AI Native Integration

## **🎯 MISSION: Convert to MCP Architecture**

Instead of scattered direct API calls, we should use Z.AI's **native MCP ecosystem**.

## **Current Chaos vs MCP Solution**

### **❌ CURRENT STATE**
```
📁 mini_agent/tools/
  ├── simple_web_search.py      (direct API calls)
  ├── zai_unified_tools.py      (scattered)
  ├── file_tools.py             (separate)
  ├── bash_tool.py              (separate)
  └── ... (many scattered tools)
```

### **✅ MCP ARCHITECTURE**
```
📁 mcp-servers/
  ├── web-search-mcp/           (Native Z.AI MCP server)
  ├── document-reader-mcp/      (Z.AI reader integration)
  ├── file-management-mcp/      (File operations server)
  └── system-monitor-mcp/       (Health check server)

📁 mini_agent/
  ├── mcp-integration/          (Z.AI MCP client)
  └── mcp-client/              (Unified interface)
```

## **Step-by-Step MCP Migration**

### **Phase 1: MCP Infrastructure Setup**

#### **1. Install MCP Dependencies**
```bash
pip install mcp-server zai-mcp-client mcp-async-client
```

#### **2. Create MCP Server Structure**
```bash
mkdir -p mcp-servers/web-search-mcp
mkdir -p mcp-servers/document-reader-mcp  
mkdir -p mcp-servers/system-monitor-mcp
```

#### **3. Convert Web Search to MCP Server**

**Create:** `mcp-servers/web-search-mcp/server.py`
```python
#!/usr/bin/env python3
"""
Web Search MCP Server
====================
Converts our working web search into a proper MCP server.
"""

import asyncio
import logging
from mcp.server import MCPServer
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logger = logging.getLogger(__name__)

class WebSearchMCPServer(MCPServer):
    """MCP Server for web search functionality"""
    
    tools = [
        Tool(
            name="search_web",
            description="Search the web for information using Z.AI GLM-4.6",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    ]
    
    async def search_web(self, query: str, max_results: int = 5):
        """Implement web search using existing working code"""
        # Use our proven web search implementation
        from mini_agent.tools.simple_web_search import web_search
        
        result = await web_search(query, max_results)
        
        return TextContent(
            type="text",
            text=result['content']
        ) if result['success'] else None

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        server = WebSearchMCPServer()
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

#### **4. Create MCP Client Integration**

**Create:** `mini_agent/mcp-integration/client.py`
```python
#!/usr/bin/env python3
"""
Mini-Agent MCP Integration
=========================
Native Z.AI MCP client for Mini-Agent.
"""

import asyncio
import logging
from mcp.client import MCPSession
from mcp.client.stdio import stdio_client
from pathlib import Path

logger = logging.getLogger(__name__)

class MiniAgentMCPClient:
    def __init__(self):
        self.servers = {}
        self.enabled = True
    
    async def initialize_servers(self):
        """Initialize all MCP servers"""
        servers_config = {
            "web_search": "mcp-servers/web-search-mcp/server.py",
            "document_reader": "mcp-servers/document-reader-mcp/server.py",
            "system_monitor": "mcp-servers/system-monitor-mcp/server.py"
        }
        
        for server_name, server_path in servers_config.items():
            if Path(server_path).exists():
                try:
                    process = await stdio_client(["python", server_path])
                    self.servers[server_name] = process
                    logger.info(f"Connected to {server_name} MCP server")
                except Exception as e:
                    logger.error(f"Failed to connect to {server_name}: {e}")
    
    async def search_web(self, query: str, max_results: int = 5):
        """Search web using MCP server"""
        if "web_search" not in self.servers:
            raise RuntimeError("Web search MCP server not connected")
        
        server = self.servers["web_search"]
        result = await server.call_tool("search_web", {
            "query": query,
            "max_results": max_results
        })
        
        return result[0].text if result else None
    
    async def shutdown(self):
        """Shutdown all MCP servers"""
        for process in self.servers.values():
            process.close()
```

#### **5. Update Mini-Agent Tools System**

**Update:** `mini_agent/tools/__init__.py`
```python
# Add MCP integration
from ..mcp_integration.client import MiniAgentMCPClient

class MCPIntegratedTools:
    def __init__(self):
        self.mcp_client = None
    
    async def initialize(self):
        self.mcp_client = MiniAgentMCPClient()
        await self.mcp_client.initialize_servers()
    
    async def get_tools(self):
        """Return MCP-integrated tools"""
        return [
            {
                "name": "mcp_search_web",
                "description": "Search web using Z.AI MCP integration",
                "function": self.mcp_client.search_web if self.mcp_client else None
            }
        ]
```

### **Phase 2: Configuration Management**

**Update:** `mini_agent/config/config.yaml`
```yaml
# MCP Configuration
mcp:
  enabled: true
  zai_integration:
    enabled: true
    api_key: "${ZAI_API_KEY}"
    base_url: "https://api.z.ai"
  
  servers:
    web_search: "mcp-servers/web-search-mcp/server.py"
    document_reader: "mcp-servers/document-reader-mcp/server.py"
    system_monitor: "mcp-servers/system-monitor-mcp/server.py"
```

### **Phase 3: Testing & Validation**

#### **1. MCP Inspector Testing**
```bash
# Test each MCP server individually
mcp-inspector test mcp-servers/web-search-mcp/server.py
mcp-inspector test mcp-servers/document-reader-mcp/server.py
```

#### **2. Integration Testing**
```bash
# Test MCP client integration
python -c "
import asyncio
from mini_agent.mcp_integration.client import MiniAgentMCPClient

async def test_mcp_integration():
    client = MiniAgentMCPClient()
    await client.initialize_servers()
    result = await client.search_web('MCP server testing')
    print('MCP Result:', result[:200] + '...')
    await client.shutdown()

asyncio.run(test_mcp_integration())
"
```

### **Phase 4: Migration & Cleanup**

#### **1. Gradual Migration**
- Start with web search (most critical)
- Test end-to-end workflows
- Monitor Z.AI credit usage
- Validate performance

#### **2. Cleanup Phase**
- Remove scattered direct API tools
- Update documentation
- Update system prompt
- Remove deprecated implementations

## **Expected Benefits**

### **Technical Benefits**
1. **Standardized Architecture** - Industry MCP standard
2. **Z.AI Native Integration** - Proper platform usage
3. **Testing Tools** - Built-in MCP Inspector
4. **Modular Design** - Each server is independent
5. **Security** - Standardized secure connections

### **Organizational Benefits**
1. **Clean Structure** - No more scattered files
2. **Maintainable** - Standard MCP patterns
3. **Extensible** - Easy to add new servers
4. **Future-Proof** - Industry standard protocol
5. **Debuggable** - Inspector tools available

## **Success Metrics**

### **Before (Current)**
- ✅ Web search working (4,094 characters retrieved)
- ❌ Scattered tools without standardization
- ❌ Manual configuration management
- ❌ No built-in testing

### **After (MCP)**
- ✅ Web search working via MCP
- ✅ Standardized server architecture  
- ✅ Z.AI native integration
- ✅ Built-in testing and debugging
- ✅ Modular and extensible design

## **Next Actions**

1. **Verify Credit Usage** - Check Z.AI dashboard
2. **Install MCP Dependencies** - Set up infrastructure
3. **Build Web Search MCP Server** - Convert working search
4. **Test MCP Integration** - Validate end-to-end
5. **Expand to Other Tools** - Document reader, system monitor

**This MCP approach represents a professional, industry-standard architecture that leverages Z.AI's native ecosystem instead of working around it!**