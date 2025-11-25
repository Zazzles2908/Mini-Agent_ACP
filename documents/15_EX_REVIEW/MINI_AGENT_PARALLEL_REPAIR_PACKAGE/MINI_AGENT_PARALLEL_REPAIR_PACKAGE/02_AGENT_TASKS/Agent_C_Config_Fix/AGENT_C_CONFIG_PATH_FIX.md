# Agent C: Configuration Path Resolution
*Priority: HIGH - Fix path chaos preventing tool functionality*

## 🎯 Mission
Resolve configuration path issues preventing MCP tools and skills from accessing required files.

## 📋 Current Problem
- **Issue:** Configuration files moved to wrong directories
- **Impact:** Tools loaded but can't access configs, causing failures
- **Symptoms:** "File not found", path resolution errors
- **Root Cause:** zai-mcp-manager scripts moving config files incorrectly

## 🛠️ Implementation Steps

### Step 1: Configuration Audit
**Check These Files:**
- `mini_agent/config/config.yaml` - Main configuration
- `mini_agent/config/.mcp.json` - MCP server configurations  
- `mini_agent/skills/zai-mcp-manager/` - Skill configurations
- Any moved config files in wrong locations

### Step 2: Path Resolution
**Identify & Fix:**
1. **Absolute vs Relative Paths:** Ensure all paths use consistent format
2. **Environment Variables:** Verify `${MINIMAX_API_KEY}` style references work
3. **MCP Server Paths:** Check all server command/args paths
4. **Skill Configuration:** Ensure skills can locate their configs

### Step 3: Standardize Paths
**Target Directory Structure:**
```
mini_agent/
├── config/
│   ├── config.yaml
│   ├── .mcp.json
│   └── [other config files]
├── skills/
│   └── zai-mcp-manager/
│       ├── SKILL.md (documentation only)
│       └── [skill metadata]
```

### Step 4: Fix Broken References
**Common Fixes Needed:**
```yaml
# Instead of: /absolute/path/to/config
# Use: mini_agent/config/config.yaml

# Instead of: ../config/file  
# Use: ./config/file

# Environment variables should work:
MINIMAX_API_KEY: ${MINIMAX_API_KEY}
ZAI_API_KEY: ${ZAI_API_KEY}
```

### Step 5: Validation Testing
```bash
# Test MCP server path resolution
python -c "import json; print(json.load(open('mini_agent/config/.mcp.json')))"

# Test configuration loading
mini-agent --test-config

# Verify no path errors in startup
mini-agent 2>&1 | grep -i "not found\|path\|error"
```

## 🎯 Success Criteria
**Complete when:**
- All config files in `mini_agent/config/`
- No "file not found" errors during startup
- MCP servers can locate their configurations
- Tools load successfully without path issues

## 📁 Resources
- **Current Config:** `mini_agent/config/config.yaml`
- **MCP Config:** `mini_agent/config/.mcp.json`
- **Backup Location:** Before making changes

## ⏱️ Estimated Time
**Target:** 2-3 hours
**Max:** 4 hours

## ⚠️ Important Notes
- **Backup First:** Always backup config files before changes
- **Test Incrementally:** Make small changes and test after each
- **Document Changes:** Note what paths were changed and why
- **Environment Variables:** Ensure they work in deployment context
