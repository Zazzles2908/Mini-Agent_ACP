"""ACP (Agent Client Protocol) bridge for Mini-Agent - Fixed version."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import aiohttp
from acp import (
    PROTOCOL_VERSION,
    AgentSideConnection,
    Agent,
    start_tool_call,
    stdio_streams,
    text_block,
    tool_content,
    update_agent_message,
    update_agent_thought,
    update_tool_call,
)

logger = logging.getLogger(__name__)


@dataclass
class SessionState:
    agent: Any  # Will be the Mini-Agent agent
    cancelled: bool = False


class MiniMaxACPAgent(Agent):
    """ACP agent that wraps the existing Mini-Agent runtime."""

    def __init__(
        self,
        config: Any,
        llm: Any,
        base_tools: list,
        system_prompt: str,
    ):
        super().__init__()
        self._config = config
        self._llm = llm
        self._base_tools = base_tools
        self._system_prompt = system_prompt
        self._sessions: dict[str, SessionState] = {}

    async def initialize(self, params: Any) -> dict[str, Any]:
        """Initialize the agent with ACP protocol."""
        return {
            'protocolVersion': PROTOCOL_VERSION,
            'agentCapabilities': {
                'loadSession': False
            },
            'agentInfo': {
                'name': "mini-agent",
                'title': "Mini-Agent",
                'version': "0.1.0"
            }
        }

    async def newSession(self, params: Any) -> dict[str, Any]:
        """Create a new agent session."""
        session_id = f"sess-{len(self._sessions)}-{uuid4().hex[:8]}"
        workspace = Path(params.get('cwd', "./workspace")).expanduser()
        if not workspace.is_absolute():
            workspace = workspace.resolve()
        
        # Create agent instance
        from mini_agent.agent import Agent
        agent = Agent(
            llm_client=self._llm, 
            system_prompt=self._system_prompt, 
            tools=self._base_tools, 
            max_steps=self._config.agent.max_steps if self._config else 10, 
            workspace_dir=str(workspace)
        )
        
        self._sessions[session_id] = SessionState(agent=agent)
        
        return {'sessionId': session_id}

    async def prompt(self, params: Any) -> dict[str, Any]:
        """Process a prompt request in an existing session."""
        session_id = params.get('sessionId')
        state = self._sessions.get(session_id)
        
        if not state:
            return {
                'content': [text_block("Session not found")],
                'hasError': True
            }
        
        if state.cancelled:
            return {
                'content': [text_block("Session cancelled")],
                'hasError': True
            }
        
        try:
            # Convert prompt to agent message format
            from mini_agent.schema import Message
            messages = [Message(role="user", content=params.get('prompt', ''))]
            
            # Run agent
            response = await state.agent.run(messages)
            
            # Convert response back to ACP format
            content = [text_block(response.content)]
            
            return {'content': content}
            
        except Exception as e:
            logger.error("Error processing prompt: %s", e)
            return {
                'content': [text_block(f"Error: {str(e)}")],
                'hasError': True
            }

    async def cancel(self, params: Any) -> dict[str, Any]:
        """Cancel a running session."""
        session_id = params.get('sessionId')
        state = self._sessions.get(session_id)
        if state:
            state.cancelled = True
        return {'cancelled': True}
    
    async def loadSession(self, params: Any) -> dict[str, Any]:
        """Load a session (not implemented yet)."""
        return {'sessionLoaded': False}
    
    async def setSessionMode(self, params: Any) -> dict[str, Any]:
        """Set session mode (not implemented yet)."""
        return {'modeSet': True}
    
    async def setSessionModel(self, params: Any) -> dict[str, Any]:
        """Set session model (not implemented yet)."""
        return {'modelSet': True}


async def main():
    """Main ACP server entry point."""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default="./", help="Workspace directory")
    args = parser.parse_args()
    
    # Load configuration
    try:
        from mini_agent.config import Config
        config = Config.from_yaml("mini_agent/config/config.yaml")
    except Exception as e:
        logger.error("Failed to load config: %s", e)
        config = None
    
    # Initialize base tools
    try:
        from mini_agent.cli import initialize_base_tools
        tools = []
        await initialize_base_tools(config or type('Config', (), {
            'llm': type('LLMConfig', (), {
                'api_key': 'test',
                'api_base': 'https://api.minimax.io',
                'model': 'MiniMax-M2',
                'retry': type('RetryConfig', (), {
                    'enabled': False,
                    'max_retries': 3,
                    'initial_delay': 1.0,
                    'max_delay': 60.0,
                    'exponential_base': 2.0
                })()
            })(),
            'tools': type('ToolsConfig', (), {
                'enable_file_tools': True,
                'enable_bash': True,
                'enable_note': True,
                'enable_zai_search': True,
                'enable_skills': True,
                'enable_mcp': True,
                'skills_dir': './skills',
                'mcp_config_path': 'mcp.json'
            })()
        })())
    except Exception as e:
        logger.error("Failed to initialize tools: %s", e)
        tools = []
    
    # Initialize LLM client
    try:
        from mini_agent.llm import LLMClient
        if config:
            llm = LLMClient(
                api_key=config.llm.api_key,
                api_base=config.llm.api_base,
                model=config.llm.model,
                retry_config=config.llm.retry
            )
        else:
            llm = LLMClient(
                api_key="test",
                api_base="https://api.minimax.io", 
                model="MiniMax-M2"
            )
    except Exception as e:
        logger.error("Failed to create LLM client: %s", e)
        llm = None
    
    # Create agent with workspace tools
    workspace = Path(args.workspace)
    
    system_prompt = "You are a helpful AI assistant integrated with the Agent Client Protocol."
    
    # Create ACP agent
    agent = MiniMaxACPAgent(
        config=config,
        llm=llm,
        base_tools=tools,
        system_prompt=system_prompt,
    )
    
    # Run with stdio streams
    try:
        streams = await stdio_streams()
        read_stream, write_stream = streams
        
        # Run the agent with stdio streams
        await agent.run(read_stream, write_stream)
            
    except Exception as e:
        logger.error("Error starting ACP server: %s", e)
        raise


__all__ = ["MiniMaxACPAgent", "main"]
