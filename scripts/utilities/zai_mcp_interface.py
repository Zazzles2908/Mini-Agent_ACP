#!/usr/bin/env python3
"""
Z.AI MCP Search Interface
========================
MCP-compatible implementation that utilizes free Lite Plan quotas.
"""

import os
import asyncio
import json
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime

class ZAIMCPSearchInterface:
    def __init__(self):
        self.zai_api_key = os.getenv('ZAI_API_KEY')
        self.search_count = 0
        self.reader_count = 0
        self.max_searches = 100  # Lite Plan limit
        self.max_readers = 100   # Lite Plan limit
        self.base_url = "https://api.z.ai/api/coding/paas/v4"
        
    async def search(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """MCP-compatible web search with quota tracking"""
        
        # Check quota before proceeding
        if self.search_count >= self.max_searches:
            return {
                'success': False,
                'error': 'Search quota exceeded (100/100 used)',
                'fallback_required': True,
                'quota_remaining': self.max_searches - self.search_count
            }
        
        # Optimize for minimal quota consumption
        max_results = min(max_results, 3)  # Conservative limit for Lite Plan
        
        print(f"🔍 MCP Search #{self.search_count + 1}: {query[:50]}...")
        
        try:
            # Direct Z.AI API call with optimized parameters
            payload = {
                "search_engine": "search-std",  # Use standard for efficiency
                "search_query": query,
                "count": max_results,
                "search_recency_filter": "noLimit"
            }
            
            headers = {
                "Authorization": f"Bearer {self.zai_api_key}",
                "Content-Type": "application/json",
                "Accept-Language": "en-US,en"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/web_search",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        search_results = result.get("search_result", [])
                        
                        # Format results for MCP consumption
                        formatted_results = []
                        for item in search_results:
                            formatted_results.append({
                                'title': item.get('title', 'N/A'),
                                'url': item.get('link', ''),
                                'snippet': item.get('content', '')[:200] + '...'  # Snippet for efficiency
                            })
                        
                        # Increment quota usage
                        self.search_count += 1
                        
                        return {
                            'success': True,
                            'query': query,
                            'results': formatted_results,
                            'result_count': len(formatted_results),
                            'quota_used': self.search_count,
                            'quota_remaining': self.max_searches - self.search_count,
                            'mcp_mode': True,
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"API error: {response.status}",
                            'quota_used': self.search_count
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f"Search failed: {str(e)}",
                'quota_used': self.search_count
            }
    
    async def read(self, url: str, max_length: int = 1000) -> Dict[str, Any]:
        """MCP-compatible web reader with quota tracking"""
        
        # Check quota before proceeding
        if self.reader_count >= self.max_readers:
            return {
                'success': False,
                'error': 'Reader quota exceeded (100/100 used)',
                'fallback_required': True,
                'quota_remaining': self.max_readers - self.reader_count
            }
        
        print(f"📄 MCP Reader #{self.reader_count + 1}: {url}")
        
        try:
            payload = {
                "url": url,
                "return_format": "text",
                "retain_images": False  # Disable for quota efficiency
            }
            
            headers = {
                "Authorization": f"Bearer {self.zai_api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/reader",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=45)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        reader_result = result.get("web_page_reader_result", {})
                        
                        content = reader_result.get("content", "")
                        if len(content) > max_length:
                            content = content[:max_length] + "\n\n[Content truncated for quota efficiency]"
                        
                        # Increment quota usage
                        self.reader_count += 1
                        
                        return {
                            'success': True,
                            'url': url,
                            'content': content,
                            'title': reader_result.get('title', 'N/A'),
                            'quota_used': self.reader_count,
                            'quota_remaining': self.max_readers - self.reader_count,
                            'mcp_mode': True,
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"Reader error: {response.status}",
                            'quota_used': self.reader_count
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': f"Reader failed: {str(e)}",
                'quota_used': self.reader_count
            }
    
    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota usage status"""
        return {
            'search_quota': {
                'used': self.search_count,
                'remaining': self.max_searches - self.search_count,
                'limit': self.max_searches,
                'percentage_used': (self.search_count / self.max_searches) * 100
            },
            'reader_quota': {
                'used': self.reader_count,
                'remaining': self.max_readers - self.reader_count,
                'limit': self.max_readers,
                'percentage_used': (self.reader_count / self.max_readers) * 100
            }
        }
    
    def reset_quota_counters(self):
        """Reset quota counters (call when quota resets)"""
        self.search_count = 0
        self.reader_count = 0
        print("✅ Quota counters reset for new cycle")

# Smart MCP wrapper for seamless integration
def smart_search(query: str, use_mcp_limit: bool = True) -> Dict[str, Any]:
    """Smart search that uses MCP first, then falls back"""
    
    mcp_interface = ZAIMCPSearchInterface()
    
    if use_mcp_limit:
        status = mcp_interface.get_quota_status()
        if status['search_quota']['remaining'] > 0:
            # Use MCP (free quota)
            result = asyncio.run(mcp_interface.search(query, max_results=3))
            result['search_method'] = 'mcp_free'
            return result
        else:
            # Fallback to external API
            return {
                'success': False,
                'error': 'MCP quota exhausted',
                'fallback_required': True,
                'search_method': 'external_required'
            }
    else:
        # Use direct MCP without limits (not recommended)
        result = asyncio.run(mcp_interface.search(query, max_results=5))
        result['search_method'] = 'mcp_unlimited'
        return result

# Usage examples
async def main():
    # Test MCP interface
    mcp = ZAIMCPSearchInterface()
    
    print("🧪 Testing Z.AI MCP Integration...")
    
    # Test search
    result = await mcp.search("python web scraping", max_results=2)
    print(f"Search result: {result.get('success', False)}")
    if result.get('success'):
        print(f"Results: {len(result.get('results', []))}")
    
    # Test quota status
    status = mcp.get_quota_status()
    print(f"Quota status: {status}")
    
    # Test smart search
    smart_result = smart_search("artificial intelligence trends")
    print(f"Smart search result: {smart_result.get('search_method')}")

if __name__ == "__main__":
    asyncio.run(main())
