#!/usr/bin/env python3
"""
Quick Validation Tool

A simple CLI tool for rapid fact-checking and validation
of AI outputs and implementations.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import our fact-checking modules
sys.path.append(str(Path(__file__).parent))
from fact_checker import FactChecker, FunctionalTester, SelfAssessor

def validate_text_facts(text: str, min_sources: int = 3) -> Dict[str, Any]:
    """Quick fact-checking of text content"""
    fact_checker = FactChecker()
    
    # Extract claims
    claims = fact_checker.extract_claims(text)
    
    if not claims:
        return {
            "status": "no_claims_found",
            "claims": [],
            "summary": "No factual claims detected in text"
        }
    
    # Verify each claim
    results = []
    for claim in claims:
        result = fact_checker.verify_claim(claim, min_sources)
        results.append({
            "claim": claim,
            "status": result.status.value,
            "confidence": result.confidence,
            "sources_count": len(result.sources)
        })
    
    # Calculate summary statistics
    total_claims = len(results)
    verified = sum(1 for r in results if r["status"] == "verified")
    partial = sum(1 for r in results if r["status"] == "partial")
    unverified = sum(1 for r in results if r["status"] == "unverified")
    
    overall_confidence = sum(r["confidence"] for r in results) / total_claims if total_claims else 0
    
    return {
        "status": "completed",
        "claims": results,
        "summary": {
            "total_claims": total_claims,
            "verified": verified,
            "partial": partial,
            "unverified": unverified,
            "overall_confidence": overall_confidence
        }
    }

def validate_files(files: List[str]) -> Dict[str, Any]:
    """Quick validation of files"""
    tester = FunctionalTester()
    
    results = {
        "files_checked": len(files),
        "existing_files": 0,
        "missing_files": 0,
        "syntax_valid": 0,
        "syntax_errors": 0,
        "details": []
    }
    
    for file_path in files:
        file_info = {"path": file_path, "status": "unknown"}
        
        # Check file existence
        if Path(file_path).exists():
            results["existing_files"] += 1
            file_info["exists"] = True
            
            # Check syntax for code files
            if file_path.endswith('.py'):
                syntax_result = tester.test_code_syntax(file_path)
                if syntax_result.passed:
                    results["syntax_valid"] += 1
                    file_info["syntax"] = "valid"
                else:
                    results["syntax_errors"] += 1
                    file_info["syntax"] = f"error: {syntax_result.details}"
        else:
            results["missing_files"] += 1
            file_info["exists"] = False
        
        results["details"].append(file_info)
    
    return results

def assess_quick(task_description: str, output_text: str = None, files: List[str] = None) -> Dict[str, Any]:
    """Quick overall assessment"""
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "task": task_description,
        "text_validation": None,
        "file_validation": None,
        "recommendations": []
    }
    
    # Validate text if provided
    if output_text:
        text_result = validate_text_facts(output_text)
        assessment["text_validation"] = text_result
        
        if text_result["status"] == "completed":
            if text_result["summary"]["overall_confidence"] < 0.7:
                assessment["recommendations"].append("🔍 Some claims need additional verification")
            if text_result["summary"]["unverified"] > 0:
                assessment["recommendations"].append("❌ Several claims remain unverified")
    
    # Validate files if provided
    if files:
        file_result = validate_files(files)
        assessment["file_validation"] = file_result
        
        if file_result["missing_files"] > 0:
            assessment["recommendations"].append(f"📁 {file_result['missing_files']} files are missing")
        if file_result["syntax_errors"] > 0:
            assessment["recommendations"].append(f"🐛 {file_result['syntax_errors']} files have syntax errors")
    
    # Overall recommendation
    if not assessment["recommendations"]:
        if output_text and files:
            text_conf = assessment["text_validation"]["summary"]["overall_confidence"]
            if text_conf > 0.8 and file_result["missing_files"] == 0 and file_result["syntax_errors"] == 0:
                assessment["recommendations"].append("✅ Assessment looks good!")
        else:
            assessment["recommendations"].append("✅ No major issues detected")
    
    return assessment

def print_results(results: Dict[str, Any], format_type: str = "text") -> None:
    """Print validation results in specified format"""
    
    if format_type == "json":
        print(json.dumps(results, indent=2))
        return
    
    # Text format
    if "text_validation" in results:
        text_val = results["text_validation"]
        print("\n📚 TEXT VALIDATION")
        print("=" * 50)
        
        if text_val["status"] == "no_claims_found":
            print("ℹ️  No factual claims detected in text")
        else:
            summary = text_val["summary"]
            print(f"Claims analyzed: {summary['total_claims']}")
            print(f"✅ Verified: {summary['verified']}")
            print(f"⚠️  Partial: {summary['partial']}")
            print(f"❌ Unverified: {summary['unverified']}")
            print(f"Overall confidence: {summary['overall_confidence']:.1%}")
    
    if "file_validation" in results:
        file_val = results["file_validation"]
        print("\n📁 FILE VALIDATION")
        print("=" * 50)
        print(f"Files checked: {file_val['files_checked']}")
        print(f"✅ Existing: {file_val['existing_files']}")
        print(f"❌ Missing: {file_val['missing_files']}")
        print(f"✅ Valid syntax: {file_val['syntax_valid']}")
        print(f"🐛 Syntax errors: {file_val['syntax_errors']}")
    
    if "recommendations" in results and results["recommendations"]:
        print("\n💡 RECOMMENDATIONS")
        print("=" * 50)
        for rec in results["recommendations"]:
            print(f"  {rec}")

def main():
    parser = argparse.ArgumentParser(description="Quick validation tool for AI outputs")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Text validation command
    text_parser = subparsers.add_parser("text", help="Validate facts in text")
    text_parser.add_argument("text", help="Text to validate")
    text_parser.add_argument("--sources", type=int, default=3, help="Minimum sources per claim")
    
    # File validation command
    file_parser = subparsers.add_parser("files", help="Validate files")
    file_parser.add_argument("files", nargs="+", help="Files to validate")
    
    # Quick assessment command
    assess_parser = subparsers.add_parser("assess", help="Quick overall assessment")
    assess_parser.add_argument("task", help="Task description")
    assess_parser.add_argument("--text", help="Output text to validate")
    assess_parser.add_argument("--files", nargs="+", help="Files to validate")
    
    # Output format
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Save results to file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute validation
    if args.command == "text":
        results = validate_text_facts(args.text, args.sources)
    elif args.command == "files":
        results = validate_files(args.files)
    elif args.command == "assess":
        results = assess_quick(args.task, args.text, args.files)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == "json":
                json.dump(results, f, indent=2)
            else:
                # Save text format
                import io
                import contextlib
        
        # Capture text output
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            print_results(results, "text")
        
        with open(args.output, 'w') as f:
            f.write(output_buffer.getvalue())
        print(f"\n📄 Results saved to: {args.output}")
    else:
        print_results(results, args.format)

if __name__ == "__main__":
    main()