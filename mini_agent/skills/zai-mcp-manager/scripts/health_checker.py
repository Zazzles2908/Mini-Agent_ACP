#!/usr/bin/env python3
"""
Z.AI MCP Health Checker - Test connectivity and performance of Z.AI MCP endpoints
"""

import os
import json
import asyncio
import aiohttp
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import statistics


@dataclass
class HealthCheckResult:
    """Health check result for an endpoint"""
    name: str
    endpoint: str
    status: str  # 'healthy', 'degraded', 'unhealthy', 'error'
    response_time_ms: float
    status_code: Optional[int]
    error_message: Optional[str]
    timestamp: str
    details: Dict[str, Any]


@dataclass
class OverallHealthStatus:
    """Overall health status across all endpoints"""
    overall_status: str  # 'healthy', 'degraded', 'unhealthy', 'error'
    endpoints: List[HealthCheckResult]
    summary: Dict[str, Any]
    timestamp: str


class ZAIMCPHealthChecker:
    """Check health and performance of Z.AI MCP endpoints"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        if not self.api_key:
            raise ValueError("ZAI_API_KEY not found in environment or provided")
        
        # Define endpoints to test
        self.endpoints = {
            "zai-search": "https://api.z.ai/api/mcp/web_search_prime/mcp",
            "zai-reader": "https://api.z.ai/api/mcp/web_reader/mcp"
        }
        
        # Performance thresholds
        self.good_response_time = 1000  # ms
        self.degraded_response_time = 3000  # ms
        self.timeout_seconds = 10
        
        # Test configuration
        self.test_requests = {
            "tools_list": {
                "method": "tools/list",
                "params": {}
            },
            "capabilities_check": {
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "health-checker",
                        "version": "1.0.0"
                    }
                }
            }
        }
    
    async def check_endpoint_health(self, endpoint_name: str, endpoint_url: str) -> HealthCheckResult:
        """Check health of a single endpoint"""
        start_time = time.time()
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout_seconds)
            ) as session:
                
                # Test 1: Capabilities check (initialization)
                init_result = await self._test_request(
                    session, endpoint_url, headers, "capabilities_check"
                )
                
                # Test 2: Tools list request
                tools_result = await self._test_request(
                    session, endpoint_url, headers, "tools_list"
                )
                
                # Calculate overall response time
                response_time = (time.time() - start_time) * 1000
                
                # Determine status based on results
                if init_result.get('success') and tools_result.get('success'):
                    if response_time <= self.good_response_time:
                        status = "healthy"
                    elif response_time <= self.degraded_response_time:
                        status = "degraded"
                    else:
                        status = "unhealthy"
                else:
                    status = "unhealthy"
                
                # Get status code from the most recent successful request
                status_code = None
                if init_result.get('status_code'):
                    status_code = init_result['status_code']
                elif tools_result.get('status_code'):
                    status_code = tools_result['status_code']
                
                # Collect error information
                error_message = None
                if not init_result.get('success') and init_result.get('error'):
                    error_message = f"Init failed: {init_result['error']}"
                elif not tools_result.get('success') and tools_result.get('error'):
                    error_message = f"Tools failed: {tools_result['error']}"
                
                return HealthCheckResult(
                    name=endpoint_name,
                    endpoint=endpoint_url,
                    status=status,
                    response_time_ms=round(response_time, 2),
                    status_code=status_code,
                    error_message=error_message,
                    timestamp=datetime.now().isoformat(),
                    details={
                        "init_test": init_result,
                        "tools_test": tools_result,
                        "performance_score": self._calculate_performance_score(response_time)
                    }
                )
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=endpoint_name,
                endpoint=endpoint_url,
                status="error",
                response_time_ms=round(response_time, 2),
                status_code=None,
                error_message=str(e),
                timestamp=datetime.now().isoformat(),
                details={}
            )
    
    async def _test_request(self, session: aiohttp.ClientSession, endpoint: str, 
                          headers: Dict[str, str], test_type: str) -> Dict[str, Any]:
        """Test a specific request type"""
        try:
            request_data = self.test_requests.get(test_type, {})
            method = request_data.get("method", "GET")
            params = request_data.get("params", {})
            
            async with session.request(
                method="POST",
                url=endpoint,
                headers=headers,
                json={"method": method, "params": params} if method == "tools/call" else request_data,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                status_code = response.status
                
                if status_code == 200:
                    # Try to parse JSON response
                    try:
                        result = await response.json()
                        return {
                            "success": True,
                            "status_code": status_code,
                            "response": result
                        }
                    except:
                        # Non-JSON response but successful HTTP status
                        text_response = await response.text()
                        return {
                            "success": True,
                            "status_code": status_code,
                            "response_text": text_response[:1000]  # Limit response size
                        }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "status_code": status_code,
                        "error": f"HTTP {status_code}: {error_text[:200]}"
                    }
                    
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def _calculate_performance_score(self, response_time_ms: float) -> int:
        """Calculate performance score from 0-100"""
        if response_time_ms <= self.good_response_time:
            return 100
        elif response_time_ms <= self.degraded_response_time:
            # Linear degradation from 100 to 60
            ratio = (response_time_ms - self.good_response_time) / (self.degraded_response_time - self.good_response_time)
            return int(100 - (ratio * 40))
        else:
            # Below 60, linear degradation to 0
            excess_time = response_time_ms - self.degraded_response_time
            ratio = min(1.0, excess_time / 2000)  # 2 seconds max penalty
            return max(0, int(60 - (ratio * 60)))
    
    async def check_all_endpoints(self) -> OverallHealthStatus:
        """Check health of all configured endpoints"""
        results = []
        
        # Check endpoints in parallel
        tasks = [
            self.check_endpoint_health(name, url)
            for name, url in self.endpoints.items()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions and convert to HealthCheckResult objects
        health_results = []
        for result in results:
            if isinstance(result, Exception):
                health_results.append(HealthCheckResult(
                    name="unknown",
                    endpoint="unknown",
                    status="error",
                    response_time_ms=0,
                    status_code=None,
                    error_message=str(result),
                    timestamp=datetime.now().isoformat(),
                    details={}
                ))
            else:
                health_results.append(result)
        
        # Determine overall status
        overall_status = self._determine_overall_status(health_results)
        
        # Calculate summary statistics
        response_times = [r.response_time_ms for r in health_results if r.response_time_ms > 0]
        avg_response_time = round(statistics.mean(response_times), 2) if response_times else 0
        
        healthy_count = len([r for r in health_results if r.status == "healthy"])
        degraded_count = len([r for r in health_results if r.status == "degraded"])
        unhealthy_count = len([r for r in health_results if r.status == "unhealthy"])
        error_count = len([r for r in health_results if r.status == "error"])
        
        summary = {
            "total_endpoints": len(health_results),
            "healthy": healthy_count,
            "degraded": degraded_count,
            "unhealthy": unhealthy_count,
            "errors": error_count,
            "average_response_time_ms": avg_response_time,
            "uptime_percentage": round((healthy_count / len(health_results)) * 100, 1) if health_results else 0
        }
        
        return OverallHealthStatus(
            overall_status=overall_status,
            endpoints=health_results,
            summary=summary,
            timestamp=datetime.now().isoformat()
        )
    
    def _determine_overall_status(self, results: List[HealthCheckResult]) -> str:
        """Determine overall status based on individual endpoint results"""
        if not results:
            return "error"
        
        error_count = len([r for r in results if r.status == "error"])
        unhealthy_count = len([r for r in results if r.status == "unhealthy"])
        degraded_count = len([r for r in results if r.status == "degraded"])
        
        if error_count > 0 or unhealthy_count > 0:
            if (error_count + unhealthy_count) >= len(results) * 0.5:
                return "unhealthy"
            else:
                return "degraded"
        elif degraded_count > 0:
            if degraded_count >= len(results) * 0.5:
                return "degraded"
            else:
                return "healthy"
        else:
            return "healthy"
    
    def generate_health_report(self, health_status: OverallHealthStatus) -> str:
        """Generate a comprehensive health report"""
        # Status emoji mapping
        status_emojis = {
            "healthy": "✅",
            "degraded": "⚠️",
            "unhealthy": "🚨",
            "error": "❌"
        }
        
        overall_emoji = status_emojis.get(health_status.overall_status, "❓")
        
        report_lines = [
            "# Z.AI MCP Health Check Report",
            "",
            f"**Overall Status:** {overall_emoji} {health_status.overall_status.upper()}",
            f"**Generated:** {health_status.timestamp}",
            "",
            "## Summary",
            "",
            f"- **Total Endpoints:** {health_status.summary['total_endpoints']}",
            f"- **Healthy:** {health_status.summary['healthy']}",
            f"- **Degraded:** {health_status.summary['degraded']}",
            f"- **Unhealthy:** {health_status.summary['unhealthy']}",
            f"- **Errors:** {health_status.summary['errors']}",
            f"- **Average Response Time:** {health_status.summary['average_response_time_ms']}ms",
            f"- **Uptime:** {health_status.summary['uptime_percentage']}%",
            "",
            "## Endpoint Details",
            ""
        ]
        
        # Add detailed results for each endpoint
        for result in health_status.endpoints:
            emoji = status_emojis.get(result.status, "❓")
            
            report_lines.extend([
                f"### {emoji} {result.name}",
                f"**Endpoint:** `{result.endpoint}`",
                f"**Status:** {result.status}",
                f"**Response Time:** {result.response_time_ms}ms",
                ""
            ])
            
            if result.status_code:
                report_lines.append(f"**Status Code:** {result.status_code}")
            
            if result.error_message:
                report_lines.extend([
                    f"**Error:** {result.error_message}",
                    ""
                ])
            
            # Add performance score
            performance_score = result.details.get('performance_score', 0)
            report_lines.append(f"**Performance Score:** {performance_score}/100")
            report_lines.append("")
        
        # Add recommendations based on overall status
        if health_status.overall_status == "unhealthy" or health_status.overall_status == "error":
            report_lines.extend([
                "## Recommendations",
                "",
                "🚨 **Immediate Actions Required:**",
                "- Check API key validity and permissions",
                "- Verify network connectivity to Z.AI endpoints",
                "- Review rate limiting or quota exhaustion",
                "- Check for service maintenance or outages",
                ""
            ])
        elif health_status.overall_status == "degraded":
            report_lines.extend([
                "## Recommendations",
                "",
                "⚠️ **Performance Issues Detected:**",
                "- Monitor response times and consider optimization",
                "- Check for network latency issues",
                "- Review timeout configurations",
                "- Consider implementing retry logic",
                ""
            ])
        else:
            report_lines.extend([
                "## Recommendations",
                "",
                "✅ **All systems operational.** Continue monitoring for:",
                "- Quota usage patterns",
                "- Response time trends",
                "- Error rate monitoring",
                ""
            ])
        
        return "\n".join(report_lines)


async def main():
    """Main function for CLI usage"""
    try:
        checker = ZAIMCPHealthChecker()
        health_status = await checker.check_all_endpoints()
        report = checker.generate_health_report(health_status)
        print(report)
        
        # Save detailed results to JSON
        results_file = f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(asdict(health_status), f, indent=2)
        
        print(f"\nDetailed results saved to: {results_file}")
        
    except Exception as e:
        print(f"Error running health check: {e}")


if __name__ == "__main__":
    asyncio.run(main())
