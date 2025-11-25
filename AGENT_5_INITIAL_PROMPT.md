# 🤖 Agent 5: MiniMax-Coding-MCP Integration

## 📋 CRITICAL CONTEXT - READ THIS FIRST

**You are Agent 5** in a Mini-Agent Parallel Repair project. Your task: Replace simulation functions with real MiniMax API integration.

### **📁 FILES TO READ IN THIS ORDER:**

1. **`PARALLEL_AGENT_COORDINATION_GUIDE.md`** - Master overview of all 5 agents
2. **`AGENT_5_PROMPT.md`** - Your complete implementation instructions
3. **`AGENT_5_INITIAL_CONTEXT.md`** - Your specific context and dependencies

### **🔍 SIMULATION FUNCTIONS TO REPLACE:**
**Current MiniMax MCP Server:** `scripts/mcp_servers/minimax_coding_plan_mcp_server.py`

**Tools to Fix:**
1. **`generate_code`** - Currently simulated → Real MiniMax API code generation
2. **`analyze_code`** - Currently simulated → Real MiniMax API code analysis
3. **`create_development_plan`** - Currently simulated → Real MiniMax API planning
4. **`review_code`** - Currently simulated → Real MiniMax API code review

### **🔧 API INTEGRATION DETAILS:**
- **API Base:** `https://api.minimax.chat`
- **API Key:** Already configured in `.env` as `MINIMAX_API_KEY`
- **Model:** GLM-4.6 (Lite plan compatible)
- **Authentication:** Bearer token format

### **⚠️ CRITICAL AWARENESS:**
- **Most isolated agent** - Least dependent on other agents' work
- **Agent 3** (Configuration paths) - MINIMAX_API_KEY must be accessible
- **Agent 4** (System transparency) - Will test your API integration
- **All other agents** work independently from your task

### **🎯 YOUR TASK:**
Analyze current simulation functions, replace with real MiniMax API calls, implement proper authentication and error handling, test response quality vs simulations, ensure no breaking changes to MCP server functionality.

**ESTIMATED TIME: 3-4 hours**

### **📋 HOW TO PROCEED:**
1. **Read files** (order listed above)
2. **Analyze current MiniMax MCP server** using your tools and code analysis
3. **Identify all simulation functions** that need replacement
4. **Plan real API integration** (tell me your approach before implementing)
5. **Implement with proper error handling** and comprehensive testing
6. **Compare output quality** vs simulations

**Remember: You have the clearest, most isolated task - focus on replacing simulations with real API calls!**