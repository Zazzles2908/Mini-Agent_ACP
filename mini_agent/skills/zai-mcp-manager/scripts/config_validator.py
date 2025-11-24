#!/usr/bin/env python3
"""
Z.AI MCP Configuration Validator - Validate MCP configuration and API setup
"""

import os
import json
import asyncio
import aiohttp
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    """Validation result levels"""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class ValidationIssue:
    """Configuration validation issue"""
    category: str
    item: str
    level: ValidationResult
    message: str
    recommendation: str
    fix_available: bool


@dataclass
class ConfigurationReport:
    """Complete configuration validation report"""
    is_valid: bool
    overall_score: int  # 0-100
    total_issues: int
    issues_by_level: Dict[str, int]
    issues: List[ValidationIssue]
    recommendations: List[str]
    timestamp: str


class ZAIMCPConfigurationValidator:
    """Validate Z.AI MCP configuration and setup"""
    
    def __init__(self):
        # Define required and recommended files
        self.required_files = [
            ".env",
            ".mcp.json"
        ]
        
        self.recommended_files = [
            "mini_agent/config/.mcp.json",
            "mini_agent/config/z_mcp_servers.json"
        ]
        
        # Define expected configuration patterns
        self.expected_patterns = {
            "zai_api_key": {
                "pattern": r"^[A-Za-z0-9\.\-_]+$",
                "min_length": 50,
                "description": "Z.AI API key format"
            },
            "search_endpoint": {
                "pattern": r"https://api\.z\.ai/api/mcp/web_search_prime/mcp",
                "description": "Z.AI web search MCP endpoint"
            },
            "reader_endpoint": {
                "pattern": r"https://api\.z\.ai/api/mcp/web_reader/mcp",
                "description": "Z.AI web reader MCP endpoint"
            }
        }
    
    async def validate_configuration(self) -> ConfigurationReport:
        """Run complete configuration validation"""
        issues = []
        
        # 1. File existence checks
        issues.extend(await self._check_file_existence())
        
        # 2. Environment variable checks
        issues.extend(await self._check_environment_variables())
        
        # 3. MCP configuration validation
        issues.extend(await self._check_mcp_configuration())
        
        # 4. API connectivity checks
        issues.extend(await self._check_api_connectivity())
        
        # 5. Security validation
        issues.extend(await self._check_security_settings())
        
        # 6. Generate recommendations
        recommendations = self._generate_recommendations(issues)
        
        # Calculate overall score and validity
        overall_score = self._calculate_score(issues)
        is_valid = overall_score >= 70  # 70% threshold for "valid"
        
        # Count issues by level
        issues_by_level = {
            "pass": len([i for i in issues if i.level == ValidationResult.PASS]),
            "warning": len([i for i in issues if i.level == ValidationResult.WARNING]),
            "fail": len([i for i in issues if i.level == ValidationResult.FAIL]),
            "error": len([i for i in issues if i.level == ValidationResult.ERROR])
        }
        
        return ConfigurationReport(
            is_valid=is_valid,
            overall_score=overall_score,
            total_issues=len(issues),
            issues_by_level=issues_by_level,
            issues=issues,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    async def _check_file_existence(self) -> List[ValidationIssue]:
        """Check if required files exist"""
        issues = []
        
        # Check required files
        for file_path in self.required_files:
            if not Path(file_path).exists():
                issues.append(ValidationIssue(
                    category="files",
                    item=file_path,
                    level=ValidationResult.FAIL,
                    message=f"Required file missing: {file_path}",
                    recommendation=f"Create {file_path} with proper configuration",
                    fix_available=True
                ))
            else:
                issues.append(ValidationIssue(
                    category="files",
                    item=file_path,
                    level=ValidationResult.PASS,
                    message=f"Required file exists: {file_path}",
                    recommendation=None,
                    fix_available=False
                ))
        
        # Check recommended files
        for file_path in self.recommended_files:
            if not Path(file_path).exists():
                issues.append(ValidationIssue(
                    category="files",
                    item=file_path,
                    level=ValidationResult.WARNING,
                    message=f"Recommended file missing: {file_path}",
                    recommendation=f"Consider adding {file_path} for better organization",
                    fix_available=True
                ))
            else:
                issues.append(ValidationIssue(
                    category="files",
                    item=file_path,
                    level=ValidationResult.PASS,
                    message=f"Recommended file exists: {file_path}",
                    recommendation=None,
                    fix_available=False
                ))
        
        return issues
    
    async def _check_environment_variables(self) -> List[ValidationIssue]:
        """Check environment variable configuration"""
        issues = []
        
        # Check ZAI_API_KEY
        zai_api_key = os.getenv('ZAI_API_KEY')
        if not zai_api_key:
            issues.append(ValidationIssue(
                category="environment",
                item="ZAI_API_KEY",
                level=ValidationResult.ERROR,
                message="ZAI_API_KEY environment variable not found",
                recommendation="Add ZAI_API_KEY to your .env file or environment variables",
                fix_available=True
            ))
        elif not re.match(self.expected_patterns["zai_api_key"]["pattern"], zai_api_key):
            issues.append(ValidationIssue(
                category="environment",
                item="ZAI_API_KEY",
                level=ValidationResult.FAIL,
                message="ZAI_API_KEY format appears invalid",
                recommendation="Verify your Z.AI API key is correct and properly formatted",
                fix_available=True
            ))
        elif len(zai_api_key) < self.expected_patterns["zai_api_key"]["min_length"]:
            issues.append(ValidationIssue(
                category="environment",
                item="ZAI_API_KEY",
                level=ValidationResult.WARNING,
                message="ZAI_API_KEY seems shorter than expected",
                recommendation="Verify your Z.AI API key is complete",
                fix_available=True
            ))
        else:
            issues.append(ValidationIssue(
                category="environment",
                item="ZAI_API_KEY",
                level=ValidationResult.PASS,
                message="ZAI_API_KEY properly configured",
                recommendation=None,
                fix_available=False
            ))
        
        return issues
    
    async def _check_mcp_configuration(self) -> List[ValidationIssue]:
        """Validate MCP configuration files"""
        issues = []
        
        # Check main .mcp.json
        if Path(".mcp.json").exists():
            try:
                with open(".mcp.json", 'r') as f:
                    mcp_config = json.load(f)
                
                # Check for Z.AI MCP servers
                mcp_servers = mcp_config.get("mcpServers", {})
                zai_servers = [name for name in mcp_servers.keys() if 'zai' in name.lower()]
                
                if not zai_servers:
                    issues.append(ValidationIssue(
                        category="configuration",
                        item="mcpServers",
                        level=ValidationResult.WARNING,
                        message="No Z.AI MCP servers found in .mcp.json",
                        recommendation="Consider adding Z.AI MCP server definitions to .mcp.json",
                        fix_available=True
                    ))
                else:
                    for server_name in zai_servers:
                        issues.append(ValidationIssue(
                            category="configuration",
                            item=f"mcpServers.{server_name}",
                            level=ValidationResult.PASS,
                            message=f"Z.AI MCP server configured: {server_name}",
                            recommendation=None,
                            fix_available=False
                        ))
                
            except json.JSONDecodeError:
                issues.append(ValidationIssue(
                    category="configuration",
                    item=".mcp.json",
                    level=ValidationResult.FAIL,
                    message="Invalid JSON in .mcp.json file",
                    recommendation="Fix JSON syntax errors in .mcp.json",
                    fix_available=True
                ))
            except Exception as e:
                issues.append(ValidationIssue(
                    category="configuration",
                    item=".mcp.json",
                    level=ValidationResult.ERROR,
                    message=f"Error reading .mcp.json: {e}",
                    recommendation="Check file permissions and content",
                    fix_available=True
                ))
        
        # Check Z.AI specific configuration
        zai_config_paths = [
            "mini_agent/config/z_mcp_servers.json",
            "mini_agent/config/.mcp.json"
        ]
        
        for config_path in zai_config_paths:
            if Path(config_path).exists():
                try:
                    with open(config_path, 'r') as f:
                        zai_config = json.load(f)
                    
                    mcp_servers = zai_config.get("mcpServers", {})
                    
                    # Check search server
                    search_server = mcp_servers.get("zai-web-search", mcp_servers.get("web-search-prime"))
                    if search_server:
                        url = search_server.get("url", "")
                        if not re.match(self.expected_patterns["search_endpoint"]["pattern"], url):
                            issues.append(ValidationIssue(
                                category="configuration",
                                item=f"{config_path}.zai-web-search.url",
                                level=ValidationResult.FAIL,
                                message="Search endpoint URL incorrect",
                                recommendation="Use: https://api.z.ai/api/mcp/web_search_prime/mcp",
                                fix_available=True
                            ))
                        else:
                            issues.append(ValidationIssue(
                                category="configuration",
                                item=f"{config_path}.zai-web-search.url",
                                level=ValidationResult.PASS,
                                message="Search endpoint URL correct",
                                recommendation=None,
                                fix_available=False
                            ))
                    else:
                        issues.append(ValidationIssue(
                            category="configuration",
                            item=f"{config_path}.zai-web-search",
                            level=ValidationResult.WARNING,
                            message="Z.AI web search server not configured",
                            recommendation="Add zai-web-search MCP server configuration",
                            fix_available=True
                        ))
                    
                    # Check reader server
                    reader_server = mcp_servers.get("zai-web-reader", mcp_servers.get("web-reader"))
                    if reader_server:
                        url = reader_server.get("url", "")
                        if not re.match(self.expected_patterns["reader_endpoint"]["pattern"], url):
                            issues.append(ValidationIssue(
                                category="configuration",
                                item=f"{config_path}.zai-web-reader.url",
                                level=ValidationResult.FAIL,
                                message="Reader endpoint URL incorrect",
                                recommendation="Use: https://api.z.ai/api/mcp/web_reader/mcp",
                                fix_available=True
                            ))
                        else:
                            issues.append(ValidationIssue(
                                category="configuration",
                                item=f"{config_path}.zai-web-reader.url",
                                level=ValidationResult.PASS,
                                message="Reader endpoint URL correct",
                                recommendation=None,
                                fix_available=False
                            ))
                    else:
                        issues.append(ValidationIssue(
                            category="configuration",
                            item=f"{config_path}.zai-web-reader",
                            level=ValidationResult.WARNING,
                            message="Z.AI web reader server not configured",
                            recommendation="Add zai-web-reader MCP server configuration",
                            fix_available=True
                        ))
                
                except Exception as e:
                    issues.append(ValidationIssue(
                        category="configuration",
                        item=config_path,
                        level=ValidationResult.ERROR,
                        message=f"Error reading {config_path}: {e}",
                        recommendation="Check file permissions and JSON syntax",
                        fix_available=True
                    ))
        
        return issues
    
    async def _check_api_connectivity(self) -> List[ValidationIssue]:
        """Test API connectivity"""
        issues = []
        api_key = os.getenv('ZAI_API_KEY')
        
        if not api_key:
            # Skip connectivity tests if no API key
            return [
                ValidationIssue(
                    category="connectivity",
                    item="api_key",
                    level=ValidationResult.ERROR,
                    message="No API key available for connectivity tests",
                    recommendation="Configure ZAI_API_KEY first",
                    fix_available=False
                )
            ]
        
        # Test search endpoint
        search_test = await self._test_endpoint_connectivity(
            "https://api.z.ai/api/mcp/web_search_prime/mcp", 
            api_key, 
            "search"
        )
        issues.extend(search_test)
        
        # Test reader endpoint
        reader_test = await self._test_endpoint_connectivity(
            "https://api.z.ai/api/mcp/web_reader/mcp", 
            api_key, 
            "reader"
        )
        issues.extend(reader_test)
        
        return issues
    
    async def _test_endpoint_connectivity(self, endpoint: str, api_key: str, 
                                        operation_type: str) -> List[ValidationIssue]:
        """Test connectivity to a specific endpoint"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(
                    endpoint,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return [
                            ValidationIssue(
                                category="connectivity",
                                item=f"{operation_type}_endpoint",
                                level=ValidationResult.PASS,
                                message=f"{operation_type.title()} endpoint accessible",
                                recommendation=None,
                                fix_available=False
                            )
                        ]
                    elif response.status == 401:
                        return [
                            ValidationIssue(
                                category="connectivity",
                                item=f"{operation_type}_endpoint",
                                level=ValidationResult.FAIL,
                                message="Authentication failed - API key invalid",
                                recommendation="Check your ZAI_API_KEY validity",
                                fix_available=True
                            )
                        ]
                    elif response.status == 429:
                        return [
                            ValidationIssue(
                                category="connectivity",
                                item=f"{operation_type}_endpoint",
                                level=ValidationResult.WARNING,
                                message="Rate limit exceeded",
                                recommendation="Wait before making requests or check quota",
                                fix_available=False
                            )
                        ]
                    else:
                        return [
                            ValidationIssue(
                                category="connectivity",
                                item=f"{operation_type}_endpoint",
                                level=ValidationResult.FAIL,
                                message=f"HTTP {response.status}: Unexpected response",
                                recommendation="Check Z.AI service status and documentation",
                                fix_available=False
                            )
                        ]
                        
        except asyncio.TimeoutError:
            return [
                ValidationIssue(
                    category="connectivity",
                    item=f"{operation_type}_endpoint",
                    level=ValidationResult.WARNING,
                    message="Connection timeout",
                    recommendation="Check network connectivity and firewall settings",
                    fix_available=False
                )
            ]
        except Exception as e:
            return [
                ValidationIssue(
                    category="connectivity",
                    item=f"{operation_type}_endpoint",
                    level=ValidationResult.ERROR,
                    message=f"Connection error: {str(e)}",
                    recommendation="Check network connectivity and endpoint URL",
                    fix_available=False
                )
            ]
    
    async def _check_security_settings(self) -> List[ValidationIssue]:
        """Check security-related configuration"""
        issues = []
        
        # Check if .env is in .gitignore
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
            if ".env" in gitignore_content:
                issues.append(ValidationIssue(
                    category="security",
                    item=".gitignore",
                    level=ValidationResult.PASS,
                    message=".env properly protected in .gitignore",
                    recommendation=None,
                    fix_available=False
                ))
            else:
                issues.append(ValidationIssue(
                    category="security",
                    item=".gitignore",
                    level=ValidationResult.WARNING,
                    message=".env file not in .gitignore",
                    recommendation="Add .env to .gitignore to prevent API key exposure",
                    fix_available=True
                ))
        else:
            issues.append(ValidationIssue(
                category="security",
                item=".gitignore",
                level=ValidationResult.WARNING,
                message=".gitignore file missing",
                recommendation="Create .gitignore file and add sensitive files",
                fix_available=True
            ))
        
        # Check .env file permissions (best effort on Windows)
        env_path = Path(".env")
        if env_path.exists():
            # On Unix systems, check file permissions
            try:
                import stat
                file_stat = env_path.stat()
                permissions = stat.filemode(file_stat.st_mode)
                
                # Check if file is world-readable (security issue)
                if file_stat.st_mode & stat.S_IROTH:
                    issues.append(ValidationIssue(
                        category="security",
                        item=".env permissions",
                        level=ValidationResult.WARNING,
                        message=".env file is world-readable",
                        recommendation="Restrict .env file permissions to owner only",
                        fix_available=False
                    ))
                else:
                    issues.append(ValidationIssue(
                        category="security",
                        item=".env permissions",
                        level=ValidationResult.PASS,
                        message=".env file permissions appear secure",
                        recommendation=None,
                        fix_available=False
                    ))
            except:
                # Skip permission check on unsupported systems
                pass
        
        return issues
    
    def _generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate actionable recommendations from issues"""
        recommendations = []
        
        # Group issues by category
        error_issues = [i for i in issues if i.level == ValidationResult.ERROR]
        fail_issues = [i for i in issues if i.level == ValidationResult.FAIL]
        warning_issues = [i for i in issues if i.level == ValidationResult.WARNING]
        
        # Critical issues
        if error_issues:
            recommendations.append("🚨 **Critical Issues:** Fix errors before using Z.AI MCP")
            for issue in error_issues:
                recommendations.append(f"- {issue.recommendation}")
        
        # Configuration issues
        if fail_issues:
            recommendations.append("⚠️ **Configuration Issues:** Review failed validations")
            for issue in fail_issues:
                recommendations.append(f"- {issue.recommendation}")
        
        # Recommendations
        if warning_issues:
            recommendations.append("💡 **Best Practice Recommendations:**")
            for issue in warning_issues:
                if issue.fix_available:
                    recommendations.append(f"- {issue.recommendation}")
        
        return recommendations
    
    def _calculate_score(self, issues: List[ValidationIssue]) -> int:
        """Calculate overall configuration score (0-100)"""
        if not issues:
            return 100
        
        # Define weights
        weights = {
            ValidationResult.PASS: 10,
            ValidationResult.WARNING: 5,
            ValidationResult.FAIL: -15,
            ValidationResult.ERROR: -25
        }
        
        total_score = 0
        max_possible_score = 0
        
        for issue in issues:
            max_possible_score += 10  # Maximum score for each issue
            total_score += weights.get(issue.level, -10)
        
        # Ensure score is within bounds
        score = max(0, min(100, total_score))
        return score
    
    def generate_validation_report(self, report: ConfigurationReport) -> str:
        """Generate a formatted validation report"""
        # Status indicator
        if report.is_valid:
            status_emoji = "✅"
            status_text = "VALID"
        else:
            status_emoji = "❌"
            status_text = "INVALID"
        
        report_lines = [
            "# Z.AI MCP Configuration Validation Report",
            "",
            f"**Status:** {status_emoji} {status_text}",
            f"**Score:** {report.overall_score}/100",
            f"**Generated:** {report.timestamp}",
            "",
            "## Summary",
            "",
            f"- **Total Checks:** {report.total_issues}",
            f"- **Passed:** {report.issues_by_level['pass']}",
            f"- **Warnings:** {report.issues_by_level['warning']}",
            f"- **Failed:** {report.issues_by_level['fail']}",
            f"- **Errors:** {report.issues_by_level['error']}",
            "",
            "## Issues by Category",
            ""
        ]
        
        # Group issues by category
        categories = {}
        for issue in report.issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue)
        
        for category, category_issues in categories.items():
            report_lines.append(f"### {category.title()}")
            
            for issue in category_issues:
                level_emoji = {
                    ValidationResult.PASS: "✅",
                    ValidationResult.WARNING: "⚠️",
                    ValidationResult.FAIL: "❌",
                    ValidationResult.ERROR: "🚨"
                }.get(issue.level, "❓")
                
                report_lines.extend([
                    f"- **{level_emoji} {issue.item}:** {issue.message}",
                    ""
                ])
            
            report_lines.append("")
        
        # Add recommendations
        if report.recommendations:
            report_lines.extend([
                "## Recommendations",
                ""
            ])
            
            for recommendation in report.recommendations:
                report_lines.append(f"{recommendation}")
                report_lines.append("")
        
        # Add next steps
        if report.is_valid:
            report_lines.extend([
                "## Next Steps",
                "",
                "🎉 **Configuration is valid!** You can now:",
                "- Start using Z.AI MCP tools",
                "- Monitor quota usage",
                "- Set up health checks",
                "- Configure alerting",
                ""
            ])
        else:
            report_lines.extend([
                "## Next Steps",
                "",
                "🔧 **Fix configuration issues before proceeding:**",
                "- Address all ERROR and FAIL level issues",
                "- Review configuration files",
                "- Test API connectivity",
                "- Re-run validation",
                ""
            ])
        
        return "\n".join(report_lines)


async def main():
    """Main function for CLI usage"""
    try:
        validator = ZAIMCPConfigurationValidator()
        report = await validator.validate_configuration()
        formatted_report = validator.generate_validation_report(report)
        print(formatted_report)
        
        # Save detailed JSON report
        results_file = f"config_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert enum values to strings for JSON serialization
        report_dict = {
            "is_valid": report.is_valid,
            "overall_score": report.overall_score,
            "total_issues": report.total_issues,
            "issues_by_level": report.issues_by_level,
            "issues": [
                {
                    "category": issue.category,
                    "item": issue.item,
                    "level": issue.level.value,
                    "message": issue.message,
                    "recommendation": issue.recommendation,
                    "fix_available": issue.fix_available
                }
                for issue in report.issues
            ],
            "recommendations": report.recommendations,
            "timestamp": report.timestamp
        }
        
        with open(results_file, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        print(f"\nDetailed results saved to: {results_file}")
        
        # Exit with appropriate code
        if report.is_valid:
            exit(0)
        else:
            exit(1)
            
    except Exception as e:
        print(f"Error running configuration validation: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
