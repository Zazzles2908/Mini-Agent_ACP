#!/usr/bin/env python3
"""
Organization Validator for Scripts and Documents

This tool validates that scripts and documents follow proper organizational structure
and categorizes any misplaced files. Essential for maintaining workspace cleanliness.

Usage: python scripts/assessment/organization_validator.py
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple

class OrganizationValidator:
    """Validates and enforces organizational standards"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.organization_rules = {
            "scripts": {
                "validation": {
                    "description": "Fact-checking and architectural compliance",
                    "keywords": ["validation", "fact", "check", "compliance", "verify"],
                    "patterns": ["*validation*", "*fact*", "*check*", "*compliance*"]
                },
                "cleanup": {
                    "description": "Workspace maintenance and organization", 
                    "keywords": ["cleanup", "organize", "clean", "maintain"],
                    "patterns": ["*cleanup*", "*organize*", "*clean*"]
                },
                "assessment": {
                    "description": "System analysis and reporting",
                    "keywords": ["assessment", "analyze", "report", "status", "metrics"],
                    "patterns": ["*assessment*", "*analyze*", "*report*", "*status*"]
                },
                "deployment": {
                    "description": "Production deployment utilities",
                    "keywords": ["deploy", "release", "publish", "install"],
                    "patterns": ["*deploy*", "*release*", "*publish*"]
                },
                "testing": {
                    "description": "Test automation and fixtures",
                    "keywords": ["test", "fixture", "mock", "unit", "integration"],
                    "patterns": ["*test*", "*fixture*", "*mock*"]
                },
                "utilities": {
                    "description": "General-purpose helper scripts",
                    "keywords": ["utility", "helper", "common", "misc"],
                    "patterns": ["*utility*", "*helper*", "*common*"]
                }
            },
            "documents": {
                "architecture": {
                    "description": "System architecture and design documents",
                    "keywords": ["architecture", "design", "pattern", "specification", "api"],
                    "patterns": ["*ARCHITECTURAL*", "*DESIGN*", "*PATTERN*", "*SPECIFICATION*"]
                },
                "workflows": {
                    "description": "Workflow protocols and procedures",
                    "keywords": ["workflow", "protocol", "procedure", "guide", "process"],
                    "patterns": ["*WORKFLOW*", "*PROTOCOL*", "*PROCEDURE*", "*GUIDE*"]
                },
                "project": {
                    "description": "Project management and context",
                    "keywords": ["project", "context", "handoff", "roadmap", "requirement"],
                    "patterns": ["*PROJECT*", "*CONTEXT*", "*HANDOFF*", "*ROADMAP*"]
                },
                "setup": {
                    "description": "Setup and configuration guides",
                    "keywords": ["setup", "config", "install", "environment", "dependency"],
                    "patterns": ["*SETUP*", "*CONFIG*", "*INSTALL*"]
                },
                "examples": {
                    "description": "Usage examples and templates",
                    "keywords": ["example", "template", "sample", "usage"],
                    "patterns": ["*EXAMPLES*", "*TEMPLATE*", "*SAMPLE*"]
                },
                "testing": {
                    "description": "Testing documentation and results",
                    "keywords": ["test", "validation", "quality", "report"],
                    "patterns": ["*TESTING*", "*VALIDATION*", "*QUALITY*"]
                },
                "troubleshooting": {
                    "description": "Problem resolution guides",
                    "keywords": ["troubleshoot", "debug", "issue", "problem", "solution"],
                    "patterns": ["*TROUBLESHOOTING*", "*DEBUGGING*", "*ISSUES*"]
                }
            }
        }
        
    def categorize_file(self, file_path: Path, category: str) -> Tuple[str, float]:
        """Categorize a file based on its name and content"""
        
        file_name = file_path.name.lower()
        file_stem = file_path.stem.lower()
        
        best_category = "utilities"  # Default category
        best_score = 0.0
        
        for subcategory, rules in self.organization_rules[category].items():
            score = 0.0
            
            # Check keywords in filename
            for keyword in rules["keywords"]:
                if keyword in file_name or keyword in file_stem:
                    score += 1.0
            
            # Check patterns
            for pattern in rules["patterns"]:
                if pattern.replace("*", "").lower() in file_name:
                    score += 0.5
            
            if score > best_score:
                best_score = score
                best_category = subcategory
        
        return best_category, best_score
    
    def validate_scripts_organization(self) -> Dict[str, Any]:
        """Validate scripts organization"""
        results = {
            "category": "scripts",
            "description": "Validates scripts are properly categorized",
            "misplaced_files": [],
            "missing_directories": [],
            "organization_score": 100,
            "recommendations": []
        }
        
        scripts_dir = self.workspace_path / "scripts"
        
        # Check if scripts directory exists
        if not scripts_dir.exists():
            results["missing_directories"].append("scripts/")
            results["organization_score"] = 0
            return results
        
        # Validate each script
        for script_file in scripts_dir.rglob("*.py"):
            if script_file.name.startswith("."):
                continue
                
            # Skip guide files
            if script_file.name.endswith("_GUIDE.md") or script_file.name.endswith("_GUIDE.txt"):
                continue
            
            intended_category, score = self.categorize_file(script_file, "scripts")
            actual_category = script_file.parent.name
            
            if actual_category != intended_category:
                results["misplaced_files"].append({
                    "file": str(script_file.relative_to(self.workspace_path)),
                    "current_location": f"scripts/{actual_category}/",
                    "recommended_location": f"scripts/{intended_category}/",
                    "confidence": score,
                    "reason": f"File name suggests {intended_category} category"
                })
                
                # Reduce score based on misplacement severity
                penalty = 25 if score > 2.0 else 15
                results["organization_score"] -= penalty
        
        # Check for missing recommended directories
        recommended_dirs = set(self.organization_rules["scripts"].keys())
        existing_dirs = {d.name for d in scripts_dir.iterdir() if d.is_dir()}
        
        for recommended in recommended_dirs:
            if recommended not in existing_dirs:
                results["missing_directories"].append(f"scripts/{recommended}/")
                results["organization_score"] -= 5
        
        results["organization_score"] = max(0, results["organization_score"])
        
        # Generate recommendations
        if results["misplaced_files"]:
            results["recommendations"].append(
                f"Found {len(results['misplaced_files'])} misplaced script(s)"
            )
        
        if results["missing_directories"]:
            results["recommendations"].append(
                f"Missing {len(results['missing_directories'])} recommended directories"
            )
        
        return results
    
    def validate_documents_organization(self) -> Dict[str, Any]:
        """Validate documents organization"""
        results = {
            "category": "documents", 
            "description": "Validates documents are properly categorized",
            "misplaced_files": [],
            "missing_directories": [],
            "organization_score": 100,
            "recommendations": []
        }
        
        documents_dir = self.workspace_path / "documents"
        
        # Check if documents directory exists
        if not documents_dir.exists():
            results["missing_directories"].append("documents/")
            results["organization_score"] = 0
            return results
        
        # Validate each document
        for doc_file in documents_dir.rglob("*.md"):
            if doc_file.name.startswith("."):
                continue
                
            # Skip organization guide files
            if doc_file.name.endswith("_ORGANIZATION_GUIDE.md"):
                continue
            
            intended_category, score = self.categorize_file(doc_file, "documents")
            actual_category = doc_file.parent.name
            
            if actual_category != intended_category:
                results["misplaced_files"].append({
                    "file": str(doc_file.relative_to(self.workspace_path)),
                    "current_location": f"documents/{actual_category}/",
                    "recommended_location": f"documents/{intended_category}/",
                    "confidence": score,
                    "reason": f"File name suggests {intended_category} category"
                })
                
                # Reduce score based on misplacement severity
                penalty = 20 if score > 2.0 else 10
                results["organization_score"] -= penalty
        
        # Check for missing recommended directories
        recommended_dirs = set(self.organization_rules["documents"].keys())
        existing_dirs = {d.name for d in documents_dir.iterdir() if d.is_dir()}
        
        for recommended in recommended_dirs:
            if recommended not in existing_dirs:
                results["missing_directories"].append(f"documents/{recommended}/")
                results["organization_score"] -= 5
        
        results["organization_score"] = max(0, results["organization_score"])
        
        # Generate recommendations
        if results["misplaced_files"]:
            results["recommendations"].append(
                f"Found {len(results['misplaced_files'])} misplaced document(s)"
            )
        
        if results["missing_directories"]:
            results["recommendations"].append(
                f"Missing {len(results['missing_directories'])} recommended directories"
            )
        
        return results
    
    def run_full_organization_validation(self) -> Dict[str, Any]:
        """Run complete organization validation"""
        scripts_results = self.validate_scripts_organization()
        documents_results = self.validate_documents_organization()
        
        # Calculate overall score
        total_score = scripts_results["organization_score"] + documents_results["organization_score"]
        overall_score = total_score / 2
        
        # Determine status
        status = "✅ Excellent"
        if overall_score < 80:
            status = "⚠️ Needs Attention"
        elif overall_score < 60:
            status = "🔄 Significant Issues"
        elif overall_score < 40:
            status = "❌ Poor Organization"
        
        results = {
            "overall_organization_score": round(overall_score, 1),
            "status": status,
            "scripts_validation": scripts_results,
            "documents_validation": documents_results,
            "total_misplaced_files": len(scripts_results["misplaced_files"]) + len(documents_results["misplaced_files"]),
            "missing_directories": scripts_results["missing_directories"] + documents_results["missing_directories"],
            "validation_timestamp": "2025-11-20 05:22:00"
        }
        
        return results

if __name__ == "__main__":
    validator = OrganizationValidator()
    results = validator.run_full_organization_validation()
    
    print("\n" + "="*60)
    print("📁 ORGANIZATION VALIDATION REPORT")
    print("="*60)
    
    print(f"\n📊 Overall Score: {results['overall_organization_score']}%")
    print(f"📋 Status: {results['status']}")
    
    # Scripts validation
    scripts = results["scripts_validation"]
    print(f"\n📜 Scripts Organization: {scripts['organization_score']}%")
    if scripts["misplaced_files"]:
        print("  🔄 Misplaced Scripts:")
        for file_info in scripts["misplaced_files"]:
            print(f"     • {file_info['file']} → should be in {file_info['recommended_location']}")
    
    # Documents validation  
    docs = results["documents_validation"]
    print(f"\n📄 Documents Organization: {docs['organization_score']}%")
    if docs["misplaced_files"]:
        print("  🔄 Misplaced Documents:")
        for file_info in docs["misplaced_files"]:
            print(f"     • {file_info['file']} → should be in {file_info['recommended_location']}")
    
    # Missing directories
    if results["missing_directories"]:
        print(f"\n📁 Missing Directories:")
        for dir_info in results["missing_directories"]:
            print(f"     • {dir_info}")
    
    # Recommendations
    all_recommendations = scripts["recommendations"] + docs["recommendations"]
    if all_recommendations:
        print(f"\n💡 Recommendations:")
        for rec in set(all_recommendations):  # Remove duplicates
            print(f"     • {rec}")
    
    print(f"\n⏰ Validation Time: {results['validation_timestamp']}")
    
    # Save detailed results
    with open("organization_validation_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed report saved: organization_validation_report.json")
    
    if results["overall_organization_score"] < 80:
        print(f"\n🚨 WARNING: Organization score below 80% threshold!")
        print(f"🔧 REMEDIATION REQUIRED: Address misplacement issues")
        exit(1)
    else:
        print(f"\n✅ ORGANIZATION COMPLIANT: Workspace properly organized")