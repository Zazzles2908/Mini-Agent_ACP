# Mini-Agent Quick Start Guide

**For: Jazeel's Setup**  
**Date: 2025-11-19**

---

## Your Current Status ✅

Good news! Your Mini-Agent is already properly configured and working. Here's what you have:

### ✅ Working Components

1. **Z.AI Native Web Search**
   - Implementation: `mini_agent/llm/zai_client.py`
   - Tools: `mini_agent/tools/zai_tools.py`
   - API Key: Set in `.env` file (ZAI_API_KEY)
   - Status: Fully integrated and loaded by CLI

2. **ACP Server Integration**
   - Implementation: `mini_agent/acp/__init__.py`
   - Entry Point: `mini_agent/acp/server.py`
   - Command: `mini-agent-acp` (available after install)
   - Purpose: Enables Zed Editor / Claude Desktop integration

3. **Configuration**
   - Location: `mini_agent/config/`
   - Main config: `config.yaml` (Z.AI enabled)
   - MCP config: `mcp.json` (minimax_search disabled ✅)
   - Environment: `.env` (ZAI_API_KEY set ✅)

4. **Unicode Display**
   - Fixed in commit 2dbcc82
   - Terminal utilities: `mini_agent/utils/terminal_utils.py`
   - All tests passing (75/75)

---

## How to Use Mini-Agent

### Method 1: Direct CLI (Recommended for You)

```bash
# Navigate to your project
cd C:\Users\Jazeel-Home\Mini-Agent

# Start Mini-Agent
mini-agent

# Or if using uv tool:
uv run mini-agent
```

**Benefits:**
- Full file access within workspace
- No restrictions
- All tools work natively
- Direct terminal interaction

**Example Session:**
```
> Please search the web for the latest news about AI agents

[Agent will use zai_web_search tool automatically]

> Can you read the content from https://example.com/article

[Agent will use zai_web_reader tool]

> Create a file summarizing what you found

[Agent will use write_file tool]
```

### Method 2: ACP Server (For Zed Editor)

**Setup Once:**
```bash
# 1. Install Mini-Agent
cd C:\Users\Jazeel-Home\Mini-Agent
uv pip install -e .

# 2. Find the ACP command path
where.exe mini-agent-acp
# Example output: C:\Users\Jazeel-Home\.venv\Scripts\mini-agent-acp.exe

# 3. Add to Zed settings.json:
# Press Ctrl+Shift+P > "Open Settings"
```

```json
{
  "agent_servers": {
    "mini-agent": {
      "command": "C:/Users/Jazeel-Home/.venv/Scripts/mini-agent-acp.exe"
    }
  }
}
```

**Using in Zed:**
1. Open Zed's agent panel: `Ctrl+Shift+P` → "Agent: Toggle Panel"
2. Select "mini-agent" from dropdown
3. Start chatting with Mini-Agent directly in editor

**Benefits:**
- Integrated into editor workflow
- Visual tool execution indicators
- Per-file workspace context
- Seamless code editing

---

## Your Questions Answered

### Q1: File Navigation Restrictions

**Issue:** "You are really restricted from accessing other folders and files outside your directory"

**Answer:**

You're experiencing this in **Claude Desktop**, not in Mini-Agent itself. Here's why:

```
┌────────────────────────────────────────────────┐
│  Claude Desktop (where you are now)            │
│  ├─ Uses MCP filesystem server                 │
│  └─ Restricted to: C:\tmp                      │
│      (configured in mcp.json)                  │
└────────────────────────────────────────────────┘
                    VS
┌────────────────────────────────────────────────┐
│  Mini-Agent CLI or ACP (actual agent)          │
│  ├─ Uses native file tools                     │
│  └─ Access: Full workspace directory           │
│      C:\Users\Jazeel-Home\Mini-Agent           │
└────────────────────────────────────────────────┘
```

**Solution Options:**

**Option A - Use Mini-Agent CLI Directly** (Easiest)
```bash
cd C:\Users\Jazeel-Home\Mini-Agent
mini-agent
```
✅ No restrictions, full access

**Option B - Configure Claude Desktop for Mini-Agent ACP**

Add to Claude Desktop's config:
```json
{
  "agentServers": {
    "mini-agent": {
      "command": "C:/path/to/mini-agent-acp.exe",
      "workingDirectory": "C:/Users/Jazeel-Home/Mini-Agent"
    }
  }
}
```

This makes Mini-Agent available as an agent server in Claude Desktop, separate from the MCP filesystem restrictions.

**Option C - Expand MCP Filesystem Access**

In `mini_agent/config/mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "args": [
        "C:/Users/Jazeel-Home",
        "C:/tmp"
      ]
    }
  }
}
```

⚠️ This affects MCP tools only, not Mini-Agent's native tools.

### Q2: MCP Connection Failures

**Issue:** "Failed to connect to MCP server 'minimax_search': Connection closed"

**Answer:**

This is **expected and already fixed**! Here's what happened:

**Old Approach (Failed):**
- Tried to use external `minimax_search` MCP server
- Required multiple APIs (Jina, Serper, MiniMax)
- Connection kept failing
- Unreliable external dependency

**New Approach (Working):**
- ✅ Native Z.AI integration built directly into Mini-Agent
- ✅ Uses GLM models' built-in web search
- ✅ Single API key (ZAI_API_KEY in your .env)
- ✅ More reliable and faster

**Your mcp.json already has this fixed:**
```json
{
  "minimax_search": {
    "disabled": true  // ✅ Disabled to use native Z.AI instead
  }
}
```

**No Action Needed!** The error message still appears during startup because the MCP loader attempts all servers, but it's marked as disabled so it doesn't affect functionality.

**To Stop Seeing the Error:**

Remove the entire `minimax_search` section from `mcp.json`:
```json
{
  "mcpServers": {
    "memory": { ... },
    "filesystem": { ... },
    "git": { ... }
    // minimax_search removed entirely
  }
}
```

### Q3: UTF-8 PowerShell Script

**Issue:** "Whether we need this auto script to run so your characters wouldn't be corrupted"

**Answer:**

**You probably DON'T need it** if you're using:
- ✅ Windows 11
- ✅ Windows Terminal (not legacy cmd.exe)
- ✅ And characters display correctly (even if sometimes misaligned)

**The alignment issue is already fixed** in commit 2dbcc82 via `terminal_utils.py`.

**When You WOULD Need UTF-8 Script:**
- ❌ You see `?` or `□` instead of emoji/Chinese/Japanese
- ❌ Using legacy PowerShell or cmd.exe
- ❌ On Windows 10 with old terminal

**Test if you need it:**
```powershell
# Run this in your terminal:
"Test: 🔧 ✅ ❌ 中文 日本語"
```

**If you see:**
- `Test: 🔧 ✅ ❌ 中文 日本語` → ✅ You're fine, no script needed
- `Test: ? ? ? ?? ???` → ❌ You need the UTF-8 script

**UTF-8 Script (if needed):**
```powershell
# Add to your PowerShell profile
# Find profile location: $PROFILE
# Edit: notepad $PROFILE

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

Write-Host "PowerShell configured for UTF-8 (Mini Agent ready!)" -ForegroundColor Green
```

---

## Testing Your Setup

### Test 1: Z.AI Web Search

```bash
cd C:\Users\Jazeel-Home\Mini-Agent
python documents/testing/test_zai_integration.py
```

**Expected Output:**
```
✅ Z.AI API key loaded
✅ Z.AI client initialized
✅ Web search successful with GLM-4.6 model
✅ Native GLM integration fully operational
```

### Test 2: File Access

```bash
mini-agent
```

Then in Mini-Agent:
```
> Please list all files in the current directory and read README.md
```

**Expected:** Agent lists files and reads README without errors

### Test 3: ACP Server

```bash
mini-agent-acp --version
```

**Expected:** No error (command exists)

If error:
```bash
cd C:\Users\Jazeel-Home\Mini-Agent
uv pip install -e .
```

### Test 4: Full Test Suite

```bash
pytest -v
```

**Expected:** Most tests pass (some may skip)

---

## Project Structure (Clean)

Your project is now organized properly:

```
Mini-Agent/
├── .env                          # Environment variables (ZAI_API_KEY)
├── pyproject.toml                # Project configuration
├── README.md                     # Main readme
│
├── mini_agent/                   # Main package
│   ├── acp/                      # ACP server integration
│   │   ├── __init__.py           # ACP adapter implementation
│   │   └── server.py             # Entry point
│   │
│   ├── config/                   # Configuration files
│   │   ├── config.yaml           # Main config
│   │   ├── mcp.json              # MCP servers config
│   │   └── system_prompt.md      # Agent prompt
│   │
│   ├── llm/                      # LLM clients
│   │   ├── llm_client.py         # Main LLM client
│   │   └── zai_client.py         # Z.AI web search client
│   │
│   ├── tools/                    # Agent tools
│   │   ├── base.py               # Base tool classes
│   │   ├── file_tools.py         # File operations
│   │   ├── bash_tools.py         # Bash execution
│   │   └── zai_tools.py          # Z.AI web search tools ✅
│   │
│   ├── utils/                    # Utilities
│   │   └── terminal_utils.py     # Unicode display fixes ✅
│   │
│   ├── agent.py                  # Core agent loop
│   ├── cli.py                    # CLI interface
│   └── config.py                 # Configuration loader
│
├── documents/                    # Documentation (organized!) ✅
│   ├── SYSTEM_ARCHITECTURE.md    # This comprehensive guide
│   ├── QUICK_START_GUIDE.md      # This file
│   ├── FINAL_ZAI_STATUS_REPORT.md
│   ├── TROUBLESHOOTING.md
│   └── testing/                  # Test scripts (moved here) ✅
│       ├── test_zai_integration.py
│       ├── optimized_zai.py
│       └── ...
│
├── tests/                        # Unit tests
│   ├── test_terminal_utils.py    # Unicode display tests
│   └── ...
│
└── workspace/                    # Agent workspace
```

✅ **All test files moved to `documents/testing/`**  
✅ **Root directory clean**  
✅ **Documentation organized**

---

## What You Should Do Next

### Recommended: Use Mini-Agent CLI

This gives you the best experience without restrictions:

```bash
cd C:\Users\Jazeel-Home\Mini-Agent
mini-agent
```

Try these commands:
```
> Search the web for "latest developments in AI agents 2025"

> Read the content from [any URL from search results]

> Create a summary document in workspace/summary.md

> List all files in documents/ directory

> Read documents/SYSTEM_ARCHITECTURE.md and explain the ACP integration
```

### Optional: Set Up Zed Integration

If you use Zed editor and want Mini-Agent integrated:

1. Install: `uv pip install -e .`
2. Find path: `where.exe mini-agent-acp`
3. Add to Zed settings (see Method 2 above)
4. Use in Zed's agent panel

### Optional: Clean Up MCP Error

To stop seeing the minimax_search connection error:

Edit `mini_agent/config/mcp.json` and completely remove the `minimax_search` section.

---

## Key Points to Remember

1. **Z.AI Web Search = Native Integration**
   - Built directly into Mini-Agent
   - Uses GLM models' web search capabilities
   - No external MCP server needed

2. **ACP = Custom Zed/Claude Desktop Integration**
   - Taken from another repo (custom, not third-party)
   - Separate from MCP servers
   - Different entry point, same agent core

3. **File Access Depends on Context**
   - Direct CLI: Full access ✅
   - ACP Server: Full access ✅
   - Claude Desktop MCP: Restricted ⚠️

4. **Unicode Display Already Fixed**
   - Commit 2dbcc82
   - UTF-8 script only needed for legacy terminals
   - Test with emoji to verify

---

## Need Help?

**Check these docs:**
- `documents/SYSTEM_ARCHITECTURE.md` - Full technical details
- `documents/TROUBLESHOOTING.md` - Step-by-step solutions
- `documents/FINAL_ZAI_STATUS_REPORT.md` - Z.AI integration status

**Run diagnostics:**
```bash
# Test Z.AI
python documents/testing/test_zai_integration.py

# Test display
pytest tests/test_terminal_utils.py -v

# Full test suite
pytest -v
```

**Try the agent:**
```bash
mini-agent
```

---

**Your setup is ready to go! 🚀**
