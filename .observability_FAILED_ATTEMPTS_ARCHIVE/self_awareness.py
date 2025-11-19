"""
Self-Awareness and Observability System for Mini-Agent
Enables the agent to track its own performance, patterns, and evolution
"""

import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ExecutionMetrics:
    task_id: str
    timestamp: str
    task_type: str
    tools_used: List[str]
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    complexity_score: int = 1
    context_quality: float = 0.5

@dataclass
class DecisionRecord:
    decision_id: str
    timestamp: str
    context: str
    options_considered: List[str]
    chosen_option: str
    reasoning: str
    outcome_quality: float
    confidence_level: float

@dataclass
class CapabilityInsight:
    insight_id: str
    timestamp: str
    capability_type: str
    discovery: str
    impact_score: float
    implementation_status: str

class SelfAwarenessSystem:
    def __init__(self, base_path: str = ".observability"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Initialize tracking structures
        self.execution_history = []
        self.decision_patterns = {}
        self.capability_insights = []
        self.performance_trends = {}
        
        # Load existing data if available
        self._load_tracking_data()
    
    def record_execution(self, task_type: str, tools_used: List[str], 
                        success: bool, complexity_score: int = 1,
                        error_message: Optional[str] = None) -> str:
        """Record an execution attempt with metrics"""
        
        task_id = f"task_{int(time.time())}_{task_type}"
        execution = ExecutionMetrics(
            task_id=task_id,
            timestamp=datetime.now().isoformat(),
            task_type=task_type,
            tools_used=tools_used,
            execution_time=0.0,  # Will be updated externally
            success=success,
            error_message=error_message,
            complexity_score=complexity_score,
            context_quality=0.7  # Will be calculated
        )
        
        self.execution_history.append(execution)
        self._update_performance_trends(execution)
        self._save_tracking_data()
        
        return task_id
    
    def record_decision(self, context: str, options_considered: List[str],
                       chosen_option: str, reasoning: str,
                       confidence_level: float = 0.7) -> str:
        """Record a significant decision for pattern analysis"""
        
        decision_id = f"decision_{int(time.time())}"
        decision = DecisionRecord(
            decision_id=decision_id,
            timestamp=datetime.now().isoformat(),
            context=context,
            options_considered=options_considered,
            chosen_option=chosen_option,
            reasoning=reasoning,
            outcome_quality=0.0,  # Will be updated when outcome is known
            confidence_level=confidence_level
        )
        
        # Update decision patterns
        pattern_key = f"{context}_{chosen_option}"
        if pattern_key not in self.decision_patterns:
            self.decision_patterns[pattern_key] = []
        self.decision_patterns[pattern_key].append(decision)
        
        self._save_tracking_data()
        return decision_id
    
    def add_capability_insight(self, capability_type: str, discovery: str,
                              impact_score: float = 0.5) -> str:
        """Record a new capability discovery or insight"""
        
        insight_id = f"insight_{int(time.time())}_{capability_type}"
        insight = CapabilityInsight(
            insight_id=insight_id,
            timestamp=datetime.now().isoformat(),
            capability_type=capability_type,
            discovery=discovery,
            impact_score=impact_score,
            implementation_status="discovered"
        )
        
        self.capability_insights.append(insight)
        self._save_tracking_data()
        return insight_id
    
    def get_performance_analysis(self) -> Dict[str, Any]:
        """Generate performance analysis and recommendations"""
        
        if not self.execution_history:
            return {"status": "no_data"}
        
        total_tasks = len(self.execution_history)
        successful_tasks = sum(1 for ex in self.execution_history if ex.success)
        success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0
        
        # Analyze tool usage patterns
        tool_usage = {}
        for execution in self.execution_history:
            for tool in execution.tools_used:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        # Most/least used tools
        most_used_tool = max(tool_usage, key=tool_usage.get) if tool_usage else None
        least_used_tool = min(tool_usage, key=tool_usage.get) if tool_usage else None
        
        return {
            "success_rate": success_rate,
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "tool_usage": tool_usage,
            "most_effective_tool": most_used_tool,
            "underutilized_tools": least_used_tool,
            "complexity_distribution": self._analyze_complexity_distribution(),
            "recommendations": self._generate_recommendations()
        }
    
    def get_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision-making patterns"""
        
        if not self.decision_patterns:
            return {"status": "no_decision_data"}
        
        patterns = {}
        for pattern_key, decisions in self.decision_patterns.items():
            avg_confidence = sum(d.confidence_level for d in decisions) / len(decisions)
            avg_outcome = sum(d.outcome_quality for d in decisions) / len(decisions)
            
            patterns[pattern_key] = {
                "frequency": len(decisions),
                "avg_confidence": avg_confidence,
                "avg_outcome": avg_outcome,
                "consistency": 1.0 - (self._calculate_variance([d.outcome_quality for d in decisions]) if len(decisions) > 1 else 0.0)
            }
        
        return patterns
    
    def _analyze_complexity_distribution(self) -> Dict[str, int]:
        """Analyze task complexity distribution"""
        distribution = {}
        for execution in self.execution_history:
            complexity = execution.complexity_score
            distribution[complexity] = distribution.get(complexity, 0) + 1
        return distribution
    
    def _generate_recommendations(self) -> List[str]:
        """Generate improvement recommendations based on patterns"""
        recommendations = []
        
        if not self.execution_history:
            return ["Start executing tasks to build performance baseline"]
        
        # Success rate recommendations
        recent_tasks = self.execution_history[-10:]  # Last 10 tasks
        if recent_tasks:
            recent_success_rate = sum(1 for t in recent_tasks if t.success) / len(recent_tasks)
            if recent_success_rate < 0.7:
                recommendations.append("Consider reviewing task approach - recent success rate below 70%")
        
        # Tool usage recommendations
        tool_usage = {}
        for execution in self.execution_history:
            for tool in execution.tools_used:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        if len(tool_usage) < 5:
            recommendations.append("Explore more diverse tool usage patterns")
        
        return recommendations
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if len(values) <= 1:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _update_performance_trends(self, execution: ExecutionMetrics):
        """Update performance trend tracking"""
        date_key = execution.timestamp[:10]  # YYYY-MM-DD
        
        if date_key not in self.performance_trends:
            self.performance_trends[date_key] = {"total": 0, "successful": 0}
        
        self.performance_trends[date_key]["total"] += 1
        if execution.success:
            self.performance_trends[date_key]["successful"] += 1
    
    def _save_tracking_data(self):
        """Save all tracking data to files"""
        data = {
            "execution_history": [asdict(exec) for exec in self.execution_history],
            "decision_patterns": {k: [asdict(d) for d in v] for k, v in self.decision_patterns.items()},
            "capability_insights": [asdict(insight) for insight in self.capability_insights],
            "performance_trends": self.performance_trends
        }
        
        with open(self.base_path / "tracking_data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def _load_tracking_data(self):
        """Load existing tracking data"""
        data_file = self.base_path / "tracking_data.json"
        if data_file.exists():
            try:
                with open(data_file, "r") as f:
                    data = json.load(f)
                
                # Reconstruct objects (simplified for this implementation)
                self.execution_history = data.get("execution_history", [])
                # Reconstruct decision patterns
                decision_patterns_data = data.get("decision_patterns", {})
                self.decision_patterns = {}
                for pattern_key, decisions_data in decision_patterns_data.items():
                    decisions = []
                    for decision_data in decisions_data:
                        if isinstance(decision_data, dict):
                            decision = DecisionRecord(**decision_data)
                            decisions.append(decision)
                        else:
                            decisions.append(decision_data)  # Already a DecisionRecord
                    self.decision_patterns[pattern_key] = decisions
                
                # Reconstruct capability insights
                capability_insights_data = data.get("capability_insights", [])
                self.capability_insights = []
                for insight_data in capability_insights_data:
                    if isinstance(insight_data, dict):
                        insight = CapabilityInsight(**insight_data)
                        self.capability_insights.append(insight)
                    else:
                        self.capability_insights.append(insight_data)  # Already a dataclass
                
                self.performance_trends = data.get("performance_trends", {})
            except Exception as e:
                print(f"Warning: Could not load tracking data: {e}")

# Global instance for agent use
self_awareness = SelfAwarenessSystem()