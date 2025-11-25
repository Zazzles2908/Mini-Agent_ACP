# 🔧 Mini-Agent Parallel Repair Coordination Plan
*Created: 2025-11-25 for local system parallel execution*

## 🎯 Executive Summary
**Goal:** Transform Mini-Agent from 65/100 health to 90+ health through parallel architectural repairs
**Strategy:** Deploy 5 specialized agents simultaneously to fix critical issues
**Expected Timeline:** 3-5 days for Phase 1 completion

---

## 🚀 Phase 1: Critical Fixes (Execute in Parallel)

### **Agent A: Supabase MCP Server Protocol Fix**
**Role:** Fix the JSONRPC parsing error causing startup failures

**Location:** `/workspace/docs/supabase_mcp_fix.md` + `supabase_admin_mcp_server_fixed.py`

**Instructions:**
1. **Backup Current Server:**
   ```bash
   cd Mini-Agent_ACP/scripts/mcp_servers
   cp supabase_admin_mcp_server.py supabase_admin_mcp_server.py.backup
   ```

2. **Deploy Fixed Server:**
   - Replace current server with fixed version from analysis
   - Ensure no stdout output during startup (only stderr for errors)
   - Install required dependencies: `fastmcp`, `supabase`

3. **Validation Steps:**
   - Test MCP connection: `python validate_supabase_config.py`
   - Verify no JSONRPC parsing errors in startup logs
   - Confirm Supabase tools become available

**Success Criteria:** No more "Failed to parse JSONRPC message" errors

---

### **Agent B: ZAI-MCP-Manager Architecture Redesign**
**Role:** Convert skill scripts to discoverable MCP tools

**Current Issue:** Scripts under `skills/zai-mcp-manager/scripts/` not available as tools

**Instructions:**
1. **Analyze Current Structure:**
   - Review `docs/zai_mcp_manager_redesign.md`
   - Examine current scripts: `quota_monitor.py`, `health_checker.py`, `config_validator.py`, `config_template_generator.py`

2. **Create MCP Server Structure:**
   ```python
   # Create: zai_mcp_manager_mcp_server.py
   # Follow pattern from minimax_coding_plan_mcp_server.py
   # Convert each script to @mcp.tool decorated function
   ```

3. **Key Conversions Needed:**
   - `quota_monitor.py` → `get_zai_quota`, `track_usage`
   - `health_checker.py` → `check_zai_health`, `validate_config`
   - `config_validator.py` → `validate_zai_config`, `fix_config_paths`
   - `config_template_generator.py` → `generate_zai_templates`

4. **Integration:**
   - Add to `.mcp.json` configuration
   - Test tool discovery in startup
   - Verify tools appear in available actions

**Success Criteria:** ZAI quota/health tools become discoverable MCP tools

---

### **Agent C: Configuration Path Resolution**
**Role:** Fix path chaos preventing tool functionality

**Current Issue:** Configuration files moved to wrong directories, breaking tool access

**Instructions:**
1. **Audit Configuration Paths:**
   - Check `mini_agent/config/config.yaml`
   - Verify all MCP server paths in `.mcp.json`
   - Identify moved/misplaced config files

2. **Fix Path Resolution:**
   - Ensure all config files in `mini_agent/config/`
   - Update absolute/relative path references
   - Fix environment variable references

3. **Test Path Dependencies:**
   - Verify MCP server can locate configs
   - Test tool configuration loading
   - Confirm no "file not found" errors

**Success Criteria:** All configuration files accessible, no path errors

---

### **Agent D: System Transparency Implementation**
**Role:** Create confidence scoring for loaded tools

**Current Issue:** 37 tools loaded but unknown functionality status

**Instructions:**
1. **Implement Health Monitoring:**
   - Create `system_health_monitor.py`
   - Test each tool category (File, Shell, Skills, MCP, etc.)
   - Generate confidence scores (0.0-1.0)

2. **Create Diagnostic Tools:**
   ```python
   # Tools to create:
   - `test_tool_functionality()` - Individual tool tests
   - `check_mcp_connections()` - Test all MCP servers
   - `validate_skill_integration()` - Verify skill accessibility
   - `generate_health_report()` - Overall system status
   ```

3. **Integration with Agent:**
   - Add health status to startup output
   - Create `system_status` command/tool
   - Implement real-time monitoring

**Success Criteria:** Agent displays tool confidence scores, transparent functionality status

---

### **Agent E: MiniMax-Coding-MCP Integration**
**Role:** Ensure coding tools work with real MiniMax API

**Current Issue:** MCP server has simulation functions, not real API integration

**Instructions:**
1. **Replace Simulations:**
   - Update `minimax_coding_plan_mcp_server.py`
   - Replace `simulate_*` functions with real MiniMax API calls
   - Use GLM-4.6 model endpoints

2. **API Integration:**
   - Connect to: `https://api.minimax.ai`
   - Implement proper authentication
   - Handle API rate limits and errors

3. **Testing:**
   - Test code generation with real API
   - Verify all 4 tools: generate, analyze, create_plan, review
   - Compare output quality vs simulations

**Success Criteria:** MiniMax coding tools use real API, not simulations

---

## 📋 Coordination Protocol

### **Pre-Execution Checklist**
- [ ] All agents have read access to workspace documentation
- [ ] Backup of current system created
- [ ] Development environment prepared
- [ ] Network access verified for API calls

### **Execution Sequence**
1. **Start All Agents Simultaneously**
2. **Monitor Progress Every 2 Hours**
3. **Handle Conflicts/Cross-Dependencies**
4. **Validate Individual Completions**
5. **Run Integration Tests**

### **Success Validation**
Each agent reports:
- ✅ Completion status
- ✅ Testing results
- ✅ Issues encountered
- ✅ Ready for integration

### **Integration Testing**
After parallel execution:
```bash
# System Health Test
mini-agent
# Should show: No errors, working tools, confidence scores
```

---

## 🎯 Expected Outcomes

### **Before Parallel Execution:**
- System Health: 65/100
- Supabase MCP: ❌ Failing
- ZAI Tools: ❌ Not discoverable  
- Configuration: ❌ Path chaos
- Transparency: ❌ Unknown functionality

### **After Parallel Execution:**
- System Health: 90/100+
- Supabase MCP: ✅ Working
- ZAI Tools: ✅ Discoverable MCP tools
- Configuration: ✅ Clean paths
- Transparency: ✅ Confidence scoring

### **Immediate User Benefits:**
- No startup errors
- All tools discoverable and usable
- Clear system health status
- Confidence in functionality
- Foundation for Phase 2 enhancements

---

## 📞 Escalation Protocol

**If any agent encounters blocking issues:**
1. Document issue in agent log
2. Request specific help from coordinator
3. Continue with other tasks while waiting
4. Re-assess upon resolution

**Cross-Dependency Issues:**
- Configuration fixes may affect MCP integration
- Coordinate changes through coordinator
- Test integration after individual completions

---

*This plan transforms Mini-Agent from a "clunky black box" to a transparent, functional AI agent through parallel architectural repairs.*