#!/usr/bin/env python3
"""
Z.AI Token Truncation Detector
Detects and handles token truncation in Z.AI API responses
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class TruncationType(Enum):
    """Types of response truncation"""
    TOKEN_LIMIT = "token_limit"
    LENGTH_TRUNCATION = "length_truncation"
    INCOMPLETE_RESPONSE = "incomplete_response"
    NO_TRUNCATION = "no_truncation"


@dataclass
class TruncationResult:
    """Token truncation detection result"""
    is_truncated: bool
    truncation_type: TruncationType
    finish_reason: Optional[str]
    truncation_message: str
    recommendations: list[str]
    severity: str  # 'info', 'warning', 'critical'


class ZAITokenTruncationDetector:
    """Detect and handle token truncation in Z.AI API responses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def detect_truncation(self, response_data: Dict[str, Any]) -> TruncationResult:
        """Detect truncation in Z.AI API response"""
        
        # Check for explicit finish reasons
        finish_reason = self._extract_finish_reason(response_data)
        
        if finish_reason == "length":
            return TruncationResult(
                is_truncated=True,
                truncation_type=TruncationType.TOKEN_LIMIT,
                finish_reason=finish_reason,
                truncation_message="Response truncated due to token limits",
                recommendations=[
                    "Use shorter queries to reduce response size",
                    "Implement pagination for large results",
                    "Consider using 'concise' mode for summaries",
                    "Split complex requests into multiple smaller requests"
                ],
                severity="warning"
            )
        
        elif finish_reason == "stop":
            # Check if response seems incomplete
            if self._response_seems_incomplete(response_data):
                return TruncationResult(
                    is_truncated=True,
                    truncation_type=TruncationType.INCOMPLETE_RESPONSE,
                    finish_reason=finish_reason,
                    truncation_message="Response appears incomplete despite normal finish",
                    recommendations=[
                        "Retry the request with a simpler query",
                        "Check for timeout issues",
                        "Verify API response format"
                    ],
                    severity="info"
                )
        
        # Check for structural truncation
        truncation_indicators = self._check_structural_truncation(response_data)
        if truncation_indicators["detected"]:
            return TruncationResult(
                is_truncated=True,
                truncation_type=TruncationType.LENGTH_TRUNCATION,
                finish_reason=finish_reason,
                truncation_message="Response structure indicates truncation",
                recommendations=truncation_indicators["recommendations"],
                severity=truncation_indicators["severity"]
            )
        
        return TruncationResult(
            is_truncated=False,
            truncation_type=TruncationType.NO_TRUNCATION,
            finish_reason=finish_reason,
            truncation_message="No truncation detected",
            recommendations=["Response appears complete"],
            severity="info"
        )
    
    def _extract_finish_reason(self, response_data: Dict[str, Any]) -> Optional[str]:
        """Extract finish_reason from response"""
        
        # Check for GLM-style response
        if "choices" in response_data and response_data["choices"]:
            choice = response_data["choices"][0]
            if "finish_reason" in choice:
                return choice["finish_reason"]
        
        # Check for MCP-style response
        if "result" in response_data:
            result = response_data["result"]
            if isinstance(result, dict) and "finish_reason" in result:
                return result["finish_reason"]
        
        # Check for direct finish_reason
        if "finish_reason" in response_data:
            return response_data["finish_reason"]
        
        return None
    
    def _response_seems_incomplete(self, response_data: Dict[str, Any]) -> bool:
        """Check if response appears incomplete despite normal finish"""
        
        # Check for unusually short content
        content = self._extract_content(response_data)
        if content and len(content) < 50:
            return True
        
        # Check for missing expected fields
        if "choices" in response_data:
            choice = response_data["choices"][0]
            if "message" in choice and choice["message"]:
                message_content = choice["message"].get("content", "")
                if not message_content.strip():
                    return True
        
        return False
    
    def _check_structural_truncation(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for structural indicators of truncation"""
        
        # Check if content ends abruptly
        content = self._extract_content(response_data)
        if content:
            # Look for truncated sentences (ending mid-word or mid-sentence)
            if content.strip() and not content.strip().endswith(('.', '!', '?', '...')):
                # Check for abrupt endings
                last_chars = content.strip()[-10:]
                if not last_chars.endswith((' ', '.', '!', '?')):
                    return {
                        "detected": True,
                        "severity": "info",
                        "recommendations": [
                            "Response may be truncated at sentence boundary",
                            "Consider using response_format='concise' for shorter output"
                        ]
                    }
        
        # Check for incomplete JSON structures
        content_str = json.dumps(response_data)
        if content_str.endswith(('...', '...}')):
            return {
                "detected": True,
                "severity": "warning",
                "recommendations": [
                    "JSON response appears truncated",
                    "Retry with reduced scope or use pagination"
                ]
            }
        
        return {"detected": False}
    
    def _extract_content(self, response_data: Dict[str, Any]) -> str:
        """Extract main content from response"""
        
        # GLM-style responses
        if "choices" in response_data:
            choice = response_data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
        
        # MCP-style responses
        if "result" in response_data:
            result = response_data["result"]
            if "content" in result:
                if isinstance(result["content"], list) and result["content"]:
                    return result["content"][0].get("text", "")
                else:
                    return str(result["content"])
        
        return ""
    
    def format_truncation_warning(self, result: TruncationResult) -> str:
        """Format truncation warning for user display"""
        
        severity_icons = {
            "info": "ℹ️",
            "warning": "⚠️", 
            "critical": "🚨"
        }
        
        icon = severity_icons.get(result.severity, "ℹ️")
        
        warning_lines = [
            f"{icon} **Response Truncation Detected**",
            "",
            f"**Type:** {result.truncation_type.value.replace('_', ' ').title()}",
            f"**Finish Reason:** {result.finish_reason or 'Unknown'}",
            "",
            f"**Issue:** {result.truncation_message}",
            "",
            "**Recommendations:**"
        ]
        
        for i, rec in enumerate(result.recommendations, 1):
            warning_lines.append(f"{i}. {rec}")
        
        warning_lines.append("")
        warning_lines.append("*This indicates the response was cut off due to token limits or response size constraints.*")
        
        return "\n".join(warning_lines)


class ZAIResponseEnhancer:
    """Enhanced response handling with truncation detection"""
    
    def __init__(self):
        self.detector = ZAITokenTruncationDetector()
        self.logger = logging.getLogger(__name__)
    
    def enhance_response(self, response_data: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Enhance response with truncation detection and warnings"""
        
        # Detect truncation
        truncation_result = self.detector.detect_truncation(response_data)
        
        enhanced_response = {
            "original_response": response_data,
            "truncation_analysis": {
                "is_truncated": truncation_result.is_truncated,
                "truncation_type": truncation_result.truncation_type.value,
                "severity": truncation_result.severity,
                "finish_reason": truncation_result.finish_reason
            },
            "enhanced_data": response_data.copy(),
            "warnings": [],
            "recommendations": truncation_result.recommendations
        }
        
        # Add truncation warning if detected
        if truncation_result.is_truncated:
            warning_message = self.detector.format_truncation_warning(truncation_result)
            enhanced_response["warnings"].append(warning_message)
            enhanced_response["enhanced_data"]["truncation_warning"] = warning_message
            
            self.logger.warning(f"Token truncation detected: {truncation_result.truncation_message}")
        
        # Add context about what was truncated
        if truncation_result.is_truncated:
            content = self.detector._extract_content(response_data)
            if content:
                enhanced_response["truncation_analysis"]["original_content_length"] = len(content)
                enhanced_response["truncation_analysis"]["content_snippet"] = content[-100:] + "..." if len(content) > 100 else content
        
        return enhanced_response
    
    def suggest_optimization(self, truncation_result: TruncationResult, query: str) -> str:
        """Suggest query optimization based on truncation"""
        
        suggestions = []
        
        if truncation_result.truncation_type == TruncationType.TOKEN_LIMIT:
            suggestions.extend([
                "**Query Optimization Suggestions:**",
                "",
                "1. **Shorten your query:**",
                f"   Current: '{query}'",
                "   Try: 'Python vs JavaScript' instead of 'detailed comparison of Python and JavaScript programming languages'",
                "",
                "2. **Use specific terms:**",
                "   Replace: 'latest trends in web development'",
                "   With: 'web dev trends 2024'",
                "",
                "3. **Request concise responses:**",
                "   Add: 'Provide a brief summary' or 'Give me the key points only'",
                "",
                "4. **Break into multiple queries:**",
                "   Instead of: 'Explain web development, mobile apps, and AI'",
                "   Try: 'What are web development trends?' then 'What are mobile app trends?'"
            ])
        
        elif truncation_result.truncation_type == TruncationType.INCOMPLETE_RESPONSE:
            suggestions.extend([
                "**Response Completion Suggestions:**",
                "",
                "1. **Retry the request:**",
                "   The response may have been interrupted",
                "",
                "2. **Simplify your query:**",
                "   Try a more focused version of your original question",
                "",
                "3. **Check network connectivity:**",
                "   Timeout issues can cause incomplete responses"
            ])
        
        return "\n".join(suggestions)


def demo_truncation_detection():
    """Demonstrate truncation detection with examples"""
    
    detector = ZAITokenTruncationDetector()
    enhancer = ZAIResponseEnhancer()
    
    # Example 1: Token limit truncation
    truncated_response = {
        "choices": [{
            "finish_reason": "length",
            "index": 0,
            "message": {
                "content": "Python is a high-level programming language that is designed to be easy to read and write. It has a large and active community of developers, and is used in many different areas including web development, data science, artificial intelligence, scientific computing, and more. One of the key features of Python is its emphasis on code readability and simplicity. Python code uses significant whitespace to indicate code blocks, which makes it visually clear and helps developers identify the structure of their code at a glance. The language also has a rich standard library that provides modules for many common tasks such as file I/O, networking, and regular expressions. Additionally, Python has a large ecosystem of third-party packages that extend its functionality even further, making it suitable for a wide range of applications.\n\n## Key Features of Python\n\nPython is a dynamically typed language, which means that variables do not need to be declared with specific types, and the type checking is done at runtime. This can make code more flexible and easier to write, but can also lead to runtime errors if not careful.\n\n## Python in Web Development\n\nPython is widely used in web development, with frameworks such as Django and Flask providing powerful tools for building web applications. Django is a full-featured framework that includes everything needed for web development, including an ORM (Object-Relational Mapper) for database access, templating engines, and built-in admin interfaces. Flask, on the other hand, is a microframework that provides only the essentials, allowing developers to build lightweight and flexible web applications.\n\n## Data Science and Machine Learning\n\nPython has become the go-to language for data science and machine learning, with libraries such as NumPy, Pandas, and scikit-learn providing powerful tools for data manipulation and analysis. These libraries make it easy to work with large datasets, perform statistical analysis, and build machine learning models.\n\n## Scientific Computing\n\nPython is also widely used in scientific computing, with libraries such as SciPy and Matplotlib providing tools for scientific calculations, data visualization, and more. These libraries make it easy to perform complex calculations and create professional-quality plots and graphs."
            }
        }]
    }
    
    # Example 2: Normal response
    normal_response = {
        "choices": [{
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "Python is a popular programming language known for its simplicity and readability."
            }
        }]
    }
    
    print("=== Z.AI TRUNCATION DETECTION DEMO ===\n")
    
    # Test truncated response
    print("1. Testing Token-Limited Response:")
    print("-" * 40)
    truncation_result = detector.detect_truncation(truncated_response)
    print(detector.format_truncation_warning(truncation_result))
    print()
    
    enhanced_response = enhancer.enhance_response(truncated_response, "Explain Python programming")
    print("Enhanced Response Warnings:")
    for warning in enhanced_response["warnings"]:
        print(warning)
    print()
    
    # Test normal response
    print("2. Testing Normal Response:")
    print("-" * 40)
    truncation_result = detector.detect_truncation(normal_response)
    print(detector.format_truncation_warning(truncation_result))
    print()


if __name__ == "__main__":
    demo_truncation_detection()
