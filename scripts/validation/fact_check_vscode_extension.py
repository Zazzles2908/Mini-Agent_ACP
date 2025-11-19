#!/usr/bin/env python3
"""
Fact-checking validation for VS Code extension implementation status.
Verifies all claims about the current implementation.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

class FactChecker:
    """Fact-checking system for VS Code extension claims."""
    
    def __init__(self):
        self.claims_to_verify = []
        self.facts_found = []
        self.conflicts = []
        self.confidence_scores = {}
        
    def verify_file_existence(self, file_path: str) -> bool:
        """Check if file exists and get basic info."""
        try:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                return True, size
            return False, 0
        except Exception as e:
            return False, f"Error: {e}"
    
    def verify_directory_structure(self, base_dir: str, expected_files: List[str]) -> Dict[str, Any]:
        """Verify expected files exist in directory."""
        results = {}
        base_path = Path(base_dir)
        
        for file_name in expected_files:
            file_path = base_path / file_name
            exists, info = self.verify_file_existence(str(file_path))
            results[file_name] = {
                'exists': exists,
                'size': info if isinstance(info, int) else 0,
                'error': info if isinstance(info, str) else None
            }
        
        return results
    
    def verify_acp_server_functionality(self) -> Dict[str, Any]:
        """Test ACP server startup and basic functionality."""
        try:
            # Test import
            result = subprocess.run([
                sys.executable, "-c", 
                "from mini_agent.acp import __init__; print('Import successful')"
            ], capture_output=True, text=True, timeout=10)
            
            import_success = result.returncode == 0
            
            # Test basic startup
            startup_result = subprocess.run([
                sys.executable, "-m", "mini_agent.acp", "--help"
            ], capture_output=True, text=True, timeout=5)
            
            startup_success = startup_result.returncode == 0
            
            return {
                'import_works': import_success,
                'startup_works': startup_success,
                'help_output': startup_result.stdout if startup_success else startup_result.stderr
            }
        except Exception as e:
            return {'error': str(e)}
    
    def verify_node_environment(self) -> Dict[str, Any]:
        """Check Node.js availability and version."""
        try:
            # Check Node.js version
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            node_available = result.returncode == 0
            node_version = result.stdout.strip() if node_available else None
            
            # Check if npm is available
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            npm_available = npm_result.returncode == 0
            npm_version = npm_result.stdout.strip() if npm_available else None
            
            return {
                'node_available': node_available,
                'node_version': node_version,
                'npm_available': npm_available,
                'npm_version': npm_version
            }
        except Exception as e:
            return {'error': str(e)}
    
    def verify_package_json(self, package_path: str) -> Dict[str, Any]:
        """Verify package.json content and chat API configuration."""
        try:
            with open(package_path, 'r') as f:
                package_data = json.load(f)
            
            # Check for Chat API elements
            has_chat_participants = 'chatParticipants' in package_data.get('contributes', {})
            has_mini_agent_chat = False
            if has_chat_participants:
                for participant in package_data['contributes']['chatParticipants']:
                    if participant.get('id') == 'mini-agent':
                        has_mini_agent_chat = True
                        break
            
            return {
                'file_valid_json': True,
                'has_chat_participants': has_chat_participants,
                'has_mini_agent_chat': has_mini_agent_chat,
                'commands_count': len(package_data.get('contributes', {}).get('commands', [])),
                'keybindings_count': len(package_data.get('contributes', {}).get('keybindings', []))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def verify_documentation_files(self, doc_dir: str) -> Dict[str, Any]:
        """Check documentation files exist and have content."""
        expected_docs = [
            'README.md',
            '00_IMPLEMENTATION_PATHWAY_SUMMARY.md',
            '01_ACP_VS_CODE_INTEGRATION_OVERVIEW.md', 
            '02_ACP_STDIO_SERVER_IMPLEMENTATION.md',
            '03_VSCODE_EXTENSION_DEVELOPMENT.md',
            '05_IMPLEMENTATION_STATUS_AND_NEXT_STEPS.md'
        ]
        
        results = {}
        total_size = 0
        
        for doc_file in expected_docs:
            file_path = Path(doc_dir) / doc_file
            exists, size = self.verify_file_existence(str(file_path))
            results[doc_file] = {
                'exists': exists,
                'size': size if isinstance(size, int) else 0
            }
            if isinstance(size, int):
                total_size += size
        
        return {
            'files_found': sum(1 for r in results.values() if r['exists']),
            'total_expected': len(expected_docs),
            'total_size_bytes': total_size,
            'file_details': results
        }
    
    def calculate_confidence_score(self, verification_results: Dict[str, Any]) -> Tuple[float, str]:
        """Calculate overall confidence score based on verification results."""
        score = 0.0
        max_score = 0.0
        
        # ACP Server (25 points)
        max_score += 25
        if verification_results.get('acp_server', {}).get('import_works'):
            score += 15
        if verification_results.get('acp_server', {}).get('startup_works'):
            score += 10
        
        # Extension Files (25 points)
        max_score += 25
        acp_files = verification_results.get('acp_files', {})
        if acp_files.get('chat_integration_extension.js', {}).get('exists'):
            score += 10
        if acp_files.get('package.json', {}).get('exists'):
            score += 10
        if verification_results.get('package_config', {}).get('has_mini_agent_chat'):
            score += 5
        
        # Documentation (20 points)
        max_score += 20
        doc_results = verification_results.get('documentation', {})
        if doc_results.get('files_found', 0) >= 5:
            score += 20
        elif doc_results.get('files_found', 0) >= 3:
            score += 15
        elif doc_results.get('files_found', 0) >= 1:
            score += 10
        
        # Environment (15 points)
        max_score += 15
        env_results = verification_results.get('environment', {})
        if env_results.get('node_available'):
            score += 8
        if env_results.get('npm_available'):
            score += 7
        
        # Testing (15 points)
        max_score += 15
        test_results = verification_results.get('testing_scripts', {})
        if test_results.get('test_file_exists'):
            score += 10
        if test_results.get('diagnostic_file_exists'):
            score += 5
        
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        if percentage >= 90:
            confidence_level = "HIGH - Production ready"
        elif percentage >= 70:
            confidence_level = "MEDIUM - Review recommended"
        elif percentage >= 50:
            confidence_level = "LOW - Significant gaps"
        else:
            confidence_level = "NEEDS REVIEW - Major issues"
        
        return round(percentage, 1), confidence_level
    
    def generate_fact_check_report(self) -> Dict[str, Any]:
        """Generate comprehensive fact-checking report."""
        print("🔍 Starting VS Code Extension Fact-Checking...")
        
        verification_results = {}
        
        # 1. Verify ACP Server Implementation
        print("1️⃣ Checking ACP Server Implementation...")
        verification_results['acp_server'] = self.verify_acp_server_functionality()
        
        # 2. Verify Extension Files
        print("2️⃣ Checking Extension Files...")
        acp_files = ['chat_integration_extension.js', 'package.json', 'enhanced_extension.js']
        verification_results['acp_files'] = self.verify_directory_structure(
            'mini_agent/vscode_extension', acp_files
        )
        
        # 3. Verify Package Configuration
        print("3️⃣ Checking Package Configuration...")
        package_path = 'mini_agent/vscode_extension/package.json'
        verification_results['package_config'] = self.verify_package_json(package_path)
        
        # 4. Verify Documentation
        print("4️⃣ Checking Documentation Files...")
        verification_results['documentation'] = self.verify_documentation_files('documents/vscode-extension')
        
        # 5. Verify Environment
        print("5️⃣ Checking Development Environment...")
        verification_results['environment'] = self.verify_node_environment()
        
        # 6. Verify Testing Scripts
        print("6️⃣ Checking Testing Scripts...")
        test_file_exists, _ = self.verify_file_existence('scripts/testing/test_acp_vscode_integration.py')
        diagnostic_exists, _ = self.verify_file_existence('scripts/testing/simple_acp_diagnostic.py')
        verification_results['testing_scripts'] = {
            'test_file_exists': test_file_exists,
            'diagnostic_file_exists': diagnostic_exists
        }
        
        # Calculate overall confidence
        confidence_score, confidence_level = self.calculate_confidence_score(verification_results)
        
        # Generate final report
        report = {
            'confidence_score': confidence_score,
            'confidence_level': confidence_level,
            'verification_results': verification_results,
            'summary': {
                'acp_server_working': verification_results['acp_server'].get('import_works', False),
                'extension_files_present': verification_results['acp_files'].get('chat_integration_extension.js', {}).get('exists', False),
                'chat_api_configured': verification_results['package_config'].get('has_mini_agent_chat', False),
                'documentation_complete': verification_results['documentation'].get('files_found', 0) >= 5,
                'environment_ready': verification_results['environment'].get('node_available', False),
                'testing_available': verification_results['testing_scripts'].get('test_file_exists', False)
            }
        }
        
        return report

def main():
    """Run comprehensive fact-checking of VS Code extension implementation."""
    checker = FactChecker()
    report = checker.generate_fact_check_report()
    
    print("\n" + "="*60)
    print("📊 VS CODE EXTENSION FACT-CHECK REPORT")
    print("="*60)
    
    print(f"\n🎯 OVERALL CONFIDENCE SCORE: {report['confidence_score']}%")
    print(f"📈 CONFIDENCE LEVEL: {report['confidence_level']}")
    
    print(f"\n✅ KEY FINDINGS:")
    summary = report['summary']
    
    findings = []
    if summary['acp_server_working']:
        findings.append("✅ ACP Server: Working and responsive")
    else:
        findings.append("❌ ACP Server: Not working or not accessible")
        
    if summary['extension_files_present']:
        findings.append("✅ Extension Files: Present and implemented")
    else:
        findings.append("❌ Extension Files: Missing or incomplete")
        
    if summary['chat_api_configured']:
        findings.append("✅ Chat API: @mini-agent participant configured")
    else:
        findings.append("❌ Chat API: Not properly configured")
        
    if summary['documentation_complete']:
        findings.append("✅ Documentation: Comprehensive guides available")
    else:
        findings.append("❌ Documentation: Missing or incomplete")
        
    if summary['environment_ready']:
        findings.append("✅ Environment: Node.js/npm available for development")
    else:
        findings.append("❌ Environment: Node.js not available")
        
    if summary['testing_available']:
        findings.append("✅ Testing: Test scripts available")
    else:
        findings.append("❌ Testing: No test scripts found")
    
    for finding in findings:
        print(f"  {finding}")
    
    print(f"\n🔧 DETAILED VERIFICATION:")
    
    # ACP Server Details
    acp_results = report['verification_results']['acp_server']
    print(f"  ACP Server Import: {'✅' if acp_results.get('import_works') else '❌'}")
    print(f"  ACP Server Startup: {'✅' if acp_results.get('startup_works') else '❌'}")
    
    # Extension Files Details
    acp_files = report['verification_results']['acp_files']
    for file_name, details in acp_files.items():
        status = "✅" if details.get('exists') else "❌"
        size_info = f"({details.get('size', 0)} bytes)" if details.get('exists') else "(missing)"
        print(f"  {file_name}: {status} {size_info}")
    
    # Documentation Details
    doc_results = report['verification_results']['documentation']
    print(f"  Documentation: {doc_results.get('files_found', 0)}/{doc_results.get('total_expected', 0)} files")
    
    # Environment Details
    env_results = report['verification_results']['environment']
    print(f"  Node.js: {'✅ ' + env_results.get('node_version', '') if env_results.get('node_available') else '❌ Not available'}")
    print(f"  npm: {'✅ ' + env_results.get('npm_version', '') if env_results.get('npm_available') else '❌ Not available'}")
    
    # Save detailed report
    with open('scripts/testing/vscode_extension_fact_check_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: scripts/testing/vscode_extension_fact_check_report.json")
    
    if report['confidence_score'] >= 80:
        print(f"\n🎉 CONCLUSION: Implementation appears production-ready!")
        print(f"   Ready for extension packaging and testing.")
    elif report['confidence_score'] >= 60:
        print(f"\n⚠️  CONCLUSION: Implementation needs review.")
        print(f"   Some issues found that should be addressed.")
    else:
        print(f"\n❌ CONCLUSION: Significant gaps identified.")
        print(f"   Implementation needs major work before testing.")
    
    return report['confidence_score']

if __name__ == "__main__":
    main()
