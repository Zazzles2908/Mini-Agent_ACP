#!/usr/bin/env python3
"""
Z.AI MCP Server - Direct implementation using Z.AI Direct API
This is a simplified, working implementation of a Z.AI MCP server.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Configure logging (redirect to stderr to avoid MCP protocol interference)
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("zai-mcp-server")

class ZAIMCPServer:
    """Simple Z.AI MCP Server using Direct API."""
    
    def __init__(self):
        self.api_key = os.getenv('ZAI_API_KEY')
        if not self.api_key:
            self.available = False
        else:
            self.available = True
        
        self.tools = {
            "web_search": {
                "name": "web_search",
                "description": "Smart Z.AI web search using Direct API with GLM models. Search for current information, research topics, or fact-check with source citations.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query or research question"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results (1-5, default 3)",
                            "minimum": 1,
                            "maximum": 5,
                            "default": 3
                        },
                        "include_reader": {
                            "type": "boolean",
                            "description": "Also fetch content from top result URLs",
                            "default": False
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol requests."""
        
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return {
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "zai-mcp-server",
                    "version": "2.0.0"
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": list(self.tools.values())
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "web_search":
                return await self._handle_web_search(arguments)
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unknown tool: {tool_name}"
                        }
                    ],
                    "isError": True
                }
        
        else:
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Unknown method: {method}"
                    }
                ],
                "isError": True
            }
    
    async def _handle_web_search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle web search requests using Direct API."""
        
        if not self.available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Z.AI MCP Server not available - ZAI_API_KEY not configured"
                    }
                ],
                "isError": True
            }
        
        try:
            import aiohttp
            
            query = arguments.get("query", "")
            max_results = min(5, max(1, arguments.get("max_results", 3)))
            include_reader = arguments.get("include_reader", False)
            
            if not query:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Query parameter is required"
                        }
                    ],
                    "isError": True
                }
            
            # Direct API call to Z.AI
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
                    "https://api.z.ai/api/coding/paas/v4/web_search",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Format the response
                        content_parts = [
                            f"**🔍 Z.AI Web Search Results**",
                            f"**Method:** Direct API",
                            "",
                            f"**Query:** {query}",
                            f"**Results:** {max_results}",
                            "",
                            "**Raw Data:**",
                            "```json",
                            json.dumps(result, indent=2),
                            "```"
                        ]
                        
                        return {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "\n".join(content_parts)
                                }
                            ]
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Search failed: HTTP {response.status} - {error_text}"
                                }
                            ],
                            "isError": True
                        }
                        
        except ImportError:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "aiohttp library not available for web search"
                    }
                ],
                "isError": True
            }
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Search error: {str(e)}"
                    }
                ],
                "isError": True
            }

async def main():
    """Main MCP server loop."""
    
    server = ZAIMCPServer()
    
    # MCP server communication over stdin/stdout
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            
            # Handle request
            response_content = await server.handle_request(request)
            
            # Get the request ID, handle None case
            request_id = request.get("id")
            if request_id is None:
                # For notifications or invalid requests, use a default ID
                request_id = 1
            
            # Format as proper JSON-RPC response
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": response_content
            }
            
            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            # Send JSON-RPC parse error (use default ID)
            error_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
            continue
        except Exception as e:
            # Send proper JSON-RPC error response
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())