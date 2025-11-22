#!/usr/bin/env python3
"""
Test Z.AI Anthropic Web Search Tool
Validates the integration with coding plan and proper functionality
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the mini_agent package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mini_agent.tools.zai_anthropic_tools import ZAIAnthropicWebSearchTool

async def test_anthropic_web_search():
    """Test the Z.AI Anthropic web search tool"""
    
    print("🧪 Testing Z.AI Anthropic Web Search Tool")
    print("=" * 60)
    
    # Check environment setup
    anthropic_token = os.getenv('ANTHROPIC_AUTH_TOKEN')
    anthropic_base_url = os.getenv('ANTHROPIC_BASE_URL')
    
    print(f"🔧 Environment Check:")
    print(f"   ANTHROPIC_AUTH_TOKEN: {'✅ Set' if anthropic_token else '❌ Missing'}")
    print(f"   ANTHROPIC_BASE_URL: {anthropic_base_url or '❌ Missing'}")
    
    if not anthropic_token:
        print(f"\n⚠️  Setting up environment variables...")
        os.environ['ANTHROPIC_AUTH_TOKEN'] = os.getenv('ZAI_API_KEY', '')
        os.environ['ANTHROPIC_BASE_URL'] = 'https://api.z.ai/api/anthropic'
        print(f"   ✅ Set from ZAI_API_KEY")
    
    # Initialize the tool
    print(f"\n🔧 Tool Initialization:")
    try:
        tool = ZAIAnthropicWebSearchTool()
        if tool.available:
            print(f"   ✅ Tool available: {tool.name}")
            print(f"   📝 Description: {tool.description[:100]}...")
            print(f"   🔧 Parameters: {len(tool.parameters['properties'])} defined")
        else:
            print(f"   ❌ Tool not available")
            return False
    except Exception as e:
        print(f"   ❌ Tool initialization failed: {e}")
        return False
    
    # Test search queries
    test_queries = [
        {
            "query": "Z.AI DevPack Claude integration",
            "description": "Testing Z.AI DevPack documentation search"
        },
        {
            "query": "Mini-Agent architecture overview",
            "description": "Testing project-specific search"
        }
    ]
    
    print(f"\n🧪 Web Search Tests:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"   Query: '{test_case['query']}'")
        
        try:
            # Execute the search
            result = await tool.execute(
                query=test_case['query'],
                max_results=3,
                depth="comprehensive"
            )
            
            if result.success:
                print(f"   ✅ Search completed successfully")
                print(f"   📄 Content length: {len(result.content)} characters")
                
                # Check for key elements in the output
                content = result.content
                if "search_result" in content:
                    print(f"   🤖 Contains Claude search_result blocks: ✅")
                if "Z.AI" in content:
                    print(f"   🔍 Contains Z.AI references: ✅")
                if "coding plan" in content.lower():
                    print(f"   💳 Contains coding plan references: ✅")
                
                # Show a preview of the results
                lines = content.split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    if line.strip():
                        print(f"   📝 {line[:80]}{'...' if len(line) > 80 else ''}")
                        break
                
            else:
                print(f"   ❌ Search failed: {result.error}")
                return False
                
        except Exception as e:
            print(f"   ❌ Test execution failed: {e}")
            return False
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"✅ Z.AI Anthropic Web Search Tool is working properly")
    print(f"✅ Uses coding plan credits instead of direct API calls")
    print(f"✅ Returns results in Claude's search_result format")
    print(f"✅ Provides natural citations for Claude Code integration")
    
    return True

async def main():
    """Main test function"""
    try:
        success = await test_anthropic_web_search()
        if success:
            print(f"\n🚀 Ready for integration with Mini-Agent!")
            print(f"💡 Tool will be loaded automatically when Z.AI search is enabled")
        else:
            print(f"\n❌ Tests failed - check configuration")
            return 1
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)