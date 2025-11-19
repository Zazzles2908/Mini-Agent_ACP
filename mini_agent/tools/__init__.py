"""Tools module."""

from .base import Tool, ToolResult
from .bash_tool import BashTool
from .file_tools import EditTool, ReadTool, WriteTool
from .note_tool import RecallNoteTool, SessionNoteTool

# Z.AI tools
try:
    from .zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
    from .claude_zai_tools import ClaudeZAIWebSearchTool, ClaudeZAIRecommendationTool
    from .zai_anthropic_tools import ZAIAnthropicWebSearchTool
    _zai_tools_available = True
except ImportError:
    _zai_tools_available = False

__all__ = [
    "Tool",
    "ToolResult",
    "ReadTool",
    "WriteTool",
    "EditTool",
    "BashTool",
    "SessionNoteTool",
    "RecallNoteTool",
]

# Add Z.AI tools to __all__ if available
if _zai_tools_available:
    __all__.extend([
        "ZAIWebSearchTool",
        "ZAIWebReaderTool", 
        "ClaudeZAIWebSearchTool",
        "ClaudeZAIRecommendationTool",
        "ZAIAnthropicWebSearchTool",
    ])
