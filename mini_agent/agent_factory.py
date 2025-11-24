"""
Production-Grade Agent Factory
Auto-configures agent with tools and settings from configuration system
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from .agent import Agent
from .config import get_config
from .llm.llm_wrapper import LLMClient, create_llm_client
from .tools.mcp_loader import load_mcp_tools_async
from .tools.file_tools import ReadTool, WriteTool, EditTool
from .tools.bash_tool import BashTool
from .logger import AgentLogger

logger = logging.getLogger(__name__)


class AgentFactory:
    """
    Production-grade agent factory that automatically configures everything
    based on the configuration system.
    """
    
    def __init__(self):
        """Initialize agent factory with configuration"""
        self.config = get_config()
        self.logger = AgentLogger()
        
    async def create_agent(
        self,
        system_prompt: Optional[str] = None,
        custom_tools: Optional[List] = None,
        workspace_dir: Optional[str] = None,
        max_steps: Optional[int] = None,
        auto_load_tools: bool = True,
        **kwargs
    ) -> Agent:
        """
        Create a fully configured production agent.
        
        Args:
            system_prompt: Custom system prompt (auto-loaded if not provided)
            custom_tools: Additional tools to include
            workspace_dir: Custom workspace directory
            max_steps: Maximum steps for agent execution
            auto_load_tools: Whether to automatically load configured tools
            
        Returns:
            Fully configured Agent instance
        """
        try:
            # 1. Load configuration
            logger.info("🚀 Creating production-grade agent...")
            
            # 2. Create LLM client with auto-configuration
            try:
                llm_client = create_llm_client(**kwargs)
                logger.info(f"✅ LLM Client: {llm_client.provider} ({llm_client.model})")
                if not llm_client.api_key:
                    logger.warning("⚠️  API key not provided. Agent will work with limited LLM functionality.")
            except Exception as e:
                logger.warning(f"⚠️  Failed to create LLM client: {e}")
                # Create a simple placeholder client for when API key is missing
                from .llm.minimax_client import MinimaxClient
                llm_client = MinimaxClient(api_key="placeholder", model="no-llm-mode")
                llm_client._api_key = None  # Mark as no-LLM mode
                logger.warning("⚠️  Running in no-LLM mode. Add MINIMAX_API_KEY to enable full functionality.")
            
            # 3. Load tools
            tools = []
            if auto_load_tools:
                tools = await self._load_tools()
                logger.info(f"✅ Loaded {len(tools)} tools")
            
            # 4. Add custom tools if provided
            if custom_tools:
                tools.extend(custom_tools)
                logger.info(f"✅ Added {len(custom_tools)} custom tools")
            
            # 5. Get system prompt
            if not system_prompt:
                system_prompt = self._load_system_prompt()
            
            # 6. Get configuration values
            workspace = workspace_dir or self.config.get("workspace.directory", default="./workspace")
            steps = max_steps or self.config.get("app.max_steps", default=50)
            token_limit = self.config.get("llm.context.token_limit", default=200000)
            
            # 7. Create the agent
            agent = Agent(
                llm_client=llm_client,
                system_prompt=system_prompt,
                tools=tools,
                max_steps=steps,
                workspace_dir=workspace,
                token_limit=token_limit,
            )
            
            logger.info(f"✅ Agent created successfully - Max steps: {steps}, Workspace: {workspace}")
            return agent
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent: {e}")
            raise
    
    async def _load_tools(self) -> List:
        """Load tools based on configuration"""
        tools = []
        config = self.config
        
        # Core tools (always enabled)
        if config.get("tools.enable_file_tools", default=True):
            tools.extend([
                ReadTool(),
                WriteTool(), 
                EditTool(),
            ])
            logger.debug("📁 Loaded file tools")
        
        if config.get("tools.enable_bash_tools", default=True):
            tools.append(BashTool())
            logger.debug("💻 Loaded bash tools")
        
        # MCP tools
        if config.get("tools.enable_mcp_tools", default=True):
            try:
                mcp_tools = await load_mcp_tools_async()
                tools.extend(mcp_tools)
                logger.debug(f"🔌 Loaded {len(mcp_tools)} MCP tools")
            except Exception as e:
                logger.warning(f"⚠️  Failed to load MCP tools: {e}")
        
        # Z.AI web tools
        if config.get("tools.enable_zai_web_search", default=True):
            try:
                from .tools.zai_web_tool import ZAIWebTool
                zai_tool = ZAIWebTool()
                tools.append(zai_tool)
                logger.debug("🌐 Loaded Z.AI web tools")
            except Exception as e:
                logger.warning(f"⚠️  Failed to load Z.AI tools: {e}")
        
        return tools
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from configuration or file"""
        # Try to get from config
        prompt = self.config.get("app.system_prompt")
        
        if prompt:
            return prompt
        
        # Try to load from file
        prompt_file = Path("mini_agent/config/system_prompt.md")
        if prompt_file.exists():
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"⚠️  Failed to load system prompt from file: {e}")
        
        # Default system prompt
        return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt"""
        return """You are a production-grade AI agent assistant.

You have access to a comprehensive toolkit of tools and capabilities that you can use to help users with a wide variety of tasks.

## Your Capabilities

### Core Tools
- **File Operations**: Read, write, and edit files in the workspace
- **Shell Commands**: Execute bash commands and scripts
- **Web Search**: Search the internet using Z.AI (with FREE quotas)
- **Web Reading**: Extract and read content from web pages
- **Code Analysis**: Generate, analyze, review, and plan code projects
- **Knowledge Graph**: Persistent memory and relationship tracking
- **Version Control**: Git operations and repository management

### Key Principles
1. **Be helpful and thorough** - Provide comprehensive assistance
2. **Use tools effectively** - Leverage the full toolkit when appropriate
3. **Think step by step** - Break down complex tasks systematically
4. **Stay within limits** - Respect configured time and step limits
5. **Communicate clearly** - Explain your reasoning and approach

## Guidelines

### Tool Usage
- Use tools when they will significantly improve your response
- For file operations, read existing files before editing them
- For web searches, be specific in your queries for better results
- For code tasks, use the coding assistance tools when available

### Error Handling
- If a tool fails, try alternative approaches
- Provide helpful error messages when things go wrong
- Use retry logic for transient failures
- Document any limitations or workarounds you discover

### Communication Style
- Be direct and helpful
- Explain your approach when tackling complex problems
- Provide code examples and explanations when relevant
- Ask clarifying questions when requirements are unclear

Remember: You are a production-grade assistant designed to help users accomplish their goals effectively and efficiently."""
    
    def get_agent_info(self, agent: Agent) -> Dict[str, Any]:
        """Get comprehensive information about a created agent"""
        return {
            "agent_type": "production-grade",
            "llm_info": agent.llm.get_model_info(),
            "configuration": {
                "max_steps": agent.max_steps,
                "token_limit": agent.token_limit,
                "workspace_dir": str(agent.workspace_dir),
                "tools_loaded": len(agent.tools),
                "tool_names": list(agent.tools.keys()),
            },
            "capabilities": {
                "file_operations": any("file" in name.lower() for name in agent.tools.keys()),
                "shell_commands": any("bash" in name.lower() for name in agent.tools.keys()),
                "web_search": any("web" in name.lower() for name in agent.tools.keys()),
                "code_assistance": any("code" in name.lower() for name in agent.tools.keys()),
                "knowledge_graph": any("graph" in name.lower() for name in agent.tools.keys()),
                "git_operations": any("git" in name.lower() for name in agent.tools.keys()),
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health = {
            "status": "healthy",
            "config_loaded": True,
            "tests": {},
            "errors": [],
            "warnings": [],
        }
        
        try:
            # Test configuration loading
            config_health = self.config.health_check()
            health["config_health"] = config_health
            if config_health["status"] != "healthy":
                health["warnings"].extend(config_health["warnings"])
                health["errors"].extend(config_health["errors"])
            
            # Test LLM client creation
            try:
                llm_client = create_llm_client()
                llm_health = llm_client.health_check()
                health["tests"]["llm_client"] = llm_health
                if llm_health["status"] != "healthy":
                    health["warnings"].extend(llm_health.get("warnings", []))
                    health["errors"].extend(llm_health.get("errors", []))
            except Exception as e:
                health["tests"]["llm_client"] = {"status": "unhealthy", "error": str(e)}
                health["errors"].append(f"LLM client test failed: {e}")
            
            # Test tool loading
            try:
                tools = asyncio.run(self._load_tools())
                health["tests"]["tool_loading"] = {
                    "status": "healthy",
                    "tools_loaded": len(tools),
                    "tool_types": [type(tool).__name__ for tool in tools]
                }
            except Exception as e:
                health["tests"]["tool_loading"] = {"status": "unhealthy", "error": str(e)}
                health["warnings"].append(f"Tool loading test failed: {e}")
            
            # Overall status
            if health["errors"]:
                health["status"] = "unhealthy"
            elif health["warnings"]:
                health["status"] = "warning"
                
        except Exception as e:
            health["status"] = "unhealthy"
            health["errors"].append(f"Health check failed: {e}")
        
        return health


# Convenience factory functions
async def create_production_agent(
    system_prompt: Optional[str] = None,
    custom_tools: Optional[List] = None,
    **kwargs
) -> Agent:
    """Create a production-grade agent with auto-configuration"""
    factory = AgentFactory()
    return await factory.create_agent(
        system_prompt=system_prompt,
        custom_tools=custom_tools,
        **kwargs
    )


def create_simple_agent() -> Agent:
    """Create a simple agent for testing (synchronous)"""
    factory = AgentFactory()
    # This would need to be async in a real implementation
    # For now, just return a placeholder
    raise NotImplementedError("Use create_production_agent() for async creation")


# Export commonly used functions
__all__ = ["AgentFactory", "create_production_agent", "create_simple_agent"]
