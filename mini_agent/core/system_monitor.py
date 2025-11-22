#!/usr/bin/env python3
"""
Mini-Agent System Monitor
========================
Integrated system health monitoring for Mini-Agent.
"""

import os
import sys
from pathlib import Path

class SystemMonitor:
    """Monitor Mini-Agent system health and functionality."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
    
    def check_environment(self):
        """Check environment variables"""
        zapi = os.environ.get('ZAI_API_KEY')
        mapi = os.environ.get('MINIMAX_API_KEY')
        
        return {
            'zapi': zapi is not None,
            'mapi': mapi is not None,
            'zapi_available': bool(zapi),
            'mapi_available': bool(mapi)
        }
    
    def check_core_imports(self):
        """Check if core system can be imported"""
        results = {}
        
        # Test Agent import
        try:
            from ..agent import Agent
            results['agent'] = True
        except Exception as e:
            results['agent'] = False
            results['agent_error'] = str(e)
        
        # Test tools import
        try:
            from ..tools import get_tools
            tools = get_tools()
            results['tools'] = True
            results['tools_count'] = len(tools)
        except Exception as e:
            results['tools'] = False
            results['tools_error'] = str(e)
        
        # Test skills import
        try:
            from ..skills import list_skills
            skills = list_skills()
            results['skills'] = True
            results['skills_count'] = len(skills)
        except Exception as e:
            results['skills'] = False
            results['skills_error'] = str(e)
        
        return results
    
    def run_health_check(self):
        """Run comprehensive system health check"""
        print("🔍 Mini-Agent System Health Check")
        print("=" * 50)
        
        # Check environment
        env = self.check_environment()
        print("\n1. Environment Variables:")
        print(f"   ZAI_API_KEY: {'✅ Available' if env['zapi'] else '❌ Missing'}")
        print(f"   MINIMAX_API_KEY: {'✅ Available' if env['mapi'] else '❌ Missing'}")
        
        # Check core imports
        imports = self.check_core_imports()
        print("\n2. Core System Imports:")
        
        if imports.get('agent'):
            print("   ✅ Agent class imported")
        else:
            print(f"   ❌ Agent import failed: {imports.get('agent_error', 'Unknown error')}")
        
        if imports.get('tools'):
            print(f"   ✅ Tools system working: {imports.get('tools_count', 0)} tools available")
        else:
            print(f"   ❌ Tools system failed: {imports.get('tools_error', 'Unknown error')}")
        
        if imports.get('skills'):
            print(f"   ✅ Skills system working: {imports.get('skills_count', 0)} skills available")
        else:
            print(f"   ❌ Skills system failed: {imports.get('skills_error', 'Unknown error')}")
        
        # Summary
        print("\n3. System Summary:")
        print("   📊 Basic functionality test complete")
        print("   🎯 Ready for detailed component testing")
        
        return {
            'environment': env,
            'imports': imports,
            'status': 'healthy' if all([imports.get('agent'), imports.get('tools'), imports.get('skills')]) else 'issues_detected'
        }

def main():
    """Run system health check"""
    monitor = SystemMonitor()
    return monitor.run_health_check()

if __name__ == "__main__":
    main()
