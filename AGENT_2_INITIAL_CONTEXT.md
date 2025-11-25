# 🚀 Agent 2: ZAI-MCP-Manager Architecture Redesign - INITIAL CONTEXT

## 📋 YOUR MISSION CONTEXT
You are **Agent 2** in a **Mini-Agent Parallel Repair Coordination Plan**. This is part of a 5-agent parallel execution to fix critical system issues and improve Mini-Agent from 65/100 health to 90+ health.

## 🎯 YOUR SPECIFIC TASK
**Convert ZAI skill scripts to discoverable MCP tools** - Currently 8 scripts in `mini_agent/skills/zai-mcp-manager/scripts/` exist but aren't discoverable as MCP tools during Mini-Agent startup.

## 📂 CRITICAL CONTEXT FILES TO READ FIRST

### **1. Understanding the Parallel Repair Project**
- **Read**: `PARALLEL_AGENT_COORDINATION_GUIDE.md` (Master overview of all 5 agents)
- **Read**: `documents/15_EX_REVIEW/MINI_AGENT_PARALLEL_REPAIR_PACKAGE/MINI_AGENT_PARALLEL_REPAIR_PACKAGE/01_COORDINATION/PARALLEL_AGENT_COORDINATION_PLAN.md` (Original coordination plan)

### **2. Your Specific Instructions**
- **Read**: `AGENT_2_PROMPT.md` (Complete implementation instructions)

### **3. MCP Server Pattern Reference**
- **Study**: `scripts/mcp_servers/minimax_coding_plan_mcp_server.py` (Follow this pattern exactly)
- **Study**: `mini_agent/config/.mcp.json` (Update with new server)

### **4. Current ZAI Scripts to Convert**
- **Examine**: `mini_agent/skills/zai-mcp-manager/scripts/`
- Scripts: `quota_monitor.py`, `health_checker.py`, `config_validator.py`, `config_template_generator.py`, `config_consolidator.py`, `enhanced_zai_web_tool.py`, `token_truncation_detector.py`

## 🔧 WHAT TO USE YOUR TOOLS FOR

### **1. File Operations**
- Read scripts to understand functionality
- Create new MCP server following FastMCP pattern
- Edit configuration files

### **2. Bash Commands**  
- Test MCP server functionality
- Install dependencies if needed
- Validate tool discovery

### **3. Your ZAI-MCP-Manager Skill**
- Use: `get_skill("zai-mcp-manager")` for detailed guidance

## ⚠️ CRITICAL AWARENESS

### **Parallel Execution Context**
- **You are NOT alone** - 4 other agents are working simultaneously:
  - **Agent 1**: Fixing Supabase MCP protocol (may affect your .mcp.json updates)
  - **Agent 3**: Fixing configuration path issues (may affect file locations)
  - **Agent 4**: Creating system transparency (may need to discover your tools)
  - **Agent 5**: MiniMax API integration (different area, minimal impact)

### **Dependencies & Coordination**
- **Agent 1's work affects you** - When Supabase MCP is fixed, your tools need to integrate with it
- **Agent 3's work affects you** - Configuration paths must be correct for your MCP server to work
- **Agent 4's work helps you** - System transparency will test your tool discovery

## 🎯 SUCCESS CRITERIA
- ✅ ZAI MCP Manager tools become discoverable MCP tools
- ✅ All 8 script functions available through MCP protocol  
- ✅ Tools appear in "Available Actions" during Mini-Agent startup
- ✅ No breaking changes to existing functionality

## ⏰ ESTIMATED TIME: 3-4 hours

## 🚀 START HERE
1. **Read the context files** listed above
2. **Use your skills and tools** to understand current ZAI scripts
3. **Plan your implementation** following the MCP server pattern
4. **Tell me how you'll implement** (before doing it)
5. **Execute your plan** and test thoroughly

Remember: **Agent 1 is working on Supabase MCP fixes that you may depend on. Coordinate accordingly!**