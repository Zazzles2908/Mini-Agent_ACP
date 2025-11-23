# Mini-Agent Visual Architecture Guide (Essential)
**Core Visual Architecture Reference**

**Created**: November 24, 2025  
**Purpose**: Essential visual concepts for understanding Mini-Agent  
**Archive**: Extended examples moved to archive

---

## The Big Picture

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                         YOUR MINI-AGENT SYSTEM                        │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    ENTRY POINTS                              │    │
│  │  (How you interact with Mini-Agent)                          │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │                                                              │    │
│  │   1. mini-agent                2. mini-agent-acp            │    │
│  │      (CLI Direct)                  (ACP Server)             │    │
│  │      Terminal use                  Zed/MiniMax-M2 Desktop       │    │
│  │      ✅ RECOMMENDED                ✅ Optional               │    │
│  │                                                              │    │
│  └───────────────────┬─────────────────┬────────────────────────┘    │
│                      │                 │                             │
│                      ▼                 ▼                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              CORE AGENT RUNTIME                               │   │
│  │  (Same for both entry points)                                 │   │
│  │                                                               │   │
│  │  • Agent Loop (mini_agent/agent.py)                          │   │
│  │  • LLM Client (mini_agent/llm/llm_wrapper.py)               │   │
│  │  • Tool Management                                           │   │
│  │  • Message History                                           │   │
│  │                                                               │   │
│  └────────────────────────┬─────────────────────────────────────┘   │
│                           │                                          │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     TOOL LAYERS                               │   │
│  │  (All the capabilities)                                       │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│   │
│  │  │ Native Tools   │  │  Z.AI Tools    │  │ Skills         ││   │
│  │  │                │  │                │  │                ││   │
│  │  │ • File ops     │  │ • Web search   │  │ • PDF/DOCX     ││   │
│  │  │ • Bash exec    │  │ • Web reader   │  │ • Presentations││   │
│  │  │ • Session notes│  │ ✅ WORKING     │  │ • Art/Design   ││   │
│  │  │ ✅ WORKING     │  │                │  │ ✅ WORKING     ││   │
│  │  │                │  │                │  │                ││   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘│   │
│  │                                                               │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ MCP Servers (External)                                 │ │   │
│  │  │                                                        │ │   │
│  │  │ • Memory (knowledge graph)    ✅ Enabled              │ │   │
│  │  │ • Git operations              ✅ Enabled              │ │   │
│  │  │ • Filesystem (restricted)     ⚠️  Limited to /tmp     │ │   │
│  │  │ • minimax_search              ❌ Disabled (obsolete)  │ │   │
│  │  │                                                        │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## File Access: Understanding the Contexts

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                  WHERE ARE YOU RUNNING?                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Context 1: Mini-Agent CLI                                          │
│  ┌─────────────────────────────────────────────────────┐           │
│  │ $ cd C:\Users\Jazeel-Home\Mini-Agent                │           │
│  │ $ mini-agent                                        │           │
│  │                                                     │           │
│  │ File Access:                                        │           │
│  │ ✅ C:\Users\Jazeel-Home\Mini-Agent\*                │           │
│  │ ✅ ./workspace/*                                    │           │
│  │ ✅ All files within workspace directory             │           │
│  │                                                     │           │
│  │ Tools Used: Native file tools                       │           │
│  │ Restrictions: NONE                                  │           │
│  │                                                     │           │
│  │ Status: ✅ RECOMMENDED - Full access               │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                     │
│  Context 2: Mini-Agent ACP (via Zed/MiniMax-M2 Desktop)                │
│  ┌─────────────────────────────────────────────────────┐           │
│  │ Zed Editor → mini-agent-acp server                  │           │
│  │                                                     │           │
│  │ File Access:                                        │           │
│  │ ✅ Session workspace (from editor)                  │           │
│  │ ✅ All files within session workspace               │           │
│  │                                                     │           │
│  │ Tools Used: Native file tools                       │           │
│  │ Restrictions: Per-session workspace only            │           │
│  │                                                     │           │
│  │ Status: ✅ OPTIONAL - For editor integration       │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                     │
│  Context 3: MiniMax-M2 Desktop (Direct - NOT Mini-Agent)                │
│  ┌─────────────────────────────────────────────────────┐           │
│  │ MiniMax-M2 Desktop → MCP filesystem server              │           │
│  │                                                     │           │
│  │ File Access:                                        │           │
│  │ ⚠️  C:\tmp only (configured in mcp.json)            │           │
│  │ ❌ Other directories blocked by MCP server          │           │
│  │                                                     │           │
│  │ Tools Used: MCP filesystem tool (external)          │           │
│  │ Restrictions: Configured in mcp.json                │           │
│  │                                                     │           │
│  │ Status: ⚠️  THIS IS WHERE YOU SAW RESTRICTIONS     │           │
│  │                                                     │           │
│  │ NOTE: This is NOT Mini-Agent! It's MiniMax-M2 Desktop's│           │
│  │       external MCP filesystem server (different)    │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**The Confusion Explained:**
You were using **MiniMax-M2 Desktop** (Context 3), which has its own MCP filesystem server with restrictions. This is **separate** from Mini-Agent's native file tools (Contexts 1 & 2).

---

## Z.AI Web Search: Current Implementation

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│               CURRENT APPROACH (Working) ✅                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  User Query                                                         │
│      ↓                                                              │
│  Mini-Agent CLI                                                     │
│      ↓                                                              │
│  ZAIWebTool (mini_agent/tools/zai_web_tool.py)                      │
│      ↓                                                              │
│  Z.AI MCP Servers (remote)                                          │
│      ↓                                                              │
│  MCP First Strategy (FREE quotas)                                   │
│      ↓                                                              │
│  ✅ Web Search + Reading Results                                    │
│                                                                     │
│  Features:                                                          │
│  • FREE quotas: 100 searches + 100 readers per day                  │
│  • MCP Protocol: Standard communication                             │
│  • Credit Protection: Automatic usage tracking                      │
│  • Fallback: Direct API when MCP unavailable                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Components Summary

### **Agent Runtime**
- **File**: `mini_agent/agent.py` - Core execution loop
- **Functions**: Tool calling, message management, context handling
- **Entry Points**: CLI direct + ACP server

### **LLM Integration** 
- **Provider**: MiniMax-M2 via OpenAI protocol
- **Client**: `mini_agent/llm/llm_wrapper.py`
- **Configuration**: `mini_agent/config/config.yaml`

### **Tool System**
- **Native Tools**: File operations, bash execution, session notes
- **Z.AI Tools**: Web search and reading (MCP-first)
- **Skills**: PDF, presentations, art/design generation
- **MCP Servers**: Memory, Git, MiniMax coding plan

### **Configuration**
- **Main Config**: `config.yaml` (LLM, tools, retry settings)
- **MCP Config**: `.mcp.json` (server definitions)
- **Environment**: `.env` (API keys)

---

## Quick Reference Commands

```bash
# Start Mini-Agent CLI
cd /path/to/mini-agent
mini-agent

# Start Mini-Agent ACP Server  
python -m mini_agent.acp

# Check configuration
mini-agent --help

# Test tools
# (Via interactive session)
```

---

## Related Documentation

- **System Architecture**: `MASTER_SYSTEM_ARCHITECTURE_COMPLETE.md`
- **Web Functionality**: `../14_WEB/MINI_AGENT_WEB_FUNCTIONALITY_OVERVIEW.md`
- **VS Code Integration**: `VSCODE_INTEGRATION_GUIDE.md`
- **Configuration**: `../04_SETUP_CONFIG/CONFIGURATION.md`

---

**This essential guide covers the core visual concepts. Extended examples and detailed explanations are available in the archive.**