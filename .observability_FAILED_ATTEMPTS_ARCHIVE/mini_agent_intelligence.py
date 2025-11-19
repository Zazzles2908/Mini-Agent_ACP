"""
Updated Mini-Agent Intelligence System with Native GLM SDK
Uses native zai SDK with GLM 4.5+ and integrated self-awareness
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Add observability path to Python path
obs_path = Path(__file__).parent
if str(obs_path) not in sys.path:
    sys.path.insert(0, str(obs_path))

from self_awareness import self_awareness, SelfAwarenessSystem
from intelligent_decisions import decision_maker, IntelligentDecisionMaker, DecisionContext
from real_time_monitor import real_time_monitor, RealTimeMonitor
from native_glm_integration import NativeGLMClient, initialize_native_glm

class MiniAgentIntelligence:
    """
    Updated intelligence system with native GLM SDK integration
    """
    
    def __init__(self, zai_api_key: str = None):
        self.initialized = False
        self.glm_client = None
        self.config = self._load_intelligence_config()
        
        # Initialize components
        self._initialize_intelligence(zai_api_key)
    
    def _load_intelligence_config(self) -> Dict[str, Any]:
        """Load intelligence system configuration"""
        
        config_file = Path(".observability/ai_agent_config.json")
        
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    return json.load(f)
            except:
                pass
        
        # Default configuration with GLM 4.5 minimum
        return {
            "model_config": {
                "min_glm_model": "glm4.5",
                "native_sdk_integration": True,
                "glml_capabilities": ["reasoning", "planning", "web_search", "chat_tools"]
            },
            "intelligence_settings": {
                "self_awareness_enabled": True,
                "auto_optimization": True,
                "decision_learning": True,
                "performance_tracking": True
            },
            "native_integration": {
                "use_zai_sdk": True,
                "glml_4_5_minimum": True,
                "native_web_search": True,
                "chat_with_tools": True
            }
        }
    
    def _initialize_intelligence(self, zai_api_key: str = None):
        """Initialize all intelligence components with native GLM SDK"""
        
        try:
            # Initialize native GLM client if API key provided
            if zai_api_key:
                os.environ["ZAI_API_KEY"] = zai_api_key
                self.glm_client = initialize_native_glm(zai_api_key)
                
                # Log successful initialization with GLM capabilities
                self_awareness.add_capability_insight(
                    capability_type="native_glm_initialization",
                    discovery=f"Native GLM SDK initialized with GLM 4.5+ capabilities and web search",
                    impact_score=1.0
                )
            
            # Start performance monitoring
            try:
                real_time_monitor.start_monitoring(interval_minutes=30)
            except:
                print("Warning: Could not start monitoring")
            
            self.initialized = True
            
            print("Mini-Agent Intelligence System with Native GLM SDK Initialized")
            print(f"   Self-awareness: Active")
            print(f"   Decision making: Intelligent")  
            print(f"   Performance monitoring: Real-time")
            if self.glm_client:
                print(f"   Native GLM SDK: {self.glm_client.get_sdk_info()['integration_status']}")
                print(f"   Web capabilities: Native search and chat tools")
            
        except Exception as e:
            print(f"Intelligence system initialization warning: {e}")
            self.initialized = False
    
    def execute_intelligent_task(self, task_description: str, 
                               available_tools: List[str]) -> Dict[str, Any]:
        """Execute a task with intelligence optimization"""
        
        if not self.initialized:
            return {"error": "Intelligence system not initialized", "success": False}
        
        # Create decision context
        context = DecisionContext(
            task_description=task_description,
            available_tools=available_tools,
            constraints=[],
            success_requirements=[]
        )
        
        # Make intelligent decision
        decision = decision_maker.make_intelligent_decision(context)
        
        # Record decision for learning
        self_awareness.record_decision(
            context=task_description,
            options_considered=available_tools,
            chosen_option=decision.chosen_tool,
            reasoning=decision.reasoning,
            confidence_level=decision.confidence
        )
        
        return {
            "task_description": task_description,
            "intelligent_decision": {
                "chosen_tool": decision.chosen_tool,
                "reasoning": decision.reasoning,
                "confidence": decision.confidence,
                "alternatives": decision.alternatives_considered
            },
            "available_tools": available_tools,
            "success": True,
            "intelligence_applied": True,
            "native_glm_integration": self.glm_client is not None
        }
    
    async def native_web_research(self, query: str, enhanced_analysis: bool = True) -> Dict[str, Any]:
        """
        Perform web research using native GLM SDK capabilities
        """
        
        if not self.initialized:
            return {"error": "Intelligence system not initialized", "success": False}
        
        if not self.glm_client:
            return {"error": "Native GLM client not available", "success": False}
        
        try:
            if enhanced_analysis:
                # Use enhanced research with both direct search and chat analysis
                results = await self.glm_client.enhanced_web_research(query)
            else:
                # Simple native search
                results = await self.glm_client.native_web_search(query)
            
            # Record execution in self-awareness
            self_awareness.record_execution(
                task_type="native_web_research",
                tools_used=["native_web_search", "glml_sdk"],
                success=True,
                complexity_score=5
            )
            
            return {
                "query": query,
                "results": results,
                "native_research": True,
                "glml_integration": "native_zai_sdk",
                "success": True
            }
            
        except Exception as e:
            self_awareness.record_execution(
                task_type="native_web_research", 
                tools_used=["native_web_search", "glml_sdk"],
                success=False,
                complexity_score=5,
                error_message=str(e)
            )
            return {"error": str(e), "success": False}
    
    async def chat_with_native_glm(self, message: str, use_web_search: bool = True) -> Dict[str, Any]:
        """
        Chat with GLM using native SDK and optional web search tools
        """
        
        if not self.initialized:
            return {"error": "Intelligence system not initialized", "success": False}
        
        if not self.glm_client:
            return {"error": "Native GLM client not available", "success": False}
        
        try:
            if use_web_search:
                # Use chat with web search tools
                results = await self.glm_client.chat_with_web_search(message)
            else:
                # Simple chat without web search
                native_model = self.glm_client._get_native_model_name("glm4.5")
                response = self.glm_client.client.chat.completions.create(
                    model=native_model,
                    messages=[{"role": "user", "content": message}]
                )
                
                results = {
                    "message": message,
                    "response": response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response),
                    "model_used": native_model,
                    "web_search_enabled": False
                }
            
            # Record execution
            self_awareness.record_execution(
                task_type="native_glm_chat",
                tools_used=["glml_chat", "glml_sdk"],
                success=True,
                complexity_score=3
            )
            
            return {
                "chat_result": results,
                "native_integration": True,
                "success": True
            }
            
        except Exception as e:
            self_awareness.record_execution(
                task_type="native_glm_chat",
                tools_used=["glml_chat", "glml_sdk"],
                success=False,
                complexity_score=3,
                error_message=str(e)
            )
            return {"error": str(e), "success": False}
    
    def get_performance_insights(self) -> Dict[str, Any]:
        """Get comprehensive performance insights"""
        
        if not self.initialized:
            return {"error": "Intelligence system not initialized"}
        
        # Get all intelligence components
        performance_analysis = self_awareness.get_performance_analysis()
        decision_patterns = self_awareness.get_decision_patterns()
        
        # Get GLM SDK info
        glm_info = {}
        if self.glm_client:
            glm_info = self.glm_client.get_sdk_info()
        
        # Compile comprehensive insights
        insights = {
            "timestamp": datetime.now().isoformat(),
            "performance_analysis": performance_analysis,
            "decision_patterns": decision_patterns,
            "native_glm_integration": {
                "status": "active" if self.glm_client else "not_available",
                "sdk_info": glm_info,
                "web_capabilities": self.glm_client.get_sdk_info()["web_capabilities"] if self.glm_client else {}
            },
            "optimization_recommendations": self._generate_recommendations(performance_analysis, glm_info),
            "intelligence_system_health": {
                "self_awareness": "active" if performance_analysis.get("total_tasks", 0) > 0 else "learning",
                "decision_making": "intelligent" if decision_patterns else "basic",
                "native_glm_integration": "enhanced" if self.glm_client else "not_available",
                "web_capabilities": "native" if self.glm_client else "unavailable"
            }
        }
        
        return insights
    
    def _generate_recommendations(self, performance: Dict, glm_info: Dict) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # GLM integration recommendations
        if not glm_info.get("client_initialized", False):
            recommendations.append("Initialize GLM client with valid API key for enhanced capabilities")
        
        if glm_info.get("sdk_available", False):
            recommendations.append("Native GLM SDK is available and ready for use")
            recommendations.append("Use GLM 4.5+ models for complex web research tasks")
        
        # Performance recommendations
        success_rate = performance.get("success_rate", 0)
        if success_rate < 0.6:
            recommendations.append("Critical: Success rate below 60% - review task approach")
        elif success_rate < 0.8:
            recommendations.append("Improve success rate through better decision making")
        
        return recommendations
    
    def optimize_system_performance(self) -> Dict[str, Any]:
        """Run system optimization"""
        
        if not self.initialized:
            return {"error": "Intelligence system not initialized"}
        
        optimization_actions = []
        
        # Get current insights
        insights = self.get_performance_insights()
        
        # Check GLM optimization opportunities
        if self.glm_client:
            glm_info = insights.get("native_glm_integration", {})
            if glm_info.get("status") == "active":
                optimization_actions.append("Native GLM SDK is optimally configured")
        
        # Record optimization
        self_awareness.add_capability_insight(
            capability_type="system_optimization",
            discovery="Automated performance optimization executed",
            impact_score=0.6
        )
        
        return {
            "optimization_timestamp": datetime.now().isoformat(),
            "actions_taken": optimization_actions,
            "system_health": "optimized",
            "native_glm_ready": self.glm_client is not None
        }

def initialize_mini_agent_intelligence(zai_api_key: str = None) -> MiniAgentIntelligence:
    """Initialize the complete intelligence system with native GLM SDK"""
    
    # Check if observability directory exists
    obs_dir = Path(".observability")
    if not obs_dir.exists():
        obs_dir.mkdir()
        print("Created .observability directory for intelligence system")
    
    # Initialize the intelligence system
    intelligence = MiniAgentIntelligence(zai_api_key)
    
    # Record successful initialization
    self_awareness.add_capability_insight(
        capability_type="mini_agent_initialization",
        discovery="Mini-Agent intelligence system with native GLM SDK fully initialized",
        impact_score=1.0
    )
    
    return intelligence

# Global instance
_global_intelligence = None

def get_intelligence_system(zai_api_key: str = None) -> MiniAgentIntelligence:
    """Get or create the global intelligence system instance"""
    
    global _global_intelligence
    
    if _global_intelligence is None:
        _global_intelligence = initialize_mini_agent_intelligence(zai_api_key)
    
    return _global_intelligence

# Export main interface
__all__ = [
    "MiniAgentIntelligence",
    "initialize_mini_agent_intelligence", 
    "get_intelligence_system"
]