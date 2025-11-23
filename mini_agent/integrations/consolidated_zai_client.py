#!/usr/bin/env python3
"""
Phase 1: Consolidated Z.AI Implementation
Creates a single, unified Z.AI client to replace fragmented implementations
"""

import asyncio
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


class ConsolidatedZAIClient:
    """Consolidated Z.AI client replacing all fragmented implementations.
    
    This single client combines the best of:
    - ZAIClient (proven working)
    - CodingPlanZAIClient 
    - ZAIWebSearchTool interface
    
    Features:
    - Unified interface for all Z.AI operations
    - Built-in credit protection
    - Test mode optimization
    - Standardized error handling
    """
    
    def __init__(self, api_key: str, config_override: Optional[Dict] = None):
        """Initialize Consolidated Z.AI Client.
        
        Args:
            api_key: Z.AI API key
            config_override: Optional config for testing/customization
        """
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/coding/paas/v4"
        self.request_id = f"consolidated-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Configuration with test mode optimizations
        self.config = {
            "max_results": 3,  # Test mode: minimal results
            "max_tokens": 200,  # Test mode: minimal tokens
            "timeout": 20,  # Reasonable timeout
            "efficiency_mode": True,
            "test_mode": True
        }
        
        if config_override:
            self.config.update(config_override)
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

    async def web_search(
        self,
        query: str,
        count: Optional[int] = None,
        search_engine: str = "search-prime",
        recency_filter: str = "noLimit",
        domain_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Unified web search interface.
        
        This replaces the fragmented web search implementations with a single,
        optimized interface based on the proven working ZAIClient approach.
        
        Args:
            query: Search query
            count: Number of results (defaults to config for test mode)
            search_engine: Search engine - "search-prime", "search_std", etc.
            recency_filter: Time filter - "oneDay", "oneWeek", etc.
            domain_filter: Optional domain restriction
            
        Returns:
            Dict with standardized search results
        """
        # Use config defaults for test mode
        result_count = count or self.config["max_results"]
        
        payload = {
            "search_engine": search_engine,
            "search_query": query,
            "count": result_count,
            "search_recency_filter": recency_filter,
            "request_id": self.request_id
        }
        
        if domain_filter:
            payload["search_domain_filter"] = domain_filter
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.config["timeout"]),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        search_result = result.get("search_result", [])
                        return {
                            "success": True,
                            "method": "consolidated_web_search",
                            "id": result.get("id"),
                            "created": result.get("created"),
                            "request_id": result.get("request_id"),
                            "search_result": search_result,
                            "search_intent": result.get("search_intent", []),
                            "query": query,
                            "count": len(search_result),
                            "config_used": {"result_count": result_count, "timeout": self.config["timeout"]},
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Consolidated search error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "method": "consolidated_web_search",
                            "error": f"API error {response.status}: {error_text}",
                            "query": query
                        }
        except Exception as e:
            logger.exception("Consolidated web search failed")
            return {"success": False, "method": "consolidated_web_search", "error": str(e)}

    async def web_reader(self, url: str, format_type: str = "markdown") -> Dict[str, Any]:
        """Unified web reader interface.
        
        Args:
            url: URL to read
            format_type: Output format - "markdown", "html", "text"
            
        Returns:
            Dict with extracted content and metadata
        """
        payload = {
            "url": url,
            "return_format": format_type,
            "retain_images": True,
        }
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/reader",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.config["timeout"]),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        reader_result = result.get("web_page_reader_result", {})
                        
                        return {
                            "success": True,
                            "method": "consolidated_web_reader",
                            "id": result.get("id"),
                            "created": result.get("created"),
                            "request_id": result.get("request_id"),
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
                        logger.error(f"Consolidated reader error {response.status}: {error_text}")
                        
                        # Fallback: use web search for information about the URL
                        search_result = await self.web_search(
                            query=f"content summary {url}",
                            count=2,
                            recency_filter="noLimit"
                        )
                        
                        if search_result["success"]:
                            results = search_result.get("search_result", [])
                            combined_content = "\n\n".join([
                                f"**{r.get('title', 'N/A')}**\n{r.get('content', 'N/A')}"
                                for r in results
                            ])
                            
                            return {
                                "success": True,
                                "method": "consolidated_web_reader_fallback",
                                "url": url,
                                "title": f"Content from {url} (via search fallback)",
                                "description": "Content extracted using web search fallback",
                                "content": combined_content,
                                "metadata": {
                                    "extraction_method": "web_search_fallback",
                                    "original_error": error_text,
                                },
                                "format": "search_fallback",
                                "word_count": len(combined_content.split()),
                                "timestamp": datetime.now().isoformat(),
                            }
                        else:
                            return {
                                "success": False,
                                "method": "consolidated_web_reader",
                                "url": url,
                                "error": f"Reader API error {response.status} and fallback failed: {error_text}",
                            }
        except Exception as e:
            logger.exception("Consolidated web reader failed")
            return {"success": False, "method": "consolidated_web_reader", "url": url, "error": str(e)}

    async def research_and_analyze(
        self,
        query: str,
        depth: str = "quick",
        use_reader: bool = False,
        max_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """Unified research and analysis workflow.
        
        This replaces the fragmented research methods with a single,
        optimized workflow based on test mode requirements.
        
        Args:
            query: Research query
            depth: Analysis depth - "quick" (3 sources), "comprehensive" (5 sources)
            use_reader: Whether to also read top URLs (use sparingly)
            max_results: Maximum results (defaults to config)
            
        Returns:
            Dict with research results
        """
        # Configure based on depth and test mode
        depth_config = {
            "quick": {"count": max_results or self.config["max_results"], "recency": "noLimit"},
            "comprehensive": {"count": 5, "recency": "oneDay"},
        }
        
        config = depth_config.get(depth, depth_config["quick"])
        
        # Step 1: Web search
        search_result = await self.web_search(
            query=query,
            count=config["count"],
            recency_filter=config["recency"]
        )
        
        if not search_result["success"]:
            return search_result
        
        # Step 2: Extract URLs for reading if requested (limit to 1 URL for test mode)
        urls_to_read = []
        if use_reader and search_result.get("search_result"):
            # Take only 1 URL for test mode to minimize cost
            urls_to_read = [search_result["search_result"][0].get("link")]
            urls_to_read = [url for url in urls_to_read if url]
        
        # Step 3: Web reading if requested
        reader_result = None
        if urls_to_read:
            reader_result = await self.web_reader(urls_to_read[0])  # Single URL for test mode
        
        # Combine results
        search_results = search_result.get("search_result", [])
        analysis_parts = []
        
        for i, item in enumerate(search_results, 1):
            analysis_parts.append(f"""
**Search Result {i}: {item.get('title', 'N/A')}**
Source: {item.get('link', 'N/A')}
Media: {item.get('media', 'N/A')}
Date: {item.get('publish_date', 'N/A')}

{item.get('content', 'N/A')}
""")
        
        if reader_result and reader_result["success"]:
            analysis_parts.append(f"""
--- Web Reader Content ---
URL: {reader_result.get('url', 'N/A')}
Title: {reader_result.get('title', 'N/A')}

{reader_result.get('content', 'N/A')}
""")
        
        analysis = "\n---\n".join(analysis_parts)
        
        return {
            "success": True,
            "method": "consolidated_research_and_analyze",
            "query": query,
            "depth": depth,
            "analysis": analysis,
            "search_evidence": search_results,
            "reader_evidence": reader_result,
            "config_used": {
                "depth": depth,
                "search_count": config["count"],
                "reader_used": bool(urls_to_read),
                "test_mode": self.config["test_mode"]
            },
            "timestamp": datetime.now().isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        """Get client status and configuration."""
        return {
            "client_type": "consolidated",
            "base_url": self.base_url,
            "config": self.config,
            "headers_present": bool(self.headers.get("Authorization")),
            "request_id": self.request_id,
            "aiohttp_available": AIOHTTP_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }


async def test_consolidated_client():
    """Test the consolidated Z.AI client."""
    print("🚀 Testing Consolidated Z.AI Client")
    print("=" * 45)
    
    try:
        api_key = os.getenv('ZAI_API_KEY')
        if not api_key:
            print("❌ No Z.AI API key found")
            return False
        
        # Create consolidated client
        client = ConsolidatedZAIClient(api_key)
        print("✅ Consolidated client created")
        
        # Test 1: Status check
        print("\n🔍 Test 1: Client Status")
        status = client.get_status()
        print(f"   Base URL: {status['base_url']}")
        print(f"   Test Mode: {status['config']['test_mode']}")
        print(f"   Max Results: {status['config']['max_results']}")
        
        # Test 2: Web search
        print("\n🔍 Test 2: Web Search")
        search_result = await client.web_search(
            query="Z.AI consolidated client test",
            count=2
        )
        
        if search_result["success"]:
            print(f"   ✅ Search successful")
            results = search_result.get("search_result", [])
            print(f"   Results: {len(results)} found")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result.get('title', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Search failed: {search_result.get('error', 'Unknown error')}")
        
        # Test 3: Research workflow (without reader for safety)
        print("\n🔍 Test 3: Research & Analysis")
        research_result = await client.research_and_analyze(
            query="Z.AI integration best practices",
            depth="quick",
            use_reader=False  # Test without reader first
        )
        
        if research_result["success"]:
            print(f"   ✅ Research successful")
            print(f"   Method: {research_result['method']}")
            print(f"   Evidence: {len(research_result.get('search_evidence', []))} search items")
            print(f"   Reader used: {research_result.get('config_used', {}).get('reader_used', False)}")
        else:
            print(f"   ❌ Research failed: {research_result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 45)
        overall_success = search_result["success"] and research_result["success"]
        print(f"📊 Overall Test: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_consolidated_client())
    print(f"\n🎯 Consolidation Status: {'✅ READY' if success else '❌ NEEDS FIXING'}")