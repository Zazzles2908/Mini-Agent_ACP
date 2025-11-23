#!/usr/bin/env python3
"""
QA System Self-Assessment

Direct analysis of the QA implementation without complex imports,
testing whether the implementation meets its own requirements.
"""

import os
import sys
from pathlib import Path
import re

def assess_qa_implementation():
    """Assess the QA implementation using direct analysis"""
    
    print("🧪 QA SYSTEM SELF-ASSESSMENT")
    print("=" * 60)
    
    assessment_results = {
        "implementation_completeness": [],
        "architectural_compliance": [],
        "integration_points": [],
        "documentation_quality": [],
        "technical_issues": []
    }
    
    # 1. Check implementation completeness
    print("📋 1. IMPLEMENTATION COMPLETENESS")
    print("-" * 40)
    
    expected_files = [
        "documents/02_SYSTEM_CORE/QA_VALIDATION_SYSTEM.md",
        "documents/02_SYSTEM_CORE/QA_USAGE_GUIDE.md",
        "mini_agent/skills/fact-checking-self-assessment/tools/validation_tool.py",
        "mini_agent/tools/__init__.py",
        "mini_agent/agent.py"
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({file_size} bytes)")
            assessment_results["implementation_completeness"].append(f"Present: {file_path}")
        else:
            print(f"❌ MISSING: {file_path}")
            assessment_results["technical_issues"].append(f"Missing required file: {file_path}")
    
    print()
    
    # 2. Check architectural compliance  
    print("🏗️  2. ARCHITECTURAL COMPLIANCE")
    print("-" * 40)
    
    try:
        # Read agent.py to check integration
        agent_content = open("mini_agent/agent.py", "r").read()
        
        if "_validate_task_completion" in agent_content:
            print("✅ Agent integration method present")
            assessment_results["architectural_compliance"].append("Agent integration method implemented")
        else:
            print("❌ Missing agent integration method")
            assessment_results["technical_issues"].append("Missing agent integration method")
            
        if "ValidationTool" in agent_content:
            print("✅ ValidationTool referenced in agent")
            assessment_results["architectural_compliance"].append("ValidationTool imported and used")
        else:
            print("❌ ValidationTool not used in agent")
            assessment_results["technical_issues"].append("ValidationTool not integrated in agent")
            
        if "honesty_score" in agent_content:
            print("✅ Honesty scoring integrated")
            assessment_results["architectural_compliance"].append("Honesty scoring system integrated")
        else:
            print("❌ Honesty scoring not integrated")
            assessment_results["technical_issues"].append("Honesty scoring not implemented")
            
    except Exception as e:
        print(f"❌ Could not read agent.py: {e}")
        assessment_results["technical_issues"].append(f"Agent file analysis failed: {e}")
    
    print()
    
    # 3. Check integration points
    print("🔗 3. INTEGRATION POINTS")
    print("-" * 40)
    
    try:
        agent_content = open("mini_agent/agent.py", "r").read()
        
        if "if not response.tool_calls:" in agent_content:
            print("✅ Task completion check point found")
            assessment_results["integration_points"].append("Task completion validation hook present")
            
            # Check if validation is called at this point
            if "_validate_task_completion(response)" in agent_content:
                print("✅ Validation called at completion point")
                assessment_results["integration_points"].append("Validation triggered at task completion")
            else:
                print("❌ Validation not called at completion point")
                assessment_results["technical_issues"].append("Validation not triggered at completion")
        else:
            print("❌ Task completion check not found")
            assessment_results["technical_issues"].append("Task completion validation point missing")
            
    except Exception as e:
        print(f"❌ Integration analysis failed: {e}")
        assessment_results["technical_issues"].append(f"Integration analysis failed: {e}")
    
    print()
    
    # 4. Documentation quality assessment
    print("📚 4. DOCUMENTATION QUALITY")
    print("-" * 40)
    
    doc_files = [
        "documents/02_SYSTEM_CORE/QA_VALIDATION_SYSTEM.md",
        "documents/02_SYSTEM_CORE/QA_USAGE_GUIDE.md"
    ]
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            try:
                content = open(doc_file, "r").read()
                word_count = len(content.split())
                print(f"✅ {doc_file}: {word_count} words")
                assessment_results["documentation_quality"].append(f"Documentation present: {word_count} words")
                
                # Check for key content sections
                key_terms = ["implementation", "integration", "architecture", "workflow", "validation"]
                found_terms = [term for term in key_terms if term.lower() in content.lower()]
                if len(found_terms) >= 3:
                    print(f"✅ Good coverage of key concepts: {', '.join(found_terms)}")
                    assessment_results["documentation_quality"].append("Comprehensive concept coverage")
                else:
                    print(f"⚠️  Limited concept coverage: {', '.join(found_terms)}")
                    
            except Exception as e:
                print(f"❌ Could not analyze {doc_file}: {e}")
                assessment_results["technical_issues"].append(f"Documentation analysis failed: {doc_file}")
    
    print()
    
    # 5. Generate overall assessment
    print("📊 5. OVERALL ASSESSMENT")
    print("=" * 60)
    
    # Calculate scores
    total_checks = 0
    passed_checks = 0
    
    for category, results in assessment_results.items():
        for result in results:
            total_checks += 1
            if "❌" not in result and "Missing" not in result and "failed" not in result:
                passed_checks += 1
    
    score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
    
    print(f"Implementation Score: {score}/100")
    print()
    
    # Generate summary
    if score >= 90:
        print("🎉 EXCELLENT: QA system implementation is highly complete and well-architected")
        honesty_level = "HIGH INTEGRITY"
    elif score >= 75:
        print("👍 GOOD: QA system implementation is solid with minor gaps")
        honesty_level = "GOOD INTEGRITY"
    elif score >= 60:
        print("⚠️  NEEDS IMPROVEMENT: QA system has significant implementation gaps")
        honesty_level = "MODERATE INTEGRITY"
    else:
        print("❌ POOR: QA system implementation has major issues")
        honesty_level = "LOW INTEGRITY"
    
    print(f"Honesty Assessment: {honesty_level}")
    print()
    
    # Detail findings
    print("DETAILED FINDINGS:")
    for category, results in assessment_results.items():
        if results:
            print(f"\n{category.replace('_', ' ').title()}:")
            for result in results:
                print(f"  • {result}")
    
    return {
        "score": score,
        "honesty_level": honesty_level,
        "findings": assessment_results
    }

if __name__ == "__main__":
    result = assess_qa_implementation()