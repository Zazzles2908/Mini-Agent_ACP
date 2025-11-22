# Complete Z.AI Web Search Implementation Guide

## 🚨 CRITICAL SECURITY ISSUE IDENTIFIED

**Current Status**: Z.AI web search tools can **bypass configuration protection**, potentially consuming credits despite `enable_zai_search: false` settings.

### Security Gap
```python
# PROBLEM: Tools bypass config protection
simple_web_search.py → Direct API calls → Ignores config settings
                    → Can consume credits → User unaware
```

**This explains credit consumption despite "disabled" configuration!**

---

## Architecture Overview

### Current System Design
- **Primary Model**: MiniMax-M2 (300 prompts/5hrs)
- **Secondary Model**: Z.AI GLM-4.6 (web search + reading)
- **Integration**: Direct API calls to `https://api.z.ai/api/coding/paas/v4`
- **Configuration**: Should be controlled via `enable_zai_search` setting

### Lite Plan Capabilities
- **Model**: GLM-4.6 only (no model selection on Lite plan)
- **Web Searches**: 100 searches included (FREE)
- **Web Readers**: 100 readers included (FREE)
- **Total Cost**: $0 for web functionality (FREE on Lite plan)

## Configuration

### Environment Variables
```bash
# Required for Z.AI web search
setx ZAI_API_KEY your_zai_api_key
```

### Configuration File
```yaml
# mini_agent/config/config.yaml
tools:
  enable_zai_search: true   # ⚠️ When false, may be bypassed by some tools
  
# CRITICAL: This setting may not protect all tools!
# Some tools make direct API calls that ignore this setting
```

### ⚠️ Important Security Note
**Current Issue**: The `enable_zai_search: false` setting does NOT protect against all Z.AI access. Some tools:
- Make direct API calls that bypass config
- Ignore the `enable_zai_search` setting
- Can consume Lite Plan credits without user awareness

## Implementation Status

### ✅ Working Components
1. **Direct API Integration**: Confirmed working to `https://api.z.ai/api/coding/paas/v4`
2. **GLM-4.6 Model**: Available and functional on Lite plan
3. **Web Search Capability**: Returns search results with sources
4. **Web Reading Capability**: Extracts and reads web content
5. **Zero Credit Testing**: Confirmed 0 credits consumed during testing

### ❌ Known Issues
1. **Configuration Bypass**: Some tools ignore `enable_zai_search: false`
2. **Unified Protection**: No system-wide credit protection
3. **Credit Visibility**: No clear indication of current usage
4. **True Disable**: Cannot truly disable all Z.AI access

## Integration Architecture

### Current Flow
```
User Request → MiniMax-M2 (Primary Reasoning)
                      ↓
              Z.AI GLM-4.6 (Web Intelligence)
                      ↓
         https://api.z.ai/api/coding/paas/v4
                      ↓
         Search Results + Web Content
```

### File Structure
```
mini_agent/
├── llm/
│   ├── zai_client.py        # Main Z.AI client
│   └── glm_client.py        # GLM model integration
├── tools/
│   ├── simple_web_search.py # ⚠️ Bypasses config protection
│   ├── zai_tools.py         # Unified Z.AI interface
│   └── zai_unified_tools.py # Consolidated access
└── utils/
    └── credit_protection.py # Partial protection only
```

## Usage Examples

### Web Search
```python
# Z.AI Web Search (uses FREE Lite plan quotas)
# Tool: simple_web_search.py (may bypass config)
result = await web_search("latest AI developments")
```

### Web Reading
```python
# Z.AI Web Reading (uses FREE Lite plan quotas)
# Extract content from web pages
content = await web_read("https://example.com")
```

## Testing Results

### Confirmed Working
- ✅ **HTTP 200 Status**: API calls successful
- ✅ **Search Results**: Returns web search results with sources
- ✅ **Content Reading**: Successfully extracts web page content
- ✅ **GLM-4.6 Model**: Confirmed available on Lite plan
- ✅ **Credit Testing**: 0 credits consumed during testing
- ✅ **Direct API**: `https://api.z.ai/api/coding/paas/v4` endpoint working

### Credit Consumption
- **Lite Plan**: 100 searches + 100 readers (FREE)
- **No Additional Cost**: Web functionality included in Lite plan
- **Current Issue**: Potential hidden consumption due to config bypass

## Security Recommendations

### Immediate Actions Needed
1. **Unified Protection**: All Z.AI tools must check `enable_zai_search`
2. **Config Enforcement**: Direct API calls must respect configuration
3. **Credit Monitoring**: Real-time tracking of Lite Plan usage
4. **Visibility**: Clear indication of which tools are active

### Future Improvements
```python
# Ideal unified credit protection
class UnifiedZaiProtection:
    def check_allowed(self, tool_name, usage_type):
        if not self.config.get('enable_zai_search', False):
            return False, "Z.AI disabled in configuration"
        
        current_usage = self.get_current_usage(usage_type)
        if current_usage >= self.get_quota_limit(usage_type):
            return False, f"{usage_type} quota exceeded"
        
        return True, "Proceed"
```

## Corrected Information

### ❌ Previous Incorrect Claims
- ~~"Uses Coding Plan credits"~~ → ✅ Uses FREE Lite plan quota
- ~~"Anthropic-compatible endpoint"~~ → ✅ Direct API to `https://api.z.ai/api/coding/paas/v4`
- ~~"120 prompts every 5 hours"~~ → ✅ 100 searches + 100 readers on Lite plan
- ~~"Multiple GLM models available"~~ → ✅ Only GLM-4.6 on Lite plan

### ✅ Correct Implementation
- **Free Web Search**: 100 searches included in Lite plan
- **Free Web Reading**: 100 readers included in Lite plan
- **Direct API**: Calls to `https://api.z.ai/api/coding/paas/v4`
- **Single Model**: GLM-4.6 only (Lite plan limitation)

## Troubleshooting

### Common Issues
1. **Credits Being Consumed Unexpectedly**
   - **Cause**: Tools bypassing config protection
   - **Solution**: Fix unified credit protection system

2. **Web Search Not Working**
   - **Check**: `ZAI_API_KEY` environment variable set
   - **Verify**: API key has valid Lite plan access
   - **Test**: Direct API call to endpoint

3. **Config Setting Ignored**
   - **Cause**: Known issue with direct API tools
   - **Solution**: Require all tools to check configuration

### Debug Commands
```bash
# Check if Z.AI is actually accessible
curl -H "Authorization: Bearer $ZAI_API_KEY" \
     "https://api.z.ai/api/coding/paas/v4/models"

# Test config bypass issue
python -c "from mini_agent.tools.simple_web_search import SimpleWebSearch; print('Bypasses config')"
```

## Integration with MiniMax-M2

### Combined Usage Pattern
1. **Primary Reasoning**: Use MiniMax-M2 for complex analysis
2. **Web Intelligence**: Use Z.AI for current information gathering
3. **Result Synthesis**: Combine both for comprehensive responses
4. **Quota Management**: Monitor both 300 prompts (M2) and 100 searches (Z.AI)

### Workflow Example
```python
# User asks for current AI developments
# 1. MiniMax-M2: Analyzes what information is needed
# 2. Z.AI: Searches for latest AI developments  
# 3. MiniMax-M2: Synthesizes and presents findings
# Result: Current, accurate information with proper reasoning
```

---

## Summary

### Current Status: Functional but Insecure
- ✅ **Web search works** with direct API integration
- ✅ **Lite plan provides FREE quotas** (100 searches + 100 readers)
- ❌ **Configuration protection is bypassable** by some tools
- ❌ **Credit consumption is not fully controlled**

### Recommended Actions
1. **Fix config bypass issue** for true Z.AI control
2. **Implement unified credit protection** system
3. **Add visibility** into Z.AI tool usage
4. **Test thoroughly** after security fixes

**This implementation provides powerful web capabilities but requires security fixes to prevent unexpected credit consumption.**
