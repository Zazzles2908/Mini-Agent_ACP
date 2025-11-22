"""Simple Web Search Tool for Mini-Max M2

Simple, clean implementation using Z.AI GLM-4.6
"""

import os
import aiohttp
import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Constants
GLM_4_6_MODEL = "glm-4.6"  # Primary model
BASE_URL = "https://api.z.ai/api/coding/paas/v4"
MAX_TOKENS = 2000
MAX_RESULTS = 5

class SimpleWebSearch:
    """Simple web search using Z.AI GLM-4.6"""
    
    def __init__(self):
        self.api_key = os.getenv('ZAI_API_KEY')
        self.base_url = BASE_URL
        self.model = GLM_4_6_MODEL
        
        if not self.api_key:
            logger.warning("Z.AI API key not found - web search unavailable")
            self.available = False
            return
            
        if not self._check_dependencies():
            self.available = False
            return
            
        self.available = True
        logger.info(f"Web search initialized with {self.model}")
    
    def _check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        try:
            import aiohttp
            return True
        except ImportError:
            logger.error("aiohttp not available - install with: pip install aiohttp")
            return False
    
    async def search(self, query: str, max_results: int = MAX_RESULTS) -> Dict[str, Any]:
        """Perform web search"""
        if not self.available:
            return {
                "success": False,
                "content": "",
                "error": "Web search not available - API key or dependencies missing"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user", 
                            "content": f"Search the web for: {query}. Provide {max_results} relevant results with URLs and summaries."
                        }
                    ],
                    "max_tokens": MAX_TOKENS,
                    "stream": False
                }
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        
                        return {
                            "success": True,
                            "content": content,
                            "error": None
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "content": "",
                            "error": f"API error {response.status}: {error_text}"
                        }
                        
        except Exception as e:
            logger.exception("Web search failed")
            return {
                "success": False,
                "content": "",
                "error": f"Search failed: {str(e)}"
            }

# Global instance
_web_search = None

def get_web_search() -> SimpleWebSearch:
    """Get web search instance"""
    global _web_search
    if _web_search is None:
        _web_search = SimpleWebSearch()
    return _web_search

async def web_search(query: str, max_results: int = MAX_RESULTS) -> Dict[str, Any]:
    """Simple web search function"""
    search_tool = get_web_search()
    return await search_tool.search(query, max_results)

# Test function
async def test_web_search():
    """Test web search functionality"""
    print("🧪 Testing simple web search...")
    
    # Check dependencies
    try:
        import aiohttp
        print("✅ aiohttp available")
    except ImportError:
        print("❌ aiohttp not available - install first")
        return False
    
    # Check API key
    api_key = os.getenv('ZAI_API_KEY')
    if not api_key:
        print("❌ Z.AI API key not found")
        return False
    
    print("✅ Dependencies and API key check passed")
    
    # Test search
    result = await web_search("Python programming", max_results=3)
    
    if result["success"]:
        print("✅ Web search successful")
        print(f"   Content length: {len(result['content'])} chars")
        return True
    else:
        print(f"❌ Web search failed: {result['error']}")
        return False

if __name__ == "__main__":
    asyncio.run(test_web_search())
