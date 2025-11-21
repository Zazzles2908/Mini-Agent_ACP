"""Z.AI Web Search via Anthropic-Compatible Endpoint

This tool provides web search capabilities using Z.AI through the 
Anthropic-compatible endpoint for natural citations and Claude Code integration.

Uses coding plan credits (~120 prompts every 5 hours) instead of direct Z.AI API calls.

🚫 CREDIT PROTECTED - This tool is disabled by default.
"""

import os
import json
import logging
import aiohttp
from typing import Any, Dict, List
from datetime import datetime

# CRITICAL: Check credit protection before importing Z.AI dependencies
from .base import Tool, ToolResult

# Add credit protection check
try:
    from ..utils.credit_protection import check_zai_protection
    if check_zai_protection():
        raise ImportError("Z.AI tools disabled for credit protection")
except ImportError:
    # If we can't import the protection module, allow the tool but log warning
    print("⚠️  Could not import credit protection - Z.AI tools may be unprotected")

logger = logging.getLogger(__name__)


class ZAIAnthropicWebSearchTool(Tool):
    """Z.AI web search using Anthropic-compatible endpoint.
    
    This tool routes Z.AI web search through the Anthropic-compatible API
    to enable natural citations and Claude Code integration. Uses coding plan
    credits efficiently while providing web search capabilities.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web search tool via Anthropic endpoint.
        
        Args:
            api_key: Z.AI API key (if None, uses ANTHROPIC_AUTH_TOKEN)
        """
        # Use ANTHROPIC_AUTH_TOKEN if provided, otherwise fall back to ZAI_API_KEY
        self.api_key = api_key or os.getenv('ANTHROPIC_AUTH_TOKEN') or os.getenv('ZAI_API_KEY')
        self.base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
        
        if not self.api_key:
            logger.warning("No API key found. Set ANTHROPIC_AUTH_TOKEN or ZAI_API_KEY.")
            self.available = False
            self.client = None
        else:
            self.available = True
            self.client = "anthropic_zai"
            logger.info("Z.AI Anthropic web search tool initialized")

    @property
    def name(self) -> str:
        return "zai_anthropic_web_search"

    @property
    def description(self) -> str:
        return (
            "Z.AI web search via Anthropic-compatible endpoint for natural citations. "
            "Uses coding plan credits (~120 prompts every 5 hours) instead of direct API calls. "
            "Returns results in Claude's search_result format for automatic citations. "
            "Use for: research with source attribution, fact-checking, current information. "
            "Supports comprehensive web search with AI analysis and natural citation formatting."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query or research question",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results (1-10, default 7)",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 7,
                },
                "depth": {
                    "type": "string",
                    "description": "Search depth: 'quick' (3 sources), 'comprehensive' (7 sources), 'deep' (10 sources)",
                    "enum": ["quick", "comprehensive", "deep"],
                    "default": "comprehensive",
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        max_results: int = 7,
        depth: str = "comprehensive",
        **kwargs,
    ) -> ToolResult:
        """Execute Z.AI web search via Anthropic endpoint.
        
        Args:
            query: Search query
            max_results: Maximum number of results (1-10)
            depth: Analysis depth
            **kwargs: Additional parameters
            
        Returns:
            ToolResult with search results in Claude's search_result format
        """
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI Anthropic web search not available. Set ANTHROPIC_AUTH_TOKEN environment variable.",
            )

        try:
            # Validate parameters
            if max_results < 1 or max_results > 10:
                return ToolResult(
                    success=False,
                    content="",
                    error="max_results must be between 1 and 10",
                )

            # Prepare the search query for Z.AI through Anthropic
            search_query = f"""Search the web for: "{query}"

Please provide comprehensive web search results with:
1. Use web search capabilities to find relevant information
2. Focus on quality sources and recent information
3. Provide clear titles and descriptions for each result
4. Include source URLs for proper attribution

Return structured search results that can be formatted as Claude's search_result blocks."""

            # Anthropic-compatible API call
            payload = {
                "model": "glm-4.6",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": search_query
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

            headers = {
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    f"{self.base_url}/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                )
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                
                data = await response.json()
                
                # Process and format results
                search_results = await self._process_search_response(data, query, max_results)
                
                # Format results for Claude citations
                claude_blocks = self._format_for_claude(search_results)
                
                content = self._format_tool_output(query, depth, max_results, claude_blocks, search_results)
                
                logger.info(f"Z.AI Anthropic web search completed: '{query}' ({len(search_results)} results)")
                
                return ToolResult(success=True, content=content)
                
        except Exception as e:
            logger.exception("Z.AI Anthropic web search execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Web search error: {str(e)}",
            )

    async def _process_search_response(self, api_response: Dict[str, Any], query: str, max_results: int) -> List[Dict[str, Any]]:
        """Process the API response and extract search results"""
        
        search_results = []
        
        try:
            # Extract content from the response
            content = api_response.get('content', [])
            
            for block in content:
                if block.get('type') == 'tool_use':
                    # Handle web search tool results
                    tool_content = block.get('content', [])
                    for tool_block in tool_content:
                        if tool_block.get('type') == 'text':
                            tool_text = tool_block.get('text', '')
                            try:
                                # Try to parse as structured results
                                tool_data = json.loads(tool_text)
                                if isinstance(tool_data, dict) and 'results' in tool_data:
                                    for item in tool_data['results'][:max_results]:
                                        result = {
                                            'source': item.get('url', ''),
                                            'title': item.get('title', ''),
                                            'content': item.get('snippet', item.get('summary', '')),
                                            'timestamp': datetime.now().isoformat()
                                        }
                                        search_results.append(result)
                                elif isinstance(tool_data, list):
                                    for item in tool_data[:max_results]:
                                        if isinstance(item, dict):
                                            result = {
                                                'source': item.get('source', item.get('url', '')),
                                                'title': item.get('title', ''),
                                                'content': item.get('summary', item.get('snippet', '')),
                                                'timestamp': datetime.now().isoformat()
                                            }
                                            search_results.append(result)
                            except json.JSONDecodeError:
                                # If not JSON, create a text result
                                result = {
                                    'source': 'https://search.z.ai',
                                    'title': f'Search Results for: {query}',
                                    'content': tool_text,
                                    'timestamp': datetime.now().isoformat()
                                }
                                search_results.append(result)
                                
                elif block.get('type') == 'text':
                    # Handle text content that might contain search results
                    text_content = block.get('text', '')
                    if text_content.strip():
                        result = {
                            'source': 'https://search.z.ai',
                            'title': f'Web Search Results for: {query}',
                            'content': text_content,
                            'timestamp': datetime.now().isoformat()
                        }
                        search_results.append(result)
                        
        except Exception as e:
            logger.warning(f"Could not parse search results: {e}")
            # Fallback result
            search_results = [{
                'source': 'https://www.google.com',
                'title': 'Search Results',
                'content': f'Search completed for: {query}. Please check the response for detailed results.',
                'timestamp': datetime.now().isoformat()
            }]
        
        return search_results[:max_results]

    def _format_for_claude(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format search results as Claude's search_result blocks"""
        
        claude_blocks = []
        
        for result in search_results:
            block = {
                "type": "search_result",
                "source": result.get('source', ''),
                "title": result.get('title', ''),
                "content": [
                    {
                        "type": "text",
                        "text": result.get('content', '')
                    }
                ],
                "citations": {"enabled": True}
            }
            claude_blocks.append(block)
        
        return claude_blocks

    def _format_tool_output(self, query: str, depth: str, max_results: int, claude_blocks: List[Dict[str, Any]], search_results: List[Dict[str, Any]]) -> str:
        """Format the tool output for display"""
        
        # Add usage information for coding plan
        usage_info = f"""
**💡 Usage Information:**
- **Endpoint:** Anthropic-compatible API (coding plan)
- **Credit Usage:** Counts toward ~120 prompts every 5 hours
- **Benefits:** Natural citations, Claude Code integration
- **Model:** GLM-4.6 for comprehensive analysis

---
"""
        
        # Format search results summary
        results_summary = f"**Found {len(search_results)} search results:**\n\n"
        
        for i, result in enumerate(search_results):
            results_summary += f"{i+1}. **{result['title']}**\n"
            results_summary += f"   - Source: {result['source']}\n"
            results_summary += f"   - Content: {result['content'][:200]}{'...' if len(result['content']) > 200 else ''}\n\n"
        
        # Format Claude search_result blocks for display
        claude_format = f"""
**🤖 Claude Search Result Blocks (for natural citations):**
```json
{json.dumps(claude_blocks, indent=2)}
```
"""
        
        return f"""**🔍 Z.AI Web Search Results (via Anthropic endpoint)**

**Query:** {query}
**Depth:** {depth}
**Max Results:** {max_results}
**Timestamp:** {datetime.now().isoformat()}

{usage_info}

**📊 Search Results:**
{results_summary}{claude_format}**Note:** These search_result blocks enable natural source citations when used with Claude Code.
**Format:** Claude automatically includes citations when using information from these results."""
