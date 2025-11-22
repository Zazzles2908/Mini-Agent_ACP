# Z.AI Web Search with MiniMax-M2 Citations Integration Guide
*Generated: November 20, 2025*

## Overview

This integration provides Z.AI GLM web search results formatted as **MiniMax-M2's search_result blocks** with proper citations, enabling natural source attribution in MiniMax-M2 responses just like MiniMax-M2's native web search.

## Architecture Pattern

```
User Query → MiniMax-M2 (via Anthropic interface) → Z.AI Web Search → Format as search_result blocks → Return to MiniMax-M2 with citations
                ↑
    GLM Coding Plan Setup
    (ANTHROPIC_BASE_URL: https://api.z.ai/api/anthropic)
```

## What This Solution Provides

### **1. Z.AI Web Search Tool with Citations**
- **File**: `mini_agent/tools/zai_web_search_with_citations.py`
- **Function**: Converts Z.AI web search results into MiniMax-M2's search_result format
- **Features**: Proper source attribution, citation formatting, natural integration

### **2. MiniMax-M2 Search Result Blocks Integration**
```json
{
  "type": "search_result",
  "source": "https://example.com/article",
  "title": "Article Title",
  "content": [
    {
      "type": "text",
      "text": "Content of the search result..."
    }
  ],
  "citations": {
    "enabled": true
  }
}
```

## Integration with MiniMax-M2 Code

### **Step 1: Configure GLM Coding Plan**
Set up MiniMax-M2 Code with Z.AI as described in your documentation:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zai_api_key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000"
  }
}
```

### **Step 2: Integrate Web Search Tool**
Add the Z.AI web search tool to your MiniMax-M2 Code setup:

```python
from mini_agent.tools.zai_web_search_with_citations import ZAIWebSearchWithCitationsTool

# Initialize the tool
search_tool = ZAIWebSearchWithCitationsTool()

# Add to MiniMax-M2 Code tools
minimax_tools = [
    # ... existing tools
    search_tool.get_minimax_tool_schema()
]
```

### **Step 3: Use in MiniMax-M2 Interactions**
```python
# When MiniMax-M2 needs web search, it can call the tool
result = await search_tool.execute(
    query="Latest developments in AI regulation",
    depth="comprehensive",
    max_results=5
)

# Result contains MiniMax-M2-formatted search_result blocks
# MiniMax-M2 can now cite these results with proper attribution
```

## Example Usage Scenarios

### **Scenario 1: Research Query**
```
User: "What are the latest developments in AI safety regulation?"
MiniMax-M2: "I'll search for current AI safety regulation developments..."
         [Uses zai_web_search_with_citations tool]
         [Receives search_result blocks with citations]
         [Provides response with proper source attribution]
```

### **Scenario 2: Fact-Checking**
```
User: "Is it true that OpenAI just announced new safety measures?"
MiniMax-M2: "Let me search for recent OpenAI safety announcements..."
         [Searches and receives results with citations]
         [Provides evidence-based answer with source links]
```

### **Scenario 3: Technical Research**
```
User: "How does quantum computing hardware work?"
MiniMax-M2: "I'll search for technical information about quantum computing hardware..."
         [Searches and gets technical results with citations]
         [Explains with proper source attribution]
```

## Technical Implementation

### **Tool Schema for MiniMax-M2**
```python
{
  "name": "zai_web_search_with_citations",
  "description": "Z.AI GLM web search with MiniMax-M2 citation formatting...",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query or research question"
      },
      "depth": {
        "type": "string",
        "enum": ["quick", "comprehensive", "deep"],
        "default": "comprehensive"
      },
      "model": {
        "type": "string",
        "enum": ["auto", "glm-4.6", "glm-4.5"],
        "default": "glm-4.5"
      },
      "max_results": {
        "type": "integer",
        "minimum": 1,
        "maximum": 10,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

### **Search Result Format**
The tool returns results in MiniMax-M2's search_result format:

```json
{
  "type": "tool_result",
  "content": [
    {
      "type": "search_result",
      "source": "https://example.com",
      "title": "Example Article",
      "content": [{"type": "text", "text": "Article content..."}],
      "citations": {"enabled": true}
    }
  ],
  "name": "zai_web_search_with_citations"
}
```

## Integration with Mini-Max Workflow

If you're using Mini-Max as a proxy to MiniMax-M2:

```python
from mini_agent.llm.anthropic_client import AnthropicClient
from mini_agent.tools.zai_web_search_with_citations import ZAIWebSearchWithCitationsTool

# Mini-Max provides MiniMax-M2 access
minimax_client = AnthropicClient(
    api_key="your_minimax_key",
    api_base="https://api.minimaxi.com/anthropic"
)

# Add Z.AI search tool with citations
search_tool = ZAIWebSearchWithCitationsTool()
tools = [search_tool.get_minimax_tool_schema()]

# Now MiniMax-M2 has web search with proper citations!
messages = [
    Message(role="user", content="Search for AI developments and provide citations")
]

response = await minimax_client.generate(messages, tools=tools)
```

## Benefits

### **1. Natural Citations**
- MiniMax-M2 automatically includes citations when using search result information
- Proper source attribution matches MiniMax-M2's native web search behavior
- Users get evidence-based responses with clear source links

### **2. Seamless Integration**
- Works with existing MiniMax-M2 Code setup using GLM Coding Plan
- Maintains conversation flow without separate web search steps
- Follows MiniMax-M2's standard tool calling interface

### **3. Z.AI GLM Advantages**
- Leverages GLM's powerful web search and analysis capabilities
- Uses Coding Plan quota (~120 prompts every 5 hours)
- Cost-effective alternative to separate web search services

### **4. Production Ready**
- Full error handling and fallback mechanisms
- Configurable search depth and result limits
- Compatible with MiniMax-M2's citation system

## Configuration

### **Environment Variables**
```bash
# Z.AI GLM Coding Plan
ZAI_API_KEY=your_zai_coding_plan_api_key

# For MiniMax-M2 integration via Mini-Max
MINIMAX_API_KEY=your_minimax_key

# For MiniMax-M2 Code setup
ANTHROPIC_AUTH_TOKEN=your_zai_api_key
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
```

### **Tool Parameters**
- **query**: Search query (required)
- **depth**: Analysis level (quick/comprehensive/deep)
- **model**: GLM model preference (auto/glm-4.6/glm-4.5)
- **max_results**: Number of results to return (1-10)

## Usage Examples

### **Example 1: Basic Web Search**
```python
search_tool = ZAIWebSearchWithCitationsTool()
result = await search_tool.execute(
    query="Latest AI policy developments",
    depth="comprehensive"
)
# Returns MiniMax-M2-formatted search results with citations
```

### **Example 2: With Custom Parameters**
```python
result = await search_tool.execute(
    query="Quantum computing breakthrough",
    depth="deep",
    model="glm-4.6",
    max_results=3
)
# Returns 3 comprehensive results using GLM-4.6
```

## Next Steps

1. **Test Integration**: Verify the tool works with your Z.AI API key
2. **MiniMax-M2 Tool Registration**: Add the tool schema to your MiniMax-M2 Code setup
3. **Citation Testing**: Test that MiniMax-M2 properly cites search results
4. **Workflow Optimization**: Adjust parameters based on your use cases

---

**This solution provides Z.AI GLM web search with proper MiniMax-M2 citations, following your established integration pattern!**