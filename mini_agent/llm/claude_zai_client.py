"""Z.AI Claude Code Integration for Web Search Results.

This module provides integration with Z.AI through the Anthropic-compatible endpoint
to enable Claude Code to use web search results with natural citations.
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class SearchResultBlock:
    """Claude-compatible search result block."""
    type: str = "search_result"
    source: str = ""
    title: str = ""
    content: List[Dict[str, str]] = None
    citations: Optional[Dict[str, bool]] = None

    def __post_init__(self):
        if self.content is None:
            self.content = [{"type": "text", "text": ""}]
        if self.citations is None:
            self.citations = {"enabled": True}


class ClaudeZAIWebSearchClient:
    """Z.AI client for Claude Code integration using Anthropic-compatible endpoint."""
    
    def __init__(self, api_key: str):
        """Initialize Claude-compatible Z.AI client.
        
        Args:
            api_key: Z.AI Coding Plan API key
        """
        self.api_key = api_key
        # Use Coding Plan API for web search (Anthropic endpoint for chat only)
        self.base_url = "https://api.z.ai/api/coding/paas/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

    async def web_search_for_claude(
        self,
        query: str,
        count: int = 5,
        search_engine: str = "search-prime",
        recency_filter: str = "noLimit",
        domain_filter: Optional[str] = None,
    ) -> List[SearchResultBlock]:
        """Perform web search and format results as Claude search_result blocks.
        
        Args:
            query: Search query
            count: Number of results (1-50, default: 5)
            search_engine: Search engine to use - "search-prime", "search_std", etc.
            recency_filter: Time filter - oneDay, oneWeek, oneMonth, noLimit
            domain_filter: Optional domain restriction
            
        Returns:
            List of SearchResultBlock objects for Claude citation
        """
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
            
        # Prepare search payload
        payload = {
            "search_engine": search_engine,
            "search_query": query,
            "count": count,
            "search_recency_filter": recency_filter,
        }
        
        if domain_filter:
            payload["search_domain_filter"] = domain_filter

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        search_results = result.get("search_result", [])
                        
                        # Format results as Claude search_result blocks
                        claude_blocks = []
                        for i, search_item in enumerate(search_results):
                            # Extract content and format it properly
                            content_text = search_item.get("content", "")
                            title = search_item.get("title", "Untitled")
                            link = search_item.get("link", "")
                            
                            # Create text content for the search result
                            text_content = {
                                "type": "text",
                                "text": content_text
                            }
                            
                            # Create Claude-compatible search result block
                            search_block = SearchResultBlock(
                                type="search_result",
                                source=link,
                                title=title,
                                content=[text_content],
                                citations={"enabled": True}
                            )
                            
                            claude_blocks.append(search_block)
                        
                        logger.info(f"Created {len(claude_blocks)} search result blocks for Claude")
                        return claude_blocks
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"Z.AI web search error {response.status}: {error_text}")
                        
                        # Return error as search result for Claude
                        return [
                            SearchResultBlock(
                                type="search_result",
                                source="z.ai",
                                title="Search Error",
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"Search failed with error {response.status}: {error_text}"
                                    }
                                ],
                                citations={"enabled": False}
                            )
                        ]
                        
        except Exception as e:
            logger.exception("Z.AI web search for Claude failed")
            return [
                SearchResultBlock(
                    type="search_result",
                    source="z.ai",
                    title="Search Exception",
                    content=[
                        {
                            "type": "text",
                            "text": f"Search failed with exception: {str(e)}"
                        }
                    ],
                    citations={"enabled": False}
                )
            ]

    async def web_reading(
        self,
        url: str,
        format_type: str = "markdown",
        include_images: bool = True,
    ) -> dict[str, Any]:
        """Read web page content using Z.AI Web Reader API.
        
        Args:
            url: URL to read
            format_type: Output format - "markdown", "html", "text"
            include_images: Whether to retain images
            
        Returns:
            Dict with extracted content and metadata
        """
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
            
        payload = {
            "url": url,
            "return_format": format_type,
            "retain_images": include_images,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/reader",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        reader_result = result.get("web_page_reader_result", {})
                        
                        return {
                            "success": True,
                            "id": result.get("id"),
                            "created": result.get("created"),
                            "request_id": result.get("request_id"),
                            "model": result.get("model"),
                            "url": url,
                            "title": reader_result.get("title", "N/A"),
                            "description": reader_result.get("description", "N/A"),
                            "content": reader_result.get("content", ""),
                            "metadata": reader_result.get("metadata", {}),
                            "external": reader_result.get("external", {}),
                            "format": format_type,
                            "word_count": len(reader_result.get("content", "").split()),
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Z.AI web reading error {response.status}: {error_text}")
                        
                        # Fallback: use web search for information about the URL
                        logger.info(f"Falling back to web search for URL: {url}")
                        search_result = await self.web_search_for_claude(
                            query=f"content summary {url}",
                            count=3,
                            search_engine="search-prime"
                        )
                        
                        if search_result:
                            # Format as reader result
                            combined_content = "\n\n".join([
                                f"**{block.title}**\n{block.content[0]['text']}"
                                for block in search_result
                            ])
                            
                            return {
                                "success": True,
                                "url": url,
                                "title": f"Content from {url} (via search fallback)",
                                "description": "Content extracted using web search fallback",
                                "content": combined_content,
                                "metadata": {
                                    "extraction_method": "web_search_fallback",
                                    "original_error": error_text,
                                },
                                "format": format_type,
                                "word_count": len(combined_content.split()),
                                "timestamp": datetime.now().isoformat(),
                            }
                        else:
                            return {
                                "success": False,
                                "url": url,
                                "error": f"Reader API error {response.status} and fallback failed: {error_text}",
                            }
        except Exception as e:
            logger.exception("Z.AI web reading failed")
            return {"success": False, "url": url, "error": str(e)}

    async def research_and_analyze_for_claude(
        self,
        query: str,
        depth: str = "comprehensive",
        search_engine: str = "search-prime"
    ) -> Dict[str, Any]:
        """Perform research and analysis for Claude Code integration.
        
        Args:
            query: Research query
            depth: Analysis depth - "quick" (3 sources), "comprehensive" (7 sources), "deep" (10 sources)
            search_engine: Search engine to use
            
        Returns:
            Dict with research results and search blocks for Claude
        """
        # Configure search parameters based on depth
        depth_config = {
            "quick": {"count": 3, "recency": "noLimit"},
            "comprehensive": {"count": 7, "recency": "oneDay"},
            "deep": {"count": 10, "recency": "oneWeek"},
        }
        
        config = depth_config.get(depth, depth_config["comprehensive"])
        
        # Perform web search
        search_blocks = await self.web_search_for_claude(
            query=query,
            count=config["count"],
            search_engine=search_engine,
            recency_filter=config["recency"]
        )
        
        if search_blocks:
            # Prepare comprehensive research result
            research_result = {
                "success": True,
                "query": query,
                "depth": depth,
                "model": "Z.AI Search Prime (Claude Compatible)",
                "search_blocks": search_blocks,
                "source_count": len(search_blocks),
                "timestamp": datetime.now().isoformat(),
                "integration_type": "Claude search_result blocks"
            }
            
            return research_result
        else:
            return {
                "success": False,
                "error": "No search results obtained",
                "query": query,
                "timestamp": datetime.now().isoformat()
            }


def get_zai_api_key() -> str | None:
    """Get Z.AI API key from environment.
    
    Returns:
        API key if found, None otherwise
    """
    return os.getenv("ZAI_API_KEY")


async def test_claude_zai_integration():
    """Test function for Z.AI Claude integration."""
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found in environment")
        return
    
    client = ClaudeZAIWebSearchClient(api_key)
    
    print("🧪 Testing Z.AI Claude Web Search Integration...")
    
    # Test search
    result = await client.web_search_for_claude(
        query="Python web scraping best practices",
        count=3,
        search_engine="search-prime"
    )
    
    print(f"✅ Search completed. Generated {len(result)} search result blocks for Claude")
    
    # Test research
    research_result = await client.research_and_analyze_for_claude(
        query="AI coding assistants 2024",
        depth="quick",
        search_engine="search-prime"
    )
    
    print(f"✅ Research completed. Sources: {research_result.get('source_count', 0)}")
    print(f"✅ Integration type: {research_result.get('integration_type')}")


if __name__ == "__main__":
    # Run test
    asyncio.run(test_claude_zai_integration())
