#!/usr/bin/env python3
"""
Z.AI MCP Server - Wraps the working Z.AI web tool for MCP protocol compliance
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from mini_agent.tools.zai_web_tool import ZAIWebTool
except ImportError:
    # Fallback if import fails
    sys.path.insert(0, str(project_root / "mini_agent"))
    from tools.zai_web_tool import ZAIWebTool

logger = logging.getLogger(__name__)

class ZAIMCPServer:
    """MCP Server wrapper for Z.AI web tools."""
    
    def __init__(self):
        self.tool = ZAIWebTool()
        self.tools = {
            "zai_web_search": {
                "name": "zai_web_search",
                "description": "Smart Z.AI web search using working Direct API approach with GLM models",
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
        
        if not self.tool.available:
            logger.warning("Z.AI tool not available - server will not function properly")
    
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
                    "version": "1.0.0"
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": list(self.tools.values())
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "zai_web_search":
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
        """Handle web search requests."""
        
        try:
            # Execute search using the working tool
            result = await self.tool.execute(
                query=arguments.get("query", ""),
                max_results=arguments.get("max_results", 3),
                include_reader=arguments.get("include_reader", False),
                method="auto"
            )
            
            if result.success:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": result.content
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Search failed: {result.error}"
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
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("zai-mcp-server")
    
    server = ZAIMCPServer()
    logger.info("Z.AI MCP Server starting...")
    
    # MCP server communication over stdin/stdout
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            logger.debug(f"Received request: {request.get('method')}")
            
            # Handle request
            response = await server.handle_request(request)
            
            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(f"Server error: {e}")
            # Send error response
            error_response = {
                "content": [
                    {
                        "type": "text",
                        "text": f"Server error: {str(e)}"
                    }
                ],
                "isError": True
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())