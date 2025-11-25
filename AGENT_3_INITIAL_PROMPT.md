# 🔧 Agent 3: Configuration Path Resolution

## 📋 CRITICAL CONTEXT - READ THIS FIRST

**You are Agent 3** in a Mini-Agent Parallel Repair project. Your task: Fix configuration path chaos preventing tool functionality.

### **📁 FILES TO READ IN THIS ORDER:**

1. **`PARALLEL_AGENT_COORDINATION_GUIDE.md`** - Master overview of all 5 agents
2. **`AGENT_3_PROMPT.md`** - Your complete implementation instructions
3. **`AGENT_3_INITIAL_CONTEXT.md`** - Your specific context and dependencies

### **🔍 PROBLEM AREAS TO INVESTIGATE:**
**Check Current Configuration State:**
- `mini_agent/config/config.yaml` (Main configuration file)
- `mini_agent/config/.mcp.json` (MCP server configurations)  
- `.env` (Environment variables and API keys)
- `scripts/mcp_servers/` (All MCP server scripts)

### **🛠️ TOOL CATEGORIES TO AUDIT:**
1. **Configuration File Locations** - Verify files are in correct directories
2. **MCP Server Path References** - All paths in .mcp.json must be consistent
3. **Environment Variable Path Resolution** - API key access patterns

### **⚠️ CRITICAL AWARENESS:**
- **Agent 1** (Supabase MCP) depends on your path fixes for their server
- **Agent 2** (ZAI scripts) needs correct .mcp.json paths
- **Agent 4** (System transparency) will test path resolution
- **Agent 5** (MiniMax integration) needs working MINIMAX_API_KEY access

### **🎯 YOUR TASK:**
Audit configuration structure, identify missing/misplaced files, fix path references in config files, ensure consistent path patterns across all configuration.

**ESTIMATED TIME: 2-3 hours**

### **📋 HOW TO PROCEED:**
1. **Read files** (order listed above)
2. **Audit current configuration** using bash find commands and file operations
3. **Identify path resolution issues** (missing files, broken references)
4. **Plan systematic fixes** (tell me your approach before executing)
5. **Execute and test each fix** thoroughly
6. **Coordinate with other agents** as their work may affect your fixes

**Remember: Your fixes enable all other agents to work properly - be thorough and test everything!**