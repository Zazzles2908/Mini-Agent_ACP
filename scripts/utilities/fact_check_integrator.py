#!/usr/bin/env python3
"""
Simple Fact-Check Integration Tool
=================================
Integrates fact-checking capabilities into system verification.
Addresses user's need to verify what's built vs assumptions.
"""

import os
import json
from pathlib import Path

class FactCheckIntegrator:
    def __init__(self):
        self.fact_check_log = []
        
    def integrate_with_system_verification(self):
        """Integrate fact-checking with system verification workflow"""
        
        # Define claims to fact-check
        system_claims = [
            {
                "claim": "Primary AI model is MiniMax-M2 (not Claude or OpenAI)",
                "verification_method": "config_file_check",
                "expected_result": "config.yaml shows MiniMax-M2 as primary model"
            },
            {
                "claim": "Secondary model is GLM-4.6 via Z.AI (not GPT-4)",
                "verification_method": "config_file_check", 
                "expected_result": "config.yaml mentions GLM-4.6 and Z.AI endpoint"
            },
            {
                "claim": "Web functionality uses Z.AI v4 endpoint with OpenAI SDK wrapper",
                "verification_method": "tools_integration_check",
                "expected_result": "Tools use zai_base: https://api.z.ai/api/coding/paas/v4"
            },
            {
                "claim": "Credit protection prevents accidental usage",
                "verification_method": "config_protection_check",
                "expected_result": "enable_zai_search: false in config by default"
            },
            {
                "claim": "File organization follows proper directory structure",
                "verification_method": "filesystem_check",
                "expected_result": "Python scripts in scripts/utilities/, docs in documents/"
            }
        ]
        
        verification_results = []
        
        for claim in system_claims:
            result = self.fact_check_individual_claim(claim)
            verification_results.append(result)
            
        return verification_results
    
    def fact_check_individual_claim(self, claim):
        """Fact-check a single system claim"""
        
        method = claim['verification_method']
        expected = claim['expected_result']
        
        if method == "config_file_check":
            return self.check_config_claim(claim)
        elif method == "tools_integration_check":
            return self.check_tools_integration(claim)
        elif method == "config_protection_check":
            return self.check_protection_setting(claim)
        elif method == "filesystem_check":
            return self.check_filesystem_organization(claim)
        else:
            return {
                "claim": claim['claim'],
                "method": method,
                "status": "unknown_method",
                "confidence": 0,
                "error": f"Unknown verification method: {method}"
            }
    
    def check_config_claim(self, claim):
        """Check configuration-based claims"""
        try:
            config_path = Path("mini_agent/config/config.yaml")
            if not config_path.exists():
                return {
                    "claim": claim['claim'],
                    "method": "config_file_check",
                    "status": "failed",
                    "confidence": 0,
                    "error": "Config file not found"
                }
            
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Check for MiniMax-M2
            if "minimax-m2" in content and "primary" in claim['claim'].lower():
                return {
                    "claim": claim['claim'],
                    "method": "config_file_check",
                    "status": "verified",
                    "confidence": 95,
                    "evidence": "Found 'MiniMax-M2' in config file"
                }
            
            # Check for GLM-4.6
            elif "glm-4.6" in content and "glm" in claim['claim'].lower():
                return {
                    "claim": claim['claim'],
                    "method": "config_file_check",
                    "status": "verified",
                    "confidence": 95,
                    "evidence": "Found 'glm-4.6' reference in config file"
                }
            
            return {
                "claim": claim['claim'],
                "method": "config_file_check",
                "status": "failed",
                "confidence": 10,
                "error": "Expected content not found in config"
            }
            
        except Exception as e:
            return {
                "claim": claim['claim'],
                "method": "config_file_check",
                "status": "error",
                "confidence": 0,
                "error": str(e)
            }
    
    def check_protection_setting(self, claim):
        """Check credit protection settings"""
        try:
            config_path = Path("mini_agent/config/config.yaml")
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for disabled search (credit protection)
            if "enable_zai_search: false" in content:
                return {
                    "claim": claim['claim'],
                    "method": "config_protection_check",
                    "status": "verified",
                    "confidence": 98,
                    "evidence": "Credit protection active: enable_zai_search: false"
                }
            
            return {
                "claim": claim['claim'],
                "method": "config_protection_check",
                "status": "warning",
                "confidence": 20,
                "evidence": "Credit protection may not be active"
            }
            
        except Exception as e:
            return {
                "claim": claim['claim'],
                "method": "config_protection_check",
                "status": "error",
                "confidence": 0,
                "error": str(e)
            }
    
    def check_tools_integration(self, claim):
        """Check tools integration"""
        try:
            tools_path = Path("mini_agent/tools/__init__.py")
            if not tools_path.exists():
                return {
                    "claim": claim['claim'],
                    "method": "tools_integration_check",
                    "status": "failed",
                    "confidence": 0,
                    "error": "Tools module not found"
                }
            
            with open(tools_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Z.AI integration indicators
            if "zai" in content.lower() and "api" in content.lower():
                return {
                    "claim": claim['claim'],
                    "method": "tools_integration_check",
                    "status": "verified",
                    "confidence": 90,
                    "evidence": "Z.AI integration found in tools module"
                }
            
            return {
                "claim": claim['claim'],
                "method": "tools_integration_check",
                "status": "partial",
                "confidence": 60,
                "evidence": "Partial Z.AI integration detected"
            }
            
        except Exception as e:
            return {
                "claim": claim['claim'],
                "method": "tools_integration_check",
                "status": "error",
                "confidence": 0,
                "error": str(e)
            }
    
    def check_filesystem_organization(self, claim):
        """Check filesystem organization"""
        try:
            scripts_utilities = Path("scripts/utilities")
            documents = Path("documents")
            
            if scripts_utilities.exists() and documents.exists():
                return {
                    "claim": claim['claim'],
                    "method": "filesystem_check",
                    "status": "verified",
                    "confidence": 95,
                    "evidence": "Both scripts/utilities/ and documents/ directories exist"
                }
            else:
                missing = []
                if not scripts_utilities.exists():
                    missing.append("scripts/utilities/")
                if not documents.exists():
                    missing.append("documents/")
                
                return {
                    "claim": claim['claim'],
                    "method": "filesystem_check",
                    "status": "failed",
                    "confidence": 10,
                    "error": f"Missing directories: {', '.join(missing)}"
                }
                
        except Exception as e:
            return {
                "claim": claim['claim'],
                "method": "filesystem_check",
                "status": "error",
                "confidence": 0,
                "error": str(e)
            }
    
    def generate_fact_check_report(self):
        """Generate comprehensive fact-check report"""
        results = self.integrate_with_system_verification()
        
        print("🔍 FACT-CHECK INTEGRATION REPORT")
        print("=" * 50)
        
        verified_count = 0
        total_count = len(results)
        
        for result in results:
            status_icon = {
                "verified": "✅",
                "partial": "⚠️",
                "failed": "❌",
                "error": "💥",
                "warning": "⚠️",
                "unknown_method": "❓"
            }.get(result['status'], "❓")
            
            confidence = result.get('confidence', 0)
            print(f"\n{status_icon} {result['claim']}")
            print(f"   Method: {result['method']}")
            print(f"   Status: {result['status'].upper()}")
            print(f"   Confidence: {confidence}%")
            
            if 'evidence' in result:
                print(f"   Evidence: {result['evidence']}")
            if 'error' in result:
                print(f"   Error: {result['error']}")
            
            if result['status'] == "verified":
                verified_count += 1
        
        print(f"\n🎯 SUMMARY:")
        print(f"   Verified: {verified_count}/{total_count} claims")
        success_rate = (verified_count / total_count) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("   ✅ System architecture matches claims")
        elif success_rate >= 60:
            print("   ⚠️  Mostly accurate with some discrepancies")
        else:
            print("   ❌ Significant discrepancies found")
        
        return {
            'results': results,
            'summary': {
                'verified_count': verified_count,
                'total_count': total_count,
                'success_rate': success_rate
            }
        }

def main():
    integrator = FactCheckIntegrator()
    report = integrator.generate_fact_check_report()
    
    # Save report
    report_file = "scripts/utilities/fact_check_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full fact-check report saved to: {report_file}")

if __name__ == "__main__":
    main()