#!/usr/bin/env python3
"""
Z.AI Integration Test Script
Tests native GLM web search and reading capabilities

Usage:
    python test_zai_integration.py
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add Mini-Agent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool


async def test_zai_api_connection():
    """Test Z.AI API key and basic connectivity"""
    print("🔑 Testing Z.AI API Connection")
    print("=" * 40)
    
    # Check API key
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found in environment")
        print("   Please set ZAI_API_KEY environment variable")
        print("   or add it to your .env file")
        return None
    
    print(f"✅ Z.AI API key found: {api_key[:20]}...")
    
    # Initialize client
    try:
        client = ZAIClient(api_key)
        print("✅ Z.AI client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Z.AI client: {e}")
        return None


async def test_web_search(client: ZAIClient):
    """Test Z.AI web search functionality"""
    print("\n🔍 Testing Z.AI Web Search")
    print("=" * 40)
    
    test_queries = [
        {
            "query": "latest AI developments 2024",
            "depth": "quick",
            "description": "Quick search test"
        },
        {
            "query": "GLM model capabilities and features",
            "depth": "comprehensive",
            "description": "Comprehensive search test"
        }
    ]
    
    results = []
    
    for test in test_queries:
        print(f"\n📋 Test: {test['description']}")
        print(f"Query: {test['query']}")
        print(f"Depth: {test['depth']}")
        
        try:
            result = await client.research_and_analyze(
                query=test["query"],
                depth=test["depth"],
                model_preference="glm-4.6"
            )
            
            if result.get("success"):
                print(f"✅ Search successful!")
                print(f"   Model: {result['model_used']}")
                print(f"   Analysis length: {len(result.get('analysis', ''))} chars")
                print(f"   Token usage: {result.get('token_usage', {}).get('total_tokens', 'N/A')}")
                
                results.append({
                    "test": test["description"],
                    "success": True,
                    "model": result["model_used"],
                    "tokens": result.get("token_usage", {}).get("total_tokens", 0)
                })
            else:
                print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
                results.append({
                    "test": test["description"],
                    "success": False,
                    "error": result.get("error")
                })
                
        except Exception as e:
            print(f"❌ Search exception: {e}")
            results.append({
                "test": test["description"],
                "success": False,
                "error": str(e)
            })
    
    return results


async def test_web_reading(client: ZAIClient):
    """Test Z.AI web reading functionality"""
    print("\n📖 Testing Z.AI Web Reading")
    print("=" * 40)
    
    test_urls = [
        {
            "url": "https://github.com",
            "description": "GitHub homepage"
        },
        {
            "url": "https://httpbin.org/json",
            "description": "Simple JSON API test"
        }
    ]
    
    results = []
    
    for test in test_urls:
        print(f"\n📋 Test: {test['description']}")
        print(f"URL: {test['url']}")
        
        try:
            result = await client.web_reading(
                url=test["url"],
                format_type="markdown",
                include_images=True
            )
            
            if result.get("success"):
                print(f"✅ Reading successful!")
                print(f"   Title: {result.get('title', 'N/A')}")
                print(f"   Word count: {result.get('word_count', 0)}")
                print(f"   Content preview: {result.get('content', '')[:100]}...")
                
                results.append({
                    "test": test["description"],
                    "success": True,
                    "word_count": result.get("word_count", 0),
                    "title": result.get("title", "N/A")
                })
            else:
                print(f"❌ Reading failed: {result.get('error', 'Unknown error')}")
                results.append({
                    "test": test["description"],
                    "success": False,
                    "error": result.get("error")
                })
                
        except Exception as e:
            print(f"❌ Reading exception: {e}")
            results.append({
                "test": test["description"],
                "success": False,
                "error": str(e)
            })
    
    return results


async def test_zai_tools():
    """Test Z.AI tools integration"""
    print("\n🛠️ Testing Z.AI Tools Integration")
    print("=" * 40)
    
    try:
        # Test web search tool
        search_tool = ZAIWebSearchTool()
        print(f"✅ ZAIWebSearchTool available: {search_tool.available}")
        print(f"   Tool name: {search_tool.name}")
        print(f"   Tool description: {search_tool.description[:100]}...")
        
        # Test web reader tool
        reader_tool = ZAIWebReaderTool()
        print(f"✅ ZAIWebReaderTool available: {reader_tool.available}")
        print(f"   Tool name: {reader_tool.name}")
        print(f"   Tool description: {reader_tool.description[:100]}...")
        
        return {
            "search_tool_available": search_tool.available,
            "reader_tool_available": reader_tool.available,
            "tools_loaded": search_tool.available or reader_tool.available
        }
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return {"tools_loaded": False, "error": str(e)}


def print_summary(test_results):
    """Print comprehensive test summary"""
    print("\n📊 Z.AI Integration Test Summary")
    print("=" * 50)
    
    # API Connection
    print(f"🔑 API Connection: {'✅ PASS' if test_results.get('api_connection') else '❌ FAIL'}")
    
    # Web Search
    search_results = test_results.get('web_search', [])
    search_success = sum(1 for r in search_results if r.get('success'))
    print(f"🔍 Web Search: {search_success}/{len(search_results)} tests passed")
    
    # Web Reading
    reading_results = test_results.get('web_reading', [])
    reading_success = sum(1 for r in reading_results if r.get('success'))
    print(f"📖 Web Reading: {reading_success}/{len(reading_results)} tests passed")
    
    # Tools Integration
    tools = test_results.get('tools', {})
    print(f"🛠️ Tools Integration: {'✅ LOADED' if tools.get('tools_loaded') else '❌ NOT LOADED'}")
    
    # Overall Status
    overall_success = (
        test_results.get('api_connection') and
        search_success > 0 and
        tools.get('tools_loaded', False)
    )
    
    print(f"\n🎯 Overall Status: {'✅ FULLY OPERATIONAL' if overall_success else '⚠️ NEEDS ATTENTION'}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if not test_results.get('api_connection'):
        print("   • Check Z.AI API key in .env file")
        print("   • Verify API key is valid and has sufficient credits")
    
    if search_success == 0:
        print("   • Check internet connectivity")
        print("   • Verify Z.AI service status")
    
    if not tools.get('tools_loaded'):
        print("   • Check Mini-Agent configuration")
        print("   • Ensure Z.AI tools are enabled in config")
    
    if overall_success:
        print("   • Z.AI integration is working correctly!")
        print("   • Web search and reading capabilities are available")
        print("   • Ready for production use")


async def main():
    """Main test function"""
    print("🧪 Z.AI Integration Test Suite")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Working Directory: {os.getcwd()}")
    
    # Initialize test results
    test_results = {}
    
    # Test 1: API Connection
    client = await test_zai_api_connection()
    test_results['api_connection'] = client is not None
    
    if not client:
        print("\n❌ Cannot continue tests without Z.AI API connection")
        print("\nTo fix:")
        print("1. Get Z.AI API key from: https://z.ai/subscribe")
        print("2. Add to .env file: ZAI_API_KEY=your_key_here")
        print("3. Restart this test")
        return
    
    # Test 2: Web Search
    web_search_results = await test_web_search(client)
    test_results['web_search'] = web_search_results
    
    # Test 3: Web Reading
    web_reading_results = await test_web_reading(client)
    test_results['web_reading'] = web_reading_results
    
    # Test 4: Tools Integration
    tools_results = await test_zai_tools()
    test_results['tools'] = tools_results
    
    # Print comprehensive summary
    print_summary(test_results)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
