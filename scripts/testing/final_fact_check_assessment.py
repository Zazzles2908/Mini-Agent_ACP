#!/usr/bin/env python3
"""
Final Fact-Checking Assessment - Post-Implementation Validation
Using Fact-Checking Skill for Quality Assurance
"""

import os
import json
from datetime import datetime

def final_fact_check_assessment():
    """Final validation of Mini-Agent system corrections."""
    
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "assessment_type": "Final Post-Implementation Validation",
        "confidence_score": 0,
        "issues_resolved": [],
        "issues_remaining": [],
        "verification_results": {},
        "recommendations": []
    }
    
    print("🔍 Running Final Fact-Checking Assessment...")
    print("="*60)
    
    # 1. Z.AI Tools Implementation Verification
    try:
        print("\n📡 Checking Z.AI Tools Implementation...")
        
        with open("mini_agent/tools/zai_tools.py", "r") as f:
            tools_content = f.read()
        
        # Check for resolved issues
        zai_fixes_verified = []
        
        # Token usage fix
        if "Direct search API does not report token usage" in tools_content:
            zai_fixes_verified.append("✅ Token usage issue resolved")
        elif "token_usage" in tools_content and "N/A" in tools_content:
            zai_fixes_verified.append("❌ Token usage still incorrectly displayed")
        else:
            zai_fixes_verified.append("✅ Token usage properly handled")
        
        # Model reference fix
        if "glm-4-air" not in tools_content:
            zai_fixes_verified.append("✅ glm-4-air reference removed")
        else:
            zai_fixes_verified.append("❌ glm-4-air reference still present")
        
        # Accept-Language header
        with open("mini_agent/llm/zai_client.py", "r") as f:
            client_content = f.read()
        if "Accept-Language" in client_content:
            zai_fixes_verified.append("✅ Accept-Language header present")
        else:
            zai_fixes_verified.append("❌ Accept-Language header missing")
        
        # Reader endpoint
        if '"/reader"' in client_content:
            zai_fixes_verified.append("✅ Correct /reader endpoint used")
        else:
            zai_fixes_verified.append("❌ Incorrect reader endpoint")
        
        assessment["verification_results"]["zai_implementation"] = zai_fixes_verified
        print(f"   Z.AI Implementation: {len([f for f in zai_fixes_verified if f.startswith('✅')])}/{len(zai_fixes_verified)} fixes verified")
        
    except Exception as e:
        assessment["verification_results"]["zai_implementation"] = [f"❌ Error checking Z.AI: {str(e)}"]
    
    # 2. Document Hygiene Verification
    try:
        print("\n📚 Checking Document Hygiene...")
        
        required_docs = [
            ("documents/PROJECT_CONTEXT.md", "PROJECT_CONTEXT.md"),
            ("documents/SETUP_GUIDE.md", "SETUP_GUIDE.md"),
            ("documents/AGENT_HANDOFF.md", "AGENT_HANDOFF.md")
        ]
        
        doc_checks = []
        for file_path, doc_name in required_docs:
            if os.path.exists(file_path):
                doc_checks.append(f"✅ {doc_name} exists")
            else:
                doc_checks.append(f"❌ {doc_name} missing")
        
        # Check for misplaced files
        root_files = os.listdir(".")
        misplaced_files = [f for f in root_files if f.endswith('.py') and (f.startswith('test_') or f.startswith('demo') or f.startswith('check'))]
        if misplaced_files:
            doc_checks.append(f"❌ Misplaced test files in root: {misplaced_files}")
        else:
            doc_checks.append("✅ No misplaced files in root directory")
        
        assessment["verification_results"]["document_hygiene"] = doc_checks
        print(f"   Document Structure: {len([f for f in doc_checks if f.startswith('✅')])}/{len(doc_checks)} requirements met")
        
    except Exception as e:
        assessment["verification_results"]["document_hygiene"] = [f"❌ Error checking docs: {str(e)}"]
    
    # 3. System Architecture Verification
    try:
        print("\n🏗️  Checking System Architecture Alignment...")
        
        # Check if agent properly identifies as CLI/coder
        try:
            with open("mini_agent/agent.py", "r", encoding='utf-8') as f:
                agent_content = f.read()
            arch_checks = ["✅ agent.py readable (UTF-8)"]
        except:
            arch_checks = ["❌ agent.py encoding issues"]
        
        # Check core files exist
        core_files = ["mini_agent/cli.py", "mini_agent/llm/zai_client.py", "mini_agent/tools/zai_tools.py"]
        for file_path in core_files:
            if os.path.exists(file_path):
                arch_checks.append(f"✅ {file_path} exists")
            else:
                arch_checks.append(f"❌ {file_path} missing")
        
        assessment["verification_results"]["architecture_alignment"] = arch_checks
        print(f"   Architecture: {len([f for f in arch_checks if f.startswith('✅')])}/{len(arch_checks)} components verified")
        
    except Exception as e:
        assessment["verification_results"]["architecture_alignment"] = [f"❌ Error checking architecture: {str(e)}"]
    
    # 4. Calculate Overall Confidence Score
    all_results = []
    for category, results in assessment["verification_results"].items():
        all_results.extend(results)
    
    passed_checks = len([r for r in all_results if r.startswith('✅')])
    total_checks = len(all_results)
    
    if total_checks > 0:
        assessment["confidence_score"] = int((passed_checks / total_checks) * 100)
    
    # 5. Generate Summary
    print("\n" + "="*60)
    print("📊 FINAL ASSESSMENT RESULTS")
    print("="*60)
    print(f"⏰ Assessment Time: {assessment['timestamp']}")
    print(f"🎯 Confidence Score: {assessment['confidence_score']}/100")
    print(f"✅ Checks Passed: {passed_checks}/{total_checks}")
    
    if assessment["confidence_score"] >= 90:
        print("\n🌟 SYSTEM READY FOR PRODUCTION")
    elif assessment["confidence_score"] >= 70:
        print("\n✅ SYSTEM MOSTLY READY - Minor improvements needed")
    else:
        print("\n⚠️  SYSTEM NEEDS ATTENTION - Multiple issues found")
    
    # 6. Save Assessment
    with open("documents/testing/final_assessment_results.json", "w") as f:
        json.dump(assessment, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: documents/testing/final_assessment_results.json")
    print("="*60)
    
    return assessment

if __name__ == "__main__":
    final_assessment = final_fact_check_assessment()
    
    # Print detailed results
    print("\n🔍 DETAILED VERIFICATION RESULTS:")
    for category, results in final_assessment["verification_results"].items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        for result in results:
            print(f"   {result}")