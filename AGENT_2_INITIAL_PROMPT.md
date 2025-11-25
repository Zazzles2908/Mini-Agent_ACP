# 🚀 Agent 2: ZAI-MCP-Manager Architecture Redesign

## 📋 CRITICAL CONTEXT - READ THIS FIRST

**You are Agent 2** in a Mini-Agent Parallel Repair project. Your task: Convert 8 ZAI skill scripts to discoverable MCP tools.

### **📁 FILES TO READ IN THIS ORDER:**

1. **`PARALLEL_AGENT_COORDINATION_GUIDE.md`** - Master overview of all 5 agents
2. **`AGENT_2_PROMPT.md`** - Your complete implementation instructions  
3. **`AGENT_2_INITIAL_CONTEXT.md`** - Your specific context and dependencies
4. **`mini_agent/skills/zai-mcp-manager/scripts/`** - The 8 scripts you need to convert:
   - `quota_monitor.py` → `get_zai_quota`, `track_usage`
   - `health_checker.py` → `check_zai_health`, `validate_config`
   - `config_validator.py` → `validate_zai_config`, `fix_config_paths`
   - `config_template_generator.py` → `generate_zai_templates`
   - Plus 4 more scripts

### **🔧 PATTERN TO FOLLOW:**
**Study**: `scripts/mcp_servers/minimax_coding_plan_mcp_server.py` (FastMCP pattern)
**Update**: `mini_agent/config/.mcp.json` (Add new ZAI-MCP-Manager server)

### **⚠️ CRITICAL AWARENESS:**
- **Agent 1** (Supabase MCP) is working - coordinate .mcp.json updates with them
- **Agent 3** (Configuration paths) affects your file locations
- **Agent 4** (System transparency) will test your tool discovery
- **Agent 5** (MiniMax integration) works independently

### **🎯 YOUR TASK:**
Convert ZAI scripts to MCP tools following FastMCP pattern, ensure tools are discoverable, update configuration, test integration.

**ESTIMATED TIME: 3-4 hours**

### **📋 HOW TO PROCEED:**
1. **Read files** (order listed above)
2. **Analyze current scripts** using your tools
3. **Plan implementation** (tell me your approach before executing)
4. **Execute systematically** and test thoroughly
5. **Coordinate with other agents** as needed

**Remember: You're converting scripts to tools - follow the MCP server pattern exactly!**