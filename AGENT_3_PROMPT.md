# Agent 3: Configuration Path Resolution
*Priority: CRITICAL - Fix path chaos preventing tool functionality*

## 🎯 Mission
Fix configuration file path issues that prevent Mini-Agent tools from accessing required configuration files, causing functionality failures.

## 📋 Current Problem
Configuration files have been moved or referenced incorrectly, breaking tool access and causing "file not found" errors. This affects MCP server startup and tool configuration loading.

## 🔍 Problem Areas to Investigate

### **1. Configuration File Locations**
**Check Current State**:
- `mini_agent/config/config.yaml` - Main configuration file
- `mini_agent/config/.mcp.json` - MCP server configurations
- `.env` - Environment variables and API keys
- Any other config files that may have been moved

### **2. MCP Server Path References**
**Examine**: All MCP server paths in `.mcp.json`
- Verify absolute vs relative path consistency
- Check if server scripts can locate their required configs
- Identify any broken file references

### **3. Environment Variable Path Resolution**
**Verify**: Environment variable references
- API key access patterns
- Path variables used by MCP servers
- Configuration loading in tools

## 🛠️ Implementation Requirements

### **Core Task**: Fix All Path Resolution Issues

**Step 1: Audit Current Configuration Structure**
```bash
# Map all configuration files and their locations
find . -name "*.yaml" -o -name "*.yml" -o -name ".mcp.json" -o -name ".env*"
# Identify any missing or moved files
```

**Step 2: Fix Configuration File Locations**
- Ensure all config files are in `mini_agent/config/`
- Create any missing configuration directories
- Update file permissions if needed

**Step 3: Update All Path References**
- Fix absolute/relative path inconsistencies in `.mcp.json`
- Update any hardcoded paths in MCP servers
- Ensure environment variables point to correct locations

**Step 4: Test Path Dependencies**
- Test each MCP server can locate its config files
- Verify tool configuration loading works
- Confirm no "file not found" errors occur

### **Required Path Fixes**:

**MCP Server Path Consistency**:
```json
// .mcp.json should have consistent path patterns
{
  "command": "python",
  "args": ["scripts/mcp_servers/server_name.py"],
  // All relative paths should be consistent
}
```

**Environment Variable Paths**:
- All config file references should use environment variables where appropriate
- Fix any hardcoded paths that break in different environments

**MCP Server Internal Paths**:
- Fix any internal file paths in server scripts
- Ensure servers can find their own configuration needs

### **Validation Steps**:
1. **File Existence Check**: Verify all referenced config files exist
2. **MCP Server Startup**: Test all MCP servers start without path errors
3. **Tool Functionality**: Verify tools can load their configurations
4. **Integration Testing**: Test Mini-Agent startup with fixed paths

### **Success Criteria**:
- ✅ No "file not found" errors during startup
- ✅ All MCP servers can locate their configuration files
- ✅ Tools load configurations successfully
- ✅ Environment variables resolve to correct paths
- ✅ Consistent path patterns across all configuration

### **Files to Focus On**:
- `mini_agent/config/config.yaml` - Main config location
- `mini_agent/config/.mcp.json` - MCP server definitions
- `scripts/mcp_servers/` - All MCP server scripts
- `.env` - Environment variables and API keys
- Any configuration references in Python files

**Expected Outcome**: Clean, consistent configuration file access with no path resolution errors, enabling all tools to function properly.

---
*Target Time: 2-3 hours*
*Success: All configuration files accessible, no path errors*
