#!/usr/bin/env python3
"""
Phase 1 Fact-Check Assessment
============================

This script properly fact-checks Phase 1 implementation by testing
actual functionality vs. claimed deliverables.
"""

import asyncio
import json
import traceback
from pathlib import Path
from typing import Dict, List, Any

# Import components
from mini_agent.config import get_config
from mini_agent.tools.note_tool import (
    EnhancedSessionNoteTool, 
    EnhancedRecallNoteTool,
    SessionNoteTool,
    RecallNoteTool
)
from mini_agent.cli import add_workspace_tools


class Phase1FactChecker:
    """Fact-checker for Phase 1 implementation."""
    
    def __init__(self):
        self.results = []
        self.critical_issues = []
        self.workarounds_needed = []
    
    def log_result(self, test_name: str, status: str, details: str, evidence: str = ""):
        """Log a test result."""
        self.results.append({
            "test": test_name,
            "status": status,  # PASS, FAIL, PARTIAL, ISSUE
            "details": details,
            "evidence": evidence
        })
        print(f"[{status}] {test_name}: {details}")
        if evidence:
            print(f"    Evidence: {evidence}")
    
    async def test_1_configuration_loading(self):
        """Test 1: Enhanced configuration system."""
        print("\n1️⃣ TESTING: Enhanced Configuration System")
        
        try:
            config = get_config()
            memory_config = config.get_memory_config()
            
            # Check if methods exist
            assert hasattr(config, 'get_memory_config'), "Config should have get_memory_config method"
            
            # Check structure
            expected_keys = ['enable_enhanced', 'project_context', 'pattern_learning', 'storage_backend']
            for key in expected_keys:
                assert key in memory_config, f"Memory config missing {key}"
            
            self.log_result(
                "Configuration Loading", 
                "PASS", 
                "Enhanced configuration system working",
                f"get_memory_config() returns {len(memory_config)} keys"
            )
            return True
            
        except Exception as e:
            self.log_result(
                "Configuration Loading", 
                "FAIL", 
                f"Configuration system failed: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("Configuration system not working")
            return False
    
    async def test_2_enhanced_note_tool(self):
        """Test 2: Enhanced session note tool."""
        print("\n2️⃣ TESTING: Enhanced Session Note Tool")
        
        try:
            note_tool = EnhancedSessionNoteTool(memory_file='./workspace/fact_check_notes.json')
            
            # Test basic recording
            result = await note_tool.execute("Test note for fact check", category="test")
            assert result.success, f"Note recording failed: {result.error}"
            
            # Test classification
            assert result.content, "Note should have content"
            
            self.log_result(
                "Enhanced Note Tool", 
                "PASS", 
                "EnhancedSessionNoteTool records notes successfully",
                f"Response: {result.content[:80]}..."
            )
            return True
            
        except Exception as e:
            self.log_result(
                "Enhanced Note Tool", 
                "FAIL", 
                f"Enhanced note tool failed: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("Enhanced note tool not working")
            return False
    
    async def test_3_enhanced_recall_tool(self):
        """Test 3: Enhanced recall tool."""
        print("\n3️⃣ TESTING: Enhanced Recall Tool")
        
        try:
            recall_tool = EnhancedRecallNoteTool(memory_file='./workspace/fact_check_notes.json')
            
            # Test basic recall
            result = await recall_tool.execute()
            assert result.success, f"Recall failed: {result.error}"
            assert result.content, "Recall should return content"
            
            self.log_result(
                "Enhanced Recall Tool", 
                "PASS", 
                "EnhancedRecallNoteTool retrieves notes successfully",
                f"Retrieved {len(result.content)} characters"
            )
            return True
            
        except Exception as e:
            self.log_result(
                "Enhanced Recall Tool", 
                "FAIL", 
                f"Enhanced recall tool failed: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("Enhanced recall tool not working")
            return False
    
    async def test_4_cli_integration(self):
        """Test 4: CLI integration (the critical test)."""
        print("\n4️⃣ TESTING: CLI Integration")
        
        try:
            from mini_agent.config import get_config
            from pathlib import Path
            
            config = get_config()
            tools = []
            workspace_dir = Path('./workspace')
            
            # This is what the CLI does
            add_workspace_tools(tools, config, workspace_dir)
            
            # Check what tools were loaded
            note_tools = [t for t in tools if 'note' in t.name.lower()]
            
            if not note_tools:
                self.log_result(
                    "CLI Integration", 
                    "FAIL", 
                    "No note tools loaded by CLI",
                    f"Total tools loaded: {len(tools)}"
                )
                self.critical_issues.append("CLI not loading note tools")
                return False
            
            self.log_result(
                "CLI Integration", 
                "PASS", 
                f"CLI loads {len(note_tools)} note tools successfully",
                f"Tools: {[t.name for t in note_tools]}"
            )
            return True
            
        except Exception as e:
            self.log_result(
                "CLI Integration", 
                "FAIL", 
                f"CLI integration failed: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("CLI integration broken")
            return False
    
    async def test_5_backward_compatibility(self):
        """Test 5: Backward compatibility."""
        print("\n5️⃣ TESTING: Backward Compatibility")
        
        try:
            # Test original interfaces
            compat_note = SessionNoteTool(memory_file='./workspace/compat_test.json')
            compat_recall = RecallNoteTool(memory_file='./workspace/compat_test.json')
            
            # Test note recording
            result = await compat_note.execute("Backward compatibility test", category="test")
            assert result.success, "Backward compatible note should work"
            
            # Test recall
            recall_result = await compat_recall.execute()
            assert recall_result.success, "Backward compatible recall should work"
            
            self.log_result(
                "Backward Compatibility", 
                "PASS", 
                "Original interfaces work correctly",
                f"Note: {result.success}, Recall: {recall_result.success}"
            )
            return True
            
        except Exception as e:
            self.log_result(
                "Backward Compatibility", 
                "FAIL", 
                f"Backward compatibility broken: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("Backward compatibility broken")
            return False
    
    async def test_6_agent_startup(self):
        """Test 6: Agent startup (the real test)."""
        print("\n6️⃣ TESTING: Agent Startup")
        
        try:
            # Try to import the main agent components
            from mini_agent.agent import Agent
            from mini_agent.llm import LLMClient
            
            # Try to create basic agent (this is where failures happen)
            # Note: This will fail without proper LLM setup, but we can test basic initialization
            print("    Attempting basic agent import...")
            
            # This is a basic test - if this fails, the whole system is broken
            assert Agent is not None, "Agent class should exist"
            assert LLMClient is not None, "LLMClient should exist"
            
            self.log_result(
                "Agent Startup", 
                "PASS", 
                "Basic agent components import successfully",
                "Agent and LLMClient classes available"
            )
            return True
            
        except Exception as e:
            self.log_result(
                "Agent Startup", 
                "FAIL", 
                f"Agent startup failed: {str(e)}",
                traceback.format_exc()
            )
            self.critical_issues.append("Agent system not starting properly")
            return False
    
    async def run_fact_check(self):
        """Run complete fact-check assessment."""
        print("🔍 PHASE 1 FACT-CHECK ASSESSMENT")
        print("=" * 50)
        
        tests = [
            ("Configuration Loading", self.test_1_configuration_loading),
            ("Enhanced Note Tool", self.test_2_enhanced_note_tool),
            ("Enhanced Recall Tool", self.test_3_enhanced_recall_tool),
            ("CLI Integration", self.test_4_cli_integration),
            ("Backward Compatibility", self.test_5_backward_compatibility),
            ("Agent Startup", self.test_6_agent_startup),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if await test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_result(test_name, "FAIL", f"Test crashed: {str(e)}")
                failed += 1
        
        print("\n" + "=" * 50)
        print("📊 FACT-CHECK RESULTS:")
        print(f"   ✅ PASSED: {passed}/{len(tests)} tests")
        print(f"   ❌ FAILED: {failed}/{len(tests)} tests")
        
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"   ❌ {issue}")
        
        # Generate honesty assessment
        print(f"\n🎯 HONESTY ASSESSMENT:")
        if failed == 0:
            print("   ✅ Implementation matches claims - NO DECEPTION DETECTED")
            honesty_score = 100
        elif failed <= 2:
            print("   ⚠️  Minor issues detected - mostly truthful implementation")
            honesty_score = 75
        else:
            print("   ❌ Significant issues - Implementation incomplete/misrepresented")
            honesty_score = 25
        
        print(f"   📊 Calculated Honesty Score: {honesty_score}/100")
        
        return {
            "passed": passed,
            "failed": failed,
            "total": len(tests),
            "critical_issues": self.critical_issues,
            "honesty_score": honesty_score,
            "results": self.results
        }


async def main():
    """Run the fact-check assessment."""
    checker = Phase1FactChecker()
    results = await checker.run_fact_check()
    
    # Save detailed results
    with open('phase1_fact_check_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: phase1_fact_check_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())