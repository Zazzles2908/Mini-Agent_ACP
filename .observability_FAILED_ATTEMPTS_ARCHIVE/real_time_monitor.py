"""
Real-time Performance Monitoring System
Continuously tracks agent performance and provides insights
"""

import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import asyncio

@dataclass
class PerformanceSnapshot:
    timestamp: str
    success_rate: float
    avg_complexity: float
    tool_usage_distribution: Dict[str, int]
    recent_tasks: List[str]
    anomalies_detected: List[str]
    recommendations: List[str]

@dataclass
class AnomalyAlert:
    alert_type: str
    severity: str
    description: str
    timestamp: str
    suggested_action: str

class RealTimeMonitor:
    def __init__(self, observability_path: str = ".observability"):
        self.observability_path = Path(observability_path)
        self.monitoring_active = False
        self.snapshots = []
        self.alerts = []
        
        # Performance thresholds
        self.thresholds = {
            "min_success_rate": 0.7,
            "max_avg_complexity": 8.0,
            "min_daily_tasks": 5,
            "max_consecutive_failures": 3
        }
        
    def start_monitoring(self, interval_minutes: int = 30):
        """Start real-time monitoring"""
        self.monitoring_active = True
        
        async def monitor_loop():
            while self.monitoring_active:
                try:
                    await self._capture_snapshot()
                    await self._detect_anomalies()
                    await self._generate_recommendations()
                    
                    # Wait for next interval
                    await asyncio.sleep(interval_minutes * 60)
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    await asyncio.sleep(60)  # Short delay on error
        
        # In a real implementation, this would start the async monitor
        print(f"Real-time monitoring started (interval: {interval_minutes} minutes)")
        return monitor_loop()
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        print("Real-time monitoring stopped")
    
    async def _capture_snapshot(self) -> PerformanceSnapshot:
        """Capture current performance snapshot"""
        
        # Load execution history
        tracking_file = self.observability_path / "tracking_data.json"
        if not tracking_file.exists():
            return self._create_empty_snapshot()
        
        try:
            with open(tracking_file, "r") as f:
                data = json.load(f)
            
            execution_history = data.get("execution_history", [])
            
            # Calculate metrics for last 24 hours
            cutoff_time = datetime.now() - timedelta(hours=24)
            recent_executions = []
            
            for exec_data in execution_history:
                exec_time = datetime.fromisoformat(exec_data.get("timestamp", ""))
                if exec_time > cutoff_time:
                    recent_executions.append(exec_data)
            
            # Calculate success rate
            total_recent = len(recent_executions)
            successful_recent = sum(1 for exec_data in recent_executions if exec_data.get("success", False))
            success_rate = successful_recent / total_recent if total_recent > 0 else 0.0
            
            # Calculate average complexity
            complexities = [exec_data.get("complexity_score", 1) for exec_data in recent_executions]
            avg_complexity = sum(complexities) / len(complexities) if complexities else 1.0
            
            # Tool usage distribution
            tool_usage = {}
            for exec_data in recent_executions:
                tools = exec_data.get("tools_used", [])
                for tool in tools:
                    tool_usage[tool] = tool_usage.get(tool, 0) + 1
            
            # Recent tasks list
            recent_tasks = [exec_data.get("task_type", "unknown") for exec_data in recent_executions[-10:]]
            
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now().isoformat(),
                success_rate=success_rate,
                avg_complexity=avg_complexity,
                tool_usage_distribution=tool_usage,
                recent_tasks=recent_tasks,
                anomalies_detected=[],  # Will be filled by anomaly detection
                recommendations=[]  # Will be filled by recommendation generation
            )
            
            self.snapshots.append(snapshot)
            
            # Keep only last 100 snapshots
            if len(self.snapshots) > 100:
                self.snapshots = self.snapshots[-100:]
            
            return snapshot
            
        except Exception as e:
            print(f"Error capturing snapshot: {e}")
            return self._create_empty_snapshot()
    
    async def _detect_anomalies(self):
        """Detect performance anomalies"""
        
        if not self.snapshots:
            return
        
        latest_snapshot = self.snapshots[-1]
        anomalies = []
        
        # Check success rate anomaly
        if latest_snapshot.success_rate < self.thresholds["min_success_rate"]:
            anomalies.append(f"Low success rate: {latest_snapshot.success_rate:.1%} (threshold: {self.thresholds['min_success_rate']:.1%})")
        
        # Check complexity anomaly
        if latest_snapshot.avg_complexity > self.thresholds["max_avg_complexity"]:
            anomalies.append(f"High complexity: {latest_snapshot.avg_complexity:.1f} (threshold: {self.thresholds['max_avg_complexity']})")
        
        # Check activity level
        if len(latest_snapshot.recent_tasks) < self.thresholds["min_daily_tasks"]:
            anomalies.append(f"Low activity: {len(latest_snapshot.recent_tasks)} tasks (minimum: {self.thresholds['min_daily_tasks']})")
        
        # Update snapshot with anomalies
        latest_snapshot.anomalies_detected = anomalies
        
        # Create alerts for significant anomalies
        for anomaly in anomalies:
            alert = AnomalyAlert(
                alert_type="performance",
                severity="medium" if "low" in anomaly.lower() else "high",
                description=anomaly,
                timestamp=datetime.now().isoformat(),
                suggested_action=self._get_suggested_action(anomaly)
            )
            self.alerts.append(alert)
    
    async def _generate_recommendations(self):
        """Generate actionable recommendations"""
        
        if not self.snapshots:
            return
        
        latest_snapshot = self.snapshots[-1]
        recommendations = []
        
        # Performance-based recommendations
        if latest_snapshot.success_rate < 0.5:
            recommendations.append("Consider reviewing task approach - success rate critically low")
        
        if len(latest_snapshot.tool_usage_distribution) < 3:
            recommendations.append("Diversify tool usage - currently using limited set of tools")
        
        # Tool optimization recommendations
        total_usage = sum(latest_snapshot.tool_usage_distribution.values())
        if total_usage > 0:
            for tool, count in latest_snapshot.tool_usage_distribution.items():
                percentage = (count / total_usage) * 100
                if percentage > 80:
                    recommendations.append(f"Over-reliance on {tool} ({percentage:.1f} of tasks)")
        
        # Update snapshot with recommendations
        latest_snapshot.recommendations = recommendations
        
        # Log significant recommendations
        for rec in recommendations:
            if "critically" in rec.lower() or "over-reliance" in rec.lower():
                print(f"Alert: {rec}")
    
    def _get_suggested_action(self, anomaly: str) -> str:
        """Get suggested action for an anomaly"""
        
        if "success rate" in anomaly.lower():
            return "Review recent task failures and adjust approach"
        elif "complexity" in anomaly.lower():
            return "Break down complex tasks into smaller components"
        elif "activity" in anomaly.lower():
            return "Increase task execution or check for blocked processes"
        elif "over-reliance" in anomaly.lower():
            return "Explore alternative tools and approaches"
        else:
            return "Manual review required"
    
    def _create_empty_snapshot(self) -> PerformanceSnapshot:
        """Create an empty snapshot when no data is available"""
        return PerformanceSnapshot(
            timestamp=datetime.now().isoformat(),
            success_rate=0.0,
            avg_complexity=1.0,
            tool_usage_distribution={},
            recent_tasks=[],
            anomalies_detected=["No performance data available"],
            recommendations=["Start executing tasks to build baseline"]
        )
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        
        if not self.snapshots:
            return {"status": "no_data", "message": "No performance snapshots available"}
        
        latest_snapshot = self.snapshots[-1]
        
        return {
            "status": "active" if self.monitoring_active else "inactive",
            "latest_snapshot": {
                "timestamp": latest_snapshot.timestamp,
                "success_rate": latest_snapshot.success_rate,
                "avg_complexity": latest_snapshot.avg_complexity,
                "total_tools_used": len(latest_snapshot.tool_usage_distribution),
                "recent_activity": len(latest_snapshot.recent_tasks)
            },
            "alerts": self.alerts[-5:] if self.alerts else [],  # Last 5 alerts
            "recommendations": latest_snapshot.recommendations
        }
    
    def export_performance_report(self, output_file: Optional[str] = None) -> str:
        """Export comprehensive performance report"""
        
        if not output_file:
            output_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "monitoring_period": {
                "start": self.snapshots[0].timestamp if self.snapshots else None,
                "end": self.snapshots[-1].timestamp if self.snapshots else None,
                "total_snapshots": len(self.snapshots)
            },
            "summary": {
                "avg_success_rate": sum(s.success_rate for s in self.snapshots) / len(self.snapshots) if self.snapshots else 0,
                "total_alerts": len(self.alerts),
                "critical_issues": len([a for a in self.alerts if a.severity == "high"])
            },
            "snapshots": [self._snapshot_to_dict(s) for s in self.snapshots],
            "alerts": [self._alert_to_dict(a) for a in self.alerts],
            "recommendations": self.snapshots[-1].recommendations if self.snapshots else []
        }
        
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return output_file
    
    def _snapshot_to_dict(self, snapshot: PerformanceSnapshot) -> Dict[str, Any]:
        """Convert snapshot to dictionary"""
        return {
            "timestamp": snapshot.timestamp,
            "success_rate": snapshot.success_rate,
            "avg_complexity": snapshot.avg_complexity,
            "tool_usage_distribution": snapshot.tool_usage_distribution,
            "recent_tasks": snapshot.recent_tasks,
            "anomalies_detected": snapshot.anomalies_detected,
            "recommendations": snapshot.recommendations
        }
    
    def _alert_to_dict(self, alert: AnomalyAlert) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "description": alert.description,
            "timestamp": alert.timestamp,
            "suggested_action": alert.suggested_action
        }

# Global instance for agent use
real_time_monitor = RealTimeMonitor()