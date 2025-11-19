# Mini-Agent VS Code Extension

AI coding assistant powered by Mini-Agent with integrated Chat API support.

## Features

### Chat Integration
- **@mini-agent**: Use in VS Code Chat to interact with Mini-Agent
- **Natural Language**: Ask questions, get explanations, generate code
- **Context Aware**: Understands your current file and workspace

### Command Palette
- `Ctrl+Shift+A` (Mac: `Cmd+Shift+A`): Ask Mini-Agent anything
- `Ctrl+Shift+E` (Mac: `Cmd+Shift+E`): Explain selected code
- `Ctrl+Shift+G` (Mac: `Cmd+Shift+G`): Generate code from description

### Right-Click Context Menus
- **Explain Code**: Select code → Right-click → Mini-Agent → Explain Code
- **Refactor Code**: Select code → Right-click → Mini-Agent → Refactor Code  
- **Generate Tests**: Select code → Right-click → Mini-Agent → Generate Tests

## Installation

### From Source
1. Clone this repository
2. Copy `mini_agent/vscode_extension/` to your local machine
3. In VS Code: `Ctrl+Shift+P` → "Extensions: Install from VSIX..." 
4. Select the folder containing these files

### Development Mode
```bash
cd mini_agent/vscode_extension
npm install
vsce package
# Install the generated .vsix file
```

## Configuration

The extension automatically detects your Mini-Agent installation. No additional configuration required.

## Usage

### Chat Interface
1. Open VS Code Chat (`Ctrl+Shift+P` → "Chat: Open Chat")
2. Type `@mini-agent` followed by your question
3. Example: `@mini-agent explain this function` (with code selected)

### Command Palette
1. Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. Type "Mini-Agent" to see available commands
3. Select the command you want to use

### Right-Click Menus
1. Select code in the editor
2. Right-click to see Mini-Agent context menu
3. Choose the action you want to perform

## Examples

### Ask Questions
```
@mini-agent How do I fix this TypeScript error?
@mini-agent What's the difference between let and const in JavaScript?
@mini-agent Can you help me optimize this Python function?
```

### Explain Code
1. Select code in editor
2. Use `@mini-agent explain this code` in chat
3. Or use right-click context menu → "Explain Code"

### Generate Code
```
@mini-agent create a React component for user authentication
@mini-agent write a Python function to sort a list of dictionaries
@mini-agent generate a SQL query to find duplicate records
```

### Refactor Code
1. Select code in editor
2. Use `@mini-agent refactor this code to be more efficient`
3. Or use right-click context menu → "Refactor Code"

## Technical Details

### Architecture
- **Transport**: stdio communication with Mini-Agent ACP server
- **Protocol**: JSON-RPC 2.0 over stdin/stdout
- **Chat API**: VS Code 1.82+ Chat Participant integration
- **Session Management**: Multi-session support with cancellation

### Communication Flow
```
VS Code Chat ↔ Extension (stdio) ↔ Mini-Agent ACP Server ↔ Mini-Agent Core
```

### Requirements
- VS Code 1.82.0 or later
- Python 3.8+ (for Mini-Agent)
- Mini-Agent installed and accessible

## Troubleshooting

### Extension Not Loading
1. Check VS Code version (1.82.0+ required)
2. Verify Python is in PATH
3. Check VS Code Developer Console for errors

### Chat Not Working
1. Ensure Mini-Agent is properly installed
2. Check that ACP server can start
3. Verify Python path in extension settings

### No Response from Mini-Agent
1. Check Mini-Agent logs in VS Code Developer Console
2. Verify ACP server is running
3. Try resetting the session

## Development

### Running Tests
```bash
cd mini_agent/vscode_extension
npm install
npm test
```

### Building Extension
```bash
npm run compile
vsce package
```

### Debugging
1. Open VS Code Developer Console (`Ctrl+Shift+I`)
2. Check Console tab for extension logs
3. Look for "ACP Server:" messages for server communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/0xSero/Mini-Agent/issues)
- Documentation: [Mini-Agent Docs](https://github.com/0xSero/Mini-Agent#readme)

---

**Mini-Agent VS Code Extension** - Bringing AI coding assistance directly into your editor with native Chat API integration.