# Mini-Agent Visual Architecture Guide

**Quick Visual Reference for Understanding the System**

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
│  │  • LLM Client (mini_agent/llm/llm_client.py)                │   │
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

## Z.AI Web Search: Old vs New

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│               OLD APPROACH (Failed) ❌                              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  User Query                                                         │
│      ↓                                                              │
│  Mini-Agent                                                         │
│      ↓                                                              │
│  MCP Client (attempts connection)                                   │
│      ↓                                                              │
│  minimax_search MCP Server (external)                               │
│      ↓                                                              │
│  ❌ Connection Failed!                                              │
│                                                                     │
│  Why it failed:                                                     │
│  • External dependency (uvx package)                                │
│  • Multiple API keys needed (Jina, Serper, MiniMax)                │
│  • Installation issues                                              │
│  • Unreliable connections                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│               NEW APPROACH (Working) ✅                             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  User Query                                                         │
│      ↓                                                              │
│  Mini-Agent CLI                                                     │
│      ↓                                                              │
│  ZAIWebSearchTool (mini_agent/tools/zai_tools.py)                  │
│      ↓                                                              │
│  ZAIClient (mini_agent/llm/zai_client.py)                          │
│      ↓                                                              │
│  Z.AI API (https://api.z.ai)                                        │
│      ↓                                                              │
│  GLM Model with Search Prime Engine                                 │
│      ↓                                                              │
│  ✅ Web Search Results + AI Analysis                               │
│                                                                     │
│  Why it works:                                                      │
│  • Native integration (no external server)                          │
│  • Single API key (ZAI_API_KEY in .env)                            │
│  • Built into GLM models                                            │
│  • Reliable and fast                                                │
│                                                                     │
│  Available Model:                                                  │
│  • glm-4.6        → Only model available on Lite plan               │
│                   → Web search and web reading capabilities          │
│                   → FREE: 100 searches + 100 readers                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ACP Integration: What It Really Is

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│         ACP = Agent Client Protocol (Custom Integration)            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  What it does:                                                      │
│  • Enables Mini-Agent to work as a server for code editors          │
│  • Provides structured communication protocol                       │
│  • Allows multiple simultaneous sessions                            │
│  • Shows tool execution visually in editors                         │
│                                                                     │
│  What it is NOT:                                                    │
│  • ❌ Not a limitation on Mini-Agent                                │
│  • ❌ Not a file access restrictor                                  │
│  • ❌ Not required for basic usage                                  │
│  • ❌ Not a third-party dependency (custom code)                    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                                                         │       │
│  │  Zed Editor                  mini-agent-acp Server     │       │
│  │  ┌─────────────┐              ┌──────────────────┐    │       │
│  │  │             │              │                  │    │       │
│  │  │ User types  │  Initialize  │ Creates session  │    │       │
│  │  │ question    ├─────────────►│ with workspace   │    │       │
│  │  │             │              │                  │    │       │
│  │  │             │   Prompt     │ Runs agent loop  │    │       │
│  │  │             ├─────────────►│ Executes tools   │    │       │
│  │  │             │              │                  │    │       │
│  │  │             │SessionUpdate │ Returns results  │    │       │
│  │  │ Sees        │◄─────────────┤ with thinking    │    │       │
│  │  │ results     │              │ and tool calls   │    │       │
│  │  │             │              │                  │    │       │
│  │  └─────────────┘              └──────────────────┘    │       │
│  │                                                         │       │
│  │  Visual feedback in editor:                            │       │
│  │  🔧 Tool: read_file(path="README.md")                  │       │
│  │  ✅ Result: Successfully read 1,234 bytes              │       │
│  │                                                         │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                     │
│  Files:                                                             │
│  • mini_agent/acp/__init__.py   → ACP adapter implementation       │
│  • mini_agent/acp/server.py     → Entry point script               │
│                                                                     │
│  How to use:                                                        │
│  1. Install: pip install agent-client-protocol                     │
│  2. Find path: where.exe mini-agent-acp                            │
│  3. Add to Zed settings.json                                       │
│  4. Select "mini-agent" in Zed's agent panel                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    HOW CONFIGURATION WORKS                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Startup Sequence:                                                  │
│  ────────────────                                                   │
│                                                                     │
│  1. Load Environment Variables                                      │
│     ┌──────────────────────────────┐                               │
│     │ .env file (root directory)   │                               │
│     │                              │                               │
│     │ ZAI_API_KEY=your_key_here    │                               │
│     └──────────────────────────────┘                               │
│                ↓                                                    │
│  2. Load Main Configuration                                         │
│     ┌──────────────────────────────────────┐                       │
│     │ mini_agent/config/config.yaml        │                       │
│     │                                      │                       │
│     │ api_key: minimax_key                 │                       │
│     │ model: MiniMax-M2                    │                       │
│     │ tools:                               │                       │
│     │   enable_zai_search: true   ← ✅     │                       │
│     │   enable_skills: true                │                       │
│     │   enable_mcp: true                   │                       │
│     └──────────────────────────────────────┘                       │
│                ↓                                                    │
│  3. Load MCP Configuration                                          │
│     ┌──────────────────────────────────────┐                       │
│     │ mini_agent/config/mcp.json           │                       │
│     │                                      │                       │
│     │ {                                    │                       │
│     │   "mcpServers": {                    │                       │
│     │     "minimax_search": {              │                       │
│     │       "disabled": true  ← ✅         │                       │
│     │     },                               │                       │
│     │     "memory": {                      │                       │
│     │       "disabled": false              │                       │
│     │     }                                │                       │
│     │   }                                  │                       │
│     │ }                                    │                       │
│     └──────────────────────────────────────┘                       │
│                ↓                                                    │
│  4. Load Tools Based on Configuration                               │
│     ┌──────────────────────────────────────┐                       │
│     │ mini_agent/cli.py                    │                       │
│     │                                      │                       │
│     │ if config.tools.enable_zai_search:   │                       │
│     │     ✅ Load ZAIWebSearchTool         │                       │
│     │     ✅ Load ZAIWebReaderTool         │                       │
│     │                                      │                       │
│     │ if config.tools.enable_skills:       │                       │
│     │     ✅ Load Skills                   │                       │
│     │                                      │                       │
│     │ if config.tools.enable_mcp:          │                       │
│     │     ✅ Load enabled MCP servers      │                       │
│     │     ❌ Skip disabled servers         │                       │
│     └──────────────────────────────────────┘                       │
│                ↓                                                    │
│  5. Agent Ready with All Tools                                      │
│     ┌──────────────────────────────────────┐                       │
│     │ Available Tools:                     │                       │
│     │ • read_file                          │                       │
│     │ • write_file                         │                       │
│     │ • edit_file                          │                       │
│     │ • bash                               │                       │
│     │ • zai_web_search        ← ✅         │                       │
│     │ • zai_web_reader        ← ✅         │                       │
│     │ • get_skill                          │                       │
│     │ • [MCP tools from servers]           │                       │
│     └──────────────────────────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree: What Should I Use?

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                 WHICH MODE SHOULD I USE?                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ What do you want     │
                   │ to do?               │
                   └──────────┬───────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ Quick tasks  │   │ Integrated   │   │ Just talking │
    │ Research     │   │ with code    │   │ to MiniMax-M2    │
    │ File work    │   │ editor       │   │              │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ USE:         │   │ USE:         │   │ USE:         │
    │              │   │              │   │              │
    │ mini-agent   │   │ mini-agent-  │   │ MiniMax-M2       │
    │ (CLI)        │   │ acp          │   │ Desktop      │
    │              │   │ (Zed)        │   │              │
    │ ✅ FULL      │   │ ✅ FULL      │   │ ⚠️ LIMITED   │
    │ ACCESS       │   │ ACCESS       │   │ ACCESS       │
    │              │   │              │   │              │
    │ • No limits  │   │ • Editor     │   │ • /tmp only  │
    │ • All tools  │   │   context    │   │ • No Mini-   │
    │ • Fast       │   │ • Visual     │   │   Agent      │
    │              │   │   feedback   │   │   tools      │
    └──────────────┘   └──────────────┘   └──────────────┘
```

**Recommendation:** Use `mini-agent` CLI for best experience!

---

## Summary Visual

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                    YOUR SYSTEM STATUS                             ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Component              Status          Location                 ║
║  ─────────────────────  ─────────────   ──────────────────────   ║
║                                                                   ║
║  Z.AI Web Search        ✅ Working      mini_agent/llm/          ║
║                                         zai_client.py            ║
║                                                                   ║
║  Z.AI Tools             ✅ Working      mini_agent/tools/        ║
║                                         zai_tools.py             ║
║                                                                   ║
║  ACP Server             ✅ Available    mini_agent/acp/          ║
║                                                                   ║
║  Native File Tools      ✅ Working      mini_agent/tools/        ║
║                         (No limits)     file_tools.py            ║
║                                                                   ║
║  Configuration          ✅ Correct      mini_agent/config/       ║
║                                         config.yaml              ║
║                                                                   ║
║  MCP minimax_search     ✅ Disabled     mini_agent/config/       ║
║                         (As intended)   mcp.json                 ║
║                                                                   ║
║  Unicode Display        ✅ Fixed        mini_agent/utils/        ║
║                                         terminal_utils.py        ║
║                                                                   ║
║  Documentation          ✅ Complete     documents/               ║
║                         (60KB total)                             ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  READY TO USE! Run: mini-agent                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

**Read the documentation in `documents/` for complete details!**

Start with: `documents/QUICK_START_GUIDE.md`
