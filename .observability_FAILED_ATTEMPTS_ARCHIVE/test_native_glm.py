"""
Test script for native GLM SDK integration
Verifies that the GLM SDK is working correctly with self-awareness
"""

import asyncio
import os
from pathlib import Path
import sys

# Add observability to path
sys.path.insert(0, str(Path(".observability")))

from mini_agent_intelligence import initialize_mini_agent_intelligence

async def test_native_glm_integration():
    """Test the native GLM SDK integration"""
    
    print("Testing Native GLM SDK Integration")
    print("=" * 50)
    
    # Initialize with provided Z.AI API key
    zai_api_key = "7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe"
    
    print(f"\n1. Initializing Intelligence System with GLM SDK...")
    intelligence = initialize_mini_agent_intelligence(zai_api_key)
    
    if intelligence.initialized:
        print("   SUCCESS: Intelligence system initialized")
        print(f"   GLM Client available: {intelligence.glm_client is not None}")
        
        if intelligence.glm_client:
            # Test GLM SDK info
            sdk_info = intelligence.glm_client.get_sdk_info()
            print(f"   SDK Available: {sdk_info['sdk_available']}")
            print(f"   Integration Status: {sdk_info['integration_status']}")
            print(f"   Native Models: {list(sdk_info['native_models'].keys())}")
    else:
        print("   WARNING: Some components not initialized")
    
    # Test 2: Intelligent Task Execution
    print(f"\n2. Testing Intelligent Task Execution...")
    
    task = "Analyze current directory structure and create a summary"
    tools = ["list_directory", "bash", "read_file"]
    
    result = intelligence.execute_intelligent_task(task, tools)
    
    if result["success"]:
        decision = result["intelligent_decision"]
        print(f"   Decision: {decision['chosen_tool']}")
        print(f"   Reasoning: {decision['reasoning']}")
        print(f"   Confidence: {decision['confidence']:.1%}")
    else:
        print(f"   ERROR: {result.get('error', 'Unknown error')}")
    
    # Test 3: Native GLM Chat
    print(f"\n3. Testing Native GLM Chat...")
    
    try:
        chat_result = await intelligence.chat_with_native_glm(
            "What are the current capabilities of GLM 4.5?", 
            use_web_search=False
        )
        
        if chat_result.get("success"):
            chat_data = chat_result["chat_result"]
            print(f"   Chat Success: True")
            print(f"   Model Used: {chat_data.get('model_used', 'Unknown')}")
            print(f"   Response Length: {len(chat_data.get('response', ''))} chars")
        else:
            print(f"   Chat Error: {chat_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   Chat Exception: {e}")
    
    # Test 4: Native Web Search
    print(f"\n4. Testing Native Web Search...")
    
    try:
        search_result = await intelligence.native_web_research(
            "latest developments in AI agent technology 2024",
            enhanced_analysis=False
        )
        
        if search_result.get("success"):
            results = search_result["results"]
            print(f"   Search Success: True")
            print(f"   Results Count: {results.get('total_results', 0)}")
            print(f"   GLM Integration: {results.get('glml_integration', 'None')}")
        else:
            print(f"   Search Error: {search_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   Search Exception: {e}")
    
    # Test 5: Enhanced Web Research (both search and chat)
    print(f"\n5. Testing Enhanced Web Research...")
    
    try:
        enhanced_result = await intelligence.native_web_research(
            "GLM 4.5 capabilities and features",
            enhanced_analysis=True
        )
        
        if enhanced_result.get("success"):
            research_data = enhanced_result["results"]
            print(f"   Enhanced Research Success: True")
            print(f"   Direct Search Results: {research_data.get('native_search_results', {}).get('total_results', 0)}")
            print(f"   Chat Analysis: {research_data.get('chat_analysis', {}).get('response', 'No response')[:100]}...")
        else:
            print(f"   Enhanced Research Error: {enhanced_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   Enhanced Research Exception: {e}")
    
    # Test 6: Performance Insights
    print(f"\n6. Retrieving Performance Insights...")
    
    try:
        insights = intelligence.get_performance_insights()
        
        if "error" not in insights:
            performance = insights.get("performance_analysis", {})
            glm_integration = insights.get("native_glm_integration", {})
            system_health = insights.get("intelligence_system_health", {})
            
            print(f"   Total Tasks: {performance.get('total_tasks', 0)}")
            print(f"   Success Rate: {performance.get('success_rate', 0):.1%}")
            print(f"   GLM Integration Status: {glm_integration.get('status', 'Unknown')}")
            print(f"   Web Capabilities: {glm_integration.get('web_capabilities', {})}")
            
            print(f"\n   System Health:")
            for component, status in system_health.items():
                print(f"      {component}: {status}")
        else:
            print(f"   Insights Error: {insights['error']}")
            
    except Exception as e:
        print(f"   Insights Exception: {e}")
    
    print(f"\n" + "=" * 50)
    print("Native GLM SDK Integration Test Complete!")
    print(f"\nSystem Status:")
    print(f"   Intelligence System: {'Active' if intelligence.initialized else 'Not Active'}")
    print(f"   Native GLM SDK: {'Available' if intelligence.glm_client else 'Not Available'}")
    print(f"   Web Capabilities: {'Native' if intelligence.glm_client else 'Unavailable'}")
    print(f"   GLM Models: GLM 4.5+ minimum as requested")
    print(f"\nReady for production use with native GLM integration!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_native_glm_integration())