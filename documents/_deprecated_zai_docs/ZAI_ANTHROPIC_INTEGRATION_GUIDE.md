# Z.AI Anthropic Web Search Integration

## Overview

The Z.AI Anthropic Web Search tool provides web search capabilities using Z.AI through the **Anthropic-compatible endpoint** (`https://api.z.ai/api/anthropic`) for natural citations and Claude Code integration.

## Key Benefits

✅ **Uses Coding Plan Credits**: Routes through Anthropic endpoint using your coding plan (~120 prompts every 5 hours)  
✅ **Natural Citations**: Returns results in Claude's `search_result` block format for automatic source attribution  
✅ **Claude Code Integration**: Works seamlessly with Claude Code's citation system  
✅ **No Direct API Calls**: Avoids separate Z.AI API usage that consumes different credits  
✅ **Production Ready**: Follows Mini-Agent tool patterns with proper error handling  

## How It Works

```
User Query → Mini-Agent → Z.AI Anthropic Tool → Anthropic API → GLM Web Search → Claude search_result blocks
```

### Architecture

1. **Environment Setup**: Uses `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` environment variables
2. **API Routing**: Routes requests through Anthropic-compatible endpoint
3. **Tool Integration**: Formats results as Claude's `search_result` blocks
4. **Citation Support**: Enables natural source attribution in Claude responses

## Usage

### Environment Configuration

```bash
# Set your Z.AI API key
setx ZAI_API_KEY your_zai_api_key

# Configure for Anthropic endpoint (done automatically)
setx ANTHROPIC_AUTH_TOKEN your_zai_api_key
setx ANTHROPIC_BASE_URL https://api.z.ai/api/anthropic
```

### Tool Parameters

- **query**: Search query or research question (required)
- **max_results**: Number of results (1-10, default 7)
- **depth**: Search depth - 'quick' (3 sources), 'comprehensive' (7 sources), 'deep' (10 sources)

### Example Usage

```python
# In Mini-Agent
zai_anthropic_web_search(
    query="Z.AI DevPack Claude integration",
    max_results=5,
    depth="comprehensive"
)
```

## Tool Output Format

The tool returns results in two formats:

1. **Display Format**: Human-readable summary with search results
2. **Claude Format**: `search_result` blocks for natural citations

### Sample Output

```
**🔍 Z.AI Web Search Results (via Anthropic endpoint)**

**Query:** Z.AI DevPack Claude integration
**Depth:** comprehensive
**Max Results:** 5

**💡 Usage Information:**
- Endpoint: Anthropic-compatible API (coding plan)
- Credit Usage: Counts toward ~120 prompts every 5 hours
- Benefits: Natural citations, Claude Code integration

**📊 Search Results:**
1. **Z.AI DevPack Overview**
   - Source: https://docs.z.ai/devpack/overview
   - Content: DevPack provides GLM model integration...

**🤖 Claude Search Result Blocks (for natural citations):**
```json
[
  {
    "type": "search_result",
    "source": "https://docs.z.ai/devpack/overview",
    "title": "Z.AI DevPack Overview",
    "content": [{"type": "text", "text": "DevPack provides..."}],
    "citations": {"enabled": true}
  }
]
```
```

## Integration with Mini-Agent

The tool is automatically loaded when:
1. `config.tools.enable_zai_search` is `True` in configuration
2. `ANTHROPIC_AUTH_TOKEN` environment variable is set

### Loading Process

1. **Initialization**: Tool checks for API key availability
2. **Registration**: Added to Mini-Agent's tool registry
3. **Availability**: Marked as available if configuration is correct

### Error Handling

- **Missing API Key**: Tool marks as unavailable with helpful error message
- **Network Issues**: Graceful failure with detailed error information
- **API Errors**: Proper error handling with retry guidance

## Technical Details

### API Endpoint
- **Base URL**: `https://api.z.ai/api/anthropic`
- **Model**: GLM-4.6 for comprehensive analysis
- **Timeout**: 60 seconds for search operations

### Credit Management
- **Usage Tracking**: Counts toward coding plan quota
- **Efficiency**: Optimized for coding plan constraints
- **Budget Awareness**: Provides usage tips and recommendations

### Error Scenarios

| Scenario | Behavior | Error Message |
|----------|----------|---------------|
| No API key | Tool unavailable | "Set ANTHROPIC_AUTH_TOKEN environment variable" |
| API error | Graceful failure | "Web search error: [details]" |
| Invalid params | Parameter validation | "max_results must be between 1 and 10" |

## Comparison with Other Z.AI Tools

| Feature | Direct Z.AI API | Anthropic Endpoint |
|---------|----------------|-------------------|
| Credits | Z.AI API credits | Coding plan quota |
| Citations | Manual formatting | Automatic search_result blocks |
| Integration | Separate setup | Claude Code native |
| Quota | Pay-per-use | ~120 prompts/5 hours |
| Error handling | Basic | Advanced with Mini-Agent patterns |

## Testing

Run the test suite to validate functionality:

```bash
python scripts/testing/test_zai_anthropic_web_search.py
```

The test validates:
- ✅ Environment configuration
- ✅ Tool initialization
- ✅ Web search functionality
- ✅ Result formatting
- ✅ Claude search_result block generation

## Next Steps

1. **Configuration**: Ensure `ANTHROPIC_AUTH_TOKEN` is set
2. **Testing**: Run the test script to validate setup
3. **Integration**: Tool loads automatically with Z.AI search enabled
4. **Usage**: Use in Mini-Agent queries for web research with citations

## Troubleshooting

### Common Issues

**Tool Not Available**
- Check that `ANTHROPIC_AUTH_TOKEN` is set
- Verify `ZAI_API_KEY` is configured
- Run the configuration script: `python scripts/setup/configure_anthropic_for_zai.py`

**Search Failures**
- Check network connectivity
- Verify API key permissions
- Review error messages in tool output

**Missing Citations**
- Ensure results contain `search_result` blocks
- Check that `citations.enabled` is `true`
- Verify Claude Code integration setup

---

*This tool enables efficient web search with natural citations using Z.AI's coding plan, providing the best of both worlds: powerful web search capabilities with seamless Claude Code integration.*