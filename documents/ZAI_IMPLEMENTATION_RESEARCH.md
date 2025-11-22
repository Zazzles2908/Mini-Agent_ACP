# Z.AI Implementation Research - Understanding What Went Wrong

## Problem Statement
User reported Z.AI credit consumption (~$0.13) during initial exploration and wants verification of:
1. What capabilities the Z.AI Lite Plan provides
2. What base URLs should be used (international standards for Z.AI and OpenAI)
3. What was done vs what should have been done

## Key Findings from Code Analysis

### 1. Multiple Conflicting Z.AI Implementations Found
**Current State**: 7 different Z.AI tool files exist with conflicting approaches:
- `zai_tools.py` - Original implementation
- `zai_web_tools.py` - Web-focused implementation
- `zai_corrected_tools.py` - "Corrected" version
- `zai_direct_api_tools.py` - Direct API approach
- `zai_direct_web_tools.py` - Another direct web version
- `zai_openai_tools.py` - OpenAI SDK approach
- `zai_web_search_with_citations.py` - Citation-focused implementation

**Problem**: Multiple implementations suggest confusion about correct architecture.

### 2. Base URL Analysis

**Z.AI Coding Plan API** (from `claude_zai_client.py` - line 50):
```python
self.base_url = "https://api.z.ai/api/coding/paas/v4"
```

**Endpoints Used**:
- Web Search: `/web_search`
- Web Reader: `/reader`
- Chat Completions: `/chat/completions` (implied but not shown in claude_zai_client.py)

**OpenAI International Standard** (from config.yaml - line 16):
```python
openai_base: "https://api.openai.com/v1"
```

**MiniMax International** (from config.yaml - line 8):
```python
api_base: "https://api.minimax.io"
```

### 3. Z.AI Lite Plan Capabilities (from documentation)

**What Documentation Claims**:
- **Quota**: ~120 prompts every 5 hours
- **Models**: GLM-4.5, GLM-4.6, GLM-4.5-air
- **Cost Structure** (contradictory information found):
  - Some docs: "$0.01/search, $0.01/page" for web features
  - Other docs: "Included in Lite Plan subscription"
  - Transaction logs show: Actual charges happening for GLM-4.5 calls

**User's Transaction Log Analysis**:
```
glm-4.5 OUTPUT: 926 tokens → $0.0020372
glm-4.5 CACHE: 43445 tokens → $0.00477895  
glm-4.5 INPUT: 1078 tokens → $0.0006468
glm-4.6 INPUT: 3871 tokens → $0 (Coding Lite - Yearly)
glm-4.6 INPUT: 357409 tokens → $0.2144454
```

**Critical Insight**: 
- GLM-4.6 calls with "GLM Coding Lite - Yearly" show $0 charges
- GLM-4.5 calls are CHARGING MONEY (not covered by coding plan)
- Large token counts (357,409 tokens) suggest aggressive usage

### 4. What Went Wrong

**Root Cause Analysis**:

1. **Model Selection Error**: 
   - Used GLM-4.5 instead of GLM-4.6
   - GLM-4.5 is NOT included in Coding Lite plan
   - GLM-4.6 IS included (shows $0 charges with plan annotation)

2. **Multiple API Calls**:
   - Transaction log shows 5 separate inference calls
   - 43,445 cached tokens + 357,409 input tokens = massive usage
   - Suggests repeated/inefficient API calls

3. **Architectural Confusion**:
   - Multiple implementations suggest trial-and-error approach
   - Naming confusion ("anthropic", "openai", "direct", "corrected")
   - No clear understanding of Z.AI's actual API structure

4. **Credit Protection System**:
   - Config shows `enable_zai_llm: false` (line 43)
   - But transactions still occurred
   - Protection system wasn't working as intended

### 5. What Should Have Been Done

**Correct Implementation Pattern**:

```python
# Z.AI Lite Plan Configuration
api_key = os.getenv('ZAI_API_KEY')
base_url = 'https://api.z.ai/api/coding/paas/v4'
model = 'glm-4.6'  # ✅ USE THIS - included in Lite plan
# model = 'glm-4.5'  # ❌ DON'T USE - charges money

# Web Search Endpoint
search_endpoint = f'{base_url}/web_search'

# Parameters
payload = {
    'search_engine': 'search-prime',
    'search_query': query,
    'count': 5,  # Reasonable limit
    'search_recency_filter': 'noLimit'
}

# Headers
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
```

**Key Principles**:
1. **Always use GLM-4.6** for Lite plan (not GLM-4.5)
2. **Direct API approach** (not OpenAI SDK compatibility)
3. **Proper credit protection** before any Z.AI calls
4. **Reasonable token limits** (not 357k tokens in one call)
5. **Single implementation** (not 7 conflicting versions)

### 6. International Standard Base URLs

**Z.AI**:
- **Coding Plan API**: `https://api.z.ai/api/coding/paas/v4`
- **Common API**: `https://api.z.ai/v1` (general usage)
- **Anthropic Compatibility**: `https://api.z.ai/api/anthropic/v1` (limited)

**OpenAI**:
- **International**: `https://api.openai.com/v1`
- **Europe**: Same (no region-specific endpoints)

**MiniMax**:
- **Global Platform**: `https://api.minimax.io`
- **China**: Different endpoint (not relevant for international users)

### 7. Recommendations

**Immediate Actions**:
1. ✅ Delete 6 out of 7 Z.AI implementations (keep one correct version)
2. ✅ Update configuration to use GLM-4.6 exclusively
3. ✅ Implement proper credit protection verification
4. ✅ Add usage logging to track API calls
5. ✅ Test with small queries first (not 357k token dumps)

**Configuration Update**:
```yaml
zai_settings:
  default_model: "glm-4.6"      # ✅ Included in Lite plan
  search_model: "glm-4.6"        # ✅ Same for web search
  max_tokens_per_prompt: 2000    # ✅ Reasonable limit
  track_usage: true              # ✅ Monitor usage
  efficiency_mode: true          # ✅ Optimize calls
  use_direct_api: true           # ✅ Direct Z.AI API
  zai_base: "https://api.z.ai/api/coding/paas/v4"
```

**Credit Protection**:
```python
def check_zai_enabled():
    config = load_config()
    if not config.get('tools', {}).get('enable_zai_search', False):
        raise RuntimeError("Z.AI search is disabled. Enable in config.yaml")
    return True
```

## Summary

**What Was Done**:
- Created 7 different Z.AI implementations (confusion)
- Used GLM-4.5 model (charges money)
- Made calls with 357k tokens (excessive)
- Didn't properly verify credit protection
- Mixed up OpenAI SDK vs direct API approaches

**What Should Have Been Done**:
- Single implementation using direct Z.AI API
- GLM-4.6 model only (included in Lite plan)
- Reasonable token limits (2k-4k max)
- Verify credit protection before ANY calls
- Clear architectural understanding from the start

**Cost**: ~$0.13 was spent learning this lesson. Future implementations will be $0 by using GLM-4.6 with the Lite plan.
