# Mini-Agent Investigation Report

**Date:** November 19, 2025  
**Investigated by:** Mini-Agent Assistant  
**Issues:** File Access Restrictions & MCP Connection Failures

---

## 🔍 Issues Identified

### 1. File Access Restricted to `C:\tmp`

**Symptom:**
```
Allowed directories:
C:\tmp
```

**Root Cause:**
When Mini-Agent runs through Claude Desktop's ACP (Agent Client Protocol) integration, file access is restricted by the ACP server configuration. The current configuration only allows access to `C:\tmp`.

**Impact:**
- Cannot access files in `C:\Users\Jazeel-Home`
- Cannot access project files in `C:\Project`
- Cannot access the Mini-Agent installation directory
- Severely limits the agent's ability to help with file operations

---

### 2. MCP Server `minimax_search` Connection Failure

**Symptom:**
```
✗ Failed to connect to MCP server 'minimax_search': Connection closed
mcp.shared.exceptions.McpError: Connection closed
```

**Investigation Results:**
- ✅ Repository exists: https://github.com/MiniMax-AI/minimax_search (HTTP 200)
- ✅ Configuration file found: `mini_agent/config/mcp.json`
- ✅ API keys are configured (JINA, SERPER, MINIMAX)
- ⚠️ Git ls-remote command timed out (network/firewall issue?)
- ❌ MCP server fails to initialize

**Possible Causes:**
1. Network connectivity issues to GitHub
2. `uvx` installation from git+https:// URL failing
3. The package may not have proper entry points configured
4. API keys may be invalid or expired
5. MCP protocol version mismatch

---

### 3. UTF-8 Encoding Issues (Minor)

**Symptom:**
Characters appear corrupted in PowerShell unless UTF-8 is explicitly configured.

**Current Workaround:**
Auto-script runs at startup to configure UTF-8 encoding.

**Status:** Manageable with workaround, permanent solution available.

---

## 🔧 Solutions Provided

### Solution 1: Fix File Access Restrictions

**Quick Fix Script:** `scripts/fix-file-access.ps1`

**What it does:**
1. Backs up Claude Desktop config
2. Adds `agentServers` section
3. Configures Mini-Agent with allowed directories:
   - `C:\Users\Jazeel-Home`
   - `C:\Project`
   - `C:\tmp`
   - Mini-Agent installation directory
4. Sets UTF-8 encoding environment variables

**How to use:**
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
.\scripts\fix-file-access.ps1
# Restart Claude Desktop
```

**Manual alternative:**
Edit `C:\Users\Jazeel-Home\AppData\Roaming\Claude\claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    // ... existing servers ...
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

---

### Solution 2: Fix MCP Server Connection Issues

**Quick Fix Script:** `scripts/fix-mcp-servers.ps1`

**What it does:**
1. Backs up MCP config
2. Disables problematic `minimax_search` server
3. Shows status of all MCP servers

**How to use:**
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
.\scripts\fix-mcp-servers.ps1
```

**Alternative approaches:**

#### A) Test manual installation:
```powershell
uvx --from git+https://github.com/MiniMax-AI/minimax_search minimax-search --help
```

#### B) Try local installation:
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
uv pip install git+https://github.com/MiniMax-AI/minimax_search

# Then update mcp.json:
# "command": "uv",
# "args": ["run", "minimax-search"]
```

#### C) Check network/proxy:
```powershell
# Test GitHub connectivity
git config --global http.proxy
git config --global https.proxy

# If behind proxy, configure:
# git config --global http.proxy http://proxy.server:port
# git config --global https.proxy https://proxy.server:port
```

#### D) Use alternative search MCP:
Consider using:
- Brave Search MCP (already in Claude Desktop config)
- Google Custom Search
- DuckDuckGo Search

---

### Solution 3: UTF-8 Encoding Permanent Fix

**Add to PowerShell Profile:**
```powershell
notepad $PROFILE
```

Add these lines:
```powershell
# UTF-8 encoding for Mini-Agent
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$env:PYTHONIOENCODING = "utf-8"
```

**Windows System-Wide UTF-8:**
Settings → Time & Language → Administrative language settings → Change system locale → Check "Beta: Use Unicode UTF-8"

---

## 📋 Current MCP Server Status

Based on `mini_agent/config/mcp.json`:

| Server | Status | Description | Notes |
|--------|--------|-------------|-------|
| minimax_search | ❌ FAILING | Web search & browsing | Connection closed error |
| memory | ✅ ENABLED | Knowledge graph memory | Uses npx, should work |
| filesystem | ✅ ENABLED | File system access | Configured for /tmp |
| git | ✅ ENABLED | Git operations | Python-based |

Based on Claude Desktop config:

| Server | Status | Description |
|--------|--------|-------------|
| gh-mcp | ✅ ENABLED | GitHub CLI integration |
| excalidraw-mermaid | ✅ ENABLED | Diagram generation |
| exai-mcp | ✅ ENABLED | EX-AI capabilities |
| filesystem | ✅ ENABLED | File access to C:/Project, C:/Users/Jazeel-Home, C:/Project/ADP |

---

## ✅ Verification Steps

After applying fixes:

### 1. Verify File Access
```powershell
# Restart Claude Desktop, then ask:
"Can you list files in C:\Users\Jazeel-Home\Mini-Agent?"
```

Expected: Should successfully list directory contents

### 2. Verify MCP Servers
```powershell
# Run mini-agent directly:
cd C:\Users\Jazeel-Home\Mini-Agent
uv run mini-agent
```

Expected startup messages:
```
✓ Connected to MCP server 'memory' - loaded X tools
✓ Connected to MCP server 'filesystem' - loaded X tools
✓ Connected to MCP server 'git' - loaded X tools
```

### 3. Verify UTF-8 Encoding
```powershell
Write-Host "✓ ✅ ❌ 🔧 📝 🚀" -ForegroundColor Green
```

Expected: Symbols display correctly

---

## 🚀 Recommended Actions

### Immediate Actions (High Priority)

1. **Run the file access fix script:**
   ```powershell
   cd C:\Users\Jazeel-Home\Mini-Agent
   .\scripts\fix-file-access.ps1
   ```

2. **Restart Claude Desktop** to apply ACP server configuration

3. **Disable problematic MCP server:**
   ```powershell
   .\scripts\fix-mcp-servers.ps1
   ```

### Optional Actions

4. **Investigate minimax_search installation:**
   - Test manual installation
   - Check network/proxy settings
   - Consider alternative search MCP servers

5. **Set up permanent UTF-8 encoding:**
   - Add to PowerShell profile
   - Or use Windows system-wide UTF-8

### Testing & Validation

6. **Test file operations in various directories:**
   - C:\Users\Jazeel-Home
   - C:\Project
   - Mini-Agent directory

7. **Test remaining MCP servers:**
   - memory (knowledge graph)
   - filesystem
   - git operations

---

## 📚 Documentation Created

The following files have been created to help resolve these issues:

1. **`documents/TROUBLESHOOTING.md`** - Comprehensive troubleshooting guide
2. **`scripts/fix-file-access.ps1`** - Automated fix for file access restrictions
3. **`scripts/fix-mcp-servers.ps1`** - Automated fix for MCP server issues
4. **`documents/INVESTIGATION_REPORT.md`** - This document

---

## 🔗 Additional Resources

- [Mini-Agent GitHub Repository](https://github.com/MiniMax-AI/Mini-Agent)
- [ACP Documentation](https://github.com/anthropics/acp)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs/claude-desktop)

---

## 🆘 Getting Further Help

If issues persist after applying these fixes:

1. **Check logs:**
   ```powershell
   Get-ChildItem C:\Users\Jazeel-Home\Mini-Agent\.observability -Recurse
   Get-Content C:\Users\Jazeel-Home\Mini-Agent\.observability\*.log -Tail 100
   ```

2. **Enable debug mode:**
   Edit `mini_agent/config/config.yaml`:
   ```yaml
   debug: true
   log_level: DEBUG
   ```

3. **Collect diagnostic information:**
   ```powershell
   # System info
   [System.Environment]::OSVersion
   python --version
   uv --version
   node --version
   
   # Check Mini-Agent installation
   cd C:\Users\Jazeel-Home\Mini-Agent
   uv run mini-agent --version
   ```

4. **Report issue with:**
   - Full error traceback
   - Configuration files (redact API keys!)
   - System information
   - Steps to reproduce

---

**Next Steps:** Run the fix scripts and restart Claude Desktop to resolve the file access issue. The MCP server issue can be temporarily bypassed by disabling the problematic server.
