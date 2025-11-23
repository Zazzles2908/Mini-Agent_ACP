#!/usr/bin/env python3
"""
QA Self-Validation Test

This script tests the QA validation system on its own implementation
to detect any issues with the implementation itself.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_qa_validation_on_own_implementation():
    """Test the QA validation system on its own implementation"""
    
    print("🧪 QA SYSTEM SELF-VALIDATION TEST")
    print("=" * 50)
    
    try:
        # Import the validation tool using the lazy loading mechanism
        from mini_agent.tools import get_validation_tool
        ValidationTool = get_validation_tool()
        
        if ValidationTool is None:
            print("❌ Validation tool could not be loaded")
            return
        
        # Task description for validation
        task_description = """
        Implement and integrate a QA Validation System into Mini-Agent that detects 
        AI deception patterns and ensures honest task completion reporting. The system 
        should integrate into the agent loop and validate work quality before allowing 
        task completion.
        """
        
        # Claimed deliverables from the implementation
        claimed_deliverables = [
            "documents/02_SYSTEM_CORE/QA_VALIDATION_SYSTEM.md - Complete implementation blueprint",
            "documents/02_SYSTEM_CORE/QA_USAGE_GUIDE.md - User integration guide", 
            "mini_agent/skills/fact-checking-self-assessment/tools/validation_tool.py - Core validation engine",
            "mini_agent/tools/__init__.py - Tool integration and availability checks",
            "mini_agent/agent.py - Agent loop integration with validation hooks",
            "Integration with agent loop at task completion point",
            "Context extraction for task descriptions, deliverables, and requirements",
            "Honesty scoring system with 80/100 threshold",
            "Graceful fallback when validation unavailable"
        ]
        
        # Requirements that should be met
        requirements_checklist = [
            "Zero breaking changes to existing Mini-Agent functionality",
            "Progressive enhancement without workflow disruption",
            "Graceful degradation when validation tools unavailable",
            "Consistent UI using established Mini-Agent patterns",
            "Comprehensive error handling with user-friendly messages",
            "Automatic validation triggers at task completion",
            "Honesty scoring and feedback system",
            "Context extraction from agent messages and workspace"
        ]
        
        # Actual files created
        actual_files = [
            "documents/02_SYSTEM_CORE/QA_VALIDATION_SYSTEM.md",
            "documents/02_SYSTEM_CORE/QA_USAGE_GUIDE.md", 
            "documents/02_SYSTEM_CORE/QA_USAGE_GUIDE.md",
            "mini_agent/skills/fact-checking-self-assessment/tools/validation_tool.py",
            "mini_agent/skills/fact-checking-self-assessment/tools/__pycache__/validation_tool.cpython-313.pyc",
            "mini_agent/skills/fact-checking-self-assessment/scripts/agent_integration.py",
            "mini_agent/skills/fact-checking-self-assessment/scripts/__pycache__/agent_integration.cpython-313.pyc",
            "mini_agent/tools/__init__.py",
            "mini_agent/agent.py"
        ]
        
        print(f"📋 Task Description: {task_description[:100]}...")
        print(f"📁 Claimed Deliverables: {len(claimed_deliverables)} items")
        print(f"✅ Requirements: {len(requirements_checklist)} items") 
        print(f"📄 Actual Files: {len(actual_files)} items")
        print()
        
        # Create and execute validation
        validation_tool = ValidationTool()
        
        print("🔍 Running QA validation on own implementation...")
        print("-" * 50)
        
        result = await validation_tool.execute(
            task_description=task_description,
            claimed_deliverables=claimed_deliverables,
            requirements_checklist=requirements_checklist,
            actual_files=actual_files,
            confidence_level="high",
            validation_level="strict"
        )
        
        print("-" * 50)
        
        if result.success:
            print("✅ VALIDATION RESULT:")
            print(result.content)
        else:
            print("❌ VALIDATION FAILED:")
            print(result.error)
            
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qa_validation_on_own_implementation())