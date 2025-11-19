"""
Native GLM SDK Integration with Self-Awareness
Uses the actual zai SDK with GLM 4.5+ models and native web search/reading
"""

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from zai import ZaiClient
    ZAI_AVAILABLE = True
except ImportError:
    ZAI_AVAILABLE = False
    print("Warning: zai-sdk not available. Install with: pip install zai-sdk")

class NativeGLMClient:
    """
    Native GLM client using the actual zai SDK with self-awareness integration
    """
    
    def __init__(self, api_key: str, observability_path: str = ".observability"):
        self.api_key = api_key
        self.observability_path = Path(observability_path)
        
        # Initialize native zai client
        if ZAI_AVAILABLE:
            try:
                self.client = ZaiClient(api_key=api_key)
                print(f"Native GLM client initialized with GLM 4.5+ capabilities")
            except Exception as e:
                print(f"Failed to initialize GLM client: {e}")
                self.client = None
        else:
            self.client = None
        
        # GLM model configuration - using glm4.5 as minimum
        self.glm_models = {
            "glm4.5": {
                "native_name": "glm-4.5",
                "description": "Minimum GLM model - strong agent capabilities",
                "capabilities": ["reasoning", "planning", "tool_integration", "complex_analysis", "native_web_search"],
                "preferred_for": ["complex_tasks", "planning", "analysis", "decision_making"]
            },
            "glm4-air": {
                "native_name": "glm-4-air",
                "description": "Lightweight GLM model for quick responses",
                "capabilities": ["fast_responses", "simple_tasks", "quick_queries"],
                "preferred_for": ["quick_queries", "simple_operations", "basic_responses"]
            },
            "glm4.6": {
                "native_name": "glm-4.6", 
                "description": "Latest flagship GLM model",
                "capabilities": ["superior_reasoning", "coding", "agent_native", "advanced_web_search"],
                "preferred_for": ["complex_coding", "advanced_reasoning", "agent_tasks"]
            }
        }
        
        # Task complexity scoring for model selection
        self.complexity_indicators = {
            "high": ["analyze", "plan", "design", "create", "optimize", "integrate", "evaluate", "research"],
            "medium": ["modify", "update", "implement", "configure", "organize", "process"],
            "low": ["list", "show", "get", "read", "simple", "basic", "check"]
        }
    
    def _assess_task_complexity(self, task_description: str) -> int:
        """Assess task complexity for model selection"""
        task_lower = task_description.lower()
        complexity_score = 1
        
        # Check complexity indicators
        for level, indicators in self.complexity_indicators.items():
            for indicator in indicators:
                if indicator in task_lower:
                    if level == "high":
                        complexity_score = max(complexity_score, 8)
                    elif level == "medium":
                        complexity_score = max(complexity_score, 5)
                    else:
                        complexity_score = max(complexity_score, 3)
        
        # Adjust for multiple operations and web-related tasks
        if len(task_description.split()) > 10:
            complexity_score += 1
        if any(word in task_lower for word in ["search", "research", "browse", "web", "internet"]):
            complexity_score += 2  # Web tasks are inherently more complex
        
        return min(complexity_score, 10)
    
    def _select_optimal_model(self, task_description: str, complexity_score: int) -> str:
        """Select optimal GLM model using native model names"""
        # Web-related tasks need GLM 4.5+ for native search capabilities
        task_lower = task_description.lower()
        if any(word in task_lower for word in ["search", "research", "browse", "web", "internet"]):
            if complexity_score >= 7:
                return "glm4.6"  # Latest flagship for complex web tasks
            else:
                return "glm4.5"  # Minimum for web capabilities
        
        # Other complex tasks
        elif complexity_score >= 6:
            return "glm4.5"
        elif complexity_score <= 3:
            return "glm4-air"
        else:
            return "glm4.5"  # Default to more capable model
    
    def _get_native_model_name(self, model_key: str) -> str:
        """Get the native SDK model name"""
        return self.glm_models.get(model_key, {}).get("native_name", "glm-4.5")
    
    async def native_web_search(self, query: str, max_results: int = 10, 
                              domain_filter: Optional[str] = None,
                              recency_filter: str = "noLimit") -> Dict[str, Any]:
        """
        Perform native GLM web search using the SDK's web_search method
        """
        
        if not self.client or not ZAI_AVAILABLE:
            return self._fallback_search(query, max_results)
        
        try:
            # Use native web search API
            search_response = self.client.web_search.web_search(
                search_engine="search-prime",
                search_query=query,
                count=max_results,
                search_domain_filter=domain_filter,
                search_recency_filter=recency_filter,
                content_size="high"
            )
            
            # Process results
            results = []
            if hasattr(search_response, 'results'):
                for result in search_response.results:
                    results.append({
                        "title": result.title if hasattr(result, 'title') else "",
                        "url": result.link if hasattr(result, 'link') else "",
                        "content": result.content if hasattr(result, 'content') else "",
                        "source": result.media if hasattr(result, 'media') else "",
                        "publish_date": result.publish_date if hasattr(result, 'publish_date') else "",
                        "icon": result.icon if hasattr(result, 'icon') else ""
                    })
            
            return {
                "query": query,
                "native_search": True,
                "results": results,
                "total_results": len(results),
                "search_engine": "search-prime",
                "glml_integration": "native_zai_sdk"
            }
            
        except Exception as e:
            print(f"Native search failed: {e}")
            return self._fallback_search(query, max_results)
    
    async def chat_with_web_search(self, query: str, model_preference: str = None) -> Dict[str, Any]:
        """
        Use GLM chat with native web search tool integration
        """
        
        if not self.client or not ZAI_AVAILABLE:
            return {"error": "GLM client not available", "fallback": True}
        
        # Assess complexity and select model
        complexity = self._assess_task_complexity(query)
        selected_model_key = model_preference or self._select_optimal_model(query, complexity)
        native_model_name = self._get_native_model_name(selected_model_key)
        
        try:
            # Define web search tool
            web_search_tool = {
                "type": "web_search",
                "web_search": {
                    "enable": "True",
                    "search_engine": "search-prime",
                    "search_result": "True",
                    "search_prompt": f"Analyze the search results for: {query}",
                    "count": "5",
                    "content_size": "high"
                }
            }
            
            # Create chat completion with web search
            response = self.client.chat.completions.create(
                model=native_model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an intelligent assistant with native web search capabilities. Use the web search tool when needed to provide accurate, up-to-date information."
                    },
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                tools=[web_search_tool],
                tool_choice="auto"
            )
            
            return {
                "query": query,
                "model_used": native_model_name,
                "complexity_score": complexity,
                "response": response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response),
                "web_search_enabled": True,
                "glml_integration": "native_zai_sdk_with_tools"
            }
            
        except Exception as e:
            print(f"Chat with web search failed: {e}")
            return {"error": str(e), "model_used": native_model_name}
    
    async def enhanced_web_research(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Enhanced web research combining direct search and chat with search
        """
        
        # Step 1: Direct native search
        search_results = await self.native_web_search(query, max_results)
        
        # Step 2: Chat with web search for analysis
        chat_results = await self.chat_with_web_search(query)
        
        return {
            "original_query": query,
            "native_search_results": search_results,
            "chat_analysis": chat_results,
            "research_integration": {
                "direct_search": search_results.get("total_results", 0),
                "ai_analysis": "completed" if "response" in chat_results else "failed",
                "glml_capabilities": "native_zai_sdk_fully_integrated"
            }
        }
    
    def _fallback_search(self, query: str, max_results: int) -> Dict[str, Any]:
        """Fallback when GLM SDK unavailable"""
        return {
            "query": query,
            "fallback_mode": True,
            "message": "Native GLM SDK not available",
            "results": [],
            "recommendation": "Install zai-sdk: pip install zai-sdk",
            "glml_integration": "fallback_mode"
        }
    
    def get_sdk_info(self) -> Dict[str, Any]:
        """Get information about GLM SDK capabilities"""
        
        return {
            "sdk_available": ZAI_AVAILABLE,
            "client_initialized": self.client is not None,
            "native_models": self.glm_models,
            "model_selection_strategy": "complexity_based",
            "web_capabilities": {
                "native_web_search": ZAI_AVAILABLE,
                "chat_with_tools": ZAI_AVAILABLE,
                "search_prime_engine": ZAI_AVAILABLE,
                "enhanced_reading": ZAI_AVAILABLE
            },
            "integration_status": "native_zai_sdk" if ZAI_AVAILABLE else "fallback_mode"
        }

# Initialize global native GLM client
def initialize_native_glm(api_key: str):
    """Initialize the native GLM client with provided API key"""
    
    if not api_key:
        raise ValueError("API key is required for GLM initialization")
    
    client = NativeGLMClient(api_key=api_key)
    
    # Log initialization
    print(f"Native GLM SDK Integration Initialized")
    print(f"   Models available: {list(client.glm_models.keys())}")
    print(f"   Web capabilities: Native search and chat tools")
    print(f"   Minimum model: GLM 4.5")
    
    return client

# Export for use
__all__ = ["NativeGLMClient", "initialize_native_glm"]