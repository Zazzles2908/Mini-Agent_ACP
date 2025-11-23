# Recommended Z.AI Implementation: MCP-First Architecture

## The Smart Hybrid Solution

Instead of pure MCP or pure direct API, use a **progressive fallback strategy**:

### 1. **Single Z.AI Tool Implementation**
**File**: `mini_agent/tools/zai_web_tool.py`

```python
class ZAIWebTool(Tool):
    """Smart Z.AI tool with MCP-first, Direct-fallback logic"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.mcp_available = None  # Will test on first use
        self.usage_count = 0
        self.mcp_quota_used = 0
        self.mcp_quota_limit = 100  # FREE quotas
    
    async def execute(self, query: str, max_results: int = 3) -> ToolResult:
        """Execute with intelligent fallback logic"""
        
        # Strategy 1: Try MCP first (FREE)
        if self.mcp_available is not False:  # Not explicitly disabled
            result = await self._try_mcp_search(query, max_results)
            if result.success:
                return result
        
        # Strategy 2: Fallback to Direct API if available and allowed
        if check_zai_protection():  # Only if explicitly enabled
            result = await self._direct_api_search(query, max_results)
            if result.success:
                return result
        
        # Strategy 3: No Z.AI available
        return ToolResult(
            success=False,
            content="",
            error="Z.AI unavailable - enable in config or use within MCP quotas"
        )
    
    async def _try_mcp_search(self, query: str, max_results: int) -> ToolResult:
        """Try MCP search with quota tracking"""
        
        if self.mcp_quota_used >= self.mcp_quota_limit:
            return ToolResult(
                success=False,
                content="",
                error=f"MCP quota exceeded ({self.mcp_quota_used}/{self.mcp_quota_limit})"
            )
        
        try:
            # Call Z.AI MCP endpoint directly
            mcp_result = await self._call_zai_mcp(query, max_results)
            self.mcp_quota_used += 1
            return ToolResult(
                success=True,
                content=self._format_mcp_result(mcp_result),
                metadata={"quota_used": self.mcp_quota_used, "method": "mcp"}
            )
        except Exception as e:
            # MCP failed, will try direct API
            self.mcp_available = False
            return ToolResult(success=False, content="", error=str(e))
```

### 2. **Simplified Configuration**
**File**: `config.yaml` (single config section)

```yaml
zai_web:
  enabled: true                    # Master enable/disable  
  prefer_mcp: true                 # Try MCP first (default: true)
  fallback_to_direct: true         # Allow direct API if enabled
  mcp_quota_limit: 100             # FREE quota limit
  cost_warnings: true              # Show cost context
  
# Credit protection remains the same
tools:
  enable_zai_web_tools: false      # Controls both MCP and direct
```

### 3. **Streamlined MCP Config**
**File**: `.mcp.json` (consolidated)

```json
{
  "mcpServers": {
    "zai-web": {
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {"Authorization": "Bearer ${ZAI_API_KEY}"},
      "timeout": 30
    },
    "zai-reader": {
      "command": "remote", 
      "url": "https://api.z.ai/api/mcp/web_reader_prime/mcp",
      "headers": {"Authorization": "Bearer ${ZAI_API_KEY}"},
      "timeout": 45
    }
  },
  "quotas": {
    "zai_web_search": {"daily_limit": 100, "warnings": [80, 95]},
    "zai_web_reader": {"daily_limit": 100, "warnings": [80, 95]}
  }
}
```

### 4. **Remove Redundant Code**
**Delete these files** (90% code reduction):
- `zai_client.py` (replaced by single tool with fallback)
- `zai_mcp_tools.py` (functionality moved to main tool)
- `zai_unified_tools.py` (redundant wrapper)
- Complex retry logic and duplicate configurations

## **Benefits of This Approach**

### **For Development:**
- **Single implementation** to maintain
- **Clear priorities**: Free MCP → Paid Direct → Not Available
- **Better testing**: One code path, not three
- **Simplified debugging**: All Z.AI calls go through one place

### **For Users:**
- **Automatic cost optimization**: Uses FREE quotas first
- **Reliability**: Falls back if one method fails
- **Transparency**: Clear indication of which method was used
- **Safety**: Hard quota limits prevent surprise bills

### **For Integration:**
- **Fits existing architecture**: Uses standard Tool interface
- **Credit protection compatible**: Works with existing protection system
- **MCP integration ready**: Can still use if MCP config is preferred
- **Minimal config changes**: Single enable/disable flag

## **Migration Path**

### **Phase 1: Create Unified Tool** (1-2 hours)
1. Create `ZAIWebTool` with MCP-first logic
2. Delete redundant implementations  
3. Update config to single section

### **Phase 2: Test & Validate** (1 hour)
1. Test MCP quota usage
2. Test fallback logic
3. Verify credit protection

### **Phase 3: Production Ready** (30 minutes)
1. Deploy to agent
2. Verify existing workflows
3. Remove old configuration

## **Bottom Line**

**MCP-only is too restrictive** (no fallback, protocol overhead)
**Direct-only wastes free quotas** (ignores FREE MCP)  
**MCP-First hybrid gives the best of both worlds:**
- ✅ Uses FREE quotas automatically
- ✅ Has fallback for reliability  
- ✅ Fits existing architecture
- ✅ Massive code reduction
- ✅ Single point of maintenance

**This approach transforms 4 complex implementations into 1 smart tool that automatically chooses the best method.**
