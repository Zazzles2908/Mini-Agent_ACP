"""Schema definitions for Mini-Agent"""
from enum import Enum
from typing import Any
from pydantic import BaseModel

class LLMProvider(str, Enum):
    """LLM provider types."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"

class FunctionCall(BaseModel):
    """Function call details."""
    name: str
    arguments: dict[str, Any]

class ToolCall(BaseModel):
    """Tool call details."""
    id: str
    type: str
    function: FunctionCall

class Message(BaseModel):
    """Message schema."""
    role: str
    content: str
    thinking: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    name: str | None = None

class LLMResponse(BaseModel):
    """Response from LLM."""
    content: str
    thinking: str | None = None
    tool_calls: list[ToolCall] | None = None
    finish_reason: str