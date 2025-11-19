# Mini-Agent Command Fix

## Problem
The `mini-agent` command was hanging/not working due to conflicting executables.

## Root Cause
Two versions of mini-agent were installed:
1. **Broken `.bat` file**: `C:\Users\Jazeel-Home\.local\bin\mini-agent.bat` - Using old `python -m mini_agent.cli` approach causing import errors
2. **Working `.exe` file**: `C:\Users\Jazeel-Home\AppData\Roaming\Python\Python313\Scripts\mini-agent.exe` - Proper installation

## Fix Applied
**Removed the broken `.bat` file** that was interfering with the proper executable:
```powershell
Remove-Item -Path "C:\Users\Jazeel-Home\.local\bin\mini-agent.bat" -Force
```

## How the System Works Now

### 1. **Command Installation**
- Package installed via: `pip install -e .` (development mode)
- Entry point defined in `pyproject.toml`: `mini-agent = "mini_agent.cli:main"`
- Executable location: `C:\Users\Jazeel-Home\AppData\Roaming\Python\Python313\Scripts\mini-agent.exe`

### 2. **How to Use It**
Simply type in your terminal:
```bash
mini-agent                              # Use current directory as workspace
mini-agent --workspace /path/to/dir     # Use specific workspace directory
mini-agent --help                        # Show help
mini-agent --version                     # Show version
```

### 3. **What Happens When You Run `mini-agent`**

**Step 1: Command Resolution**
- Windows searches PATH for `mini-agent.exe`
- Finds executable in Python Scripts directory

**Step 2: Entry Point Execution**
- `mini-agent.exe` calls `mini_agent.cli:main()` function
- Entry point defined in `pyproject.toml`

**Step 3: Configuration Loading**
- Loads `.env` from current directory (if exists)
- Searches for config in priority order:
  1. `./mini_agent/config/config.yaml` (development)
  2. `~/.mini-agent/config/config.yaml` (user config)
  3. `<package>/config/config.yaml` (installed package)

**Step 4: Tool Initialization**
- Loads base tools (bash, Z.AI search, skills, MCP)
- Adds workspace-dependent tools (file operations, session notes)
- All tools configured from `mini_agent/config/config.yaml`

**Step 5: MCP Integration**
- Loads MCP servers from `mini_agent/config/mcp.json`
- Initializes configured servers (memory, filesystem, git)
- Exposes MCP tools to the agent

**Step 6: Interactive Session**
- Displays welcome banner with session info
- Enters interactive loop with prompt_toolkit
- Agent ready to process user requests

### 4. **Configuration Files**

**Main Config: `mini_agent/config/config.yaml`**
- LLM provider (MiniMax with Anthropic provider)
- Model selection (abab7.5-chat-preview)
- Tool enablement flags
- Retry configuration
- Agent settings (max_steps, system_prompt path)

**MCP Config: `mini_agent/config/mcp.json`**
- MCP server definitions
- Currently active: memory, filesystem, git
- Each server has command, args, environment variables

**Environment: `.env`**
- API keys (MINIMAX_API_KEY, ZAI_API_KEY)
- Sensitive credentials
- Loaded automatically when mini-agent starts

### 5. **System Architecture**

```
mini-agent command
    ↓
mini-agent.exe (Python Scripts)
    ↓
mini_agent.cli:main()
    ↓
Load Config (config.yaml)
    ↓
Initialize LLM Client (MiniMax M2)
    ↓
Load Tools (39+ tools total)
    ├── Bash tools
    ├── Z.AI Web Search & Reader
    ├── File operation tools (workspace-aware)
    ├── Skill tools (get_skill)
    ├── MCP tools (memory, filesystem, git)
    └── Session note tool
    ↓
Load System Prompt (system_prompt.md)
    ↓
Create Agent Instance
    ↓
Interactive REPL Loop
```

## Verification

**Check installation:**
```bash
where.exe mini-agent
# Output: C:\Users\Jazeel-Home\AppData\Roaming\Python\Python313\Scripts\mini-agent.exe
```

**Test command:**
```bash
mini-agent --help
# Shows help text - confirms working
```

**Start agent:**
```bash
mini-agent
# Launches interactive session
```

## Notes

- **No more `.bat` files needed** - The Python package installer creates proper executables
- **Clean PATH** - Only one mini-agent executable in PATH
- **Development mode** - Using `pip install -e .` means code changes take effect immediately
- **Workspace flexibility** - Can specify any workspace directory via `--workspace` flag
