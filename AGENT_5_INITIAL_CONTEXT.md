# 🤖 Agent 5: MiniMax-Coding-MCP Integration - INITIAL CONTEXT

## 📋 YOUR MISSION CONTEXT
You are **Agent 5** in a **Mini-Agent Parallel Repair Coordination Plan**. This is part of a 5-agent parallel execution to fix critical system issues and improve Mini-Agent from 65/100 health to 90+ health.

## 🎯 YOUR SPECIFIC TASK
**Replace simulation functions with real MiniMax API integration** - The MiniMax Coding MCP server currently uses simulation functions instead of connecting to the real MiniMax API.

## 📂 CRITICAL CONTEXT FILES TO READ FIRST

### **1. Understanding the Parallel Repair Project**
- **Read**: `PARALLEL_AGENT_COORDINATION_GUIDE.md` (Master overview of all 5 agents)
- **Read**: `documents/15_EX_REVIEW/MINI_AGENT_PARALLEL_REPAIR_PACKAGE/MINI_AGENT_PARALLEL_REPAIR_PACKAGE/01_COORDINATION/PARALLEL_AGENT_COORDINATION_PLAN.md` (Original coordination plan)

### **2. Your Specific Instructions**
- **Read**: `AGENT_5_PROMPT.md` (Complete implementation instructions)

### **3. Current MiniMax MCP Server**
- **Study**: `scripts/mcp_servers/minimax_coding_plan_mcp_server.py` (Current implementation)
- **Identify**: Which functions are simulations vs real API calls

### **4. MiniMax API Resources**
- **Check**: `.env` contains `MINIMAX_API_KEY`
- **API Base**: `https://api.minimax.chat`
- **Model**: GLM-4.6 (Lite plan compatible)

## 🔧 WHAT TO USE YOUR TOOLS FOR

### **1. File Operations**
- Analyze current simulation functions
- Replace with real API integration
- Test API authentication and responses

### **2. Code Analysis**
- Understand simulation vs real API requirements
- Map outputs to expected formats
- Implement proper error handling

### **3. API Integration**
- Handle MiniMax API authentication
- Implement rate limiting and error recovery
- Test response quality vs simulations

## ⚠️ CRITICAL AWARENESS

### **Parallel Execution Context**
- **You are NOT alone** - 4 other agents are working simultaneously:
  - **Agent 1**: Fixing Supabase MCP protocol (different area, minimal impact)
  - **Agent 2**: Converting ZAI scripts to MCP tools (different area, minimal impact)  
  - **Agent 3**: Fixing configuration paths (needs working MINIMAX_API_KEY)
  - **Agent 4**: Creating system transparency (will test your tools)

### **Dependencies & Coordination**
- **Agent 3's work affects you** - MINIMAX_API_KEY must be accessible
- **Agent 4's work helps you** - System transparency will validate your API integration
- **Least dependent on others** - Most isolated agent task

## 🛠️ SIMULATION FUNCTIONS TO REPLACE

### **Current Tools in MCP Server**:
1. **`generate_code`** - Currently simulated code generation
2. **`analyze_code`** - Currently simulated code analysis
3. **`create_development_plan`** - Currently simulated planning  
4. **`review_code`** - Currently simulated code review

### **Real API Integration Required**:
- Connect to `https://api.minimax.chat`
- Use GLM-4.6 model
- Implement proper authentication with MINIMAX_API_KEY
- Handle API rate limits and errors
- Map responses to existing tool formats

## 🎯 SUCCESS CRITERIA
- ✅ All simulation functions replaced with real API calls
- ✅ MiniMax API authentication working correctly
- ✅ All 4 tools (generate, analyze, plan, review) use real API
- ✅ Proper error handling and fallback mechanisms
- ✅ Response quality improvements over simulations
- ✅ No breaking changes to MCP server functionality

## ⏰ ESTIMATED TIME: 3-4 hours

## 🚀 START HERE
1. **Read the context files** listed above
2. **Analyze current MiniMax MCP server** using your tools
3. **Identify all simulation functions** that need replacement
4. **Plan real API integration** (tell me your approach before implementing)
5. **Implement with proper error handling** and testing

Remember: **You have the clearest, most isolated task - focus on replacing simulations with real API calls!**