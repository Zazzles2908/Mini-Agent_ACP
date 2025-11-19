"""
Intelligent Decision-Making System
Uses self-awareness data to make better strategic decisions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DecisionContext:
    task_description: str
    available_tools: List[str]
    constraints: List[str]
    success_requirements: List[str]

@dataclass
class IntelligentDecision:
    chosen_tool: str
    reasoning: str
    confidence: float
    alternatives_considered: List[str]
    expected_outcome: str

class IntelligentDecisionMaker:
    def __init__(self, observability_path: str = ".observability"):
        self.observability_path = Path(observability_path)
        self.config_file = self.observability_path / "ai_agent_config.json"
        
        # Load configuration
        self._load_config()
        
        # Decision templates and patterns
        self.tool_preferences = self._initialize_tool_preferences()
        self.pattern_matching = {}
    
    def make_intelligent_decision(self, context: DecisionContext) -> IntelligentDecision:
        """Make an intelligent decision based on self-awareness and patterns"""
        
        # Analyze context and match against historical patterns
        pattern_match = self._find_pattern_match(context)
        
        # Score available tools based on success history
        tool_scores = self._score_tools(context.available_tools, context.task_description)
        
        # Consider constraints and requirements
        constrained_scores = self._apply_constraints(tool_scores, context.constraints)
        
        # Select best tool with reasoning
        if constrained_scores:
            best_tool = max(constrained_scores, key=constrained_scores.get)
            confidence = constrained_scores[best_tool]
            
            alternatives = sorted([tool for tool, score in constrained_scores.items() if tool != best_tool], 
                                key=constrained_scores.get, reverse=True)[:2]
            
            reasoning = self._generate_reasoning(best_tool, context, pattern_match, confidence)
            
            decision = IntelligentDecision(
                chosen_tool=best_tool,
                reasoning=reasoning,
                confidence=confidence,
                alternatives_considered=alternatives,
                expected_outcome=f"Expected high success rate ({confidence:.1%}) based on historical patterns"
            )
        else:
            # Fallback to primary tool with default reasoning
            decision = IntelligentDecision(
                chosen_tool=context.available_tools[0] if context.available_tools else "bash",
                reasoning="No historical data available - using fallback strategy",
                confidence=0.5,
                alternatives_considered=context.available_tools[1:2] if len(context.available_tools) > 1 else [],
                expected_outcome="Standard expected outcome"
            )
        
        # Log the decision for pattern learning
        self._log_decision(context, decision)
        
        return decision
    
    def _find_pattern_match(self, context: DecisionContext) -> Optional[Dict]:
        """Find matching patterns from historical data"""
        
        # Load execution history
        tracking_file = self.observability_path / "tracking_data.json"
        if not tracking_file.exists():
            return None
        
        try:
            with open(tracking_file, "r") as f:
                data = json.load(f)
            
            # Look for similar task types
            execution_history = data.get("execution_history", [])
            
            # Find patterns by task description keywords
            context_words = set(context.task_description.lower().split())
            best_matches = []
            
            for execution in execution_history:
                task_type = execution.get("task_type", "")
                if any(word in task_type.lower() for word in context_words):
                    success = execution.get("success", False)
                    tools_used = execution.get("tools_used", [])
                    if tools_used and success:
                        best_matches.append({
                            "task_type": task_type,
                            "successful_tools": tools_used,
                            "confidence": self._calculate_pattern_confidence(execution)
                        })
            
            # Return the best match
            if best_matches:
                return max(best_matches, key=lambda x: x["confidence"])
            
        except Exception as e:
            print(f"Warning: Could not load pattern data: {e}")
        
        return None
    
    def _score_tools(self, tools: List[str], task_description: str) -> Dict[str, float]:
        """Score tools based on historical success"""
        
        if not tools:
            return {}
        
        # Load execution history
        tracking_file = self.observability_path / "tracking_data.json"
        scores = {tool: 0.5 for tool in tools}  # Base score
        
        if not tracking_file.exists():
            return scores
        
        try:
            with open(tracking_file, "r") as f:
                data = json.load(f)
            
            execution_history = data.get("execution_history", [])
            
            # Calculate success rates for each tool
            for tool in tools:
                tool_executions = [exec for exec in execution_history if tool in exec.get("tools_used", [])]
                if tool_executions:
                    success_count = sum(1 for exec in tool_executions if exec.get("success", False))
                    success_rate = success_count / len(tool_executions)
                    
                    # Boost score for recent successful uses
                    recent_executions = tool_executions[-5:]  # Last 5 uses
                    recent_success_rate = sum(1 for exec in recent_executions if exec.get("success", False)) / len(recent_executions) if recent_executions else 0
                    
                    # Weighted score (recent performance + historical)
                    scores[tool] = (recent_success_rate * 0.7 + success_rate * 0.3)
                
        except Exception as e:
            print(f"Warning: Could not calculate tool scores: {e}")
        
        return scores
    
    def _apply_constraints(self, tool_scores: Dict[str, float], constraints: List[str]) -> Dict[str, float]:
        """Apply constraints to tool selection"""
        
        constrained_scores = tool_scores.copy()
        
        # Handle file operations constraints
        if any("file" in constraint.lower() for constraint in constraints):
            file_tools = ["read_file", "write_file", "edit_file", "search_files"]
            for tool in tool_scores:
                if tool not in file_tools:
                    constrained_scores[tool] *= 0.3  # Penalize non-file tools
        
        # Handle command execution constraints
        if any("command" in constraint.lower() for constraint in constraints):
            command_tools = ["bash", "command"]
            for tool in tool_scores:
                if tool in command_tools:
                    constrained_scores[tool] *= 1.2  # Boost command tools
        
        return constrained_scores
    
    def _generate_reasoning(self, chosen_tool: str, context: DecisionContext, 
                          pattern_match: Optional[Dict], confidence: float) -> str:
        """Generate reasoning for the decision"""
        
        reasons = []
        
        # Base confidence reasoning
        if confidence > 0.8:
            reasons.append("High confidence based on recent successful pattern")
        elif confidence > 0.6:
            reasons.append("Good confidence based on historical data")
        else:
            reasons.append("Moderate confidence - limited historical data")
        
        # Pattern-based reasoning
        if pattern_match:
            reasons.append(f"Similar tasks have succeeded with this approach")
        
        # Tool-specific reasoning
        tool_reasons = {
            "read_file": "Direct file access is most efficient",
            "write_file": "File creation is the primary requirement",
            "bash": "Command execution is required",
            "search": "Web search is needed for information gathering",
            "browse": "Content extraction from web sources"
        }
        
        if chosen_tool in tool_reasons:
            reasons.append(tool_reasons[chosen_tool])
        
        return "; ".join(reasons)
    
    def _calculate_pattern_confidence(self, execution: Dict) -> float:
        """Calculate confidence score for a pattern match"""
        
        # Base confidence from execution success
        base_confidence = 0.8 if execution.get("success", False) else 0.3
        
        # Boost for recent executions (within last day)
        try:
            timestamp = execution.get("timestamp", "")
            if timestamp:
                # Simple time-based boost (in real implementation, would parse and compare)
                base_confidence *= 1.1
        except:
            pass
        
        return min(base_confidence, 1.0)
    
    def _log_decision(self, context: DecisionContext, decision: IntelligentDecision):
        """Log decision for pattern learning"""
        
        # In a full implementation, this would integrate with the self-awareness system
        # For now, we'll create a simple log entry
        log_entry = {
            "timestamp": str(datetime.now()),
            "context": context.task_description,
            "chosen_tool": decision.chosen_tool,
            "confidence": decision.confidence,
            "reasoning": decision.reasoning
        }
        
        # This would be logged to the self-awareness system
        print(f"Decision logged: {json.dumps(log_entry, indent=2)}")
    
    def _initialize_tool_preferences(self) -> Dict[str, float]:
        """Initialize baseline tool preferences"""
        
        return {
            "read_file": 0.8,
            "write_file": 0.7,
            "bash": 0.6,
            "search": 0.7,
            "browse": 0.8,
            "list_directory": 0.7,
            "create_directory": 0.6,
            "edit_file": 0.7
        }
    
    def _load_config(self):
        """Load agent configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {}

# Global instance for agent use
decision_maker = IntelligentDecisionMaker()