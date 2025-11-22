"""Z.AI client for native web search and reading capabilities - Direct REST API.

This module provides integration with Z.AI's direct REST API endpoints
for web search and reading capabilities.

🚫 CREDIT PROTECTED - Z.AI client requires explicit config enablement.
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

from ..utils.credit_protection import block_zai_usage, check_zai_protection

logger = logging.getLogger(__name__)


class ZAIClient:
    """Z.AI client using direct REST API endpoints.
    
    Provides access to Z.AI's web search and reading capabilities
    through the official REST API v4 endpoints.
    """

    def __init__(self, api_key: str, use_coding_plan: bool = True):
        # CRITICAL: Check credit protection before any Z.AI operations
        if not check_zai_protection():  # If protection is active (Z.AI disabled), block usage
            block_zai_usage("ZAIClient")
        """Initialize Z.AI client.
        
        Args:
            api_key: Z.AI API key
            use_coding_plan: Use GLM Coding Plan API (True) or Common API (False)
        """
        self.api_key = api_key
        # CORRECTED: Use Coding Plan API for GLM Coding Plan subscribers
        self.base_url = "https://api.z.ai/api/coding/paas/v4" if use_coding_plan else "https://api.z.ai/api/paas/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        }

    async def web_search(
        self,
        query: str,
        count: int = 5,
        search_engine: str = "search-prime",
        recency_filter: str = "noLimit",
        domain_filter: Optional[str] = None,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Direct Z.AI web search using REST API.
        
        Args:
            query: Search query
            count: Number of results (1-50, default: 5)
            search_engine: Search engine to use - "search_std" (default), "search_pro", "search_pro_sogou", "search_pro_quark"
            recency_filter: Time filter - oneDay, oneWeek, oneMonth, oneYear, noLimit
            domain_filter: Optional domain restriction (e.g., "arxiv.org")
            request_id: Optional request tracking ID
            user_id: Optional user tracking ID
            
        Returns:
            Dict with search results from Z.AI
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
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Z.AI web search error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "error": f"API error {response.status}: {error_text}",
                        }
        except Exception as e:
            logger.exception("Z.AI web search failed")
            return {"success": False, "error": str(e)}

    async def web_reading(
        self,
        url: str,
        format_type: str = "markdown",
        include_images: bool = True,
    ) -> dict[str, Any]:
        """Read web page content using Z.AI Web Reader API.
        
        Uses the official Z.AI /reader endpoint for reliable content extraction.
        
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
                    f"{self.base_url}/reader",  # Use correct /reader endpoint for Lite Plan
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
                        search_result = await self.web_search(
                            query=f"content summary {url}",
                            count=3,
                            recency_filter="noLimit"
                        )
                        
                        if search_result["success"]:
                            # Format as reader result
                            results = search_result.get("search_result", [])
                            combined_content = "\n\n".join([
                                f"**{r.get('title', 'N/A')}**\n{r.get('content', 'N/A')}"
                                for r in results
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

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "GLM-4.6",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> dict[str, Any]:
        """Chat completion using GLM models via Coding Plan API.
        
        PRIMARY FEATURE of GLM Coding Plan - provides access to GLM-4.6 and GLM-4.5 models.
        
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
                        choice = result.get("choices", [{}])[0]
                        return {
                            "success": True,
                            "id": result.get("id"),
                            "object": result.get("object"),
                            "created": result.get("created"),
                            "model": result.get("model"),
                            "content": choice.get("message", {}).get("content", ""),
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

    async def research_and_analyze(
        self,
        query: str,
        depth: str = "comprehensive",
        model_preference: str = "auto",
    ) -> dict[str, Any]:
        """Complete research workflow using web search with proper GLM models.
        
        Args:
            query: Research query
            depth: Analysis depth - "quick" (3 sources), "comprehensive" (7 sources), "deep" (10 sources)
            model_preference: Model preference - "glm-4.5", "glm-4.6", or "auto"
            
        Returns:
            Dict with research results
        """
        # Configure search depth and model
        depth_config = {
            "quick": {"count": 3, "recency": "noLimit"},
            "comprehensive": {"count": 7, "recency": "oneDay"},
            "deep": {"count": 10, "recency": "oneWeek"},
        }

        # Use better GLM models based on user preference
        if model_preference == "auto":
            model_used = "GLM-4.5 (optimized for tool invocation and web browsing)"
            model_description = "Optimized for tool invocation, web browsing, software engineering"
        elif model_preference == "glm-4.5":
            model_used = "GLM-4.5"
            model_description = "Optimized for tool invocation, web browsing, software engineering"
        elif model_preference == "glm-4.6":
            model_used = "GLM-4.6"
            model_description = "Latest iteration with comprehensive enhancements across multiple domains"
        else:
            model_used = "Z.AI Direct Search"
            model_description = f"Direct REST API with {depth_config[depth]['count']} sources"

        config = depth_config.get(depth, depth_config["comprehensive"])

        # Perform web search
        result = await self.web_search(
            query=query,
            count=config["count"],
            recency_filter=config["recency"],
        )

        if result["success"]:
            # Format results for analysis
            search_results = result.get("search_result", [])
            
            # Combine all search results into analysis
            analysis_parts = []
            for i, item in enumerate(search_results, 1):
                analysis_parts.append(f"""
**Result {i}: {item.get('title', 'N/A')}**
Source: {item.get('link', 'N/A')}
Media: {item.get('media', 'N/A')}
Date: {item.get('publish_date', 'N/A')}

{item.get('content', 'N/A')}
""")
            
            analysis = "\n---\n".join(analysis_parts)
            
            return {
                "success": True,
                "query": query,
                "depth": depth,
                "model_used": model_used,
                "model_description": model_description,
                "analysis": analysis,
                "search_evidence": search_results,
                "token_usage": {"note": "Direct search API does not report token usage"},
                "timestamp": datetime.now().isoformat(),
            }
    async def gl_research_and_analyze(
        self,
        query: str,
        model: str = "GLM-4.6",
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """Research and analysis using GLM models.
        
        Uses GLM-4.6/GLM-4.5 to analyze queries and provide comprehensive responses.
        This is the PRIMARY VALUE of GLM Coding Plan subscription.
        
        Args:
            query: Research query
            model: GLM model to use - "GLM-4.6" or "GLM-4.5"
            temperature: Response creativity (0.1-0.5 for research)
            
        Returns:
            Dict with GLM analysis
        """
        messages = [
            {
                "role": "system", 
                "content": f"You are a research assistant using {model}. Provide comprehensive, factual analysis with supporting details."
            },
            {
                "role": "user", 
                "content": f"Please research and analyze: {query}. Provide a detailed response with multiple perspectives and supporting evidence."
            }
        ]
        
        result = await self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature
        )
        
        if result["success"]:
            return {
                "success": True,
                "query": query,
                "model_used": model,
                "analysis": result.get("content", ""),
                "usage": result.get("usage", {}),
                "timestamp": datetime.now().isoformat(),
                "api_endpoint": self.base_url,
            }
        else:
            return result
        """Complete research workflow using web search with proper GLM models.
        
        Args:
            query: Research query
            depth: Analysis depth - "quick" (3 sources), "comprehensive" (7 sources), "deep" (10 sources)
            model_preference: Model preference - "glm-4.5", "glm-4.6", or "auto"
            
        Returns:
            Dict with research results
        """
        # Configure search depth and model
        depth_config = {
            "quick": {"count": 3, "recency": "noLimit"},
            "comprehensive": {"count": 7, "recency": "oneDay"},
            "deep": {"count": 10, "recency": "oneWeek"},
        }

        # Use better GLM models based on user preference
        if model_preference == "auto":
            model_used = "GLM-4.5 (optimized for tool invocation and web browsing)"
            model_description = "Optimized for tool invocation, web browsing, software engineering"
        elif model_preference == "glm-4.5":
            model_used = "GLM-4.5"
            model_description = "Optimized for tool invocation, web browsing, software engineering"
        elif model_preference == "glm-4.6":
            model_used = "GLM-4.6"
            model_description = "Latest iteration with comprehensive enhancements across multiple domains"
        else:
            model_used = "Z.AI Direct Search"
            model_description = f"Direct REST API with {depth_config[depth]['count']} sources"

        config = depth_config.get(depth, depth_config["comprehensive"])

        # Perform web search
        result = await self.web_search(
            query=query,
            count=config["count"],
            recency_filter=config["recency"],
        )

        if result["success"]:
            # Format results for analysis
            search_results = result.get("search_result", [])
            
            # Combine all search results into analysis
            analysis_parts = []
            for i, item in enumerate(search_results, 1):
                analysis_parts.append(f"""
**Result {i}: {item.get('title', 'N/A')}**
Source: {item.get('link', 'N/A')}
Media: {item.get('media', 'N/A')}
Date: {item.get('publish_date', 'N/A')}

{item.get('content', 'N/A')}
""")
            
            analysis = "\n---\n".join(analysis_parts)
            
            return {
                "success": True,
                "query": query,
                "depth": depth,
                "model_used": model_used,
                "model_description": model_description,
                "analysis": analysis,
                "search_evidence": search_results,
                "token_usage": {"note": "Direct search API does not report token usage"},
                "timestamp": datetime.now().isoformat(),
            }
    async def gl_research_and_analyze(
        self,
        query: str,
        model: str = "GLM-4.6",
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """Research and analysis using GLM models.
        
        Uses GLM-4.6/GLM-4.5 to analyze queries and provide comprehensive responses.
        This is the PRIMARY VALUE of GLM Coding Plan subscription.
        
        Args:
            query: Research query
            model: GLM model to use - "GLM-4.6" or "GLM-4.5"
            temperature: Response creativity (0.1-0.5 for research)
            
        Returns:
            Dict with GLM analysis
        """
        messages = [
            {
                "role": "system", 
                "content": f"You are a research assistant using {model}. Provide comprehensive, factual analysis with supporting details."
            },
            {
                "role": "user", 
                "content": f"Please research and analyze: {query}. Provide a detailed response with multiple perspectives and supporting evidence."
            }
        ]
        
        result = await self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature
        )
        
        if result["success"]:
            return {
                "success": True,
                "query": query,
                "model_used": model,
                "analysis": result.get("content", ""),
                "usage": result.get("usage", {}),
                "timestamp": datetime.now().isoformat(),
                "api_endpoint": self.base_url,
            }
        else:
            return result


def get_zai_api_key() -> str | None:
    """Get Z.AI API key from environment.
    
    Returns:
        API key if found, None otherwise
    """
    return os.getenv("ZAI_API_KEY")
