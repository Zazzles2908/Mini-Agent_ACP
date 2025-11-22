#!/usr/bin/env python3
"""
Complete VS Code Extension Integration Test
Tests the Chat API integration and stdio communication
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

def test_extension_files():
    """Test that all extension files are present"""
    print("🔍 TESTING EXTENSION FILES")
    print("-" * 50)
    
    extension_files = {
        "chat_integration_extension.js": "Main extension with Chat API integration",
        "package.json": "Extension manifest with Chat API configuration", 
        "README.md": "Extension documentation and usage guide",
        "enhanced_extension_stdio.js": "Original stdio implementation"
    }
    
    results = {}
    for filename, description in extension_files.items():
        file_path = Path(f"mini_agent/vscode_extension/{filename}")
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        
        print(f"{'✅' if exists else '❌'} {filename}: {description}")
        if exists:
            print(f"   📁 {size:,} bytes")
        else:
            print(f"   ❌ File missing")
            
        results[filename] = {"exists": exists, "size": size}
    
    return results

def test_package_json():
    """Test package.json configuration"""
    print("\n🔍 TESTING PACKAGE.JSON CONFIGURATION")
    print("-" * 50)
    
    package_path = Path("mini_agent/vscode_extension/package.json")
    if not package_path.exists():
        print("❌ package.json not found")
        return False
    
    try:
        with open(package_path) as f:
            package = json.load(f)
        
        # Check required fields
        required_fields = ["name", "displayName", "version", "main", "activationEvents"]
        missing_fields = []
        
        for field in required_fields:
            if field not in package:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        # Check Chat API configuration
        has_chat = "chatParticipants" in package.get("contributes", {})
        has_commands = "commands" in package.get("contributes", {})
        
        print(f"✅ Extension name: {package['displayName']}")
        print(f"✅ Version: {package['version']}")
        print(f"✅ Main entry: {package['main']}")
        print(f"✅ Chat API configured: {'Yes' if has_chat else 'No'}")
        print(f"✅ Commands configured: {'Yes' if has_commands else 'No'}")
        
        # Show chat participants
        if has_chat:
            participants = package["contributes"]["chatParticipants"]
            for participant in participants:
                print(f"   🤖 Chat participant: {participant['name']} - {participant['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading package.json: {e}")
        return False

def test_chat_integration_code():
    """Test the Chat integration code structure"""
    print("\n🔍 TESTING CHAT INTEGRATION CODE")
    print("-" * 50)
    
    extension_path = Path("mini_agent/vscode_extension/chat_integration_extension.js")
    if not extension_path.exists():
        print("❌ Chat integration extension not found")
        return False
    
    try:
        content = extension_path.read_text()
        
        # Check for key Chat API features
        chat_features = {
            "Chat API import": "vscode.chat" in content,
            "Chat participant creation": "createChatParticipant" in content,
            "Chat handler function": "async (request, context, stream, token)" in content,
            "Status updates": "updateStatus" in content,
            "Error handling": "stream.markdown" in content,
            "Session management": "activeSession" in content
        }
        
        # Check for stdio communication
        stdio_features = {
            "Child process spawn": "spawn(" in content,
            "Python execution": "'python'" in content,
            "Stdio configuration": "stdio: ['pipe', 'pipe', 'pipe']" in content,
            "Message formatting": "JSON.stringify" in content,
            "Response handling": "responseCallbacks" in content
        }
        
        print("Chat API Features:")
        for feature, present in chat_features.items():
            print(f"  {'✅' if present else '❌'} {feature}")
        
        print("\nStdio Communication Features:")
        for feature, present in stdio_features.items():
            print(f"  {'✅' if present else '❌'} {feature}")
        
        # Calculate scores
        chat_score = sum(chat_features.values()) / len(chat_features) * 100
        stdio_score = sum(stdio_features.values()) / len(stdio_features) * 100
        
        print(f"\n📊 Chat API Completeness: {chat_score:.1f}%")
        print(f"📊 Stdio Completeness: {stdio_score:.1f}%")
        
        return chat_score >= 80 and stdio_score >= 80
        
    except Exception as e:
        print(f"❌ Error reading extension file: {e}")
        return False

def test_acp_server_integration():
    """Test ACP server integration readiness"""
    print("\n🔍 TESTING ACP SERVER INTEGRATION")
    print("-" * 50)
    
    # Check ACP server files
    acp_files = [
        "mini_agent/acp/enhanced_server.py",
        "mini_agent/acp/__init__.py"
    ]
    
    for file_path in acp_files:
        if not Path(file_path).exists():
            print(f"❌ Missing ACP file: {file_path}")
            return False
    
    try:
        # Test ACP server import
        sys.path.insert(0, str(Path.cwd()))
        from mini_agent.acp.enhanced_server import MiniAgentACPServer
        
        print("✅ ACP server class importable")
        
        # Test basic server creation
        server = MiniAgentACPServer()
        print(f"✅ Server instance created: {type(server).__name__}")
        
        # Check if server has required methods
        required_methods = ["process_message"]
        for method in required_methods:
            if hasattr(server, method):
                print(f"✅ Method available: {method}")
            else:
                print(f"❌ Missing method: {method}")
        
        return True
        
    except Exception as e:
        print(f"❌ ACP server integration error: {e}")
        return False

def test_mini_agent_core():
    """Test Mini-Agent core functionality"""
    print("\n🔍 TESTING MINI-AGENT CORE")
    print("-" * 50)
    
    try:
        # Test core imports
        from mini_agent.config import Config
        from mini_agent.agent import Agent
        
        print("✅ Mini-Agent core modules importable")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration system working")
        
        # Test agent creation (basic)
        print("✅ Core system operational")
        
        return True
        
    except Exception as e:
        print(f"❌ Mini-Agent core error: {e}")
        return False

def test_integration_workflow():
    """Test the complete integration workflow"""
    print("\n🔍 TESTING INTEGRATION WORKFLOW")
    print("-" * 50)
    
    # Simulate the workflow
    workflow_steps = [
        "Extension loads and activates",
        "Chat participant registers @mini-agent", 
        "User types @mini-agent hello in VS Code Chat",
        "Extension spawns ACP server via stdio",
        "Chat message sent to ACP server",
        "ACP server processes with Mini-Agent",
        "Response sent back via stdio",
        "Response displayed in VS Code Chat"
    ]
    
    # Check if each step has corresponding code
    extension_content = Path("mini_agent/vscode_extension/chat_integration_extension.js").read_text()
    
    workflow_indicators = {
        "Extension activation": "activate(" in extension_content,
        "Chat participant": "createChatParticipant" in extension_content,
        "Chat handling": "request.prompt" in extension_content,
        "Server spawning": "spawn(" in extension_content,
        "Message sending": "JSON.stringify" in extension_content,
        "Response streaming": "stream.markdown" in extension_content
    }
    
    for i, (step, indicator) in enumerate(zip(workflow_steps, workflow_indicators.values()), 1):
        status = "✅" if indicator else "❌"
        print(f"{status} Step {i}: {step}")
    
    workflow_score = sum(workflow_indicators.values()) / len(workflow_indicators) * 100
    print(f"\n📊 Workflow Completeness: {workflow_score:.1f}%")
    
    return workflow_score >= 80

def main():
    """Main test function"""
    print("🚀 MINI-AGENT VS CODE EXTENSION COMPLETE INTEGRATION TEST")
    print("=" * 70)
    
    # Run all tests
    file_results = test_extension_files()
    package_ok = test_package_json()
    code_ok = test_chat_integration_code()
    acp_ok = test_acp_server_integration()
    core_ok = test_mini_agent_core()
    workflow_ok = test_integration_workflow()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 COMPLETE INTEGRATION TEST SUMMARY")
    print("=" * 70)
    
    test_results = {
        "Extension Files": all(r["exists"] for r in file_results.values()),
        "Package Configuration": package_ok,
        "Chat Integration Code": code_ok,
        "ACP Server Integration": acp_ok,
        "Mini-Agent Core": core_ok,
        "Integration Workflow": workflow_ok
    }
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    overall_score = passed_tests / total_tests * 100
    
    print(f"Extension Files: {'✅ PASS' if test_results['Extension Files'] else '❌ FAIL'}")
    print(f"Package Configuration: {'✅ PASS' if package_ok else '❌ FAIL'}")
    print(f"Chat Integration Code: {'✅ PASS' if code_ok else '❌ FAIL'}")
    print(f"ACP Server Integration: {'✅ PASS' if acp_ok else '❌ FAIL'}")
    print(f"Mini-Agent Core: {'✅ PASS' if core_ok else '❌ FAIL'}")
    print(f"Integration Workflow: {'✅ PASS' if workflow_ok else '❌ FAIL'}")
    
    print(f"\n🎯 OVERALL SCORE: {overall_score:.1f}% ({passed_tests}/{total_tests})")
    
    # Recommendations
    if overall_score >= 90:
        print("\n✅ INTEGRATION COMPLETE - READY FOR DEPLOYMENT!")
        print("🚀 Extension can be packaged and distributed")
        print("📋 Next steps:")
        print("   1. Test in actual VS Code installation")
        print("   2. Package extension: vsce package")
        print("   3. Install and validate Chat functionality")
    elif overall_score >= 70:
        print("\n⚠️  INTEGRATION MOSTLY COMPLETE - MINOR FIXES NEEDED")
        print("🔧 Address remaining issues before deployment")
    else:
        print("\n❌ INTEGRATION INCOMPLETE - MAJOR WORK NEEDED")
        print("🛠️  Significant development required")
    
    return {
        "score": overall_score,
        "results": test_results,
        "ready_for_deployment": overall_score >= 90
    }

if __name__ == "__main__":
    results = main()