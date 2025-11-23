"""Unified MCP Client for Z.AI Integration.

This module provides a unified MCP-based approach to replace the fragmented
Z.AI implementations. It uses MCP protocol for standardized communication
with Z.AI's MCP servers.

MCP (Model Context Protocol) provides:
- Standardized tool calling interface
- Built-in quota tracking
- Native Z.AI integration
- Configuration-based enablement
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

logger = logging.getLogger(__name__)


class UnifiedZAIMCPClient:
    """Unified Z.AI client using MCP protocol.
    
    This replaces the fragmented approach with a single, consolidated client
    that uses MCP protocol for all Z.AI operations.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.z.ai/api/coding/paas/v4"):
        """Initialize Unified MCP Client.
        
        Args:
            api_key: Z.AI API key
            base_url: Base URL for Z.AI API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }
        self.request_id = f"mcp-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
    async def web_search_mcp(
        self, 
        query: str, 
        count: int = 3,
        search_engine: str = "search-prime",
        recency_filter: str = "noLimit"
    ) -> Dict[str, Any]:
        """Perform web search using MCP protocol.
        
        Args:
            query: Search query
            count: Number of results (1-50, default: 3 for testing)
            search_engine: Search engine - "search_std", "search_pro", etc.
            recency_filter: Time filter - "oneDay", "oneWeek", etc.
            
        Returns:
            Dict with search results
        """
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp not installed")
                
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "web_search_prime",
                "params": {
                    "query": query,
                    "count": count,
                    "search_engine": search_engine,
                    "recency_filter": recency_filter,
                    "request_id": self.request_id
                }
            }
            
            mcp_url = "https://api.z.ai/api/mcp/web_search_prime/mcp"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    mcp_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "method": "mcp_web_search",
                            "id": result.get("id"),
                            "search_result": result.get("result", []),
                            "query": query,
                            "count": count,
                            "timestamp": datetime.now().isoformat(),
                            "mcp_url": mcp_url
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"MCP search error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "method": "mcp_web_search",
                            "error": f"HTTP {response.status}: {error_text}",
                            "query": query
                        }
                        
        except Exception as e:
            logger.exception("MCP web search failed")
            return {
                "success": False,
                "method": "mcp_web_search", 
                "error": str(e),
                "query": query
            }
    
    async def web_reader_mcp(self, urls: List[str], format_type: str = "markdown") -> Dict[str, Any]:
        """Read web content using MCP protocol.
        
        Args:
            urls: List of URLs to read
            format_type: Output format - "markdown", "html", "text"
            
        Returns:
            Dict with web content
        """
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp not installed")
                
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "web_reader",
                "params": {
                    "urls": urls,
                    "return_format": format_type,
                    "retain_images": True,
                    "request_id": self.request_id
                }
            }
            
            mcp_url = "https://api.z.ai/api/mcp/web_reader/mcp"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    mcp_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=45)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "method": "mcp_web_reader",
                            "result": result.get("result", {}),
                            "urls": urls,
                            "format": format_type,
                            "timestamp": datetime.now().isoformat(),
                            "mcp_url": mcp_url
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"MCP reader error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "method": "mcp_web_reader",
                            "error": f"HTTP {response.status}: {error_text}",
                            "urls": urls
                        }
                        
        except Exception as e:
            logger.exception("MCP web reader failed")
            return {
                "success": False,
                "method": "mcp_web_reader",
                "error": str(e),
                "urls": urls
            }
    
    async def research_and_analyze_mcp(
        self,
        query: str,
        depth: str = "quick",
        use_reader: bool = False
    ) -> Dict[str, Any]:
        """Complete research workflow using MCP protocol.
        
        Args:
            query: Research query
            depth: Analysis depth - "quick" (3 sources), "comprehensive" (7 sources)
            use_reader: Whether to also read top URLs
            
        Returns:
            Dict with research results
        """
        # Configure based on depth and test mode
        depth_config = {
            "quick": {"count": 3, "recency": "noLimit"},
            "comprehensive": {"count": 7, "recency": "oneDay"},
        }
        
        config = depth_config.get(depth, depth_config["quick"])
        
        # Step 1: Web search
        search_result = await self.web_search_mcp(
            query=query,
            count=config["count"],
            recency_filter=config["recency"]
        )
        
        if not search_result["success"]:
            return search_result
        
        # Step 2: Extract URLs for reading if requested
        urls_to_read = []
        if use_reader and search_result.get("search_result"):
            # Take first 2 URLs for reader test (minimize cost)
            urls_to_read = [item.get("link") for item in search_result["search_result"][:2] if item.get("link")]
        
        # Step 3: Web reading if requested
        reader_result = None
        if urls_to_read:
            reader_result = await self.web_reader_mcp(urls_to_read)
        
        # Combine results
        search_results = search_result.get("search_result", [])
        analysis_content = []
        
        for i, item in enumerate(search_results, 1):
            analysis_content.append(f"""
**Search Result {i}: {item.get('title', 'N/A')}**
Source: {item.get('link', 'N/A')}
Summary: {item.get('content', 'N/A')[:200]}...
""")
        
        if reader_result and reader_result["success"]:
            analysis_content.append("\n--- Web Reader Content ---\n")
            reader_content = reader_result.get("result", {})
            if isinstance(reader_content, dict):
                for url, content in reader_content.items():
                    analysis_content.append(f"URL: {url}\nContent: {str(content)[:300]}...\n")
        
        return {
            "success": True,
            "method": "mcp_research_and_analyze",
            "query": query,
            "depth": depth,
            "search_used": search_result["success"],
            "reader_used": bool(urls_to_read) and reader_result and reader_result["success"],
            "analysis": "\n".join(analysis_content),
            "search_evidence": search_results,
            "reader_evidence": reader_result,
            "timestamp": datetime.now().isoformat(),
        }


async def test_unified_mcp_client():
    """Test the unified MCP client with real Z.AI endpoints."""
    from mini_agent.config.config import Config
    
    print("🚀 Testing Unified Z.AI MCP Client")
    print("=" * 40)
    
    try:
        config = Config()
        
        if not config.zai_api_key:
            print("❌ No Z.AI API key found")
            return False
        
        print(f"✅ Config loaded - API key present")
        
        # Create client
        client = UnifiedZAIMCPClient(config.zai_api_key)
        print(f"✅ MCP Client initialized")
        
        # Test 1: Basic web search
        print("\n🔍 Test 1: MCP Web Search")
        search_result = await client.web_search_mcp(
            query="MCP protocol Z.AI documentation",
            count=2
        )
        
        if search_result["success"]:
            print(f"   ✅ Search successful - {len(search_result.get('search_result', []))} results")
            for i, result in enumerate(search_result.get("search_result", [])[:2], 1):
                print(f"   {i}. {result.get('title', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Search failed: {search_result.get('error', 'Unknown error')}")
        
        # Test 2: Research workflow (with minimal reader usage)
        print("\n🔍 Test 2: MCP Research & Analysis")
        research_result = await client.research_and_analyze_mcp(
            query="Z.AI MCP servers configuration",
            depth="quick",
            use_reader=False  # Test without reader first
        )
        
        if research_result["success"]:
            print(f"   ✅ Research successful")
            print(f"   Depth: {research_result['depth']}")
            print(f"   Search evidence: {len(research_result.get('search_evidence', []))} items")
            print(f"   Reader used: {research_result['reader_used']}")
        else:
            print(f"   ❌ Research failed: {research_result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 40)
        return search_result["success"] and research_result["success"]
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run test
    success = asyncio.run(test_unified_mcp_client())
    print(f"\n📊 Overall Test Result: {'✅ PASSED' if success else '❌ FAILED'}")