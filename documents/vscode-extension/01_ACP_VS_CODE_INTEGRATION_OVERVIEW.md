# VS Code Extension Integration Overview
## Agent Client Protocol (ACP) + Mini-Agent Architecture

**Last Updated**: 2025-11-20  
**Status**: Implementation Planning Phase  
**Architecture Compliance**: ✅ Following Mini-Agent Progressive Enhancement Pattern

---

## 🎯 Mission Statement

Create a fully-featured VS Code Chat Extension that integrates Mini-Agent's capabilities through the Agent Client Protocol (ACP), providing users with an intelligent coding assistant directly in their IDE.

---

## 📋 Executive Summary

### What We're Building
A **VS Code Chat Extension** that:
- Integrates with VS Code's native Chat UI (`@mini-agent`)
- Communicates with Mini-Agent via ACP (JSON-RPC 2.0 over stdio)
- Provides full access to Mini-Agent's capabilities (file operations, web search, skills, knowledge graph)
- Maintains session context and conversation history
- Supports streaming responses with real-time tool execution feedback

### Current State Analysis

#### ✅ What We Have
1. **Mini-Agent Core Runtime**
   - LLM integration (Anthropic, OpenAI, Z.AI)
   - Tool ecosystem (file ops, bash, web search, git, knowledge graph)
   - Skills system with progressive loading
   - Configuration management

2. **ACP Server Implementation** (WebSocket-based)
   - Location: `mini_agent/acp/enhanced_server.py`
   - Protocol: Custom WebSocket with JSON messages
   - Session management working
   - ⚠️ **Issue**: Uses WebSocket, but VS Code/Zed need **stdio**

3. **Basic VS Code Extension Stub**
   - Location: `vscode-extension/`
   - Minimal command registration
   - ⚠️ **Issue**: No actual ACP communication, no Chat API integration

#### ❌ What's Missing
1. **ACP Server Stdio Mode**
   - Need JSON-RPC 2.0 over stdin/stdout (current implementation uses WebSocket)
   - Must follow official ACP spec: https://agentclientprotocol.com/protocol/overview

2. **VS Code Chat Extension**
   - Chat Participant API integration
   - Language Model provider setup
   - Proper ACP client for stdio communication

3. **Protocol Bridge Layer**
   - Translate VS Code Chat API ↔ ACP Protocol ↔ Mini-Agent Core
   - Handle streaming responses
   - Manage tool execution visibility

---

## 🏗️ Architecture Design

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     VS CODE EXTENSION LAYER                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Chat Participant (@mini-agent)                             │    │
│  │  • Chat UI Integration                                      │    │
│  │  • User prompt handling                                     │    │
│  │  • Response streaming display                               │    │
│  │  • Tool execution visualization                             │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              ↕ VS Code Chat API                     │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Extension Host (extension.js)                              │    │
│  │  • Command registration                                     │    │
│  │  • Configuration management                                 │    │
│  │  • Session lifecycle management                             │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              ↕ Process spawn + stdio
┌─────────────────────────────────────────────────────────────────────┐
│                      ACP PROTOCOL LAYER                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  ACP Server (stdio mode)                                    │    │
│  │  • JSON-RPC 2.0 message handling                            │    │
│  │  • Session management                                       │    │
│  │  • Protocol translation                                     │    │
│  │  • Stdin/stdout communication                               │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              ↕ Python function calls
┌─────────────────────────────────────────────────────────────────────┐
│                     MINI-AGENT CORE LAYER                            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Agent Runtime                                              │    │
│  │  • LLM client wrapper                                       │    │
│  │  • Tool execution engine                                    │    │
│  │  • Skills system                                            │    │
│  │  • Knowledge graph integration                              │    │
│  │  • Session notes & memory                                   │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Communication Flow

```
User Types in VS Code Chat:
    "@mini-agent create a Python script to analyze CSV files"
         ↓
VS Code Chat Participant receives prompt
         ↓
Extension spawns Mini-Agent ACP Server (if not running)
         ↓
Extension sends JSON-RPC request over stdin:
    {
      "jsonrpc": "2.0",
      "id": "1",
      "method": "agent/createSession",
      "params": { "workspaceDir": "/path/to/workspace" }
    }
         ↓
ACP Server receives, creates session, returns session ID
         ↓
Extension sends prompt:
    {
      "jsonrpc": "2.0",
      "id": "2",
      "method": "agent/prompt",
      "params": {
        "sessionId": "uuid",
        "prompt": "create a Python script..."
      }
    }
         ↓
ACP Server forwards to Mini-Agent Core
         ↓
Mini-Agent Core processes with LLM + Tools
         ↓
ACP Server streams updates via JSON-RPC notifications:
    {"jsonrpc": "2.0", "method": "agent/update", "params": {...}}
         ↓
Extension receives updates on stdout
         ↓
Extension renders in VS Code Chat UI with markdown/code blocks
         ↓
User sees real-time response with tool execution details
```

---

## 🔑 Key Technical Requirements

### 1. ACP Protocol Compliance

**Official Spec**: https://agentclientprotocol.com/protocol/overview

**Required Features**:
- ✅ JSON-RPC 2.0 format
- ✅ Stdio transport (stdin for requests, stdout for responses)
- ✅ Message types:
  - `initialize` - Protocol handshake
  - `agent/createSession` - Create conversation session
  - `agent/prompt` - Send user prompt
  - `agent/cancelSession` - Cancel ongoing operation
  - `agent/update` - Streaming update notification
- ✅ Session management (multiple concurrent sessions)
- ✅ Proper error handling with JSON-RPC error objects

### 2. VS Code Chat API Integration

**Official API**: https://code.visualstudio.com/api/extension-guides/ai/chat

**Required Implementation**:
```typescript
// Chat Participant registration
const chatParticipant = vscode.chat.createChatParticipant(
  'mini-agent',
  async (request, context, stream, token) => {
    // Handle chat request
    // Communicate with ACP server
    // Stream responses
  }
);
```

**Features to Implement**:
- ✅ Chat participant with `@mini-agent` handle
- ✅ Prompt handling and validation
- ✅ Streaming response display
- ✅ Markdown rendering support
- ✅ Code block syntax highlighting
- ✅ Tool execution progress indicators
- ✅ File reference support (`#file` mentions)
- ✅ Cancellation support

### 3. Mini-Agent Core Integration

**Must Preserve**:
- ✅ All existing tool capabilities
- ✅ Skills system access
- ✅ Knowledge graph operations
- ✅ Web search integration (Z.AI)
- ✅ Configuration system
- ✅ Session notes and memory

**Integration Points**:
```python
# ACP Server must wrap existing Agent class
from mini_agent.agent import Agent
from mini_agent.config import Config
from mini_agent.llm import LLMClient

class ACPServer:
    def __init__(self):
        self.config = Config.load()
        self.llm_client = LLMClient(...)
        self.sessions = {}  # session_id -> Agent instance
    
    def create_session(self, workspace_dir):
        agent = Agent(
            llm_client=self.llm_client,
            system_prompt=...,
            tools=self.load_tools(),
            workspace_dir=workspace_dir
        )
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = agent
        return session_id
    
    def process_prompt(self, session_id, prompt):
        agent = self.sessions[session_id]
        # Stream results back via JSON-RPC notifications
        async for update in agent.run_streaming(prompt):
            self.send_notification('agent/update', update)
```

---

## 📊 Implementation Phases

### Phase 1: ACP Server Refactor (Stdio Mode) 🎯 **PRIORITY**
**Goal**: Modify existing ACP server to use stdio instead of WebSocket

**Files to Create/Modify**:
- `mini_agent/acp/stdio_server.py` - New stdio-based server
- `mini_agent/acp/protocol.py` - JSON-RPC 2.0 message handling
- `mini_agent/acp/__init__.py` - Update exports

**Acceptance Criteria**:
- ✅ Server accepts JSON-RPC requests on stdin
- ✅ Server sends responses/notifications on stdout
- ✅ Proper error handling
- ✅ Session management working
- ✅ Can be tested with simple stdio client

### Phase 2: VS Code Extension Core 🎯
**Goal**: Create VS Code extension with Chat API integration

**Files to Create**:
- `vscode-extension/src/extension.ts` - Main extension entry
- `vscode-extension/src/chatParticipant.ts` - Chat participant handler
- `vscode-extension/src/acpClient.ts` - ACP protocol client
- `vscode-extension/src/sessionManager.ts` - Session lifecycle
- `vscode-extension/package.json` - Extension manifest
- `vscode-extension/tsconfig.json` - TypeScript config

**Acceptance Criteria**:
- ✅ Extension activates in VS Code
- ✅ Chat participant registered (`@mini-agent`)
- ✅ Can spawn ACP server process
- ✅ Can send/receive JSON-RPC messages
- ✅ Basic prompt-response working

### Phase 3: Response Streaming & Tool Visualization 🎯
**Goal**: Implement rich response display with tool execution tracking

**Features**:
- ✅ Streaming markdown responses
- ✅ Code block highlighting
- ✅ Tool execution progress indicators
- ✅ File operation feedback
- ✅ Web search result display
- ✅ Error handling with user-friendly messages

### Phase 4: Advanced Features 🎯
**Goal**: Full feature parity with Mini-Agent capabilities

**Features**:
- ✅ Skills system integration
- ✅ Knowledge graph operations
- ✅ Session notes in chat context
- ✅ File references (`#file` mentions)
- ✅ Multi-turn conversation context
- ✅ Configuration UI in VS Code settings

### Phase 5: Testing & Documentation 🎯
**Goal**: Production-ready extension

**Deliverables**:
- ✅ Unit tests for all components
- ✅ Integration tests for ACP protocol
- ✅ End-to-end tests for VS Code extension
- ✅ User documentation
- ✅ Developer setup guide
- ✅ Troubleshooting guide

---

## 🎨 Design Principles (Mini-Agent Architecture Alignment)

### 1. Progressive Enhancement
- Start with minimal working prototype
- Add features incrementally
- Maintain backwards compatibility

### 2. Modular Design
- Clear separation of concerns (Extension ↔ ACP ↔ Core)
- Each layer has well-defined responsibilities
- Independent testing possible

### 3. Protocol Compliance
- Strict adherence to ACP specification
- Standard JSON-RPC 2.0 format
- Proper error handling

### 4. Native Capabilities First
- Use Mini-Agent's existing tools
- Preserve all current functionality
- Don't reinvent the wheel

### 5. Quality & Reliability
- Comprehensive error handling
- Graceful degradation
- Clear user feedback

---

## 📚 Reference Documentation

### Official Specifications
1. **Agent Client Protocol**: https://agentclientprotocol.com/
   - Protocol Overview: https://agentclientprotocol.com/protocol/overview
   - Transports: https://agentclientprotocol.com/protocol/transports
   - Message Schema: https://agentclientprotocol.com/protocol/schema

2. **VS Code Chat API**: https://code.visualstudio.com/api/extension-guides/ai/chat
   - Chat Participant API
   - Language Model API
   - Extension Guides

3. **Zed External Agents**: https://zed.dev/docs/ai/external-agents
   - Reference implementation guidance
   - Configuration examples

### Mini-Agent Internal References
1. **Architectural Mastery**: `documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md`
2. **ACP Integration Guide**: `documents/technical/ACP_INTEGRATION_GUIDE.md`
3. **System Architecture**: `documents/technical/SYSTEM_ARCHITECTURE.md`
4. **Project Context**: `documents/PROJECT_CONTEXT.md`

---

## 🚀 Next Steps

See the following detailed implementation guides:
1. **Phase 1 Guide**: `02_ACP_STDIO_SERVER_IMPLEMENTATION.md`
2. **Phase 2 Guide**: `03_VSCODE_EXTENSION_DEVELOPMENT.md`
3. **Phase 3 Guide**: `04_STREAMING_AND_VISUALIZATION.md`
4. **Phase 4 Guide**: `05_ADVANCED_FEATURES.md`
5. **Testing Guide**: `06_TESTING_AND_VALIDATION.md`

---

**Status**: ✅ **OVERVIEW COMPLETE**  
**Next Document**: Phase 1 - ACP Stdio Server Implementation  
**Ready for**: Technical implementation planning
