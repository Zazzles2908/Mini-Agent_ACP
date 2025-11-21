"""Z.AI Coding Plan web search and reading tools.

Provides access to Z.AI's Coding Plan functionality.
Includes usage quota management and efficiency optimization.

🚫 CREDIT PROTECTED - Z.AI tools are disabled by default to prevent credit consumption.
"""

import logging
from typing import Any

from ..llm.zai_client import ZAIClient, get_zai_api_key
from ..utils.credit_protection import block_zai_usage, check_zai_protection
from .base import Tool, ToolResult

logger = logging.getLogger(__name__)


class ZAIWebSearchTool(Tool):
    """Native GLM web search using Z.AI's Search Prime engine.
    
    This tool uses GLM models' built-in web search capability to find
    and analyze information from the web. Results include both raw
    search data and AI-powered analysis.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web search tool.
        
        Args:
            api_key: Z.AI API key (if None, loads from ZAI_API_KEY env var)
        """
        # CRITICAL: Check credit protection before any Z.AI operations
        if check_zai_protection():
            block_zai_usage("ZAIWebSearchTool")
        
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            logger.warning("Z.AI API key not found. Web search will not be available.")
            self.available = False
            self.client = None
        else:
            try:
                self.client = ZAIClient(self.api_key)
                self.available = True
                logger.info("Z.AI web search tool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Z.AI client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "zai_web_search"

    @property
    def description(self) -> str:
        return (
            "Z.AI Coding Plan web search using Search Prime engine. "
            "Searches the web and provides AI-powered analysis of results. "
            "Use for: current information, research, fact-checking, recent developments, news. "
            "Usage quota: ~120 prompts every 5 hours (included in Coding Plan). "
            "Supports time-based filtering and domain restrictions. "
            "Efficient for information gathering before expensive GLM calls."
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
                "model": {
                    "type": "string",
                    "description": "GLM model to use: 'glm-4.6' (best comprehensive), 'glm-4.5' (tool invocation optimized), or 'auto' (automatic selection)",
                    "enum": ["auto", "glm-4.6", "glm-4.5"],
                    "default": "glm-4.5",
                },
                "search_engine": {
                    "type": "string",
                    "description": "Search engine type: 'search-prime' (default), 'search_std' (standard), 'search_pro' (professional), 'search_pro_sogou', 'search_pro_quark'",
                    "enum": ["search-prime", "search_std", "search_pro", "search_pro_sogou", "search_pro_quark"],
                    "default": "search-prime",
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        depth: str = "comprehensive",
        model: str = "auto",
        **kwargs,
    ) -> ToolResult:
        """Execute Z.AI web search with analysis.
        
        Args:
            query: Search query
            depth: Analysis depth (quick/comprehensive/deep)
            **kwargs: Additional parameters including search_engine
            
        Returns:
            ToolResult with search results and analysis
        """
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web search not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            # Extract search_engine from kwargs (if provided)
            search_engine = kwargs.get("search_engine", "search-prime")
            
            # Add usage awareness based on parameters
            usage_tip = ""
            if depth == "deep":
                usage_tip = "⚠️ **USAGE TIP (Coding Plan):** Deep searches use more quota. Consider 'comprehensive' for efficiency.\n\n"
            elif depth == "comprehensive" and kwargs.get("search_engine") in ["search_pro", "search_pro_sogou", "search_pro_quark"]:
                usage_tip = "💡 **EFFICIENCY TIP (Coding Plan):** Professional search engines use more quota. Use 'search-prime' for standard queries.\n\n"
            
            # Perform research with analysis using GLM models
            result = await self.client.research_and_analyze(
                query=query,
                depth=depth,
                model_preference=model,
            )

            if result.get("success"):
                content = f"""**Z.AI Web Search Results**

{usage_tip}**Query:** {result['query']}
**Model:** {result['model_used']} ({result['model_description']})
**Analysis Depth:** {result['depth']}
**Timestamp:** {result['timestamp']}

---

**Analysis:**

{result['analysis']}

---

**Note:** Direct search API does not report token usage metrics.
**Sources:** {len(result.get('search_evidence', []))} web sources analyzed
**Quota Usage:** Counts toward ~120 prompts every 5 hours limit
"""
                return ToolResult(success=True, content=content)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Z.AI web search failed: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Web search failed: {error_msg}",
                )

        except Exception as e:
            logger.exception("Z.AI web search execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Web search error: {str(e)}",
            )


class ZAIWebReaderTool(Tool):
    """Z.AI web page reader with intelligent content extraction.
    
    Reads and extracts content from web pages with smart cleaning,
    formatting, and metadata extraction.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web reader tool.
        
        Args:
            api_key: Z.AI API key (if None, loads from ZAI_API_KEY env var)
        """
        # CRITICAL: Check credit protection before any Z.AI operations
        if check_zai_protection():
            block_zai_usage("ZAIWebReaderTool")
        
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            logger.warning("Z.AI API key not found. Web reader will not be available.")
            self.available = False
            self.client = None
        else:
            try:
                self.client = ZAIClient(self.api_key)
                self.available = True
                logger.info("Z.AI web reader tool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Z.AI client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "zai_web_reader"

    @property
    def description(self) -> str:
        return (
            "Z.AI Coding Plan web page reader with intelligent content extraction. "
            "Reads and extracts content from web pages with smart cleaning and formatting. "
            "Use this to read articles, documentation, blog posts, or specific web content. "
            "Supports markdown, HTML, and text output formats with metadata extraction. "
            "Usage quota: Counts toward ~120 prompts every 5 hours limit."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the web page to read",
                },
                "format": {
                    "type": "string",
                    "description": "Output format: 'markdown', 'html', or 'text'",
                    "enum": ["markdown", "html", "text"],
                    "default": "markdown",
                },
                "include_images": {
                    "type": "boolean",
                    "description": "Whether to retain images in the output",
                    "default": True,
                },
            },
            "required": ["url"],
        }

    async def execute(
        self,
        url: str,
        format: str = "markdown",
        include_images: bool = True,
    ) -> ToolResult:
        """Execute web page reading.
        
        Args:
            url: URL to read
            format: Output format (markdown/html/text)
            include_images: Whether to retain images
            
        Returns:
            ToolResult with extracted content
        """
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web reader not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            # Add usage awareness for Coding Plan
            usage_tip = "📊 **USAGE TIP (Coding Plan):** Web reader counts toward ~120 prompts every 5 hours. Use selectively.\n\n"
            
            result = await self.client.web_reading(
                url=url,
                format_type=format,
                include_images=include_images,
            )

            if result.get("success"):
                content = f"""**Z.AI Web Reader Results**

{usage_tip}**URL:** {result['url']}
**Title:** {result.get('title', 'N/A')}
**Description:** {result.get('description', 'N/A')}
**Format:** {result['format']}
**Word Count:** {result['word_count']}
**Timestamp:** {result['timestamp']}

---

**Content:**

{result['content']}

---

**Quota Usage:** Counts toward Coding Plan ~120 prompts every 5 hours limit
"""
                return ToolResult(success=True, content=content)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Z.AI web reading failed: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Web reading failed: {error_msg}",
                )

        except Exception as e:
            logger.exception("Z.AI web reader execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Web reader error: {str(e)}",
            )
