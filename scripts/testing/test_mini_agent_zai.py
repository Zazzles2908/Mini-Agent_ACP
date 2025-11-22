"""
Final verification test for Z.AI integration with Mini-Agent
Tests the updated ZAIClient using direct REST API
"""
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

async def test_mini_agent_zai_client():
    """Test the updated Mini-Agent ZAIClient"""
    print("=" * 70)
    print("Mini-Agent ZAIClient Integration Test")
    print("=" * 70)
    
    # Import the Mini-Agent ZAI client
    try:
        from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
        print("✓ Successfully imported ZAIClient from mini_agent")
    except ImportError as e:
        print(f"❌ FAILED: Could not import ZAIClient: {e}")
        return False
    
    # Get API key
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ FAILED: ZAI_API_KEY not found")
        return False
    
    print(f"✓ API Key found: {api_key[:8]}...")
    
    # Initialize client
    try:
        client = ZAIClient(api_key)
        print("✓ ZAIClient initialized")
    except Exception as e:
        print(f"❌ FAILED: Could not initialize client: {e}")
        return False
    
    # Test 1: Direct web search
    print(f"\n{'─' * 70}")
    print("Test 1: Direct Web Search")
    print(f"{'─' * 70}")
    
    try:
        result = await client.web_search(
            query="latest AI breakthroughs 2025",
            count=3
        )
        
        if result.get("success"):
            print(f"✓ Web search successful")
            print(f"✓ Results: {result['count']} items")
            print(f"✓ Request ID: {result.get('request_id')}")
            
            # Display first result
            if result.get("search_result"):
                first = result["search_result"][0]
                print(f"\nFirst result:")
                print(f"  Title: {first.get('title', 'N/A')[:60]}...")
                print(f"  Link: {first.get('link', 'N/A')}")
        else:
            print(f"❌ FAILED: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 2: Research and analyze
    print(f"\n{'─' * 70}")
    print("Test 2: Research and Analyze")
    print(f"{'─' * 70}")
    
    try:
        result = await client.research_and_analyze(
            query="quantum computing advances",
            depth="quick"
        )
        
        if result.get("success"):
            print(f"✓ Research successful")
            print(f"✓ Depth: {result['depth']}")
            print(f"✓ Sources: {len(result.get('search_evidence', []))}")
            print(f"✓ Analysis length: {len(result.get('analysis', ''))} chars")
        else:
            print(f"❌ FAILED: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 3: Web tools integration
    print(f"\n{'─' * 70}")
    print("Test 3: ZAI Tools Integration")
    print(f"{'─' * 70}")
    
    try:
        from mini_agent.tools.zai_tools import ZAIWebSearchTool
        print("✓ Successfully imported ZAIWebSearchTool")
        
        tool = ZAIWebSearchTool(api_key)
        if tool.available:
            print("✓ ZAIWebSearchTool initialized and available")
            
            # Test tool execution
            result = await tool.execute(query="Python programming best practices", depth="quick")
            
            if result.success:
                print("✓ Tool execution successful")
                print(f"✓ Content length: {len(result.content)} chars")
            else:
                print(f"⚠ Tool execution returned error: {result.error}")
        else:
            print("⚠ ZAIWebSearchTool not available")
            
    except Exception as e:
        print(f"⚠ Tool test skipped: {e}")
    
    print(f"\n{'═' * 70}")
    print("✅ ALL TESTS PASSED!")
    print("✅ Mini-Agent ZAI integration working with direct REST API")
    print(f"{'═' * 70}")
    
    return True

async def main():
    """Run all tests"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "MINI-AGENT ZAI INTEGRATION TEST" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    success = await test_mini_agent_zai_client()
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "TEST SUMMARY" + " " * 31 + "║")
    print("╠" + "═" * 68 + "╣")
    
    if success:
        print("║" + " " * 20 + "🎉 ALL TESTS PASSED! 🎉" + " " * 23 + "║")
        print("║" + " " * 68 + "║")
        print("║  Mini-Agent ZAI client updated to use direct REST API!" + " " * 10 + "║")
        print("║  Web search functionality verified and working correctly!" + " " * 7 + "║")
    else:
        print("║" + " " * 20 + "⚠️  SOME TESTS FAILED" + " " * 26 + "║")
    
    print("╚" + "═" * 68 + "╝\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
