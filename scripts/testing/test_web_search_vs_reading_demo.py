#!/usr/bin/env python3
"""
Demonstration script to show the difference between web search and web reading
using Z.AI APIs with raw output capture.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

# Import our Z.AI tools
import sys
sys.path.append(str(Path(__file__).parent.parent))

from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool


async def demonstrate_web_search_vs_reading():
    """Demonstrate the difference between web search and web reading."""
    
    target_url = "https://docs.z.ai/devpack/tool/claude"
    
    print("🔍 Z.AI Web Search vs Web Reading Demonstration")
    print("=" * 60)
    print(f"Target URL: {target_url}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Initialize tools
    search_tool = ZAIWebSearchTool()
    reader_tool = ZAIWebReaderTool()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "target_url": target_url,
        "web_search_results": None,
        "web_reading_results": None,
        "comparison_analysis": None
    }
    
    # Test 1: Web Search
    print("\n🕷️  TEST 1: WEB SEARCH")
    print("-" * 30)
    try:
        search_result = await search_tool.execute(
            query="Z.AI DevPack Claude integration tools",
            depth="comprehensive",
            search_engine="search-prime",
            model="glm-4.5"
        )
        
        print("✅ Web Search SUCCESSFUL")
        print(f"Search response type: {type(search_result)}")
        
        # Display search results
        if hasattr(search_result, 'content'):
            print(f"Search content preview (first 500 chars):")
            print("-" * 50)
            print(search_result.content[:500] + "..." if len(search_result.content) > 500 else search_result.content)
            print("-" * 50)
        elif isinstance(search_result, dict):
            print(f"Search keys: {list(search_result.keys())}")
            
            if 'results' in search_result:
                print(f"Number of search results: {len(search_result['results'])}")
                for i, result in enumerate(search_result['results'][:3], 1):
                    print(f"\nResult {i}:")
                    if isinstance(result, dict):
                        print(f"  Title: {result.get('title', 'N/A')}")
                        print(f"  URL: {result.get('url', 'N/A')}")
                        print(f"  Summary: {result.get('summary', 'N/A')[:100]}...")
        
        results["web_search_results"] = {
            "success": search_result.success,
            "content": search_result.content,
            "error": search_result.error,
            "type": "ToolResult"
        }
        
    except Exception as e:
        print(f"❌ Web Search FAILED: {str(e)}")
        results["web_search_results"] = {"error": str(e)}
    
    # Test 2: Web Reading
    print("\n📖 TEST 2: WEB READING")
    print("-" * 30)
    try:
        reading_result = await reader_tool.execute(
            url=target_url,
            return_format="markdown",
            retain_images=False
        )
        
        print("✅ Web Reading SUCCESSFUL")
        print(f"Reading response type: {type(reading_result)}")
        
        # Display reading results
        if hasattr(reading_result, 'content'):
            content = reading_result.content
            print(f"Content length: {len(content)} characters")
            print(f"Content preview (first 500 chars):")
            print("-" * 50)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-" * 50)
        elif isinstance(reading_result, dict):
            print(f"Reading keys: {list(reading_result.keys())}")
            
            if 'content' in reading_result:
                content = reading_result['content']
                print(f"Content length: {len(content)} characters")
                print(f"Content preview (first 500 chars):")
                print("-" * 50)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 50)
        
        results["web_reading_results"] = {
            "success": reading_result.success,
            "content": reading_result.content,
            "error": reading_result.error,
            "type": "ToolResult"
        }
        
    except Exception as e:
        print(f"❌ Web Reading FAILED: {str(e)}")
        results["web_reading_results"] = {"error": str(e)}
    
    # Test 3: Direct API call analysis
    print("\n🔧 TEST 3: RAW API CALL ANALYSIS")
    print("-" * 30)
    
    try:
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {search_tool.api_key}",
            "Content-Type": "application/json"
        }
        
        # Get base URL from client
        base_url = "https://api.z.ai/api/coding/paas/v4"  # Coding Plan endpoint
        
        # Direct web search API call
        search_payload = {
            "query": "Z.AI DevPack Claude integration documentation",
            "depth": "comprehensive",
            "search_engine": "search-prime",
            "model": "glm-4.5",
            "max_results": 5
        }
        
        async with aiohttp.ClientSession() as session:
            print("Making direct API call to Z.AI web search...")
            async with session.post(
                f"{base_url}/web_search",
                headers=headers,
                json=search_payload
            ) as response:
                
                print(f"Status: {response.status}")
                print(f"Headers: {dict(response.headers)}")
                
                raw_response = await response.text()
                print(f"Raw response length: {len(raw_response)} characters")
                
                # Try to parse as JSON
                try:
                    json_response = json.loads(raw_response)
                    print("✅ Response is valid JSON")
                    print(f"Response keys: {list(json_response.keys())}")
                    
                    if 'results' in json_response:
                        print(f"Number of results: {len(json_response['results'])}")
                        for i, result in enumerate(json_response['results'][:2], 1):
                            print(f"\nResult {i} raw data:")
                            print(json.dumps(result, indent=2)[:300] + "...")
                    
                    results["raw_api_response"] = json_response
                    
                except json.JSONDecodeError:
                    print("❌ Response is not valid JSON")
                    print("Raw response (first 500 chars):")
                    print(raw_response[:500])
                    results["raw_api_response"] = raw_response
        
    except Exception as e:
        print(f"❌ Raw API call FAILED: {str(e)}")
        results["raw_api_response"] = {"error": str(e)}
    
    # Analysis
    print("\n📊 ANALYSIS")
    print("-" * 30)
    
    analysis = {
        "web_search_provides": [
            "Metadata and snippets",
            "Multiple source results",
            "Ranked by relevance",
            "Summaries, not full content",
            "Structured data with citations"
        ],
        "web_reading_provides": [
            "Full page content extraction",
            "Complete article text",
            "May include images/formatting",
            "Raw HTML converted to text/markdown",
            "Direct content access"
        ],
        "key_differences": [
            "Search = Discovery (what exists)",
            "Reading = Extraction (get the content)",
            "Search = Multiple sources",
            "Reading = Single page focus",
            "Search = Summaries",
            "Reading = Full content"
        ],
        "use_cases": {
            "web_search": [
                "Finding relevant pages",
                "Getting overview of topics",
                "Discovering multiple sources",
                "Getting quick summaries"
            ],
            "web_reading": [
                "Extracting full content",
                "Reading complete articles",
                "Getting detailed information",
                "Processing specific pages"
            ]
        }
    }
    
    results["comparison_analysis"] = analysis
    
    print("✅ Key Differences Identified:")
    for key, value in analysis.items():
        if isinstance(value, list):
            print(f"\n{key.replace('_', ' ').title()}:")
            for item in value:
                print(f"  • {item}")
    
    return results


async def main():
    """Main execution function."""
    results = await demonstrate_web_search_vs_reading()
    
    # Save results to output directory
    output_dir = Path("output/research")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save comprehensive results
    results_file = output_dir / f"zai_web_search_vs_reading_demo_{timestamp}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Create readable summary
    summary_file = output_dir / f"zai_demo_summary_{timestamp}.md"
    
    summary_content = f"""# Z.AI Web Search vs Web Reading Demonstration

**Timestamp**: {results['timestamp']}
**Target URL**: {results['target_url']}

## Executive Summary

This demonstration shows the key differences between Z.AI's web search and web reading capabilities.

## Key Differences

### Web Search Provides:
{chr(10).join(f"• {item}" for item in results['comparison_analysis']['web_search_provides'])}

### Web Reading Provides:
{chr(10).join(f"• {item}" for item in results['comparison_analysis']['web_reading_provides'])}

## Why You're Not Seeing Full Page Content

**The Issue**: Web search returns **summaries and metadata**, not full page content.

**The Solution**: Use web reading for full content extraction.

## Use Cases

### Use Web Search When:
{chr(10).join(f"• {item}" for item in results['comparison_analysis']['use_cases']['web_search'])}

### Use Web Reading When:
{chr(10).join(f"• {item}" for item in results['comparison_analysis']['use_cases']['web_reading'])}

## Technical Details

- **Search Endpoint**: `{results['target_url']}/web_search`
- **Reading Endpoint**: `{results['target_url']}/reader`
- **Search Returns**: Structured result blocks with citations
- **Reading Returns**: Full page content in markdown/text format

## Raw Results Location

Full raw API responses and detailed results saved in:
`{results_file}`

---

*Generated by Z.AI demonstration script*
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"📄 Summary saved to: {summary_file}")
    print("\n🎯 CONCLUSION: Use web READING, not web SEARCH, for full page content!")


if __name__ == "__main__":
    asyncio.run(main())