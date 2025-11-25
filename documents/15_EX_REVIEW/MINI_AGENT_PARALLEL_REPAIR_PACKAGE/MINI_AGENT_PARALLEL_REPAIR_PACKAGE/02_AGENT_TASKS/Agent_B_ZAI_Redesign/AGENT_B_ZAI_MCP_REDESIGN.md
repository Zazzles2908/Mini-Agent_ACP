# Agent B: ZAI-MCP-Manager Architecture Redesign
*Priority: CRITICAL - Convert skill scripts to discoverable MCP tools*

## 🎯 Mission
Transform zai-mcp-manager from skill scripts under `skills/` into discoverable MCP tools that Mini-Agent can actually use.

## 📋 Current Problem
- **Issue:** Scripts under `skills/zai-mcp-manager/scripts/` not available as tools
- **Architecture:** Skills provide documentation, scripts provide execution - disconnected
- **Impact:** ZAI quota/health tools invisible to Mini-Agent
- **Location:** `skills/zai-mcp-manager/scripts/`

## 🛠️ Implementation Steps

### Step 1: Analyze Current Scripts
**Review These Files:**
- `quota_monitor.py` - ZAI usage tracking
- `health_checker.py` - Connection tests
- `config_validator.py` - Setup validation  
- `config_template_generator.py` - Configuration templates

### Step 2: Create MCP Server Structure
**Create:** `zai_mcp_manager_mcp_server.py`
**Follow Pattern:** `minimax_coding_plan_mcp_server.py`

**Key Conversions:**
```python
# quota_monitor.py → 
@mcp.tool
async def get_zai_quota() -> str: ...

@mcp.tool  
async def track_zai_usage() -> str: ...

# health_checker.py →
@mcp.tool
async def check_zai_health() -> str: ...

@mcp.tool
async def validate_zai_config() -> str: ...

# config_validator.py → 
@mcp.tool
async def validate_zai_setup() -> str: ...

# config_template_generator.py →
@mcp.tool
async def generate_zai_templates() -> str: ...
```

### Step 3: Add to MCP Configuration
**Update:** `.mcp.json`
```json
{
  "zai-mcp-manager": {
    "command": "python", 
    "args": ["zai_mcp_manager_mcp_server.py"],
    "disabled": false
  }
}
```

### Step 4: Testing & Integration
```bash
# Test tool discovery
mini-agent
# Should show ZAI tools in available actions

# Test individual tools
# Use new MCP tools to verify functionality
```

## 📁 Resources
- **Redesign Plan:** `/workspace/docs/zai_mcp_manager_redesign.md`
- **Reference Implementation:** `minimax_coding_plan_mcp_server.py`
- **Current Scripts:** `skills/zai-mcp-manager/scripts/`

## 🎯 Success Criteria
**Complete when:** ZAI quota/health tools appear in Mini-Agent's available tools list and are functional.

## ⏱️ Estimated Time
**Target:** 4-5 hours
**Max:** 6 hours

## 📝 Expected Tool Output
**Before:** No ZAI tools visible
**After:** 
- `get_zai_quota` - Check remaining searches/readers
- `check_zai_health` - Verify connectivity  
- `validate_zai_config` - Test configuration
- `generate_zai_templates` - Create optimized configs
