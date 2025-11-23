# ACP Protocol Complete Guide
**Merged Overview and Integration Documentation**

**Created**: November 24, 2025  
**Merged From**: ACP_OVERVIEW.md + ACP_PROTOCOL_INTEGRATION.md  
**Status**: Complete ACP protocol reference  

---

## 🎯 **What is ACP?**

**Agent Client Protocol (ACP)** is a standardized communication protocol that allows AI agents to communicate with external clients (editors, IDEs, applications) through a consistent interface.

### **Official Specification**
- **Website**: [agentclientprotocol.com](https://agentclientprotocol.com)
- **Protocol**: JSON-RPC 2.0 over stdio
- **Standard**: Open protocol for agent-client communication
- **Used by**: Zed Editor, MiniMax-M2 Code, and other professional tools

### **Why ACP Matters**
1. **Protocol Compliance**: Standard approach instead of custom implementations
2. **Editor Integration**: Native support in VS Code, Zed, other editors
3. **Scalability**: Multiple clients can connect to the same agent
4. **Future-Proofing**: Industry-standard approach that will evolve with the ecosystem

---

## 🏗️ **Mini-Max Agent ACP Implementation**

### **Implementation Location**
- **File**: `mini_agent/acp/__init__.py`
- **Class**: `MiniMaxACPAgent`
- **Transport**: stdio (standard input/output)
- **Protocol**: JSON-RPC 2.0

### **Architecture Overview**
```
┌─────────────────────────────────────────────────────┐
│              Editor Client                           │
│  (VS Code, Zed, etc.)                                │
│  • Chat interface                                    │
│  • User interactions                                 │
└─────────────────────────────────────────────────────┘
                        ↓ stdin/stdout
┌─────────────────────────────────────────────────────┐
│              MiniMaxACPAgent                         │
│  • Protocol handler                                  │
│  • Session management                                │
│  • Mini-Max Agent wrapper                            │
└─────────────────────────────────────────────────────┘
                        ↓ Python functions
┌─────────────────────────────────────────────────────┐
│              Mini-Max Agent Core                     │
│  • Tool execution                                    │
│  • LLM integration                                   │
│  • Message management                                │
└─────────────────────────────────────────────────────┘
```

### **Core Components**

**Location**: `mini_agent/acp/`

```python
mini_agent/acp/
├── __init__.py              # Main ACP agent implementation (stdio-based)
├── server.py                # Server entry point
└── enhanced_server.py       # Enhanced WebSocket implementation
```

### **Protocol Compliance**

Mini-Agent's ACP implementation follows the official ACP specification:

```python
# Required ACP imports
from acp import (
    PROTOCOL_VERSION,
    AgentSideConnection,
    start_tool_call,
    stdio_streams,
    text_block,
    tool_content,
    update_agent_message,
    update_agent_thought,
    update_tool_call,
)
```

---

## 🔧 **Technical Implementation**

### **What is ACP?**
The Agent Client Protocol (ACP) is an open standard for AI agent-client communication that provides:
- **Message-based bidirectional communication** between agents and clients
- **Asynchronous operations support** for complex workflows
- **JSON-based structured message format** for reliable data exchange
- **Cross-platform interoperability** across different development environments

### **Core Methods**

```python
class MiniMaxACPAgent:
    """Main ACP agent implementation with stdio transport."""
    
    def __init__(self):
        """Initialize ACP agent with protocol compliance."""
        
    async def handle_client_request(self, request):
        """Process incoming client requests and route to appropriate handlers."""
        
    async def stream_response(self, response_generator):
        """Stream responses back to client using ACP protocol."""
        
    async def handle_tool_calls(self, tool_calls):
        """Execute tool calls and return formatted results."""
        
    async def update_agent_state(self, state_updates):
        """Update agent state and notify client of changes."""
```

### **Transport Methods**
1. **stdio transport**: Standard input/output (primary method)
2. **WebSocket transport**: Enhanced real-time communication
3. **HTTP transport**: Alternative communication method

---

## 🚀 **Editor Integration**

### **VS Code Integration**
Mini-Agent provides VS Code extension integration through ACP protocol:

**Extension Components**:
- **Package**: `vscode-extension/` directory
- **Integration**: Native VS Code Chat API
- **Communication**: ACP stdio protocol

**Setup Process**:
1. Install VS Code extension
2. Configure Mini-Agent ACP server
3. Establish stdio communication
4. Enable Chat API integration

### **Zed Editor Integration**
Zed Editor has native ACP support:
- **Protocol**: JSON-RPC 2.0 over stdio
- **Connection**: Direct ACP agent connection
- **Features**: Real-time chat and tool integration

---

## 📋 **Configuration & Usage**

### **Enable ACP Server**
```bash
# Start ACP server
python -m mini_agent.acp

# Test ACP server
python -m mini_agent.acp --test

# Connect via editor
# Configure editor to connect to Mini-Agent ACP endpoint
```

### **Client Connection**
```python
# Example client connection
import asyncio
from acp import AgentSideConnection, stdio_streams

async def connect_to_mini_agent():
    streams = await stdio_streams()
    connection = AgentSideConnection(streams)
    await connection.send_request("agent/say", {
        "message": "Hello from client!"
    })
```

---

## 📊 **Benefits & Features**

### **Protocol Advantages**
- **Standard Compliance**: Industry-standard communication
- **Multiple Client Support**: Connect different editors simultaneously
- **Asynchronous Communication**: Non-blocking operations
- **Extensible Design**: Easy to add new capabilities

### **Mini-Agent ACP Features**
- **Tool Integration**: Direct access to all Mini-Agent tools
- **Real-time Communication**: Streaming responses and updates
- **Session Management**: Persistent conversation context
- **Error Handling**: Robust error reporting and recovery

---

## 🔗 **Related Documentation**

- **VS Code Integration**: `VSCODE_INTEGRATION_GUIDE.md`
- **System Architecture**: `MASTER_SYSTEM_ARCHITECTURE_COMPLETE.md`
- **Tool System**: Tool framework documentation
- **Configuration**: `04_SETUP_CONFIG/CONFIGURATION.md`

---

**This merged guide provides complete ACP protocol documentation for Mini-Agent implementation, combining overview concepts with technical integration details.**