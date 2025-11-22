#!/usr/bin/env python3
"""
Comprehensive Codebase Research Script
Analyzes the Mini-Agent system to understand current architecture and web search implementation
"""

import os
import ast
import json
import yaml
import asyncio
import aiohttp
from pathlib import Path
import subprocess
import re
from datetime import datetime

class CodebaseAnalyzer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.analysis_results = {}
        self.issues = []
        self.recommendations = []
        
    def analyze_directory_structure(self):
        """Analyze the complete directory structure"""
        print("🔍 Analyzing directory structure...")
        
        structure = {}
        for root, dirs, files in os.walk(self.base_path):
            # Skip hidden and build directories
            if any(skip in root for skip in ['.git', '.venv', '__pycache__', 'node_modules']):
                continue
                
            rel_path = os.path.relpath(root, self.base_path)
            if rel_path == '.':
                rel_path = 'root'
                
            structure[rel_path] = {
                'directories': dirs,
                'files': files
            }
            
        self.analysis_results['structure'] = structure
        return structure
    
    def analyze_config_files(self):
        """Analyze all configuration files"""
        print("⚙️ Analyzing configuration files...")
        
        config_files = {}
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(('.yaml', '.yml', '.json', '.toml', '.ini')):
                    if any(skip in root for skip in ['.git', '.venv', '__pycache__']):
                        continue
                        
                    file_path = Path(root) / file
                    rel_path = os.path.relpath(file_path, self.base_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        if file.endswith(('.yaml', '.yml')):
                            config_data = yaml.safe_load(content)
                        else:
                            try:
                                config_data = json.loads(content)
                            except:
                                config_data = content[:500]  # First 500 chars
                                
                        config_files[rel_path] = config_data
                        
                        # Look for web search related configs
                        if isinstance(config_data, dict):
                            self._analyze_web_config(config_data, rel_path)
                            
                    except Exception as e:
                        config_files[rel_path] = f"Error reading: {e}"
                        
        self.analysis_results['config_files'] = config_files
        return config_files
    
    def _analyze_web_config(self, config_data: dict, file_path: str):
        """Analyze web search configuration"""
        if 'tools' in config_data and 'enable_zai_search' in config_data['tools']:
            search_enabled = config_data['tools']['enable_zai_search']
            self.analysis_results['web_search_config'] = {
                'enabled': search_enabled,
                'config_file': file_path,
                'full_config': config_data
            }
    
    def analyze_web_search_implementation(self):
        """Analyze web search implementation files"""
        print("🌐 Analyzing web search implementation...")
        
        web_search_files = []
        web_imports = []
        
        # Find files containing web search related code
        for root, dirs, files in os.walk(self.base_path):
            if any(skip in root for skip in ['.git', '.venv', '__pycache__']):
                continue
                
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    rel_path = os.path.relpath(file_path, self.base_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Check for web search related code
                        web_indicators = [
                            'z.ai', 'zai', 'web_search', 'web_reader', 
                            'api.z.ai', 'glm-4.6', 'aiohttp'
                        ]
                        
                        if any(indicator in content.lower() for indicator in web_indicators):
                            web_search_files.append({
                                'path': rel_path,
                                'size': len(content),
                                'contains': [ind for ind in web_indicators if ind in content.lower()]
                            })
                            
                        # Extract imports
                        try:
                            tree = ast.parse(content)
                            imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import)]
                            for imp in imports:
                                for alias in imp.names:
                                    if any(term in alias.name.lower() for term in ['aiohttp', 'requests', 'http']):
                                        web_imports.append({
                                            'file': rel_path,
                                            'import': alias.name,
                                            'line': imp.lineno
                                        })
                        except:
                            pass
                            
                    except Exception as e:
                        self.issues.append(f"Error reading {rel_path}: {e}")
                        
        self.analysis_results['web_search_files'] = web_search_files
        self.analysis_results['web_imports'] = web_imports
        return web_search_files, web_imports
    
    def test_current_web_functionality(self):
        """Test current web search functionality"""
        print("🧪 Testing current web search functionality...")
        
        # Test Z.AI API directly
        async def test_api():
            try:
                import os
                api_key = os.getenv('ZAI_API_KEY')
                if not api_key:
                    return {"status": "error", "message": "ZAI_API_KEY not found"}
                    
                url = 'https://api.z.ai/api/coding/paas/v4/web-search'
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'query': 'MCP Model Context Protocol',
                    'model': 'glm-4.6',
                    'max_results': 2
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as response:
                        result = await response.json()
                        
                        return {
                            "status": "success" if response.status == 200 else "error",
                            "status_code": response.status,
                            "response_length": len(str(result)),
                            "has_results": "results" in result,
                            "sample_result": result.get("results", [{}])[0] if "results" in result else None
                        }
                        
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        # Run the test
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            api_test_result = loop.run_until_complete(test_api())
            self.analysis_results['api_test'] = api_test_result
        except Exception as e:
            self.analysis_results['api_test'] = {"status": "error", "message": str(e)}
    
    def analyze_script_organization(self):
        """Analyze script organization issues"""
        print("📁 Analyzing script organization...")
        
        scripts = []
        for root, dirs, files in os.walk(self.base_path):
            if any(skip in root for skip in ['.git', '.venv', '__pycache__', 'node_modules']):
                continue
                
            for file in files:
                if file.endswith('.py') and 'script' in file.lower():
                    file_path = Path(root) / file
                    rel_path = os.path.relpath(file_path, self.base_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        scripts.append({
                            'path': rel_path,
                            'size': len(content),
                            'is_test': 'test' in content.lower(),
                            'has_main': 'def main(' in content or 'if __name__' in content
                        })
                    except Exception as e:
                        scripts.append({
                            'path': rel_path,
                            'error': str(e)
                        })
                        
        self.analysis_results['scripts'] = scripts
        return scripts
    
    def generate_recommendations(self):
        """Generate research-based recommendations"""
        print("💡 Generating recommendations...")
        
        recommendations = []
        
        # Web search functionality recommendations
        if 'web_search_config' in self.analysis_results:
            enabled = self.analysis_results['web_search_config']['enabled']
            recommendations.append({
                'category': 'web_search',
                'priority': 'high',
                'issue': f'Web search is currently {"enabled" if enabled else "disabled"}',
                'recommendation': 'Ensure web search functionality is properly integrated with credit protection'
            })
        
        # Script organization recommendations
        if len(self.analysis_results.get('scripts', [])) > 20:
            recommendations.append({
                'category': 'organization',
                'priority': 'medium',
                'issue': 'Too many scattered scripts causing maintenance issues',
                'recommendation': 'Consolidate scripts into proper module structure'
            })
        
        # API test recommendations
        if self.analysis_results.get('api_test', {}).get('status') == 'success':
            recommendations.append({
                'category': 'functionality',
                'priority': 'high',
                'issue': 'Z.AI API is working but may not be properly integrated',
                'recommendation': 'Implement proper MCP integration for native Z.AI web capabilities'
            })
        
        self.recommendations = recommendations
        return recommendations
    
    def create_comprehensive_report(self):
        """Create a comprehensive analysis report"""
        print("📋 Creating comprehensive report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis_results': self.analysis_results,
            'issues': self.issues,
            'recommendations': self.recommendations,
            'summary': {
                'total_files_analyzed': len([f for f in self.analysis_results.get('structure', {}).values() 
                                            for f in f.get('files', [])]),
                'web_search_files_found': len(self.analysis_results.get('web_search_files', [])),
                'config_files_found': len(self.analysis_results.get('config_files', {})),
                'scripts_found': len(self.analysis_results.get('scripts', [])),
                'critical_issues': len([r for r in self.recommendations if r['priority'] == 'high'])
            }
        }
        
        return report

async def main():
    print("🚀 Starting Comprehensive Codebase Research...")
    
    analyzer = CodebaseAnalyzer("C:\\Users\\Jazeel-Home\\Mini-Agent")
    
    # Run all analyses
    analyzer.analyze_directory_structure()
    analyzer.analyze_config_files()
    analyzer.analyze_web_search_implementation()
    analyzer.test_current_web_functionality()
    analyzer.analyze_script_organization()
    analyzer.generate_recommendations()
    
    # Generate report
    report = analyzer.create_comprehensive_report()
    
    # Save report
    with open('codebase_research_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("✅ Research complete!")
    print(f"📊 Summary: {report['summary']}")
    print(f"🔍 Found {len(analyzer.analysis_results.get('web_search_files', []))} web search related files")
    print(f"⚙️ Found {len(analyzer.analysis_results.get('config_files', {}))} configuration files")
    print(f"🐍 Found {len(analyzer.analysis_results.get('scripts', []))} scripts")
    print(f"💡 Generated {len(analyzer.recommendations)} recommendations")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())