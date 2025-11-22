"""MiniMax-M2 Code Z.AI Web Search Tool for natural web citations.

This tool enables MiniMax-M2 to cite Z.AI web search results naturally 
by formatting results as MiniMax-M2's search_result blocks.

🚫 CREDIT PROTECTED - This tool is disabled by default.
"""

import logging
from typing import Any

# CRITICAL: Check credit protection before importing Z.AI dependencies
from ..utils.credit_protection import check_zai_protection

if check_zai_protection():
    # Block module loading if protection is active
    raise ImportError("Z.AI tools disabled for credit protection")

from ..llm.minimax_zai_client import MiniMax-M2ZAIWebSearchClient, get_zai_api_key
from .base import Tool, ToolResult

logger = logging.getLogger(__name__)


class MiniMax-M2ZAIWebSearchTool(Tool):
    """Z.AI web search tool that formats results for MiniMax-M2 natural citations.
    
    This tool uses Z.AI's web search and formats results as MiniMax-M2's 
    search_result blocks, enabling natural source citations like web search.
    """
    
    def __init__(self, api_key: str | None = None):
        """Initialize MiniMax-M2 Z.AI web search tool.
        
        Args:
            api_key: Z.AI API key (if None, loads from ZAI_API_KEY env var)
        """
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            logger.warning("Z.AI API key not found. MiniMax-M2 web search will not be available.")
            self.available = False
            self.client = None
        else:
            try:
                self.client = MiniMax-M2ZAIWebSearchClient(self.api_key)
                self.available = True
                logger.info("MiniMax-M2 Z.AI web search tool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize MiniMax-M2 Z.AI client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "minimax_zai_web_search"

    @property
    def description(self) -> str:
        return (
            "Z.AI web search for MiniMax-M2 Code with natural citations. "
            "Searches the web using Z.AI and formats results as MiniMax-M2's search_result blocks. "
            "MiniMax-M2 can then cite sources naturally like web search results. "
            "Use for: current information, research, fact-checking, recent developments, news. "
            "Endpoint: Coding Plan API (api.z.ai/api/coding/paas/v4) + MiniMax-M2 Code config: api.z.ai/api/anthropic. "
            "Usage quota: ~120 prompts every 5 hours (Coding Plan). "
            "Benefits: Natural citations, web search quality, seamless MiniMax-M2 integration."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query or research question",
                },
                "depth": {
                    "type": "string",
                    "description": "Analysis depth: 'quick' (3 sources), 'comprehensive' (7 sources), 'deep' (10 sources)",
                    "enum": ["quick", "comprehensive", "deep"],
                    "default": "comprehensive",
                },
                "search_engine": {
                    "type": "string",
                    "description": "Search engine type: 'search-prime' (default), 'search_std', 'search_pro', 'search_pro_sogou', 'search_pro_quark'",
                    "enum": ["search-prime", "search_std", "search_pro", "search_pro_sogou", "search_pro_quark"],
                    "default": "search-prime",
                },
                "include_citations": {
                    "type": "boolean",
                    "description": "Whether to enable citations for search results (default: True)",
                    "default": True,
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        depth: str = "comprehensive",
        search_engine: str = "search-prime",
        include_citations: bool = True,
        **kwargs,
    ) -> ToolResult:
        """Execute Z.AI web search for MiniMax-M2 integration.
        
        Args:
            query: Search query
            depth: Analysis depth (quick/comprehensive/deep)
            search_engine: Search engine type
            include_citations: Whether to enable citations
            **kwargs: Additional parameters
            
        Returns:
            ToolResult with search blocks formatted for MiniMax-M2
        """
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="MiniMax-M2 Z.AI web search not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            # Perform research using MiniMax-M2-compatible Z.AI client
            result = await self.client.research_and_analyze_for_minimax(
                query=query,
                depth=depth,
                search_engine=search_engine,
            )

            if result.get("success"):
                search_blocks = result.get("search_blocks", [])
                
                # Format summary for display
                content = f"""**MiniMax-M2 Z.AI Web Search Results**

📊 **Query:** {result['query']}
🔍 **Model:** {result['model']}  
📈 **Depth:** {result['depth']}
📚 **Sources:** {result['source_count']} search result blocks
⏰ **Timestamp:** {result['timestamp']}

---

**Generated MiniMax-M2 Search Result Blocks:**
These results are formatted as MiniMax-M2's search_result blocks and can be cited naturally:

"""

                # Show summary of search results for user
                for i, block in enumerate(search_blocks[:3], 1):  # Show first 3 for preview
                    content += f"""
**Result {i}:** {block.title}
🔗 Source: {block.source}
📝 Content Preview: {block.content[0]['text'][:100]}...
✅ Citations: {"Enabled" if block.citations.get("enabled", False) else "Disabled"}

---
"""
                
                if len(search_blocks) > 3:
                    content += f"\n*... and {len(search_blocks) - 3} more search result blocks*\n"
                
                content += f"""

**MiniMax-M2 Integration Benefits:**
✅ **Natural Citations** - MiniMax-M2 can cite these sources like web search
✅ **Search Result Blocks** - Formatted per MiniMax-M2's search_result schema  
✅ **Usage Efficiency** - ~120 prompts every 5 hours (Coding Plan)
✅ **Web Search Quality** - Same citation format as native web search

**How to Use:**
1. Use this tool to search and get search_result blocks
2. Provide blocks to MiniMax-M2 in tool_result content
3. MiniMax-M2 will automatically cite sources when using information
"""

                return ToolResult(success=True, content=content)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"MiniMax-M2 Z.AI web search failed: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"MiniMax-M2 web search failed: {error_msg}",
                )

        except Exception as e:
            logger.exception("MiniMax-M2 Z.AI web search execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"MiniMax-M2 web search error: {str(e)}",
            )


class MiniMax-M2ZAIRecommendationTool(Tool):
    """Tool that recommends MiniMax-M2 Code integration setup with Z.AI."""
    
    @property
    def name(self) -> str:
        return "minimax_zai_setup_guide"

    @property
    def description(self) -> str:
        return (
            "Provides setup guide for integrating Z.AI with MiniMax-M2 Code. "
            "Explains how to configure MiniMax-M2 Code with Z.AI's Anthropic endpoint "
            "to enable web search with natural citations through Coding Plan."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "description": "Specific section to show: 'setup', 'configuration', 'usage', or 'all'",
                    "enum": ["setup", "configuration", "usage", "all"],
                    "default": "all",
                }
            },
        }

    async def execute(self, section: str = "all", **kwargs) -> ToolResult:
        """Provide MiniMax-M2 Code setup guide for Z.AI integration."""
        
        guide_content = ""
        
        if section in ["setup", "all"]:
            guide_content += """**MiniMax-M2 Code + Z.AI Setup Guide**

### Step 1: Install MiniMax-M2 Code
```bash
npm install -g @anthropic-ai/minimax-code
```

### Step 2: Configure Environment Variables
Set these in your terminal or system environment:

```bash
export ANTHROPIC_AUTH_TOKEN="your_zai_api_key"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export API_TIMEOUT_MS="3000000"
```

### Step 3: Test Integration
```bash
minimax
# Follow prompts to complete setup
```

"""

        if section in ["configuration", "all"]:
            guide_content += """
**Configuration Details**

**API Endpoint:** https://api.z.ai/api/anthropic
**Models Available:** GLM-4.6, GLM-4.5-air
**Usage Quota:** ~120 prompts every 5 hours
**Web Search:** Enabled through search_result blocks

**Environment Variables:**
- `ANTHROPIC_AUTH_TOKEN`: Your Z.AI Coding Plan API key
- `ANTHROPIC_BASE_URL`: Set to https://api.z.ai/api/anthropic
- `API_TIMEOUT_MS`: Recommended: 3000000 (50 minutes)

"""

        if section in ["usage", "all"]:
            guide_content += """
**Usage Pattern**

1. **Web Search with Natural Citations:**
   - Use tools that return search_result blocks
   - MiniMax-M2 cites sources automatically like web search
   - Format: `{type: "search_result", source: "...", title: "..."}`

2. **Optimal Workflow:**
   - Search first for current information
   - Provide search_result blocks to MiniMax-M2
   - Ask follow-up questions with source context

3. **Coding Plan Benefits:**
   - 3× the usage of MiniMax-M2 Pro
   - Web search integration via search_result blocks
   - Natural citation quality matching web search

**Example Integration:**
```python
# Tool returns MiniMax-M2-compatible search_result blocks
search_results = [
    {
        "type": "search_result",
        "source": "https://docs.python.org",
        "title": "Python Best Practices",
        "content": [{"type": "text", "text": "..."}],
        "citations": {"enabled": True}
    }
]
# MiniMax-M2 automatically cites when using this information
```
"""

        return ToolResult(
            success=True,
            content=guide_content,
            metadata={"guide_type": "minimax_zai_setup"}
        )
