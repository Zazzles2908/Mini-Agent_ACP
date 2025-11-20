# Mini-Agent VS Code Extension

## Overview
This VS Code extension provides seamless integration between VS Code and Mini-Agent through the Agent Client Protocol (ACP).

## Features
- **Chat Integration**: Use @mini-agent in VS Code chat to interact with Mini-Agent
- **Command Palette**: Access Mini-Agent commands through VS Code command palette
- **Terminal Integration**: Start Mini-Agent ACP server in integrated terminal

## Installation

### From Source
1. Copy this `vscode-extension` folder to your local repository
2. Open VS Code in this folder
3. Press `F5` to start extension development host
4. Or use `Ctrl+Shift+P` > "Extensions: Install Extension from Folder"

### From VSIX
1. Build extension: `vsce package`
2. Install: `code --install-extension mini-agent-acp-1.0.0.vsix`

## Usage

### Chat Interface
1. Open VS Code chat (`Ctrl+Shift+P` > "Chat: Open Chat")
2. Type `@mini-agent` followed by your prompt
3. Example: `@mini-agent explain this code`

### Commands
- **Start Mini-Agent ACP Session**: Opens integrated terminal with Mini-Agent server
- **Send Prompt to Mini-Agent**: Quick prompt entry via input box

### Configuration
Access via `File` > `Preferences` > `Settings` > `Extensions` > `Mini-Agent`

```json
{
  "miniAgent.acpServerPath": "python -m mini_agent.acp.server",
  "miniAgent.enabled": true
}