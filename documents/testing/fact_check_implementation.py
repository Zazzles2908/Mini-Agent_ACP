#!/usr/bin/env python3
"""Fact-checking assessment of Mini-Agent current implementation."""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool

async def fact_check_mini_agent_implementation():
    """Perform comprehensive fact-checking assessment of Mini-Agent current state."""
    
    print("=" * 80)
    print("MINI-AGENT IMPLEMENTATION FACT-CHECKING ASSESSMENT")
    print("=" * 80)
    
    assessment_results = []
    issues_found = []
    
    # 1. System Architecture Verification
    print("\n1. SYSTEM ARCHITECTURE ASSESSMENT")
    print("-" * 50)
    
    core_files = [
        "mini_agent/agent.py",
        "mini_agent/cli.py", 
        "mini_agent/llm/zai_client.py",
        "mini_agent/tools/zai_tools.py",
        "mini_agent/acp/enhanced_server.py",
        "mini_agent/skills/fact-checking-self-assessment/SKILL.md"
    ]
    
    for file_path in core_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            assessment_results.append(f"✅ {file_path} exists ({size} bytes)")
        else:
            issues_found.append(f"❌ Missing core file: {file_path}")
            assessment_results.append(f"❌ {file_path} missing")
    
    # 2. Z.AI Integration Assessment
    print("\n2. Z.AI INTEGRATION ASSESSMENT")
    print("-" * 50)
    
    try:
        search_tool = ZAIWebSearchTool()
        if search_tool.available:
            result = await search_tool.execute(
                query="Mini-Agent system architecture current status",
                depth="quick"
            )
            if result.success:
                assessment_results.append("✅ Z.AI web search functional")
                print(f"✅ Web search test passed - content length: {len(result.content)}")
            else:
                issues_found.append(f"❌ Z.AI web search failed: {result.error}")
                assessment_results.append("❌ Z.AI web search not functional")
        else:
            issues_found.append("❌ Z.AI web search tool not available")
    except Exception as e:
        issues_found.append(f"❌ Z.AI search tool error: {e}")
    
    try:
        reader_tool = ZAIWebReaderTool()
        if reader_tool.available:
            result = await reader_tool.execute(
                url="https://httpbin.org/json",
                format="markdown"
            )
            if result.success:
                assessment_results.append("✅ Z.AI web reader functional")
                print(f"✅ Web reader test passed - content length: {len(result.content)}")
            else:
                issues_found.append(f"❌ Z.AI web reader failed: {result.error}")
                assessment_results.append("❌ Z.AI web reader not functional")
        else:
            issues_found.append("❌ Z.AI web reader tool not available")
    except Exception as e:
        issues_found.append(f"❌ Z.AI reader tool error: {e}")
    
    # 3. System Organization Assessment
    print("\n3. SYSTEM ORGANIZATION ASSESSMENT")
    print("-" * 50)
    
    # Check for proper documentation structure
    doc_files = [
        "documents/AGENT_HANDOFF.md",
        "documents/README.md",
        "documents/SYSTEM_STATUS.md",
        "documents/ZAI_DIRECT_API_IMPLEMENTATION.md"
    ]
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            size = os.path.getsize(doc_file)
            assessment_results.append(f"✅ Documentation exists: {doc_file} ({size} bytes)")
        else:
            issues_found.append(f"❌ Missing documentation: {doc_file}")
            assessment_results.append(f"❌ Missing: {doc_file}")
    
    # 4. Environment Assessment
    print("\n4. ENVIRONMENT ASSESSMENT")
    print("-" * 50)
    
    env_check = {
        "ZAI_API_KEY": bool(os.getenv("ZAI_API_KEY")),
        ".env exists": os.path.exists(".env"),
        ".venv exists": os.path.exists(".venv"),
        "requirements.txt exists": os.path.exists("requirements.txt")
    }
    
    for env_var, status in env_check.items():
        if status:
            assessment_results.append(f"✅ {env_var} configured")
        else:
            issues_found.append(f"❌ {env_var} not configured")
            assessment_results.append(f"❌ {env_var} missing")
    
    # 5. Generate Summary Report
    print("\n" + "=" * 80)
    print("FACT-CHECKING ASSESSMENT SUMMARY")
    print("=" * 80)
    
    total_items = len(assessment_results)
    passed_items = len([item for item in assessment_results if "✅" in item])
    failed_items = len([item for item in assessment_results if "❌" in item])
    
    confidence_score = (passed_items / total_items * 100) if total_items > 0 else 0
    
    print(f"Overall Confidence Score: {confidence_score:.1f}%")
    print(f"Total Items Assessed: {total_items}")
    print(f"Passed: {passed_items}")
    print(f"Failed: {failed_items}")
    
    if issues_found:
        print(f"\nCRITICAL ISSUES IDENTIFIED ({len(issues_found)}):")
        for i, issue in enumerate(issues_found, 1):
            print(f"{i}. {issue}")
    
    print(f"\nIMPLEMENTATION STATUS:")
    if confidence_score >= 90:
        print("🟢 HIGH CONFIDENCE - Production Ready")
    elif confidence_score >= 70:
        print("🟡 MEDIUM CONFIDENCE - Review Recommended")
    elif confidence_score >= 50:
        print("🟠 LOW CONFIDENCE - Significant Improvements Needed")
    else:
        print("🔴 NEEDS REVIEW - Major Gaps Identified")
    
    return {
        "confidence_score": confidence_score,
        "total_items": total_items,
        "passed_items": passed_items,
        "failed_items": failed_items,
        "issues": issues_found,
        "results": assessment_results
    }

if __name__ == "__main__":
    asyncio.run(fact_check_mini_agent_implementation())