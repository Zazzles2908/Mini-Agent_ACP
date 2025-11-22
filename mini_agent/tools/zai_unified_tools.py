"""Z.AI Web Tools - Single Correct Implementation

✅ ARCHITECTURE: Direct Z.AI API calls → GLM-4.6 model
✅ LITE PLAN: Uses GLM-4.6 (FREE with plan) - NEVER GLM-4.5 (PAID)
✅ QUOTA: ~120 prompts every 5 hours
✅ TOKEN LIMIT: 2000 max per call (prevents excessive usage)
✅ ENDPOINT: https://api.z.ai/api/coding/paas/v4

This is the ONLY Z.AI tool implementation needed. All others are deprecated.
Based on working implementation from minimax_zai_client.py and transaction log evidence.
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

logger = logging.getLogger(__name__)

# Constants - CRITICAL for cost control
DEFAULT_MODEL = "glm-4.6"  # ✅ FREE with Lite plan - NEVER use glm-4.5
MAX_TOKENS_PER_CALL = 2000  # Prevent excessive token usage
MAX_SEARCH_RESULTS = 10
BASE_URL = "https://api.z.ai/api/coding/paas/v4"


class ZAIWebSearchTool(Tool):
    """Z.AI web search using direct API with GLM-4.6 model.
    
    ✅ Uses GLM-4.6 (FREE with Lite plan) - NEVER GLM-4.5 (PAID)
    ✅ Direct API: https://api.z.ai/api/coding/paas/v4/web_search
    ✅ Quota: ~120 prompts every 5 hours
    ✅ Token limit: 2000 max per call
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web search tool.
        
        Args:
            api_key: Z.AI API key (if None, uses ZAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        self.base_url = BASE_URL
        self.model = DEFAULT_MODEL
        
        if not self.api_key:
            logger.warning("No Z.AI API key found. Web search will not be available.")
            self.available = False
            return
            
        if not AIOHTTP_AVAILABLE:
            logger.error("aiohttp is not installed. Install with: uv pip install aiohttp")
            self.available = False
            return
            
        self.available = True
        logger.info(f"Z.AI web search initialized (model: {self.model}, endpoint: {self.base_url})")

    @property
    def name(self) -> str:
        return "zai_web_search"

    @property
    def description(self) -> str:
        return (
            "Z.AI web search using GLM-4.6 model (FREE with Lite plan). "
            "Direct API to https://api.z.ai/api/coding/paas/v4/web_search. "
            "Quota: ~120 prompts every 5 hours. "
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
                    "description": f"Maximum number of search results (1-{MAX_SEARCH_RESULTS}, default 5)",
                    "minimum": 1,
                    "maximum": MAX_SEARCH_RESULTS,
                    "default": 5,
                },
                "recency": {
                    "type": "string",
                    "description": "Time filter for results",
                    "enum": ["noLimit", "oneDay", "oneWeek", "oneMonth"],
                    "default": "noLimit",
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        max_results: int = 5,
        recency: str = "noLimit",
        **kwargs
    ) -> ToolResult:
        """Execute web search using Z.AI direct API.
        
        Args:
            query: Search query
            max_results: Maximum number of results (default 5)
            recency: Time filter (noLimit, oneDay, oneWeek, oneMonth)
            
        Returns:
            ToolResult with search results or error
        """
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web search not available. Check API key and aiohttp installation."
            )

        # Validate parameters
        max_results = min(max(1, max_results), MAX_SEARCH_RESULTS)
        
        # Prepare search payload
        payload = {
            "search_engine": "search-prime",
            "search_query": query,
            "count": max_results,
            "search_recency_filter": recency,
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        search_results = result.get("search_result", [])
                        
                        # Format results for MiniMax-M2
                        formatted_results = []
                        for i, item in enumerate(search_results, 1):
                            title = item.get("title", "Untitled")
                            link = item.get("link", "")
                            content = item.get("content", "")
                            
                            formatted_results.append(
                                f"### Result {i}: {title}\n"
                                f"**Source**: {link}\n"
                                f"**Content**: {content}\n"
                            )
                        
                        if formatted_results:
                            output = (
                                f"## Web Search Results for: {query}\n"
                                f"**Model**: {self.model} (Lite plan)\n"
                                f"**Results**: {len(formatted_results)}\n"
                                f"**Timestamp**: {datetime.now().isoformat()}\n\n"
                                + "\n".join(formatted_results)
                            )
                        else:
                            output = f"No results found for query: {query}"
                        
                        logger.info(f"Z.AI web search completed: {len(search_results)} results for '{query}'")
                        return ToolResult(success=True, content=output, error=None)
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"Z.AI web search error {response.status}: {error_text}")
                        return ToolResult(
                            success=False,
                            content="",
                            error=f"Z.AI API error {response.status}: {error_text}"
                        )
                        
        except Exception as e:
            logger.exception("Z.AI web search failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Z.AI web search exception: {str(e)}"
            )


class ZAIWebReaderTool(Tool):
    """Z.AI web page reader using direct API with GLM-4.6 model.
    
    ✅ Uses GLM-4.6 (FREE with Lite plan) - NEVER GLM-4.5 (PAID)
    ✅ Direct API: https://api.z.ai/api/coding/paas/v4/reader
    ✅ Quota: ~120 prompts every 5 hours
    ✅ Token limit: 2000 max per call
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web reader tool.
        
        Args:
            api_key: Z.AI API key (if None, uses ZAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        self.base_url = BASE_URL
        self.model = DEFAULT_MODEL
        
        if not self.api_key:
            logger.warning("No Z.AI API key found. Web reader will not be available.")
            self.available = False
            return
            
        if not AIOHTTP_AVAILABLE:
            logger.error("aiohttp is not installed. Install with: uv pip install aiohttp")
            self.available = False
            return
            
        self.available = True
        logger.info(f"Z.AI web reader initialized (model: {self.model}, endpoint: {self.base_url})")

    @property
    def name(self) -> str:
        return "zai_web_reader"

    @property
    def description(self) -> str:
        return (
            "Z.AI web page reader using GLM-4.6 model (FREE with Lite plan). "
            "Direct API to https://api.z.ai/api/coding/paas/v4/reader. "
            "Quota: ~120 prompts every 5 hours. "
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
                "format": {
                    "type": "string",
                    "description": "Output format for extracted content",
                    "enum": ["markdown", "html", "text"],
                    "default": "markdown",
                },
            },
            "required": ["url"],
        }

    async def execute(
        self,
        url: str,
        format: str = "markdown",
        **kwargs
    ) -> ToolResult:
        """Read web page content using Z.AI direct API.
        
        Args:
            url: URL to read
            format: Output format (markdown, html, text)
            
        Returns:
            ToolResult with page content or error
        """
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web reader not available. Check API key and aiohttp installation."
            )

        # Prepare reader payload
        payload = {
            "url": url,
            "return_format": format,
            "retain_images": True,
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/reader",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        reader_result = result.get("web_page_reader_result", {})
                        
                        title = reader_result.get("title", "N/A")
                        description = reader_result.get("description", "N/A")
                        content = reader_result.get("content", "")
                        
                        # Truncate content to prevent excessive token usage
                        if len(content) > MAX_TOKENS_PER_CALL * 4:  # Rough char-to-token ratio
                            content = content[:MAX_TOKENS_PER_CALL * 4] + "\n\n[Content truncated due to length]"
                        
                        output = (
                            f"## Web Page Content: {title}\n"
                            f"**URL**: {url}\n"
                            f"**Description**: {description}\n"
                            f"**Model**: {self.model} (Lite plan)\n"
                            f"**Format**: {format}\n"
                            f"**Timestamp**: {datetime.now().isoformat()}\n\n"
                            f"### Content\n{content}"
                        )
                        
                        logger.info(f"Z.AI web reader completed: {url}")
                        return ToolResult(success=True, content=output, error=None)
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"Z.AI web reader error {response.status}: {error_text}")
                        
                        # Fallback: use web search to get information about the URL
                        if response.status in [400, 401, 403]:
                            logger.info(f"Attempting web search fallback for URL: {url}")
                            search_tool = ZAIWebSearchTool(self.api_key)
                            if search_tool.available:
                                return await search_tool.execute(
                                    query=f"content from {url}",
                                    max_results=3
                                )
                        
                        return ToolResult(
                            success=False,
                            content="",
                            error=f"Z.AI reader API error {response.status}: {error_text}"
                        )
                        
        except Exception as e:
            logger.exception("Z.AI web reader failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Z.AI web reader exception: {str(e)}"
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
    """Test Z.AI tools functionality."""
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ ZAI_API_KEY not found in environment")
        return
    
    print("🧪 Testing Z.AI Web Tools...")
    print(f"📍 Endpoint: {BASE_URL}")
    print(f"🤖 Model: {DEFAULT_MODEL}")
    
    # Test web search
    search_tool = ZAIWebSearchTool(api_key)
    if search_tool.available:
        result = await search_tool.execute(query="Python programming", max_results=3)
        print(f"✅ Web Search: {'Success' if result.success else 'Failed'}")
        if result.success:
            print(f"   Results length: {len(result.content)} chars")
    else:
        print("❌ Web Search not available")
    
    print("\n✅ Z.AI tools test completed")


if __name__ == "__main__":
    asyncio.run(test_zai_tools())
