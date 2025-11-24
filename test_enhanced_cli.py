#!/usr/bin/env python3
"""
Test enhanced CLI integration with memory features enabled.
"""

import asyncio
from mini_agent.cli import add_workspace_tools
from mini_agent.config import get_config
from pathlib import Path


async def test_enhanced_cli():
    """Test that enhanced CLI loads enhanced tools when enabled."""
    print("🧪 Testing Enhanced CLI Integration")
    print("=" * 40)
    
    # Check configuration
    config = get_config()
    memory_config = config.get_memory_config()
    print(f"Enhanced memory enabled: {memory_config['enable_enhanced']}")
    
    # Load tools
    tools = []
    workspace_dir = Path('./workspace')
    add_workspace_tools(tools, config, workspace_dir)
    
    # Check note tools
    note_tools = [t for t in tools if 'note' in t.name.lower() or 'recall' in t.name.lower()]
    print(f"Note tools loaded: {len(note_tools)}")
    
    for tool in note_tools:
        print(f"  - {tool.name}: {tool.__class__.__name__}")
    
    # Check if enhanced tools are loaded
    enhanced_tools = [t for t in note_tools if 'Enhanced' in t.__class__.__name__]
    print(f"Enhanced tools loaded: {len(enhanced_tools)}")
    
    if len(enhanced_tools) >= 2:
        print("✅ Enhanced tools loaded successfully")
        return True
    else:
        print("❌ Enhanced tools not loaded - CLI integration incomplete")
        return False


if __name__ == "__main__":
    asyncio.run(test_enhanced_cli())