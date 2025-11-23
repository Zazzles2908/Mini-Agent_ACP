# Z.AI Simplified Architecture Guide

## Problem Identified
**OVER-ENGINEERING**: Multiple redundant implementations for the same Z.AI web search functionality.

## Current Redundant Components
1. `zai_client.py` - Direct REST API calls (paid)
2. `zai_mcp_tools.py` - MCP protocol wrapper (free quotas)  
3. `zai_unified_tools.py` - Another MCP wrapper (redundant)
4. `.mcp.json` - MCP server configuration

## Recommended Simplified Architecture

### Single Z.AI Web Tool Implementation
**File**: `mini_agent/tools/zai_web_tool.py` (unified solution)

```python
class ZAIWebTool:
    """UNIFIED Z.AI web search and reading tool with AUTO-FALLBACK"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage_count = 0
        
        # Try MCP first (FREE quotas), fall back to Direct API (paid)
        self.mcp_available = await self._test_mcp_availability()
        self.direct_available = await self._test_direct_availability()
    
    async def search(self, query: str) -> dict:
        """Web search with intelligent fallbacks"""
        
        # Strategy 1: Use MCP if available (FREE)
        if self.mcp_available and self.usage_count < 100:
            return await self._mcp_search(query)
        
        # Strategy 2: Use Direct API if available and enabled
        if self.direct_available:
            return await self._direct_search(query)
        
        # Strategy 3: No Z.AI available, use other tools
        return {"success": False, "error": "Z.AI unavailable"}
```

### Configuration Simplification
**File**: `config.yaml` (single configuration)

```yaml
zai:
  enabled: true                    # Master enable/disable
  preferred_method: "mcp"          # "mcp" or "direct"
  fallback_enabled: true           # Auto-fallback if primary fails
  daily_quota_limit: 100           # MCP quota limit
  cost_protection: true            # Warn before paid calls
```

### MCP Integration Cleanup
**Single MCP Configuration**: `zai_mcp_config.json`

```json
{
  "mcp_servers": {
    "zai-web": {
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {"Authorization": "Bearer ${ZAI_API_KEY}"}
    }
  }
}
```

## Why This Matters

### Current Problems:
- **Code Duplication**: 3+ implementations doing same task
- **Configuration Confusion**: Multiple config files and flags
- **Debugging Nightmare**: Which tool is actually being used?
- **Quota Waste**: May not optimally use FREE quotas

### Benefits of Simplification:
- **Single Source of Truth**: One tool to maintain
- **Intelligent Fallback**: Auto-use free MCP, fall back to paid only when needed
- **Better Cost Control**: Clear visibility into what costs money
- **Easier Debugging**: One code path to debug

## Implementation Plan

### Phase 1: Create Unified Tool
1. Remove redundant implementations
2. Create single `ZAIWebTool` with fallback logic
3. Integrate with existing credit protection

### Phase 2: Configuration Consolidation  
1. Simplify config.yaml to single Z.AI section
2. Remove conflicting MCP configs
3. Add smart quota tracking

### Phase 3: MCP Integration Cleanup
1. Consolidate .mcp.json entries
2. Remove duplicate server definitions
3. Test MCP availability automatically

## Usage Examples

### Current (Over-Engineered)
```python
# Which one is actually being used?
client = ZAIClient(api_key)      # Direct API
tool = ZAIMCPTool(api_key)       # MCP  
unified = ZAIUnifiedTool()       # What?
```

### Recommended (Simplified)
```python
# Single, clear interface
tool = ZAIWebTool(api_key)
result = await tool.search("query")  # Auto-fallback logic handles the rest
```

## Key Insight
**GLM is just an LLM** - it doesn't have web search. All web functionality comes from Z.AI services. We need ONE way to access Z.AI, not three different implementations.

---

**Bottom Line**: The current architecture has multiple "how to call Z.AI" implementations, but we should have ONE smart implementation that handles all cases.
