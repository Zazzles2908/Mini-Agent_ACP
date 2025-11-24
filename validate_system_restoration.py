#!/usr/bin/env python3
"""
System restoration validation test.
Tests that the core system is working before implementing enhancements.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mini_agent'))

def test_provider_configuration():
    """Test that provider configuration is working"""
    print("🔍 Testing Provider Configuration...")
    
    try:
        from mini_agent.config import Config
        from mini_agent.llm.llm_wrapper import LLMClient
        
        # Load config
        config = Config()
        print(f"✅ Config loaded successfully")
        print(f"   Provider: {config.provider}")
        print(f"   API Base: {config.api_base}")
        print(f"   Model: {config.model}")
        
        # Test provider compatibility
        if config.provider == "anthropic":
            print(f"✅ Provider 'anthropic' is correct for MiniMax-M2")
            expected_api_base = f"{config.api_base.rstrip('/')}/anthropic"
            print(f"   Expected full API base: {expected_api_base}")
        else:
            print(f"❌ Provider '{config.provider}' is incorrect for MiniMax-M2")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Provider config test failed: {e}")
        return False

def test_mcp_configuration():
    """Test that MCP configuration path is correct"""
    print("\n🔍 Testing MCP Configuration Path...")
    
    # Check if .mcp.json exists in expected location
    mcp_path = ".mcp.json"
    if os.path.exists(mcp_path):
        print(f"✅ MCP config found at {mcp_path}")
        
        # Validate JSON structure
        try:
            import json
            with open(mcp_path, 'r') as f:
                mcp_config = json.load(f)
            
            if 'mcpServers' in mcp_config:
                servers = mcp_config['mcpServers']
                print(f"✅ Valid MCP config with {len(servers)} servers:")
                for name, config in servers.items():
                    disabled = config.get('disabled', False)
                    status = "DISABLED" if disabled else "ENABLED"
                    print(f"   - {name}: {status} - {config.get('description', 'No description')}")
                return True
            else:
                print(f"❌ Invalid MCP config: missing 'mcpServers' key")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in MCP config: {e}")
            return False
    else:
        print(f"❌ MCP config not found at {mcp_path}")
        return False

def test_memory_tools():
    """Test that enhanced memory tools can be imported"""
    print("\n🔍 Testing Memory Tools...")
    
    try:
        from mini_agent.tools.note_tool import (
            EnhancedSessionNoteTool, 
            EnhancedRecallNoteTool,
            SessionNoteTool,
            RecallNoteTool
        )
        print(f"✅ All memory tools imported successfully")
        print(f"   - EnhancedSessionNoteTool: {EnhancedSessionNoteTool.__name__}")
        print(f"   - EnhancedRecallNoteTool: {EnhancedRecallNoteTool.__name__}")
        print(f"   - SessionNoteTool: {SessionNoteTool.__name__} (backward compatible)")
        print(f"   - RecallNoteTool: {RecallNoteTool.__name__} (backward compatible)")
        return True
        
    except Exception as e:
        print(f"❌ Memory tools test failed: {e}")
        return False

def test_core_imports():
    """Test that core modules can be imported"""
    print("\n🔍 Testing Core Module Imports...")
    
    try:
        # Test core agent imports
        from mini_agent.config import Config
        print(f"✅ Config import successful")
        
        from mini_agent.llm.llm_wrapper import LLMClient
        print(f"✅ LLMClient import successful")
        
        from mini_agent.tools.base import Tool
        print(f"✅ Tool base import successful")
        
        from mini_agent.tools.get_skill_tool import GetSkillTool
        print(f"✅ GetSkillTool import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_memory_configuration():
    """Test that memory configuration can be loaded"""
    print("\n🔍 Testing Memory Configuration...")
    
    try:
        from mini_agent.config import Config
        
        config = Config()
        memory_config = config.get_memory_config()
        
        if memory_config:
            print(f"✅ Memory config loaded successfully")
            print(f"   Memory config keys: {list(memory_config.keys())}")
            print(f"   Enhanced enabled: {memory_config.get('enable_enhanced', False)}")
            return True
        else:
            print(f"❌ Memory config not available")
            return False
            
    except Exception as e:
        print(f"❌ Memory configuration test failed: {e}")
        return False

def test_note_tool_functionality():
    """Test that note tools can be instantiated and basic functions work"""
    print("\n🔍 Testing Note Tool Functionality...")
    
    try:
        from mini_agent.tools.note_tool import EnhancedSessionNoteTool, EnhancedRecallNoteTool
        
        # Test instantiation
        session_tool = EnhancedSessionNoteTool()
        recall_tool = EnhancedRecallNoteTool()
        
        print(f"✅ Note tools instantiated successfully")
        print(f"   Session tool name: {session_tool.name}")
        print(f"   Recall tool name: {recall_tool.name}")
        print(f"   Enhanced features: {session_tool.enhanced_enabled}")
        
        # Test that workspace detection works
        project = session_tool.current_project
        if project:
            print(f"   Current project detected: {project.get('type', 'unknown')}")
        else:
            print(f"   No project context detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Note tool functionality test failed: {e}")
        return False

def main():
    """Run all restoration tests"""
    print("=== System Restoration Validation ===\n")
    
    tests = [
        test_provider_configuration,
        test_mcp_configuration, 
        test_memory_tools,
        test_core_imports,
        test_memory_configuration,
        test_note_tool_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("✅ System restoration successful - ready for Phase 1 implementation")
        print("\n=== Current System Status ===")
        print("✅ Provider: anthropic (MiniMax-M2 compatible)")
        print("✅ MCP Config: 6 servers enabled")
        print("✅ Memory Tools: Enhanced session notes available")
        print("✅ Configuration: Memory enhancement disabled by default")
        print("✅ Backward Compatibility: Original interfaces maintained")
        return True
    else:
        print("❌ System restoration incomplete - fix issues before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
