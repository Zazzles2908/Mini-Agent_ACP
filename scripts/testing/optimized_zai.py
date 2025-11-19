#!/usr/bin/env python3
"""
Optimized Z.AI Integration
Properly utilizes Z.AI's full capabilities with GLM models
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ZAIModel:
    """Z.AI model configuration"""
    name: str
    description: str
    best_for: str
    max_tokens: int

class ZAIKeyManager:
    """Secure Z.AI key management"""
    
    def __init__(self):
        self.api_key = None
        self.env_loaded = self._load_from_env()
        if not self.api_key:
            self.api_key = self._prompt_for_key()
    
    def _load_from_env(self) -> bool:
        """Load API key from environment"""
        self.api_key = os.getenv('ZAI_API_KEY')
        if self.api_key:
            print(f"✅ Loaded Z.AI API key from environment")
            return True
        return False
    
    def _prompt_for_key(self) -> str:
        """Prompt user for API key if not in environment"""
        print("🔑 Z.AI API key not found in environment")
        print("📋 Get your key from: https://z.ai/subscribe")
        key = input("Enter your Z.AI API key: ").strip()
        if key:
            # Save to environment file
            with open('.env', 'w') as f:
                f.write(f'ZAI_API_KEY={key}')
            print("💾 API key saved to .env file")
            return key
        else:
            raise ValueError("No API key provided")

class OptimizedZAIClient:
    """Fully optimized Z.AI client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/paas/v4"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Available GLM models
        self.models = {
            'glm-4.6': ZAIModel('glm-4.6', 'Flagship model for reasoning and coding', 'Complex reasoning, coding, agentic tasks', 8192),
            'glm-4.5': ZAIModel('glm-4.5', 'Latest model with strong agent capabilities', 'Agent-centric applications', 8192),
            'glm-4-air': ZAIModel('glm-4-air', 'Lightweight fast model', 'Quick responses, chat', 4096),
            'glm-4.6-plus': ZAIModel('glm-4.6-plus', 'Enhanced version with better performance', 'High-performance reasoning', 8192)
        }
    
    def select_model(self, task: str) -> ZAIModel:
        """Smart model selection based on task"""
        task_lower = task.lower()
        
        if 'reasoning' in task_lower or 'analysis' in task_lower or 'complex' in task_lower:
            return self.models['glm-4.6']
        elif 'coding' in task_lower or 'programming' in task_lower or 'development' in task_lower:
            return self.models['glm-4.6']
        elif 'agent' in task_lower or 'autonomous' in task_lower:
            return self.models['glm-4.5']
        elif 'quick' in task_lower or 'fast' in task_lower or 'simple' in task_lower:
            return self.models['glm-4-air']
        else:
            return self.models['glm-4.6']  # Default to best model
    
    async def advanced_web_search(self, 
                                 query: str, 
                                 count: int = 10,
                                 search_engine: str = "search-prime",
                                 recency: str = "oneDay",
                                 domain_filter: Optional[str] = None,
                                 intent_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Advanced web search with full Z.AI capabilities"""
        
        payload = {
            "search_engine": search_engine,
            "search_query": query,
            "count": count,
            "search_recency_filter": recency
        }
        
        if domain_filter:
            payload["search_domain_filter"] = domain_filter
        
        if intent_prompt:
            payload["search_prompt"] = intent_prompt
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/web_search",
                headers=self.headers,
                json=payload,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "query": query,
                        "search_engine": search_engine,
                        "results": result.get("search_result", []),
                        "count": len(result.get("search_result", [])),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    return {"success": False, "error": f"API error {response.status}: {error_text}"}
    
    async def web_search_in_chat(self, 
                                query: str, 
                                model_name: str = "glm-4.6",
                                search_params: Dict = None) -> Dict[str, Any]:
        """Web search integrated with GLM chat for enhanced results"""
        
        if not search_params:
            search_params = {
                "enable": "True",
                "search_engine": "search-prime",
                "search_result": "True",
                "search_prompt": f"Provide comprehensive analysis for: {query}",
                "count": "5"
            }
        
        messages = [
            {"role": "system", "content": "You are an AI assistant with web search capabilities. Provide detailed, accurate information using the latest web data."},
            {"role": "user", "content": query}
        ]
        
        chat_payload = {
            "model": model_name,
            "messages": messages,
            "tools": [{
                "type": "web_search",
                "web_search": search_params
            }],
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=chat_payload,
                timeout=60
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "model": model_name,
                        "query": query,
                        "response": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                        "tool_calls": result.get("choices", [{}])[0].get("message", {}).get("tool_calls", []),
                        "usage": result.get("usage", {}),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    return {"success": False, "error": f"API error {response.status}: {error_text}"}
    
    async def intelligent_web_reading(self, 
                                     url: str,
                                     format_type: str = "markdown",
                                     include_images: bool = True,
                                     extract_summary: bool = True) -> Dict[str, Any]:
        """Advanced web reading with Z.AI optimization"""
        
        payload = {
            "url": url,
            "timeout": 20,
            "no_cache": False,
            "return_format": format_type,
            "retain_images": include_images,
            "no_gfm": False,
            "keep_img_data_url": False
        }
        
        if extract_summary:
            payload["with_images_summary"] = True
            payload["with_links_summary"] = True
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/reader",
                headers=self.headers,
                json=payload,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    reader_result = result.get("reader_result", {})
                    
                    return {
                        "success": True,
                        "url": url,
                        "format": format_type,
                        "content": reader_result.get("content", ""),
                        "title": reader_result.get("title", ""),
                        "description": reader_result.get("description", ""),
                        "metadata": reader_result.get("metadata", {}),
                        "external_stylesheets": reader_result.get("external", {}).get("stylesheet", []),
                        "word_count": len(reader_result.get("content", "").split()),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    return {"success": False, "error": f"API error {response.status}: {error_text}"}
    
    async def research_and_analyze(self, 
                                  query: str, 
                                  depth: str = "comprehensive",
                                  model_preference: str = "auto") -> Dict[str, Any]:
        """Complete research workflow using web search + GLM analysis"""
        
        # Determine model based on depth and task
        if model_preference == "auto":
            model = self.select_model(query)
            model_name = model.name
        else:
            model_name = model_preference
            model = self.models.get(model_name, self.models['glm-4.6'])
        
        # Configure search parameters based on depth
        if depth == "quick":
            search_params = {
                "enable": "True",
                "search_result": "True",
                "count": "3"
            }
        elif depth == "deep":
            search_params = {
                "enable": "True", 
                "search_result": "True",
                "count": "10",
                "search_recency_filter": "oneWeek"
            }
        else:  # comprehensive
            search_params = {
                "enable": "True",
                "search_result": "True", 
                "count": "7",
                "search_recency_filter": "oneDay",
                "search_prompt": f"Analyze and synthesize information about: {query}. Provide insights, trends, and key findings."
            }
        
        # Perform web search + chat analysis
        result = await self.web_search_in_chat(query, model_name, search_params)
        
        if result["success"]:
            return {
                "success": True,
                "query": query,
                "depth": depth,
                "model_used": model_name,
                "model_description": model.description,
                "analysis": result["response"],
                "search_evidence": result.get("tool_calls", []),
                "token_usage": result.get("usage", {}),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return result
    
    async def batch_research(self, 
                           queries: List[str], 
                           model_preference: str = "glm-4.6") -> Dict[str, Any]:
        """Research multiple queries efficiently"""
        
        tasks = []
        for query in queries:
            task = asyncio.create_task(self.research_and_analyze(query, "comprehensive", model_preference))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = []
        failed_queries = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_queries.append({"query": queries[i], "error": str(result)})
            elif result.get("success"):
                successful_results.append({
                    "query": queries[i],
                    "analysis": result["analysis"],
                    "model_used": result["model_used"]
                })
            else:
                failed_queries.append({"query": queries[i], "error": result.get("error")})
        
        return {
            "success": True,
            "total_queries": len(queries),
            "successful": len(successful_results),
            "failed": len(failed_queries),
            "results": successful_results,
            "failures": failed_queries,
            "timestamp": datetime.now().isoformat()
        }

class ZAIMonitoringSystem:
    """Advanced monitoring with Z.AI capabilities"""
    
    def __init__(self, zai_client: OptimizedZAIClient):
        self.zai = zai_client
        self.watches = []
        self.history = {}
    
    def add_intelligent_watch(self, 
                            name: str, 
                            query: str, 
                            interval_minutes: int = 60,
                            analysis_depth: str = "quick",
                            model_preference: str = "auto") -> None:
        """Add a watch with intelligent analysis"""
        
        self.watches.append({
            "name": name,
            "query": query,
            "interval_minutes": interval_minutes,
            "analysis_depth": analysis_depth,
            "model_preference": model_preference,
            "last_analysis": None,
            "active": True
        })
        
        print(f"🧠 Added intelligent watch: {name}")
        print(f"   Query: {query}")
        print(f"   Depth: {analysis_depth}")
        print(f"   Interval: {interval_minutes} minutes")
    
    async def analyze_watch(self, watch: Dict) -> Dict[str, Any]:
        """Perform intelligent analysis for a watch"""
        
        try:
            # Choose model based on preference
            if watch["model_preference"] == "auto":
                model = self.zai.select_model(watch["query"])
                model_name = model.name
            else:
                model_name = watch["model_preference"]
            
            # Perform research analysis
            analysis = await self.zai.research_and_analyze(
                watch["query"], 
                watch["analysis_depth"],
                model_name
            )
            
            # Check for new insights
            analysis_key = watch["name"]
            is_new = True
            
            if analysis_key in self.history:
                last_content = self.history[analysis_key].get("analysis", "")
                current_content = analysis.get("analysis", "")
                
                # Simple similarity check
                if len(set(last_content.split()) & set(current_content.split())) > 50:
                    is_new = False
            
            result = {
                "watch_name": watch["name"],
                "timestamp": datetime.now().isoformat(),
                "is_new": is_new,
                "model_used": analysis.get("model_used"),
                "analysis": analysis.get("analysis", ""),
                "search_evidence": analysis.get("search_evidence", []),
                "token_usage": analysis.get("token_usage", {}),
                "success": analysis.get("success", False)
            }
            
            self.history[analysis_key] = result
            return result
            
        except Exception as e:
            return {
                "watch_name": watch["name"],
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    async def start_intelligent_monitoring(self) -> None:
        """Start monitoring with intelligent analysis"""
        print(f"🧠 Starting intelligent monitoring for {len(self.watches)} topics...")
        
        while True:
            for watch in self.watches:
                if watch["active"]:
                    print(f"🔍 Analyzing: {watch['name']}")
                    result = await self.analyze_watch(watch)
                    
                    if result.get("success"):
                        if result.get("is_new"):
                            print(f"🆕 NEW INSIGHTS: {watch['name']}")
                            print(f"   Model: {result['model_used']}")
                            print(f"   Summary: {result['analysis'][:200]}...")
                        else:
                            print(f"🔄 No new insights: {watch['name']}")
                    else:
                        print(f"❌ Analysis failed: {watch['name']} - {result.get('error')}")
            
            print("⏱️ Waiting for next cycle...")
            await asyncio.sleep(60)  # Check every minute

def main():
    """Demo the optimized Z.AI integration"""
    print("🧠 Optimized Z.AI Integration Demo")
    print("=" * 40)
    
    # Initialize with proper key management
    key_manager = ZAIKeyManager()
    zai = OptimizedZAIClient(key_manager.api_key)
    
    async def demo():
        print("\n🔍 Testing Advanced Web Search...")
        
        # Test advanced search
        result = await zai.advanced_web_search(
            query="artificial intelligence breakthrough 2025",
            count=5,
            recency="oneDay",
            domain_filter="arxiv.org"
        )
        
        if result["success"]:
            print(f"✅ Found {result['count']} results")
            for item in result["results"]:
                print(f"  📄 {item['title']}")
        
        print("\n🧠 Testing Web Search + Chat Analysis...")
        
        # Test web search in chat
        chat_result = await zai.web_search_in_chat(
            "What are the latest developments in AI research?",
            "glm-4.6"
        )
        
        if chat_result["success"]:
            print(f"✅ Model: {chat_result['model']}")
            print(f"📝 Analysis: {chat_result['response'][:300]}...")
        
        print("\n📖 Testing Intelligent Web Reading...")
        
        # Test web reading
        read_result = await zai.intelligent_web_reading(
            "https://arxiv.org",
            format_type="markdown",
            include_images=True
        )
        
        if read_result["success"]:
            print(f"✅ Title: {read_result['title']}")
            print(f"📊 Words: {read_result['word_count']}")
        
        print("\n🧠 Testing Research & Analysis...")
        
        # Test comprehensive research
        research = await zai.research_and_analyze(
            "machine learning trends 2025",
            depth="comprehensive"
        )
        
        if research["success"]:
            print(f"✅ Model: {research['model_used']}")
            print(f"📝 Analysis: {research['analysis'][:200]}...")
        
        print("\n🎯 Testing Intelligent Monitoring...")
        
        # Test monitoring system
        monitor = ZAIMonitoringSystem(zai)
        monitor.add_intelligent_watch(
            "AI News",
            "artificial intelligence breakthrough",
            interval_minutes=30,
            analysis_depth="quick",
            model_preference="glm-4.6"
        )
        
        # Run one analysis cycle
        print("🔍 Running one analysis cycle...")
        for watch in monitor.watches:
            result = await monitor.analyze_watch(watch)
            if result.get("success"):
                print(f"✅ {watch['name']}: Analyzed with {result['model_used']}")
        
        print("\n🎉 Demo completed! Integration fully optimized.")
    
    # Run the demo
    asyncio.run(demo())

if __name__ == "__main__":
    main()
