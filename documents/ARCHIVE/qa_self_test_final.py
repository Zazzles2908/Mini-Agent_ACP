#!/usr/bin/env python3
"""
QA System Vulnerability Self-Assessment Test
"""

import sys
import os
import asyncio

# Add current directory to path to ensure imports work
sys.path.insert(0, '.')

async def test_qa_system():
    try:
        # Direct import from the file path
        sys.path.append(os.path.join(os.getcwd(), 'mini_agent', 'skills', 'fact-checking-self-assessment', 'tools'))
        
        import validation_tool as qa_validation
        import json

        print("=== QA SYSTEM SELF-VALIDATION TEST ===\n")

        # Create validation request for our own vulnerability analysis
        validation_request = {
            'task_description': 'Analyze AI deception vulnerabilities in QA validation system',
            'claimed_deliverables': [
                'Comprehensive vulnerability analysis document',
                'Identification of 10+ exploitation pathways', 
                'Risk level assessment for each vulnerability',
                'Mitigation recommendations',
                'System weakness summary',
                'Critical security recommendations'
            ],
            'requirements_checklist': [
                'Identify specific ways AIs can bypass validation',
                'Provide concrete exploitation examples',
                'Assess bypass potential for each vulnerability',
                'Recommend immediate mitigation actions',
                'Analyze system trust-based weaknesses',
                'Provide brutal honesty assessment'
            ],
            'actual_files': ['documents/06_TESTING_QA/QA_SYSTEM_VULNERABILITY_ANALYSIS.md'],
            'validation_level': 'strict',
            'confidence_level': 'high'
        }

        # Run validation
        engine = qa_validation.ValidationEngine()
        
        # Create ValidationRequest object from the dict
        request = qa_validation.ValidationRequest(
            task_description=validation_request['task_description'],
            claimed_deliverables=validation_request['claimed_deliverables'],
            requirements_checklist=validation_request['requirements_checklist'],
            actual_files=validation_request['actual_files'],
            validation_level=validation_request['validation_level'],
            confidence_level=validation_request['confidence_level']
        )
        
        result = await engine.validate_completion(request)

        print(f'Honesty Score: {result.honesty_score}/100')
        print(f'Integrity Level: {getattr(result, "integrity_level", "Unknown")}')
        print(f'Overall Assessment: {result.validation_summary}')
        print()

        if result.deception_patterns:
            print('Detected Deception Patterns:')
            for pattern in result.deception_patterns:
                print(f'- {pattern["type"]}: {pattern["description"]}')
        else:
            print('✅ No deception patterns detected.')

        print()
        print('Strengths Identified:')
        strengths = getattr(result, 'strengths', [])
        if strengths:
            for strength in strengths:
                print(f'✓ {strength}')
        else:
            print('(No specific strengths identified)')

        print()
        print('Issues Identified:')
        issues = getattr(result, 'issues', [])
        if issues:
            for issue in issues:
                print(f'❌ {issue}')
        else:
            print('(No specific issues identified)')

        print()
        print('Recommendations:')
        for rec in result.recommendations:
            print(f'→ {rec}')

        print()
        print(f'Detailed Analysis: {result.validation_summary}')

        # Additional brutal honesty analysis
        print("\n" + "="*50)
        print("BRUTAL HONESTY ANALYSIS")
        print("="*50)

        # Check if the system is honest about its own limitations
        if result.honesty_score < 90:
            print("✅ System demonstrates honesty by not inflating self-assessment")
        else:
            print("❌ System may be overconfident in its self-assessment")

        # Check for vulnerability awareness
        rec_text = " ".join(result.recommendations).lower()
        if "vulnerability" in rec_text:
            print("✅ System shows awareness of its own vulnerabilities")
        else:
            print("❌ System may lack awareness of its own limitations")

        # Check for brutal honesty about vulnerabilities
        if result.honesty_score < 85:
            print("✅ System demonstrates brutal honesty about its own capabilities")
        else:
            print("❌ System may be avoiding brutal honesty about limitations")

        print("\n" + "="*50)
        print("VULNERABILITY DETECTION CHECK")
        print("="*50)

        # The test: Does the QA system detect its own vulnerabilities?
        vulnerability_detected = "vulnerability" in rec_text
        
        if vulnerability_detected:
            print("✅ QA system successfully detects its own vulnerabilities")
            print("✅ System maintains intellectual honesty")
        else:
            print("❌ QA system failed to detect its own vulnerabilities")
            print("❌ Potential self-deception detected")

    except Exception as e:
        print(f"❌ ERROR during validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qa_system())