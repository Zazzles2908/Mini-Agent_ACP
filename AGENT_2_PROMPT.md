# Agent 2: ZAI-MCP-Manager Architecture Redesign
*Priority: HIGH - Make ZAI quota management tools discoverable as MCP tools*

## 🎯 Mission
Convert skill scripts under `mini_agent/skills/zai-mcp-manager/scripts/` from standalone Python scripts to discoverable MCP tools that Mini-Agent can use directly.

## 📋 Current Problem
The ZAI MCP management scripts (quota_monitor.py, health_checker.py, config_validator.py, config_template_generator.py) exist but are not discoverable as MCP tools during Mini-Agent startup.

## 🛠️ Implementation Requirements

### **Core Task**: Create ZAI MCP Manager MCP Server
**Location**: `scripts/mcp_servers/zai_mcp_manager_mcp_server.py`

**Key Requirements**:
1. **Follow MCP Server Pattern**: Use the same structure as `minimax_coding_plan_mcp_server.py`
2. **Convert Scripts to Tools**: Each script becomes an @mcp.tool decorated function
3. **Maintain Functionality**: All existing script features must work in MCP tool format
4. **Add to Configuration**: Update `.mcp.json` with new server definition

### **Required Tool Conversions**:

**From `quota_monitor.py`**:
- `get_zai_quota_status()` → ZAI quota monitoring
- `track_zai_usage()` → Usage tracking and analytics
- `generate_quota_report()` → Comprehensive quota reports

**From `health_checker.py`**:
- `check_zai_health()` → Test ZAI MCP connectivity
- `validate_zai_config()` → Configuration validation
- `test_zai_endpoints()` → Endpoint connectivity testing

**From `config_validator.py`**:
- `validate_zai_config_schema()` → Configuration schema validation
- `fix_zai_config_paths()` → Path resolution fixes
- `generate_zai_templates()` → Configuration template generation

**From `config_template_generator.py`**:
- `create_zai_template()` → Create MCP server configurations
- `update_zai_settings()` → Dynamic configuration updates

### **Integration Steps**:
1. **Analyze Current Scripts**: Review all 8 scripts in `mini_agent/skills/zai-mcp-manager/scripts/`
2. **Create MCP Server**: Follow FastMCP pattern with proper tool definitions
3. **Update Configuration**: Add to `.mcp.json` as "zai-mcp-manager"
4. **Test Discovery**: Verify tools appear in Mini-Agent startup
5. **Functionality Testing**: Ensure all tools work identically to original scripts

### **Success Criteria**:
- ✅ ZAI MCP Manager tools become discoverable MCP tools
- ✅ All 8 script functions available through MCP protocol
- ✅ Tools appear in "Available Actions" during Mini-Agent startup
- ✅ No breaking changes to existing functionality

### **Reference Files**:
- Current scripts: `mini_agent/skills/zai-mcp-manager/scripts/`
- MCP pattern: `scripts/mcp_servers/minimax_coding_plan_mcp_server.py`
- Configuration: `mini_agent/config/.mcp.json`
- Skill docs: `mini_agent/skills/zai-mcp-manager/`

**Expected Outcome**: ZAI quota monitoring, health checking, and configuration management become first-class MCP tools that Mini-Agent can discover and use automatically.

---
*Target Time: 3-4 hours*
*Success: All ZAI management tools discoverable as MCP tools*
