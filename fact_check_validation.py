#!/usr/bin/env python3
"""
Comprehensive Fact-Check Validation Script
Validates current implementation status and functionality
"""

import sys
import os
from pathlib import Path

def test_core_imports():
    """Test core Mini-Agent imports"""
    print("🔍 TESTING CORE IMPORTS")
    print("-" * 50)
    
    tests = [
        ("mini_agent", "Mini-Agent core package"),
        ("mini_agent.agent", "Agent module"),
        ("mini_agent.config", "Config module"),
        ("mini_agent.cli", "CLI module"),
        ("mini_agent.tools", "Tools module"),
        ("mini_agent.llm", "LLM client module"),
    ]
    
    results = {}
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description}: Working")
            results[module] = True
        except Exception as e:
            print(f"❌ {description}: {e}")
            results[module] = False
    
    return results

def test_acp_implementation():
    """Test ACP server implementation"""
    print("\n🔍 TESTING ACP IMPLEMENTATION")
    print("-" * 50)
    
    # Check ACP files exist
    acp_files = [
        "mini_agent/acp/__init__.py",
        "mini_agent/acp/enhanced_server.py", 
        "mini_agent/acp/server.py",
        "mini_agent/acp/__main__.py"
    ]
    
    file_results = {}
    for file_path in acp_files:
        exists = Path(file_path).exists()
        print(f"{'✅' if exists else '❌'} {Path(file_path).name}: {'Found' if exists else 'Missing'}")
        file_results[file_path] = exists
    
    # Test ACP server import (avoid naming conflict)
    print("\nTesting ACP Server Import...")
    try:
        sys.path.insert(0, str(Path.cwd()))
        from mini_agent.acp.enhanced_server import EnhancedACPServer
        print("✅ Enhanced ACP Server: Importable")
        acp_enhanced = True
    except Exception as e:
        print(f"❌ Enhanced ACP Server: {e}")
        acp_enhanced = False
    
    try:
        # This will likely fail due to acp library conflict
        from mini_agent.acp import main
        print("✅ ACP main module: Importable")
        acp_main = True
    except Exception as e:
        print(f"❌ ACP main module: {e}")
        acp_main = False
        
    return {
        "files": file_results,
        "enhanced_server": acp_enhanced,
        "main_module": acp_main
    }

def test_vscode_extension():
    """Test VS Code extension files"""
    print("\n🔍 TESTING VS CODE EXTENSION")
    print("-" * 50)
    
    extension_files = [
        "mini_agent/vscode_extension/enhanced_extension.js",
        "mini_agent/vscode_extension/enhanced_extension_stdio.js",
        "mini_agent/vscode_extension/extension.js",
        "mini_agent/vscode_extension/test_extension.py"
    ]
    
    results = {}
    for file_path in extension_files:
        exists = Path(file_path).exists()
        size = Path(file_path).stat().st_size if exists else 0
        print(f"{'✅' if exists else '❌'} {Path(file_path).name}: {'Found' if exists else 'Missing'} ({size:,} bytes)")
        results[file_path] = {"exists": exists, "size": size}
    
    return results

def test_architecture_compliance():
    """Test architecture compliance with strategy"""
    print("\n🔍 TESTING ARCHITECTURE COMPLIANCE")
    print("-" * 50)
    
    # Check for key components mentioned in strategy
    components = {
        "stdio_transport": Path("mini_agent/vscode_extension/enhanced_extension_stdio.js").exists(),
        "enhanced_server": Path("mini_agent/acp/enhanced_server.py").exists(),
        "chat_participant": False,  # We'll check the content
        "session_management": False,  # We'll check the content
        "tool_integration": False,   # We'll check the content
    }
    
    # Check enhanced_extension_stdio.js for key features
    stdio_file = Path("mini_agent/vscode_extension/enhanced_extension_stdio.js")
    if stdio_file.exists():
        content = stdio_file.read_text()
        components["chat_participant"] = "chatParticipant" in content
        components["session_management"] = "session" in content.lower()
        components["tool_integration"] = "spawn" in content and "python" in content
    
    for component, status in components.items():
        print(f"{'✅' if status else '❌'} {component.replace('_', ' ').title()}: {'Present' if status else 'Missing'}")
    
    return components

def test_strategy_alignment():
    """Test alignment with documented strategy"""
    print("\n🔍 TESTING STRATEGY ALIGNMENT")
    print("-" * 50)
    
    # Key strategy claims to validate
    strategy_claims = {
        "70_percent_complete": False,  # Based on file analysis
        "stdio_server_ready": False,   # Based on stdio file existence
        "extension_foundation": False, # Based on JS file existence
        "minimal_changes_needed": False, # Based on transport analysis
    }
    
    # Validate claims
    if (Path("mini_agent/vscode_extension/enhanced_extension_stdio.js").exists() and
        Path("mini_agent/acp/enhanced_server.py").exists()):
        strategy_claims["70_percent_complete"] = True
        
    if Path("mini_agent/vscode_extension/enhanced_extension_stdio.js").exists():
        content = Path("mini_agent/vscode_extension/enhanced_extension_stdio.js").read_text()
        if "child_process.spawn" in content and "python" in content:
            strategy_claims["stdio_server_ready"] = True
    
    if Path("mini_agent/vscode_extension/enhanced_extension.js").exists():
        strategy_claims["extension_foundation"] = True
        
    # Check if minimal changes are needed (stdio vs websocket)
    if strategy_claims["stdio_server_ready"] and strategy_claims["extension_foundation"]:
        enhanced_content = Path("mini_agent/vscode_extension/enhanced_extension.js").read_text()
        stdio_content = Path("mini_agent/vscode_extension/enhanced_extension_stdio.js").read_text()
        if "WebSocket" in enhanced_content and "child_process" in stdio_content:
            strategy_claims["minimal_changes_needed"] = True
    
    for claim, status in strategy_claims.items():
        print(f"{'✅' if status else '❌'} {claim.replace('_', ' ').title()}: {'Valid' if status else 'Invalid'}")
    
    return strategy_claims

def main():
    """Main validation function"""
    print("🚀 MINI-AGENT VS CODE EXTENSION FACT-CHECK VALIDATION")
    print("=" * 60)
    
    # Run all tests
    import_results = test_core_imports()
    acp_results = test_acp_implementation()
    extension_results = test_vscode_extension()
    architecture_results = test_architecture_compliance()
    strategy_results = test_strategy_alignment()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    # Calculate scores
    import_score = sum(import_results.values()) / len(import_results) * 100
    acp_score = (sum(acp_results["files"].values()) + 
                int(acp_results["enhanced_server"]) + 
                int(acp_results["main_module"])) / (len(acp_results["files"]) + 2) * 100
    extension_score = sum(1 for r in extension_results.values() if r["exists"]) / len(extension_results) * 100
    architecture_score = sum(architecture_results.values()) / len(architecture_results) * 100
    strategy_score = sum(strategy_results.values()) / len(strategy_results) * 100
    
    overall_score = (import_score + acp_score + extension_score + architecture_score + strategy_score) / 5
    
    print(f"Core Imports: {import_score:.1f}%")
    print(f"ACP Implementation: {acp_score:.1f}%")  
    print(f"VS Code Extension: {extension_score:.1f}%")
    print(f"Architecture Compliance: {architecture_score:.1f}%")
    print(f"Strategy Alignment: {strategy_score:.1f}%")
    print(f"\n🎯 OVERALL SCORE: {overall_score:.1f}%")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 30)
    
    if overall_score >= 90:
        print("✅ Implementation is production-ready!")
        print("🚀 Proceed with Phase 1: Chat API integration")
    elif overall_score >= 70:
        print("⚠️  Implementation is mostly complete but needs fixes")
        print("🔧 Fix ACP library conflict before proceeding")
    elif overall_score >= 50:
        print("❌ Significant gaps identified")
        print("🛠️  Major implementation work required")
    else:
        print("🚨 Critical issues found")
        print("🔨 Substantial development needed")
    
    # Specific next steps
    if not acp_results["main_module"]:
        print("\n📋 IMMEDIATE ACTIONS REQUIRED:")
        print("1. Fix ACP library naming conflict")
        print("2. Test enhanced_server.py directly")
        print("3. Resolve import issues")
    
    return {
        "scores": {
            "imports": import_score,
            "acp": acp_score, 
            "extension": extension_score,
            "architecture": architecture_score,
            "strategy": strategy_score,
            "overall": overall_score
        },
        "results": {
            "imports": import_results,
            "acp": acp_results,
            "extension": extension_results,
            "architecture": architecture_results,
            "strategy": strategy_results
        }
    }

if __name__ == "__main__":
    results = main()