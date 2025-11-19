# Enhanced Mini-Agent VS Code Extension Installation Guide

## Overview

This guide provides step-by-step instructions for installing and configuring the enhanced Mini-Agent VS Code extension with full Agent Client Protocol (ACP) support.

## Features

- **Full ACP Protocol Support**: Implements the complete Agent Client Protocol specification
- **WebSocket Communication**: Real-time bidirectional communication between VS Code and Mini-Agent
- **Session Management**: Persistent sessions with context preservation
- **Enhanced UI**: Improved webview interface with conversation history
- **Keyboard Shortcuts**: Quick access to Mini-Agent features
- **Error Handling**: Robust error handling and recovery mechanisms

## Prerequisites

1. **Mini-Agent Installation**: Ensure Mini-Agent is properly installed and configured
2. **VS Code**: Version 1.80.0 or higher
3. **Python Environment**: Python 3.8+ with required dependencies
4. **WebSockets Support**: The `websockets` Python library

## Installation Methods

### Method 1: Direct Installation from Files

1. **Navigate to Extension Directory**
   ```bash
   cd C:\Users\Jazeel-Home\Mini-Agent\mini_agent\vscode_extension
   ```

2. **Copy Enhanced Extension Files**
   ```bash
   # Copy enhanced extension as main extension
   copy enhanced_extension.js extension.js
   copy enhanced_package.json package.json
   ```

3. **Install Extension in VS Code**
   ```bash
   # In VS Code terminal or command palette
   code --install-extension ./mini_agent/vscode_extension
   ```

### Method 2: Package and Install

1. **Create VSIX Package**
   ```bash
   cd C:\Users\Jazeel-Home\Mini-Agent\mini_agent\vscode_extension
   npx vsce package
   ```

2. **Install from VSIX**
   ```bash
   code --install-extension mini-agent-vscode-enhanced-1.0.0.vsix
   ```

## Configuration

### 1. Environment Variables

Ensure your `.env` file contains:
```bash
# Mini-Agent Configuration
MINIMAX_API_KEY=your_minimax_api_key_here
ZAI_API_KEY=your_zai_api_key_here

# ACP Server Configuration (optional)
ACP_HOST=127.0.0.1
ACP_PORT=8765
```

### 2. VS Code Settings

Add to your VS Code settings (`.vscode\settings.json`):
```json
{
    "miniAgent.enabled": true,
    "miniAgent.autoStart": true,
    "miniAgent.host": "127.0.0.1",
    "miniAgent.port": 8765
}
```

### 3. Workspace Configuration

Create `.vscode\settings.json` in your project:
```json
{
    "files.associations": {
        "*.agent": "markdown"
    },
    "miniAgent.workspaceSupport": true
}
```

## Usage

### 1. Activation

- **Command Palette**: Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and type "Mini-Agent: Activate Assistant"
- **Status Bar**: Click the Mini-Agent robot icon in the status bar
- **Activity Bar**: Click the Mini-Agent icon in the activity bar

### 2. Available Commands

| Command | Keyboard Shortcut | Description |
|---------|------------------|-------------|
| Mini-Agent: Ask Question | `Ctrl+Shift+A` | Ask a general question |
| Mini-Agent: Explain Code | `Ctrl+Shift+E` | Explain selected code |
| Mini-Agent: Generate Code | `Ctrl+Shift+G` | Generate new code |
| Mini-Agent: Refactor Selection | `Ctrl+Shift+R` | Refactor selected code |
| Mini-Agent: Generate Tests | `Ctrl+Shift+T` | Generate unit tests |
| Mini-Agent: Reset Session | `Ctrl+Shift+Reset` | Reset the conversation |

### 3. Context Menu Integration

- **Editor Context**: Right-click on selected code for quick actions
- **Explorer Context**: Right-click in explorer for general questions

### 4. Webview Interface

The enhanced webview provides:
- **Conversation History**: Persistent chat history
- **Real-time Status**: Connection and processing status
- **Rich Formatting**: Code blocks and markdown support
- **Error Display**: Clear error messages and recovery options

## ACP Protocol Features

### 1. Real-time Communication

- WebSocket-based bidirectional communication
- Immediate status updates during processing
- Automatic reconnection handling

### 2. Session Management

- **Session Creation**: Automatic session initialization
- **Context Preservation**: Maintains conversation context
- **Workspace Integration**: Works with your project workspace
- **Session Reset**: Clean slate when needed

### 3. Message Types

The extension supports all ACP message types:

| Type | Direction | Purpose |
|------|-----------|---------|
| `initialize` | Client → Server | Protocol handshake |
| `newSession` | Client → Server | Create new session |
| `prompt` | Client → Server | Send user prompt |
| `status_update` | Server → Client | Processing status |
| `prompt_response` | Server → Client | AI response |
| `error` | Server → Client | Error reporting |
| `heartbeat` | Both | Connection keepalive |

### 4. Error Handling

- **Connection Errors**: Automatic retry with exponential backoff
- **Protocol Errors**: Clear error messages with recovery suggestions
- **Session Errors**: Session invalidation and recreation
- **Timeout Handling**: Graceful timeout management

## Troubleshooting

### Common Issues

1. **Extension Not Loading**
   - Check VS Code version compatibility (1.80.0+)
   - Verify Python environment has required packages
   - Check VS Code console for errors

2. **Connection Failed**
   - Ensure Mini-Agent is properly installed
   - Check firewall settings for port 8765
   - Verify environment variables are set

3. **Authentication Errors**
   - Check `.env` file has valid API keys
   - Verify API key permissions
   - Test API key directly with Mini-Agent CLI

4. **WebSocket Errors**
   - Check Python websockets library installation
   - Verify port 8765 is not in use
   - Check antivirus software blocking WebSocket

### Debug Mode

Enable debug logging:
```bash
# Start VS Code with extension debugging
code --logExtensionHost --verbose

# Or set in settings.json
{
    "miniAgent.debugMode": true,
    "miniAgent.logLevel": "DEBUG"
}
```

### Log Locations

- **VS Code**: `View → Output → Mini-Agent`
- **Extension**: Developer Tools Console
- **ACP Server**: Mini-Agent terminal output

## Advanced Configuration

### 1. Custom ACP Server

Use a custom ACP server endpoint:
```json
{
    "miniAgent.host": "192.168.1.100",
    "miniAgent.port": 9000,
    "miniAgent.useCustomServer": true
}
```

### 2. Workspace Integration

Configure workspace-specific settings:
```json
{
    "miniAgent.workspacePath": "${workspaceFolder}/.mini-agent",
    "miniAgent.autoLoadWorkspace": true,
    "miniAgent.enableFileTools": true
}
```

### 3. Performance Tuning

Optimize for your environment:
```json
{
    "miniAgent.requestTimeout": 30000,
    "miniAgent.maxRetries": 3,
    "miniAgent.connectionTimeout": 5000,
    "miniAgent.enableCaching": true
}
```

## Development Mode

### 1. Running from Source

```bash
# Clone and setup
git clone <repository>
cd Mini-Agent

# Install dependencies
uv pip install -r requirements.txt
uv pip install websockets

# Link extension (development mode)
cd mini_agent/vscode_extension
npm link

# Install in VS Code
code --install-extension mini-agent-vscode-enhanced
```

### 2. Debugging Extension

1. Open VS Code with the extension loaded
2. Press `F5` to start debugging
3. Use Developer Tools for console access
4. Set breakpoints in extension code

### 3. Testing ACP Integration

```bash
# Run ACP integration tests
python scripts/test_enhanced_acp.py

# Test WebSocket communication
python scripts/test_acp_integration.py
```

## Support

### Getting Help

1. **Check Documentation**: Review this guide and Mini-Agent docs
2. **Check Logs**: Review VS Code output and extension logs
3. **Test Integration**: Run the test scripts provided
4. **Create Issue**: Report bugs on the project repository

### Contributing

1. **Code Contributions**: Follow the project's coding standards
2. **Testing**: Add tests for new features
3. **Documentation**: Update guides for changes
4. **Reviews**: Submit pull requests for review

## Version History

### v1.0.0 - Enhanced ACP Implementation
- Full ACP protocol implementation
- WebSocket communication
- Enhanced webview interface
- Session management
- Error handling
- Keyboard shortcuts
- Context menu integration

### v0.1.0 - Basic Integration
- Basic VS Code integration
- Simple chat interface
- File operations
- Basic authentication

## License

This extension is part of the Mini-Agent project and follows the same license terms.

---

**Happy Coding with Mini-Agent!** 🤖✨
