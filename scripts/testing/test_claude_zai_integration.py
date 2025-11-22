#!/usr/bin/env python3
"""Test script for MiniMax-M2 Z.AI Web Search Integration.

This script validates the MiniMax-M2 Code integration with Z.AI web search
by testing search result formatting and MiniMax-M2 compatibility.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mini_agent.llm.minimax_zai_client import MiniMax-M2ZAIWebSearchClient, get_zai_api_key
from mini_agent.tools.minimax_zai_tools import MiniMax-M2ZAIWebSearchTool, MiniMax-M2ZAIRecommendationTool


async def test_zai_api_connection():
    """Test connection to Z.AI Anthropic endpoint."""
    print("🔧 Testing Z.AI API Connection...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found in environment")
        return False
    
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    # Test basic connection with a simple search
    try:
        result = await client.web_search_for_minimax(
            query="Python programming",
            count=2,
            search_engine="search-prime"
        )
        
        if result and len(result) > 0:
            print(f"✅ Z.AI API connection successful")
            print(f"   - Endpoint: {client.base_url}")
            print(f"   - Results returned: {len(result)} search blocks")
            return True
        else:
            print("❌ Z.AI API returned empty results")
            return False
            
    except Exception as e:
        print(f"❌ Z.AI API connection failed: {e}")
        return False


async def test_search_result_formatting():
    """Test that search results are formatted correctly for MiniMax-M2."""
    print("\n📄 Testing Search Result Formatting...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
        
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    try:
        result = await client.web_search_for_minimax(
            query="best practices Python 2024",
            count=3,
            search_engine="search-prime"
        )
        
        if not result:
            print("❌ No search results returned")
            return False
            
        # Validate MiniMax-M2 search_result block format
        for i, block in enumerate(result):
            print(f"\n✅ Search Result Block {i+1}:")
            print(f"   Type: {block.type}")
            print(f"   Title: {block.title[:50]}...")
            print(f"   Source: {block.source}")
            print(f"   Citations Enabled: {block.citations.get('enabled', False)}")
            print(f"   Content Type: {block.content[0]['type']}")
            print(f"   Content Preview: {block.content[0]['text'][:100]}...")
            
            # Validate required fields
            assert block.type == "search_result", f"Block {i} missing type"
            assert hasattr(block, 'source') and block.source, f"Block {i} missing source"
            assert hasattr(block, 'title') and block.title, f"Block {i} missing title"
            assert hasattr(block, 'content') and block.content, f"Block {i} missing content"
            assert hasattr(block, 'citations'), f"Block {i} missing citations"
            
        print(f"\n✅ All {len(result)} search blocks formatted correctly for MiniMax-M2")
        return True
        
    except Exception as e:
        print(f"❌ Search result formatting test failed: {e}")
        return False


async def test_tool_integration():
    """Test the Mini-Agent tool integration."""
    print("\n🔧 Testing Mini-Agent Tool Integration...")
    
    try:
        tool = MiniMax-M2ZAIWebSearchTool()
        
        if not tool.available:
            print("❌ MiniMax-M2 Z.AI web search tool not available")
            return False
            
        print(f"✅ Tool initialized: {tool.name}")
        print(f"   Description: {tool.description[:100]}...")
        print(f"   Parameters: {list(tool.parameters['properties'].keys())}")
        
        # Test tool execution
        result = await tool.execute(
            query="AI coding assistants comparison 2024",
            depth="quick",
            search_engine="search-prime"
        )
        
        if result.success:
            print("✅ Tool execution successful")
            metadata = result.metadata
            print(f"   Total blocks: {metadata.get('total_blocks', 0)}")
            print(f"   MiniMax-M2 compatible: {metadata.get('minimax_compatible', False)}")
            print(f"   Integration type: {metadata.get('integration_type', 'unknown')}")
            return True
        else:
            print(f"❌ Tool execution failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Tool integration test failed: {e}")
        return False


async def test_research_integration():
    """Test the research and analysis integration."""
    print("\n🔬 Testing Research & Analysis Integration...")
    
    api_key = get_zai_api_key()
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
        
    client = MiniMax-M2ZAIWebSearchClient(api_key)
    
    try:
        result = await client.research_and_analyze_for_minimax(
            query="web scraping ethics and legal considerations",
            depth="comprehensive",
            search_engine="search-prime"
        )
        
        if result.get("success"):
            print("✅ Research and analysis successful")
            print(f"   Query: {result['query']}")
            print(f"   Depth: {result['depth']}")
            print(f"   Sources: {result['source_count']}")
            print(f"   Integration type: {result['integration_type']}")
            
            # Verify search blocks are included
            search_blocks = result.get("search_blocks", [])
            if search_blocks:
                print(f"   Search blocks included: {len(search_blocks)}")
                return True
            else:
                print("❌ Research result missing search blocks")
                return False
        else:
            print(f"❌ Research failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Research integration test failed: {e}")
        return False


async def test_setup_guide():
    """Test the setup guide tool."""
    print("\n📚 Testing Setup Guide Tool...")
    
    try:
        tool = MiniMax-M2ZAIRecommendationTool()
        
        result = await tool.execute(section="all")
        
        if result.success:
            print("✅ Setup guide generation successful")
            print(f"   Content length: {len(result.content)} characters")
            print(f"   Guide type: {result.metadata.get('guide_type', 'unknown')}")
            
            # Check for key sections
            content = result.content.lower()
            required_sections = ["setup", "configuration", "usage", "minimax code", "z.ai"]
            missing_sections = []
            
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if not missing_sections:
                print("✅ All required sections present in guide")
                return True
            else:
                print(f"❌ Missing sections: {missing_sections}")
                return False
        else:
            print(f"❌ Setup guide generation failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Setup guide test failed: {e}")
        return False


def validate_minimax_schema_compatibility():
    """Validate that the schema matches MiniMax-M2's search_result specification."""
    print("\n🔍 Validating MiniMax-M2 Schema Compatibility...")
    
    try:
        from mini_agent.llm.minimax_zai_client import SearchResultBlock
        
        # Test schema with sample data
        test_block = SearchResultBlock(
            type="search_result",
            source="https://example.com",
            title="Test Title",
            content=[{"type": "text", "text": "Test content"}],
            citations={"enabled": True}
        )
        
        # Validate required fields per MiniMax-M2 spec
        required_fields = ["type", "source", "title", "content", "citations"]
        missing_fields = []
        
        for field in required_fields:
            if not hasattr(test_block, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
            
        # Validate field values
        if test_block.type != "search_result":
            print("❌ Invalid type field")
            return False
            
        if test_block.source != "https://example.com":
            print("❌ Invalid source field")
            return False
            
        if not test_block.content or test_block.content[0]["type"] != "text":
            print("❌ Invalid content field")
            return False
            
        if not isinstance(test_block.citations.get("enabled"), bool):
            print("❌ Invalid citations field")
            return False
            
        print("✅ Schema matches MiniMax-M2's search_result specification")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False


async def run_comprehensive_test():
    """Run all tests and provide a comprehensive report."""
    print("🚀 MiniMax-M2 Z.AI Web Search Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("API Connection", test_zai_api_connection),
        ("Schema Compatibility", validate_minimax_schema_compatibility), 
        ("Search Result Formatting", test_search_result_formatting),
        ("Tool Integration", test_tool_integration),
        ("Research Integration", test_research_integration),
        ("Setup Guide", test_setup_guide),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                success = await test_func()
            else:
                success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! MiniMax-M2 Z.AI integration is ready.")
        print("\nNext steps:")
        print("1. Configure MiniMax-M2 Code with Z.AI endpoint")
        print("2. Use minimax_zai_web_search tool for web results with citations")
        print("3. Test integration with your MiniMax-M2 Code workflow")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    # Run the comprehensive test suite
    success = asyncio.run(run_comprehensive_test())
    sys.exit(0 if success else 1)
