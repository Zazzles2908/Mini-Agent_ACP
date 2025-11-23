#!/usr/bin/env python3
"""
QA System Vulnerability Self-Assessment Test
"""

import sys
sys.path.append('.')

try:
    from mini_agent.skills.fact-checking-self-assessment.tools.validation_tool import ValidationEngine, DeceptionType
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
    engine = ValidationEngine()
    result = engine.validate_task_completion(validation_request)

    print(f'Honesty Score: {result["honesty_score"]}/100')
    print(f'Integrity Level: {result["integrity_level"]}')
    print(f'Overall Assessment: {result["overall_assessment"]}')
    print()

    if result['deception_patterns']:
        print('Detected Deception Patterns:')
        for pattern in result['deception_patterns']:
            print(f'- {pattern["type"]}: {pattern["description"]}')
    else:
        print('✅ No deception patterns detected.')

    print()
    print('Strengths Identified:')
    for strength in result['strengths']:
        print(f'✓ {strength}')

    print()
    print('Issues Identified:')
    for issue in result['issues']:
        print(f'❌ {issue}')

    print()
    print('Recommendations:')
    for rec in result['recommendations']:
        print(f'→ {rec}')

    print()
    print(f'Detailed Analysis: {result["detailed_analysis"]}')

    # Additional brutal honesty analysis
    print("\n" + "="*50)
    print("BRUTAL HONESTY ANALYSIS")
    print("="*50)

    # Check if the system is honest about its own limitations
    if result["honesty_score"] < 90:
        print("✅ System demonstrates honesty by not inflating self-assessment")
    else:
        print("❌ System may be overconfident in its self-assessment")

    # Check for vulnerability awareness
    if any("vulnerability" in str(rec).lower() for rec in result["recommendations"]):
        print("✅ System shows awareness of its own vulnerabilities")
    else:
        print("❌ System may lack awareness of its own limitations")

    # Check for brutal honesty about vulnerabilities
    if result["honesty_score"] < 85:
        print("✅ System demonstrates brutal honesty about its own capabilities")
    else:
        print("❌ System may be avoiding brutal honesty about limitations")

    print("\n" + "="*50)
    print("VULNERABILITY DETECTION CHECK")
    print("="*50)

    # The test: Does the QA system detect its own vulnerabilities?
    vulnerability_detected = any("vulnerability" in str(rec).lower() for rec in result["recommendations"])
    
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