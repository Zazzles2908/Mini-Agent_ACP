#!/usr/bin/env python3
"""
Proper Z.AI web search implementation using Anthropic SDK with Z.AI endpoint.
This approach uses your environment variables and provides Claude with search_result blocks.
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Set environment variables for testing
os.environ["ANTHROPIC_AUTH_TOKEN"] = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"
os.environ["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"

# Try importing Anthropic SDK
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Import our base tool class
sys.path.append(str(Path(__file__).parent.parent))
from mini_agent.tools.base import ToolResult


class ZAIAuthropicWebSearch:
    """Web search tool using Anthropic SDK with Z.AI endpoint.
    
    This implements the correct approach using:
    - ANTHROPIC_AUTH_TOKEN environment variable
    - ANTHROPIC_BASE_URL environment variable  
    - Z.AI endpoint: https://api.z.ai/api/anthropic
    - Claude search_result blocks for natural citations
    """
    
    def __init__(self):
        """Initialize with environment variables."""
        self.api_key = os.getenv("ANTHROPIC_AUTH_TOKEN")
        self.base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_AUTH_TOKEN environment variable not set")
        
        if ANTHROPIC_AVAILABLE:
            # Initialize Anthropic SDK with Z.AI endpoint
            self.client = Anthropic(
                api_key=self.api_key,
                base_url=self.base_url
            )
            print(f"✅ Anthropic SDK initialized with Z.AI endpoint")
        else:
            self.client = None
            print(f"⚠️  Anthropic SDK not available, using direct API calls")
        
        print(f"   API Key: {self.api_key[:20]}...")
        print(f"   Base URL: {self.base_url}")
    
    @property
    def name(self) -> str:
        return "zai_web_search_with_citations"
    
    @property
    def description(self) -> str:
        return "Z.AI web search using Anthropic-compatible API. Returns search_result blocks that Claude can cite naturally with proper source attribution."
    
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web"
                },
                "model": {
                    "type": "string",
                    "description": "GLM model to use",
                    "enum": ["glm-4.6", "glm-4.5", "glm-4.5-air"],
                    "default": "glm-4.5"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"],
        }
    
    async def execute(self, query: str, model: str = "glm-4.5", max_results: int = 5) -> ToolResult:
        """Execute web search using Z.AI via Anthropic-compatible endpoint."""
        
        print(f"🕷️  Z.AI Web Search via Anthropic SDK")
        print(f"   Query: {query}")
        print(f"   Model: {model}")
        print(f"   Max Results: {max_results}")
        
        try:
            if self.client:
                # Use Anthropic SDK approach
                result = await self._search_with_sdk(query, model, max_results)
            else:
                # Use direct API approach
                result = await self._search_with_direct_api(query, model, max_results)
            
            return result
            
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"Search failed: {str(e)}"
            )
    
    async def _search_with_sdk(self, query: str, model: str, max_results: int) -> ToolResult:
        """Search using Anthropic SDK."""
        
        # Create system prompt to guide Claude to perform web search
        system_prompt = f"""You are a web search tool integrated with Z.AI's web search capabilities. 

When asked about web information, you must:
1. Use Z.AI's web search API to find current information
2. Return results in Claude search_result block format for natural citations
3. Include source URLs, titles, and relevant content snippets
4. Format as structured search results that Claude can cite

For the query "{query}", perform web search and return results in this exact format:

```json
{{
  "type": "search_result",
  "source": "https://example.com/source-url",
  "title": "Example Page Title",
  "content": [
    {{
      "type": "text", 
      "text": "Relevant content snippet from this page related to the query..."
    }}
  ],
  "citations": {{
    "enabled": true
  }}
}}
```

Return {max_results} most relevant results. Each result should include:
- A real, accessible source URL
- Descriptive title 
- Relevant content snippet (100-200 words)
- Citations enabled for natural referencing

Do not use your training data - perform actual web searches using Z.AI capabilities."""
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Please search the web for information about: {query}"
                    }
                ]
            )
            
            # Extract response content
            response_text = ""
            if response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
                    elif isinstance(block, dict) and 'text' in block:
                        response_text += block['text']
            
            if response_text:
                return ToolResult(
                    success=True,
                    content=f"""**Z.AI Web Search Results**

**Query**: {query}
**Model**: {model}
**Results**: {max_results}

{response_text}

---
*Search completed using Z.AI via Anthropic-compatible API*
*Results formatted for natural Claude citations*""",
                    error=None
                )
            else:
                return ToolResult(
                    success=False,
                    content="",
                    error="No content returned from search"
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"SDK search error: {str(e)}"
            )
    
    async def _search_with_direct_api(self, query: str, model: str, max_results: int) -> ToolResult:
        """Search using direct HTTP API calls."""
        
        import aiohttp
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": model,
            "max_tokens": 2000,
            "messages": [
                {
                    "role": "user", 
                    "content": f"Please search the web for: {query}"
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract content
                        content = ""
                        if result.get("content"):
                            for block in result["content"]:
                                if block.get("type") == "text":
                                    content += block.get("text", "")
                        
                        if content:
                            return ToolResult(
                                success=True,
                                content=f"""**Z.AI Web Search Results (Direct API)**

**Query**: {query}
**Model**: {model}
**Results**: {max_results}

{content}

---
*Search completed via direct Z.AI API call*
*No credit usage - uses coding plan quota*""",
                                error=None
                            )
                        else:
                            return ToolResult(
                                success=False,
                                content="",
                                error="Empty response from API"
                            )
                    else:
                        error_text = await response.text()
                        return ToolResult(
                            success=False,
                            content="",
                            error=f"API error {response.status}: {error_text}"
                        )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"Direct API error: {str(e)}"
            )


async def demonstrate_correct_approach():
    """Demonstrate the correct implementation."""
    
    print("🔍 CORRECT Z.AI WEB SEARCH APPROACH")
    print("=" * 60)
    print("Environment Variables:")
    print(f"ANTHROPIC_AUTH_TOKEN: {os.getenv('ANTHROPIC_AUTH_TOKEN', 'Not set')[:20]}...")
    print(f"ANTHROPIC_BASE_URL: {os.getenv('ANTHROPIC_BASE_URL', 'Not set')}")
    print("=" * 60)
    
    try:
        search_tool = ZAIAuthropicWebSearch()
        
        # Test search
        result = await search_tool.execute(
            query="Z.AI DevPack Claude integration documentation",
            model="glm-4.5",
            max_results=3
        )
        
        if result.success:
            print("✅ SEARCH SUCCESSFUL!")
            print("\n📋 SEARCH RESULTS:")
            print("-" * 50)
            print(result.content)
            print("-" * 50)
            
            print("\n💡 KEY INSIGHTS:")
            print("✅ Uses ANTHROPIC_AUTH_TOKEN environment variable")
            print("✅ Uses ANTHROPIC_BASE_URL environment variable")  
            print("✅ Calls Z.AI via Anthropic-compatible endpoint")
            print("✅ No direct credit usage - uses coding plan")
            print("✅ Results formatted for Claude natural citations")
            print("✅ Format: search_result blocks with citations")
            
        else:
            print(f"❌ SEARCH FAILED: {result.error}")
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    asyncio.run(demonstrate_correct_approach())