#!/usr/bin/env python3
"""
Comprehensive Mini-Agent System Architecture Assessment
Using Fact-Checking Skill for Production Readiness Validation
"""

import os
import json
from pathlib import Path
from datetime import datetime

def assess_mini_agent_architecture():
    """Comprehensive assessment of Mini-Agent system architecture."""
    
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "system": "Mini-Agent Platform",
        "scope": "Complete Architecture Validation",
        "components": {},
        "issues": [],
        "recommendations": [],
        "confidence_score": 0
    }
    
    # Core Component Files to Check
    core_files = {
        "mini_agent/agent.py": "Core Agent implementation",
        "mini_agent/cli.py": "Command line interface", 
        "mini_agent/llm/zai_client.py": "Z.AI Direct API client",
        "mini_agent/tools/zai_tools.py": "Z.AI web search and reading tools",
        "mini_agent/skills/fact-checking-self-assessment/SKILL.md": "Fact-checking skill documentation",
        "mini_agent/acp/enhanced_server.py": "Enhanced ACP server protocol"
    }
    
    # Architecture Components to Validate
    architecture_components = {
        "core_platform": {
            "files": ["agent.py", "cli.py"],
            "expected_behavior": "CLI/coder tool with protocol support"
        },
        "zai_integration": {
            "files": ["zai_client.py", "zai_tools.py"], 
            "expected_behavior": "Direct REST API with web search/reading"
        },
        "skill_system": {
            "files": ["skills/"],
            "expected_behavior": "Modular skill loading with progressive disclosure"
        },
        "protocol_implementation": {
            "files": ["acp/enhanced_server.py"],
            "expected_behavior": "Agent Client Protocol server with WebSocket communication"
        },
        "document_organization": {
            "files": ["documents/"],
            "expected_behavior": "Structured documentation following established patterns"
        }
    }
    
    # Z.AI Specific Issues to Check
    zai_issues = {
        "web_reader_endpoint": "Using correct /reader endpoint vs /web_reading",
        "model_selection": "Proper GLM-4.5, GLM-4.6 model references vs glm-4-air",
        "token_usage": "Web search API doesn't report token usage",
        "headers": "Accept-Language header inclusion",
        "tool_inheritance": "Tools properly inheriting from fixed ZAIClient"
    }
    
    # Document Hygiene Standards
    document_standards = {
        "AGENT_HANDOFF.md": "Transfer notes for next agent",
        "PROJECT_CONTEXT.md": "Project overview and goals",
        "SETUP_GUIDE.md": "Environment setup and dependencies", 
        "SYSTEM_ARCHITECTURE_CURRENT.md": "Current system design",
        "testing/": "Test files organized in documents/testing/"
    }
    
    # Assessment Execution
    print("🔍 Starting Comprehensive Mini-Agent System Assessment...")
    
    # 1. File Existence Validation
    missing_files = []
    for file_path, description in core_files.items():
        if not os.path.exists(file_path):
            missing_files.append(f"{file_path}: {description}")
    
    if missing_files:
        assessment["issues"].append({
            "type": "missing_files",
            "severity": "critical",
            "details": missing_files
        })
    
    # 2. Z.AI Integration Issues Assessment
    zai_issues_found = []
    try:
        # Check ZAI client implementation
        with open("mini_agent/llm/zai_client.py", "r") as f:
            zai_client_content = f.read()
        
        # Check for wrong endpoints
        if "/web_reading" in zai_client_content:
            zai_issues_found.append("Incorrect /web_reading endpoint used instead of /reader")
        
        # Check for proper model references
        if "glm-4-air" in zai_client_content:
            zai_issues_found.append("glm-4-air model reference found (should be glm-4.5/4.6)")
        
        # Check for token usage in web search
        if "token_usage" in zai_client_content:
            zai_issues_found.append("Token usage referenced in web search (not supported)")
            
    except Exception as e:
        zai_issues_found.append(f"Error reading ZAI client: {str(e)}")
    
    # Check ZAI tools wrapper
    try:
        with open("mini_agent/tools/zai_tools.py", "r") as f:
            zai_tools_content = f.read()
            
        # Check for model enum consistency
        if '"glm-4-air"' in zai_tools_content:
            zai_issues_found.append("Tools have inconsistent model references")
            
        # Check for token usage in response formatting
        if "token_usage" in zai_tools_content:
            zai_issues_found.append("Tools incorrectly reference token usage for web search")
            
    except Exception as e:
        zai_issues_found.append(f"Error reading ZAI tools: {str(e)}")
    
    if zai_issues_found:
        assessment["issues"].append({
            "type": "zai_integration",
            "severity": "critical", 
            "details": zai_issues_found
        })
    
    # 3. Document Hygiene Assessment
    document_issues = []
    try:
        # Check document structure
        if not os.path.exists("documents/"):
            document_issues.append("No documents/ directory found")
        else:
            expected_docs = ["AGENT_HANDOFF.md", "PROJECT_CONTEXT.md", "SETUP_GUIDE.md"]
            for doc in expected_docs:
                if not os.path.exists(f"documents/{doc}"):
                    document_issues.append(f"Missing required document: {doc}")
        
        # Check for misplaced files in root directory
        root_files = os.listdir(".")
        misplaced_test_files = [f for f in root_files if f.endswith('.py') and f.startswith('test_')]
        if misplaced_test_files:
            document_issues.append(f"Test files in root directory: {misplaced_test_files}")
            
    except Exception as e:
        document_issues.append(f"Error checking document structure: {str(e)}")
    
    if document_issues:
        assessment["issues"].append({
            "type": "document_hygiene", 
            "severity": "high",
            "details": document_issues
        })
    
    # 4. Architecture Alignment Assessment
    architecture_issues = []
    try:
        # Check if agent.py correctly identifies as CLI tool
        with open("mini_agent/agent.py", "r") as f:
            agent_content = f.read()
            
        # Look for proper system role definition
        if "Mini-Agent is currently being used as a CLI/coder" not in agent_content:
            architecture_issues.append("Agent not properly identified as CLI/coder tool")
            
    except Exception as e:
        architecture_issues.append(f"Error reading agent.py: {str(e)}")
    
    if architecture_issues:
        assessment["issues"].append({
            "type": "architecture_alignment",
            "severity": "medium",
            "details": architecture_issues
        })
    
    # 5. Calculate Overall Confidence Score
    total_issues = len(assessment["issues"])
    if total_issues == 0:
        assessment["confidence_score"] = 100
    elif total_issues <= 2:
        assessment["confidence_score"] = 80
    elif total_issues <= 4:
        assessment["confidence_score"] = 60
    else:
        assessment["confidence_score"] = 40
    
    # 6. Generate Recommendations
    if zai_issues_found:
        assessment["recommendations"].append({
            "priority": "critical",
            "action": "Fix Z.AI integration issues",
            "details": [
                "Replace /web_reading endpoint with /reader",
                "Remove glm-4-air references", 
                "Fix token usage references in web search",
                "Ensure Accept-Language header inclusion"
            ]
        })
    
    if document_issues:
        assessment["recommendations"].append({
            "priority": "high",
            "action": "Improve document hygiene",
            "details": document_issues
        })
    
    if architecture_issues:
        assessment["recommendations"].append({
            "priority": "medium", 
            "action": "Align architecture documentation",
            "details": architecture_issues
        })
    
    return assessment

def print_assessment_report(assessment):
    """Print formatted assessment report."""
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE MINI-AGENT SYSTEM ASSESSMENT REPORT")
    print("="*80)
    
    print(f"\n⏰ Assessment Timestamp: {assessment['timestamp']}")
    print(f"🎯 Confidence Score: {assessment['confidence_score']}/100")
    
    if assessment['issues']:
        print(f"\n❌ Issues Found: {len(assessment['issues'])}")
        for i, issue in enumerate(assessment['issues'], 1):
            print(f"\n{i}. {issue['type'].upper()} (Severity: {issue['severity']})")
            for detail in issue['details']:
                print(f"   • {detail}")
    else:
        print("\n✅ No critical issues found!")
    
    if assessment['recommendations']:
        print(f"\n💡 Recommendations: {len(assessment['recommendations'])}")
        for i, rec in enumerate(assessment['recommendations'], 1):
            print(f"\n{i}. {rec['action']} (Priority: {rec['priority']})")
            for detail in rec['details']:
                print(f"   • {detail}")
    
    print("\n" + "="*80)
    print("Assessment completed successfully")
    print("="*80)

if __name__ == "__main__":
    # Run comprehensive assessment
    assessment_results = assess_mini_agent_architecture()
    print_assessment_report(assessment_results)
    
    # Save results for further analysis
    with open("documents/testing/comprehensive_assessment_results.json", "w") as f:
        json.dump(assessment_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: documents/testing/comprehensive_assessment_results.json")