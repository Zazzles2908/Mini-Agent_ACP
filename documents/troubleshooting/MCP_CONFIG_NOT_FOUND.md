# MCP Configuration Issue - DIAGNOSIS

**Problem**: MCP config file not found when running mini-agent

## Root Cause

You have TWO MCP config files:
1. `.mcp.json` (root directory) - ✅ Working config
2. `mini_agent/config/mcp.json` - ❌ Different location, not found

The code searches for the file specified in `config.yaml`:
```yaml
mcp_config_path: ".mcp.json"  # <-- Looking for THIS
```

**Search Priority** (from `Config.find_config_file()`):
1. `mini_agent/config/.mcp.json` ❌ Doesn't exist
2. `~/.mini-agent/config/.mcp.json` ❌ Doesn't exist  
3. `{package}/mini_agent/config/.mcp.json` ❌ Doesn't exist
4. Falls back to root `.mcp.json` ❌ Not in search path!

## Solution Options

### Option 1: Use Root .mcp.json (Recommended)
Keep `.mcp.json` in root and update config to use relative path:

```bash
# Edit mini_agent/config/config.yaml
# Change:
mcp_config_path: ".mcp.json"
# To:
mcp_config_path: "mcp.json"  # Without the dot
```

OR update to explicitly use root:
```yaml
mcp_config_path: "./.mcp.json"  # Root directory
```

### Option 2: Move to Standard Location
Move `.mcp.json` to the config directory:

```bash
# Move root .mcp.json to config directory
cp .mcp.json mini_agent/config/.mcp.json
# OR rename to match
mv mini_agent/config/mcp.json mini_agent/config/.mcp.json
```

### Option 3: Update Config to Use mcp.json (No Dot)
If you want to use `mini_agent/config/mcp.json`:

```bash
# Edit mini_agent/config/config.yaml
# Change:
mcp_config_path: ".mcp.json"
# To:
mcp_config_path: "mcp.json"  # Will find mini_agent/config/mcp.json
```

## Comparison of Two Files

**Root `.mcp.json`**:
- Has memory server (enabled)
- Has git server (enabled)
- Notes about removed servers

**mini_agent/config/mcp.json`**:
- Same content (checked)

## Recommended Fix

**Use Option 1** - Keep root `.mcp.json` and update config:

1. Edit `mini_agent/config/config.yaml`:
```yaml
tools:
  # MCP Tools
  enable_mcp: true
  mcp_config_path: "mcp.json"  # Changed from ".mcp.json"
```

2. Delete duplicate:
```bash
rm mini_agent/config/mcp.json  # If it's a duplicate
```

3. OR consolidate by moving root to config:
```bash
mv .mcp.json mini_agent/config/.mcp.json
git add mini_agent/config/.mcp.json
git rm .mcp.json
```

## Why This Happened

During cleanup, we removed root `mcp.json` (no dot) but kept `.mcp.json` (with dot). The config file expects the dotted version in the config directory, but the actual file is in root with a dot.

## Quick Fix (Immediate)

```bash
# Copy root .mcp.json to config directory with dot
cp .mcp.json mini_agent/config/.mcp.json

# Test
mini-agent
# Should now show: "✅ Loaded X MCP tools"
```

## Proper Fix (After Testing)

```bash
# Once working, remove the duplicate
git rm .mcp.json  # Root version
git add mini_agent/config/.mcp.json  # Config version
git commit -m "fix: Move .mcp.json to config directory"
```

## Verification

After fix, you should see:
```
Loading MCP tools...
✅ Loaded 2 MCP tools (from: mini_agent/config/.mcp.json)
  - memory (Knowledge graph memory system)
  - git (Git repository operations)
```

Instead of:
```
Loading MCP tools...
⚠️  MCP config file not found: .mcp.json
```
