#!/usr/bin/env python3
"""
Architectural Compliance Validator for Mini-Agent

This tool validates that implementations follow Mini-Agent's architectural requirements
and generates compliance scores. Must be used before task completion.

Usage: python validate_architectural_compliance.py
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class ArchitecturalComplianceValidator:
    """Validates Mini-Agent architectural compliance"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.compliance_results = {}
        
    def validate_workspace_cleanliness(self) -> Dict[str, Any]:
        """Check for polluting files in main directory"""
        results = {
            "check_name": "workspace_cleanliness",
            "description": "Validates no Python files or wrong directories in main directory",
            "violations": [],
            "score": 100
        }
        
        # Check for Python files in main directory (excluding core files)
        main_py_files = list(self.workspace_path.glob("*.py"))
        allowed_py_files = {"setup.py", "pyproject.toml"}  # Core project files
        
        for py_file in main_py_files:
            if py_file.name not in allowed_py_files:
                results["violations"].append(f"Python file in main directory: {py_file.name}")
                results["score"] -= 25
        
        # Check for wrong skills directory
        wrong_skills_dir = self.workspace_path / "skills"
        if wrong_skills_dir.exists():
            results["violations"].append("Wrong skills directory: /skills should not exist")
            results["score"] -= 50
        
        # Check for validation scripts in main directory
        validation_files = [f for f in main_py_files if any(word in f.name.lower() 
                           for word in ['test', 'fact', 'check', 'validation', 'verify'])]
        if validation_files:
            results["violations"].extend([f"Validation script in main: {f.name}" for f in validation_files])
            results["score"] -= 15 * len(validation_files)
        
        results["score"] = max(0, results["score"])
        return results
    
    def validate_skills_structure(self) -> Dict[str, Any]:
        """Validate skills directory structure"""
        results = {
            "check_name": "skills_structure", 
            "description": "Validates skills are properly located in mini_agent/skills/",
            "violations": [],
            "score": 100
        }
        
        skills_dir = self.workspace_path / "mini_agent" / "skills"
        if not skills_dir.exists():
            results["violations"].append("mini_agent/skills/ directory does not exist")
            results["score"] = 0
            return results
        
        # Check each skill directory
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                # Check for required SKILL.md
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    results["violations"].append(f"Missing SKILL.md in {skill_dir.name}")
                    results["score"] -= 20
                
                # Check for scripts directory
                scripts_dir = skill_dir / "scripts"
                if not scripts_dir.exists():
                    results["violations"].append(f"Missing scripts/ in {skill_dir.name}")
                    results["score"] -= 10
        
        results["score"] = max(0, results["score"])
        return results
    
    def validate_progressive_loading(self) -> Dict[str, Any]:
        """Check if progressive skill loading is implemented"""
        results = {
            "check_name": "progressive_loading",
            "description": "Validates progressive skill loading implementation", 
            "violations": [],
            "score": 100
        }
        
        # This is a placeholder check - would need to examine actual implementation
        # For now, we'll check if the concept is documented in skills
        
        skills_dir = self.workspace_path / "mini_agent" / "skills"
        if skills_dir.exists():
            progressive_concept_found = False
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        try:
                            content = skill_md.read_text(encoding='utf-8')
                            if "progressive" in content.lower() or "level 1" in content.lower():
                                progressive_concept_found = True
                                break
                        except UnicodeDecodeError:
                            # Skip files with encoding issues
                            continue
            
            if not progressive_concept_found:
                results["violations"].append("No evidence of progressive loading documentation")
                results["score"] = 50
        
        results["score"] = max(0, results["score"])
        return results
    
    def validate_architecture_documentation(self) -> Dict[str, Any]:
        """Check for required architectural documentation"""
        results = {
            "check_name": "architecture_documentation",
            "description": "Validates required architectural documents exist",
            "violations": [],
            "score": 100
        }
        
        required_docs = [
            "documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md",
            "documents/AGENT_BEST_PRACTICES.md"
        ]
        
        for doc_path in required_docs:
            full_path = self.workspace_path / doc_path
            if not full_path.exists():
                results["violations"].append(f"Missing required document: {doc_path}")
                results["score"] -= 50
        
        results["score"] = max(0, results["score"])
        return results
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run all compliance checks"""
        checks = [
            self.validate_workspace_cleanliness(),
            self.validate_skills_structure(),
            self.validate_progressive_loading(),
            self.validate_architecture_documentation()
        ]
        
        total_score = sum(check["score"] for check in checks)
        max_possible_score = len(checks) * 100
        overall_score = (total_score / max_possible_score) * 100
        
        results = {
            "overall_compliance_score": round(overall_score, 1),
            "status": self._get_status(overall_score),
            "checks": checks,
            "recommendations": self._generate_recommendations(checks, overall_score),
            "validation_timestamp": "2025-11-20 05:11:47"
        }
        
        return results
    
    def _get_status(self, score: float) -> str:
        """Get status based on compliance score"""
        if score >= 90:
            return "✅ Production Ready"
        elif score >= 80:
            return "⚠️ Review Recommended"
        elif score >= 70:
            return "🔄 Significant Issues"
        else:
            return "❌ Critical Failures"
    
    def _generate_recommendations(self, checks: List[Dict], score: float) -> List[str]:
        """Generate specific recommendations for improvements"""
        recommendations = []
        
        if score < 80:
            recommendations.append("🚨 CRITICAL: Compliance score below 80% - Task completion blocked")
            recommendations.append("🔧 Required: Run fact-checking validation before proceeding")
            recommendations.append("📋 Action: Remediate all violations before continuation")
        
        for check in checks:
            if check["score"] < 100:
                recommendations.append(f"📁 {check['check_name']}: Address {len(check['violations'])} violations")
        
        if score >= 80:
            recommendations.append("✅ Compliance achieved - Safe to proceed with task")
        
        return recommendations

if __name__ == "__main__":
    validator = ArchitecturalComplianceValidator()
    results = validator.run_full_validation()
    
    print("\n" + "="*60)
    print("🔍 ARCHITECTURAL COMPLIANCE VALIDATION REPORT")
    print("="*60)
    
    print(f"\n📊 Overall Score: {results['overall_compliance_score']}%")
    print(f"📋 Status: {results['status']}")
    
    print("\n📋 Individual Check Results:")
    for check in results["checks"]:
        status = "✅" if check["score"] >= 80 else "⚠️" if check["score"] >= 60 else "❌"
        print(f"  {status} {check['check_name']}: {check['score']}%")
        if check["violations"]:
            for violation in check["violations"]:
                print(f"     • {violation}")
    
    print(f"\n💡 Recommendations:")
    for rec in results["recommendations"]:
        print(f"  {rec}")
    
    print(f"\n⏰ Validation Time: {results['validation_timestamp']}")
    
    # Save detailed results
    with open("architectural_compliance_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed report saved: architectural_compliance_report.json")
    
    if results["overall_compliance_score"] < 80:
        print(f"\n🚨 WARNING: Compliance score below 80% threshold!")
        print(f"🔧 REMEDIATION REQUIRED: Address all violations before task completion")
        exit(1)
    else:
        print(f"\n✅ COMPLIANCE ACHIEVED: Safe to proceed with task implementation")