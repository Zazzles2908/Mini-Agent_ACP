"""Tools module."""

from .base import Tool, ToolResult
from .bash_tool import BashTool
from .file_tools import EditTool, ReadTool, WriteTool
from .note_tool import RecallNoteTool, SessionNoteTool

# Z.AI tools - CRITICAL: Import only if explicitly enabled in config for credit protection
_zai_tools_available = False

# Import the credit protection module
try:
    import os
    import sys
    from pathlib import Path
    
    # Add the project root to path if not already there
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    from mini_agent.utils.credit_protection import check_zai_protection
    
    # Check if Z.AI is enabled in config
    zai_enabled = check_zai_protection()
    
    if zai_enabled:
        # Z.AI is enabled - allow imports
        print("✅ Z.AI tools enabled - Credit consumption active")
        _zai_tools_available = True
    else:
        # Z.AI is disabled - prevent imports and throw ImportError
        print("✅ Z.AI tools disabled - Credit protection active")
        raise ImportError("Z.AI tools disabled for credit protection")
        
except ImportError:
    # If config check fails, default to safe (disabled) - should not happen often
    if 'zai_enabled' not in locals():
        print("⚠️  Z.AI config check failed - Defaulting to disabled for safety")
    # Either way, Z.AI tools remain unavailable
    _zai_tools_available = False
except Exception as e:
    # If any import fails, default to safe (disabled) to prevent credit consumption
    print(f"⚠️  Z.AI import error - Defaulting to disabled for safety: {e}")
    _zai_tools_available = False

# Only import Z.AI tools if explicitly enabled
if _zai_tools_available:
    try:
        from .zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
        from .claude_zai_tools import ClaudeZAIWebSearchTool, ClaudeZAIRecommendationTool
        from .zai_anthropic_tools import ZAIAnthropicWebSearchTool
    except ImportError as e:
        # If individual tools fail to import, log but don't crash
        print(f"⚠️  Failed to import some Z.AI tools: {e}")
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

# Add Z.AI tools to __all__ only if explicitly enabled
if _zai_tools_available:
    __all__.extend([
        "ZAIWebSearchTool",
        "ZAIWebReaderTool", 
        "ClaudeZAIWebSearchTool",
        "ClaudeZAIRecommendationTool",
        "ZAIAnthropicWebSearchTool",
    ])

# Function to check if Z.AI tools are available (for agent initialization)
def zai_tools_available() -> bool:
    """Check if Z.AI tools are available based on configuration"""
    return _zai_tools_available
