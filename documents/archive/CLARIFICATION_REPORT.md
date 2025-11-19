# Mini-Agent Clarification Report

**Date:** November 19, 2025  
**Re-investigation based on:** User clarification about GLM search and ACP system

---

## 🔍 Corrected Understanding

### 1. Native Web Search Capability (GLM/Z.AI Integration)

**User Clarification:** Mini-Agent should be using **native GLM search functionality** through Z.AI SDK, NOT external MCP servers for web search.

#### Current Status

**✅ Integration EXISTS:**
- `optimized_zai.py` - Full Z.AI client with GLM web search
- `.observability/native_glm_integration.py` - Native GLM client implementation
- `.observability/test_native_glm.py` - Test suite for GLM integration

**❌ NOT INTEGRATED into main Mini-Agent:**
The GLM search capabilities are in separate files but NOT wired into the main agent runtime:
- `mini_agent/llm/` - Only has Anthropic and OpenAI clients
- `mini_agent/cli.py` - Doesn't load GLM/Z.AI tools
- `mini_agent/config/mcp.json` - Has external `minimax_search` MCP (which is failing)

#### What Should Happen

Your native web searching should use the **GLM models' built-in web search capability**:

```python
# From optimized_zai.py - THIS EXISTS BUT ISN'T USED
async def web_search_in_chat(self, query: str, model_name: str = "glm-4.6"):
    """Web search integrated with GLM chat for enhanced results"""
    
    search_params = {
        "enable": "True",
        "search_engine": "search-prime",  # Z.AI's optimized engine
        "search_result": "True",
        "search_prompt": f"Provide comprehensive analysis for: {query}",
        "count": "5"
    }
    
    # Uses GLM's native web search tool
    chat_payload = {
        "model": model_name,
        "messages": messages,
        "tools": [{
            "type": "web_search",
            "web_search": search_params
        }],
        "stream": False
    }
```

#### The Real Issue

**The `minimax_search` MCP server is WRONG:**
- Mini-Agent doesn't need an external MCP server for search
- It should use the **native GLM web search tool** built into GLM 4.5+ models
- The failing MCP connection is actually a non-issue if native search is used

---

### 2. ACP (Agent Client Protocol) System

**User Clarification:** ACP is a **custom part of the Mini-Agent repo**, not a third-party system.

#### What ACP Is

ACP is Mini-Agent's **integration layer for Zed Editor** and Claude Desktop:

```
mini_agent/acp/
├── __init__.py        # Main ACP server implementation
└── server.py          # Entry point for mini-agent-acp command
```

**Purpose:**
- Exposes Mini-Agent as an ACP-compatible server
- Allows Zed Editor and Claude Desktop to use Mini-Agent
- Provides stdio-based communication protocol
- Handles session management, tool execution, and streaming responses

#### How ACP Works

1. **Zed/Claude Desktop starts the ACP server:**
   ```bash
   mini-agent-acp  # Defined in pyproject.toml
   ```

2. **ACP Server (mini_agent/acp/__init__.py):**
   - Creates `MiniMaxACPAgent` instance
   - Wraps the existing `Agent` class
   - Translates ACP protocol ↔ Mini-Agent internal format
   - Manages multiple sessions

3. **Client sends requests via stdio**
4. **ACP server executes tools and returns results**

#### The File Access Issue

Looking at `mini_agent/acp/__init__.py` line 97-101:

```python
async def newSession(self, params: NewSessionRequest) -> NewSessionResponse:
    session_id = f"sess-{len(self._sessions)}-{uuid4().hex[:8]}"
    workspace = Path(params.cwd or self._config.agent.workspace_dir).expanduser()
    if not workspace.is_absolute():
        workspace = workspace.resolve()
    tools = list(self._base_tools)
    add_workspace_tools(tools, self._config, workspace)
```

**The workspace is determined by:**
1. `params.cwd` - Current working directory from the ACP client request
2. Fallback: `config.agent.workspace_dir` (default: `./workspace`)

**The `C:\tmp` restriction comes from:**
- The filesystem MCP server configured in Claude Desktop
- NOT from Mini-Agent's ACP server itself!

**Correction:** My previous fix script was targeting the wrong thing. The issue is:
1. Claude Desktop has a `filesystem` MCP server restricted to `/tmp`
2. Mini-Agent's ACP server doesn't impose directory restrictions
3. But when file operations go through the `filesystem` MCP server, they're restricted

---

## 🔧 Correct Solutions

### Solution 1: Integrate Native GLM Web Search

**Priority: HIGH** - This is what you want working!

#### Step 1: Create GLM Web Search Tool

Create: `mini_agent/tools/glm_search_tool.py`

```python
"""GLM Native Web Search Tool"""
from typing import Any
from .base import Tool, ToolResult

class GLMWebSearchTool(Tool):
    """Native GLM web search using Z.AI SDK"""
    
    def __init__(self, zai_api_key: str):
        self.zai_api_key = zai_api_key
        # Import here to avoid dependency if not used
        try:
            from optimized_zai import OptimizedZAIClient
            self.zai_client = OptimizedZAIClient(zai_api_key)
            self.available = True
        except ImportError:
            self.available = False
    
    @property
    def name(self) -> str:
        return "glm_web_search"
    
    @property
    def description(self) -> str:
        return (
            "Native GLM web search using Z.AI's Search Prime engine. "
            "Use this for web research, current information, and real-time data. "
            "Supports advanced filtering, recency filters, and intelligent analysis."
        )
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of results (default: 5)",
                    "default": 5
                },
                "recency": {
                    "type": "string",
                    "description": "Time filter: oneDay, oneWeek, oneMonth, oneYear, noLimit",
                    "default": "noLimit"
                },
                "depth": {
                    "type": "string",
                    "description": "Analysis depth: quick, comprehensive, deep",
                    "default": "comprehensive"
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, count: int = 5, recency: str = "noLimit", depth: str = "comprehensive") -> ToolResult:
        """Execute GLM web search"""
        
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="GLM web search not available. Install: pip install zai-sdk"
            )
        
        try:
            # Use research_and_analyze for comprehensive results
            result = await self.zai_client.research_and_analyze(
                query=query,
                depth=depth,
                model_preference="auto"
            )
            
            if result.get("success"):
                content = f"""**GLM Web Search Results**

**Query:** {result['query']}
**Model Used:** {result['model_used']} ({result['model_description']})
**Analysis Depth:** {result['depth']}

**Analysis:**
{result['analysis']}

**Token Usage:**
- Prompt: {result['token_usage'].get('prompt_tokens', 'N/A')}
- Completion: {result['token_usage'].get('completion_tokens', 'N/A')}
- Total: {result['token_usage'].get('total_tokens', 'N/A')}
"""
                return ToolResult(success=True, content=content)
            else:
                return ToolResult(success=False, content="", error=result.get("error", "Unknown error"))
                
        except Exception as e:
            return ToolResult(success=False, content="", error=f"GLM search failed: {str(e)}")
```

#### Step 2: Register GLM Tool in CLI

Edit `mini_agent/cli.py`, add to `initialize_base_tools()`:

```python
# Add after bash tools, before Skills section:

# GLM Native Web Search
if config.tools.enable_glm_search:  # Add this config option
    try:
        # Get Z.AI API key from config or environment
        zai_api_key = config.llm.api_key  # Or separate key if needed
        
        from mini_agent.tools.glm_search_tool import GLMWebSearchTool
        glm_search_tool = GLMWebSearchTool(zai_api_key)
        
        if glm_search_tool.available:
            tools.append(glm_search_tool)
            print(f"{Colors.GREEN}✅ Loaded GLM Native Web Search tool{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️  GLM Web Search unavailable (zai-sdk not installed){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Failed to load GLM Web Search: {e}{Colors.RESET}")
```

#### Step 3: Update Configuration

Add to `mini_agent/config/config.yaml`:

```yaml
tools:
  enable_file_tools: true
  enable_bash: true
  enable_note: true
  enable_glm_search: true  # ← ADD THIS
  enable_skills: true
  skills_dir: "./skills"
  enable_mcp: true
  mcp_config_path: "mcp.json"
```

And add to the ToolsConfig in `mini_agent/config.py`:

```python
class ToolsConfig(BaseModel):
    """Tools configuration"""
    # Basic tools
    enable_file_tools: bool = True
    enable_bash: bool = True
    enable_note: bool = True
    enable_glm_search: bool = True  # ← ADD THIS
    
    # Skills
    enable_skills: bool = True
    skills_dir: str = "./skills"
    
    # MCP tools
    enable_mcp: bool = True
    mcp_config_path: str = "mcp.json"
```

#### Step 4: Disable the Failing MCP Server

Since you have native GLM search, disable the external `minimax_search` MCP:

Edit `mini_agent/config/mcp.json`:

```json
{
  "mcpServers": {
    "minimax_search": {
      "description": "DEPRECATED - Use native GLM web search instead",
      "disabled": true  // ← Set to true
    }
  }
}
```

---

### Solution 2: Fix File Access (Corrected Understanding)

The file access restriction comes from the **filesystem MCP server**, not the ACP server.

#### Option A: Expand Filesystem MCP Server Directories

Edit Claude Desktop config: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Project",
        "C:/Users/Jazeel-Home",  // ← Already there
        "C:/Project/ADP",
        "C:/tmp"  // ← Add if not there
      ]
    }
  }
}
```

#### Option B: Remove Filesystem MCP (Use Native File Tools)

Mini-Agent already has native file tools (`ReadTool`, `WriteTool`, `EditTool`) that work with the workspace directory. The filesystem MCP might be redundant!

**Test:** Disable the filesystem MCP and see if file operations still work through Mini-Agent's native tools.

---

## 📋 Implementation Checklist

### Phase 1: Native GLM Web Search (HIGH PRIORITY)

- [ ] Create `mini_agent/tools/glm_search_tool.py`
- [ ] Update `mini_agent/cli.py` to load GLM search tool
- [ ] Update `mini_agent/config.py` with `enable_glm_search` field
- [ ] Update `mini_agent/config/config.yaml` to enable GLM search
- [ ] Disable `minimax_search` MCP server in `mcp.json`
- [ ] Test GLM web search functionality
- [ ] Verify Z.AI API key is configured

### Phase 2: File Access (LOWER PRIORITY)

- [ ] Understand if filesystem MCP is actually needed
- [ ] Test file operations with only native file tools
- [ ] If filesystem MCP is needed, expand allowed directories
- [ ] Document which tool handles which file operations

### Phase 3: Documentation

- [ ] Update README with GLM web search capabilities
- [ ] Document the distinction between:
  - Native Mini-Agent file tools (workspace-based)
  - Filesystem MCP server (restricted directories)
  - GLM native web search (built-in to GLM models)
  - External MCP search servers (not needed)
- [ ] Create usage examples for GLM web search

---

## 🎯 Expected Results

### After Implementing Native GLM Search:

**When you ask for web search:**
```
User: "Search for the latest AI developments in 2024"

Agent: 🔧 glm_web_search(query="latest AI developments 2024", depth="comprehensive")

✅ **GLM Web Search Results**

**Query:** latest AI developments 2024
**Model Used:** glm-4.6 (Flagship model for reasoning and coding)
**Analysis Depth:** comprehensive

**Analysis:**
Based on recent web search results from Z.AI's Search Prime engine:

1. **Multi-modal AI Advances** - GPT-4V and similar models...
2. **Agent Frameworks** - LangChain, AutoGPT developments...
3. **Hardware Acceleration** - New AI chips from NVIDIA...

[Detailed analysis with sources and citations]

**Token Usage:**
- Prompt: 245
- Completion: 892
- Total: 1137
```

### Benefits:

✅ **Native integration** - No external dependencies failing
✅ **Better results** - GLM models optimized for web search
✅ **Faster responses** - Direct API calls, no MCP overhead
✅ **Intelligent analysis** - GLM 4.6 can reason about search results
✅ **Cost effective** - Single API call vs multiple MCP calls

---

## 🚫 What NOT to Do

❌ **Don't** try to fix the `minimax_search` MCP server - it's not needed
❌ **Don't** add more external search MCP servers - use native GLM
❌ **Don't** modify ACP server for file access - it's not the issue
❌ **Don't** use the previous fix scripts I created - they targeted wrong issues

---

## ✅ What TO Do

✅ **DO** integrate the native GLM web search tool
✅ **DO** use Z.AI's Search Prime engine through GLM models
✅ **DO** leverage the existing `optimized_zai.py` code
✅ **DO** configure Z.AI API key in Mini-Agent config
✅ **DO** test with GLM 4.5+ models for web search capability

---

## 📞 Questions to Verify

Before implementing, please confirm:

1. **Z.AI API Key:** Do you have a Z.AI API key configured?
2. **GLM Models:** Are you using GLM 4.5+ models (which have native web search)?
3. **Current Provider:** Is Mini-Agent configured to use Z.AI/GLM or Anthropic/OpenAI?
4. **File Access:** Are you actually experiencing file access issues, or was that a misunderstanding?

---

## 🎓 Key Learnings

1. **Native capabilities > External MCP servers**
   - GLM models have built-in web search
   - Don't add external search when native exists

2. **ACP is Mini-Agent's protocol, not a third-party system**
   - It's the bridge to Zed/Claude Desktop
   - File restrictions come from Claude Desktop's MCP config, not ACP

3. **Understand the architecture before fixing**
   - My initial investigation was based on incorrect assumptions
   - The real issues were different from what they appeared

---

**Next Step:** Should I proceed with creating the GLM native web search tool integration?
