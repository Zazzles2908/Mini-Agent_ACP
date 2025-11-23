#!/usr/bin/env python3
"""
QA Validation Skill Registration Script

Registers the QA validation system with Mini-Agent's skill loading framework.
This script ensures the validation tool is properly integrated into the agent's tool ecosystem.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "mini_agent"))

from mini_agent.tools.base import Tool


def create_validation_tool():
    """
    Create a QA validation tool instance using direct module loading.
    
    Returns:
        Tool object for validation or None if failed
    """
    try:
        # Load the validation tool module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "validation_tool",
            Path(__file__).parent / "tools" / "validation_tool.py"
        )
        validation_module = importlib.util.module_from_spec(spec)
        
        # Load the base Tool class first
        from mini_agent.tools.base import Tool, ToolResult
        
        # Add base classes to validation module
        validation_module.Tool = Tool
        validation_module.ToolResult = ToolResult
        
        # Execute the validation module
        spec.loader.exec_module(validation_module)
        
        # Create and return validation tool instance
        tool_instance = validation_module.ValidationTool()
        return tool_instance
        
    except Exception as e:
        print(f"Failed to create validation tool: {e}")
        return None


def register_qa_validation_tools() -> List[Tool]:
    """
    Register QA validation tools with Mini-Agent's tool system.
    
    Returns:
        List of Tool objects ready for agent integration
    """
    try:
        # Create the validation tool instance
        validation_tool = create_validation_tool()
        
        if validation_tool:
            print(f"QA Validation Tool registered: {validation_tool.name}")
            print(f"   Description: {validation_tool.description}")
            print(f"   Parameters: {len(validation_tool.parameters['properties'])} validation parameters")
            return [validation_tool]
        else:
            print("Failed to create validation tool instance")
            return []
        
    except Exception as e:
        print(f"Failed to register QA validation tools: {e}")
        return []


def get_skill_metadata() -> Dict[str, Any]:
    """
    Get metadata for the QA validation skill.
    
    Returns:
        Dictionary containing skill information
    """
    return {
        "name": "fact-checking-self-assessment",
        "version": "1.0.0",
        "description": "AI behavior validation and completion verification system",
        "category": "Quality Assurance",
        "capabilities": [
            "Claim vs Reality Validation",
            "Deception Pattern Detection", 
            "Implementation Quality Assessment",
            "Honesty Score Generation",
            "Competence Evaluation",
            "Automated Feedback Generation"
        ],
        "integration_points": [
            "Agent completion workflow",
            "Task validation checkpoint",
            "Quality assessment feedback",
            "Continuous improvement tracking"
        ],
        "architectural_notes": {
            "uses_minimax_m2": True,  # Uses MiniMax-M2 for reasoning
            "uses_zai": False,        # Does NOT use Z.AI (web functionality only)
            "native_integration": True,  # Built into agent loop
            "optional_enablement": True,  # Graceful degradation when unavailable
            "credit_protection": "Not applicable"  # No external API calls
        }
    }


def validate_installation():
    """
    Validate that the QA validation system is properly installed.
    
    Returns:
        True if installation is valid, False otherwise
    """
    try:
        # Check if validation tool can be created
        tool = create_validation_tool()
        if tool:
            print("Validation tool creation successful")
        else:
            print("Validation tool creation failed")
            return False
        
        # Check if agent integration methods exist
        agent_path = project_root / "mini_agent" / "agent.py"
        if agent_path.exists():
            with open(agent_path, 'r') as f:
                content = f.read()
                if "_validate_task_completion" in content:
                    print("Agent integration methods present")
                else:
                    print("Agent integration methods missing")
                    return False
        else:
            print("Agent.py not found")
            return False
            
        # Check if tools module integration exists
        tools_init_path = project_root / "mini_agent" / "tools" / "__init__.py"
        if tools_init_path.exists():
            with open(tools_init_path, 'r') as f:
                content = f.read()
                if "ValidationTool" in content and "_qa_tools_available" in content:
                    print("Tools module integration present")
                else:
                    print("Tools module integration missing")
                    return False
        else:
            print("Tools __init__.py not found")
            return False
            
        print("QA Validation System installation validated")
        return True
        
    except Exception as e:
        print(f"Installation validation failed: {e}")
        return False


def main():
    """Main registration function"""
    print("QA Validation System Registration")
    print("=" * 50)
    
    # Validate installation
    if not validate_installation():
        print("Installation validation failed")
        return False
    
    # Register tools
    tools = register_qa_validation_tools()
    if not tools:
        print("Tool registration failed")
        return False
    
    # Display skill metadata
    metadata = get_skill_metadata()
    print(f"\nSkill Metadata:")
    print(f"   Name: {metadata['name']} v{metadata['version']}")
    print(f"   Category: {metadata['category']}")
    print(f"   Capabilities: {len(metadata['capabilities'])} features")
    print(f"   Integration Points: {len(metadata['integration_points'])} points")
    
    # Architectural transparency
    arch_notes = metadata['architectural_notes']
    print(f"\nArchitecture Transparency:")
    print(f"   Uses MiniMax-M2: {arch_notes['uses_minimax_m2']} YES")
    print(f"   Uses Z.AI: {arch_notes['uses_zai']} NO (Z.AI only for web functionality)")
    print(f"   Native Integration: {arch_notes['native_integration']} YES")
    print(f"   Optional Enablement: {arch_notes['optional_enablement']} YES")
    print(f"   Credit Protection: {arch_notes['credit_protection']} N/A")
    
    print("\nQA Validation System ready for use!")
    print("   Integrates automatically into agent completion workflow")
    print("   Detects AI deception patterns and validates claims")
    print("   Protects against false completion reporting")
    print("   Improves AI honesty and competence over time")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)