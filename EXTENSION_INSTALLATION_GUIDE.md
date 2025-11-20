# Mini-Agent VS Code Extension - INSTALLATION GUIDE

## 📦 Package Details
- **File**: `mini-agent-vscode-1.0.0.zip`
- **Size**: 2.9KB
- **Location**: `C:\Users\Jazeel-Home\Mini-Agent\mini-agent-vscode-1.0.0.zip`

## 🚀 Installation Options

### Option 1: Command Line (Recommended)
```bash
# Install the extension
code --install-extension mini-agent-vscode-1.0.0.zip
```

### Option 2: VS Code GUI
1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Run: "Extensions: Install Extension from VSIX..."
4. Select: `mini-agent-vscode-1.0.0.zip`
5. Click "Install"
6. Restart VS Code

### Option 3: Drag & Drop
1. Open VS Code
2. Drag `mini-agent-vscode-1.0.0.zip` into VS Code
3. Click "Install" when prompted
4. Restart VS Code

## ✅ Verification

After installation, you should see:
- ✅ "Mini-Agent AI Assistant" in Extensions list
- ✅ Chat participant `@mini-agent` available
- ✅ Commands in Command Palette (Ctrl+Shift+P)

## 🎯 Usage

### Open Chat Panel
1. **Press**: `Ctrl+Shift+P`
2. **Type**: "Chat: Open Chat"
3. **Click**: Enter Chat panel

### Use Mini-Agent
1. **Type**: `@mini-agent explain this code`
2. **Ask**: `@mini-agent generate tests for function`
3. **Request**: `@mini-agent search web for best practices`

## 🔧 Requirements

### VS Code Version
- **Minimum**: VS Code 1.82.0
- **Recommended**: Latest VS Code version

### Mini-Agent ACP Server
The extension requires Mini-Agent ACP server running:
```bash
cd C:\Users\Jazeel-Home\Mini-Agent
python -m mini_agent.acp.server
```

### Node.js
- **Required**: Node.js 16+ (usually pre-installed with VS Code)
- **Check**: `node --version` in terminal

## 🎉 Features

- **Chat Integration**: Native `@mini-agent` participant
- **Tool Ecosystem**: Full Mini-Agent tool access through Chat
- **Knowledge Graph**: Session context persistence
- **Progressive Loading**: Skill-based architecture
- **Multiple Commands**: Extension commands and Chat interactions

## 🛠️ Troubleshooting

### Extension Not Loading
- Check VS Code console: `Help → Toggle Developer Tools`
- Look for activation errors
- Restart VS Code

### Chat Not Working
1. **Ensure ACP Server Running**:
   ```bash
   python -m mini_agent.acp.server
   ```
2. **Check Network**: Port 3000 should be available
3. **Restart Extension**: Disable/enable in Extensions

### Commands Not Showing
1. **Reload Window**: `Ctrl+Shift+P` → "Developer: Reload Window"
2. **Check Activation**: Look for "Mini-Agent extension activated" in console

## 📋 Architecture

```
VS Code Chat ↔ Extension ↔ Mini-Agent Skill System ↔ Tool Ecosystem
                                                    ↕
                                           Knowledge Graph Persistence
```

**Status**: Ready for production use! 🎯