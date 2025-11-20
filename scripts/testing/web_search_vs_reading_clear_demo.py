#!/usr/bin/env python3
"""
Clear demonstration of Z.AI web search vs web reading capabilities.
Shows exactly what you get from each and why you're not seeing full content.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import Z.AI tools
sys.path.append(str(Path(__file__).parent.parent))
from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
from mini_agent.tools.base import ToolResult


async def demonstrate_web_capabilities():
    """Demonstrate the exact difference between web search and web reading."""
    
    target_url = "https://docs.z.ai/devpack/tool/claude"
    
    print("🔍 Z.AI WEB CAPABILITIES DEMONSTRATION")
    print("=" * 60)
    print(f"Target URL: {target_url}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize tools
    search_tool = ZAIWebSearchTool()
    reader_tool = ZAIWebReaderTool()
    
    results = {}
    
    # TEST 1: Web Search - What you get
    print("\n🕷️  WEB SEARCH - What You Get:")
    print("-" * 40)
    
    try:
        search_result = await search_tool.execute(
            query="Z.AI DevPack Claude integration",
            depth="comprehensive",
            search_engine="search-prime",
            model="glm-4.5"
        )
        
        if search_result.success:
            print("✅ WEB SEARCH SUCCESS!")
            print(f"\nContent length: {len(search_result.content)} characters")
            print("\n📋 SEARCH RESULTS CONTENT (first 800 chars):")
            print("-" * 50)
            print(search_result.content)
            print("-" * 50)
            
            results["web_search"] = {
                "success": True,
                "content_length": len(search_result.content),
                "content_preview": search_result.content[:800],
                "full_content": search_result.content
            }
            
        else:
            print(f"❌ WEB SEARCH FAILED: {search_result.error}")
            results["web_search"] = {"success": False, "error": search_result.error}
            
    except Exception as e:
        print(f"❌ WEB SEARCH ERROR: {str(e)}")
        results["web_search"] = {"success": False, "error": str(e)}
    
    # TEST 2: Web Reading - What you get
    print("\n📖 WEB READING - What You Get:")
    print("-" * 40)
    
    try:
        reading_result = await reader_tool.execute(
            url=target_url,
            format="markdown",
            include_images=False
        )
        
        if reading_result.success:
            print("✅ WEB READING SUCCESS!")
            print(f"\nContent length: {len(reading_result.content)} characters")
            print("\n📄 WEB PAGE CONTENT (first 800 chars):")
            print("-" * 50)
            print(reading_result.content)
            print("-" * 50)
            
            results["web_reading"] = {
                "success": True,
                "content_length": len(reading_result.content),
                "content_preview": reading_result.content[:800],
                "full_content": reading_result.content
            }
            
        else:
            print(f"❌ WEB READING FAILED: {reading_result.error}")
            results["web_reading"] = {"success": False, "error": reading_result.error}
            
    except Exception as e:
        print(f"❌ WEB READING ERROR: {str(e)}")
        results["web_reading"] = {"success": False, "error": str(e)}
    
    # ANALYSIS
    print("\n🔬 ANALYSIS - Why You're Not Seeing Full Content:")
    print("-" * 55)
    
    if results.get("web_search", {}).get("success"):
        print(f"✅ Web Search: Returns {results['web_search']['content_length']} characters")
        print("   → This is what you saw - summaries and metadata")
        print("   → NOT the full page content")
        
    if results.get("web_reading", {}).get("success"):
        print(f"✅ Web Reading: Returns {results['web_reading']['content_length']} characters")
        print("   → This is the FULL PAGE CONTENT")
        print("   → What you were looking for!")
    elif results.get("web_reading", {}).get("success") is False:
        print(f"❌ Web Reading Failed: {results['web_reading']['error']}")
    
    print("\n💡 KEY INSIGHT:")
    print("   Web Search = Discovery (find pages)")
    print("   Web Reading = Extraction (get full content)")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output/research")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = output_dir / f"web_capabilities_demo_{timestamp}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Raw results saved to: {results_file}")
    
    return results


async def main():
    """Main execution."""
    results = await demonstrate_web_capabilities()
    
    print("\n🎯 CONCLUSION:")
    print("   To get FULL PAGE CONTENT, use WEB READING")
    print("   Web search only gives you summaries and metadata")
    
    # Show specific examples
    if results.get("web_search", {}).get("success"):
        print("\n📋 WEB SEARCH GAVE YOU:")
        search_content = results["web_search"]["content"]
        if "Result 1:" in search_content:
            result1_start = search_content.find("Result 1:")
            result1_end = search_content.find("Result 2:", result1_start)
            if result1_end == -1:
                result1_end = len(search_content)
            result1_content = search_content[result1_start:result1_end]
            print(result1_content.strip())
    
    if results.get("web_reading", {}).get("success"):
        print("\n📄 WEB READING GIVES YOU:")
        reading_content = results["web_reading"]["content"]
        print(reading_content[:400] + "..." if len(reading_content) > 400 else reading_content)


if __name__ == "__main__":
    asyncio.run(main())