# Why You Only See Snippets - Full Web Search vs Web Reading Explained

## 🔍 **What Just Happened**

### Search Results (What you saw)
The web search returned **snippets** like:
```
"Claude Code · Step 1: Installing the Claude Code · Step 2: Config GLM Coding Plan · Step 3: Start with Claude Code"
```

### Web Reading Results (What I tested)
The web reading tried to get full content but encountered errors:
```
❌ Web reading error 400: Unknown Model, please check the model code
```

---

## 📊 **Two Different APIs, Two Different Purposes**

### 1. 🔍 **Web Search API** (Working Perfectly)
- **Purpose**: Find relevant pages and get brief descriptions
- **Response**: Snippets/meta descriptions (~50-200 characters)
- **Use Case**: "Find me pages about topic X"
- **Status**: ✅ **FULLY WORKING**

**Example Output**:
```json
{
  "title": "Claude Code - Z.AI DEVELOPER DOCUMENT",
  "content": "Claude Code · Step 1: Installing the Claude Code · Step 2: Config GLM Coding Plan...",
  "link": "https://docs.z.ai/devpack/tool/claude"
}
```

### 2. 📖 **Web Reading API** (Has Issues)
- **Purpose**: Read full page content from specific URLs
- **Response**: Complete page content in Markdown/text/HTML
- **Use Case**: "Get the full content of this specific page"
- **Status**: ❌ **API Configuration Issue**

---

## 🛠️ **What This Means for Our Implementation**

### ✅ **What Works Perfectly**:
1. **Finding Pages**: Search API finds relevant documentation
2. **Claude Citations**: Search result blocks enable natural source citations
3. **Research Workflow**: Can search comprehensively and get multiple sources

### ❌ **What Has Issues**:
1. **Full Page Reading**: Web reading API has model configuration problems
2. **Content Extraction**: Can't get the full detailed documentation

### 💡 **The Solution Strategy**:
1. **Use search** to find the right pages ✅
2. **Use search depth** to get more comprehensive snippets ✅
3. **Cite the found pages** with natural citations ✅
4. **For full content**: May need to visit pages directly or use different reading approach

---

## 🎯 **Current Implementation Status**

### ✅ **Web Search Tool**: Production Ready
- **Function**: `claude_zai_web_search`
- **Capability**: Find relevant pages with Claude-compatible citations
- **Quality**: Real API calls, real results, proper formatting

### ⚠️ **Web Reading Tool**: Needs API Fix
- **Function**: `claude_zai_web_reader`
- **Issue**: "Unknown Model" error suggests API endpoint/model mismatch
- **Impact**: Can't extract full page content automatically

---

## 📈 **How to Get Better Information Now**

### For Research Tasks:
```python
# Use comprehensive depth for more snippets
result = await tool.execute(
    query="Z.AI DevPack Claude setup",
    depth="comprehensive",  # Gets 7 sources instead of 3
    search_engine="search-prime"
)
```

### For Detailed Analysis:
1. **Use web search** to find the right pages
2. **Reference the URLs** in your analysis  
3. **Visit pages manually** if you need full content
4. **Cite sources** using the provided search_result blocks

---

## 🔧 **API Technical Details**

### Web Search API (Working):
```
POST https://api.z.ai/api/coding/paas/v4/web_search
{
  "search_engine": "search-prime",
  "search_query": "your query",
  "count": 10
}
```

### Web Reading API (Has Issues):
```
POST https://api.z.ai/api/coding/paas/v4/reader
{
  "url": "https://docs.z.ai/devpack/tool/claude",
  "return_format": "markdown"
}
# Error: Unknown Model (code 1211)
```

---

## 🎯 **Bottom Line**

**The Z.AI web search IS working perfectly** for its intended purpose:

1. ✅ **Finds relevant pages** - Real search results from Z.AI
2. ✅ **Provides snippets** - Enough info to understand page relevance  
3. ✅ **Enables citations** - Claude can cite sources naturally
4. ✅ **Supports research** - Comprehensive depth options

**The web reading has a separate API issue** that's unrelated to the search implementation quality.

**For most use cases**, the search with comprehensive depth gives you enough information to work with, plus proper source citations for Claude.