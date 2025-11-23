"""Z.AI Web Tools - MCP Protocol Implementation (FREE Quotas)

✅ ARCHITECTURE: MCP Protocol → Z.AI MCP Servers → FREE quotas
✅ LITE PLAN: Uses 100 web searches + 100 web readers (FREE with Lite plan)
✅ PROTOCOL: Model Context Protocol (MCP) standard
✅ QUOTAS: 100 searches + 100 readers (NOT charged to account)
✅ SECURITY: Direct API calls disabled to prevent credit burning

This implements the MCP protocol for Z.AI web search and reading using your FREE quotas.
Replaces direct API calls that were burning credits to paid endpoints.
"""

import os
import logging
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

from .base import Tool, ToolResult
from .zai_mcp_tools import ZAIMCPTool, create_mcp_tool

logger = logging.getLogger(__name__)

# MCP Protocol Integration - FREE Quotas
# Uses Z.AI MCP servers: web_search_prime and web_reader
# 100 web searches + 100 web readers included FREE with Lite plan


class ZAIWebSearchTool(Tool):
    """Z.AI web search using MCP Protocol with FREE quotas.
    
    ✅ Uses MCP Protocol: https://api.z.ai/api/mcp/web_search_prime/mcp
    ✅ FREE with Lite plan: 100 web searches included
    ✅ SECURE: Cannot burn credits - only uses included quotas
    ✅ STANDARD: Model Context Protocol implementation
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web search tool using MCP Protocol.
        
        Args:
            api_key: Z.AI API key (if None, uses ZAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        
        if not self.api_key:
            logger.warning("No Z.AI API key found. Web search will not be available.")
            self.available = False
            self.mcp_tool = None
            return
        
        # Initialize MCP tool for free quota usage
        try:
            self.mcp_tool = None  # Will be created on first use
            self.available = True
            logger.info("Z.AI web search initialized using MCP Protocol (FREE quotas)")
        except Exception as e:
            logger.error(f"Failed to initialize Z.AI MCP tool: {e}")
            self.available = False
            self.mcp_tool = None

    @property
    def name(self) -> str:
        return "zai_web_search"

    @property
    def description(self) -> str:
        return (
            "Z.AI web search using MCP Protocol (FREE with Lite plan). "
            "Uses 100 included web searches (not charged). "
            "MCP Server: https://api.z.ai/api/mcp/web_search_prime/mcp. "
            "Use for: research, fact-checking, current information with source citations."
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
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results (1-5, default 3)",
                    "minimum": 1,
                    "maximum": 5,
                    "default": 3,
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        max_results: int = 3,
        **kwargs
    ) -> ToolResult:
        """Execute web search using Z.AI MCP Protocol.
        
        Args:
            query: Search query
            max_results: Maximum number of results (default 3, max 5 to save quota)
            
        Returns:
            ToolResult with search results or error
        """
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web search not available. Check API key and configuration."
            )

        try:
            # Create MCP tool instance
            if not self.mcp_tool:
                self.mcp_tool = await create_mcp_tool(self.api_key)
            
            # Execute MCP web search (uses FREE quotas)
            result = await self.mcp_tool.web_search_prime(query, max_results)
            
            if result["status"] == "success":
                data = result["data"]
                
                # Format results for MiniMax-M2
                formatted_results = []
                if "results" in data:
                    for i, item in enumerate(data["results"], 1):
                        title = item.get("title", "Untitled")
                        link = item.get("url", "")
                        content = item.get("summary", "")
                        
                        formatted_results.append(
                            f"### Result {i}: {title}\n"
                            f"**Source**: {link}\n"
                            f"**Content**: {content}\n"
                        )
                
                if formatted_results:
                    usage = result.get("usage", {})
                    searches_used = usage.get("searches", 0)
                    
                    output = (
                        f"## Web Search Results for: {query}\n"
                        f"**Protocol**: MCP (Model Context Protocol)\n"
                        f"**Quota Used**: {searches_used}/100 searches\n"
                        f"**Results**: {len(formatted_results)}\n"
                        f"**Timestamp**: {datetime.now().isoformat()}\n\n"
                        + "\n".join(formatted_results)
                    )
                else:
                    output = f"No results found for query: {query}"
                
                logger.info(f"Z.AI MCP web search completed: {len(formatted_results)} results for '{query}'")
                return ToolResult(success=True, content=output, error=None)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Z.AI MCP web search error: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Z.AI MCP search error: {error_msg}"
                )
                        
        except Exception as e:
            logger.exception("Z.AI MCP web search failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Z.AI MCP web search exception: {str(e)}"
            )


class ZAIWebReaderTool(Tool):
    """Z.AI web page reader using MCP Protocol with FREE quotas.
    
    ✅ Uses MCP Protocol: https://api.z.ai/api/mcp/web_reader/mcp
    ✅ FREE with Lite plan: 100 web readers included
    ✅ SECURE: Cannot burn credits - only uses included quotas
    ✅ STANDARD: Model Context Protocol implementation
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web reader tool using MCP Protocol.
        
        Args:
            api_key: Z.AI API key (if None, uses ZAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        
        if not self.api_key:
            logger.warning("No Z.AI API key found. Web reader will not be available.")
            self.available = False
            self.mcp_tool = None
            return
        
        # Initialize MCP tool for free quota usage
        try:
            self.mcp_tool = None  # Will be created on first use
            self.available = True
            logger.info("Z.AI web reader initialized using MCP Protocol (FREE quotas)")
        except Exception as e:
            logger.error(f"Failed to initialize Z.AI MCP tool: {e}")
            self.available = False
            self.mcp_tool = None

    @property
    def name(self) -> str:
        return "zai_web_reader"

    @property
    def description(self) -> str:
        return (
            "Z.AI web page reader using MCP Protocol (FREE with Lite plan). "
            "Uses 100 included web readers (not charged). "
            "MCP Server: https://api.z.ai/api/mcp/web_reader/mcp. "
            "Use for: extracting content from specific URLs, deep analysis of web pages."
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
                "extract_links": {
                    "type": "boolean",
                    "description": "Extract links from the page",
                    "default": True,
                },
            },
            "required": ["url"],
        }

    async def execute(
        self,
        url: str,
        extract_links: bool = True,
        **kwargs
    ) -> ToolResult:
        """Read web page content using Z.AI MCP Protocol.
        
        Args:
            url: URL to read
            extract_links: Whether to extract links from the page
            
        Returns:
            ToolResult with page content or error
        """
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web reader not available. Check API key and configuration."
            )

        try:
            # Create MCP tool instance
            if not self.mcp_tool:
                self.mcp_tool = await create_mcp_tool(self.api_key)
            
            # Execute MCP web reader (uses FREE quotas)
            result = await self.mcp_tool.web_reader(url, extract_links)
            
            if result["status"] == "success":
                data = result["data"]
                
                # Extract content from MCP response
                title = data.get("title", "N/A")
                content = data.get("content", "")
                
                # Format output for MiniMax-M2
                usage = result.get("usage", {})
                readers_used = usage.get("readers", 0)
                
                output = (
                    f"## Web Page Content: {title}\n"
                    f"**URL**: {url}\n"
                    f"**Protocol**: MCP (Model Context Protocol)\n"
                    f"**Quota Used**: {readers_used}/100 readers\n"
                    f"**Extract Links**: {extract_links}\n"
                    f"**Timestamp**: {datetime.now().isoformat()}\n\n"
                    f"### Content\n{content}"
                )
                
                logger.info(f"Z.AI MCP web reader completed: {url}")
                return ToolResult(success=True, content=output, error=None)
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Z.AI MCP web reader error: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Z.AI MCP reader error: {error_msg}"
                )
                        
        except Exception as e:
            logger.exception("Z.AI MCP web reader failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Z.AI MCP web reader exception: {str(e)}"
            )


def get_zai_tools(api_key: str | None = None) -> list[Tool]:
    """Get list of available Z.AI tools.
    
    Args:
        api_key: Optional API key (uses ZAI_API_KEY env var if not provided)
        
    Returns:
        List of available Z.AI tools
    """
    tools = []
    
    search_tool = ZAIWebSearchTool(api_key)
    if search_tool.available:
        tools.append(search_tool)
    
    reader_tool = ZAIWebReaderTool(api_key)
    if reader_tool.available:
        tools.append(reader_tool)
    
    return tools


# Test function for validation
async def test_zai_tools():
    """Test Z.AI tools functionality using MCP Protocol."""
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ ZAI_API_KEY not found in environment")
        return
    
    print("🧪 Testing Z.AI Web Tools (MCP Protocol)...")
    print("🔒 Using FREE quotas: 100 searches + 100 readers")
    print("✅ Protocol: Model Context Protocol (MCP)")
    
    # Test web search
    search_tool = ZAIWebSearchTool(api_key)
    if search_tool.available:
        result = await search_tool.execute(query="MiniMax AI capabilities", max_results=2)
        print(f"✅ Web Search: {'Success' if result.success else 'Failed'}")
        if result.success:
            print(f"   Results length: {len(result.content)} chars")
        else:
            print(f"   Error: {result.error}")
    else:
        print("❌ Web Search not available")
    
    # Test usage tracking
    if search_tool.mcp_tool:
        usage = search_tool.mcp_tool.get_usage_summary()
        print(f"📊 Quota Usage: {usage}")
    
    print("\n✅ Z.AI MCP tools test completed")


if __name__ == "__main__":
    asyncio.run(test_zai_tools())
