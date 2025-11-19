# ACP (Agent Client Protocol) Integration Guide

## What is ACP and Why It Matters

**ACP (Agent Client Protocol)** is the architectural backbone that enables Mini-Agent to function as a server for code editors and IDEs. It's the protocol that bridges AI assistants with development environments.

### Architecture Overview
```
┌─────────────────┐    ACP Protocol    ┌─────────────────┐    Mini-Agent    ┌─────────────────┐
│  Code Editor    │ ◄────────────────► │   ACP Bridge    │ ◄──────────────► │  Core Runtime   │
│  (VS Code/Zed)  │    (StdIO Stream)  │   (Protocol)    │    (Native)      │  (LLM + Tools)  │
│                 │                    │                 │                  │                 │
│ • User Input    │ ◄─ Prompt         │ • Protocol      │ ◄─ Agent Run    │ • File Tools    │
│ • Visual UI     │ ──► Updates       │   Bridge        │ ──► Results      │ • Z.AI Search   │
│ • Tool Display  │ ◄─ Tool Updates   │ • Session Mgmt  │ ◄─ Tool Calls   │ • Skills        │
└─────────────────┘                    └─────────────────┘                  └─────────────────┘
```

## Current Status Assessment

### ✅ What's Already Implemented
- **ACP Protocol Layer**: Complete implementation in `/mini_agent/acp/`
- **Protocol Bridge**: `MiniMaxACPAgent` class wraps Mini-Agent core
- **Server Entry Point**: `mini-agent-acp` command available
- **Tool Schema Mapping**: All tools properly exported for editor consumption
- **Session Management**: Multiple concurrent editor sessions supported

### ⚠️ What's Missing for Full Integration
- **VS Code Extension**: Editor-side integration
- **Protocol Client**: Standard ACP client implementation
- **Configuration**: Editor-specific settings
- **Documentation**: Setup instructions for users

## Implementation Plan

### Phase 1: Verify Current ACP Server ✅
```bash
# Test ACP server works
cd C:\Users\Jazeel-Home\Mini-Agent
python -m mini_agent.acp.server
```

### Phase 2: Create VS Code Extension (Required)
ACP needs an editor extension to work. Create minimal VS Code extension:

#### Extension Structure
```
vscode-mini-agent/
├── package.json          # Extension manifest
├── extension.js          # Main extension logic
├── acp-client.js         # ACP protocol client
└── README.md
```

#### Key Components Needed

**1. ACP Protocol Client** (`acp-client.js`)
```javascript
class ACPClient {
    constructor(command) {
        this.command = command;
        this.process = null;
    }
    
    async start() {
        // Start mini-agent-acp server
        this.process = spawn(this.command, [], { stdio: 'pipe' });
        // Handle protocol communication
    }
    
    async initialize() {
        // Send InitializeRequest
    }
    
    async newSession(cwd) {
        // Send NewSessionRequest  
    }
    
    async prompt(sessionId, prompt) {
        // Send PromptRequest
    }
}
```

**2. VS Code Extension** (`extension.js`)
```javascript
const vscode = require('vscode');
const ACPClient = require('./acp-client');

function activate(context) {
    // Register commands
    // Setup panel/terminal integration
    // Handle file system events
}

exports.activate = activate;
```

### Phase 3: Editor Integration Options

#### Option A: VS Code Extension (Recommended)
**Pros**: Full integration, professional UX
**Cons**: Requires extension development
**Time**: 2-3 days

#### Option B: Simple CLI Wrapper (Quick Start)
**Pros**: Immediate functionality
**Cons**: Limited visual feedback
**Time**: 30 minutes

```python
# quick_bridge.py - Simple command wrapper
import subprocess
import json

def start_acp_session():
    """Start ACP session with JSON output for editor parsing"""
    cmd = ["python", "-m", "mini_agent.acp.server"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return process
```

#### Option C: WebSocket Bridge (Hybrid)
**Pros**: Browser-based interface with real-time updates
**Cons**: Additional complexity
**Time**: 1 day

### Phase 4: Configuration and Setup

#### 4.1 Environment Configuration
```bash
# Add to VS Code settings.json
{
    "miniAgent.command": "python",
    "miniAgent.args": ["-m", "mini_agent.acp.server"],
    "miniAgent.workspace": "${workspaceFolder}",
    "miniAgent.enabled": true
}
```

#### 4.2 Path Configuration
```python
# Ensure ACP server is accessible
# Add to PATH or use absolute paths
ACP_SERVER_PATH = "C:/Users/Jazeel-Home/Mini-Agent/mini_agent/acp/server.py"
```

#### 4.3 Protocol Configuration
```yaml
# config.yaml additions
acp:
  enabled: true
  server_path: "mini_agent.acp.server"
  timeout: 30
  session_limit: 5
```

## Current Working Directory Bridge

Since you're in VS Code terminal, here's the **immediate solution**:

### Quick Bridge Implementation (5 minutes)

Create a bridge script that connects your terminal to ACP:

```python
#!/usr/bin/env python3
"""
VS Code Terminal → ACP Bridge
Quick integration for immediate use
"""

import subprocess
import sys
import json
from pathlib import Path

def setup_vscode_acp_bridge():
    """Setup immediate ACP integration from VS Code terminal"""
    
    # Ensure working directory is Mini-Agent root
    project_root = Path(__file__).parent
    print(f"Working directory: {project_root}")
    
    # Test ACP server
    try:
        print("🔧 Testing ACP server...")
        result = subprocess.run([
            sys.executable, "-m", "mini_agent.acp.server"
        ], cwd=project_root, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ ACP server is functional")
            print("📋 Integration instructions:")
            print("1. Install VS Code extension (future step)")
            print("2. Or use terminal-based bridge for now")
            return True
        else:
            print(f"❌ ACP server error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    setup_vscode_acp_bridge()
```

## Architectural Significance

### Why ACP is the Backbone

1. **Standardization**: Provides consistent protocol for all editor integrations
2. **Separation of Concerns**: 
   - Mini-Agent: Core AI logic
   - ACP: Protocol bridge
   - Editor: User interface
3. **Scalability**: Single server, multiple editor instances
4. **Future-Proof**: Protocol remains stable even as editors evolve

### The Complete Integration Flow

```
┌─ VS Code ─┐    ACP Protocol     ┌─ ACP Bridge ─┐    Internal     ┌─ Mini-Agent ─┐
│  Terminal │ ◄────────────────► │   (Python)   │ ◄──────────────┘     Core       │
│  CLI      │    JSON over IPC   │              │    Function       │  Runtime     │
│           │                    │              │    Calls         │              │
│ Commands  │ ◄─ prompt()        │  • Session   │ ◄─ agent.run()  │  • LLM       │
│ Responses │ ──► updates()      │    Management│ ──► results()   │  • Tools     │
│ Tool Logs │ ◄─ tool_calls()    │  • Protocol  │ ◄─ tool_exec()  │  • Skills    │
└───────────┘                    │    Translation│ ──► tool_result│              │
                                  └──────────────┘               └──────────────┘
```

## Next Steps Recommendation

### Immediate (5 minutes)
1. ✅ Test current ACP server: `python -m mini_agent.acp.server`
2. ✅ Create simple terminal bridge for current session

### Short-term (30 minutes)
1. 📝 Create basic VS Code settings for ACP
2. 🔧 Develop simple CLI wrapper with protocol output
3. 📋 Document terminal-based workflow

### Medium-term (1-2 days)
1. 🎯 Develop minimal VS Code extension
2. 🔗 Add protocol client implementation
3. 📖 Create complete setup documentation

### Long-term (1 week)
1. 🌐 Full editor integration with visual feedback
2. 🔄 Real-time tool execution display
3. 📊 Advanced features (file watching, etc.)

## Current Status

**✅ Foundation**: ACP protocol layer is complete and functional
**✅ Server**: `mini-agent-acp` command works
**⚠️ Missing**: Editor-side integration (VS Code extension)
**🎯 Next**: Implement bridge for immediate VS Code terminal use

You're perfectly positioned - the architectural backbone is solid, we just need to bridge it to your VS Code workflow!
