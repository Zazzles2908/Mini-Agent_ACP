"""Quick status check for Mini-Agent components."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

print("\n" + "="*50)
print("MINI-AGENT COMPONENT STATUS CHECK")
print("="*50 + "\n")

# 1. Environment Check
print("1. Environment Variables:")
zai_key = os.getenv("ZAI_API_KEY")
if zai_key:
    print(f"   ✅ ZAI_API_KEY: Set ({zai_key[:20]}...)")
else:
    print("   ❌ ZAI_API_KEY: Not set")

# 2. Z.AI Tools Check
print("\n2. Z.AI Tools:")
try:
    from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
    
    search_tool = ZAIWebSearchTool()
    reader_tool = ZAIWebReaderTool()
    
    print(f"   ✅ ZAIWebSearchTool imported")
    print(f"      - Available: {search_tool.available}")
    print(f"      - Name: {search_tool.name}")
    
    print(f"   ✅ ZAIWebReaderTool imported")
    print(f"      - Available: {reader_tool.available}")
    print(f"      - Name: {reader_tool.name}")
except Exception as e:
    print(f"   ❌ Failed to import Z.AI tools: {e}")

# 3. Z.AI Client Check
print("\n3. Z.AI Client:")
try:
    from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
    
    api_key = get_zai_api_key()
    if api_key:
        client = ZAIClient(api_key)
        print(f"   ✅ ZAIClient initialized")
        print(f"      - Available models: {len(client.models)}")
        print(f"      - Models: {', '.join(client.models.keys())}")
    else:
        print(f"   ⚠️  ZAIClient: API key not found")
except Exception as e:
    print(f"   ❌ Failed to initialize Z.AI client: {e}")

# 4. ACP Server Check
print("\n4. ACP Server:")
try:
    from mini_agent.acp import MiniMaxACPAgent
    print(f"   ✅ ACP module imported")
    print(f"      - MiniMaxACPAgent available")
except Exception as e:
    print(f"   ❌ Failed to import ACP: {e}")

# 5. Configuration Check
print("\n5. Configuration:")
try:
    from mini_agent.config import Config
    
    config = Config.load()
    print(f"   ✅ Configuration loaded")
    print(f"      - Z.AI search enabled: {config.tools.enable_zai_search}")
    print(f"      - Skills enabled: {config.tools.enable_skills}")
    print(f"      - MCP enabled: {config.tools.enable_mcp}")
    print(f"      - Max steps: {config.agent.max_steps}")
except Exception as e:
    print(f"   ❌ Failed to load configuration: {e}")

# 6. Terminal Utils Check
print("\n6. Terminal Display Utils:")
try:
    from mini_agent.utils.terminal_utils import calculate_display_width, pad_to_width
    
    test_emoji = "🔧"
    test_cjk = "中文"
    
    emoji_width = calculate_display_width(test_emoji)
    cjk_width = calculate_display_width(test_cjk)
    
    print(f"   ✅ Terminal utils available")
    print(f"      - Emoji '{test_emoji}' width: {emoji_width} (expected: 2)")
    print(f"      - CJK '{test_cjk}' width: {cjk_width} (expected: 4)")
except Exception as e:
    print(f"   ❌ Failed to import terminal utils: {e}")

print("\n" + "="*50)
print("STATUS CHECK COMPLETE")
print("="*50 + "\n")

# Summary
print("Summary:")
all_checks = [
    zai_key is not None,
    'search_tool' in locals() and search_tool.available,
    'client' in locals(),
    'config' in locals(),
]

passed = sum(all_checks)
total = len(all_checks)

if passed == total:
    print(f"✅ All checks passed ({passed}/{total})")
    print("\nYour Mini-Agent is ready to use!")
    print("Run: mini-agent")
else:
    print(f"⚠️  Some checks failed ({passed}/{total})")
    print("\nPlease check the output above for issues.")
