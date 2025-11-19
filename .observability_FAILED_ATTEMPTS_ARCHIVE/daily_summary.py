"""
Automated Daily Summary Report Generator

Generates daily observability summaries from Supabase data.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from supabase import create_client, Client

class DailySummaryGenerator:
    """Generate daily observability summaries."""
    
    def __init__(self):
        """Initialize Supabase client."""
        self.supabase_url = os.getenv(
            "SUPABASE_URL",
            "https://mxaazuhlqewmkweewyaz.supabase.co"
        )
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.supabase_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY not set")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def fetch_session_metrics(self, date: datetime) -> Dict:
        """Fetch session metrics for a given date."""
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)
        
        # Query traces
        result = self.supabase.table("agent_traces") \
            .select("*") \
            .gte("start_time", start_time.isoformat()) \
            .lt("start_time", end_time.isoformat()) \
            .execute()
        
        traces = result.data
        
        total_sessions = len(traces)
        successful_sessions = sum(1 for t in traces if t.get("status") == "success")
        avg_duration = sum(t.get("duration", 0) for t in traces) / total_sessions if total_sessions > 0 else 0
        
        return {
            "total_sessions": total_sessions,
            "successful_sessions": successful_sessions,
            "success_rate": successful_sessions / total_sessions if total_sessions > 0 else 0,
            "avg_duration": avg_duration
        }
    
    def fetch_tool_metrics(self, date: datetime) -> Dict:
        """Fetch tool execution metrics for a given date."""
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)
        
        # Query tool executions
        result = self.supabase.table("agent_tool_executions") \
            .select("*") \
            .gte("start_time", start_time.isoformat()) \
            .lt("start_time", end_time.isoformat()) \
            .execute()
        
        executions = result.data
        
        total_executions = len(executions)
        successful_executions = sum(1 for e in executions if e.get("status") == "success")
        
        # Count by tool name
        tool_counts = {}
        for execution in executions:
            tool_name = execution.get("tool_name", "unknown")
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        most_used_tool = max(tool_counts.items(), key=lambda x: x[1]) if tool_counts else ("none", 0)
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "most_used_tool": most_used_tool[0],
            "most_used_count": most_used_tool[1],
            "unique_tools": len(tool_counts)
        }
    
    def fetch_error_metrics(self, date: datetime) -> Dict:
        """Fetch error metrics for a given date."""
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)
        
        # Query decisions (which track errors)
        result = self.supabase.table("agent_decisions") \
            .select("*") \
            .gte("timestamp", start_time.isoformat()) \
            .lt("timestamp", end_time.isoformat()) \
            .execute()
        
        decisions = result.data
        
        errors = [d for d in decisions if "error" in d.get("decision_type", "").lower()]
        
        # Count by error type
        error_types = {}
        for error in errors:
            error_type = error.get("decision_type", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        top_error = max(error_types.items(), key=lambda x: x[1]) if error_types else ("none", 0)
        
        return {
            "total_errors": len(errors),
            "unique_error_types": len(error_types),
            "top_error_type": top_error[0],
            "top_error_count": top_error[1]
        }
    
    def calculate_trends(self, date: datetime, session_metrics: Dict, tool_metrics: Dict) -> Dict:
        """Calculate trends compared to previous day."""
        prev_date = date - timedelta(days=1)
        
        try:
            prev_session_metrics = self.fetch_session_metrics(prev_date)
            prev_tool_metrics = self.fetch_tool_metrics(prev_date)
            
            session_change = ((session_metrics["total_sessions"] - prev_session_metrics["total_sessions"]) 
                            / prev_session_metrics["total_sessions"] * 100 
                            if prev_session_metrics["total_sessions"] > 0 else 0)
            
            tool_change = ((tool_metrics["total_executions"] - prev_tool_metrics["total_executions"]) 
                         / prev_tool_metrics["total_executions"] * 100 
                         if prev_tool_metrics["total_executions"] > 0 else 0)
            
            return {
                "session_change_pct": session_change,
                "tool_change_pct": tool_change
            }
        except Exception as e:
            print(f"[WARN] Could not calculate trends: {e}")
            return {
                "session_change_pct": 0,
                "tool_change_pct": 0
            }
    
    def generate_report(self, date: datetime = None) -> str:
        """Generate daily summary report."""
        if date is None:
            date = datetime.now() - timedelta(days=1)  # Yesterday
        
        print(f"Generating report for {date.strftime('%Y-%m-%d')}...")
        
        # Fetch metrics
        session_metrics = self.fetch_session_metrics(date)
        tool_metrics = self.fetch_tool_metrics(date)
        error_metrics = self.fetch_error_metrics(date)
        trends = self.calculate_trends(date, session_metrics, tool_metrics)
        
        # Calculate error rate
        error_rate = (error_metrics["total_errors"] / tool_metrics["total_executions"] * 100 
                     if tool_metrics["total_executions"] > 0 else 0)
        
        # Generate report
        report = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║  Mini-Agent Daily Summary - {date.strftime('%Y-%m-%d')}                    ║
╚═══════════════════════════════════════════════════════════════════════╝

📊 SESSION METRICS
  • Total Sessions: {session_metrics['total_sessions']}
  • Success Rate: {session_metrics['success_rate']:.1%}
  • Avg Duration: {session_metrics['avg_duration']:.2f}s
  • Trend: {trends['session_change_pct']:+.1f}% vs yesterday

🔧 TOOL EXECUTION
  • Total Executions: {tool_metrics['total_executions']}
  • Unique Tools Used: {tool_metrics['unique_tools']}
  • Most Used: {tool_metrics['most_used_tool']} ({tool_metrics['most_used_count']} times)
  • Success Rate: {tool_metrics['success_rate']:.1%}
  • Trend: {trends['tool_change_pct']:+.1f}% vs yesterday

⚠️  ERRORS & ISSUES
  • Total Errors: {error_metrics['total_errors']}
  • Error Rate: {error_rate:.2f}%
  • Unique Error Types: {error_metrics['unique_error_types']}
  • Top Error: {error_metrics['top_error_type']} ({error_metrics['top_error_count']} occurrences)

📈 KEY INSIGHTS
  • System Health: {"✅ Excellent" if session_metrics['success_rate'] > 0.95 else "⚠️ Needs Attention"}
  • Performance: {"✅ Good" if session_metrics['avg_duration'] < 5 else "⚠️ Slow"}
  • Error Rate: {"✅ Low" if error_rate < 5 else "⚠️ High"}

═══════════════════════════════════════════════════════════════════════

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report

def main():
    """Main entry point."""
    print("=" * 70)
    print("MINI-AGENT DAILY SUMMARY GENERATOR")
    print("=" * 70)
    
    try:
        generator = DailySummaryGenerator()
        
        # Generate report for yesterday
        report = generator.generate_report()
        
        print(report)
        
        # Save to file
        date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        filename = f"daily_summary_{date_str}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
