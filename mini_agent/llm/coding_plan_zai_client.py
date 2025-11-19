"""Corrected Z.AI client using Coding Plan API.

This is the PROPER implementation for GLM Coding Plan users.
Based on Z.AI documentation: https://docs.z.ai/devpack/tool/others
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

logger = logging.getLogger(__name__)


class CodingPlanZAIClient:
    """Z.AI client using Coding Plan API endpoints.
    
    IMPORTANT: This uses the exclusive Coding API for paid subscribers.
    Base URL: https://api.z.ai/api/coding/paas/v4
    
    This provides access to GLM-4.6 and GLM-4.5 models through
    the official Coding Plan endpoints.
    """

    def __init__(self, api_key: str):
        """Initialize Coding Plan Z.AI client.
        
        Args:
            api_key: Z.AI Coding Plan API key
        """
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/coding/paas/v4"  # CORRECT ENDPOINT
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

    async def web_search(
        self,
        query: str,
        count: int = 5,
        search_engine: str = "search-std",
        recency_filter: str = "noLimit",
        domain_filter: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Coding Plan web search using exclusive API.
        
        This uses the Coding Plan API which provides access to GLM-4.6.
        
        Args:
            query: Search query
            count: Number of results (1-50, default: 5)
            search_engine: Search engine to use - "search_std" (default), "search_pro", "search_pro_sogou", "search_pro_quark"
            recency_filter: Time filter - oneDay, oneWeek, oneMonth, oneYear, noLimit
            domain_filter: Optional domain restriction (e.g., "arxiv.org")
            request_id: Optional request tracking ID
            user_id: Optional user tracking ID
            
        Returns:
            Dict with search results from Z.AI Coding Plan API
        """
        # Prepare payload
        payload = {
            "search_engine": search_engine,
            "search_query": query,
            "count": count,
            "search_recency_filter": recency_filter,
        }

        if domain_filter:
            payload["search_domain_filter"] = domain_filter
        if request_id:
            payload["request_id"] = request_id
        if user_id:
            payload["user_id"] = user_id

        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    response_text = await response.text()
                    logger.info(f"Coding Plan API Response Status: {response.status}")
                    logger.info(f"Coding Plan API Response: {response_text}")
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "id": result.get("id"),
                            "created": result.get("created"),
                            "request_id": result.get("request_id"),
                            "search_result": result.get("search_result", []),
                            "search_intent": result.get("search_intent", []),
                            "query": query,
                            "count": len(result.get("search_result", [])),
                            "timestamp": datetime.now().isoformat(),
                            "api_endpoint": self.base_url,
                        }
                    elif response.status == 429:
                        return {
                            "success": False,
                            "error": f"Billing Error: {response_text}",
                            "api_endpoint": self.base_url,
                            "recommendation": "Check Coding Plan subscription and billing"
                        }
                    else:
                        logger.error(f"Coding Plan web search error {response.status}: {response_text}")
                        return {
                            "success": False,
                            "error": f"API error {response.status}: {response_text}",
                            "api_endpoint": self.base_url,
                        }
        except Exception as e:
            logger.exception("Coding Plan web search failed")
            return {"success": False, "error": str(e), "api_endpoint": self.base_url}

    async def web_reading(
        self,
        url: str,
        format_type: str = "markdown",
        include_images: bool = True,
    ) -> dict[str, Any]:
        """Read web page content using Coding Plan API.
        
        Uses the exclusive Coding Plan /web_page_reader endpoint.
        
        Args:
            url: URL to read
            format_type: Output format - "markdown", "html", "text"
            include_images: Whether to retain images
            
        Returns:
            Dict with extracted content and metadata
        """
        payload = {
            "url": url,
            "return_format": format_type,
            "retain_images": include_images,
        }

        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_page_reader",  # CORRECT endpoint
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    response_text = await response.text()
                    logger.info(f"Coding Plan Reader Response Status: {response.status}")
                    logger.info(f"Coding Plan Reader Response: {response_text}")
                    
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
                            "api_endpoint": self.base_url,
                        }
                    elif response.status == 404:
                        # The /web_page_reader endpoint might not exist in Coding Plan API
                        return {
                            "success": False,
                            "error": f"Endpoint not available in Coding Plan API: {response_text}",
                            "url": url,
                            "api_endpoint": self.base_url,
                            "recommendation": "Use web search fallback for content extraction"
                        }
                    else:
                        logger.error(f"Coding Plan web reading error {response.status}: {response_text}")
                        return {
                            "success": False,
                            "error": f"API error {response.status}: {response_text}",
                            "url": url,
                            "api_endpoint": self.base_url,
                        }
        except Exception as e:
            logger.exception("Coding Plan web reading failed")
            return {"success": False, "url": url, "error": str(e), "api_endpoint": self.base_url}

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "GLM-4.6",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> dict[str, Any]:
        """Chat completion using GLM models via Coding Plan.
        
        This is the primary use case for Coding Plan - GLM model access.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name - "GLM-4.6", "GLM-4.5", or "GLM-4.5-air"
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict with chat completion result
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed. Please install it with: pip install aiohttp")
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",  # OpenAI-compatible endpoint
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    response_text = await response.text()
                    logger.info(f"GLM Chat Response Status: {response.status}")
                    logger.info(f"GLM Chat Response: {response_text}")
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "id": result.get("id"),
                            "object": result.get("object"),
                            "created": result.get("created"),
                            "model": result.get("model"),
                            "choices": result.get("choices", []),
                            "usage": result.get("usage", {}),
                            "timestamp": datetime.now().isoformat(),
                            "api_endpoint": self.base_url,
                        }
                    elif response.status == 429:
                        return {
                            "success": False,
                            "error": f"Billing Error: {response_text}",
                            "api_endpoint": self.base_url,
                            "recommendation": "Check Coding Plan subscription and billing"
                        }
                    else:
                        logger.error(f"GLM chat completion error {response.status}: {response_text}")
                        return {
                            "success": False,
                            "error": f"API error {response.status}: {response_text}",
                            "api_endpoint": self.base_url,
                        }
        except Exception as e:
            logger.exception("GLM chat completion failed")
            return {"success": False, "error": str(e), "api_endpoint": self.base_url}


def get_coding_plan_api_key() -> str | None:
    """Get Coding Plan API key from environment.
    
    Returns:
        API key if found, None otherwise
    """
    return os.getenv("ZAI_CODING_PLAN_API_KEY")
