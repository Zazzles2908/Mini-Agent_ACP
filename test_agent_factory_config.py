#!/usr/bin/env python3
"""
Test script to verify agent factory supports both ACPAgent and ModularAgent based on config.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from mini_agent.agent_factory import AgentFactory
from mini_agent.config import get_config


async def test_agent_factory_agent_type_selection():
    """Test that AgentFactory correctly selects agent type based on configuration"""
    
    print("🧪 Testing AgentFactory agent type selection...")
    
    # Test 1: Default configuration (should be ACPAgent)
    print("\n1️⃣  Testing with default config (should create ACPAgent):")
    
    factory = AgentFactory()
    config = get_config()
    
    agent_config = config.get("agent", {})
    agent_type = agent_config.get("type", "acp")
    acp_config = agent_config.get("acp_config", {})
    
    print(f"   Agent type from config: {agent_type}")
    print(f"   ACP config: {acp_config}")
    
    # Verify the configuration
    assert agent_type == "acp", f"Expected 'acp', got '{agent_type}'"
    print("   ✅ Configuration correct - ACPAgent expected")
    
    # Test 2: Create agent and verify it's ACPAgent
    print("\n2️⃣  Testing agent creation with ACPAgent configuration:")
    
    try:
        agent = await factory.create_agent(auto_load_tools=False)
        agent_type_name = type(agent).__name__
        print(f"   Created agent type: {agent_type_name}")
        
        if agent_type_name == "ACPAgent":
            print("   ✅ ACPAgent created successfully")
            
            # Verify ACPAgent specific attributes
            if hasattr(agent, 'acp_config'):
                print(f"   ✅ ACPAgent has acp_config: {agent.acp_config}")
            else:
                print("   ⚠️  ACPAgent missing acp_config attribute")
                
        else:
            print(f"   ❌ Expected ACPAgent, got {agent_type_name}")
            
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Test with basic configuration (temporarily modify config)
    print("\n3️⃣  Testing configuration modification for basic agent:")
    
    # Save original config
    original_type = config._config.get("agent", {}).get("type", "acp")
    
    try:
        # Temporarily set to basic
        if "agent" not in config._config:
            config._config["agent"] = {}
        config._config["agent"]["type"] = "basic"
        
        agent_type = config.get("agent", {}).get("type", "acp")
        print(f"   Modified agent type: {agent_type}")
        
        # Create basic agent
        basic_agent = await factory.create_agent(auto_load_tools=False)
        basic_agent_type = type(basic_agent).__name__
        print(f"   Created basic agent type: {basic_agent_type}")
        
        if basic_agent_type == "ModularAgent":
            print("   ✅ ModularAgent created successfully")
        else:
            print(f"   ❌ Expected ModularAgent, got {basic_agent_type}")
            
    except Exception as e:
        print(f"   ❌ Basic agent creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore original config
        if "agent" not in config._config:
            config._config["agent"] = {}
        config._config["agent"]["type"] = original_type
    
    # Test 4: Test invalid configuration
    print("\n4️⃣  Testing invalid configuration:")
    
    try:
        config._config["agent"]["type"] = "invalid_type"
        
        try:
            invalid_agent = await factory.create_agent(auto_load_tools=False)
            print("   ❌ Should have failed with invalid agent type")
        except ValueError as e:
            print(f"   ✅ Correctly rejected invalid type: {e}")
        except Exception as e:
            print(f"   ⚠️  Unexpected error: {e}")
            
    except Exception as e:
        print(f"   ❌ Test setup failed: {e}")
    
    finally:
        # Restore original config
        if "agent" not in config._config:
            config._config["agent"] = {}
        config._config["agent"]["type"] = original_type
    
    print("\n🎉 AgentFactory configuration test completed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_factory_agent_type_selection())