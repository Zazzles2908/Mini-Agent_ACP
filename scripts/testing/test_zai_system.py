#!/usr/bin/env python3
"""
Comprehensive Z.AI System Test
Tests actual Z.AI functionality, not fake responses.
"""

import asyncio
import sys
import json
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, '.')

async def test_zai_web_search():
    """Test real Z.AI web search functionality."""
    print("🔍 Testing Z.AI Web Search...")
    
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        # Get API key from environment
        zai_api_key = os.getenv('ZAI_API_KEY')
        if not zai_api_key:
            print("❌ ZAI_API_KEY not found in environment")
            return False
            
        print(f"✅ ZAI_API_KEY found: {zai_api_key[:10]}...{zai_api_key[-10:]}")
        
        # Initialize client
        client = ZAIClient(api_key=zai_api_key, use_coding_plan=True)
        
        # Test with a specific, verifiable query
        test_query = "OpenAI CEO 2024"
        print(f"Testing search for: {test_query}")
        
        try:
            result = await client.web_search(
                query=test_query,
                count=3,
                search_engine="search-prime"
            )
            
            print(f"✅ Z.AI Search Result Type: {type(result)}")
            
            if isinstance(result, dict):
                print("Raw result:")
                print(json.dumps(result, indent=2, default=str))
                
                # Check if we have actual search results
                # The actual key is "search_result" not "results"
                if "search_result" in result and len(result["search_result"]) > 0:
                    print(f"✅ Found {len(result['search_result'])} search results")
                    for i, r in enumerate(result["search_result"][:2]):
                        print(f"  Result {i+1}: {r.get('title', 'No title')} - {r.get('link', 'No link')}")
                    return True
                else:
                    print("❌ No search results found in response")
                    print(f"Available keys: {list(result.keys())}")
                    return False
            else:
                print(f"❌ Unexpected result format: {type(result)}")
                return False
                
        except Exception as e:
            print(f"❌ Z.AI Search Error: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

async def test_zai_web_reader():
    """Test Z.AI web reader functionality."""
    print("\n📖 Testing Z.AI Web Reader...")
    
    try:
        from mini_agent.llm.zai_client import ZAIClient
        
        zai_api_key = os.getenv('ZAI_API_KEY')
        if not zai_api_key:
            return False
            
        client = ZAIClient(api_key=zai_api_key, use_coding_plan=True)
        
        # Test with a real URL
        test_url = "https://www.openai.com"
        print(f"Testing reader with URL: {test_url}")
        
        try:
            result = await client.web_reading(url=test_url)
            
            print(f"✅ Z.AI Reader Result Type: {type(result)}")
            
            if isinstance(result, dict):
                print("Raw result:")
                print(json.dumps(result, indent=2, default=str))
                
                # Check what content keys are available
                content_keys = [k for k in result.keys() if 'content' in k.lower()]
                if content_keys:
                    content = result[content_keys[0]]
                    print(f"✅ Found {content_keys[0]}: {len(content)} characters")
                    print(f"Preview: {str(content)[:200]}...")
                    return True
                else:
                    print("❌ No content found in response")
                    print(f"Available keys: {list(result.keys())}")
                    return False
            else:
                print(f"❌ Unexpected result format: {type(result)}")
                return False
                
        except Exception as e:
            print(f"❌ Z.AI Reader Error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_minimax_integration():
    """Test MiniMax LLM integration."""
    print("\n🤖 Testing MiniMax LLM Integration...")
    
    try:
        from mini_agent.llm.llm_wrapper import LLMClient
        from mini_agent.schema import LLMProvider
        
        minimax_api_key = os.getenv('MINIMAX_API_KEY')
        if not minimax_api_key:
            print("❌ MINIMAX_API_KEY not found")
            return False
            
        print(f"✅ MINIMAX_API_KEY found: {minimax_api_key[:10]}...{minimax_api_key[-10:]}")
        
        # Test LLM client initialization
        client = LLMClient(
            api_key=minimax_api_key,
            provider=LLMProvider.ANTHROPIC,
            model="MiniMax-M2"
        )
        
        print(f"✅ LLMClient initialized with provider: {client.provider}")
        print(f"✅ API base: {client.api_base}")
        print(f"✅ Model: {client.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ MiniMax Integration Error: {e}")
        return False

def test_aiohttp_import():
    """Test aiohttp import status."""
    print("\n📦 Testing Dependencies...")
    
    try:
        import aiohttp
        print(f"✅ aiohttp available: {aiohttp.__version__}")
        return True
    except ImportError as e:
        print(f"❌ aiohttp import error: {e}")
        return False

def test_tools_system():
    """Test the tools system."""
    print("\n🛠️ Testing Tools System...")
    
    try:
        # Test if tools can be imported
        from mini_agent.tools.file_tools import ReadTool
        from mini_agent.tools.bash_tool import BashTool
        from mini_agent.tools.skill_tool import GetSkillTool
        
        print("✅ Core tools imported successfully")
        
        # Test tool instantiation
        read_tool = ReadTool()
        bash_tool = BashTool()
        
        print(f"✅ ReadTool: {read_tool.name}")
        print(f"✅ BashTool: {bash_tool.name}")
        print(f"✅ GetSkillTool: Available")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools System Error: {e}")
        return False

async def main():
    """Run comprehensive system test."""
    print("=" * 60)
    print("🚀 Mini-Agent System Comprehensive Audit")
    print("=" * 60)
    
    results = {
        "aiohttp_import": test_aiohttp_import(),
        "minimax_integration": test_minimax_integration(),
        "tools_system": test_tools_system(),
        "zai_web_search": await test_zai_web_search(),
        "zai_web_reader": await test_zai_web_reader(),
    }
    
    print("\n" + "=" * 60)
    print("📊 SYSTEM AUDIT RESULTS")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test:20s}: {status}")
    
    print(f"\nOverall Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! System is production-ready.")
    else:
        print("⚠️  Some tests failed. Review results above.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())
