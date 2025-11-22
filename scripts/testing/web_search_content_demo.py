#!/usr/bin/env python3
"""
Simple demonstration of Z.AI web search showing exactly what content it returns.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Import Z.AI tools
sys.path.append(str(Path(__file__).parent.parent))
from mini_agent.tools.zai_tools import ZAIWebSearchTool


async def show_web_search_content():
    """Show exactly what web search returns."""
    
    print("🔍 Z.AI WEB SEARCH CONTENT DEMONSTRATION")
    print("=" * 60)
    print("Target: Z.AI DevPack Claude documentation")
    print("=" * 60)
    
    # Initialize tool
    search_tool = ZAIWebSearchTool()
    
    try:
        # Perform web search
        result = await search_tool.execute(
            query="Z.AI DevPack Claude integration tools documentation",
            depth="comprehensive",
            search_engine="search-prime",
            model="glm-4.5"
        )
        
        if result.success:
            print("✅ WEB SEARCH SUCCESSFUL!")
            print(f"\n📊 Content Analysis:")
            print(f"   • Total characters: {len(result.content)}")
            print(f"   • Total words (approx): {len(result.content.split())}")
            
            print(f"\n📋 COMPLETE WEB SEARCH CONTENT:")
            print("=" * 60)
            print(result.content)
            print("=" * 60)
            
            # Analysis
            print(f"\n🔬 ANALYSIS:")
            print(f"   • This is what you see when using web search")
            print(f"   • It contains SUMMARIES and METADATA, not full page content")
            print(f"   • Each result shows title, URL, and brief description")
            print(f"   • This is why you're not seeing the full information")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("output/research")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save as markdown for easy reading
            md_file = output_dir / f"web_search_content_demo_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"""# Z.AI Web Search Content Demonstration

**Timestamp**: {datetime.now().isoformat()}
**Query**: Z.AI DevPack Claude integration tools documentation

## What Web Search Returns

Web search provides **summaries and metadata**, not full page content:

### Content Analysis
- **Total Characters**: {len(result.content)}
- **Type**: Search result summaries with citations
- **Purpose**: Discovery and quick overview

### Raw Content

{result.content}

## Key Insight

**Web Search = Discovery** (find relevant pages)
**Web Reading = Extraction** (get full content)

To see the FULL content of a page, you need to use web reading, not web search.
""")
            
            # Save as JSON for programmatic access
            json_file = output_dir / f"web_search_content_demo_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "query": "Z.AI DevPack Claude integration tools documentation",
                    "content_length": len(result.content),
                    "content": result.content,
                    "analysis": {
                        "type": "web_search_results",
                        "purpose": "discovery_and_summaries",
                        "not_full_content": True
                    }
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Files saved:")
            print(f"   📄 {md_file}")
            print(f"   📊 {json_file}")
            
        else:
            print(f"❌ WEB SEARCH FAILED: {result.error}")
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    asyncio.run(show_web_search_content())