#!/usr/bin/env python3
"""
Enhanced Z.AI Web Tool with Token Truncation Detection
Improves upon existing zai_web_tool.py with better truncation handling
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

from .base import Tool, ToolResult
from .token_truncation_detector import ZAIResponseEnhancer, ZAITokenTruncationDetector


logger = logging.getLogger(__name__)


class EnhancedZAIWebTool(Tool):
    """
    Enhanced Z.AI web search tool with token truncation detection and handling.
    
    This tool improves upon the existing ZAIWebTool by:
    1. Detecting token truncation in responses
    2. Providing actionable warnings to users
    3. Suggesting query optimizations
    4. Enhanced error handling for truncated responses
    """
    
    def __init__(self, api_key: str | None = None):
        """Initialize enhanced Z.AI web tool with truncation detection."""
        
        # API key setup
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        if not self.api_key:
            logger.warning("No Z.AI API key found. Web tools will not be available.")
            self.available = False
            return
        
        # Usage tracking
        self.mcp_searches_used = 0
        self.mcp_readers_used = 0
        self.mcp_quota_limit = 100  # FREE quota per day
        
        # Status tracking
        self.mcp_available = None  # Will test on first use
        self.direct_available = None  # Will test if protected
        
        # Truncation detection
        self.truncation_enhancer = ZAIResponseEnhancer()
        self.detector = ZAITokenTruncationDetector()
        
        # MCP endpoints (FREE quotas)
        self.mcp_search_endpoint = "https://api.z.ai/api/mcp/web_search_prime/mcp"
        self.mcp_reader_endpoint = "https://api.z.ai/api/mcp/web_reader_prime/mcp"
        
        # Direct API endpoints (paid)
        self.direct_base_url = "https://api.z.ai/api/coding/paas/v4"
        
        # Initialize successfully
        self.available = True
        logger.info("Enhanced Z.AI Web Tool initialized with truncation detection")
    
    @property
    def name(self) -> str:
        return "enhanced_zai_web_search"
    
    @property
    def description(self) -> str:
        return (
            "Enhanced Z.AI web search with token truncation detection and query optimization. "
            "Uses FREE MCP quotas (100 searches included) with fallback to paid Direct API. "
            "Detects response truncation and provides actionable optimization suggestions. "
            "Perfect for research, fact-checking, and current information gathering."
        )
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query or research question (use concise language for better results)",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (1-5, default 3)",
                    "minimum": 1,
                    "maximum": 5,
                    "default": 3,
                },
                "method": {
                    "type": "string", 
                    "description": "Preferred method: 'auto' (default), 'mcp', or 'direct'",
                    "enum": ["auto", "mcp", "direct"],
                    "default": "auto"
                },
                "include_reader": {
                    "type": "boolean",
                    "description": "Also fetch content from top result URLs (uses reader quota)",
                    "default": False,
                },
                "detect_truncation": {
                    "type": "boolean",
                    "description": "Enable token truncation detection and optimization suggestions",
                    "default": True
                }
            },
            "required": ["query"],
        }
    
    async def execute(self, **kwargs) -> ToolResult:
        """Execute enhanced web search with truncation detection."""
        
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Enhanced Z.AI web tool not available - no API key configured"
            )
        
        # Extract parameters
        query = kwargs.get("query", "")
        max_results = kwargs.get("max_results", 3)
        method = kwargs.get("method", "auto")
        include_reader = kwargs.get("include_reader", False)
        detect_truncation = kwargs.get("detect_truncation", True)
        
        if not query:
            return ToolResult(
                success=False,
                content="",
                error="Query parameter is required"
            )
        
        # Validate inputs
        max_results = max(1, min(5, max_results))
        
        # Try search based on preferred method
        search_result = None
        search_method_used = None
        
        if method == "mcp" or (method == "auto" and self.mcp_available is not False):
            search_result, search_method_used = await self._try_mcp_search(query, max_results, detect_truncation)
        
        if not search_result and (method == "direct" or method == "auto"):
            # Check credit protection before trying direct API
            from mini_agent.utils.credit_protection import check_zai_protection
            if check_zai_protection():
                search_result, search_method_used = await self._try_direct_search(query, max_results, detect_truncation)
            else:
                logger.info("Direct API blocked by credit protection")
        
        if not search_result:
            return ToolResult(
                success=False,
                content="",
                error="All Z.AI methods unavailable (MCP exhausted or disabled, Direct API protected)"
            )
        
        # Handle truncation detection if enabled
        if detect_truncation and search_result.get("success") and "enhanced_data" in search_result:
            enhanced_data = search_result["enhanced_data"]
            truncation_analysis = enhanced_data.get("truncation_analysis", {})
            
            if truncation_analysis.get("is_truncated", False):
                # Add truncation warning to the response
                warnings = enhanced_data.get("warnings", [])
                if warnings:
                    # Insert truncation warning at the beginning
                    content = search_result.get("content", "")
                    warning_text = f"\n\n{warnings[0]}\n\n"
                    search_result["content"] = warning_text + content
        
        return ToolResult(
            success=search_result.get("success", False),
            content=search_result.get("content", ""),
            error=search_result.get("error")
        )
    
    async def _try_mcp_search(self, query: str, max_results: int, detect_truncation: bool) -> tuple[Dict[str, Any], str]:
        """Try MCP search with optional truncation detection."""
        
        # Check quota
        if self.mcp_searches_used >= self.mcp_quota_limit:
            return {"success": False, "error": f"MCP quota exceeded ({self.mcp_searches_used}/{self.mcp_quota_limit})"}, "mcp"
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed")
            
            # MCP protocol request format
            mcp_request = {
                "method": "tools/call",
                "params": {
                    "name": "webSearchPrime",
                    "arguments": {
                        "query": query,
                        "max_results": min(max_results, 5),
                        "format": "detailed"
                    }
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.mcp_search_endpoint,
                    headers=headers,
                    json=mcp_request,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.mcp_searches_used += 1
                        
                        base_result = {
                            "success": True,
                            "data": result,
                            "usage": f"MCP searches: {self.mcp_searches_used}/{self.mcp_quota_limit}",
                            "method": "mcp"
                        }
                        
                        # Add truncation detection if enabled
                        if detect_truncation:
                            enhanced_response = self.truncation_enhancer.enhance_response(result, query)
                            base_result["enhanced_data"] = enhanced_response
                            base_result["content"] = self._format_mcp_content(result)
                        else:
                            base_result["content"] = self._format_mcp_content(result)
                        
                        return base_result, "mcp"
                    else:
                        error_text = await response.text()
                        self.mcp_available = False
                        return {"success": False, "error": f"MCP error {response.status}: {error_text}"}, "mcp"
                        
        except Exception as e:
            self.mcp_available = False
            return {"success": False, "error": f"MCP search failed: {str(e)}"}, "mcp"
    
    async def _try_direct_search(self, query: str, max_results: int, detect_truncation: bool) -> tuple[Dict[str, Any], str]:
        """Try Direct API search with optional truncation detection."""
        
        try:
            if not AIOHTTP_AVAILABLE:
                raise ImportError("aiohttp is not installed")
            
            payload = {
                "search_engine": "search_prime",
                "search_query": query,
                "count": max_results,
                "search_recency_filter": "noLimit"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept-Language": "en-US,en"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.direct_base_url}/web_search",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        base_result = {
                            "success": True,
                            "data": result,
                            "usage": "Direct API (paid)",
                            "method": "direct"
                        }
                        
                        # Add truncation detection if enabled
                        if detect_truncation:
                            enhanced_response = self.truncation_enhancer.enhance_response(result, query)
                            base_result["enhanced_data"] = enhanced_response
                            base_result["content"] = self._format_direct_content(result)
                        else:
                            base_result["content"] = self._format_direct_content(result)
                        
                        return base_result, "direct"
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": f"Direct API error {response.status}: {error_text}"}, "direct"
                        
        except Exception as e:
            return {"success": False, "error": f"Direct search failed: {str(e)}"}, "direct"
    
    def _format_mcp_content(self, result: Dict[str, Any]) -> str:
        """Format MCP response content for display."""
        return f"**MCP Response:**\n\n{json.dumps(result, indent=2)}"
    
    def _format_direct_content(self, result: Dict[str, Any]) -> str:
        """Format direct API response content for display."""
        # Extract main content from GLM-style responses
        if "choices" in result:
            choices = result["choices"]
            if choices and len(choices) > 0:
                content = choices[0].get("message", {}).get("content", "")
                if content:
                    return f"**Direct API Response:**\n\n{content}"
        
        return f"**Direct API Response:**\n\n{json.dumps(result, indent=2)}"
    
    async def detect_response_truncation(self, response_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Detect truncation in a response and provide optimization suggestions."""
        
        truncation_result = self.detector.detect_truncation(response_data)
        suggestions = self.truncation_enhancer.suggest_optimization(truncation_result, query)
        
        return {
            "truncation_detected": truncation_result.is_truncated,
            "truncation_type": truncation_result.truncation_type.value,
            "severity": truncation_result.severity,
            "message": truncation_result.truncation_message,
            "recommendations": truncation_result.recommendations,
            "optimization_suggestions": suggestions
        }


def create_enhanced_zai_web_tool(api_key: str | None = None) -> EnhancedZAIWebTool:
    """Factory function to create enhanced Z.AI web tool."""
    return EnhancedZAIWebTool(api_key)


# Example usage
async def example_enhanced_usage():
    """Example of how to use the enhanced Z.AI web tool."""
    
    tool = EnhancedZAIWebTool()
    
    # Search with truncation detection enabled (default)
    result = await tool.execute(
        query="Explain Python programming in detail with examples",
        max_results=3,
        detect_truncation=True
    )
    
    print("Enhanced Search Result:")
    print("=" * 50)
    print(result.content)
    
    if result.success:
        print("\n\nTruncation Analysis:")
        # Additional analysis can be done here
    
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_enhanced_usage())
