#!/usr/bin/env python3
"""
Mini-Agent Integration Script

This script integrates the fact-checking system with Mini-Agent workflows,
providing seamless validation and assessment capabilities.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import our fact-checking modules
sys.path.append(str(Path(__file__).parent))
from fact_checker import FactChecker, FunctionalTester, SelfAssessor, FactCheckResult, TestResult, QualityMetrics

class MiniAgentIntegration:
    """Integration layer for Mini-Agent workflows"""
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.fact_checker = FactChecker()
        self.tester = FunctionalTester()
        self.assessor = SelfAssessor()
        
    def assess_implementation(self, 
                            task_description: str,
                            implementation_files: List[str],
                            requirements: List[str],
                            claims_to_verify: List[str] = None) -> Dict[str, Any]:
        """Perform comprehensive assessment of an implementation"""
        
        print(f"🔍 Starting assessment for: {task_description}")
        
        # Step 1: Fact-checking (if claims provided)
        fact_checks = []
        if claims_to_verify:
            print("📚 Running fact-checks...")
            for claim in claims_to_verify:
                result = self.fact_checker.verify_claim(claim)
                fact_checks.append(result)
                status_icon = {"verified": "✅", "partial": "⚠️", "unverified": "❌"}
                print(f"   {status_icon[result.status.value]} {claim[:60]}...")
        
        # Step 2: Functional testing
        print("🧪 Running functional tests...")
        test_results = []
        
        # Test file existence
        file_tests = self.tester.test_file_existence(implementation_files)
        test_results.extend(file_tests)
        
        # Test code syntax for Python files
        for file_path in implementation_files:
            if file_path.endswith('.py'):
                syntax_test = self.tester.test_code_syntax(file_path)
                test_results.append(syntax_test)
        
        # Test requirements coverage
        # Read content from files to check requirements
        for file_path in implementation_files:
            if Path(file_path).exists():
                try:
                    content = Path(file_path).read_text(encoding='utf-8')
                    req_tests = self.tester.test_requirements_coverage(content, requirements)
                    test_results.extend(req_tests)
                except UnicodeDecodeError:
                    # Try with different encodings
                    for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                        try:
                            content = Path(file_path).read_text(encoding=encoding)
                            req_tests = self.tester.test_requirements_coverage(content, requirements)
                            test_results.extend(req_tests)
                            break
                        except UnicodeDecodeError:
                            continue
        
        # Step 3: Calculate metrics
        metrics = self.assessor.calculate_quality_metrics(fact_checks, test_results, requirements)
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(fact_checks, test_results, metrics)
        
        # Step 5: Create comprehensive assessment
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "implementation_files": implementation_files,
            "requirements": requirements,
            "fact_checks": [fc.__dict__ for fc in fact_checks],
            "test_results": [tr.__dict__ for tr in test_results],
            "metrics": metrics.__dict__,
            "recommendations": recommendations,
            "overall_status": self._determine_status(metrics)
        }
        
        return assessment
    
    def _generate_recommendations(self, 
                                fact_checks: List[FactCheckResult], 
                                test_results: List[TestResult],
                                metrics: QualityMetrics) -> List[str]:
        """Generate actionable recommendations based on assessment"""
        recommendations = []
        
        # Fact-checking recommendations
        unverified = [fc for fc in fact_checks if fc.status.value in ['unverified', 'conflicting']]
        if unverified:
            recommendations.append(f"🔍 Verify {len(unverified)} unverified claims with additional sources")
        
        # Testing recommendations
        failed_tests = [tr for tr in test_results if not tr.passed]
        if failed_tests:
            recommendations.append(f"🔧 Address {len(failed_tests)} failing tests")
        
        # Quality recommendations
        if metrics.accuracy_score < 80:
            recommendations.append("📚 Improve factual accuracy with more reliable sources")
        
        if metrics.completeness_score < 80:
            recommendations.append("📋 Ensure all requirements are fully addressed")
        
        if metrics.functionality_score < 80:
            recommendations.append("⚙️ Improve functional implementation and testing")
        
        if metrics.reliability_score < 80:
            recommendations.append("🔄 Add error handling and edge case coverage")
        
        # General recommendations
        if metrics.overall_confidence >= 90:
            recommendations.append("✨ Excellent work! Consider adding advanced features or optimizations")
        elif metrics.overall_confidence >= 75:
            recommendations.append("👍 Good implementation. Review minor issues before finalizing")
        
        return recommendations
    
    def _determine_status(self, metrics: QualityMetrics) -> str:
        """Determine overall status based on metrics"""
        if metrics.overall_confidence >= 90:
            return "APPROVED"
        elif metrics.overall_confidence >= 75:
            return "CONDITIONAL_APPROVAL"
        elif metrics.overall_confidence >= 60:
            return "NEEDS_IMPROVEMENT"
        else:
            return "REJECTED"
    
    def save_assessment(self, assessment: Dict[str, Any], filename: str = None) -> str:
        """Save assessment to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"assessment_{timestamp}.json"
        
        filepath = self.workspace_path / filename
        with open(filepath, 'w') as f:
            json.dump(assessment, f, indent=2, default=str)
        
        return str(filepath)
    
    def generate_markdown_report(self, assessment: Dict[str, Any]) -> str:
        """Generate human-readable markdown report"""
        metrics = assessment["metrics"]
        
        # Calculate test statistics
        total_tests = len(assessment["test_results"])
        passed_tests = sum(1 for tr in assessment["test_results"] if tr["passed"])
        
        # Calculate fact-check statistics
        total_claims = len(assessment["fact_checks"])
        verified_claims = sum(1 for fc in assessment["fact_checks"] 
                            if (fc["status"].value if hasattr(fc["status"], 'value') else fc["status"]) == "verified")
        
        report = f"""# Implementation Assessment Report

## Task Overview
**Description:** {assessment["task_description"]}  
**Assessment Date:** {datetime.fromisoformat(assessment["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")}  
**Overall Status:** {assessment["overall_status"]}

## Quality Summary
**Overall Confidence:** {metrics["overall_confidence"]:.1f}/100

### Metrics Breakdown
- **Accuracy:** {metrics["accuracy_score"]:.1f}/100
- **Completeness:** {metrics["completeness_score"]:.1f}/100  
- **Functionality:** {metrics["functionality_score"]:.1f}/100
- **Reliability:** {metrics["reliability_score"]:.1f}/100

## Test Results Summary
- **Total Tests:** {total_tests}
- **Passed:** {passed_tests}
- **Failed:** {total_tests - passed_tests}
- **Success Rate:** {(passed_tests/total_tests*100) if total_tests > 0 else 0:.1f}%

## Fact-Checking Summary
- **Total Claims:** {total_claims}
- **Verified:** {verified_claims}
- **Success Rate:** {(verified_claims/total_claims*100) if total_claims > 0 else 0:.1f}%

## Recommendations
"""
        
        for i, rec in enumerate(assessment["recommendations"], 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## Detailed Results

### Functional Tests
"""
        for tr in assessment["test_results"]:
            status_icon = "✅" if tr["passed"] else "❌"
            report += f"- **{status_icon} {tr['test_name']}**\n  - {tr['details']}\n"
        
        if assessment["fact_checks"]:
            report += "\n### Fact-Checking Results\n"
            for fc in assessment["fact_checks"]:
                status = fc["status"]
                if hasattr(status, 'value'):
                    status = status.value
                status_icon = {"verified": "✅", "partial": "⚠️", "unverified": "❌", "conflicting": "⚠️"}
                report += f"- **{status_icon.get(status, '❓')} {fc['claim'][:80]}...**\n"
                report += f"  - Confidence: {fc['confidence']:.1%}\n"
                report += f"  - Sources: {len(fc['sources'])}\n"
        
        report += f"""
---
*Assessment generated automatically by Mini-Agent Integration System*
"""
        
        return report

def quick_assess(task: str, files: List[str], requirements: List[str]) -> None:
    """Quick assessment function for common use cases"""
    integration = MiniAgentIntegration()
    
    assessment = integration.assess_implementation(
        task_description=task,
        implementation_files=files,
        requirements=requirements
    )
    
    # Save JSON assessment
    json_path = integration.save_assessment(assessment)
    
    # Generate and save markdown report
    md_report = integration.generate_markdown_report(assessment)
    report_path = integration.workspace_path / "assessment_report.md"
    report_path.write_text(md_report)
    
    # Print summary
    print("\n" + "="*60)
    print("🎯 ASSESSMENT COMPLETE")
    print("="*60)
    print(f"Status: {assessment['overall_status']}")
    print(f"Confidence: {assessment['metrics']['overall_confidence']:.1f}/100")
    print(f"JSON Report: {json_path}")
    print(f"Markdown Report: {report_path}")
    print("="*60)

def main():
    """Main entry point for the integration script"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python agent_integration.py quick <task> <file1> <file2> ...")
        print("  python agent_integration.py assess <config.json>")
        print("\nExample:")
        print("  python agent_integration.py quick \"Create web scraper\" scraper.py requirements.txt")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "quick":
        if len(sys.argv) < 4:
            print("Quick assessment requires: task file1 file2 [file3 ...]")
            sys.exit(1)
        
        task = sys.argv[2]
        files = sys.argv[3:]
        requirements = [f"Implement {task}", "Include error handling", "Add documentation"]
        
        quick_assess(task, files, requirements)
    
    elif command == "assess":
        if len(sys.argv) < 3:
            print("Assessment requires: config.json")
            sys.exit(1)
        
        config_path = sys.argv[2]
        with open(config_path) as f:
            config = json.load(f)
        
        integration = MiniAgentIntegration()
        assessment = integration.assess_implementation(**config)
        
        # Save results
        json_path = integration.save_assessment(assessment)
        report = integration.generate_markdown_report(assessment)
        
        print(f"Assessment complete! Results saved to {json_path}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()