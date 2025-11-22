# ACP Protocol Integration Guide

## Overview

This document provides comprehensive guidance for Mini-Agent's integration with the Agent Client Protocol (ACP), enabling seamless connection with external editors like VS Code and Zed.

## What is ACP?

The Agent Client Protocol (ACP) is an open standard for AI agent-client communication that provides:
- **Message-based bidirectional communication** between agents and clients
- **Asynchronous operations support** for complex workflows
- **JSON-based structured message format** for reliable data exchange
- **Cross-platform interoperability** across different development environments

## Mini-Agent ACP Implementation

### Core Components

**Location**: `mini_agent/acp/`

```python
mini_agent/acp/
├── __init__.py              # Main ACP agent implementation (stdio-based)
├── server.py                # Server entry point
└── enhanced_server.py       # Enhanced WebSocket implementation
```

### Protocol Compliance

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

### Core Methods

```python
class MiniMaxACPAgent:
    async def initialize(self, params) -> AgentCapabilities
    async def newSession(self, params) -> SessionId
    async def prompt(self, params) -> PromptResponse
    async def cancelSession(self, sessionId) -> None
    async def cleanup(self) -> None
```

## VS Code Integration

### Configuration

**Location**: `mini_agent/vscode_extension/`

#### package.json
```json
{
  "name": "Mini-Agent ACP Integration",
  "version": "0.1.0",
  "contributes": {
    "configuration": {
      "properties": {
        "miniAgent.acpServerPath": {
          "type": "string",
          "default": "python -m mini_agent.acp.server",
          "description": "Command to start ACP server"
        }
      }
    }
  }
}
```

#### Extension Integration
```javascript
// Start ACP server
terminal.sendText('python -m mini_agent.acp.server');

// Chat API integration
// @mini-agent explain this code
// @mini-agent generate tests
// @mini-agent search web for [query]
```

## Zed Editor Integration

### Configuration
```json
{
  "agent_servers": {
    "mini-agent": {
      "command": "python -m mini_agent.acp.server"
    }
  }
}
```

## Usage Examples

### Starting ACP Server
```bash
# Method 1: Direct module call
python -m mini_agent.acp.server

# Method 2: Module import
python -c "from mini_agent.acp import main; main()"

# Method 3: Using mini-agent command
mini-agent-acp
```

### VS Code Chat Usage
```
# Natural language commands
@mini-agent explain this Python function
@mini-agent generate unit tests for this file
@mini-agent search web for Python best practices
@mini-agent help me debug this error
@mini-agent create a flowchart of this system
```

## Implementation Status

### Current Capabilities
- ✅ **stdio-based communication** - Primary method for editor integration
- ✅ **JSON-RPC 2.0 protocol** - Full ACP specification compliance
- ✅ **Session management** - Multi-session support with cancellation
- ✅ **Tool integration** - All Mini-Agent tools accessible via ACP
- ✅ **Error handling** - Robust error handling with user feedback
- ✅ **Status updates** - Real-time status indicators

### Protocol Features
- ✅ **Initialize** - Set up agent capabilities and parameters
- ✅ **newSession** - Create new conversation sessions
- ✅ **prompt** - Process user prompts and return responses
- ✅ **cancelSession** - Cancel ongoing sessions
- ✅ **cleanup** - Proper resource cleanup

## Architecture Integration

### Mini-Agent Core Integration
- **LLM Client**: MiniMax-M2 as primary, Z.AI for web search
- **Tool System**: All 20+ tools accessible via ACP
- **Skills System**: Progressive skill loading (Level 1→2→3)
- **Knowledge Graph**: Session context maintained across interactions

### Transport Layer
- **Primary**: stdio (standard input/output) for editor integration
- **Secondary**: WebSocket for custom implementations
- **Message Format**: JSON-RPC 2.0 structured communication

## Development Guidelines

### Adding New ACP Features

1. **Follow ACP Specification**: Maintain protocol compliance
2. **Session Management**: Properly handle multiple concurrent sessions
3. **Error Handling**: Implement comprehensive error responses
4. **Tool Integration**: Ensure all tools are accessible via ACP
5. **Testing**: Validate with both stdio and WebSocket transports

### Best Practices

```python
# Proper session handling
async def newSession(self, params) -> SessionId:
    session_id = generate_session_id()
    session_context = self.initialize_context(params)
    self.sessions[session_id] = session_context
    return session_id

# Proper error handling
async def prompt(self, params) -> PromptResponse:
    try:
        result = await self.process_prompt(params)
        return PromptResponse.success(result)
    except Exception as e:
        return PromptResponse.error(str(e))
```

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Check Python environment and dependencies
   - Verify ACP package installation
   - Check configuration file syntax

2. **Editor can't connect**
   - Verify server command in editor settings
   - Check firewall and port restrictions
   - Ensure stdio communication works

3. **Tools not accessible**
   - Verify Mini-Agent tool registration
   - Check session context initialization
   - Validate tool permissions

### Debug Commands

```bash
# Test ACP server directly
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}' | python -m mini_agent.acp.server

# Check tool registration
python -c "from mini_agent.acp import main; import asyncio; asyncio.run(main())"

# Validate configuration
python -c "from mini_agent.config import load_config; load_config()"
```

## Future Enhancements

### Planned Features
- **Multi-language support** for international users
- **Advanced session persistence** for long-running workflows
- **Enhanced tool visualization** for better UX
- **Plugin system** for custom extensions
- **Performance optimization** for large projects

### Protocol Updates
- Keep ACP implementation current with protocol specifications
- Add support for new ACP features as they're standardized
- Maintain backward compatibility with older editor versions

---

**Status**: Production Ready  
**Last Updated**: 2025-11-20  
**Protocol Version**: ACP 1.0  
**Mini-Agent Version**: 0.1.0  
**Integration**: VS Code, Zed Editor, Custom Clients  
