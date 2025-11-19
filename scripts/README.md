# Mini-Agent Scripts

This directory contains utility scripts for managing and troubleshooting Mini-Agent.

## 🔧 Available Scripts

### File Access Fix
**Script:** `fix-file-access.ps1`

**Purpose:** Configures Claude Desktop to allow Mini-Agent access to more than just `C:\tmp`

**Usage:**
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
.\scripts\fix-file-access.ps1
```

**What it does:**
- Backs up Claude Desktop config
- Adds `agentServers` configuration
- Grants access to:
  - `C:\Users\Jazeel-Home`
  - `C:\Project`
  - `C:\tmp`
  - Mini-Agent installation directory
- Sets UTF-8 encoding

**After running:** Restart Claude Desktop

---

### MCP Server Fix
**Script:** `fix-mcp-servers.ps1`

**Purpose:** Disables problematic MCP servers that fail to connect

**Usage:**
```powershell
cd C:\Users\Jazeel-Home\Mini-Agent
.\scripts\fix-mcp-servers.ps1
```

**What it does:**
- Backs up MCP configuration
- Disables `minimax_search` server (connection issues)
- Shows status of all MCP servers

**After running:** Next Mini-Agent startup will skip the disabled server

---

## 📚 Related Documentation

- [`documents/TROUBLESHOOTING.md`](../documents/TROUBLESHOOTING.md) - Detailed troubleshooting guide
- [`documents/INVESTIGATION_REPORT.md`](../documents/INVESTIGATION_REPORT.md) - Investigation findings and recommendations

---

## ⚠️ Important Notes

### Backups
Both scripts automatically create backups before making changes:
- `claude_desktop_config.json.backup-YYYYMMDD-HHMMSS`
- `mcp.json.backup-YYYYMMDD-HHMMSS`

### Requirements
- Windows PowerShell 5.1+ or PowerShell Core 7+
- Mini-Agent installed at `C:\Users\Jazeel-Home\Mini-Agent`
- Claude Desktop installed

### Safety
All scripts:
- Create backups before modifying files
- Validate file existence before proceeding
- Provide clear status messages
- Are non-destructive (can be reverted)

---

## 🐛 Troubleshooting

### "Cannot be loaded because running scripts is disabled"
Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Config file not found"
Verify paths in the script match your installation:
- Claude Desktop config: `C:\Users\Jazeel-Home\AppData\Roaming\Claude\claude_desktop_config.json`
- MCP config: `C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\mcp.json`

### Changes not taking effect
- For file access: Fully restart Claude Desktop (close all windows)
- For MCP servers: Restart Mini-Agent or run `uv run mini-agent` fresh

---

## 🔄 Reverting Changes

If you need to revert changes:

### File Access Changes
```powershell
# Find backup
Get-ChildItem "$env:APPDATA\Claude" -Filter "claude_desktop_config.json.backup-*"

# Restore (replace TIMESTAMP with actual timestamp)
Copy-Item "$env:APPDATA\Claude\claude_desktop_config.json.backup-TIMESTAMP" `
          "$env:APPDATA\Claude\claude_desktop_config.json" -Force

# Restart Claude Desktop
```

### MCP Server Changes
```powershell
# Find backup
Get-ChildItem "C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config" -Filter "mcp.json.backup-*"

# Restore (replace TIMESTAMP with actual timestamp)
Copy-Item "C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\mcp.json.backup-TIMESTAMP" `
          "C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\mcp.json" -Force

# Restart Mini-Agent
```

---

## 📝 Adding Custom Scripts

When adding new scripts to this directory:

1. **Use descriptive names:** `fix-issue-name.ps1`
2. **Add comments:** Explain what the script does
3. **Create backups:** Before modifying any config files
4. **Provide feedback:** Use `Write-Host` with colors for status
5. **Update this README:** Add documentation for your script

### Template
```powershell
# Script Description
# What this script fixes or does

$configPath = "path/to/config"

Write-Host "=== Script Name ===" -ForegroundColor Cyan

# Backup
$backupPath = "$configPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $configPath $backupPath
Write-Host "✅ Backed up to: $backupPath" -ForegroundColor Green

# ... main logic ...

Write-Host "✅ Done!" -ForegroundColor Green
```

---

## 🚀 Quick Reference

| Issue | Script to Run | Restart Required |
|-------|---------------|------------------|
| Cannot access files outside C:\tmp | `fix-file-access.ps1` | Claude Desktop |
| MCP server connection failures | `fix-mcp-servers.ps1` | Mini-Agent |
| Both issues | Run both scripts | Both |

---

For more help, see the [Troubleshooting Guide](../documents/TROUBLESHOOTING.md).
