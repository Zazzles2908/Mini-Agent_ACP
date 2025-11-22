# OpenAI Web Functions Wrapper - Implementation Plan

## 🎯 Problem Solved
**Original Issue**: GLM Lite plan doesn't provide direct web function access  
**Solution**: OpenAI SDK wrapper around Z.AI backend  
**Benefit**: MiniMax-M2 compatibility + proven Z.AI implementation

## 🏗️ Architecture
```
MiniMax-M2 (OpenAI SDK)
       ↓
OpenAI Web Functions Wrapper
       ↓  
Z.AI Backend (GLM-4.6 - FREE with Lite plan)
       ↓
Direct API calls to https://api.z.ai/api/coding/paas/v4
```

## 📦 Package Components
1. **base.py**: Tool framework (Tool, ToolResult classes)
2. **openai_web_functions.py**: OpenAI SDK compatible interface
3. **zai_unified_tools.py**: Z.AI backend implementation (GLM-4.6)
4. **integration_example.py**: Integration examples
5. **test_openai_integration.py**: Safe testing without API calls

## 🛠️ Implementation Strategy

### Phase 1: Integration Setup
- [ ] Copy package to main Mini-Agent directory
- [ ] Add to tool loader with credit protection
- [ ] Test without API calls (mock environment)

### Phase 2: Safe Testing
- [ ] Load tools without real API calls
- [ ] Verify schema compatibility
- [ ] Test error handling and fallbacks

### Phase 3: Production Deployment
- [ ] Enable Z.AI tools with proper configuration
- [ ] Test with real API calls (small queries)
- [ ] Monitor credit usage (should be $0)

### Phase 4: Cleanup
- [ ] Remove old conflicting Z.AI implementations
- [ ] Update documentation
- [ ] Commit changes

## ✅ Key Benefits
- **OpenAI SDK Format**: Direct compatibility with MiniMax-M2
- **Proven Backend**: Uses existing Z.AI implementation
- **Cost Control**: GLM-4.6 (FREE) + 2k token limits
- **Safety**: Maintains all credit protection mechanisms
- **Minimal Changes**: No disruption to existing functionality

## 🔧 Technical Details
- **Model**: GLM-4.6 (FREE with Lite plan)
- **Quota**: ~120 prompts every 5 hours
- **Token Limit**: 2000 max per call
- **API**: Direct calls to https://api.z.ai/api/coding/paas/v4
- **Tools**: web_search, web_read, web_research

## 🚫 Credit Safety
- Uses GLM-4.6 (not GLM-4.5 which costs money)
- Token limits prevent quota exhaustion
- Configuration-based activation
- Testing without API calls initially