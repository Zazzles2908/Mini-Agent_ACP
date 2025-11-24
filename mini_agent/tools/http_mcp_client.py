#!/usr/bin/env python3
"""
HTTP-based MCP Client for remote MCP servers.

This module provides support for MCP servers that run over HTTP (remote servers)
like Z.AI's MCP endpoints. It implements the MCP protocol over HTTP/JSON-RPC.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

from .base import Tool, ToolResult

logger = logging.getLogger(__name__)


class HTTPMCPTool(Tool):
    """Tool wrapper for HTTP MCP tools."""
    
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        session: 'HTTPMCPClientSession'
    ):
        self._name = name
        self._description = description
        self._parameters = parameters
        self._session = session

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters(self) -> Dict[str, Any]:
        return self._parameters

    async def execute(self, **kwargs) -> ToolResult:
        """Execute MCP tool via HTTP session."""
        try:
            result = await self._session.call_tool(self._name, arguments=kwargs)

            # MCP tool results are a list of content items
            content_parts = []
            for item in result.get('content', []):
                if isinstance(item, dict):
                    if 'text' in item:
                        content_parts.append(item['text'])
                    else:
                        content_parts.append(str(item))
                else:
                    content_parts.append(str(item))

            content_str = '\n'.join(content_parts)
            is_error = result.get('isError', False)

            return ToolResult(
                success=not is_error,
                content=content_str,
                error=None if not is_error else "Tool returned error"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"MCP tool execution failed: {str(e)}"
            )


class HTTPMCPClientSession:
    """HTTP-based MCP client session for Z.AI's custom MCP protocol."""
    
    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str],
        timeout: int = 30,
        retry_config: Optional[Dict[str, Any]] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.headers = headers
        self.timeout = timeout
        self.retry_config = retry_config or {"max_retries": 3, "initial_delay": 1.0}
        
        # Ensure we have a session
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp is required for HTTP MCP client")
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.tools: List[Dict[str, Any]] = []
        
    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _parse_sse_response(self, response) -> List[Dict[str, Any]]:
        """Parse Server-Sent Events response from Z.AI MCP endpoint."""
        messages = []
        async for line in response.content:
            try:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith('data: '):
                    # Remove 'data: ' prefix and parse JSON
                    data = json.loads(line_str[6:])
                    messages.append(data)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.debug(f"Skipping invalid SSE line: {e}")
                continue
        return messages
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic and SSE support."""
        if not self.session:
            raise RuntimeError("Session not initialized")
            
        url = urljoin(self.base_url + '/', endpoint)
        
        for attempt in range(self.retry_config["max_retries"] + 1):
            try:
                async with self.session.request(method, url, json=data) as response:
                    if response.status == 200:
                        # Check content type to determine parsing strategy
                        content_type = response.headers.get('Content-Type', '')
                        
                        if 'text/event-stream' in content_type:
                            # Parse Server-Sent Events
                            logger.debug(f"Parsing SSE response from {url}")
                            messages = await self._parse_sse_response(response)
                            
                            # Extract actual result from SSE stream
                            if messages:
                                # Return the last message which typically contains the result
                                for msg in reversed(messages):
                                    if 'result' in msg:
                                        return msg['result']
                                    elif 'content' in msg:
                                        return msg
                                # Fallback: return last message
                                return messages[-1]
                            else:
                                return {"content": [], "isError": True, "error": "Empty SSE response"}
                        else:
                            # Standard JSON response
                            result = await response.json()
                            return result
                    else:
                        text = await response.text()
                        logger.warning(f"HTTP {response.status} for {method} {url}: {text}")
                        
                        # Don't retry on client errors (4xx)
                        if 400 <= response.status < 500:
                            break
                            
            except Exception as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                
                if attempt < self.retry_config["max_retries"]:
                    delay = self.retry_config["initial_delay"] * (2 ** attempt)
                    await asyncio.sleep(delay)
                else:
                    raise
                    
        raise RuntimeError(f"HTTP request failed after {self.retry_config['max_retries']} retries")
    
    async def initialize(self) -> bool:
        """Initialize the MCP session (Z.AI style - just test connectivity)."""
        try:
            # For Z.AI, we test connectivity by calling the endpoint with an empty request
            result = await self._make_request('POST', '', {})
            logger.info(f"MCP session initialized: {result}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MCP session: {e}")
            return False
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools using Z.AI's custom format."""
        try:
            # For Z.AI, we define the tools we know should be available
            # based on the endpoint type
            if "web_search" in self.base_url:
                self.tools = [{
                    "name": "webSearchPrime",
                    "description": "Z.AI web search using MCP protocol with FREE quota",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query or research question"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results (1-5)",
                                "minimum": 1,
                                "maximum": 5,
                                "default": 3
                            },
                            "format": {
                                "type": "string",
                                "description": "Response format",
                                "enum": ["detailed", "summary"],
                                "default": "detailed"
                            }
                        },
                        "required": ["query"]
                    }
                }]
            elif "web_reader" in self.base_url:
                self.tools = [{
                    "name": "webReader",
                    "description": "Z.AI web content reader using MCP protocol with FREE quota",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to read content from"
                            },
                            "extract_links": {
                                "type": "boolean",
                                "description": "Extract links from the content",
                                "default": True
                            },
                            "format": {
                                "type": "string",
                                "description": "Response format",
                                "enum": ["markdown", "text", "html"],
                                "default": "markdown"
                            }
                        },
                        "required": ["url"]
                    }
                }]
            else:
                self.tools = []
                
            logger.info(f"Listed {len(self.tools)} tools from {self.base_url}")
            return self.tools
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool using Z.AI's custom MCP format."""
        try:
            # Z.AI MCP format
            data = {
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            result = await self._make_request('POST', '', data)
            logger.debug(f"Tool {tool_name} called successfully")
            return result
        except Exception as e:
            logger.error(f"Failed to call tool {tool_name}: {e}")
            raise


class HTTPMCPClient:
    """HTTP-based MCP client for connecting to remote MCP servers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize HTTP MCP client.
        
        Args:
            config: Server configuration with 'url', 'headers', etc.
        """
        self.name = config.get('name', 'unknown')
        self.url = config.get('url')
        self.headers = config.get('headers', {})
        self.timeout = config.get('timeout', 30)
        self.retry_config = config.get('retry', {"max_retries": 3, "initial_delay": 1.0})
        
        if not self.url:
            raise ValueError("HTTP MCP client requires 'url' in config")
    
    async def connect(self) -> List[Tool]:
        """Connect to remote MCP server and return tools."""
        if not AIOHTTP_AVAILABLE:
            logger.error("aiohttp not available - cannot connect to HTTP MCP server")
            return []
            
        try:
            async with HTTPMCPClientSession(
                self.url, 
                self.headers, 
                self.timeout, 
                self.retry_config
            ) as session:
                
                # Initialize session
                if not await session.initialize():
                    logger.error(f"Failed to initialize MCP session for {self.name}")
                    return []
                
                # List tools
                tools_data = await session.list_tools()
                if not tools_data:
                    logger.warning(f"No tools found for MCP server {self.name}")
                    return []
                
                # Wrap tools
                wrapped_tools = []
                for tool_data in tools_data:
                    tool = HTTPMCPTool(
                        name=tool_data.get('name', ''),
                        description=tool_data.get('description', ''),
                        parameters=tool_data.get('inputSchema', {}),
                        session=session
                    )
                    wrapped_tools.append(tool)
                
                logger.info(f"✓ Connected to remote MCP server '{self.name}' - loaded {len(wrapped_tools)} tools")
                for tool in wrapped_tools:
                    desc = tool.description[:60] if len(tool.description) > 60 else tool.description
                    print(f"  - {tool.name}: {desc}...")
                
                return wrapped_tools
                
        except Exception as e:
            logger.error(f"Failed to connect to remote MCP server '{self.name}': {e}")
            import traceback
            traceback.print_exc()
            return []


# Import asyncio for the sleep function
import asyncio