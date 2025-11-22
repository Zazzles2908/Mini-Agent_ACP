# VS Code Extension Integration Guide

## Overview

This guide provides comprehensive instructions for integrating Mini-Agent with VS Code through the Agent Client Protocol (ACP), enabling native Chat API support and seamless AI assistance within the editor.

## Architecture

### Communication Flow
```
VS Code Extension ↔ ACP Server (stdio) ↔ Mini-Agent Core
```

### Components
1. **Mini-Agent ACP Server** (`mini_agent/acp/__init__.py`)
2. **VS Code Extension** (`mini_agent/vscode_extension/`)
3. **Chat API Integration** (Native VS Code Chat interface)
4. **Stdio Transport** (JSON-RPC 2.0 communication)

## Installation & Setup

### 1. Prerequisites

```bash
# Ensure Mini-Agent is installed
uv pip install -e .

# Verify ACP server works
python -m mini_agent.acp.server --test
```

### 2. VS Code Extension Setup

**Location**: `mini_agent/vscode_extension/`

#### Install Extension
```bash
# Navigate to extension directory
cd mini_agent/vscode_extension

# Install dependencies (if needed)
npm install

# Package for development
npm run build

# Install in VS Code (development)
code --install-extension mini-agent-0.1.0.vsix
```

#### Configuration
Edit VS Code settings (`~/.vscode/settings.json`):

```json
{
  "miniAgent.acpServerPath": "python -m mini_agent.acp.server",
  "miniAgent.enabled": true,
  "chat.experimental.chatProvider": "vscode"
}
```

## Features

### Chat API Integration

#### Available Commands
```
@mini-agent explain this code
@mini-agent generate unit tests
@mini-agent create documentation
@mini-agent search web for [query]
@mini-agent help debug this error
@mini-agent analyze this function
@mini-agent create flowchart
@mini-agent suggest improvements
```

#### Chat Participant
- **Name**: `@mini-agent`
- **Capability**: Full Mini-Agent tool ecosystem
- **Interface**: Native VS Code Chat API
- **Response Format**: Structured text with tool execution results

### Native Integration

#### File Operations
- Read and edit files directly in chat
- View file contents with syntax highlighting
- Create new files through conversation

#### Code Analysis
- Explain code functionality
- Identify potential issues
- Suggest optimizations
- Generate documentation

#### Testing & Debugging
- Create unit tests
- Debug error messages
- Suggest fixes
- Validate solutions

## Implementation Details

### Extension Structure

```javascript
// extension.js
const vscode = require('vscode');
const { spawn } = require('child_process');

class MiniAgentChatParticipant {
    constructor() {
        this.name = 'mini-agent';
        this.fullName = 'Mini-Agent AI Assistant';
    }
    
    async provideResponse(query, context, stream, token) {
        // Send to ACP server via stdio
        const response = await this.sendToACPServer(query);
        stream.markdown(response);
    }
    
    sendToACPServer(query) {
        return new Promise((resolve, reject) => {
            const process = spawn('python', ['-m', 'mini_agent.acp.server']);
            
            const message = {
                jsonrpc: "2.0",
                method: "prompt",
                params: {
                    message: query,
                    context: context
                },
                id: Date.now()
            };
            
            process.stdin.write(JSON.stringify(message) + '\n');
            
            let result = '';
            process.stdout.on('data', (data) => {
                result += data.toString();
            });
            
            process.on('close', (code) => {
                if (code === 0) {
                    resolve(result);
                } else {
                    reject(new Error(`Process exited with code ${code}`));
                }
            });
        });
    }
}
```

### ACP Server Integration

```python
# mini_agent/acp/__init__.py
import json
import asyncio
from acp import AgentSideConnection, text_block

class MiniMaxACPAgent:
    def __init__(self):
        self.agent = MiniAgent()  # Core Mini-Agent instance
        self.sessions = {}
    
    async def prompt(self, params):
        """Handle VS Code Chat API requests"""
        query = params.get('message', '')
        context = params.get('context', {})
        
        # Process through Mini-Agent
        result = await self.agent.chat(query, context)
        
        # Format for VS Code
        return {
            "content": [
                {
                    "kind": "text",
                    "value": result.content
                }
            ]
        }
```

## Usage Examples

### Basic Interactions

#### Code Explanation
```
User: @mini-agent explain this function
Assistant: 
[Function explanation with code analysis]

Tool Execution:
- File read: ✅ Completed
- Code analysis: ✅ Completed  
- Documentation: ✅ Generated
```

#### Web Search Integration
```
User: @mini-agent search web for Python async best practices
Assistant:
[Search results with Z.AI GLM integration]

Tool Execution:
- Web search: ✅ 3 results found
- Content extraction: ✅ Completed
- Summary generation: ✅ Completed
```

#### File Operations
```
User: @mini-agent create a test file for this module
Assistant:
[Test file content displayed]

Tool Execution:
- File creation: ✅ test_module.py created
- Test generation: ✅ pytest format
- Documentation: ✅ Included
```

## Configuration Options

### Extension Settings

```json
{
  "miniAgent.acpServerPath": "python -m mini_agent.acp.server",
  "miniAgent.enabled": true,
  "miniAgent.workingDirectory": "${workspaceFolder}",
  "miniAgent.timeout": 30000,
  "miniAgent.toolsEnabled": true,
  "miniAgent.webSearchEnabled": true
}
```

### Server Configuration

```python
# mini_agent/acp/config.py
ACP_CONFIG = {
    "timeout": 30,
    "max_tokens": 4000,
    "tools": [
        "file_tools",
        "bash_tool", 
        "zai_web_search",
        "skill_tool"
    ],
    "session_cleanup": 300  # 5 minutes
}
```

## Troubleshooting

### Common Issues

#### Extension Not Loading
```bash
# Check extension logs
View → Output → Mini-Agent

# Verify installation
code --list-extensions | grep mini-agent

# Reload window
Ctrl+Shift+P → Developer: Reload Window
```

#### Chat API Not Responding
```bash
# Test ACP server manually
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}' | python -m mini_agent.acp.server

# Check Python environment
python --version
which python
uv pip list | grep mini-agent
```

#### Tools Not Working
```bash
# Verify tool registration
python -c "from mini_agent import tools; print([t.name for t in tools.get_all_tools()])"

# Check Z.AI integration
python -c "from mini_agent.tools.zai_tools import test_zai_connection; test_zai_connection()"
```

### Debug Mode

Enable verbose logging in VS Code settings:
```json
{
  "miniAgent.debug": true,
  "logging.level": "DEBUG",
  "chat.experimental.chatProvider": "vscode"
}
```

## Performance Optimization

### Response Time
- **First Response**: < 2 seconds
- **Tool Execution**: Depends on tool complexity
- **Web Search**: ~3-5 seconds
- **File Operations**: < 1 second

### Resource Usage
- **Memory**: ~200MB for base system
- **CPU**: Low during idle, moderate during tool execution
- **Network**: Only when using web search or external tools

### Scaling
- Single session: Optimal performance
- Multiple sessions: Linear resource increase
- Large files: Chunked processing to avoid memory issues

## Future Enhancements

### Planned Features
- **Real-time collaboration** for team environments
- **Code completion** integrated with chat
- **Multi-workspace support** for complex projects
- **Custom tool plugins** for specific workflows
- **Advanced debugging** with step-by-step guidance

### Integration Roadmap
1. **Phase 1**: Basic chat integration ✅ Complete
2. **Phase 2**: Advanced tool visualization (In Progress)
3. **Phase 3**: Multi-language support
4. **Phase 4**: Enterprise features

---

**Status**: Production Ready  
**Last Updated**: 2025-11-20  
**Extension Version**: 0.1.0  
**Chat API**: Native VS Code integration  
**Protocol**: ACP 1.0 over stdio  
