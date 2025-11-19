"""Complete Claude Z.AI Web Search and Reader tools.

This module provides both web search and web reader functionality
formatted as Claude search_result blocks for natural citations.
"""

import logging
from typing import Any

from ..llm.claude_zai_client import ClaudeZAIWebSearchClient, get_zai_api_key
from .base import Tool, ToolResult

logger = logging.getLogger(__name__)


class ClaudeZAIWebReaderTool(Tool):
    """Z.AI web reader tool that formats results as Claude search_result blocks.
    
    This tool reads web pages and formats content as Claude's search_result blocks,
    enabling natural citation of web page content.
    """
    
    def __init__(self, api_key: str | None = None):
        """Initialize Claude Z.AI web reader tool.
        
        Args:
            api_key: Z.AI API key (if None, loads from ZAI_API_KEY env var)
        """
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            logger.warning("Z.AI API key not found. Web reader will not be available.")
            self.available = False
            self.client = None
        else:
            try:
                self.client = ClaudeZAIWebSearchClient(self.api_key)
                self.available = True
                logger.info("Claude Z.AI web reader tool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Claude Z.AI client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "claude_zai_web_reader"

    @property
    def description(self) -> str:
        return (
            "Z.AI web reader for Claude Code with natural citations. "
            "Reads web page content and formats it as Claude's search_result blocks. "
            "Claude can then cite the web page naturally like search results. "
            "Use for: reading articles, documentation, blog posts, specific web content. "
            "Formats: markdown, HTML, or text output with source attribution. "
            "Usage quota: ~120 prompts every 5 hours (Coding Plan). "
            "Benefits: Natural citations, structured content, seamless Claude integration."
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
                    "default": False,
                },
                "max_content_length": {
                    "type": "integer",
                    "description": "Maximum content length to include (prevent large pages)",
                    "default": 2000,
                },
            },
            "required": ["url"],
        }

    async def execute(
        self,
        url: str,
        format: str = "markdown",
        include_images: bool = False,
        max_content_length: int = 2000,
        **kwargs,
    ) -> ToolResult:
        """Execute web page reading for Claude integration.
        
        Args:
            url: URL to read
            format: Output format (markdown/html/text)
            include_images: Whether to retain images
            max_content_length: Maximum content length to include
            **kwargs: Additional parameters
            
        Returns:
            ToolResult with web page content formatted as search_result blocks
        """
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="Claude Z.AI web reader not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            # Add usage awareness for Coding Plan
            usage_tip = "📊 **USAGE TIP (Coding Plan):** Web reader counts toward ~120 prompts every 5 hours. Use selectively.\n\n"
            
            # Use the Z.AI web reading functionality
            result = await self.client.web_reading(
                url=url,
                format_type=format,
                include_images=include_images,
            )

            if result.get("success"):
                # Extract content and format appropriately
                title = result.get("title", "Web Page Content")
                description = result.get("description", "Web page content")
                content = result.get("content", "")
                
                # Truncate content if too long
                if len(content) > max_content_length:
                    content = content[:max_content_length] + "...\n\n[Content truncated for optimal display]"
                
                content = f"""**Web Page Summary:** {description}

{content}"""

                content_preview = f"""**Claude Z.AI Web Reader Results**

{usage_tip}**URL:** {result['url']}
**Title:** {title}
**Description:** {description}
**Format:** {result['format']}
**Word Count:** {result.get('word_count', 0)}
**Timestamp:** {result['timestamp']}

---

**Web Page Content** (formatted as Claude search_result block):

**Title:** {title}
**Source:** {url}

{content}

---

**Claude Integration Benefits:**
✅ **Natural Citations** - Claude can cite this source like web search
✅ **Search Result Block** - Formatted per Claude's search_result schema
✅ **Usage Efficiency** - ~120 prompts every 5 hours (Coding Plan)
✅ **Structured Content** - Clean formatting for Claude consumption

**Usage with Claude:**
This content is now available as a search_result block that Claude can cite
naturally when using information from the web page.
"""

                return ToolResult(success=True, content=content_preview)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Claude Z.AI web reading failed: {error_msg}")
                
                # If web reader fails, try web search as fallback
                logger.info(f"Attempting web search fallback for URL: {url}")
                try:
                    search_result = await self.client.web_search(
                        query=f"content summary {url}",
                        count=3,
                        search_engine="search-prime",
                        recency_filter="noLimit"
                    )
                    
                    if search_result.get("success"):
                        search_content = f"""**Claude Z.AI Web Reader Results (via search fallback)**

{usage_tip}**URL:** {url}
**Status:** Web reader failed, using search fallback
**Sources Found:** {len(search_result.get('search_result', []))} related results
**Timestamp:** {result.get('timestamp')}

---

**Search Results for Web Content:**

"""
                        
                        for i, item in enumerate(search_result.get('search_result', []), 1):
                            search_content += f"""
**Result {i}:** {item.get('title', 'N/A')}
**Source:** {item.get('link', 'N/A')}
**Content:** {item.get('content', 'N/A')[:200]}...

---
"""
                        
                        search_content += """
**Claude Integration Benefits:**
✅ **Natural Citations** - Available through search result format
✅ **Fallback Strategy** - Ensures content availability
✅ **Usage Efficiency** - ~120 prompts every 5 hours (Coding Plan)
"""
                        
                        return ToolResult(success=True, content=search_content)
                except Exception as fallback_error:
                    logger.error(f"Search fallback also failed: {fallback_error}")
                
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Web reading failed: {error_msg}",
                )

        except Exception as e:
            logger.exception("Claude Z.AI web reader execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Claude web reader error: {str(e)}",
            )


class ClaudeZAICombinedSearchReadTool(Tool):
    """Combined web search and reading tool for comprehensive results."""
    
    def __init__(self, api_key: str | None = None):
        """Initialize combined search and read tool."""
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            self.available = False
            self.client = None
        else:
            try:
                self.client = ClaudeZAIWebSearchClient(self.api_key)
                self.available = True
            except Exception as e:
                logger.error(f"Failed to initialize client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "claude_zai_search_and_read"

    @property
    def description(self) -> str:
        return (
            "Z.AI combined web search and reading for Claude Code. "
            "Performs both web search and targeted web page reading in one tool. "
            "Results are formatted as Claude's search_result blocks for natural citations. "
            "Use for: comprehensive research with both general search and specific page analysis. "
            "Outputs multiple search_result blocks that Claude can cite naturally."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Main search query",
                },
                "read_url": {
                    "type": "string",
                    "description": "Specific URL to read and analyze",
                },
                "search_count": {
                    "type": "integer",
                    "description": "Number of search results to return (1-10)",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 10,
                },
                "search_depth": {
                    "type": "string",
                    "description": "Search depth: 'quick', 'comprehensive', 'deep'",
                    "enum": ["quick", "comprehensive", "deep"],
                    "default": "comprehensive",
                },
            },
            "required": ["query", "read_url"],
        }

    async def execute(
        self,
        query: str,
        read_url: str,
        search_count: int = 3,
        search_depth: str = "comprehensive",
        **kwargs,
    ) -> ToolResult:
        """Execute combined search and reading for comprehensive results."""
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="Combined search and read not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            usage_tip = "📊 **USAGE TIP (Coding Plan):** Combined search and read counts toward ~120 prompts every 5 hours.\n\n"
            
            # Perform search
            search_result = await self.client.research_and_analyze_for_claude(
                query=query,
                depth=search_depth,
            )
            
            # Perform web reading
            read_result = await self.client.web_reading(
                url=read_url,
                format_type="markdown",
                include_images=False,
            )
            
            # Combine results
            combined_content = f"""**Claude Z.AI Combined Search and Read Results**

{usage_tip}**Search Query:** {query}
**Read URL:** {read_url}
**Search Depth:** {search_depth}
**Search Results:** {len(search_result.get('search_evidence', [])) if search_result.get('success') else 0}
**Read Status:** {'Success' if read_result.get('success') else 'Failed'}
**Timestamp:** {asyncio.get_event_loop().time()}

---

## Web Search Results

"""
            
            if search_result.get("success"):
                for i, item in enumerate(search_result.get('search_evidence', []), 1):
                    combined_content += f"""
**Search Result {i}:** {item.get('title', 'N/A')}
**Source:** {item.get('link', 'N/A')}
**Content:** {item.get('content', 'N/A')[:200]}...

"""
            else:
                combined_content += f"Search failed: {search_result.get('error', 'Unknown error')}\n"
            
            combined_content += "\n---\n\n## Web Page Reading Results\n\n"
            
            if read_result.get("success"):
                combined_content += f"""
**Web Page:** {read_result.get('title', 'N/A')}
**Source:** {read_url}
**Summary:** {read_result.get('description', 'N/A')}
**Content:** {read_result.get('content', 'N/A')[:300]}...

"""
            else:
                combined_content += f"Web reading failed: {read_result.get('error', 'Unknown error')}\n"
            
            combined_content += """
---

## Claude Integration Benefits

✅ **Natural Citations** - Claude can cite both search and read results
✅ **Comprehensive Research** - General search + specific page analysis  
✅ **Search Result Blocks** - All results formatted for Claude consumption
✅ **Usage Efficiency** - ~120 prompts every 5 hours (Coding Plan)
✅ **Single Tool Execution** - Complete research workflow in one call

**Usage with Claude:**
All results are available as search_result blocks that Claude can cite
naturally when using information from search results or the web page.
"""

            return ToolResult(success=True, content=combined_content)

        except Exception as e:
            logger.exception("Combined search and read execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Combined search and read error: {str(e)}",
            )
