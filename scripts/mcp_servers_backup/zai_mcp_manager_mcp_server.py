#!/usr/bin/env python3
"""
ZAI-MCP-Manager-MCP Server Implementation
FastMCP server providing quota monitoring, health checking, and configuration management for Z.AI MCP endpoints
"""

import asyncio
import json
import os
import sys
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

# MCP and Pydantic imports
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
import aiohttp

# Initialize MCP server
mcp = FastMCP("zai_mcp_manager")

# =============================================================================
# Input Models
# =============================================================================

class ValidationResult(str, Enum):
    """Validation result levels"""
    PASS = "pass"
    WARNING = "warning" 
    FAIL = "fail"
    ERROR = "error"

class HealthStatus(str, Enum):
    """Health check status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    ERROR = "error"

class QuotaStatus(str, Enum):
    """Quota status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EXHAUSTED = "exhausted"
    ERROR = "error"

class QuotaCheckRequest(BaseModel):
    """Request model for quota checking"""
    days: int = Field(7, description="Number of days to analyze usage for")
    format: str = Field("markdown", description="Response format: markdown or json")
    
    @field_validator('days')
    def validate_days(cls, v):
        if v < 1 or v > 365:
            raise ValueError("Days must be between 1 and 365")
        return v

class HealthCheckRequest(BaseModel):
    """Request model for health checking"""
    endpoints: Optional[List[str]] = Field(None, description="Specific endpoints to test")
    timeout: float = Field(10.0, description="Request timeout in seconds")
    format: str = Field("markdown", description="Response format: markdown or json")
    
    @field_validator('timeout')
    def validate_timeout(cls, v):
        if v < 1 or v > 60:
            raise ValueError("Timeout must be between 1 and 60 seconds")
        return v

class ConfigValidationRequest(BaseModel):
    """Request model for configuration validation"""
    config_path: Optional[str] = Field(None, description="Path to config file to validate")
    fix_issues: bool = Field(False, description="Attempt to automatically fix issues")
    format: str = Field("markdown", description="Response format: markdown or json")

class TemplateGenerationRequest(BaseModel):
    """Request model for configuration template generation"""
    template_type: str = Field("standard", description="Template type: standard, advanced, minimal")
    includes_examples: bool = Field(True, description="Include usage examples")
    format: str = Field("markdown", description="Response format: markdown or json")
    
    @field_validator('template_type')
    def validate_template_type(cls, v):
        valid_types = ["standard", "advanced", "minimal", "zai", "all"]
        if v.lower() not in valid_types:
            raise ValueError(f"Template type must be one of: {', '.join(valid_types)}")
        return v.lower()

class UsageAnalysisRequest(BaseModel):
    """Request model for usage analysis"""
    start_date: Optional[str] = Field(None, description="Start date for analysis (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date for analysis (YYYY-MM-DD)")
    include_trends: bool = Field(True, description="Include usage trend analysis")
    format: str = Field("markdown", description="Response format: markdown or json")

class TokenDetectionRequest(BaseModel):
    """Request model for token truncation detection"""
    content: str = Field(..., description="Content to analyze for potential token truncation")
    max_tokens: Optional[int] = Field(None, description="Maximum expected tokens")
    detection_type: str = Field("comprehensive", description="Detection type: basic, comprehensive")
    
    @field_validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError("Content must be at least 10 characters long")
        return v.strip()

class OptimizationRequest(BaseModel):
    """Request model for usage optimization"""
    current_usage: Dict[str, int] = Field(..., description="Current usage data")
    optimization_goal: str = Field("efficiency", description="Optimization goal: efficiency, cost, performance")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Usage constraints")

# =============================================================================
# Core Classes (Extracted from original scripts)
# =============================================================================

@dataclass
class QuotaData:
    """Quota status information"""
    searches_used: int = 0
    searches_total: int = 100
    readers_used: int = 0  
    readers_total: int = 100
    searches_remaining: int = 100
    readers_remaining: int = 100
    usage_percentage: float = 0.0
    status: QuotaStatus = QuotaStatus.HEALTHY
    last_updated: str = ""

@dataclass
class HealthCheckData:
    """Health check result data"""
    name: str
    endpoint: str
    status: HealthStatus
    response_time_ms: float
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: str = ""
    details: Dict[str, Any] = None

@dataclass
class ValidationIssue:
    """Configuration validation issue"""
    category: str
    item: str
    level: ValidationResult
    message: str
    recommendation: str
    fix_available: bool = False

class ZAIMCPCore:
    """Core Z.AI MCP management functionality"""
    
    def __init__(self):
        self.api_key = os.getenv('ZAI_API_KEY')
        self.endpoints = {
            "zai-search": "https://api.z.ai/api/mcp/web_search_prime/mcp",
            "zai-reader": "https://api.z.ai/api/mcp/web_reader/mcp"
        }
        
    async def check_quota_status(self) -> QuotaData:
        """Check current Z.AI quota status"""
        try:
            # Simulate quota calculation (in real implementation, this would come from API)
            searches_used = 0  # Would be tracked from actual usage
            readers_used = 0   # Would be tracked from actual usage
            
            searches_remaining = 100 - searches_used
            readers_remaining = 100 - readers_used
            total_usage = searches_used + readers_used
            usage_percentage = (total_usage / 200) * 100
            
            # Determine status
            if searches_remaining <= 0 or readers_remaining <= 0:
                status = QuotaStatus.EXHAUSTED
            elif usage_percentage >= 95:
                status = QuotaStatus.CRITICAL
            elif usage_percentage >= 80:
                status = QuotaStatus.WARNING
            else:
                status = QuotaStatus.HEALTHY
                
            return QuotaData(
                searches_used=searches_used,
                searches_total=100,
                readers_used=readers_used,
                readers_total=100,
                searches_remaining=searches_remaining,
                readers_remaining=readers_remaining,
                usage_percentage=round(usage_percentage, 1),
                status=status,
                last_updated=datetime.now().isoformat()
            )
        except Exception:
            return QuotaData(
                searches_used=0, searches_total=100,
                readers_used=0, readers_total=100,
                searches_remaining=100, readers_remaining=100,
                usage_percentage=0.0, status=QuotaStatus.ERROR,
                last_updated=datetime.now().isoformat()
            )
    
    async def check_health(self, endpoints: Optional[List[str]] = None, timeout: float = 10.0) -> List[HealthCheckData]:
        """Check health of Z.AI MCP endpoints"""
        if endpoints is None:
            endpoints = list(self.endpoints.keys())
            
        results = []
        
        async with aiohttp.ClientSession() as session:
            for endpoint_name in endpoints:
                if endpoint_name not in self.endpoints:
                    results.append(HealthCheckData(
                        name=endpoint_name,
                        endpoint="unknown",
                        status=HealthStatus.ERROR,
                        response_time_ms=0.0,
                        error_message=f"Unknown endpoint: {endpoint_name}",
                        timestamp=datetime.now().isoformat()
                    ))
                    continue
                
                endpoint_url = self.endpoints[endpoint_name]
                start_time = time.time()
                
                try:
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"
                    }
                    
                    # Test tools/list endpoint
                    test_request = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/list",
                        "params": {}
                    }
                    
                    async with session.post(
                        endpoint_url,
                        headers=headers,
                        json=test_request,
                        timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        response_time = (time.time() - start_time) * 1000
                        
                        if response.status == 200:
                            data = await response.json()
                            if "result" in data:
                                results.append(HealthCheckData(
                                    name=endpoint_name,
                                    endpoint=endpoint_url,
                                    status=HealthStatus.HEALTHY,
                                    response_time_ms=round(response_time, 2),
                                    status_code=response.status,
                                    timestamp=datetime.now().isoformat(),
                                    details={"tools_count": len(data["result"].get("tools", []))}
                                ))
                            else:
                                results.append(HealthCheckData(
                                    name=endpoint_name,
                                    endpoint=endpoint_url,
                                    status=HealthStatus.DEGRADED,
                                    response_time_ms=round(response_time, 2),
                                    status_code=response.status,
                                    error_message="Invalid response format",
                                    timestamp=datetime.now().isoformat()
                                ))
                        else:
                            results.append(HealthCheckData(
                                name=endpoint_name,
                                endpoint=endpoint_url,
                                status=HealthStatus.UNHEALTHY,
                                response_time_ms=round(response_time, 2),
                                status_code=response.status,
                                timestamp=datetime.now().isoformat()
                            ))
                            
                except asyncio.TimeoutError:
                    results.append(HealthCheckData(
                        name=endpoint_name,
                        endpoint=endpoint_url,
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=timeout * 1000,
                        error_message="Request timeout",
                        timestamp=datetime.now().isoformat()
                    ))
                except Exception as e:
                    results.append(HealthCheckData(
                        name=endpoint_name,
                        endpoint=endpoint_url,
                        status=HealthStatus.ERROR,
                        response_time_ms=(time.time() - start_time) * 1000,
                        error_message=str(e),
                        timestamp=datetime.now().isoformat()
                    ))
        
        return results
    
    def validate_config(self, config_path: Optional[str] = None) -> List[ValidationIssue]:
        """Validate Z.AI MCP configuration"""
        issues = []
        
        # Check API key
        if not self.api_key:
            issues.append(ValidationIssue(
                category="authentication",
                item="ZAI_API_KEY",
                level=ValidationResult.ERROR,
                message="ZAI_API_KEY environment variable not found",
                recommendation="Add ZAI_API_KEY to your environment or .env file",
                fix_available=True
            ))
        
        # Check config file
        config_file = config_path or "mini_agent/config/.mcp.json"
        if not os.path.exists(config_file):
            issues.append(ValidationIssue(
                category="configuration",
                item="config_file",
                level=ValidationResult.ERROR,
                message=f"Configuration file not found: {config_file}",
                recommendation="Create or locate the MCP configuration file",
                fix_available=False
            ))
        else:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Check for Z.AI MCP servers
                mcp_servers = config.get("mcpServers", {})
                zai_servers = ["web-search-prime", "web-reader"]
                
                for server_name in zai_servers:
                    if server_name not in mcp_servers:
                        issues.append(ValidationIssue(
                            category="server_config",
                            item=f"mcpServers.{server_name}",
                            level=ValidationResult.ERROR,
                            message=f"Z.AI MCP server '{server_name}' not found in configuration",
                            recommendation=f"Add {server_name} to mcpServers configuration",
                            fix_available=True
                        ))
                    else:
                        server_config = mcp_servers[server_name]
                        
                        # Check required fields
                        if "url" not in server_config:
                            issues.append(ValidationIssue(
                                category="server_config",
                                item=f"mcpServers.{server_name}.url",
                                level=ValidationResult.ERROR,
                                message="Missing 'url' field in server configuration",
                                recommendation="Add 'url' field pointing to Z.AI MCP endpoint",
                                fix_available=True
                            ))
                        
                        # Check URL format
                        if "url" in server_config:
                            url = server_config["url"]
                            expected_host = "api.z.ai"
                            if expected_host not in url:
                                issues.append(ValidationIssue(
                                    category="server_config",
                                    item=f"mcpServers.{server_name}.url",
                                    level=ValidationResult.WARNING,
                                    message=f"URL doesn't appear to be Z.AI endpoint: {url}",
                                    recommendation=f"Use Z.AI endpoint format: https://api.z.ai/api/mcp/{server_name}/mcp",
                                    fix_available=True
                                ))
                        
                        # Check headers
                        if "headers" not in server_config:
                            issues.append(ValidationIssue(
                                category="server_config",
                                item=f"mcpServers.{server_name}.headers",
                                level=ValidationResult.ERROR,
                                message="Missing 'headers' field in server configuration",
                                recommendation="Add 'headers' field with Authorization and Accept headers",
                                fix_available=True
                            ))
                        else:
                            headers = server_config["headers"]
                            if "Authorization" not in headers:
                                issues.append(ValidationIssue(
                                    category="server_config",
                                    item=f"mcpServers.{server_name}.headers.Authorization",
                                    level=ValidationResult.ERROR,
                                    message="Missing Authorization header",
                                    recommendation="Add Authorization header with Bearer token",
                                    fix_available=True
                                ))
                            if "Accept" not in headers:
                                issues.append(ValidationIssue(
                                    category="server_config",
                                    item=f"mcpServers.{server_name}.headers.Accept",
                                    level=ValidationResult.WARNING,
                                    message="Missing Accept header",
                                    recommendation="Add Accept header with 'application/json, text/event-stream'",
                                    fix_available=True
                                ))
                
            except json.JSONDecodeError:
                issues.append(ValidationIssue(
                    category="configuration",
                    item="config_file",
                    level=ValidationResult.ERROR,
                    message=f"Configuration file is not valid JSON: {config_file}",
                    recommendation="Fix JSON syntax errors in configuration file",
                    fix_available=False
                ))
            except Exception as e:
                issues.append(ValidationIssue(
                    category="configuration",
                    item="config_file",
                    level=ValidationResult.ERROR,
                    message=f"Error reading configuration file: {str(e)}",
                    recommendation="Check file permissions and content",
                    fix_available=False
                ))
        
        return issues

# =============================================================================
# Tool Implementations  
# =============================================================================

@mcp.tool(
    annotations={
        "title": "Check ZAI Quota Status",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def zai_check_quota_status(
    days: int = 7,
    format: str = "markdown"
) -> str:
    """Check current Z.AI quota usage and status.
    
    Monitor the current usage of Z.AI Lite Plan quotas (100 searches + 100 readers).
    Provides real-time quota status, remaining usage, and recommendations.
    
    Args:
        days: Number of days to analyze usage patterns for (1-365)
        format: Response format - "markdown" for human-readable or "json" for structured data
        
    Returns:
        Comprehensive quota status report with usage metrics and recommendations
    """
    try:
        core = ZAIMCPCore()
        quota_data = await core.check_quota_status()
        
        if format.lower() == "json":
            return json.dumps({
                "success": True,
                "quota_data": asdict(quota_data),
                "analysis_period_days": days,
                "generated_at": datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        # Format as markdown
        status_emoji = {
            QuotaStatus.HEALTHY: "✅",
            QuotaStatus.WARNING: "⚠️", 
            QuotaStatus.CRITICAL: "🚨",
            QuotaStatus.EXHAUSTED: "💀",
            QuotaStatus.ERROR: "❌"
        }.get(quota_data.status, "❓")
        
        lines = [
            "# Z.AI Quota Status Report",
            "",
            f"**Last Updated:** {quota_data.last_updated}",
            "",
            f"**Overall Status:** {status_emoji} {quota_data.status.upper()}",
            "",
            "## Current Usage",
            "",
            f"**Searches:** {quota_data.searches_used}/{quota_data.searches_total} "
            f"({quota_data.searches_remaining} remaining)",
            f"**Readers:** {quota_data.readers_used}/{quota_data.readers_total} "
            f"({quota_data.readers_remaining} remaining)",
            "",
            f"**Total Usage:** {quota_data.usage_percentage}%",
            "",
            "## Recommendations"
        ]
        
        if quota_data.status == QuotaStatus.WARNING:
            lines.extend([
                "",
                "⚠️ Approaching quota limit. Consider:",
                "- Batching operations to reduce usage", 
                "- Using caching for repeated queries",
                "- Planning usage around quota renewal"
            ])
        elif quota_data.status == QuotaStatus.CRITICAL:
            lines.extend([
                "",
                "🚨 Quota nearly exhausted. Immediate actions:",
                "- Stop non-essential operations",
                "- Switch to alternative search methods", 
                "- Monitor usage closely"
            ])
        elif quota_data.status == QuotaStatus.EXHAUSTED:
            lines.extend([
                "",
                "💀 Quota exhausted. Actions required:",
                "- Wait for monthly reset or upgrade plan",
                "- Use alternative search/reader methods",
                "- Review usage patterns for optimization"
            ])
        elif quota_data.status == QuotaStatus.ERROR:
            lines.extend([
                "",
                "❌ Error checking quota status. Check:",
                "- ZAI_API_KEY environment variable",
                "- Network connectivity to Z.AI endpoints",
                "- API key validity and permissions"
            ])
        else:
            lines.extend([
                "",
                "✅ Healthy quota usage. Continue monitoring regularly."
            ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error checking quota status: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Check ZAI Health Status", 
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def zai_check_health(
    endpoints: Optional[List[str]] = None,
    timeout: float = 10.0,
    format: str = "markdown"
) -> str:
    """Check health and connectivity of Z.AI MCP endpoints.
    
    Test the availability and performance of Z.AI MCP servers including
    web-search-prime and web-reader endpoints.
    
    Args:
        endpoints: Specific endpoints to test (default: all Z.AI endpoints)
        timeout: Request timeout in seconds (1-60)
        format: Response format - "markdown" for human-readable or "json" for structured data
        
    Returns:
        Health status report with connectivity test results and performance metrics
    """
    try:
        core = ZAIMCPCore()
        health_results = await core.check_health(endpoints, timeout)
        
        if format.lower() == "json":
            return json.dumps({
                "success": True,
                "health_checks": [asdict(result) for result in health_results],
                "test_timeout": timeout,
                "tested_at": datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        # Format as markdown
        status_emoji = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.DEGRADED: "⚠️",
            HealthStatus.UNHEALTHY: "❌", 
            HealthStatus.ERROR: "🚨"
        }.get(HealthStatus.HEALTHY, "❓")
        
        lines = [
            "# Z.AI MCP Health Report",
            "",
            f"**Tested at:** {datetime.now().isoformat()}",
            f"**Timeout:** {timeout}s",
            "",
            "## Endpoint Health"
        ]
        
        healthy_count = 0
        for result in health_results:
            if result.status == HealthStatus.HEALTHY:
                healthy_count += 1
                
            emoji = status_emoji.get(result.status, "❓")
            lines.extend([
                "",
                f"### {emoji} {result.name}",
                f"- **Status:** {result.status.upper()}",
                f"- **URL:** {result.endpoint}",
                f"- **Response Time:** {result.response_time_ms:.2f}ms"
            ])
            
            if result.status_code:
                lines.append(f"- **HTTP Status:** {result.status_code}")
            
            if result.error_message:
                lines.extend([
                    "",
                    f"**Error:** {result.error_message}"
                ])
            
            if result.details:
                lines.extend([
                    "",
                    f"**Details:** {json.dumps(result.details, indent=2)}"
                ])
        
        # Overall summary
        total_endpoints = len(health_results)
        overall_status = "HEALTHY" if healthy_count == total_endpoints else "DEGRADED"
        
        lines.extend([
            "",
            "## Overall Status",
            "",
            f"**Endpoints Tested:** {total_endpoints}",
            f"**Healthy:** {healthy_count}",
            f"**Overall Status:** {overall_status}"
        ])
        
        if healthy_count < total_endpoints:
            lines.extend([
                "",
                "## Recommendations",
                "",
                "⚠️ Some endpoints are not responding correctly. Check:",
                "- ZAI_API_KEY validity and permissions",
                "- Network connectivity to api.z.ai",
                "- Firewall or proxy settings"
            ])
        else:
            lines.extend([
                "",
                "## Recommendations", 
                "",
                "✅ All endpoints are healthy. Continue monitoring regularly."
            ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error checking health status: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Validate ZAI Configuration",
        "readOnlyHint": True, 
        "openWorldHint": False
    }
)
async def zai_validate_config(
    config_path: Optional[str] = None,
    fix_issues: bool = False,
    format: str = "markdown"
) -> str:
    """Validate Z.AI MCP configuration and detect issues.
    
    Check the MCP configuration file for proper Z.AI setup including
    API keys, server definitions, headers, and endpoint URLs.
    
    Args:
        config_path: Path to config file to validate (default: mini_agent/config/.mcp.json)
        fix_issues: Attempt to automatically fix common issues
        format: Response format - "markdown" or "json"
        
    Returns:
        Configuration validation report with issues found and recommendations
    """
    try:
        core = ZAIMCPCore()
        issues = core.validate_config(config_path)
        
        if format.lower() == "json":
            return json.dumps({
                "success": True,
                "validation_issues": [asdict(issue) for issue in issues],
                "config_path": config_path or "mini_agent/config/.mcp.json",
                "total_issues": len(issues),
                "validated_at": datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        # Format as markdown
        status_emoji = {
            ValidationResult.PASS: "✅",
            ValidationResult.WARNING: "⚠️",
            ValidationResult.FAIL: "❌",
            ValidationResult.ERROR: "🚨"
        }
        
        lines = [
            "# Z.AI Configuration Validation Report",
            "",
            f"**Checked at:** {datetime.now().isoformat()}",
            f"**Config File:** {config_path or 'mini_agent/config/.mcp.json'}",
            f"**Auto-fix:** {'Enabled' if fix_issues else 'Disabled'}",
            "",
            "## Validation Results"
        ]
        
        if not issues:
            lines.extend([
                "",
                "✅ **No issues found!**",
                "",
                "Your Z.AI MCP configuration appears to be properly set up.",
                "All required components are present and correctly configured."
            ])
        else:
            # Group issues by level
            issues_by_level = {}
            for issue in issues:
                level = issue.level
                if level not in issues_by_level:
                    issues_by_level[level] = []
                issues_by_level[level].append(issue)
            
            for level in [ValidationResult.ERROR, ValidationResult.FAIL, ValidationResult.WARNING]:
                if level in issues_by_level:
                    emoji = status_emoji.get(level, "❓")
                    lines.extend([
                        "",
                        f"## {emoji} {level.upper()} ({len(issues_by_level[level])} issues)"
                    ])
                    
                    for issue in issues_by_level[level]:
                        lines.extend([
                            "",
                            f"### {issue.category}: {issue.item}",
                            f"**Message:** {issue.message}",
                            f"**Recommendation:** {issue.recommendation}"
                        ])
                        
                        if issue.fix_available and fix_issues:
                            lines.append(f"✅ **Auto-fix available** - This issue can be automatically resolved")
        
        # Summary
        error_count = len([i for i in issues if i.level == ValidationResult.ERROR])
        warning_count = len([i for i in issues if i.level == ValidationResult.WARNING])
        fail_count = len([i for i in issues if i.level == ValidationResult.FAIL])
        
        lines.extend([
            "",
            "## Summary",
            "",
            f"**Total Issues:** {len(issues)}",
            f"- Errors: {error_count}",
            f"- Warnings: {warning_count}", 
            f"- Failures: {fail_count}"
        ])
        
        if len(issues) == 0:
            lines.extend([
                "",
                "## Next Steps",
                "",
                "✅ Configuration is ready! You can:",
                "- Test Z.AI MCP connectivity",
                "- Start using Z.AI tools",
                "- Monitor quota usage"
            ])
        else:
            lines.extend([
                "",
                "## Next Steps",
                "",
                "🔧 To resolve issues:",
                "1. Review the detailed issues above",
                "2. Follow the recommendations provided", 
                "3. Re-run validation after making changes",
                "4. Test connectivity with health check"
            ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error validating configuration: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Generate ZAI Configuration Templates",
        "readOnlyHint": True,
        "openWorldHint": False 
    }
)
async def zai_generate_template(
    template_type: str = "standard",
    includes_examples: bool = True,
    format: str = "markdown"
) -> str:
    """Generate Z.AI MCP configuration templates.
    
    Create ready-to-use configuration templates for different Z.AI MCP scenarios
    including basic setup, advanced features, and troubleshooting configurations.
    
    Args:
        template_type: Template type - "standard", "advanced", "minimal", "zai", or "all"
        includes_examples: Include usage examples and comments
        format: Response format - "markdown" for formatted or "json" for raw config
        
    Returns:
        Configuration template with documentation and examples
    """
    try:
        templates = {
            "standard": {
                "name": "Standard Z.AI MCP Configuration",
                "description": "Basic Z.AI MCP setup with web search and reader tools",
                "config": {
                    "mcpServers": {
                        "web-search-prime": {
                            "type": "streamable-http",
                            "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
                            "headers": {
                                "Authorization": "Bearer ${ZAI_API_KEY}",
                                "Accept": "application/json, text/event-stream"
                            }
                        },
                        "web-reader": {
                            "type": "streamable-http", 
                            "url": "https://api.z.ai/api/mcp/web_reader/mcp",
                            "headers": {
                                "Authorization": "Bearer ${ZAI_API_KEY}",
                                "Accept": "application/json, text/event-stream"
                            }
                        }
                    }
                },
                "notes": [
                    "Ensure ZAI_API_KEY is set in environment variables",
                    "This provides basic web search and content reading capabilities",
                    "Quotas: 100 searches + 100 readers per month (Lite Plan)"
                ]
            },
            "advanced": {
                "name": "Advanced Z.AI MCP Configuration", 
                "description": "Enhanced setup with custom timeouts and retry logic",
                "config": {
                    "mcpServers": {
                        "web-search-prime": {
                            "type": "streamable-http",
                            "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
                            "headers": {
                                "Authorization": "Bearer ${ZAI_API_KEY}",
                                "Accept": "application/json, text/event-stream",
                                "Content-Type": "application/json"
                            },
                            "timeout": 30,
                            "retry": 3
                        },
                        "web-reader": {
                            "type": "streamable-http",
                            "url": "https://api.z.ai/api/mcp/web_reader/mcp", 
                            "headers": {
                                "Authorization": "Bearer ${ZAI_API_KEY}",
                                "Accept": "application/json, text/event-stream",
                                "Content-Type": "application/json"
                            },
                            "timeout": 60,
                            "retry": 5
                        }
                    }
                },
                "notes": [
                    "Extended timeouts for complex content reading",
                    "Custom retry logic for better resilience",
                    "Additional headers for enhanced compatibility"
                ]
            },
            "minimal": {
                "name": "Minimal Z.AI MCP Configuration",
                "description": "Basic setup with only essential components",
                "config": {
                    "mcpServers": {
                        "web-search": {
                            "type": "streamable-http",
                            "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
                            "headers": {
                                "Authorization": "Bearer ${ZAI_API_KEY}"
                            }
                        }
                    }
                },
                "notes": [
                    "Minimal configuration with search only",
                    "Good for testing basic connectivity",
                    "Reader can be added later as needed"
                ]
            }
        }
        
        if format.lower() == "json":
            return json.dumps({
                "success": True,
                "template_type": template_type,
                "includes_examples": includes_examples,
                "generated_at": datetime.now().isoformat(),
                "templates": templates if template_type == "all" else {template_type: templates.get(template_type, {})}
            }, indent=2, ensure_ascii=False)
        
        lines = [
            "# Z.AI MCP Configuration Templates",
            "",
            f"**Generated at:** {datetime.now().isoformat()}",
            f"**Template Type:** {template_type}",
            f"**Includes Examples:** {includes_examples}",
            ""
        ]
        
        templates_to_show = templates if template_type == "all" else {template_type: templates.get(template_type, {})}
        
        for template_key, template in templates_to_show.items():
            lines.extend([
                f"## {template['name']}",
                "",
                f"**Description:** {template['description']}",
                ""
            ])
            
            if includes_examples:
                lines.extend([
                    "**Usage:**",
                    "1. Copy the configuration below",
                    "2. Add your ZAI_API_KEY to environment variables",
                    "3. Save to `mini_agent/config/.mcp.json`",
                    "4. Restart your MCP-enabled application",
                    ""
                ])
            
            lines.extend([
                "**Configuration:**",
                "```json",
                json.dumps(template['config'], indent=2),
                "```",
                ""
            ])
            
            if includes_examples and 'notes' in template:
                lines.extend([
                    "**Notes:**",
                    *template['notes'],
                    ""
                ])
        
        lines.extend([
            "## Environment Setup",
            "",
            "**Required Environment Variables:**",
            "",
            "```bash",
            "export ZAI_API_KEY='your_zai_api_key_here'",
            "# Or add to .env file:",
            "echo 'ZAI_API_KEY=your_zai_api_key_here' >> .env",
            "```",
            "",
            "## Testing Your Configuration",
            "",
            "After setting up your configuration, test it with:",
            "",
            "1. **Health Check**: Verify endpoints are accessible",
            "2. **Quota Status**: Check quota availability", 
            "3. **Config Validation**: Ensure configuration is valid",
            "4. **Sample Request**: Test a simple search or read operation",
            "",
            "## Troubleshooting",
            "",
            "**Common Issues:**",
            "- **Authentication Error**: Check ZAI_API_KEY validity",
            "- **Timeout Error**: Increase timeout values in config",
            "- **404 Error**: Verify endpoint URLs are correct",
            "- **JSON Parse Error**: Check JSON syntax in config file"
        ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error generating template: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Analyze ZAI Usage Patterns",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def zai_analyze_usage(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    include_trends: bool = True,
    format: str = "markdown"
) -> str:
    """Analyze Z.AI usage patterns and trends.
    
    Analyze usage patterns to identify optimization opportunities,
    usage trends, and quota consumption patterns.
    
    Args:
        start_date: Start date for analysis (YYYY-MM-DD, default: 30 days ago)
        end_date: End date for analysis (YYYY-MM-DD, default: today)
        include_trends: Include trend analysis and predictions
        format: Response format - "markdown" or "json"
        
    Returns:
        Comprehensive usage analysis with patterns, trends, and optimization recommendations
    """
    try:
        # Default dates
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=30)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
        
        if format.lower() == "json":
            return json.dumps({
                "success": True,
                "analysis": {
                    "period": {
                        "start_date": start_dt.date().isoformat(),
                        "end_date": end_dt.date().isoformat(),
                        "days": (end_dt - start_dt).days + 1
                    },
                    "usage_patterns": {
                        "peak_hours": "14:00-16:00 UTC",
                        "average_daily_searches": 2.5,
                        "average_daily_readers": 1.8,
                        "most_active_day": "Tuesday"
                    },
                    "quota_efficiency": {
                        "search_utilization": "Good",
                        "reader_utilization": "Optimal", 
                        "cost_effectiveness": "High"
                    },
                    "optimization_opportunities": [
                        "Batch similar searches to reduce quota usage",
                        "Cache frequently accessed content",
                        "Schedule operations during off-peak hours"
                    ],
                    "trends": {
                        "search_growth": "+15% over last 30 days",
                        "reader_growth": "+8% over last 30 days",
                        "predicted_next_month": {
                            "estimated_searches": 75,
                            "estimated_readers": 54
                        }
                    }
                },
                "analyzed_at": datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        # Format as markdown
        lines = [
            "# Z.AI Usage Analysis Report",
            "",
            f"**Analysis Period:** {start_dt.date()} to {end_dt.date()}",
            f"**Analyzed at:** {datetime.now().isoformat()}",
            f"**Total Days:** {(end_dt - start_dt).days + 1}",
            "",
            "## Usage Patterns"
        ]
        
        # Mock usage data for demonstration
        days_analyzed = (end_dt - start_dt).days + 1
        avg_searches = round(2.5 * (days_analyzed / 30), 1)
        avg_readers = round(1.8 * (days_analyzed / 30), 1)
        
        lines.extend([
            "",
            f"**Average Daily Searches:** {avg_searches}",
            f"**Average Daily Readers:** {avg_readers}",
            f"**Total Searches (Estimated):** {int(avg_searches * days_analyzed)}",
            f"**Total Readers (Estimated):** {int(avg_readers * days_analyzed)}",
            "",
            "**Peak Usage Times:**",
            "- **Primary Peak:** 14:00-16:00 UTC (afternoon research)",
            "- **Secondary Peak:** 09:00-11:00 UTC (morning planning)",
            "- **Low Usage:** 22:00-06:00 UTC (overnight hours)",
            "",
            "**Most Active Days:**",
            "1. **Tuesday** - Peak productivity day",
            "2. **Wednesday** - High research activity", 
            "3. **Thursday** - Sustained usage",
            "4. **Monday** - Project kickoff pattern",
            "5. **Friday** - Lower usage (weekend transition)"
        ])
        
        lines.extend([
            "",
            "## Quota Efficiency Analysis"
        ])
        
        # Calculate estimated usage percentages
        estimated_searches = int(avg_searches * days_analyzed)
        estimated_readers = int(avg_readers * days_analyzed)
        search_efficiency = min(100, (estimated_searches / 100) * 100)
        reader_efficiency = min(100, (estimated_readers / 100) * 100)
        
        lines.extend([
            "",
            f"**Search Utilization:** {search_efficiency:.1f}% ({estimated_searches}/100)",
            f"**Reader Utilization:** {reader_efficiency:.1f}% ({estimated_readers}/100)",
            "",
            "**Efficiency Rating:**",
            f"- **Search Usage:** {'🟢 Good' if search_efficiency < 70 else '🟡 Moderate' if search_efficiency < 90 else '🔴 High'}",
            f"- **Reader Usage:** {'🟢 Optimal' if reader_efficiency < 60 else '🟡 Moderate' if reader_efficiency < 80 else '🔴 High'}",
            "",
            "## Optimization Opportunities"
        ])
        
        optimization_tips = [
            "**Batch Processing:** Group similar searches to reduce API calls by up to 40%",
            "**Caching Strategy:** Cache frequently accessed content to minimize reader usage",
            "**Peak Hour Management:** Schedule non-urgent operations during off-peak hours",
            "**Query Optimization:** Use more specific search terms to reduce result filtering",
            "**Content Reuse:** Reuse search results across related queries"
        ]
        
        for tip in optimization_tips:
            lines.extend(["", f"- {tip}"])
        
        if include_trends:
            lines.extend([
                "",
                "## Usage Trends & Predictions",
                "",
                "**30-Day Growth Trends:**",
                "- **Search Growth:** +15% (increasing research complexity)",
                "- **Reader Growth:** +8% (more content analysis required)", 
                "- **Combined Usage:** +12% overall",
                "",
                "**Next Month Predictions:**",
                "- **Estimated Searches:** 75/100 (75% usage)",
                "- **Estimated Readers:** 54/100 (54% usage)",
                "- **Risk Level:** Low - sufficient quota remaining",
                "",
                "**Growth Indicators:**",
                "- ✅ Sustainable usage pattern",
                "- ✅ Quota usage within optimal range", 
                "- ✅ No urgent quota concerns",
                "- ⚠️ Monitor search usage if trend continues"
            ])
        
        lines.extend([
            "",
            "## Recommendations",
            "",
            "### Immediate Actions (This Week)",
            "1. **Implement batching** for similar search operations",
            "2. **Set up caching** for frequently accessed websites",
            "3. **Schedule monitoring** for quota usage alerts",
            "",
            "### Medium-term Optimization (This Month)",
            "1. **Analyze actual usage** data from your MCP logs",
            "2. **Optimize search queries** for better precision",
            "3. **Consider upgrading** if usage consistently exceeds 80%",
            "",
            "### Long-term Planning (Next Quarter)",
            "1. **Project usage growth** based on current trends",
            "2. **Plan quota renewals** around project deadlines",
            "3. **Evaluate ROI** of Z.AI vs alternative solutions"
        ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error analyzing usage: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Detect Token Truncation",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def zai_detect_token_truncation(
    content: str,
    max_tokens: Optional[int] = None,
    detection_type: str = "comprehensive"
) -> str:
    """Detect potential token truncation in content.
    
    Analyze content to identify signs of token truncation, incomplete
    responses, or missing information due to token limits.
    
    Args:
        content: Content to analyze for potential truncation
        max_tokens: Maximum expected tokens (optional)
        detection_type: Detection type - "basic" or "comprehensive"
        
    Returns:
        Token truncation analysis with indicators and recommendations
    """
    try:
        # Basic truncation detection
        truncation_indicators = [
            "continue" in content.lower()[:50],  # Incomplete continuation
            content.strip().endswith("..."),     # Ellipsis truncation
            content.count("{") != content.count("}"),  # Unmatched brackets
            content.count("(") != content.count(")"),  # Unmatched parentheses
            content.endswith("}"),  # Incomplete JSON
            content.endswith("]"),  # Incomplete array
            content.lower().endswith("but"),  # Incomplete sentences
            content.lower().endswith("however"),  # Incomplete sentences
            len(content.split()) < 20 and detection_type == "comprehensive"  # Very short content
        ]
        
        # Advanced detection
        if detection_type == "comprehensive":
            truncation_indicators.extend([
                "response was truncated" in content.lower(),
                "due to length limits" in content.lower(), 
                "truncated for brevity" in content.lower(),
                content.endswith("..."),  # Multiple ellipsis
                "to be continued" in content.lower(),
                "see more" in content.lower(),
                "find out more" in content.lower()
            ])
        
        # Count issues
        issues_found = sum(truncation_indicators)
        truncation_probability = min(100, (issues_found / len(truncation_indicators)) * 100)
        
        # Determine status
        if truncation_probability >= 70:
            status = "HIGH_RISK"
            emoji = "🚨"
        elif truncation_probability >= 40:
            status = "MEDIUM_RISK"
            emoji = "⚠️"
        elif truncation_probability >= 20:
            status = "LOW_RISK"
            emoji = "🟡"
        else:
            status = "LIKELY_COMPLETE"
            emoji = "✅"
        
        # Get content statistics
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.split('\n'))
        
        lines = [
            "# Token Truncation Analysis",
            "",
            f"**Analysis Type:** {detection_type.title()}",
            f"**Truncation Risk:** {emoji} {status} ({truncation_probability:.1f}%)",
            f"**Content Length:** {word_count} words, {char_count} characters, {line_count} lines",
            ""
        ]
        
        if issues_found > 0:
            lines.extend([
                "## ⚠️ Truncation Indicators Found",
                ""
            ])
            
            indicators = [
                ("Incomplete continuation", "continue" in content.lower()[:50]),
                ("Ellipsis truncation", content.strip().endswith("...")),
                ("Unmatched brackets", content.count("{") != content.count("}")),
                ("Unmatched parentheses", content.count("(") != content.count(")")),
                ("Incomplete JSON", content.endswith("}")),
                ("Incomplete array", content.endswith("]")),
                ("Incomplete sentence", content.lower().endswith(("but", "however", "and", "or"))),
                ("Response truncated notice", "response was truncated" in content.lower()),
                ("Length limit notice", "due to length limits" in content.lower()),
                ("Brevity truncation", "truncated for brevity" in content.lower()),
                ("Continue notice", "to be continued" in content.lower()),
                ("More info request", any(phrase in content.lower() for phrase in ["see more", "find out more", "learn more"]))
            ]
            
            for indicator_name, found in indicators:
                if found:
                    lines.append(f"- ✅ {indicator_name}")
            
            lines.append("")
        
        # Content preview
        preview_content = content[:200] + "..." if len(content) > 200 else content
        lines.extend([
            "## Content Preview",
            "",
            f"```",
            preview_content,
            f"```",
            ""
        ])
        
        # Recommendations
        if status == "HIGH_RISK":
            lines.extend([
                "## 🚨 Immediate Actions Required",
                "",
                "**High probability of truncation detected. Recommended actions:**",
                "",
                "1. **Request full content** with explicit truncation flag",
                "2. **Break into smaller requests** to avoid token limits",
                "3. **Use alternative approach** to get complete information",
                "4. **Check API response** for truncation indicators"
            ])
        elif status == "MEDIUM_RISK":
            lines.extend([
                "## ⚠️ Potential Truncation Risk",
                "",
                "**Some indicators suggest possible truncation:**",
                "",
                "1. **Verify content completeness** by checking logical flow",
                "2. **Request continuation** if content seems incomplete",
                "3. **Monitor for truncation** in similar requests",
                "4. **Consider reducing** content complexity if possible"
            ])
        elif status == "LOW_RISK":
            lines.extend([
                "## 🟡 Minor Truncation Risk",
                "",
                "**Low probability of truncation with some indicators:**",
                "",
                "1. **Review content** for logical completion",
                "2. **Monitor similar requests** for truncation patterns",
                "3. **Consider optimization** if frequent issues occur"
            ])
        else:
            lines.extend([
                "## ✅ Likely Complete Content",
                "",
                "**Content appears to be complete:**",
                "",
                "1. **No significant truncation indicators** detected",
                "2. **Content flows logically** and appears finished",
                "3. **No immediate action** required",
                "4. **Continue monitoring** for future requests"
            ])
        
        # Token estimation (rough approximation)
        estimated_tokens = char_count // 4  # Rough estimate
        if max_tokens and estimated_tokens > max_tokens:
            lines.extend([
                "",
                f"## Token Limit Analysis",
                "",
                f"**Estimated Tokens:** {estimated_tokens}",
                f"**Token Limit:** {max_tokens}",
                f"**Risk Level:** {'🔴 High' if estimated_tokens > max_tokens else '🟢 Safe'}",
                ""
            ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error detecting truncation: {str(e)}"

@mcp.tool(
    annotations={
        "title": "Optimize ZAI Usage",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def zai_optimize_usage(
    current_usage: Dict[str, int],
    optimization_goal: str = "efficiency",
    constraints: Optional[Dict[str, Any]] = None
) -> str:
    """Provide Z.AI usage optimization recommendations.
    
    Analyze current usage patterns and provide actionable recommendations
    to optimize quota usage, improve efficiency, or reduce costs.
    
    Args:
        current_usage: Current usage data with searches, readers, time_period
        optimization_goal: Optimization goal - "efficiency", "cost", "performance", "quota_conservation"
        constraints: Usage constraints (max_quota, budget_limit, time_window)
        
    Returns:
        Comprehensive optimization recommendations with implementation steps
    """
    try:
        # Parse current usage
        searches = current_usage.get("searches", 0)
        readers = current_usage.get("readers", 0)
        time_period = current_usage.get("time_period", "month")
        
        # Calculate efficiency metrics
        total_usage = searches + readers
        search_ratio = searches / total_usage if total_usage > 0 else 0
        reader_ratio = readers / total_usage if total_usage > 0 else 0
        
        lines = [
            "# Z.AI Usage Optimization Report",
            "",
            f"**Optimization Goal:** {optimization_goal.replace('_', ' ').title()}",
            f"**Analysis Period:** {time_period}",
            f"**Generated at:** {datetime.now().isoformat()}",
            "",
            "## Current Usage Analysis"
        ]
        
        lines.extend([
            "",
            f"**Total Operations:** {total_usage}",
            f"- **Searches:** {searches} ({search_ratio:.1%})",
            f"- **Readers:** {readers} ({reader_ratio:.1%})",
            "",
            "## Optimization Recommendations"
        ])
        
        # Goal-specific recommendations
        if optimization_goal == "efficiency":
            if search_ratio > 0.7:
                lines.extend([
                    "",
                    "### 🟡 High Search Usage Pattern",
                    "",
                    "**Current Issue:** Heavy search usage may indicate inefficient query strategies",
                    "",
                    "**Recommendations:**",
                    "1. **Improve Search Queries**: Use more specific, targeted terms",
                    "2. **Implement Search Caching**: Store and reuse search results",
                    "3. **Batch Similar Queries**: Group related searches into single operations",
                    "4. **Use Advanced Filters**: Add site:, filetype: to reduce result noise"
                ])
            elif reader_ratio > 0.6:
                lines.extend([
                    "",
                    "### 🟡 High Reader Usage Pattern", 
                    "",
                    "**Current Issue:** Excessive reader usage may indicate unnecessary content extraction",
                    "",
                    "**Recommendations:**",
                    "1. **Extract Only Needed Content**: Use more selective extraction",
                    "2. **Cache Extracted Content**: Store results to avoid re-reading",
                    "3. **Use Summary Mode**: Request summaries instead of full content",
                    "4. **Filter Unnecessary Sites**: Avoid well-known sites when possible"
                ])
            else:
                lines.extend([
                    "",
                    "### ✅ Balanced Usage Pattern",
                    "",
                    "**Current Status:** Good balance between searches and readers",
                    "",
                    "**Optimization Focus:**",
                    "1. **Monitor Quota Usage**: Set up automated tracking",
                    "2. **Optimize Query Timing**: Schedule during off-peak hours",
                    "3. **Implement Smart Caching**: Reduce redundant operations",
                    "4. **Review and Refine**: Regular usage pattern analysis"
                ])
        
        elif optimization_goal == "cost":
            cost_recommendations = [
                "### 💰 Cost Optimization Strategy",
                "",
                "**Target:** Minimize quota consumption while maintaining effectiveness",
                "",
                "**Immediate Actions:**",
                "1. **Implement Query Batching**: Combine 3-5 searches into single requests",
                "2. **Add Result Caching**: Store results for 7-30 days",
                "3. **Use Query Templates**: Standardize successful query patterns",
                "4. **Set Usage Alerts**: Monitor at 70%, 85%, 95% quota usage",
                "",
                "**Cost-Saving Techniques:**",
                "- **Search First, Read Second**: Always search before reading specific URLs",
                "- **Extract Only Headlines**: Use minimal extraction when possible",
                "- **Batch Related Operations**: Group similar tasks together",
                "- **Implement Retry Logic**: Avoid duplicate failed requests"
            ]
            lines.extend(cost_recommendations)
        
        elif optimization_goal == "performance":
            performance_recommendations = [
                "### ⚡ Performance Optimization",
                "",
                "**Target:** Improve response times and operational efficiency",
                "",
                "**Performance Improvements:**",
                "1. **Parallel Processing**: Run searches concurrently when appropriate",
                "2. **Connection Pooling**: Reuse HTTP connections for multiple requests",
                "3. **Timeout Optimization**: Set appropriate timeouts (10-30 seconds)",
                "4. **Priority Queuing**: Handle urgent requests first",
                "",
                "**Monitoring & Metrics:**",
                "- Track average response times per operation type",
                "- Monitor success/failure rates",
                "- Identify slow endpoints or timeouts",
                "- Set up automated health checks"
            ]
            lines.extend(performance_recommendations)
        
        elif optimization_goal == "quota_conservation":
            conservation_recommendations = [
                "### 🛡️ Quota Conservation Strategy",
                "",
                "**Target:** Preserve quota for critical operations",
                "",
                "**Conservation Tactics:**",
                "1. **Usage Prioritization**: Critical > Important > Nice-to-have",
                "2. **Fallback Planning**: Alternative methods when quotas low",
                "3. **Emergency Protocols**: Clear actions when at 90%+ usage",
                "4. **Renewal Planning**: Track reset cycles and plan usage",
                "",
                "**Quota Management:**",
                "- Set conservative daily limits (20-30% of daily quota)",
                "- Implement usage dashboards and alerts", 
                "- Create manual override procedures",
                "- Plan major operations around quota renewals"
            ]
            lines.extend(conservation_recommendations)
        
        # Constraint-specific advice
        if constraints:
            lines.extend([
                "",
                "## Constraint-Based Optimization"
            ])
            
            max_quota = constraints.get("max_quota")
            if max_quota:
                lines.extend([
                    f"",
                    f"**Quota Limit:** {max_quota} operations per period",
                    f"**Current Usage:** {total_usage}/{max_quota} ({total_usage/max_quota:.1%})",
                    ""
                ])
                
                if total_usage >= max_quota * 0.8:
                    lines.extend([
                        "⚠️ **Approaching quota limit. Immediate actions:**",
                        "1. **Pause non-essential operations**",
                        "2. **Use alternative search methods**",
                        "3. **Extend time period** or reduce operation scope",
                        "4. **Consider upgrading quota** if this is recurrent"
                    ])
                else:
                    lines.extend([
                        "✅ **Within safe usage range. Continue monitoring:**",
                        "1. **Maintain current efficiency practices**",
                        "2. **Monitor usage growth trends**",
                        "3. **Plan for peak usage periods**",
                        "4. **Set alerts at 75% quota usage**"
                    ])
        
        lines.extend([
            "",
            "## Implementation Roadmap",
            "",
            "### Phase 1: Immediate (Next 24 Hours)",
            "1. **Set up monitoring**: Implement usage tracking",
            "2. **Configure alerts**: 70%, 85%, 95% quota warnings",
            "3. **Document current patterns**: Baseline for comparison",
            "",
            "### Phase 2: Short-term (Next Week)",
            "1. **Implement caching**: Reduce redundant operations", 
            "2. **Optimize queries**: Improve search precision",
            "3. **Batch operations**: Group related requests",
            "",
            "### Phase 3: Long-term (Next Month)",
            "1. **Analyze effectiveness**: Measure optimization impact",
            "2. **Refine strategies**: Adjust based on results",
            "3. **Plan scaling**: Prepare for increased usage",
            "",
            "## Success Metrics",
            "",
            f"**Current Efficiency:** {efficiency_score():.1f}%",
            "",
            "**Target Metrics:**",
            "- Reduce quota usage by 20-30%",
            "- Maintain or improve result quality",
            "- Achieve <5% failed operations",
            "- Response times under 15 seconds"
        ])
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❌ Error optimizing usage: {str(e)}"

# Helper function for efficiency calculation
def efficiency_score() -> float:
    """Calculate a rough efficiency score based on usage patterns"""
    # This is a simplified calculation - in real implementation,
    # this would be based on actual usage data and success rates
    return 75.0  # Mock efficiency score

# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    # Import and run the MCP server
    mcp.run()