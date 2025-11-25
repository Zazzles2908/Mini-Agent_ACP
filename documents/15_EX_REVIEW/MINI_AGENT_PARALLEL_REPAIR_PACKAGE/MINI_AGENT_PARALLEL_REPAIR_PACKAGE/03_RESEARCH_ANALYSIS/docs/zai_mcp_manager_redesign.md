# Z.AI MCP Manager Redesign Plan

**Date**: November 25, 2025  
**Status**: Architecture Redesign Required  
**Priority**: High - Critical for Tool Discovery and Integration

---

## 🎯 **PROBLEM STATEMENT**

The current zai-mcp-manager exists as a skill under `skills/` but is not discoverable as available tools. The architecture is fundamentally wrong because:

1. **Tool Discovery Failure**: Skill scripts are not exposed as MCP tools
2. **Architecture Mismatch**: Skills are for documentation, not execution
3. **No MCP Integration**: Scripts lack proper MCP server structure
4. **Missing Bridge**: No communication layer between skills and MCP ecosystem

---

## 🔍 **CURRENT ARCHITECTURE ANALYSIS**

### Current Structure
```
mini_agent/skills/zai-mcp-manager/
├── README.md              # Documentation only
├── SKILL.md               # Metadata and usage docs
├── SKILL.json             # Minimal configuration
├── requirements.txt       # Dependencies
└── scripts/               # Executable scripts (NOT exposed as tools)
    ├── config_validator.py
    ├── quota_monitor.py
    ├── health_checker.py
    ├── config_template_generator.py
    └── [other scripts]
```

### Issues Identified
- Scripts are not MCP tools (no `@mcp.tool` decorators)
- No proper tool discovery mechanism
- Missing FastMCP server structure
- No Pydantic models for validation
- Skills and tools exist in separate, disconnected systems

---

## 🏗️ **REDESIGN ARCHITECTURE**

### New Structure (MCP-First Design)
```
zai-mcp-manager/
├── zai_mcp_manager.py                 # Main FastMCP server
├── models/
│   ├── __init__.py
│   ├── quota_models.py               # Pydantic models
│   ├── health_models.py
│   ├── config_models.py
│   └── template_models.py
├── tools/
│   ├── __init__.py
│   ├── quota_tools.py                # Convert quota_monitor.py
│   ├── health_tools.py               # Convert health_checker.py
│   ├── config_tools.py               # Convert config_validator.py
│   └── template_tools.py             # Convert config_template_generator.py
├── utils/
│   ├── __init__.py
│   ├── quota_tracker.py              # Shared quota logic
│   ├── health_checker.py             # Shared health logic
│   ├── config_validator.py           # Shared config logic
│   └── zai_api_client.py             # Z.AI API client
├── pyproject.toml                    # MCP server configuration
├── requirements.txt                  # Dependencies
└── README.md                         # MCP server documentation
```

---

## 📋 **CONVERSION PLAN**

### Phase 1: Core MCP Infrastructure (1-2 days)

#### 1.1 Create FastMCP Server Base
```python
#!/usr/bin/env python3
"""
Z.AI MCP Manager - FastMCP Server Implementation
Converts skill scripts to discoverable MCP tools
"""

import asyncio
import os
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize MCP server
mcp = FastMCP("zai-mcp-manager")

# Constants
CHARACTER_LIMIT = 25000
ZAI_BASE_URL = "https://api.z.ai"

# Import tool modules
from tools.quota_tools import *
from tools.health_tools import *
from tools.config_tools import *
from tools.template_tools import *

if __name__ == "__main__":
    mcp.run()
```

#### 1.2 Create Pydantic Models
```python
# models/quota_models.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class QuotaStatus(BaseModel):
    """Quota status information"""
    searches_used: int = Field(..., description="Number of searches used")
    searches_total: int = Field(..., description="Total search quota")
    readers_used: int = Field(..., description="Number of readers used")
    readers_total: int = Field(..., description="Total reader quota")
    searches_remaining: int = Field(..., description="Searches remaining")
    readers_remaining: int = Field(..., description="Readers remaining")
    usage_percentage: float = Field(..., description="Overall usage percentage")
    status: str = Field(..., description="Status: healthy, warning, critical")
    last_updated: str = Field(..., description="Last update timestamp")

class QuotaAlert(BaseModel):
    """Quota alert configuration"""
    warning_threshold: float = Field(80.0, description="Warning threshold percentage")
    critical_threshold: float = Field(95.0, description="Critical threshold percentage")
    enable_notifications: bool = Field(True, description="Enable quota notifications")
```

### Phase 2: Convert Skill Scripts to MCP Tools (2-3 days)

#### 2.1 Quota Monitor → MCP Tools
**Current**: `scripts/quota_monitor.py` → `tools/quota_tools.py`

```python
# tools/quota_tools.py
from mcp.server.fastmcp import mcp
from pydantic import BaseModel
from models.quota_models import QuotaStatus, QuotaAlert

@mcp.tool(
    annotations={
        "title": "Check Z.AI Quota Status",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def check_quota_status(
    api_key: str,
    alert_config: Optional[QuotaAlert] = None
) -> str:
    """Check current Z.AI quota usage and status.
    
    Monitors search and reader quota usage for Z.AI Lite Plan.
    Provides real-time status with warning alerts.
    
    Args:
        api_key: Z.AI API key for authentication
        alert_config: Optional alert configuration settings
        
    Returns:
        Detailed quota status report with usage statistics
    """
    try:
        # Convert to internal quota monitor logic
        monitor = ZAIMCPQuotaMonitor(api_key, alert_config.dict() if alert_config else {})
        status = await monitor.check_quota_status()
        
        return format_quota_response(status)
    except Exception as e:
        return f"❌ Quota check failed: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Generate Quota Usage Report",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def generate_quota_report(
    api_key: str,
    days: int = 30,
    format_type: str = "markdown"
) -> str:
    """Generate comprehensive quota usage analytics report.
    
    Creates detailed reports showing quota consumption patterns,
    usage trends, and optimization recommendations.
    
    Args:
        api_key: Z.AI API key for authentication
        days: Number of days to analyze (1-365)
        format_type: Report format - "markdown" or "json"
        
    Returns:
        Comprehensive quota usage report with analytics
    """
    # Implementation here
    pass
```

#### 2.2 Health Checker → MCP Tools
**Current**: `scripts/health_checker.py` → `tools/health_tools.py`

```python
# tools/health_tools.py
@mcp.tool(
    annotations={
        "title": "Check Z.AI MCP Server Health",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def check_mcp_health(
    api_key: str,
    endpoints: Optional[List[str]] = None
) -> str:
    """Check health status of Z.AI MCP servers.
    
    Tests connectivity, response times, and availability
    of all Z.AI MCP endpoints with comprehensive health scoring.
    
    Args:
        api_key: Z.AI API key for authentication
        endpoints: Optional list of specific endpoints to check
        
    Returns:
        Detailed health report with performance metrics
    """
    # Implementation here
    pass
```

#### 2.3 Configuration Validator → MCP Tools
**Current**: `scripts/config_validator.py` → `tools/config_tools.py`

```python
# tools/config_tools.py
@mcp.tool(
    annotations={
        "title": "Validate Z.AI Configuration",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def validate_configuration(
    config_path: Optional[str] = None,
    check_connectivity: bool = True
) -> str:
    """Validate Z.AI MCP configuration and setup.
    
    Comprehensive validation of .env files, .mcp.json configurations,
    API key validity, and endpoint connectivity with scoring.
    
    Args:
        config_path: Path to configuration directory
        check_connectivity: Whether to test actual API connectivity
        
    Returns:
        Configuration validation report with scores and recommendations
    """
    # Implementation here
    pass
```

#### 2.4 Template Generator → MCP Tools
**Current**: `scripts/config_template_generator.py` → `tools/template_tools.py`

```python
# tools/template_tools.py
@mcp.tool(
    annotations={
        "title": "Generate Z.AI Configuration Templates",
        "readOnlyHint": False,
        "openWorldHint": False
    }
)
async def generate_config_templates(
    output_directory: str,
    include_examples: bool = True,
    generate_env_template: bool = True
) -> str:
    """Generate optimized Z.AI MCP configuration templates.
    
    Creates comprehensive configuration templates including .env files,
    .mcp.json configs, Python clients, and integration guides.
    
    Args:
        output_directory: Directory to write generated templates
        include_examples: Whether to include example configurations
        generate_env_template: Whether to generate .env template
        
    Returns:
        Summary of generated files and setup instructions
    """
    # Implementation here
    pass
```

### Phase 3: Tool Discovery Mechanism (1 day)

#### 3.1 Discovery Protocol
```python
# Add to main server
@mcp.tool()
async def discover_zai_tools() -> str:
    """Discover all available Z.AI MCP Manager tools.
    
    Returns complete list of available tools with descriptions
    and usage examples for the Z.AI MCP Manager.
    
    Returns:
        Comprehensive list of available tools and their capabilities
    """
    tools_info = {
        "quota_management": [
            "check_quota_status - Monitor current quota usage",
            "generate_quota_report - Generate usage analytics",
            "set_quota_alerts - Configure quota warnings"
        ],
        "health_monitoring": [
            "check_mcp_health - Test MCP server connectivity",
            "monitor_performance - Track response times",
            "diagnose_issues - Troubleshoot problems"
        ],
        "configuration": [
            "validate_configuration - Check setup integrity",
            "optimize_settings - Improve configuration",
            "backup_config - Create configuration backups"
        ],
        "template_generation": [
            "generate_config_templates - Create config files",
            "generate_integration_guide - Create setup docs",
            "generate_client_code - Create Python clients"
        ]
    }
    
    return format_discovery_response(tools_info)
```

### Phase 4: Skill-to-MCP Communication Bridge (1 day)

#### 4.1 Skill Integration Layer
```python
# bridge/skill_mcp_bridge.py
class SkillMCPBridge:
    """Bridge between skills and MCP tools"""
    
    def __init__(self):
        self.mcp_server_path = "zai_mcp_manager.py"
        self.skill_path = "skills/zai-mcp-manager"
    
    def convert_skill_to_mcp(self, skill_script: str) -> str:
        """Convert skill script to MCP tool format"""
        # Parse skill script
        # Extract functionality
        # Generate MCP tool with proper decorators
        # Return MCP-compatible code
        pass
    
    def register_skill_as_tool(self, skill_path: str) -> bool:
        """Register skill as discoverable MCP tool"""
        # Convert skill
        # Generate MCP tool file
        # Update tool registry
        pass
    
    def discover_unregistered_skills(self) -> List[str]:
        """Find skills that haven't been converted to MCP tools"""
        # Scan skills directory
        # Check for missing MCP implementations
        # Return list of unregistered skills
        pass
```

### Phase 5: Integration & Testing (1-2 days)

#### 5.1 Integration Points
1. **Agent Integration**: Update agent to load Z.AI MCP tools
2. **Discovery Integration**: Add to tool discovery mechanism
3. **Skills Bridge**: Auto-convert skill scripts to MCP tools
4. **Testing Suite**: Comprehensive MCP tool testing

---

## 🔄 **MIGRATION STRATEGY**

### Step 1: Parallel Development
- Keep existing skill scripts functional
- Develop new MCP server alongside
- Test both systems in parallel

### Step 2: Gradual Migration
- Convert one tool category at a time
- Maintain backward compatibility
- Update documentation progressively

### Step 3: Full Transition
- Remove skill scripts when all tools converted
- Update agent configuration to use MCP server
- Deprecate skill-based approach

---

## 🧪 **TESTING PLAN**

### Unit Tests
- Each MCP tool with comprehensive test cases
- Input validation with Pydantic models
- Error handling and edge cases

### Integration Tests
- MCP server lifecycle (start/stop)
- Tool discovery mechanism
- Inter-tool communication

### End-to-End Tests
- Full agent integration scenarios
- Real Z.AI API connectivity (with test keys)
- Performance and reliability testing

---

## 📚 **DOCUMENTATION UPDATES**

### 1. MCP Server Documentation
- Complete FastMCP server documentation
- Tool usage examples and API reference
- Configuration and deployment guides

### 2. Migration Guide
- Step-by-step migration from skill to MCP
- Backward compatibility information
- Breaking changes documentation

### 3. Integration Guide
- How to use Z.AI MCP tools in agents
- Best practices for quota management
- Troubleshooting common issues

---

## 🎯 **SUCCESS CRITERIA**

1. **✅ Tool Discovery**: All zai-mcp-manager functionality available as MCP tools
2. **✅ Proper Architecture**: FastMCP server with Pydantic models
3. **✅ Skill Bridge**: Automatic conversion of skill scripts to MCP tools
4. **✅ Integration**: Seamless integration with Mini-Agent tool system
5. **✅ Documentation**: Complete documentation for new architecture
6. **✅ Testing**: Comprehensive test coverage for all tools

---

## 🚀 **IMPLEMENTATION TIMELINE**

**Total Estimate: 6-8 days**

- **Days 1-2**: Phase 1 - Core MCP Infrastructure
- **Days 3-5**: Phase 2 - Convert Skill Scripts to MCP Tools
- **Day 6**: Phase 3 - Tool Discovery Mechanism
- **Day 7**: Phase 4 - Skill-to-MCP Communication Bridge
- **Days 8-9**: Phase 5 - Integration & Testing

---

## 💡 **KEY IMPROVEMENTS**

### Before (Current)
- ❌ Skills not discoverable as tools
- ❌ Manual script execution required
- ❌ No proper MCP integration
- ❌ Architecture mismatch

### After (Redesigned)
- ✅ All functionality as discoverable MCP tools
- ✅ Proper FastMCP server architecture
- ✅ Pydantic input validation
- ✅ Tool discovery and auto-conversion
- ✅ Seamless Mini-Agent integration
- ✅ Professional MCP server structure

---

## 🔗 **REFERENCES**

- **Reference Implementation**: `minimax_coding_plan_mcp_server.py`
- **Current Skill**: `mini_agent/skills/zai-mcp-manager/`
- **MCP Protocol**: https://modelcontextprotocol.io/
- **FastMCP Framework**: https://github.com/mcp-server/fastmcp

---

**Next Steps**: Begin Phase 1 implementation with core MCP infrastructure setup.
