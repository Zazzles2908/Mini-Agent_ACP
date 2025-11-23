#!/usr/bin/env python3
"""
QA Validation Skill Integration

Integrates the QA validation tool with Mini-Agent's skill system,
providing seamless access to AI behavior validation capabilities.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directories to path for imports
skill_path = Path(__file__).parent.parent
sys.path.append(str(skill_path))

from tools.validation_tool import ValidationTool, ValidationRequest, ValidationResult
from tools.base import Tool, ToolResult


class QAValidationSkill:
    """QA Validation skill wrapper for Mini-Agent"""
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.validation_tool = ValidationTool()
        self.name = "qa_validation"
        self.description = "AI behavior validation and completion verification system"
    
    def get_skill_info(self) -> Dict[str, Any]:
        """Get skill information for skill loader"""
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0",
            "license": "MIT",
            "allowed_tools": ["validate_completion"],
            "skill_path": str(self.skill_path),
            "main_tool": self.validation_tool.name,
            "capabilities": [
                "AI claim verification",
                "Deception pattern detection", 
                "Implementation quality assessment",
                "Honesty score calculation",
                "Competence evaluation",
                "Automated validation workflows"
            ]
        }
    
    def get_tools(self) -> List[Tool]:
        """Get all tools provided by this skill"""
        return [self.validation_tool]
    
    def quick_validate(self, task_description: str, claimed_deliverables: List[str], 
                      actual_files: List[str], confidence_level: str = "medium") -> Dict[str, Any]:
        """Quick validation without full requirements analysis"""
        
        validation_request = ValidationRequest(
            task_description=task_description,
            claimed_deliverables=claimed_deliverables,
            requirements_checklist=[],  # No requirements for quick validation
            actual_files=actual_files,
            confidence_level=confidence_level,
            validation_level="quick"
        )
        
        import asyncio
        result = asyncio.run(self.validation_tool.engine.validate_completion(validation_request))
        
        return {
            "honesty_score": result.honesty_score,
            "pass_validation": result.pass_validation,
            "summary": result.validation_summary,
            "completed_claims": result.completed_claims,
            "recommendations": result.recommendations[:3]  # Top 3 recommendations
        }
    
    def strict_validate(self, task_description: str, claimed_deliverables: List[str],
                       requirements_checklist: List[str], actual_files: List[str],
                       confidence_level: str = "medium") -> Dict[str, Any]:
        """Comprehensive validation with full requirements analysis"""
        
        validation_request = ValidationRequest(
            task_description=task_description,
            claimed_deliverables=claimed_deliverables,
            requirements_checklist=requirements_checklist,
            actual_files=actual_files,
            confidence_level=confidence_level,
            validation_level="strict"
        )
        
        import asyncio
        result = asyncio.run(self.validation_tool.engine.validate_completion(validation_request))
        
        return {
            "honesty_score": result.honesty_score,
            "pass_validation": result.pass_validation,
            "summary": result.validation_summary,
            "completed_claims": result.completed_claims,
            "deception_patterns": result.deception_patterns,
            "competence_assessment": result.competence_assessment,
            "recommendations": result.recommendations,
            "requirement_coverage": result.reality_vs_claims.get("requirement_coverage", {}),
            "quality_metrics": result.competence_assessment
        }


def register_qa_validation_skill() -> QAValidationSkill:
    """Register the QA validation skill with Mini-Agent"""
    skill_path = Path(__file__).parent.parent
    return QAValidationSkill(skill_path)


def integrate_with_agent(agent_tools: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate QA validation tool with existing agent tools"""
    validation_tool = ValidationTool()
    
    # Add validation tool to agent's tool collection
    agent_tools[validation_tool.name] = validation_tool
    
    return agent_tools


def create_agent_integration_patch() -> str:
    """Generate a code patch for agent integration"""
    return """
# Agent Integration Patch for QA Validation

# 1. Add to agent tools initialization (in agent.py or tools/__init__.py)
from mini_agent.skills.fact-checking-self-assessment.tools.validation_tool import ValidationTool

# Add to tool registry
self.tools = {
    # existing tools...
    "validate_completion": ValidationTool(),
}

# 2. Add pre-completion validation method
async def run_qa_validation(self, task: Task) -> Dict[str, Any]:
    '''Run QA validation before task completion'''
    qa_tool = self.tools.get("validate_completion")
    if not qa_tool:
        return {"honesty_score": 100, "pass_validation": True}  # Skip if tool not available
    
    request = ValidationRequest(
        task_description=task.description,
        claimed_deliverables=task.completed_items,
        actual_files=task.created_files,
        confidence_level=getattr(task, 'confidence_level', 'medium')
    )
    
    return await qa_tool.execute(**request.__dict__)

# 3. Add to task completion logic (in agent.py)
async def complete_task(self, task: Task) -> TaskResult:
    if not self.task_is_complete(task):
        return self.continue_task()
    
    # 🚨 NEW: QA Validation Phase
    qa_result = await self.run_qa_validation(task)
    
    if not qa_result.get("pass_validation", True):
        # Force iteration with honest feedback
        feedback = f"QA Validation Failed (Score: {qa_result['honesty_score']}/100):\\n"
        feedback += "\\n".join(qa_result.get("recommendations", []))
        self.add_to_context(f"QA Validation failed - needs improvement")
        return self.continue_task(f"Fix QA issues: {feedback}")
    
    # Add honesty score to task context
    task.honesty_score = qa_result.get("honesty_score", 100)
    
    return self.finalize_completion(task)
"""


def main():
    """Demonstration and testing of QA validation skill"""
    print("🧪 QA Validation Skill Integration Test")
    print("=" * 50)
    
    # Initialize QA validation skill
    skill = register_qa_validation_skill()
    skill_info = skill.get_skill_info()
    
    print(f"✅ Skill Registered: {skill_info['name']}")
    print(f"📋 Description: {skill_info['description']}")
    print(f"🔧 Tools: {skill_info['allowed_tools']}")
    
    # Test quick validation
    print("\\n🚀 Testing Quick Validation...")
    
    test_task = "Build web authentication system"
    test_claims = [
        "Created auth.py with JWT authentication",
        "Implemented user registration and login",
        "Added error handling for invalid credentials",
        "Deployed to production server"
    ]
    test_files = ["auth.py", "login.html"]
    
    quick_result = skill.quick_validate(test_task, test_claims, test_files, "high")
    
    print(f"📊 Quick Validation Results:")
    print(f"   Honesty Score: {quick_result['honesty_score']}/100")
    print(f"   Pass Validation: {quick_result['pass_validation']}")
    print(f"   Summary: {quick_result['summary']}")
    print(f"   Completed Claims: {len(quick_result['completed_claims'])}")
    print(f"   Top Recommendations: {quick_result['recommendations']}")
    
    # Test strict validation
    print("\\n🔍 Testing Strict Validation...")
    
    test_requirements = [
        "JWT token generation",
        "Password hashing and security",
        "Session management", 
        "Error handling for invalid credentials",
        "Logout functionality"
    ]
    
    strict_result = skill.strict_validate(test_task, test_claims, test_requirements, test_files, "high")
    
    print(f"📊 Strict Validation Results:")
    print(f"   Honesty Score: {strict_result['honesty_score']}/100")
    print(f"   Pass Validation: {strict_result['pass_validation']}")
    print(f"   Summary: {strict_result['summary']}")
    print(f"   Deception Patterns: {len(strict_result['deception_patterns'])}")
    print(f"   Competence Assessment: {strict_result['competence_assessment']}")
    
    # Show integration patch
    print("\\n🔧 Agent Integration Instructions:")
    print("=" * 30)
    print(create_agent_integration_patch())
    
    print("\\n✅ QA Validation Skill Ready for Integration!")
    print("📝 Next steps:")
    print("   1. Add ValidationTool to agent tool registry")
    print("   2. Integrate pre-completion validation in agent loop") 
    print("   3. Test with real agent workflows")
    print("   4. Enable automatic validation for all completions")


if __name__ == "__main__":
    main()
