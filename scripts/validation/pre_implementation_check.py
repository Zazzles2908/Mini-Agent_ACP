#!/usr/bin/env python3
"""
Pre-Implementation Check for Mini-Agent Tasks

This script performs comprehensive validation before starting any implementation task.
Must be run by all agents before beginning work to ensure proper setup and compliance.

Usage: python scripts/validation/pre_implementation_check.py
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

class PreImplementationValidator:
    """Comprehensive pre-implementation validation"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.validation_results = {}
        
    def check_workspace_cleanliness(self) -> Dict[str, Any]:
        """Check for polluting files in main directory"""
        results = {
            "check_name": "workspace_cleanliness",
            "description": "Validates no Python files or wrong directories in main directory",
            "passed": True,
            "violations": [],
            "score": 100
        }
        
        # Check for Python files in main directory (excluding core files)
        main_py_files = list(self.workspace_path.glob("*.py"))
        allowed_py_files = {"setup.py", "pyproject.toml", "__init__.py"}  # Core project files
        
        for py_file in main_py_files:
            if py_file.name not in allowed_py_files:
                results["violations"].append(f"Python file in main directory: {py_file.name}")
                results["passed"] = False
                results["score"] -= 25
        
        # Check for wrong skills directory
        wrong_skills_dir = self.workspace_path / "skills"
        if wrong_skills_dir.exists():
            results["violations"].append("Wrong skills directory: /skills should not exist")
            results["passed"] = False
            results["score"] -= 50
        
        # Check for validation scripts in main directory
        validation_files = [f for f in main_py_files if any(word in f.name.lower() 
                           for word in ['test', 'fact', 'check', 'validation', 'verify'])]
        if validation_files:
            results["violations"].extend([f"Validation script in main: {f.name}" for f in validation_files])
            results["passed"] = False
            results["score"] -= 15 * len(validation_files)
        
        results["score"] = max(0, results["score"])
        return results
    
    def check_required_directories(self) -> Dict[str, Any]:
        """Check for required directory structure"""
        results = {
            "check_name": "required_directories",
            "description": "Validates required directories exist and are properly organized",
            "passed": True,
            "violations": [],
            "score": 100
        }
        
        required_dirs = [
            "documents/",
            "documents/architecture/",
            "documents/workflows/", 
            "scripts/",
            "scripts/validation/",
            "mini_agent/skills/"
        ]
        
        missing_dirs = []
        for req_dir in required_dirs:
            dir_path = self.workspace_path / req_dir
            if not dir_path.exists():
                missing_dirs.append(req_dir)
                results["violations"].append(f"Missing required directory: {req_dir}")
        
        if missing_dirs:
            results["passed"] = False
            results["score"] = max(0, 100 - (len(missing_dirs) * 20))
        
        return results
    
    def check_architecture_documents(self) -> Dict[str, Any]:
        """Check for required architectural documents"""
        results = {
            "check_name": "architecture_documents",
            "description": "Validates required architectural documents exist",
            "passed": True,
            "violations": [],
            "score": 100
        }
        
        required_docs = [
            "documents/architecture/MINI_AGENT_ARCHITECTURAL_MASTERY.md",
            "documents/workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md",
            "documents/AGENT_BEST_PRACTICES.md"
        ]
        
        missing_docs = []
        for doc_path in required_docs:
            full_path = self.workspace_path / doc_path
            if not full_path.exists():
                missing_docs.append(doc_path)
                results["violations"].append(f"Missing required document: {doc_path}")
        
        if missing_docs:
            results["passed"] = False
            results["score"] = max(0, 100 - (len(missing_docs) * 33))
        
        return results
    
    def check_git_status(self) -> Dict[str, Any]:
        """Check git repository status"""
        results = {
            "check_name": "git_status",
            "description": "Validates git repository is in good state",
            "passed": True,
            "violations": [],
            "score": 100
        }
        
        try:
            # Check if git repo exists
            git_result = subprocess.run(
                ["git", "status", "--porcelain"], 
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )
            
            if git_result.returncode != 0:
                results["violations"].append("Not a git repository or git not available")
                results["passed"] = False
                results["score"] = 50
                return results
            
            # Check for uncommitted changes
            if git_result.stdout.strip():
                results["violations"].append("Uncommitted changes in repository")
                results["score"] = 80  # Not critical but should be noted
            
            # Check git log access
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-1"], 
                cwd=self.workspace_path,
                capture_output=True,
                text=True
            )
            
            if log_result.returncode != 0:
                results["violations"].append("Cannot access git log")
                results["score"] -= 20
                
        except FileNotFoundError:
            results["violations"].append("Git not installed or not in PATH")
            results["passed"] = False
            results["score"] = 0
        except Exception as e:
            results["violations"].append(f"Git validation error: {str(e)}")
            results["score"] = 60
        
        return results
    
    def run_comprehensive_pre_check(self) -> Dict[str, Any]:
        """Run all pre-implementation checks"""
        checks = [
            self.check_workspace_cleanliness(),
            self.check_required_directories(),
            self.check_architecture_documents(),
            self.check_git_status()
        ]
        
        # Calculate overall score
        total_score = sum(check["score"] for check in checks)
        overall_score = total_score / len(checks)
        
        # Determine if ready to proceed
        ready_to_proceed = all(check["passed"] for check in checks) and overall_score >= 80
        
        # Generate summary
        all_violations = []
        for check in checks:
            all_violations.extend(check["violations"])
        
        results = {
            "ready_to_proceed": ready_to_proceed,
            "overall_score": round(overall_score, 1),
            "pre_check_status": "✅ Ready" if ready_to_proceed else "❌ Not Ready",
            "individual_checks": checks,
            "total_violations": len(all_violations),
            "violations": all_violations,
            "recommendations": self._generate_recommendations(checks, ready_to_proceed),
            "validation_timestamp": "2025-11-20 05:22:00"
        }
        
        return results
    
    def _generate_recommendations(self, checks: List[Dict], ready: bool) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        if not ready:
            recommendations.append("🚨 CRITICAL: Pre-implementation checks failed")
            recommendations.append("🔧 REQUIRED: Address all violations before proceeding")
            recommendations.append("📋 ACTION: Run validation and remediation scripts")
        else:
            recommendations.append("✅ PRE-CHECKS PASSED: Safe to proceed with implementation")
            recommendations.append("📝 NEXT: Review Universal Workflow Protocol")
            recommendations.append("🎯 READY: Begin Phase 1 of implementation workflow")
        
        # Add specific recommendations based on violations
        workspace_check = next((c for c in checks if c["check_name"] == "workspace_cleanliness"), None)
        if workspace_check and not workspace_check["passed"]:
            recommendations.append("🧹 CLEANUP: Remove polluting files from main directory")
        
        dirs_check = next((c for c in checks if c["check_name"] == "required_directories"), None)
        if dirs_check and not dirs_check["passed"]:
            recommendations.append("📁 STRUCTURE: Create missing required directories")
        
        docs_check = next((c for c in checks if c["check_name"] == "architecture_documents"), None)
        if docs_check and not docs_check["passed"]:
            recommendations.append("📚 DOCUMENTATION: Add missing architectural documents")
        
        return recommendations

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🚀 PRE-IMPLEMENTATION VALIDATION")
    print("="*60)
    
    validator = PreImplementationValidator()
    results = validator.run_comprehensive_pre_check()
    
    print(f"\n📊 Overall Score: {results['overall_score']}%")
    print(f"📋 Status: {results['pre_check_status']}")
    
    print(f"\n📋 Individual Check Results:")
    for check in results["individual_checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"  {status} {check['check_name']}: {check['score']}%")
        if check["violations"]:
            for violation in check["violations"]:
                print(f"     • {violation}")
    
    print(f"\n💡 Recommendations:")
    for rec in results["recommendations"]:
        print(f"  {rec}")
    
    print(f"\n⏰ Validation Time: {results['validation_timestamp']}")
    
    # Save detailed results
    with open("pre_implementation_check_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed report saved: pre_implementation_check_report.json")
    
    # Exit with appropriate code
    if results["ready_to_proceed"]:
        print(f"\n✅ VALIDATION SUCCESSFUL: Ready to proceed with implementation")
        exit(0)
    else:
        print(f"\n🚨 VALIDATION FAILED: Please address violations before proceeding")
        print(f"🔧 REQUIRED ACTIONS:")
        print(f"   1. Fix all workspace cleanliness violations")
        print(f"   2. Create missing required directories")
        print(f"   3. Add missing architectural documents")
        print(f"   4. Re-run this validation")
        exit(1)

if __name__ == "__main__":
    main()