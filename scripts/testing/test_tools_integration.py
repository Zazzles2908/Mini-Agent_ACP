#!/usr/bin/env python3
"""
Test Z.AI Tools Integration
"""

import sys
import asyncio
from pathlib import Path

# Add mini_agent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mini_agent.config import Config
from mini_agent.cli import initialize_base_tools

async def test_tools_integration():
    print("🧪 Testing Z.AI Tools Integration")
    print("=" * 50)
    
    # Create minimal config
    config = Config(
        llm=Config.LLMConfig(
            api_key="test",
            api_base="https://api.minimax.io",
            model="MiniMax-M2",
            provider="anthropic"
        ),
        agent=Config.AgentConfig(),
        tools=Config.ToolsConfig(
            enable_zai_search=True,
            enable_bash=True,
            enable_file_tools=True,
            enable_note=True,
            enable_skills=False,
            enable_mcp=False
        )
    )
    
    try:
        tools, skill_loader = await initialize_base_tools(config)
        
        print(f"\n✅ Total tools loaded: {len(tools)}")
        
        # Check for Z.AI tools
        zai_tools = []
        minimax_zai_tools = []
        
        for tool in tools:
            tool_name = tool.name
            print(f"  - {tool_name}")
            
            if 'zai' in tool_name.lower() and 'minimax' not in tool_name.lower():
                zai_tools.append(tool_name)
            elif 'minimax' in tool_name.lower():
                minimax_zai_tools.append(tool_name)
        
        print(f"\n📊 Z.AI Tools Summary:")
        print(f"  Standard Z.AI tools: {len(zai_tools)}")
        for tool in zai_tools:
            print(f"    ✅ {tool}")
            
        print(f"\n📊 MiniMax-M2 Z.AI Tools Summary:")
        print(f"  MiniMax-M2-compatible tools: {len(minimax_zai_tools)}")
        for tool in minimax_zai_tools:
            print(f"    ✅ {tool}")
        
        if 'minimax_zai_web_search' in [t.name for t in tools]:
            print(f"\n🎯 SUCCESS: MiniMax-M2 Z.AI web search tool is loaded!")
            print(f"🚀 Ready for integration testing!")
        else:
            print(f"\n❌ ISSUE: MiniMax-M2 Z.AI web search tool not found in loaded tools")
            
    except Exception as e:
        print(f"❌ Error loading tools: {e}")
        print(f"Type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_tools_integration())