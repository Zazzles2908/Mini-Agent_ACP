"""
Mini-Agent Intelligence System Demo
Demonstrates the self-awareness and optimization capabilities
"""

import asyncio
import os
from pathlib import Path

# Add observability to path
import sys
sys.path.insert(0, str(Path(".observability")))

from mini_agent_intelligence import initialize_mini_agent_intelligence

async def demo_intelligence_system():
    """Demonstrate the intelligence system capabilities"""
    
    print("Mini-Agent Intelligence System Demo")
    print("=" * 50)
    
    # Initialize with provided Z.AI API key
    zai_api_key = "7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe"
    
    print(f"\n1. Initializing Intelligence System...")
    intelligence = initialize_mini_agent_intelligence(zai_api_key)
    
    if intelligence.initialized:
        print("   Success: Intelligence system initialized successfully")
    else:
        print("   Warning: Some components may not be fully initialized")
    
    # Demo 1: Intelligent Task Execution
    print(f"\n2. Testing Intelligent Task Execution...")
    
    sample_task = "Analyze the current project structure and identify optimization opportunities"
    available_tools = ["list_directory", "read_file", "bash", "search", "browse"]
    
    execution_result = intelligence.execute_intelligent_task(sample_task, available_tools)
    
    if execution_result["success"]:
        decision = execution_result["intelligent_decision"]
        print(f"   Decision: {decision['chosen_tool']}")
        print(f"   Reasoning: {decision['reasoning']}")
        print(f"   Confidence: {decision['confidence']:.1%}")
        if decision['alternatives']:
            print(f"   Alternatives: {', '.join(decision['alternatives'])}")
    
    # Demo 2: Intelligent Web Research
    print(f"\n3. Testing Intelligent Web Research...")
    
    try:
        research_query = "latest developments in AI agent technology 2024"
        
        research_result = await intelligence.intelligent_web_research(
            research_query, 
            enhanced_reading=True
        )
        
        if research_result.get("success"):
            results = research_result.get("results", {})
            search_results = results.get("search_results", [])
            read_contents = results.get("read_contents", [])
            
            print(f"   Search completed with {len(search_results)} results")
            print(f"   Enhanced reading of {len(read_contents)} sources")
            
            if read_contents:
                print(f"   Model intelligence applied to {len(read_contents)} articles")
            
        else:
            print(f"   Warning: Research failed: {research_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   Warning: Research demonstration error: {e}")
    
    # Demo 3: Performance Insights
    print(f"\n4. Retrieving Performance Insights...")
    
    insights = intelligence.get_performance_insights()
    
    if "error" not in insights:
        performance = insights.get("performance_analysis", {})
        system_health = insights.get("intelligence_system_health", {})
        
        print(f"   Total Tasks Executed: {performance.get('total_tasks', 0)}")
        print(f"   Success Rate: {performance.get('success_rate', 0):.1%}")
        print(f"   Tool Usage Diversity: {len(performance.get('tool_usage', {}))} tools")
        
        print(f"\n   System Health:")
        for component, status in system_health.items():
            print(f"      {component}: {status}")
        
        # Show recommendations
        recommendations = insights.get("optimization_recommendations", [])
        if recommendations:
            print(f"\n   Optimization Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"      {i}. {rec}")
    else:
        print(f"   Warning: Could not retrieve insights: {insights['error']}")
    
    # Demo 4: System Optimization
    print(f"\n5. Running System Optimization...")
    
    optimization_result = intelligence.optimize_system_performance()
    
    if "error" not in optimization_result:
        actions = optimization_result.get("actions_taken", [])
        print(f"   Optimization Actions: {len(actions)}")
        for action in actions:
            print(f"      • {action}")
        print(f"   System optimized at {optimization_result['optimization_timestamp']}")
    else:
        print(f"   Warning: Optimization failed: {optimization_result['error']}")
    
    print(f"\n" + "=" * 50)
    print("Demo Complete!")
    print(f"\nThe Mini-Agent Intelligence System is now:")
    print(f"   Self-aware of its performance patterns")
    print(f"   Making intelligent decisions based on context")
    print(f"   Continuously monitoring and optimizing")
    print(f"   Using enhanced Z.AI capabilities (glm4.5+ models)")
    print(f"\nReady for production use!")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_intelligence_system())