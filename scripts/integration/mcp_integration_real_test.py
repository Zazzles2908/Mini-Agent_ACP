#!/usr/bin/env python3
"""
Real MCP Integration Test for Z.AI
Tests actual MCP server connectivity and functionality before migration
"""

import asyncio
import json
import aiohttp
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mini_agent.config.config import Config

class RealMCPIntegrationTest:
    def __init__(self):
        self.config = Config()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'zai_api_key': bool(self.config.zai_api_key),
            'zai_endpoint': 'https://api.z.ai/api/coding/paas/v4',
            'tests': {}
        }
    
    async def test_mcp_server_connectivity(self):
        """Test direct connection to Z.AI MCP server"""
        print("🔍 Testing MCP Server Connectivity...")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.config.zai_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Test MCP web search endpoint
            search_payload = {
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'web_search_prime',
                'params': {
                    'query': 'MCP protocol specifications',
                    'count': 3
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.z.ai/api/mcp/web_search_prime/mcp',
                    headers=headers,
                    json=search_payload,
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ MCP Search Server: Working (Status: {response.status})")
                        self.results['tests']['mcp_search_server'] = {
                            'status': 'working',
                            'status_code': response.status,
                            'response_size': len(str(data)),
                            'response_preview': str(data)[:200] + "..."
                        }
                    else:
                        print(f"❌ MCP Search Server: Error (Status: {response.status})")
                        self.results['tests']['mcp_search_server'] = {
                            'status': 'error',
                            'status_code': response.status,
                            'error': f'HTTP {response.status}'
                        }
                        
        except Exception as e:
            print(f"❌ MCP Search Server: Exception - {str(e)}")
            self.results['tests']['mcp_search_server'] = {
                'status': 'exception',
                'error': str(e)
            }
    
    async def test_mcp_reader_connectivity(self):
        """Test MCP reader server connectivity"""
        print("🔍 Testing MCP Reader Server...")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.config.zai_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Test a real URL with MCP reader
            reader_payload = {
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'web_reader',
                'params': {
                    'urls': ['https://docs.z.ai/devpack/mcp/web-search-mcp']
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.z.ai/api/mcp/web_reader/mcp',
                    headers=headers,
                    json=reader_payload,
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ MCP Reader Server: Working (Status: {response.status})")
                        self.results['tests']['mcp_reader_server'] = {
                            'status': 'working',
                            'status_code': response.status,
                            'response_size': len(str(data)),
                            'response_preview': str(data)[:200] + "..."
                        }
                    else:
                        print(f"❌ MCP Reader Server: Error (Status: {response.status})")
                        self.results['tests']['mcp_reader_server'] = {
                            'status': 'error',
                            'status_code': response.status,
                            'error': f'HTTP {response.status}'
                        }
                        
        except Exception as e:
            print(f"❌ MCP Reader Server: Exception - {str(e)}")
            self.results['tests']['mcp_reader_server'] = {
                'status': 'exception',
                'error': str(e)
            }
    
    async def test_current_zai_clients(self):
        """Test current working Z.AI client implementations"""
        print("🔍 Testing Current Z.AI Client Implementations...")
        
        clients_to_test = [
            ('mini_agent.llm.zai_client', 'ZAIClient'),
            ('mini_agent.llm.coding_plan_zai_client', 'CodingPlanZAIClient'),
            ('mini_agent.tools.zai_unified_tools', 'ZAIWebSearchTool')
        ]
        
        for module_path, class_name in clients_to_test:
            try:
                # Test import
                module = __import__(module_path, fromlist=[class_name])
                client_class = getattr(module, class_name)
                
                print(f"✅ {class_name}: Import successful")
                self.results['tests'][f'{module_path}_{class_name}'] = {
                    'status': 'import_success',
                    'module': module_path,
                    'class': class_name
                }
                
                # Test instantiation if possible
                if class_name == 'ZAIWebSearchTool':
                    try:
                        tool = client_class()
                        print(f"✅ {class_name}: Instantiation successful")
                        self.results['tests'][f'{module_path}_{class_name}']['instantiation'] = 'success'
                    except Exception as e:
                        print(f"⚠️ {class_name}: Instantiation failed - {str(e)}")
                        self.results['tests'][f'{module_path}_{class_name}']['instantiation'] = f'failed: {str(e)}'
                
            except Exception as e:
                print(f"❌ {class_name}: Import failed - {str(e)}")
                self.results['tests'][f'{module_path}_{class_name}'] = {
                    'status': 'import_failed',
                    'error': str(e)
                }
    
    async def run_comprehensive_test(self):
        """Run all integration tests"""
        print("🚀 Starting Real MCP Integration Test")
        print("=" * 50)
        
        # Test MCP servers
        await self.test_mcp_server_connectivity()
        await self.test_mcp_reader_connectivity()
        
        # Test current implementations
        await self.test_current_zai_clients()
        
        # Save results
        results_file = 'MCP_INTEGRATION_TEST_RESULTS.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results Summary:")
        print(f"   • MCP Search Server: {self.results['tests'].get('mcp_search_server', {}).get('status', 'not_tested')}")
        print(f"   • MCP Reader Server: {self.results['tests'].get('mcp_reader_server', {}).get('status', 'not_tested')}")
        print(f"   • Z.AI API Key: {'✅ Present' if self.results['zai_api_key'] else '❌ Missing'}")
        print(f"   • Results saved to: {results_file}")
        
        return self.results

async def main():
    """Main test execution"""
    test = RealMCPIntegrationTest()
    results = await test.run_comprehensive_test()
    
    # Print summary for terminal
    working_servers = []
    for server_name, result in results['tests'].items():
        if 'mcp' in server_name and result.get('status') == 'working':
            working_servers.append(server_name)
    
    if working_servers:
        print(f"\n🎯 MCP Servers Working: {len(working_servers)}/2")
        print("✅ Ready for Phase 1 (Consolidation)")
    else:
        print(f"\n⚠️ MCP Servers Not Working")
        print("🔧 Need to fix MCP connectivity before consolidation")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())