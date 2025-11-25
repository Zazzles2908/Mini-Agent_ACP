"""MCP tool loader with real MCP client integration for both local and remote servers."""

import json
import logging
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .base import Tool, ToolResult
from .http_mcp_client import HTTPMCPClient

logger = logging.getLogger(__name__)


class MCPTool(Tool):
    """Wrapper for MCP tools."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        session: ClientSession,
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
    def parameters(self) -> dict[str, Any]:
        return self._parameters

    async def execute(self, **kwargs) -> ToolResult:
        """Execute MCP tool via the session."""
        try:
            result = await self._session.call_tool(self._name, arguments=kwargs)

            # MCP tool results are a list of content items
            content_parts = []
            for item in result.content:
                if hasattr(item, 'text'):
                    content_parts.append(item.text)
                else:
                    content_parts.append(str(item))

            content_str = '\n'.join(content_parts)

            is_error = result.isError if hasattr(result, 'isError') else False

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


class MCPServerConnection:
    """Manages connection to a single MCP server."""

    def __init__(self, name: str, command: str, args: list[str], env: dict[str, str] | None = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env or {}
        self.session: ClientSession | None = None
        self.exit_stack: AsyncExitStack | None = None
        self.tools: list[MCPTool] = []

    async def connect(self) -> bool:
        """Connect to the MCP server using proper async context management."""
        try:
            server_params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=self.env if self.env else None
            )

            # Use AsyncExitStack to properly manage multiple async context managers
            self.exit_stack = AsyncExitStack()
            
            # Enter stdio client context
            read_stream, write_stream = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            
            # Enter client session context
            session = await self.exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            self.session = session

            # Initialize the session
            await session.initialize()

            # List available tools with validation
            tools_list = await session.list_tools()
            
            # Validate that tools were successfully loaded
            if not hasattr(tools_list, 'tools'):
                raise Exception("Failed to retrieve tools list from server")
                
            if not tools_list.tools:
                logger.warning(f"No tools found from MCP server '{self.name}' - server may not be functioning properly")
                print(f"⚠️  Warning: No tools found from MCP server '{self.name}'")
                return False

            # Wrap each tool with validation
            for tool in tools_list.tools:
                # Validate tool has required properties
                if not hasattr(tool, 'name') or not tool.name:
                    logger.error(f"Tool missing required 'name' property from server '{self.name}'")
                    continue
                    
                if not hasattr(tool, 'description'):
                    logger.warning(f"Tool '{tool.name}' missing 'description' from server '{self.name}'")
                    
                # Convert MCP tool schema to our format
                parameters = tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                
                # Validate parameters if present
                if not isinstance(parameters, dict):
                    logger.warning(f"Tool '{tool.name}' has invalid parameters schema")
                    parameters = {}

                mcp_tool = MCPTool(
                    name=tool.name,
                    description=getattr(tool, 'description', ""),
                    parameters=parameters,
                    session=session
                )
                self.tools.append(mcp_tool)

            print(f"✓ Connected to MCP server '{self.name}' - loaded {len(self.tools)} tools")
            for tool in self.tools:
                desc = tool.description[:60] if len(tool.description) > 60 else tool.description
                print(f"  - {tool.name}: {desc}...")
            return True

        except Exception as e:
            print(f"✗ Failed to connect to MCP server '{self.name}': {e}")
            # Clean up exit stack if connection failed
            if self.exit_stack:
                await self.exit_stack.aclose()
                self.exit_stack = None
            import traceback
            traceback.print_exc()
            return False

    async def disconnect(self):
        """Properly disconnect from the MCP server."""
        if self.exit_stack:
            # AsyncExitStack handles all cleanup properly
            await self.exit_stack.aclose()
            self.exit_stack = None
            self.session = None


# Global connections registry
_mcp_connections: list[MCPServerConnection] = []


async def load_mcp_tools_async(config_path: str = "mini_agent/config/.mcp.json") -> list[Tool]:
    """
    Load MCP tools from config file.

    This function:
    1. Reads the MCP config file
    2. Identifies server type (local vs remote)
    3. Connects to each server using appropriate client
    4. Fetches tool definitions
    5. Wraps them as Tool objects

    Args:
        config_path: Path to MCP configuration file (default: "mcp.json")

    Returns:
        List of Tool objects representing MCP tools
    """
    global _mcp_connections

    config_file = Path(config_path)

    if not config_file.exists():
        print(f"MCP config not found: {config_path}")
        return []

    try:
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)

        mcp_servers = config.get("mcpServers", {})

        if not mcp_servers:
            print("No MCP servers configured")
            return []

        all_tools = []

        # Connect to each enabled server
        for server_name, server_config in mcp_servers.items():
            if server_config.get("disabled", False):
                print(f"Skipping disabled server: {server_name}")
                continue

            try:
                # Determine if this is a remote server
                if (server_config.get("command") == "remote" and server_config.get("url")) or \
                   (server_config.get("type") == "http" and server_config.get("url")) or \
                   (server_config.get("type") == "sse" and server_config.get("url")) or \
                   (server_config.get("type") == "streamable-http" and server_config.get("url")):
                    # Remote server configuration
                    print(f"Connecting to remote MCP server: {server_name}")
                    import os
                    
                    # Handle environment variable substitution in headers and URL
                    config_headers = server_config.get("headers", {})
                    processed_headers = {}
                    for key, value in config_headers.items():
                        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                            env_var = value[2:-1]  # Remove ${ and }
                            processed_headers[key] = os.environ.get(env_var, value)
                        else:
                            processed_headers[key] = value
                    
                    # Handle environment variable substitution in URL
                    url = server_config.get("url", "")
                    if url.startswith("${") and url.endswith("}"):
                        env_var = url[2:-1]
                        url = os.environ.get(env_var, url)
                    
                    http_client = HTTPMCPClient({
                        "name": server_name,
                        "url": url,
                        "headers": processed_headers,
                        "timeout": server_config.get("timeout", 30),
                        "retry": server_config.get("retry", {"max_retries": 3, "initial_delay": 1.0})
                    })
                    
                    tools = await http_client.connect()
                    all_tools.extend(tools)
                    
                else:
                    # Local server configuration (stdio-based)
                    command = server_config.get("command")
                    args = server_config.get("args", [])
                    env = server_config.get("env", {})

                    if not command:
                        print(f"No command specified for server: {server_name}")
                        continue

                    # Validate that the command exists
                    import shutil
                    if not shutil.which(command):
                        print(f"✗ Command '{command}' not found in PATH for server: {server_name}")
                        logger.error(f"Command '{command}' not found for MCP server '{server_name}'")
                        continue

                    # Validate that the script file exists if it's a Python script
                    if command == "python" and args:
                        script_path = Path(args[0])
                        if not script_path.exists():
                            print(f"✗ Script file not found: {script_path} for server: {server_name}")
                            logger.error(f"Script file not found: {script_path} for MCP server '{server_name}'")
                            continue

                    print(f"Starting local MCP server: {server_name}")
                    connection = MCPServerConnection(server_name, command, args, env)
                    success = await connection.connect()

                    if success:
                        # Validate that tools were actually loaded
                        if not connection.tools:
                            print(f"✗ No tools loaded from server: {server_name}")
                            logger.warning(f"No tools loaded from MCP server '{server_name}'")
                            await connection.disconnect()
                            continue
                            
                        _mcp_connections.append(connection)
                        all_tools.extend(connection.tools)
                        print(f"✓ Successfully loaded {len(connection.tools)} tools from '{server_name}'")
                    else:
                        print(f"✗ Failed to establish connection to server: {server_name}")

            except Exception as e:
                logger.error(f"Failed to connect to MCP server '{server_name}': {e}")
                print(f"✗ Failed to connect to MCP server '{server_name}': {e}")
                continue

        print(f"\nTotal MCP tools loaded: {len(all_tools)}")
        
        # Provide summary of loading results
        if all_tools:
            print("\n=== MCP Server Loading Summary ===")
            successful_servers = []
            failed_servers = []
            
            for server_name, server_config in mcp_servers.items():
                if server_config.get("disabled", False):
                    continue
                    
                # Check if this server contributed tools
                server_tools = [tool for tool in all_tools if hasattr(tool, '_session') and 
                               any(conn.name == server_name for conn in _mcp_connections)]
                
                if server_tools:
                    successful_servers.append((server_name, len(server_tools)))
                else:
                    failed_servers.append(server_name)
            
            if successful_servers:
                print("✅ Successfully loaded tools from:")
                for server_name, tool_count in successful_servers:
                    print(f"   - {server_name}: {tool_count} tools")
            
            if failed_servers:
                print("❌ Failed to load tools from:")
                for server_name in failed_servers:
                    print(f"   - {server_name}")
                print(f"\nTotal failed servers: {len(failed_servers)}")

        return all_tools

    except Exception as e:
        print(f"Error loading MCP config: {e}")
        import traceback
        traceback.print_exc()
        return []


async def cleanup_mcp_connections():
    """Clean up all MCP connections."""
    global _mcp_connections
    for connection in _mcp_connections:
        await connection.disconnect()
    _mcp_connections.clear()
