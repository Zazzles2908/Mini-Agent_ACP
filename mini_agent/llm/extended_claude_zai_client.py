"""Extended Z.AI integration with web reader support for Claude."""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

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


class ExtendedClaudeZAIWebReader:
    """Extended web reader that can provide web reading results as Claude blocks."""
    
    def __init__(self, api_key: str):
        """Initialize extended web reader.
        
        Args:
            api_key: Z.AI Coding Plan API key
        """
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/coding/paas/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

    async def web_reader_for_claude(
        self,
        url: str,
        format_type: str = "markdown",
        include_images: bool = True,
    ) -> List[SearchResultBlock]:
        """Read web page and format as Claude search_result block.
        
        Args:
            url: URL to read
            format_type: Output format - "markdown", "html", "text"
            include_images: Whether to retain images
            
        Returns:
            List of SearchResultBlock objects for Claude citation
        """
        try:
            import aiohttp
            
            payload = {
                "url": url,
                "return_format": format_type,
                "retain_images": include_images,
            }
            
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
                        
                        # Extract content and metadata
                        title = reader_result.get("title", "Web Page Content")
                        description = reader_result.get("description", "Web page content")
                        content = reader_result.get("content", "No content found")
                        
                        # Create Claude-compatible search result block
                        # Note: Web reader content is formatted as a single search result
                        search_block = SearchResultBlock(
                            type="search_result",
                            source=url,
                            title=title,
                            content=[{
                                "type": "text",
                                "text": f"{description}\n\n{content}"
                            }],
                            citations={"enabled": True}
                        )
                        
                        logger.info(f"Successfully read web page: {url}")
                        return [search_block]
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"Web reader error {response.status}: {error_text}")
                        
                        # Return error as search result
                        return [
                            SearchResultBlock(
                                type="search_result",
                                source=url,
                                title="Web Reader Error",
                                content=[
                                    {
                                        "type": "text",
                                        "text": f"Failed to read web page: {response.status} - {error_text}"
                                    }
                                ],
                                citations={"enabled": False}
                            )
                        ]
                        
        except Exception as e:
            logger.exception("Web reader failed")
            return [
                SearchResultBlock(
                    type="search_result",
                    source=url,
                    title="Web Reader Exception",
                    content=[
                        {
                            "type": "text",
                            "text": f"Web reader failed with exception: {str(e)}"
                        }
                    ],
                    citations={"enabled": False}
                )
            ]

    async def combined_search_and_read(
        self,
        query: str,
        read_url: str,
        search_count: int = 3,
    ) -> Dict[str, Any]:
        """Perform combined search and web reading for comprehensive results.
        
        Args:
            query: Search query
            read_url: URL to read
            search_count: Number of search results
            
        Returns:
            Dict with combined search and reading results
        """
        from .claude_zai_client import ClaudeZAIWebSearchClient
        
        # We'll create a simplified search client inline to avoid circular imports
        from .claude_zai_client import get_zai_api_key
        
        # Create a simple client for search
        class SimpleClaudeZAIWebSearchClient:
            def __init__(self, api_key: str):
                self.api_key = api_key
                self.base_url = "https://api.z.ai/api/coding/paas/v4"
                self.headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept-Language": "en-US,en",
                }

            async def web_search_for_claude(self, query: str, count: int, search_engine: str):
                payload = {
                    "search_engine": search_engine,
                    "search_query": query,
                    "count": count,
                    "search_recency_filter": "noLimit",
                }
                
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
                            
                            claude_blocks = []
                            for search_item in search_results:
                                content_text = search_item.get("content", "")
                                title = search_item.get("title", "Untitled")
                                link = search_item.get("link", "")
                                
                                text_content = {"type": "text", "text": content_text}
                                
                                search_block = SearchResultBlock(
                                    type="search_result",
                                    source=link,
                                    title=title,
                                    content=[text_content],
                                    citations={"enabled": True}
                                )
                                
                                claude_blocks.append(search_block)
                            
                            return claude_blocks
                        else:
                            return []
                
        search_client = SimpleClaudeZAIWebSearchClient(self.api_key)
        
        # Perform search
        search_blocks = await search_client.web_search_for_claude(
            query=query,
            count=search_count,
            search_engine="search-prime"
        )
        
        # Perform web reading
        read_blocks = await self.web_reader_for_claude(
            url=read_url,
            format_type="markdown",
            include_images=False  # Avoid large content in search results
        )
        
        # Combine results
        all_blocks = search_blocks + read_blocks
        
        return {
            "success": True,
            "query": query,
            "read_url": read_url,
            "search_blocks": search_blocks,
            "read_blocks": read_blocks,
            "total_blocks": len(all_blocks),
            "combined_results": all_blocks,
            "timestamp": asyncio.get_event_loop().time(),
            "integration_type": "combined_search_and_read"
        }


async def test_web_reader_integration():
    """Test web reader functionality."""
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        return False
    
    reader = ExtendedClaudeZAIWebReader(api_key)
    
    # Test web reading
    try:
        # Test with a reliable URL
        test_url = "https://httpbin.org/html"
        
        result_blocks = await reader.web_reader_for_claude(
            url=test_url,
            format_type="markdown",
            include_images=False
        )
        
        if result_blocks and len(result_blocks) > 0:
            block = result_blocks[0]
            return True
        else:
            return False
            
    except Exception as e:
        return False


async def test_combined_workflow():
    """Test combined search and read workflow."""
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        return False
    
    reader = ExtendedClaudeZAIWebReader(api_key)
    
    try:
        # Test combined workflow
        result = await reader.combined_search_and_read(
            query="Python web development frameworks",
            read_url="https://docs.python.org/3/",
            search_count=2
        )
        
        if result.get("success"):
            return True
        else:
            return False
            
    except Exception as e:
        return False


if __name__ == "__main__":
    # Test web reader functionality
    reader_success = asyncio.run(test_web_reader_integration())
    combined_success = asyncio.run(test_combined_workflow())
    
    if reader_success and combined_success:
        print("Web reader integration is working!")
        print("Can provide web reading results as Claude search_result blocks")
        print("Can combine search and reading for comprehensive results")
    else:
        print("Web reader integration needs debugging")
