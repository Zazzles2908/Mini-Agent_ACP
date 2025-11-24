# Understanding the Fundamental Architectural Issues

## Root Problem Analysis

Our current codebase has fundamental architectural problems that prevent proper provider switching:

### 1. **Architecture Complexity vs Reference Simplicity**

**Reference Implementation (Working):**
- Clean, focused architecture
- Single provider default: "anthropic"
- Simple LLM wrapper that properly appends /anthropic or /v1
- Direct Anthropic SDK usage
- No extra complexity

**Our Current Implementation (Broken):**
- Complex hybrid architecture supporting multiple protocols
- Bloated configuration with Z.AI integration, multiple API keys, etc.
- Our Anthropic client has custom logic that breaks standard Anthropic SDK usage
- Retry configuration issues

### 2. **Platform Differences**
- **Reference**: Uses China platform `https://api.minimaxi.com`
- **We use**: Global platform `https://api.minimax.io`
- **Result**: Different APIs, different authentication

### 3. **Client Implementation Differences**

**Reference AnthropicClient (Working):**
```python
def __init__(self, api_key: str, api_base: str = "https://api.minimaxi.com/anthropic", model: str = "MiniMax-M2", retry_config: RetryConfig | None = None):
    self.client = anthropic.Anthropic(base_url=api_base, api_key=api_key)
```

**Our AnthropicClient (Broken):**
- Has custom logic for "minimax.io" domains
- Manually appends "/anthropic" 
- Complex authentication handling
- Custom retry configuration issues

## The Real Solution

Instead of fixing our complex implementation, we need to:

1. **Strip down to reference pattern** - Remove all the extra complexity
2. **Copy reference architecture exactly** - Don't try to "improve" it
3. **Fix platform configuration** - Use proper global vs China platform setup
4. **Clean provider switching** - Simple, working LLM wrapper

### Why Provider Switching Doesn't Work

Our provider switching is broken because:
- Our wrapper has custom logic that interferes with standard SDKs
- Our Anthropic client doesn't follow reference patterns
- Our configuration is too complex and mismatched
- We have authentication issues from complex setup

## The Path Forward

1. **Implement reference architecture exactly** - Don't "enhance" it
2. **Test provider switching** - Verify both OpenAI and Anthropic work
3. **Clean up configuration** - Match reference patterns
4. **Remove complexity** - Focus on core functionality first

The key insight: **Keep it simple like the reference implementation.**
