# Mini-Agent Troubleshooting Guide

## Issue 1: File Navigation Restrictions (`C:\tmp` only)

### Problem
When running Mini-Agent through MiniMax-M2 Desktop's ACP integration, file access is restricted to `C:\tmp` only. The agent reports:
```
Allowed directories:
C:\tmp
```

### Root Cause
This restriction comes from the ACP (Agent Client Protocol) server configuration. When MiniMax-M2 Desktop invokes mini-agent as an ACP server, it needs to be explicitly configured with allowed directories.

### Solution

#### Option 1: Add agentServers Configuration to MiniMax-M2 Desktop (Recommended)

Add the following to your `minimax_desktop_config.json` located at:
`C:\Users\Jazeel-Home\AppData\Roaming\MiniMax-M2\minimax_desktop_config.json`

```json
{
  "mcpServers": {
    // ... your existing MCP servers ...
  },
  "agentServers": {
    "mini-agent": {
      "command": "uv",
      "args": ["run", "mini-agent-acp"],
      "cwd": "C:/Users/Jazeel-Home/Mini-Agent",
      "allowedDirectories": [
        "C:/Users/Jazeel-Home",
        "C:/Project",
        "C:/tmp"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Note:** Make sure to:
1. Add comma after the `mcpServers` closing brace if agentServers is added
2. Adjust paths to match your system
3. Restart MiniMax-M2 Desktop after making changes

#### Option 2: Modify ACP Server Code (For Development)

If you need to modify the allowed directories programmatically, edit:
`C:\Users\Jazeel-Home\Mini-Agent\mini_agent\acp\__init__.py`

However, this is not recommended as it should be configured through MiniMax-M2 Desktop's config.

#### Option 3: Use Direct CLI Mode

Run mini-agent directly from the command line instead of through MiniMax-M2 Desktop:
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
uv run mini-agent
```

In this mode, file operations work relative to the workspace directory without ACP restrictions.

---

## Issue 2: MCP Server Connection Failure (minimax_search)

### Problem
```
✗ Failed to connect to MCP server 'minimax_search': Connection closed
Traceback (most recent call last):
  File "C:\Users\Jazeel-Home\Mini-Agent\mini_agent\tools\mcp_loader.py", line 107
    await session.initialize()
    ...
mcp.shared.exceptions.McpError: Connection closed
```

### Root Cause
The `minimax_search` MCP server is attempting to install from GitHub using `uvx --from git+https://github.com/MiniMax-AI/minimax_search` but the installation or initialization is failing.

### Diagnosis Steps

1. **Test manual installation:**
```powershell
uvx --from git+https://github.com/MiniMax-AI/minimax_search minimax-search --help
```

2. **Check if the repository exists and is accessible:**
```powershell
git ls-remote https://github.com/MiniMax-AI/minimax_search
```

3. **Verify API keys are set correctly** in `mini_agent/config/mcp.json`:
   - JINA_API_KEY
   - SERPER_API_KEY
   - MINIMAX_API_KEY

4. **Check uvx version:**
```powershell
uvx --version
```

### Solutions

#### Solution 1: Verify Repository Availability
The GitHub repository might not be public or might not exist. Check if the URL is correct:
- Visit: https://github.com/MiniMax-AI/minimax_search

#### Solution 2: Disable the Problematic Server Temporarily
Edit `C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\mcp.json`:
```json
{
  "mcpServers": {
    "minimax_search": {
      "description": "MiniMax Search - Powerful web search and intelligent browsing ⭐",
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/MiniMax-AI/minimax_search",
        "minimax-search"
      ],
      "env": {
        "JINA_API_KEY": "...",
        "SERPER_API_KEY": "...",
        "MINIMAX_API_KEY": "..."
      },
      "disabled": true   // ← Add this line
    }
  }
}
```

#### Solution 3: Use Alternative Search MCP Server
If minimax_search is not available, consider using:
- Brave Search MCP
- Google Search MCP
- DuckDuckGo Search MCP

Example configuration for Brave Search (if you have API key):
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key-here"
      }
    }
  }
}
```

#### Solution 4: Install Package Locally First
If the package exists but uvx has issues:
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
uv pip install git+https://github.com/MiniMax-AI/minimax_search
```

Then modify mcp.json to use the installed package:
```json
"command": "uv",
"args": ["run", "minimax-search"]
```

---

## Issue 3: UTF-8 Encoding Issues

### Problem
PowerShell characters appear corrupted, requiring UTF-8 configuration.

### Current Workaround
The auto-script that runs:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
Write-Host "PowerShell configured for UTF-8 (Mini Agent ready!)" -ForegroundColor Green
```

### Permanent Solution

#### Option 1: Add to PowerShell Profile
Edit your PowerShell profile:
```powershell
notepad $PROFILE
```

Add these lines:
```powershell
# UTF-8 encoding for Mini-Agent and Unicode support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$env:PYTHONIOENCODING = "utf-8"
```

#### Option 2: Windows Terminal Settings
If using Windows Terminal, add to settings.json:
```json
{
  "profiles": {
    "defaults": {
      "font": {
        "face": "Cascadia Code",
        "features": {
          "calt": 1
        }
      },
      "colorScheme": "One Half Dark"
    },
    "list": [
      {
        "commandline": "powershell.exe -NoExit -Command \"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\"",
        "name": "PowerShell (UTF-8)",
        "icon": "ms-appx:///ProfileIcons/{61c54bbd-c2c6-5271-96e7-009a87ff44bf}.png"
      }
    ]
  }
}
```

#### Option 3: Set System-Wide UTF-8
Windows 10/11:
1. Open Settings → Time & Language → Language & Region
2. Click "Administrative language settings"
3. Click "Change system locale"
4. Check "Beta: Use Unicode UTF-8 for worldwide language support"
5. Restart computer

**Warning:** This may affect legacy applications.

---

## Verification

After applying fixes:

### Test File Access:
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
uv run mini-agent

# Then ask the agent:
"Can you list the files in C:\Users\Jazeel-Home\Mini-Agent?"
```

### Test MCP Servers:
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
uv run mini-agent

# Check the startup messages for:
"✓ Connected to MCP server 'minimax_search'"
```

### Test UTF-8 Encoding:
```powershell
# Should display correctly:
Write-Host "✓ ✅ ❌ 🔧 📝 🚀" -ForegroundColor Green
```

---

## Additional Resources

- [ACP Documentation](https://github.com/anthropics/acp)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Mini-Agent GitHub](https://github.com/MiniMax-AI/Mini-Agent)
- [MiniMax-M2 Desktop Config Guide](https://docs.anthropic.com/minimax/docs/minimax-desktop)

---

## Getting Help

If issues persist:

1. **Check logs:**
   ```powershell
   Get-Content C:\Users\Jazeel-Home\Mini-Agent\.observability\*.log -Tail 50
   ```

2. **Enable debug mode:**
   Edit `mini_agent/config/config.yaml`:
   ```yaml
   debug: true
   log_level: DEBUG
   ```

3. **Report issue with details:**
   - OS version: `[System.Environment]::OSVersion`
   - Python version: `python --version`
   - uv version: `uv --version`
   - Node version: `node --version`
   - Full error traceback
   - Configuration files (redact API keys!)
