#!/usr/bin/env python3
"""
QA System Test - Simple Import and Functionality Check

Tests the QA validation system to ensure imports work and basic functionality is operational.
"""

import sys
import json
from pathlib import Path

# Simple path setup
sys.path.insert(0, str(Path(__file__).parent / "mini_agent"))

def test_qa_imports():
    """Test basic imports"""
    print("Testing QA Validation System Imports")
    print("=" * 40)
    
    try:
        # Test base imports
        from tools.base import Tool, ToolResult
        print("✓ Base tools import successful")
        
        # Test validation tool loading
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "validation_tool",
            Path(__file__).parent / "mini_agent" / "skills" / "fact-checking-self-assessment" / "tools" / "validation_tool.py"
        )
        validation_module = importlib.util.module_from_spec(spec)
        
        # Add base classes to module
        validation_module.Tool = Tool
        validation_module.ToolResult = ToolResult
        
        # Execute module
        spec.loader.exec_module(validation_module)
        print("✓ Validation tool module loaded successfully")
        
        # Test tool creation
        validation_tool = validation_module.ValidationTool()
        print(f"✓ Tool created: {validation_tool.name}")
        
        # Test basic functionality
        print("\n--- Testing Basic Validation ---")
        
        # Simple test case
        import asyncio
        
        async def test_validation():
            result = await validation_tool.execute(
                task_description="Test validation system",
                claimed_deliverables=["created test file"],
                actual_files=["test_file.py"],
                confidence_level="medium"
            )
            return result
        
        result = asyncio.run(test_validation())
        
        if result.success:
            print("✓ Validation execution successful")
            validation_data = json.loads(result.content)
            print(f"  Honesty Score: {validation_data.get('honesty_score', 'N/A')}/100")
            print(f"  Pass: {validation_data.get('pass_validation', False)}")
            return True
        else:
            print(f"✗ Validation execution failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"✗ Import/functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """Test that required files exist"""
    print("\n--- Testing File Structure ---")
    
    base_path = Path(__file__).parent / "mini_agent"
    
    required_files = [
        "agent.py",
        "tools/__init__.py",
        "skills/fact-checking-self-assessment/tools/validation_tool.py",
        "skills/fact-checking-self-assessment/scripts/register_validation_skill.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def test_agent_integration():
    """Test agent integration points"""
    print("\n--- Testing Agent Integration ---")
    
    agent_file = Path(__file__).parent / "mini_agent" / "agent.py"
    
    if not agent_file.exists():
        print("✗ agent.py not found")
        return False
    
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key integration points
        checks = [
            ("_validate_task_completion", "Task completion validation method"),
            ("validation_result", "Validation result processing"),
            ("honesty_score", "Honesty score handling")
        ]
        
        integration_ok = True
        for check, description in checks:
            if check in content:
                print(f"✓ {description} present")
            else:
                print(f"✗ {description} missing")
                integration_ok = False
        
        return integration_ok
        
    except Exception as e:
        print(f"✗ Error reading agent.py: {e}")
        return False


def main():
    """Run all tests"""
    print("QA Validation System - Comprehensive Test")
    print("=" * 50)
    
    # Run tests
    test1 = test_qa_imports()
    test2 = test_file_structure()
    test3 = test_agent_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Import Test: {'PASS' if test1 else 'FAIL'}")
    print(f"File Structure Test: {'PASS' if test2 else 'FAIL'}")
    print(f"Agent Integration Test: {'PASS' if test3 else 'FAIL'}")
    
    if test1 and test2 and test3:
        print("\n🎉 ALL TESTS PASSED")
        print("QA Validation System is operational and properly integrated!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED")
        print("QA Validation System needs fixes before production use.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)