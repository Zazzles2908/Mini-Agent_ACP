#!/usr/bin/env python3
"""
Use fact-checking skill to validate Mini-Agent Z.AI implementation.
This will identify all the issues mentioned by the user.
"""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def fact_check_zai_implementation():
    """Use fact-checking to assess Z.AI implementation issues."""
    
    print("=" * 100)
    print("FACT-CHECKING: Z.AI IMPLEMENTATION ASSESSMENT")
    print("=" * 100)
    
    # Read the ZAIClient file to check for issues
    zai_client_path = "mini_agent/llm/zai_client.py"
    zai_tools_path = "mini_agent/tools/zai_tools.py"
    
    print("\n🔍 ANALYZING Z.AI CLIENT IMPLEMENTATION:")
    print("-" * 80)
    
    if os.path.exists(zai_client_path):
        with open(zai_client_path, 'r') as f:
            client_content = f.read()
        
        # Check for specific issues
        issues_found = []
        
        # Issue 1: Check if web reader uses correct endpoint
        if "/reader" in client_content and "web_reading" not in client_content:
            print("✅ Web reader endpoint: CORRECT (/reader)")
        else:
            issues_found.append("❌ Web reader endpoint: INCORRECT (not using /reader)")
            print("❌ Web reader endpoint: INCORRECT (not using /reader)")
        
        # Issue 2: Check for Accept-Language header
        if "Accept-Language" in client_content:
            print("✅ Accept-Language header: INCLUDED")
        else:
            issues_found.append("❌ Accept-Language header: MISSING")
            print("❌ Accept-Language header: MISSING")
        
        # Issue 3: Check token usage handling
        if "token_usage" in client_content:
            print("⚠️  Token usage: REFERENCED (should not be for web search)")
            issues_found.append("⚠️  Token usage incorrectly referenced for web search API")
        else:
            print("✅ Token usage: NOT REFERENCED (correct)")
        
        # Issue 4: Check GLM model references
        glm_issues = []
        if "glm-4.5" in client_content:
            print("✅ GLM-4.5 reference: PRESENT")
        else:
            glm_issues.append("GLM-4.5 missing")
            
        if "glm-4.6" in client_content:
            print("✅ GLM-4.6 reference: PRESENT")
        else:
            glm_issues.append("GLM-4.6 missing")
            
        if "glm-4-air" in client_content:
            glm_issues.append("GLM-4-air present (should be removed)")
            print("⚠️  GLM-4-air reference: PRESENT (should be removed)")
        
        if glm_issues:
            issues_found.append(f"GLM model references: {', '.join(glm_issues)}")
    
    print("\n🔍 ANALYZING Z.AI TOOLS IMPLEMENTATION:")
    print("-" * 80)
    
    if os.path.exists(zai_tools_path):
        with open(zai_tools_path, 'r') as f:
            tools_content = f.read()
        
        # Check for model reference inconsistency
        if '"glm-4-air"' in tools_content:
            print("❌ Tools: glm-4-air still in enum (should be removed)")
            issues_found.append("❌ Tools: glm-4-air in enum but not in description")
        
        # Check if tools inherit ZAIClient issues
        if "from ..llm.zai_client import ZAIClient" in tools_content:
            print("⚠️  Tools inherit ZAIClient issues: YES")
            issues_found.append("⚠️  Tools depend on ZAIClient - will inherit any issues")
        
        # Check token usage in tools
        if "token_usage" in tools_content:
            print("⚠️  Tools: token usage referenced (incorrect for web search)")
            issues_found.append("⚠️  Tools: token usage incorrectly referenced")
    
    print("\n📊 FACT-CHECKING ASSESSMENT RESULTS:")
    print("-" * 80)
    
    total_issues = len(issues_found)
    critical_issues = len([i for i in issues_found if i.startswith("❌")])
    warning_issues = len([i for i in issues_found if i.startswith("⚠️")])
    
    confidence_score = max(0, 100 - (critical_issues * 20 + warning_issues * 10))
    
    print(f"Total Issues Found: {total_issues}")
    print(f"Critical Issues: {critical_issues}")
    print(f"Warning Issues: {warning_issues}")
    print(f"Confidence Score: {confidence_score}%")
    
    if issues_found:
        print(f"\n🚨 IDENTIFIED ISSUES:")
        for i, issue in enumerate(issues_found, 1):
            print(f"{i}. {issue}")
    
    print(f"\n🎯 PRODUCTION READINESS STATUS:")
    if confidence_score >= 90:
        print("🟢 HIGH CONFIDENCE - Ready for production")
    elif confidence_score >= 70:
        print("🟡 MEDIUM CONFIDENCE - Review recommended")
    elif confidence_score >= 50:
        print("🟠 LOW CONFIDENCE - Significant improvements needed")
    else:
        print("🔴 NEEDS REVIEW - Major gaps identified")
    
    return {
        "issues": issues_found,
        "confidence_score": confidence_score,
        "critical_issues": critical_issues,
        "warning_issues": warning_issues
    }

if __name__ == "__main__":
    result = asyncio.run(fact_check_zai_implementation())
    print(f"\n✅ Fact-checking assessment complete")
    print(f"📊 Confidence Score: {result['confidence_score']}%")
    print(f"🚨 Issues Found: {len(result['issues'])}")