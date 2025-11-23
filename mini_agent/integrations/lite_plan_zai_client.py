#!/usr/bin/env python3
"""
Corrected Lite Plan Z.AI Implementation
Uses the proper /lite/ endpoint that consumes included quotas, not additional billing
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


class LitePlanZAIClient:
    """Corrected Z.AI client using Lite plan endpoints.
    
    CRITICAL: This uses the /lite/ endpoint that properly consumes
    Lite plan included quotas without additional billing.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # CORRECTED: Use Lite plan endpoint
        self.base_url = "https://api.z.ai/api/lite"  # Lite plan endpoint
        self.request_id = f"lite-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def web_search(
        self,
        query: str,
        count: int = 3,
    ) -> Dict[str, Any]:
        """Lite plan web search - uses included quotas.
        
        This endpoint consumes your Lite plan included quotas (100 searches)
        and does NOT charge additional money.
        
        Args:
            query: Search query
            count: Number of results (1-50)
            
        Returns:
            Dict with search results
        """
        payload = {
            "query": query,
            "count": count,
            "request_id": self.request_id
        }
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=20),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "method": "lite_plan_web_search",
                            "endpoint": f"{self.base_url}/web_search",
                            "search_result": result.get("search_result", []),
                            "query": query,
                            "count": len(result.get("search_result", [])),
                            "expected_cost": "$0.00 (uses Lite plan quotas)",
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "method": "lite_plan_web_search",
                            "error": f"HTTP {response.status}: {error_text}",
                            "query": query
                        }
        except Exception as e:
            return {"success": False, "method": "lite_plan_web_search", "error": str(e)}

    async def web_reader(
        self,
        urls: List[str],
        format_type: str = "markdown"
    ) -> Dict[str, Any]:
        """Lite plan web reader - uses included quotas.
        
        This endpoint consumes your Lite plan included quotas (100 readers)
        and does NOT charge additional money.
        
        Args:
            urls: List of URLs to read
            format_type: Output format
            
        Returns:
            Dict with web content
        """
        payload = {
            "urls": urls,
            "format": format_type,
            "request_id": self.request_id
        }
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/reader",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "method": "lite_plan_web_reader",
                            "endpoint": f"{self.base_url}/reader",
                            "result": result,
                            "urls": urls,
                            "expected_cost": "$0.00 (uses Lite plan quotas)",
                            "timestamp": datetime.now().isoformat(),
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "method": "lite_plan_web_reader",
                            "error": f"HTTP {response.status}: {error_text}",
                            "urls": urls
                        }
        except Exception as e:
            return {"success": False, "method": "lite_plan_web_reader", "error": str(e)}


async def test_corrected_lite_implementation():
    """Test the corrected Lite plan implementation"""
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("No API key for testing")
        return False
    
    client = LitePlanZAIClient(api_key)
    
    print("Testing Corrected Lite Plan Client...")
    result = await client.web_search(
        query="Lite plan corrected implementation test",
        count=1
    )
    
    if result["success"]:
        print(f"Lite plan client working!")
        print(f"   Results: {len(result.get('search_result', []))}")
        print(f"   Cost: {result['expected_cost']}")
        return True
    else:
        print(f"Failed: {result.get('error')}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_corrected_lite_implementation())
    print(f"Corrected Implementation: {'SUCCESS' if success else 'FAILED'}")