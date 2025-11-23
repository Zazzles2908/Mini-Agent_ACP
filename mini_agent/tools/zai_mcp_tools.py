import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import logging

# MCP Protocol implementation for Z.AI servers
class ZAIMCPTool:
    """
    Z.AI MCP Tools - Using FREE Lite plan quotas
    Web Search: 100 searches included
    Web Reader: 100 readers included
    """
    
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/mcp"
        self.timeout = timeout
        self.usage_log = {"searches": 0, "readers": 0}
        
        # MCP server endpoints (FREE with Lite plan)
        self.servers = {
            "web_search": f"{self.base_url}/web_search_prime/mcp",
            "web_reader": f"{self.base_url}/web_reader/mcp"
        }
        
        # Headers for MCP protocol
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def web_search_prime(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """
        Web Search using MCP protocol - FREE with Lite plan
        Returns: Search results with titles, URLs, summaries
        """
        try:
            # MCP protocol request format
            mcp_request = {
                "method": "tools/call",
                "params": {
                    "name": "webSearchPrime",
                    "arguments": {
                        "query": query,
                        "max_results": min(max_results, 5),  # Limit to 5 to save quota
                        "format": "detailed"
                    }
                }
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    self.servers["web_search"],
                    headers=self.headers,
                    json=mcp_request
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.usage_log["searches"] += 1
                        return {"status": "success", "data": result, "usage": self.usage_log}
                    else:
                        error_text = await response.text()
                        return {"status": "error", "error": f"HTTP {response.status}: {error_text}"}
                        
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def web_reader(self, url: str, extract_links: bool = True) -> Dict[str, Any]:
        """
        Web Reader using MCP protocol - FREE with Lite plan
        Returns: Page content, title, metadata, links
        """
        try:
            # MCP protocol request format
            mcp_request = {
                "method": "tools/call", 
                "params": {
                    "name": "webReader",
                    "arguments": {
                        "url": url,
                        "extract_images": False,  # Save bandwidth
                        "extract_links": extract_links,
                        "format": "structured"
                    }
                }
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    self.servers["web_reader"],
                    headers=self.headers,
                    json=mcp_request
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.usage_log["readers"] += 1
                        return {"status": "success", "data": result, "usage": self.usage_log}
                    else:
                        error_text = await response.text()
                        return {"status": "error", "error": f"HTTP {response.status}: {error_text}"}
                        
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_usage_summary(self) -> Dict[str, int]:
        """Get current quota usage"""
        return {
            "searches_used": self.usage_log["searches"],
            "readers_used": self.usage_log["readers"], 
            "searches_remaining": 100 - self.usage_log["searches"],
            "readers_remaining": 100 - self.usage_log["readers"],
            "plan": "Lite (FREE quotas)"
        }

# Utility functions for integration
async def create_mcp_tool(api_key: str) -> ZAIMCPTool:
    """Create configured MCP tool instance"""
    return ZAIMCPTool(api_key=api_key)

async def search_and_read(query: str, api_key: str, max_results: int = 2) -> Dict[str, Any]:
    """
    Combined search and read using MCP protocol
    Uses FREE quotas from Lite plan
    """
    tool = await create_mcp_tool(api_key)
    
    # Step 1: Search for relevant pages
    search_result = await tool.web_search_prime(query, max_results)
    
    if search_result["status"] != "success":
        return {"status": "error", "error": f"Search failed: {search_result['error']}"}
    
    # Extract URLs from search results and read first result
    urls = []
    try:
        data = search_result["data"]
        if "results" in data:
            for result in data["results"][:1]:  # Read only first result
                if "url" in result:
                    urls.append(result["url"])
    except:
        pass
    
    # Step 2: Read content from first URL
    reader_result = None
    if urls:
        reader_result = await tool.web_reader(urls[0])
    
    return {
        "search": search_result,
        "reader": reader_result,
        "usage": tool.get_usage_summary()
    }

if __name__ == "__main__":
    # Test usage
    import os
    api_key = os.getenv("ZAI_API_KEY")
    if api_key:
        import asyncio
        
        async def test():
            tool = await create_mcp_tool(api_key)
            result = await search_and_read("MiniMax AI capabilities", api_key)
            print(json.dumps(result, indent=2))
        
        asyncio.run(test())
    else:
        print("ZAI_API_KEY environment variable not set")