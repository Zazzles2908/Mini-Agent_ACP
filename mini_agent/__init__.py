"""Mini Agent - Enhanced agent with modular architecture and MCP support."""

# Import modular components (single source of truth)
from .agent_factory import AgentFactory, create_production_agent
from .core.acp_agent import ACPAgent as Agent

from .llm import LLMClient
from .schema import FunctionCall, LLMProvider, LLMResponse, Message, ToolCall

__version__ = "2.0.0"

__all__ = [
    "Agent",
    "LLMClient",
    "LLMProvider",
    "Message",
    "LLMResponse",
    "ToolCall",
    "FunctionCall",
    "AgentFactory",
    "create_production_agent",
]
