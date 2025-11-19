#!/usr/bin/env python3
"""
Architectural Compliance Validation for VS Code Integration

Validates that VS Code integration follows Mini-Agent's intrinsic architecture:
- Progressive skill loading system
- Knowledge graph integration  
- Native skill system alignment
- Modular design patterns
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

def validate_progressive_skill_system():
    """Validate VS Code integration follows progressive skill loading"""
    print("🔍 VALIDATING PROGRESSIVE SKILL LOADING")
    print("-" * 60)
    
    # Check skill metadata
    skill_file = Path("skills/vscode_integration_skill.md")
    if not skill_file.exists():
        print("❌ VS Code integration skill file missing")
        return False
    
    content = skill_file.read_text()
    
    # Validate progressive levels
    progressive_indicators = {
        "Level 1 (list_skills)": "list_skills()" in content,
        "Level 2 (get_skill)": "get_skill()" in content, 
        "Level 3 (execute_with_resources)": "execute_with_resources()" in content,
        "Progressive pattern": "Level 1:" in content and "Level 2:" in content and "Level 3:" in content
    }
    
    print("Progressive Skill Loading Pattern:")
    for level, present in progressive_indicators.items():
        print(f"  {'✅' if present else '❌'} {level}: {'Present' if present else 'Missing'}")
    
    # Validate implementation follows architecture
    implementation_file = Path("skills/vscode_integration_implementation.py")
    if not implementation_file.exists():
        print("❌ Implementation file missing")
        return False
    
    impl_content = implementation_file.read_text()
    
    implementation_indicators = {
        "list_skills method": "async def list_skills" in impl_content,
        "get_skill method": "async def get_skill" in impl_content,
        "execute_with_resources method": "async def execute_with_resources" in impl_content,
        "VSCodeIntegrationSkill class": "class VSCodeIntegrationSkill" in impl_content
    }
    
    print("\nImplementation Methods:")
    for method, present in implementation_indicators.items():
        print(f"  {'✅' if present else '❌'} {method}: {'Present' if present else 'Missing'}")
    
    progressive_score = (
        sum(progressive_indicators.values()) + 
        sum(implementation_indicators.values())
    ) / (len(progressive_indicators) + len(implementation_indicators)) * 100
    
    print(f"\n📊 Progressive Skill System Compliance: {progressive_score:.1f}%")
    
    return progressive_score >= 90

def validate_knowledge_graph_integration():
    """Validate knowledge graph integration"""
    print("\n🔍 VALIDATING KNOWLEDGE GRAPH INTEGRATION")
    print("-" * 60)
    
    impl_file = Path("skills/vscode_integration_implementation.py")
    if not impl_file.exists():
        print("❌ Implementation file missing")
        return False
    
    content = impl_file.read_text()
    
    # Check knowledge graph integration indicators
    kg_indicators = {
        "Session context tracking": "session_id" in content,
        "Knowledge graph reference": "knowledge_graph" in content.lower(),
        "Context preservation": "context_preservation" in content.lower(),
        "Persistent state": "persistent" in content.lower(),
        "Workspace intelligence": "workspace" in content.lower()
    }
    
    print("Knowledge Graph Integration:")
    for indicator, present in kg_indicators.items():
        print(f"  {'✅' if present else '❌'} {indicator}: {'Present' if present else 'Missing'}")
    
    kg_score = sum(kg_indicators.values()) / len(kg_indicators) * 100
    print(f"\n📊 Knowledge Graph Integration: {kg_score:.1f}%")
    
    return kg_score >= 80

def validate_native_skill_system_alignment():
    """Validate alignment with Mini-Agent's native skill system"""
    print("\n🔍 VALIDATING NATIVE SKILL SYSTEM ALIGNMENT")
    print("-" * 60)
    
    # Check skill loader integration
    skill_loader = Path("mini_agent/tools/skill_loader.py")
    if not skill_loader.exists():
        print("❌ Skill loader not found")
        return False
    
    # Check if VS Code integration follows skill system patterns
    impl_file = Path("skills/vscode_integration_implementation.py")
    impl_content = impl_file.read_text() if impl_file.exists() else ""
    
    system_indicators = {
        "Skill metadata structure": "skill_metadata" in impl_content,
        "Allowed tools definition": "allowed_tools" in impl_content.lower(),
        "Tool routing through Mini-Agent": "route_through_mini_agent" in impl_content.lower(),
        "Native tool access": "existing_tools" in impl_content.lower(),
        "Skill registration function": "register_vscode_integration_skill" in impl_content
    }
    
    print("Native Skill System Alignment:")
    for indicator, present in system_indicators.items():
        print(f"  {'✅' if present else '❌'} {indicator}: {'Present' if present else 'Missing'}")
    
    system_score = sum(system_indicators.values()) / len(system_indicators) * 100
    print(f"\n📊 Native Skill System Alignment: {system_score:.1f}%")
    
    return system_score >= 85

def validate_modular_design():
    """Validate modular design principles"""
    print("\n🔍 VALIDATING MODULAR DESIGN")
    print("-" * 60)
    
    # Check separation of concerns
    skill_file = Path("skills/vscode_integration_skill.md")
    impl_file = Path("skills/vscode_integration_implementation.py")
    
    modular_indicators = {
        "Skill definition separated": skill_file.exists(),
        "Implementation separated": impl_file.exists(),
        "Clear skill boundaries": "Skill:" in skill_file.read_text() if skill_file.exists() else False,
        "Progressive disclosure": "## Overview" in skill_file.read_text() if skill_file.exists() else False,
        "Modular architecture": "modular" in impl_file.read_text().lower() if impl_file.exists() else False
    }
    
    print("Modular Design Principles:")
    for principle, present in modular_indicators.items():
        print(f"  {'✅' if present else '❌'} {principle}: {'Present' if present else 'Missing'}")
    
    modular_score = sum(modular_indicators.values()) / len(modular_indicators) * 100
    print(f"\n📊 Modular Design Compliance: {modular_score:.1f}%")
    
    return modular_score >= 90

def validate_architecture_compliance():
    """Validate overall architectural compliance"""
    print("\n🔍 VALIDATING ARCHITECTURAL COMPLIANCE")
    print("-" * 60)
    
    # Read architectural requirements
    arch_doc = Path("documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md")
    if not arch_doc.exists():
        print("❌ Architectural document missing")
        return False
    
    arch_content = arch_doc.read_text()
    
    # Check key architectural patterns
    arch_patterns = {
        "Progressive skill system": "Progressive Skill Loading System" in arch_content,
        "Tool loading architecture": "Tool Loading Architecture" in arch_content,
        "Knowledge graph": "Knowledge Graph Persistence" in arch_content,
        "Protocol compliance": "ACP Server Integration" in arch_content,
        "Workspace intelligence": "Workspace Intelligence" in arch_content
    }
    
    print("Required Architectural Patterns:")
    for pattern, required in arch_patterns.items():
        status = "✅ Required" if required else "❌ Missing"
        print(f"  {status} {pattern}")
    
    # Check our implementation against these patterns
    impl_content = Path("skills/vscode_integration_implementation.py").read_text()
    
    implementation_patterns = {
        "Follows progressive loading": "list_skills" in impl_content and "get_skill" in impl_content,
        "Uses skill loader pattern": "Skill" in impl_content and "loader" in impl_content.lower(),
        "Integrates with knowledge graph": "knowledge_graph" in impl_content.lower(),
        "Protocol compliant": "Chat API" in impl_content and "JSON-RPC" in impl_content,
        "Workspace aware": "workspace" in impl_content.lower()
    }
    
    print("\nImplementation Against Patterns:")
    for pattern, implemented in implementation_patterns.items():
        print(f"  {'✅' if implemented else '❌'} {pattern}: {'Implemented' if implemented else 'Missing'}")
    
    arch_score = sum(implementation_patterns.values()) / len(implementation_patterns) * 100
    print(f"\n📊 Architectural Compliance: {arch_score:.1f}%")
    
    return arch_score >= 85

def test_skill_progression():
    """Test the actual skill progression workflow"""
    print("\n🔍 TESTING SKILL PROGRESSION WORKFLOW")
    print("-" * 60)
    
    try:
        # Import the skill implementation
        sys.path.insert(0, str(Path.cwd()))
        from skills.vscode_integration_implementation import VSCodeIntegrationSkill, register_vscode_integration_skill
        
        # Test skill registration
        registration = register_vscode_integration_skill()
        print(f"✅ Skill registration function: {registration['skill_name']}")
        
        # Test skill instantiation
        skill = VSCodeIntegrationSkill()
        print(f"✅ Skill instance created: {skill.skill_metadata['name']}")
        
        # Test Level 1: list_skills
        level1_result = await_skill_method(skill.list_skills())
        if level1_result and "skill_name" in level1_result:
            print(f"✅ Level 1 (list_skills): {level1_result['skill_name']}")
        else:
            print("❌ Level 1 (list_skills) failed")
            return False
        
        # Test Level 2: get_skill  
        level2_result = await_skill_method(skill.get_skill("vscode_integration"))
        if level2_result and "skill_name" in level2_result:
            print(f"✅ Level 2 (get_skill): {level2_result['skill_name']}")
        else:
            print("❌ Level 2 (get_skill) failed")
            return False
        
        # Test Level 3: execute_with_resources
        level3_result = await_skill_method(skill.execute_with_resources("vscode_integration", mode="chat_api"))
        if level3_result and "status" in level3_result:
            print(f"✅ Level 3 (execute_with_resources): {level3_result['status']}")
        else:
            print("❌ Level 3 (execute_with_resources) failed")
            return False
        
        print("✅ Complete skill progression workflow tested successfully")
        return True
        
    except Exception as e:
        print(f"❌ Skill progression test failed: {e}")
        return False

def await_skill_method(method):
    """Helper to handle async method testing"""
    import asyncio
    try:
        return asyncio.run(method())
    except Exception as e:
        print(f"   ⚠️ Async execution issue: {e}")
        return None

def main():
    """Main validation function"""
    print("🏗️ MINI-AGENT ARCHITECTURAL COMPLIANCE VALIDATION")
    print("=" * 80)
    print("Validating VS Code integration against Mini-Agent's intrinsic architecture")
    print("=" * 80)
    
    # Run all validations
    progressive_ok = validate_progressive_skill_system()
    knowledge_graph_ok = validate_knowledge_graph_integration()
    native_system_ok = validate_native_skill_system_alignment()
    modular_ok = validate_modular_design()
    architecture_ok = validate_architecture_compliance()
    
    # Test skill progression
    progression_ok = test_skill_progression()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 ARCHITECTURAL COMPLIANCE SUMMARY")
    print("=" * 80)
    
    test_results = {
        "Progressive Skill Loading": progressive_ok,
        "Knowledge Graph Integration": knowledge_graph_ok,
        "Native Skill System Alignment": native_system_ok,
        "Modular Design": modular_ok,
        "Architecture Compliance": architecture_ok,
        "Skill Progression Workflow": progression_ok
    }
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    overall_score = passed_tests / total_tests * 100
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 ARCHITECTURAL COMPLIANCE SCORE: {overall_score:.1f}% ({passed_tests}/{total_tests})")
    
    # Final assessment
    if overall_score >= 90:
        print("\n✅ ARCHITECTURAL COMPLIANCE EXCELLENT")
        print("🚀 VS Code integration fully aligns with Mini-Agent architecture")
        print("📋 Implementation follows progressive skill loading patterns")
        print("🔧 Ready for integration with Mini-Agent's skill system")
    elif overall_score >= 75:
        print("\n⚠️ ARCHITECTURAL COMPLIANCE GOOD")
        print("🔧 Minor adjustments needed for full compliance")
    else:
        print("\n❌ ARCHITECTURAL COMPLIANCE NEEDS WORK")
        print("🛠️ Significant alignment required")
    
    # Architectural recommendations
    print("\n💡 ARCHITECTURAL RECOMMENDATIONS")
    print("-" * 50)
    
    if not progressive_ok:
        print("📝 Ensure all three progressive levels are implemented")
    if not knowledge_graph_ok:
        print("🧠 Integrate with Mini-Agent's knowledge graph system")
    if not native_system_ok:
        print("🔧 Align with native skill loader patterns")
    if not modular_ok:
        print("📦 Maintain clear separation between skill definition and implementation")
    if not architecture_ok:
        print("🏗️ Follow architectural patterns from MINI_AGENT_ARCHITECTURAL_MASTERY.md")
    
    return {
        "compliance_score": overall_score,
        "test_results": test_results,
        "architecturally_compliant": overall_score >= 90
    }

if __name__ == "__main__":
    import asyncio
    
    # Fix async execution in main
    async def run_validation():
        return main()
    
    result = asyncio.run(run_validation())
