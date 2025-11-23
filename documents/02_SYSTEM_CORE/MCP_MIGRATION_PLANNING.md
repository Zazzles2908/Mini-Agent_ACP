# MCP Migration Planning - Z.AI Implementation Consolidation

## Current State Analysis

**🔴 FRAGMENTED CHAOS IDENTIFIED (12 Z.AI implementations):**

### LLM Clients (4 files)
- `zai_client.py` - Direct REST API approach
- `claude_zai_client.py` - Claude-specific implementation  
- `extended_claude_zai_client.py` - Extended Claude variant
- `coding_plan_zai_client.py` - Coding plan specific

### Tools (8 files)  
- `zai_unified_tools.py` - Attempted consolidation
- `claude_zai_tools.py` - Claude-specific tools
- `zai_web_tools.py` - Web search tools
- `zai_direct_api_tools.py` - Direct API approach
- `zai_direct_web_tools.py` - Direct web tools  
- `zai_openai_tools.py` - OpenAI format tools
- `zai_openai_web_tools.py` - OpenAI web tools
- `zai_corrected_tools.py` - "Corrected" version

**TOTAL: 12 different implementations doing similar things**

## Critical Issues Identified

### 1. Inverted Security Logic
```python
# From zai_client.py - Line 22
from ..utils.credit_protection import block_zai_usage, check_zai_protection

# But then:
# "🚫 CREDIT PROTECTED - Z.AI client requires explicit config enablement"
# If credit protection blocks usage, why is it "enabled" in the code?
```

### 2. Multiple API Approaches
- **Direct REST API** calls
- **OpenAI format** wrappers  
- **Claude format** wrappers
- **Direct web** endpoints

### 3. Configuration Bypass
- Some implementations may ignore `enable_zai_search: false`
- No unified way to disable ALL Z.AI access

## MCP Migration Strategy (Aligned with User's 4-Phase Plan)

### Phase 1: Single Unified MCP Client (1-2 weeks)

**Target Architecture:**
```python
# New unified approach
class ZAIMCPClient:
    """Single MCP-based Z.AI client replacing all 12 implementations."""
    
    def __init__(self, mcp_config):
        self.mcp_client = mcp_client_from_config(mcp_config)
    
    async def web_search(self, query):
        """MCP-based web search - replace all existing implementations."""
        return await self.mcp_client.call_tool("webSearchPrime", {"query": query})
    
    async def web_read(self, url):
        """MCP-based web reading - replace all existing implementations."""
        return await self.mcp_client.call_tool("webRead", {"url": url})
```

**MCP Configuration:**
```json
{
  "mcpServers": {
    "zai-web-search": {
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    },
    "zai-web-reader": {
      "command": "remote", 
      "url": "https://api.z.ai/api/mcp/web_reader/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### Phase 2: Fix Credit Protection Logic (Immediate)

**Current Problem:**
```python
# The credit protection import suggests it blocks Z.AI
from ..utils.credit_protection import block_zai_usage, check_zai_protection

# But if it's blocking, why is the client trying to enable it?
# Credit protection logic is INVERTED
```

**Corrected Logic:**
```python
class UnifiedZaiCreditProtection:
    def __init__(self, config):
        self.config = config
    
    def is_zai_enabled(self):
        """Proper logic - check if explicitly enabled."""
        return self.config.get('enable_zai_search', False)
    
    def can_use_zai(self, tool_name):
        """Check if specific tool can be used."""
        if not self.is_zai_enabled():
            return False, "Z.AI disabled in configuration"
        
        current_usage = self.get_current_usage(tool_name)
        quota_limit = self.get_quota_limit(tool_name)
        
        if current_usage >= quota_limit:
            return False, f"{tool_name} quota exceeded"
        
        return True, "Proceed"
```

### Phase 3: MCP Tool Migration (2-4 weeks)

**Replace ALL 12 implementations with MCP calls:**

#### Migration Mapping
| Current Implementation | Replace With MCP Tool |
|----------------------|---------------------|
| `zai_client.py` | MCP server: webSearchPrime |
| `claude_zai_client.py` | MCP server: webSearchPrime |
| `zai_web_tools.py` | MCP server: webSearchPrime |
| `zai_direct_api_tools.py` | MCP server: webRead |
| All 12 files | 2 MCP tools |

### Phase 4: Configuration Simplification

**Single Source of Truth:**
```yaml
# mini_agent/config/config.yaml
tools:
  enable_zai_search: true  # Single config controls ALL Z.AI access
  
# Remove all these conflicting settings:
# - coding_plan_zai_client.py config
# - extended_claude_zai_client.py config  
# - zai_unified_tools.py config
# - etc.
```

## Migration Risk Assessment

### High Risk Items
1. **Breaking existing functionality** - Need to identify which of the 12 implementations are actually being used
2. **API compatibility** - Ensure MCP endpoints match current functionality
3. **Credit tracking** - MCP protocol needs to integrate with quota management

### Migration Strategy
1. **Audit current usage** - Determine which of the 12 implementations are actively used
2. **Parallel implementation** - Run MCP version alongside existing for testing
3. **Gradual migration** - Replace one implementation at a time
4. **Rollback plan** - Keep existing implementations disabled but available

## Next Steps

1. **Complete Phase 2** - Fix credit protection logic to properly block when disabled
2. **Audit usage** - Determine which of the 12 Z.AI implementations are actually needed
3. **Implement MCP client** - Create single unified client
4. **Test parallel** - Run both MCP and existing implementations
5. **Gradual migration** - Replace one implementation at a time

**Status**: Ready to begin MCP migration planning with concrete implementation strategy.
