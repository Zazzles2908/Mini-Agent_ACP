"""Tools module.

Core tools are always available. Z.AI tools require explicit config enablement for credit protection.
"""

from .base import Tool, ToolResult
from .bash_tool import BashTool
from .file_tools import EditTool, ReadTool, WriteTool, ReadFileTool
from .note_tool import RecallNoteTool, SessionNoteTool

# QA Validation Tool - Core AI behavior validation system
_qa_tools_available = False
ValidationTool = None

# QA validation tools - loaded lazily to avoid circular imports
_qa_tools_available = False
ValidationTool = None

def _try_load_qa_validation_tool():
    """Attempt to load QA validation tool without causing circular imports"""
    global _qa_tools_available, ValidationTool
    
    if _qa_tools_available:
        return True
    
    try:
        import sys
        import importlib.util
        from pathlib import Path
        
        # Load validation tool module directly to avoid circular import
        validation_path = Path(__file__).parent.parent / "skills" / "fact-checking-self-assessment" / "tools" / "validation_tool.py"
        
        # Check if validation tool file exists
        if not validation_path.exists():
            return False
        
        # Load the validation tool module
        spec = importlib.util.spec_from_file_location("validation_tool", validation_path)
        validation_module = importlib.util.module_from_spec(spec)
        
        # Add base classes to the module
        validation_module.Tool = Tool
        validation_module.ToolResult = ToolResult
        
        # Execute the module
        spec.loader.exec_module(validation_module)
        
        # Get the ValidationTool class (which is the actual Tool implementation)
        ValidationTool = validation_module.ValidationTool
        _qa_tools_available = True
        print("QA Validation tools enabled - AI behavior validation active")
        return True
        
    except Exception as e:
        print(f"QA Validation tools not available: {e}")
        _qa_tools_available = False
        ValidationTool = None
        return False

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
        print("✅ Z.AI tools enabled - Credit consumption active (GLM-4.6, ~120 prompts/5hrs)")
        _zai_tools_available = True
    else:
        # Z.AI is disabled - prevent imports
        print("✅ Z.AI tools disabled - Credit protection active")
        
except ImportError as e:
    # If config check fails, default to safe (disabled)
    if 'zai_enabled' not in locals():
        print("⚠️  Z.AI config check failed - Defaulting to disabled for safety")
    _zai_tools_available = False
except Exception as e:
    # If any import fails, default to safe (disabled) to prevent credit consumption
    print(f"⚠️  Z.AI import error - Defaulting to disabled for safety: {e}")
    _zai_tools_available = False

# Only import Z.AI tools if explicitly enabled
if _zai_tools_available:
    try:
        # Import the unified Z.AI tools (single source of truth)
        from .zai_unified_tools import ZAIWebSearchTool, ZAIWebReaderTool, get_zai_tools
        print("✅ Z.AI unified tools loaded - Web search/reading available")
        print("   📍 Using Z.AI GLM-4.6 backend (FREE with Lite plan)")
            
    except ImportError as e:
        # If primary tools fail to import, log but don't crash
        print(f"⚠️  Failed to import Z.AI unified tools: {e}")
        _zai_tools_available = False

__all__ = [
    "Tool",
    "ToolResult",
    "ReadTool",
    "ReadFileTool",  # Alias for validation system compatibility
    "WriteTool",
    "EditTool",
    "BashTool",
    "SessionNoteTool",
    "RecallNoteTool",
]

# Add Z.AI tools to __all__ only if explicitly enabled and successfully imported
if _zai_tools_available:
    __all__.extend([
        "ZAIWebSearchTool",
        "ZAIWebReaderTool",
        "get_zai_tools",
    ])

# Lazy load QA validation tools to avoid circular imports
def get_validation_tool():
    """Get ValidationTool class if available"""
    if not _qa_tools_available:
        _try_load_qa_validation_tool()
    return ValidationTool

# Add to __all__ conditionally
if _qa_tools_available:
    __all__.append("ValidationTool")


def zai_tools_available() -> bool:
    """Check if Z.AI tools are available.
    
    Returns:
        True if Z.AI tools are enabled and imported successfully
    """
    return _zai_tools_available
