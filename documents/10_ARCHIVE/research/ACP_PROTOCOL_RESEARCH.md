# ACP (Agent Client Protocol) Research Summary

**Date:** 2025-11-19  
**Sources:**  
- https://agentclientprotocol.com/protocol/overview
- https://zed.dev/docs/ai/external-agents

---

## What is ACP?

**Agent Client Protocol (ACP)** is an **open, standardized protocol** designed to enable seamless communication and interoperability between AI agents and client applications. It's described as "TCP/IP for AI agents" or "USB for AI services."

---

## The Problem ACP Solves

### Current State (Siloed AI):
- ❌ One-off integrations between agents and apps
- ❌ No interoperability between different agents/clients
- ❌ High development cost (custom integration every time)
- ❌ Difficult to chain multiple agents together

### ACP Solution:
- ✅ Standardized communication protocol
- ✅ Any ACP agent can work with any ACP client
- ✅ Composable AI workflows
- ✅ Reduced development overhead

---

## ACP Architecture: Three Components

### 1. **Agents (The Workers)**
- Autonomous services that perform specific tasks
- Advertise their "Capabilities" (e.g., "book-a-flight", "summarize-document")
- Execute tasks on behalf of users
- Run as separate processes

### 2. **Clients (The Applications)**
- User-facing applications (web apps, mobile apps, terminals, Slack bots)
- Capture user intent and translate to ACP requests
- Present results back to users
- Example: Zed editor, VS Code (with extensions)

### 3. **Orchestrators (The Marketplace)**
- Central hub maintaining registry of agents and capabilities
- **Discovery**: Finds agents with required capabilities
- **Mediation**: Facilitates connections between clients and agents
- **Management**: Handles agent lifecycle, monitoring, routing

---

## How ACP Works: Interaction Flow

```
1. Agent Advertisement
   Agent → Orchestrator: "I am AcmeTravelAgent, I can book-a-flight"

2. Client Request  
   User → Client: "Book a flight from SFO to JFK"
   Client → Orchestrator: "I need book-a-flight capability"

3. Orchestration
   Orchestrator searches registry → Finds AcmeTravelAgent
   Orchestrator → Client: "Connect to AcmeTravelAgent"

4. Connection & Communication
   Client ↔ Agent: Direct communication using ACP messages
   (gathering info, processing, execution)

5. Result Delivery
   Agent → Client: Booking confirmation
   Client → User: Display results
```

---

## Communication Method

**JSON-RPC over stdin/stdout**
- Client and Agent communicate through standard input/output
- JSON messages for requests and responses
- Async message passing
- Event handling for long-running tasks

---

## Real-World Implementation: Zed Editor

### Zed's External Agents

Zed supports **terminal-based agents through ACP**, including:

1. **Gemini CLI** (reference implementation)
   - Installation: `@google/gemini-cli`
   - Authentication: Google OAuth or API key
   - Managed by Zed, updated automatically

2. **MiniMax-M2 Code** (included by default)
   - Installation: `@zed-industries/minimax-code-acp`
   - Authentication: Separate from Zed (API key or MiniMax-M2 Pro)
   - Runs via ACP adapter

3. **Custom ACP-compatible agents**
   - Any agent implementing ACP can be added

### How Zed Uses ACP

```typescript
// Zed configuration example
{
  "agent_servers": {
    "gemini": {
      "ignore_system_version": false
    },
    "minimax": {
      "env": {
        "MINIMAX_CODE_EXECUTABLE": "/path/to/executable"
      }
    }
  }
}
```

**Key Features:**
- Agent panel UI (cmd-? / ctrl-?)
- Keyboard shortcuts for new threads
- @-mention files, symbols, threads
- Web fetching capabilities
- File editing integration

### Important Notes from Zed:
- ⚠️ **Billing is direct** between user and agent provider
- ⚠️ Zed does **not charge** for external agents
- ⚠️ Privacy guarantees **only for Zed's hosted models**
- ⚠️ External agents use **your own API keys/billing**

---

## Mini-Agent ACP Implementation Requirements

### Current Status
Mini-Agent has basic ACP implementation in `mini_agent/acp/`:
- `__init__.py` - MiniMaxACPAgent class
- `server.py` - Entry point

### Required Capabilities (Based on Research)

1. **Agent Capabilities Declaration** ✅ Partially implemented
   ```python
   async def initialize(self, params):
       return AgentCapabilities(
           loadSession=False,
           # Need to add more capabilities
       )
   ```

2. **Session Management** ✅ Implemented
   - `newSession()` - Creates agent sessions
   - `cancelSession()` - Cancels running sessions
   - `cleanup()` - Cleanup on shutdown

3. **Prompt Handling** ✅ Implemented
   - `prompt()` - Process user requests

4. **Communication Protocol** ✅ Using official ACP package
   - Uses `stdio_streams()` for IPC
   - JSON-RPC message passing
   - Async operations

### What Needs Enhancement

1. **Advertise Native Capabilities**
   - Declare Z.AI web search capability
   - Declare file operations capability
   - Declare code execution capability

2. **Orchestrator Integration** (Optional)
   - Currently standalone
   - Could integrate with ACP orchestrator for discovery

3. **VS Code Extension Integration**
   - Extension should launch Mini-Agent via ACP
   - Similar to Zed's approach
   - Direct communication over stdio

---

## VS Code Extension Requirements

### Based on Zed Model

**Current Mini-Agent VS Code Extension:**
```json
// package.json
{
  "miniAgent.acpServerPath": "python -m mini_agent.acp.server"
}
```

**Should Support:**

1. **Agent Panel UI**
   - Similar to Zed's agent panel
   - Start/stop agent threads
   - Message history
   - File context (@-mentions)

2. **Communication**
   - Launch ACP server via stdio
   - JSON-RPC message passing
   - Async request/response

3. **Authentication**
   - Use user's API keys (not VS Code's)
   - Separate billing (user pays directly)
   - Secure key storage

4. **Features**
   - @-mention files in workspace
   - Web search integration
   - Code editing capabilities
   - Multi-turn conversations

---

## Key Differences: Mini-Agent vs Zed Implementation

| Aspect | Zed | Mini-Agent Current | Mini-Agent Should Be |
|--------|-----|-------------------|---------------------|
| **Protocol** | ACP (JSON-RPC) | ACP (JSON-RPC) | ✅ Same |
| **Installation** | Managed by Zed | Manual | Auto-install in extension |
| **Authentication** | Separate from Zed | Separate (.env) | ✅ Same (user's keys) |
| **Capabilities** | Advertised upfront | Not declared | **Needs improvement** |
| **UI Integration** | Native panel | Terminal-based | **Needs native panel** |
| **Web Search** | Via @web | Via tool | **Native Z.AI integration** |

---

## Action Items for Mini-Agent

### 1. Enhance ACP Server ✅ Already Correct
- ✅ Uses official `acp` Python package
- ✅ Implements required methods
- ✅ stdio_streams communication

### 2. Declare Capabilities
```python
class MiniMaxACPAgent:
    def get_capabilities(self):
        return [
            {
                "name": "web_search",
                "description": "Search the web using Z.AI",
                "provider": "zai"
            },
            {
                "name": "file_operations",  
                "description": "Read, write, edit files"
            },
            {
                "name": "code_execution",
                "description": "Execute bash/python code"
            }
        ]
```

### 3. Update VS Code Extension
- Add agent panel UI
- Implement message passing
- Add @-mention support for files
- Integrate Z.AI web search natively

### 4. Documentation
- Update README with ACP information
- Add VS Code extension setup guide
- Document capability declarations

---

## Benefits of Proper ACP Implementation

1. **Interoperability**
   - Mini-Agent can work with any ACP client (Zed, VS Code, custom)
   - Other ACP agents can be added to Mini-Agent ecosystem

2. **Standardization**
   - Follow established protocol (like TCP/IP)
   - Easier for developers to integrate
   - Community support and tooling

3. **Composability**
   - Chain Mini-Agent with other ACP agents
   - Build complex AI workflows
   - Specialize agents for specific tasks

4. **Ecosystem Growth**
   - Participate in emerging ACP marketplace
   - Agents as services model
   - Reduced custom integration work

---

## References

- **ACP Overview:** https://agentclientprotocol.com/protocol/overview
- **Zed External Agents:** https://zed.dev/docs/ai/external-agents
- **ACP Python Package:** `acp` (already used in Mini-Agent)
- **Gemini CLI:** `@google/gemini-cli` (reference implementation)
- **MiniMax-M2 Code:** `@zed-industries/minimax-code-acp`

---

## Conclusion

**Mini-Agent is already on the right track** with ACP implementation using the official Python package. The key enhancements needed are:

1. ✅ **ACP Server** - Already correct
2. 🔧 **Capability Declaration** - Needs enhancement
3. 🔧 **VS Code Extension** - Needs native UI panel
4. ✅ **Z.AI Integration** - Already working via direct REST API

**The foundation is solid, just needs polish for full ACP compliance and better UX.**
