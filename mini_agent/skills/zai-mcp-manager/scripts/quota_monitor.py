#!/usr/bin/env python3
"""
Z.AI MCP Quota Monitor - Real-time quota tracking and alerting
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class QuotaStatus:
    """Quota status information"""
    searches_used: int
    searches_total: int
    readers_used: int
    readers_total: int
    searches_remaining: int
    readers_remaining: int
    days_until_reset: int
    usage_percentage: float
    status: str  # 'healthy', 'warning', 'critical'
    last_updated: str


class ZAIMCPQuotaMonitor:
    """Monitor Z.AI MCP quota usage and provide alerts"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        if not self.api_key:
            raise ValueError("ZAI_API_KEY not found in environment or provided")
        
        # Z.AI MCP endpoints
        self.search_endpoint = "https://api.z.ai/api/mcp/web_search_prime/mcp"
        self.reader_endpoint = "https://api.z.ai/api/mcp/web_reader/mcp"
        
        # Quota limits (Lite Plan)
        self.search_limit = 100
        self.reader_limit = 100
        
        # Alert thresholds
        self.warning_threshold = 80  # 80%
        self.critical_threshold = 95  # 95%
        
        # In-memory usage tracking
        self.usage_log = []
    
    async def check_quota_status(self) -> QuotaStatus:
        """Check current quota status"""
        try:
            # Make a small test request to get quota info
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                }
                
                # Test search endpoint
                search_result = await self._test_endpoint(
                    session, self.search_endpoint, headers, "search"
                )
                
                # Test reader endpoint
                reader_result = await self._test_endpoint(
                    session, self.reader_endpoint, headers, "reader"
                )
                
                # Simulate quota calculation (in real implementation, this would come from the API)
                searches_used = len([entry for entry in self.usage_log if entry['type'] == 'search'])
                readers_used = len([entry for entry in self.usage_log if entry['type'] == 'reader'])
                
                searches_remaining = self.search_limit - searches_used
                readers_remaining = self.reader_limit - readers_used
                
                # Calculate overall usage percentage
                total_used = searches_used + readers_used
                total_limit = self.search_limit + self.reader_limit
                usage_percentage = (total_used / total_limit) * 100
                
                # Determine status
                if usage_percentage >= self.critical_threshold:
                    status = "critical"
                elif usage_percentage >= self.warning_threshold:
                    status = "warning"
                else:
                    status = "healthy"
                
                # Calculate days until reset (approximate)
                now = datetime.now()
                days_until_reset = 30 - now.day  # Approximate monthly reset
                
                return QuotaStatus(
                    searches_used=searches_used,
                    searches_total=self.search_limit,
                    readers_used=readers_used,
                    readers_total=self.reader_limit,
                    searches_remaining=searches_remaining,
                    readers_remaining=readers_remaining,
                    days_until_reset=max(1, days_until_reset),
                    usage_percentage=round(usage_percentage, 1),
                    status=status,
                    last_updated=datetime.now().isoformat()
                )
                
        except Exception as e:
            # Return error status
            return QuotaStatus(
                searches_used=0,
                searches_total=self.search_limit,
                readers_used=0,
                readers_total=self.reader_limit,
                searches_remaining=self.search_limit,
                readers_remaining=self.reader_limit,
                days_until_reset=30,
                usage_percentage=0.0,
                status="error",
                last_updated=datetime.now().isoformat()
            )
    
    async def _test_endpoint(self, session: aiohttp.ClientSession, endpoint: str, 
                           headers: Dict[str, str], operation_type: str) -> Dict[str, Any]:
        """Test MCP endpoint connectivity"""
        try:
            # Make a minimal test request to check connectivity
            test_request = {
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(
                endpoint,
                headers=headers,
                json=test_request,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {"status": "healthy", "response": result}
                else:
                    return {"status": "error", "status_code": response.status}
                    
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def log_usage(self, operation_type: str, success: bool, response_time: Optional[float] = None):
        """Log usage for tracking"""
        self.usage_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": operation_type,
            "success": success,
            "response_time": response_time
        })
        
        # Keep only last 1000 entries
        if len(self.usage_log) > 1000:
            self.usage_log = self.usage_log[-1000:]
    
    def get_usage_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate usage report for specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_usage = [
            entry for entry in self.usage_log
            if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
        ]
        
        searches = [entry for entry in recent_usage if entry['type'] == 'search']
        readers = [entry for entry in recent_usage if entry['type'] == 'reader']
        
        successful_searches = [s for s in searches if s['success']]
        successful_readers = [r for r in readers if r['success']]
        
        avg_response_time = None
        if recent_usage:
            response_times = [entry['response_time'] for entry in recent_usage 
                            if entry['response_time'] is not None]
            if response_times:
                avg_response_time = round(sum(response_times) / len(response_times), 2)
        
        return {
            "period_days": days,
            "total_operations": len(recent_usage),
            "searches": {
                "total": len(searches),
                "successful": len(successful_searches),
                "success_rate": round(len(successful_searches) / len(searches) * 100, 1) if searches else 0
            },
            "readers": {
                "total": len(readers),
                "successful": len(successful_readers),
                "success_rate": round(len(successful_readers) / len(readers) * 100, 1) if readers else 0
            },
            "performance": {
                "avg_response_time_ms": avg_response_time
            }
        }
    
    async def generate_quota_report(self) -> str:
        """Generate a comprehensive quota report"""
        status = await self.check_quota_status()
        usage_report = self.get_usage_report(30)
        
        # Format status emoji
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "🚨",
            "error": "❌"
        }.get(status.status, "❓")
        
        # Generate report
        report_lines = [
            "# Z.AI MCP Quota Status Report",
            "",
            f"**Last Updated:** {status.last_updated}",
            "",
            f"**Overall Status:** {status_emoji} {status.status.upper()}",
            "",
            "## Quota Usage",
            "",
            f"**Searches:** {status.searches_used}/{status.searches_total} "
            f"({status.searches_remaining} remaining)",
            f"**Readers:** {status.readers_used}/{status.readers_total} "
            f"({status.readers_remaining} remaining)",
            "",
            f"**Total Usage:** {status.usage_percentage}%",
            f"**Days Until Reset:** {status.days_until_reset}",
            "",
            "## Usage Trends (Last 30 Days)",
            "",
            f"**Total Operations:** {usage_report['total_operations']}",
            f"**Search Success Rate:** {usage_report['searches']['success_rate']}%",
            f"**Reader Success Rate:** {usage_report['readers']['success_rate']}%",
            ""
        ]
        
        if usage_report['performance']['avg_response_time_ms']:
            report_lines.append(
                f"**Average Response Time:** {usage_report['performance']['avg_response_time_ms']}ms"
            )
        
        # Add status-specific recommendations
        if status.status == "warning":
            report_lines.extend([
                "",
                "## Recommendations",
                "",
                "⚠️ Approaching quota limit. Consider:",
                "- Batching operations to reduce usage",
                "- Using caching for repeated queries",
                "- Planning usage around quota renewal",
                ""
            ])
        elif status.status == "critical":
            report_lines.extend([
                "",
                "## Urgent Recommendations",
                "",
                "🚨 Quota nearly exhausted. Immediate actions:",
                "- Stop non-essential operations",
                "- Switch to alternative search methods",
                "- Request quota increase if needed",
                ""
            ])
        
        return "\n".join(report_lines)


async def main():
    """Main function for CLI usage"""
    try:
        monitor = ZAIMCPQuotaMonitor()
        report = await monitor.generate_quota_report()
        print(report)
        
    except Exception as e:
        print(f"Error generating quota report: {e}")


if __name__ == "__main__":
    asyncio.run(main())
