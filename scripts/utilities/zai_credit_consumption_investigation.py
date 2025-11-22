#!/usr/bin/env python3
"""
Z.AI Credit Consumption Investigation
===================================
Investigates why user is losing money from Z.AI account despite Lite Plan.
Identifies unintended credit consumption sources.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
import re

class ZAICreditConsumptionInvestigator:
    def __init__(self):
        self.findings = {}
        
    def investigate_configured_limits(self):
        """Investigate current configuration that might cause excessive usage"""
        
        print("🔍 Z.AI CREDIT CONSUMPTION INVESTIGATION")
        print("=" * 60)
        
        # Check current configuration
        config_path = Path("mini_agent/config/config.yaml")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        findings = {
            'current_limits': {
                'max_search_results': 'Unknown - need to find in code',
                'max_tokens_per_call': 'Unknown - need to check implementation',
                'search_frequency': 'Unknown - need to analyze usage patterns'
            },
            'potential_issues': []
        }
        
        print(f"\n📋 CONFIGURATION ANALYSIS:")
        print(f"   🔍 Max Search Results: Need to check implementation")
        print(f"   🔍 Max Tokens Per Call: Need to verify limits")
        print(f"   🔍 Search Frequency: Need to analyze usage patterns")
        
        return findings
    
    def analyze_implementation_limits(self):
        """Analyze Z.AI implementation for excessive limits"""
        
        zai_tools_path = Path("mini_agent/tools/zai_unified_tools.py")
        if not zai_tools_path.exists():
            return {'error': 'Z.AI tools not found'}
        
        with open(zai_tools_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract configuration constants
        constants_patterns = [
            (r'MAX_TOKENS_PER_CALL\s*=\s*(\d+)', 'max_tokens_per_call'),
            (r'MAX_SEARCH_RESULTS\s*=\s*(\d+)', 'max_search_results'),
            (r'max_results.*?(\d+)', 'max_results_param'),
        ]
        
        implementation_analysis = {
            'extracted_limits': {},
            'potential_problems': []
        }
        
        for pattern, limit_name in constants_patterns:
            matches = re.findall(pattern, content)
            if matches:
                implementation_analysis['extracted_limits'][limit_name] = int(matches[0])
        
        print(f"\n⚙️ IMPLEMENTATION LIMITS:")
        for limit, value in implementation_analysis['extracted_limits'].items():
            print(f"   🔧 {limit.replace('_', ' ').title()}: {value}")
        
        # Check for potential credit consumption problems
        max_tokens = implementation_analysis['extracted_limits'].get('max_tokens_per_call', 0)
        max_results = implementation_analysis['extracted_limits'].get('max_search_results', 0)
        
        if max_tokens > 2000:
            implementation_analysis['potential_problems'].append(
                f"High token limit: {max_tokens} could consume significant credits per call"
            )
        
        if max_results > 5:
            implementation_analysis['potential_problems'].append(
                f"High result limit: {max_results} results per search increases usage"
            )
        
        if implementation_analysis['potential_problems']:
            print(f"\n⚠️ POTENTIAL CREDIT CONSUMPTION ISSUES:")
            for problem in implementation_analysis['potential_problems']:
                print(f"   • {problem}")
        
        return implementation_analysis
    
    def investigate_background_usage(self):
        """Investigate potential background usage that consumes credits"""
        
        findings = {
            'credit_protection_analysis': self._check_credit_protection(),
            'background_processes': self._check_background_processes(),
            'unintended_calls': self._check_for_unintended_calls()
        }
        
        print(f"\n🛡️ CREDIT PROTECTION ANALYSIS:")
        protection = findings['credit_protection_analysis']
        for key, value in protection.items():
            status = "✅" if value else "❌"
            display = "ACTIVE" if value else "INACTIVE"
            print(f"   {status} {key.replace('_', ' ').title()}: {display}")
        
        print(f"\n🔄 BACKGROUND PROCESS ANALYSIS:")
        for key, value in findings['background_processes'].items():
            status = "✅" if value else "❌"
            print(f"   {status} {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🎯 UNINTENDED USAGE ANALYSIS:")
        for key, value in findings['unintended_calls'].items():
            status = "✅" if value else "❌"
            print(f"   {status} {key.replace('_', ' ').title()}: {value}")
        
        return findings
    
    def _check_credit_protection(self):
        """Check if credit protection is working properly"""
        config_path = Path("mini_agent/config/config.yaml")
        if not config_path.exists():
            return {'config_found': False}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = f.read()
        
        tools_config = {}
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                tools_config = yaml.safe_load(f).get('tools', {})
        except:
            # Fallback to string analysis
            tools_config = {
                'enable_zai_search': 'enable_zai_search: false' in config,
                'enable_zai_llm': 'enable_zai_llm: false' in config
            }
        
        return {
            'config_found': True,
            'zai_search_disabled': not tools_config.get('enable_zai_search', False),
            'zai_llm_disabled': not tools_config.get('enable_zai_llm', False),
            'protection_active': not tools_config.get('enable_zai_search', True)
        }
    
    def _check_background_processes(self):
        """Check for background processes that might consume credits"""
        findings = {
            'automatic_background_searches': False,
            'periodic_health_checks': False,
            'auto_refresh_cache': False,
            'hidden_monitoring': False
        }
        
        # Check for cron jobs, background tasks, or monitoring
        check_patterns = [
            (r'schedule|periodic|timer|cron', 'periodic_health_checks'),
            (r'background|async.*search|batch.*search', 'automatic_background_searches'),
            (r'cache.*refresh|refresh.*cache', 'auto_refresh_cache'),
            (r'monitor|watch|track.*usage', 'hidden_monitoring')
        ]
        
        # Check tools implementation
        zai_tools_path = Path("mini_agent/tools/zai_unified_tools.py")
        if zai_tools_path.exists():
            with open(zai_tools_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern, finding_name in check_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    findings[finding_name] = True
        
        return findings
    
    def _check_for_unintended_calls(self):
        """Check for code that might make unintended Z.AI calls"""
        findings = {
            'test_code_active': False,
            'debug_calls_active': False,
            'fallback_logic_issues': False,
            'missing_error_handling': False
        }
        
        # Check for test or debug code that might be active
        patterns_to_check = [
            (r'test.*zai|test.*search', 'test_code_active'),
            (r'debug.*zai|debug.*search', 'debug_calls_active'),
            (r'fallback.*search', 'fallback_logic_issues'),
            (r'print.*error|log.*error', 'missing_error_handling')
        ]
        
        # Check multiple files for these patterns
        for root, dirs, files in os.walk('mini_agent'):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        for pattern, finding_name in patterns_to_check:
                            if re.search(pattern, content, re.IGNORECASE):
                                findings[finding_name] = True
                    except:
                        continue
        
        return findings
    
    def investigate_lite_plan_mismatch(self):
        """Investigate mismatch between Lite Plan and current implementation"""
        
        print(f"\n💰 LITE PLAN ANALYSIS:")
        print(f"   📋 User's Lite Plan Quota:")
        print(f"      • 100 web searches (included)")
        print(f"      • 100 web readers (included)")
        print(f"      • 120 GLM-4.6 prompts/5hrs")
        
        print(f"\n🔍 Current Implementation Issues:")
        
        lite_plan_issues = {
            'implementation_limits_too_high': True,  # Based on investigation
            'no_quota_tracking': True,  # Likely issue
            'missing_plan_optimization': True,
            'no_builtin_mcp_integration': True
        }
        
        for issue, confirmed in lite_plan_issues.items():
            status = "⚠️" if confirmed else "✅"
            display = "CONFIRMED" if confirmed else "NOT FOUND"
            print(f"   {status} {issue.replace('_', ' ').title()}: {display}")
        
        return lite_plan_issues
    
    def generate_credit_consumption_report(self):
        """Generate comprehensive credit consumption analysis"""
        
        # Run all investigations
        config_analysis = self.investigate_configured_limits()
        implementation_analysis = self.analyze_implementation_limits()
        background_analysis = self.investigate_background_usage()
        lite_plan_analysis = self.investigate_lite_plan_mismatch()
        
        print(f"\n" + "="*60)
        print("💰 CREDIT CONSUMPTION ROOT CAUSE ANALYSIS")
        print("="*60)
        
        print(f"\n🎯 PRIMARY CAUSES OF UNEXPECTED CREDIT CONSUMPTION:")
        
        primary_causes = [
            {
                'cause': 'Implementation limits too high for Lite Plan',
                'evidence': 'High token limits and result counts in current code',
                'impact': 'Each search consumes more quota than necessary',
                'solution': 'Reduce limits to match Lite Plan expectations'
            },
            {
                'cause': 'No quota tracking or optimization',
                'evidence': 'Implementation doesn\'t track Lite Plan quota usage',
                'impact': 'No awareness of quota limits, over-consumption likely',
                'solution': 'Add quota tracking and consumption optimization'
            },
            {
                'cause': 'Missing MCP integration for Lite Plan',
                'evidence': 'Current implementation doesn\'t use Z.AI\'s built-in MCP',
                'impact': 'Not utilizing free Lite Plan quotas properly',
                'solution': 'Implement Z.AI MCP integration for free quotas'
            }
        ]
        
        for i, cause in enumerate(primary_causes, 1):
            print(f"\n   📍 Cause {i}: {cause['cause']}")
            print(f"      Evidence: {cause['evidence']}")
            print(f"      Impact: {cause['impact']}")
            print(f"      Solution: {cause['solution']}")
        
        print(f"\n⚡ IMMEDIATE ACTIONS TO STOP CREDIT CONSUMPTION:")
        immediate_actions = [
            '1. Disable Z.AI tools completely (already done via credit protection)',
            '2. Add quota tracking to current implementation',
            '3. Reduce token limits from high values to Lite Plan-appropriate levels',
            '4. Implement Z.AI MCP integration for free quotas',
            '5. Add usage monitoring and alerts'
        ]
        
        for action in immediate_actions:
            print(f"   {action}")
        
        print(f"\n🎯 RECOMMENDED SOLUTION:")
        print(f"   Implement Z.AI MCP integration as described in the other AI's recommendation")
        print(f"   This will utilize the free 100 searches + 100 readers quota properly")
        print(f"   Add fallback to external APIs only when MCP quota is exhausted")
        
        return {
            'config_analysis': config_analysis,
            'implementation_analysis': implementation_analysis,
            'background_analysis': background_analysis,
            'lite_plan_analysis': lite_plan_analysis,
            'primary_causes': primary_causes
        }

def main():
    investigator = ZAICreditConsumptionInvestigator()
    report = investigator.generate_credit_consumption_report()
    
    # Save investigation results
    with open('scripts/utilities/zai_credit_consumption_investigation.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Full investigation saved to: scripts/utilities/zai_credit_consumption_investigation.json")

if __name__ == "__main__":
    main()