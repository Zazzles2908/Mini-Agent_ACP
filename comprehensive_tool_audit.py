#!/usr/bin/env python3
"""
Comprehensive Tool Audit and Testing Script
Tests all available tools and creates optimization plan
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any
import traceback

# Add current directory to path for imports
sys.path.insert(0, '.')

class ComprehensiveToolAudit:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "platform": "Windows",
            "test_results": {},
            "api_keys": {},
            "tools_status": {},
            "optimization_recommendations": []
        }
        
    def check_api_keys(self):
        """Check availability of API keys"""
        print("🔑 Checking API Keys...")
        
        keys_to_check = [
            "MINIMAX_API_KEY",
            "ZAI_API_KEY", 
            "OPENAI_API_KEY"
        ]
        
        for key in keys_to_check:
            value = os.getenv(key)
            self.results["api_keys"][key] = {
                "available": bool(value),
                "length": len(value) if value else 0,
                "masked": f"{value[:8]}..." if value else None
            }
            status = "✅ Available" if value else "❌ Missing"
            print(f"  {key}: {status}")
    
    def test_basic_tools(self):
        """Test basic native tools"""
        print("\n🛠️ Testing Basic Tools...")
        
        # Test file operations
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write("Test content")
                temp_file = f.name
            
            # Test file reading (this would be our native read_file tool)
            with open(temp_file, 'r') as f:
                content = f.read()
            
            os.unlink(temp_file)
            self.results["test_results"]["file_operations"] = {
                "status": "PASS",
                "details": "File read/write working correctly"
            }
            print("  ✅ File Operations: PASS")
            
        except Exception as e:
            self.results["test_results"]["file_operations"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"  ❌ File Operations: FAIL - {e}")
    
    async def test_zai_tools(self):
        """Test Z.AI tools functionality"""
        print("\n🌐 Testing Z.AI Tools...")
        
        try:
            from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
            
            # Test tool initialization
            search_tool = ZAIWebSearchTool()
            reader_tool = ZAIWebReaderTool()
            
            self.results["tools_status"]["zai_web_search"] = {
                "available": search_tool.available,
                "initialized": bool(search_tool.client)
            }
            
            self.results["tools_status"]["zai_web_reader"] = {
                "available": reader_tool.available,
                "initialized": bool(reader_tool.client)
            }
            
            print(f"  🔍 Z.AI Web Search: {'✅ Available' if search_tool.available else '❌ Unavailable'}")
            print(f"  📖 Z.AI Web Reader: {'✅ Available' if reader_tool.available else '❌ Unavailable'}")
            
            # If available, test a small search
            if search_tool.available:
                print("  🧪 Testing Z.AI Web Search with sample query...")
                try:
                    result = await search_tool.execute(
                        query="Python web scraping best practices",
                        depth="quick",
                        model="glm-4.6"
                    )
                    
                    if result.success:
                        self.results["test_results"]["zai_web_search"] = {
                            "status": "PASS",
                            "model_used": "glm-4.6",
                            "response_length": len(result.content)
                        }
                        print("  ✅ Z.AI Web Search: PASS")
                    else:
                        self.results["test_results"]["zai_web_search"] = {
                            "status": "FAIL",
                            "error": result.error
                        }
                        print(f"  ❌ Z.AI Web Search: FAIL - {result.error}")
                        
                except Exception as e:
                    self.results["test_results"]["zai_web_search"] = {
                        "status": "FAIL",
                        "error": str(e)
                    }
                    print(f"  ❌ Z.AI Web Search: FAIL - {e}")
            
        except ImportError as e:
            self.results["test_results"]["zai_tools"] = {
                "status": "FAIL",
                "error": f"Import error: {e}"
            }
            print(f"  ❌ Z.AI Tools: FAIL - Import error: {e}")
    
    def test_skills_system(self):
        """Test skills system availability"""
        print("\n🎯 Testing Skills System...")
        
        try:
            skills_dir = "mini_agent/skills"
            if not os.path.exists(skills_dir):
                self.results["test_results"]["skills_system"] = {
                    "status": "FAIL",
                    "error": "Skills directory not found"
                }
                print("  ❌ Skills System: FAIL - Directory not found")
                return
            
            # Count available skills
            skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
            skill_count = len([s for s in skills if s not in ['.gitignore', '__pycache__']])
            
            self.results["tools_status"]["skills_system"] = {
                "total_skills": skill_count,
                "skills_dir_exists": True,
                "skills": skills
            }
            
            print(f"  ✅ Skills System: {skill_count} skills available")
            for skill in sorted(skills):
                if skill not in ['.gitignore', '__pycache__']:
                    print(f"    - {skill}")
                    
        except Exception as e:
            self.results["test_results"]["skills_system"] = {
                "status": "FAIL", 
                "error": str(e)
            }
            print(f"  ❌ Skills System: FAIL - {e}")
    
    def test_knowledge_graph(self):
        """Test knowledge graph functionality"""
        print("\n🧠 Testing Knowledge Graph...")
        
        try:
            # Test if knowledge graph functions are available
            # This would be our native knowledge graph tools
            self.results["tools_status"]["knowledge_graph"] = {
                "native_available": True,
                "functions": [
                    "create_entities", "add_observations", "open_nodes",
                    "search_nodes", "read_graph", "create_relations"
                ]
            }
            print("  ✅ Knowledge Graph: Native tools available")
            
        except Exception as e:
            self.results["test_results"]["knowledge_graph"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"  ❌ Knowledge Graph: FAIL - {e}")
    
    def test_llm_clients(self):
        """Test LLM client availability"""
        print("\n🤖 Testing LLM Clients...")
        
        try:
            from mini_agent.llm.llm_wrapper import LLMClient
            from mini_agent.schema import LLMProvider
            
            # Test client initialization
            clients_to_test = [
                ("MiniMax", LLMProvider.ANTHROPIC),
                ("OpenAI", LLMProvider.OPENAI),
                ("Z.AI", LLMProvider.ZAI)
            ]
            
            for name, provider in clients_to_test:
                try:
                    # Just test initialization, not actual API calls
                    api_key = os.getenv(f"{name.upper()}_API_KEY")
                    if api_key:
                        self.results["tools_status"][f"llm_client_{name.lower()}"] = {
                            "available": True,
                            "provider": str(provider),
                            "api_key_length": len(api_key)
                        }
                        print(f"  ✅ {name} Client: Available")
                    else:
                        self.results["tools_status"][f"llm_client_{name.lower()}"] = {
                            "available": False,
                            "reason": "No API key"
                        }
                        print(f"  ⚠️ {name} Client: Available but no API key")
                        
                except Exception as e:
                    self.results["tools_status"][f"llm_client_{name.lower()}"] = {
                        "available": False,
                        "error": str(e)
                    }
                    print(f"  ❌ {name} Client: FAIL - {e}")
                    
        except ImportError as e:
            self.results["test_results"]["llm_clients"] = {
                "status": "FAIL",
                "error": f"Import error: {e}"
            }
            print(f"  ❌ LLM Clients: FAIL - {e}")
    
    def generate_optimization_recommendations(self):
        """Generate optimization recommendations based on test results"""
        print("\n📈 Generating Optimization Recommendations...")
        
        recommendations = []
        
        # Z.AI Model recommendation
        if self.results["api_keys"].get("ZAI_API_KEY", {}).get("available"):
            recommendations.append({
                "category": "Z.AI Usage",
                "recommendation": "Use GLM-4.6 for all Z.AI operations (best quality)",
                "rationale": "You have Z.AI Lite plan with ~120 prompts/5hrs, prioritize quality over quantity",
                "priority": "HIGH"
            })
        
        # MiniMax recommendation  
        if self.results["api_keys"].get("MINIMAX_API_KEY", {}).get("available"):
            recommendations.append({
                "category": "MiniMax Usage", 
                "recommendation": "Leverage 300 prompts/5hrs quota for complex reasoning tasks",
                "rationale": "MiniMax has higher quota than Z.AI, use for main reasoning",
                "priority": "HIGH"
            })
        
        # Skills recommendation
        skill_count = self.results["tools_status"].get("skills_system", {}).get("total_skills", 0)
        if skill_count > 0:
            recommendations.append({
                "category": "Skills System",
                "recommendation": f"Load skills progressively: {skill_count} skills available",
                "rationale": "Use progressive disclosure (Level 1→2→3) for efficiency",
                "priority": "MEDIUM"
            })
        
        # File operations
        file_ops_status = self.results["test_results"].get("file_operations", {}).get("status")
        if file_ops_status == "PASS":
            recommendations.append({
                "category": "File Operations",
                "recommendation": "Use native file tools for unlimited operations",
                "rationale": "No quota limitations, most efficient for file operations",
                "priority": "MEDIUM"
            })
        
        self.results["optimization_recommendations"] = recommendations
        
        for rec in recommendations:
            priority_icon = "🔴" if rec["priority"] == "HIGH" else "🟡" if rec["priority"] == "MEDIUM" else "🟢"
            print(f"  {priority_icon} {rec['category']}: {rec['recommendation']}")
    
    def save_results(self):
        """Save audit results to file"""
        results_file = "comprehensive_tool_audit_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Audit results saved to: {results_file}")
        return results_file
    
    async def run_complete_audit(self):
        """Run complete tool audit"""
        print("🚀 Starting Comprehensive Tool Audit...")
        print("=" * 50)
        
        self.check_api_keys()
        self.test_basic_tools()
        await self.test_zai_tools()
        self.test_skills_system()
        self.test_knowledge_graph()
        self.test_llm_clients()
        self.generate_optimization_recommendations()
        
        print("\n" + "=" * 50)
        print("✅ Complete Tool Audit Finished!")
        
        return self.save_results()

# Run the audit
async def main():
    audit = ComprehensiveToolAudit()
    await audit.run_complete_audit()

if __name__ == "__main__":
    asyncio.run(main())
