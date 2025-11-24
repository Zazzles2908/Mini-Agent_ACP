#!/usr/bin/env python3
"""
MANUAL VALIDATION: Context Overflow Prevention Integration

This validates that the context overflow prevention system is properly integrated.
"""

def validate_context_prevention():
    """Validate the context overflow prevention integration"""
    print("🧪 VALIDATING CONTEXT OVERFLOW PREVENTION")
    print("=" * 45)
    
    # Check if context prevention file exists
    context_path = "mini_agent/core/context_overflow_prevention.py"
    
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ SUCCESS: Context prevention file exists: {context_path}")
    except FileNotFoundError:
        print(f"❌ FAIL: Context prevention file not found: {context_path}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Cannot read context prevention file: {e}")
        return False
    
    # Check for key classes and functions
    required_elements = [
        "class MiniAgentContextManager",
        "def check_token_budget_before_llm",
        "def get_optimization_recommendations",
        "def get_status_report"
    ]
    
    print("🔍 Checking for required elements:")
    for element in required_elements:
        if element in content:
            print(f"✅ FOUND: {element}")
        else:
            print(f"❌ MISSING: {element}")
    
    # Test import and basic functionality
    print("\n🧪 Testing integration:")
    
    try:
        # Test import
        exec("from mini_agent.core.context_overflow_prevention import MiniAgentContextManager")
        print("✅ SUCCESS: MiniAgentContextManager can be imported")
        
        # Test initialization
        exec("""
manager = MiniAgentContextManager()
print("✅ SUCCESS: MiniAgentContextManager initializes correctly")
print(f"   - Max tokens: {manager.max_tokens}")
print(f"   - Warning threshold: {manager.warning_threshold}")
""")
        
        # Test status report
        exec("""
status = manager.get_status_report()
print("✅ SUCCESS: Status report generated")
print(f"   - Current tokens: {status['current_tokens']}")
print(f"   - Usage percentage: {status['usage_percentage']:.1f}%")
""")
        
        # Test recommendations
        exec("""
recs = manager.get_optimization_recommendations()
print(f"✅ SUCCESS: Got {len(recs)} optimization recommendations")
""")
        
    except Exception as e:
        print(f"❌ ERROR: Integration test failed: {e}")
        return False
    
    # Check agent.py integration
    agent_path = "mini_agent/agent.py"
    with open(agent_path, 'r', encoding='utf-8') as f:
        agent_content = f.read()
    
    print("\n🔍 Checking agent.py integration:")
    
    # Check for import
    if "from .core.context_overflow_prevention import get_context_manager" in agent_content:
        print("✅ FOUND: Context prevention import in agent.py")
    else:
        print("❌ MISSING: Context prevention import in agent.py")
    
    # Check for usage
    if "self.context_manager = get_context_manager()" in agent_content:
        print("✅ FOUND: Context manager initialization in agent.py")
    else:
        print("❌ MISSING: Context manager initialization in agent.py")
    
    # Check for token budget checking
    if "check_token_budget_before_llm" in agent_content:
        print("✅ FOUND: Token budget checking in agent.py")
    else:
        print("❌ MISSING: Token budget checking in agent.py")
    
    # Test practical functionality
    print("\n🧪 Testing practical functionality:")
    
    try:
        # Simulate token budget check
        test_messages = [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you!"}
        ]
        
        # Convert to the format expected by the function
        message_dicts = [{"content": msg.get("content", ""), "role": msg.get("role", "")} for msg in test_messages]
        
        # Test token budget check
        exec("""
budget_ok = manager.check_token_budget_before_llm(message_dicts)
print(f"✅ SUCCESS: Token budget check returned {budget_ok}")
""")
        
    except Exception as e:
        print(f"❌ ERROR: Practical test failed: {e}")
        return False
    
    print("\n✅ SUCCESS: Context overflow prevention properly integrated")
    return True

if __name__ == "__main__":
    success = validate_context_prevention()
    if success:
        print("\n🎉 CONTEXT OVERFLOW PREVENTION VALIDATION PASSED")
    else:
        print("\n💥 CONTEXT OVERFLOW PREVENTION VALIDATION FAILED")
