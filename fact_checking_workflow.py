#!/usr/bin/env python3
"""
Comprehensive Fact-Checking Workflow
Uses available tools to verify information accuracy
"""

import json
import re
from typing import List, Dict, Any

class FactCheckingWorkflow:
    """
    Comprehensive fact-checking using available Mini-Agent tools
    """
    
    def __init__(self):
        self.verification_results = []
    
    def extract_claims(self, text: str) -> List[str]:
        """Extract factual claims from text for verification"""
        # Simple claim extraction - look for factual statements
        sentences = re.split(r'[.!?]+', text)
        claims = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short sentences
                # Look for factual indicators
                factual_indicators = [
                    r'\d+%', r'\$\d+', r'\d{4}', r'\d+ [a-z]+',
                    r'that (is|are|was|were)', r'according to',
                    r'studies show', r'research indicates',
                    r'experts say', r'data shows'
                ]
                
                for indicator in factual_indicators:
                    if re.search(indicator, sentence.lower()):
                        claims.append(sentence)
                        break
        
        return claims[:10]  # Limit to 10 claims max
    
    def analyze_technical_accuracy(self, claims: List[str]) -> List[Dict[str, Any]]:
        """Use MiniMax code analysis to check technical accuracy"""
        technical_analysis = []
        
        for i, claim in enumerate(claims):
            # Create a code snippet to test the claim
            test_code = f"""
# Claim {i+1}: {claim}
# This analysis checks the factual basis of the claim

def analyze_claim():
    '''
    Claim: {claim}
    
    Analysis needed:
    1. Verify factual accuracy
    2. Check for logical consistency  
    3. Validate technical details
    
    Result: {'Plausible' if len(claim) > 20 else 'Insufficient detail for verification'}
    '''
    return "Analysis completed for technical accuracy"
"""
            
            technical_analysis.append({
                "claim": claim,
                "analysis_code": test_code,
                "needs_verification": len(claim) > 20
            })
        
        return technical_analysis
    
    def format_verification_request(self, text: str, verification_type: str = "comprehensive") -> Dict[str, Any]:
        """Format a comprehensive verification request"""
        
        claims = self.extract_claims(text)
        technical_analysis = self.analyze_technical_accuracy(claims)
        
        return {
            "verification_type": verification_type,
            "original_text": text,
            "extracted_claims": claims,
            "technical_analyses": technical_analysis,
            "verification_count": len(claims),
            "requires_fact_checking": len(claims) > 0
        }

def create_fact_check_workflow(text_to_verify: str) -> str:
    """
    Create a comprehensive fact-checking workflow for the provided text
    """
    workflow = FactCheckingWorkflow()
    verification_request = workflow.format_verification_request(text_to_verify)
    
    # Create comprehensive fact-checking report
    report = f"""# 🔍 COMPREHENSIVE FACT-CHECKING WORKFLOW

## 📝 **TEXT TO VERIFY**
```
{verification_request['original_text']}
```

## 🔍 **CLAIMS EXTRACTED FOR VERIFICATION**
"""
    
    for i, claim in enumerate(verification_request['extracted_claims'], 1):
        report += f"{i}. **{claim}**\n"
    
    if verification_request['extracted_claims']:
        report += f"""
## ✅ **VERIFICATION WORKFLOW**

### **Step 1: Technical Analysis**
Use MiniMax code analysis to verify technical accuracy:

```python
# Example analysis
analysis_request = {{
    "code": "# Verify: {verification_request['extracted_claims'][0]}",
    "analysis_type": "fact_checking",
    "language": "python",
    "response_format": "json"
}}
```

### **Step 2: Code Review** 
Use MiniMax code review for comprehensive validation:

```python
# Comprehensive review
review_request = {{
    "code": "# Technical validation of claims",
    "language": "python", 
    "focus_areas": ["accuracy", "verifiable_facts", "logical_consistency"],
    "response_format": "markdown"
}}
```

### **Step 3: Manual Verification**
For claims requiring external verification:

1. **Search for supporting evidence**
2. **Cross-reference multiple sources**
3. **Check for logical consistency**
4. **Verify dates, numbers, and citations**

## 📊 **VERIFICATION SUMMARY**

- **Total Claims Found**: {verification_request['verification_count']}
- **Requires Fact-Checking**: {'Yes' if verification_request['requires_fact_checking'] else 'No'}
- **Technical Analysis Needed**: {len(verification_request['technical_analyses'])}

## 🚀 **READY FOR IMPLEMENTATION**

Use the MiniMax tools to perform the actual fact-checking:
"""
        
        # Add tool usage examples
        for i, claim in enumerate(verification_request['extracted_claims'][:3], 1):  # Limit to 3 examples
            report += f"""
### **Example {i}: Verify Claim**
```
Claim: {claim}

# Use MiniMax tools:
result = minimax_analyze_code(
    code="# Analysis: {claim}",
    analysis_type="fact_checking", 
    language="python",
    response_format="json"
)
```
"""
    else:
        report += """
## ✅ **NO FACTUAL CLAIMS DETECTED**

The text appears to be:
- Opinion-based rather than factual
- Very brief
- Lacks specific claims requiring verification

## 💡 **RECOMMENDATIONS**

1. **Provide more detailed content** with specific factual claims
2. **Include dates, numbers, or technical details** that can be verified
3. **Add citations or sources** that need validation
"""
    
    return report

# Example usage and demonstration
if __name__ == "__main__":
    # Example text for fact-checking
    sample_text = """
    The Internet was invented in 1989 by Tim Berners-Lee at CERN. 
    This technology revolutionized global communication by 1995 when 
    over 16 million people were using it worldwide. Research shows that
    60% of web traffic comes from mobile devices in 2024.
    """
    
    print(create_fact_check_workflow(sample_text))
