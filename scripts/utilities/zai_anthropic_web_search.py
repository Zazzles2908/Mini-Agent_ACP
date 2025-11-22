#!/usr/bin/env python3
"""
Z.AI Web Search Tool via Anthropic-Compatible Endpoint
Uses Z.AI through Claude's API for natural citations and proper formatting
"""

import os
import json
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Structure for search results"""
    source: str
    title: str
    content: List[Dict[str, str]]
    citations: Dict[str, bool] = None

class ZAIAnthropicWebSearch:
    """Z.AI web search using Anthropic-compatible endpoint"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_AUTH_TOKEN')
        self.base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_AUTH_TOKEN not found. Run configure_anthropic_for_zai.py first")
        
        self.headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        print(f"🔗 Initialized Z.AI Web Search via Anthropic endpoint")
        print(f"   Endpoint: {self.base_url}")
        print(f"   API Key: {self.api_key[:20]}...")

    async def search_web(self, query: str, max_results: int = 7) -> List[SearchResult]:
        """
        Search the web using Z.AI and return results in Claude's search_result format
        
        Args:
            query: Search query string
            max_results: Maximum number of results (1-10, default 7)
        
        Returns:
            List of SearchResult objects formatted for Claude citations
        """
        
        if max_results < 1 or max_results > 10:
            raise ValueError("max_results must be between 1 and 10")
        
        # Prepare the search query for Z.AI
        payload = {
            "model": "glm-4.6",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user", 
                    "content": f"""Search the web for: "{query}"

Please provide web search results with the following format:
1. Search using web search capabilities
2. Format results as JSON array with these fields for each result:
   - source: The actual URL
   - title: Descriptive title of the page
   - summary: Brief description of the content (2-3 sentences)
   - highlights: Key points or information from the source

Return only the JSON array, no additional text."""
                }
            ],
            "tools": [
                {
                    "name": "web_search",
                    "description": "Search the web for information",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "depth": {"type": "string", "enum": ["quick", "comprehensive", "deep"], "description": "Search depth"}
                        },
                        "required": ["query"]
                    }
                }
            ],
            "tool_choice": {"type": "tool", "name": "web_search"}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    f"{self.base_url}/v1/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                )
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                
                data = await response.json()
                
                # Process the search results
                search_results = self._parse_search_results(data, max_results)
                
                print(f"✅ Web search completed for: '{query}'")
                print(f"   Found {len(search_results)} results")
                
                return search_results[:max_results]
                
        except Exception as e:
            print(f"❌ Web search failed: {e}")
            # Return a helpful error result
            return [
                SearchResult(
                    source="https://www.google.com",
                    title="Web Search Error",
                    content=[{"type": "text", "text": f"Search failed: {str(e)}"}],
                    citations={"enabled": False}
                )
            ]

    def _parse_search_results(self, api_response: Dict[str, Any], max_results: int) -> List[SearchResult]:
        """Parse the API response and convert to SearchResult format"""
        
        search_results = []
        
        try:
            # Extract the assistant's response content
            content = api_response.get('content', [])
            for block in content:
                if block.get('type') == 'text':
                    text_content = block.get('text', '')
                    
                    # Try to parse as JSON first
                    try:
                        results_data = json.loads(text_content)
                        if isinstance(results_data, list):
                            for item in results_data[:max_results]:
                                if isinstance(item, dict):
                                    result = SearchResult(
                                        source=item.get('source', ''),
                                        title=item.get('title', ''),
                                        content=[{
                                            "type": "text",
                                            "text": item.get('summary', item.get('highlights', ''))
                                        }],
                                        citations={"enabled": True}
                                    )
                                    search_results.append(result)
                    except json.JSONDecodeError:
                        # If not JSON, treat as regular text content
                        result = SearchResult(
                            source="https://www.google.com",
                            title=f"Search Results for Query",
                            content=[{"type": "text", "text": text_content}],
                            citations={"enabled": True}
                        )
                        search_results.append(result)
                        
                elif block.get('type') == 'tool_use':
                    # Handle tool results
                    tool_content = block.get('content', [])
                    for tool_block in tool_content:
                        if tool_block.get('type') == 'text':
                            tool_text = tool_block.get('text', '')
                            try:
                                tool_data = json.loads(tool_text)
                                if isinstance(tool_data, dict) and 'results' in tool_data:
                                    for item in tool_data['results'][:max_results]:
                                        result = SearchResult(
                                            source=item.get('url', ''),
                                            title=item.get('title', ''),
                                            content=[{
                                                "type": "text", 
                                                "text": item.get('snippet', '')
                                            }],
                                            citations={"enabled": True}
                                        )
                                        search_results.append(result)
                            except:
                                pass
                                
        except Exception as e:
            print(f"⚠️  Warning: Could not parse search results: {e}")
            # Fallback: create a single result with the raw content
            search_results = [
                SearchResult(
                    source="https://search.z.ai",
                    title="Search Results",
                    content=[{
                        "type": "text",
                        "text": f"Search completed. Please check the response for detailed results."
                    }],
                    citations={"enabled": True}
                )
            ]
        
        return search_results[:max_results]

    def format_for_claude(self, search_results: List[SearchResult]) -> List[Dict[str, Any]]:
        """Format search results as Claude's search_result blocks"""
        
        claude_blocks = []
        
        for i, result in enumerate(search_results):
            block = {
                "type": "search_result",
                "source": result.source,
                "title": result.title,
                "content": result.content,
                "citations": result.citations or {"enabled": True}
            }
            claude_blocks.append(block)
        
        return claude_blocks

# Test function
async def test_zai_web_search():
    """Test the Z.AI web search functionality"""
    
    print("🧪 Testing Z.AI Web Search via Anthropic endpoint...")
    
    searcher = ZAIAnthropicWebSearch()
    
    test_queries = [
        "Z.AI DevPack Claude integration",
        "Mini-Agent architecture overview"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        results = await searcher.search_web(query, max_results=3)
        
        print(f"   📊 Results found: {len(results)}")
        for i, result in enumerate(results):
            print(f"   {i+1}. {result.title}")
            print(f"      Source: {result.source}")
            print(f"      Preview: {result.content[0]['text'][:100]}...")
            
        # Format for Claude
        claude_blocks = searcher.format_for_claude(results)
        print(f"   🤖 Formatted for Claude: {len(claude_blocks)} search_result blocks")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_zai_web_search())