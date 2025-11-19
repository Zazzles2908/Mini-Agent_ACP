# Langfuse Dashboard Configuration Guide

**Date**: November 17, 2025  
**Purpose**: Configure Langfuse for comprehensive Mini-Agent observability

---

## Overview

This guide walks through setting up Langfuse dashboards for monitoring Mini-Agent tool execution, session performance, and error patterns.

## Prerequisites

- ✅ Langfuse server running on http://localhost:3000
- ✅ Supabase schema deployed with observability tables
- ✅ Mini-Agent observability client configured

---

## Task 5.1: Langfuse Dashboard Configuration

### Step 1: Access Langfuse UI

1. **Open Langfuse**: Navigate to http://localhost:3000
2. **Create Account** (first time only):
   - Email: `admin@mini-agent.local`
   - Password: Choose a strong password
   - Organization: `Mini-Agent Observability`

### Step 2: Create Mini-Agent Project

1. Click **"New Project"**
2. **Project Name**: `mini-agent-monitoring`
3. **Description**: `Real-time observability for Mini-Agent tool execution`
4. Click **"Create"**

### Step 3: Obtain API Keys

1. Go to **Settings** → **API Keys**
2. Copy and save:
   - `LANGFUSE_PUBLIC_KEY`: pk_...
   - `LANGFUSE_SECRET_KEY`: sk_...
   - `LANGFUSE_HOST`: http://localhost:3000

### Step 4: Configure Environment Variables

Create or update `.env` file in observability directory:

```bash
# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk_your_public_key_here
LANGFUSE_SECRET_KEY=sk_your_secret_key_here
LANGFUSE_HOST=http://localhost:3000

# Supabase Configuration (already configured)
SUPABASE_URL=https://mxaazuhlqewmkweewyaz.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### Step 5: Configure Custom Metrics

#### Agent-Specific Dashboards

Create custom views in Langfuse:

1. **Tool Execution Dashboard**
   - Metric: Tool execution count by tool name
   - Visualization: Bar chart
   - Time Range: Last 24 hours
   - Grouping: By tool category (file, mcp, document, skill)

2. **Session Performance Dashboard**
   - Metric: Average session duration
   - Visualization: Line chart
   - Time Range: Last 7 days
   - Grouping: By session outcome (success/failure)

3. **Error Tracking Dashboard**
   - Metric: Error rate by error type
   - Visualization: Pie chart
   - Time Range: Last 24 hours
   - Alerting: Email on error rate > 5%

### Step 6: Set Up Alerting

Configure proactive issue detection:

1. **High Error Rate Alert**
   - Condition: Error rate > 5% over 1 hour
   - Action: Email notification
   - Recipients: Admin team

2. **Slow Tool Execution Alert**
   - Condition: Tool execution time > 30s (95th percentile)
   - Action: Slack notification
   - Channel: #mini-agent-ops

3. **Session Failure Alert**
   - Condition: Session failure rate > 10% over 4 hours
   - Action: PagerDuty incident
   - Severity: High

### Step 7: Configure Data Filtering

Set up filters for focused observability:

```python
# Filter Configuration
FILTERS = {
    "production_only": {
        "environment": "production",
        "exclude_test_sessions": True
    },
    "error_sessions_only": {
        "status": "error",
        "min_duration": 1  # Only sessions > 1 second
    },
    "high_value_tools": {
        "tool_categories": ["mcp", "workflow", "consensus"],
        "exclude_basic": True
    }
}
```

---

## Task 5.2: Custom Visualization

### Dashboard 1: Agent Performance Overview

**Purpose**: Real-time session success rates and latency trends

**Metrics**:
- Session success rate (24h rolling)
- Average session duration
- Tool execution count
- Active sessions (real-time)

**Visualization Setup**:

```python
# Custom Langfuse Query for Agent Performance
from langfuse import Langfuse

langfuse = Langfuse()

# Session Success Rate
success_rate = langfuse.get_dataset(
    name="session_metrics",
    filters={"timerange": "24h"},
    aggregation="success_rate"
)

# Session Duration Trends
duration_trends = langfuse.get_traces(
    name="mini_agent_session",
    group_by="hour",
    metric="avg_duration"
)
```

**Dashboard Layout**:
```
┌─────────────────────────────────────────────────────┐
│  Session Success Rate (24h)          95.3%         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
├─────────────────────────────────────────────────────┤
│  Average Latency (p50/p95)      1.2s / 4.5s        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
├─────────────────────────────────────────────────────┤
│  Tool Executions (24h)               1,247         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
└─────────────────────────────────────────────────────┘
```

### Dashboard 2: Tool Usage Analytics

**Purpose**: Identify most/least effective tools

**Metrics**:
- Tool execution frequency
- Tool success rate by category
- Average execution time per tool
- Tool usage trends over time

**Visualization Setup**:

```python
# Tool Usage Query
tool_usage = langfuse.get_spans(
    name_contains="tool_execution",
    group_by="metadata.tool_name",
    metrics=["count", "success_rate", "avg_duration"]
)

# Top 10 Most Used Tools
top_tools = tool_usage.sort_by("count", descending=True).limit(10)

# Bottom 10 Least Effective Tools (by success rate)
least_effective = tool_usage.sort_by("success_rate", ascending=True).limit(10)
```

**Dashboard Layout**:
```
┌─────────────────────────────────────────────────────┐
│  Top 10 Most Used Tools                             │
│  1. read_file           847 executions (98.2%)      │
│  2. write_file          623 executions (96.5%)      │
│  3. chat                412 executions (99.1%)      │
│  4. bash                389 executions (92.3%)      │
│  5. edit_file           301 executions (95.7%)      │
│  ...                                                 │
├─────────────────────────────────────────────────────┤
│  Tools Needing Attention (Low Success Rate)         │
│  1. complex_tool_x       45% success rate           │
│  2. flaky_integration    67% success rate           │
│  ...                                                 │
└─────────────────────────────────────────────────────┘
```

### Dashboard 3: Error Pattern Analysis

**Purpose**: Common failure modes and root cause analysis

**Metrics**:
- Error count by error type
- Error frequency over time
- Most common error messages
- Error resolution time

**Visualization Setup**:

```python
# Error Pattern Query
error_patterns = langfuse.get_observations(
    type="event",
    level="ERROR",
    group_by="metadata.error_type"
)

# Error Timeline
error_timeline = langfuse.get_traces(
    status="ERROR",
    group_by="hour",
    metric="count"
)
```

**Dashboard Layout**:
```
┌─────────────────────────────────────────────────────┐
│  Error Distribution (24h)                           │
│  ■■■■■■ Timeout Errors          45%                 │
│  ■■■■  Network Errors           30%                 │
│  ■■    Permission Errors        15%                 │
│  ■     Other                    10%                 │
├─────────────────────────────────────────────────────┤
│  Error Timeline (Last 7 Days)                       │
│  Mon  ▁▂▃▂▁  12 errors                              │
│  Tue  ▁▁▂▁▁   8 errors                              │
│  Wed  ▃▅▇▅▃  23 errors ⚠️                           │
│  ...                                                 │
└─────────────────────────────────────────────────────┘
```

---

## Task 5.3: Automated Reporting

### Daily Summary Report

**Schedule**: Every day at 9:00 AM  
**Recipients**: Admin team, stakeholders  
**Content**:

```python
# daily_summary.py
from langfuse import Langfuse
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

def generate_daily_summary():
    langfuse = Langfuse()
    yesterday = datetime.now() - timedelta(days=1)
    
    # Fetch metrics
    sessions = langfuse.get_traces(
        name="mini_agent_session",
        timestamp_gte=yesterday.isoformat()
    )
    
    tool_executions = langfuse.get_spans(
        name_contains="tool_execution",
        timestamp_gte=yesterday.isoformat()
    )
    
    errors = langfuse.get_observations(
        level="ERROR",
        timestamp_gte=yesterday.isoformat()
    )
    
    # Generate report
    report = f"""
    Mini-Agent Daily Summary - {yesterday.strftime('%Y-%m-%d')}
    
    📊 SESSION METRICS
    - Total Sessions: {sessions.count()}
    - Success Rate: {sessions.success_rate():.1%}
    - Avg Duration: {sessions.avg_duration():.2f}s
    
    🔧 TOOL EXECUTION
    - Total Executions: {tool_executions.count()}
    - Most Used: {tool_executions.most_common()[0]}
    - Success Rate: {tool_executions.success_rate():.1%}
    
    ⚠️ ERRORS
    - Total Errors: {errors.count()}
    - Error Rate: {errors.count() / tool_executions.count():.2%}
    - Top Error: {errors.most_common_type()}
    
    📈 TRENDS
    - Sessions vs Yesterday: {sessions.compare_previous_period()}
    - Tool Usage vs Yesterday: {tool_executions.compare_previous_period()}
    """
    
    return report

def send_email_report(report):
    msg = MIMEText(report)
    msg['Subject'] = f'Mini-Agent Daily Summary - {datetime.now().strftime("%Y-%m-%d")}'
    msg['From'] = 'observability@mini-agent.local'
    msg['To'] = 'admin@mini-agent.local'
    
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)

if __name__ == "__main__":
    report = generate_daily_summary()
    print(report)
    send_email_report(report)
```

**Cron Schedule**:
```bash
# Add to crontab
0 9 * * * cd /path/to/observability && python daily_summary.py
```

### Weekly Analysis Report

**Schedule**: Every Monday at 10:00 AM  
**Purpose**: Performance patterns and insights

```python
# weekly_analysis.py
def generate_weekly_analysis():
    langfuse = Langfuse()
    last_week = datetime.now() - timedelta(days=7)
    
    # Trend analysis
    trends = langfuse.get_trends(
        timerange="7d",
        metrics=["session_count", "success_rate", "avg_duration"]
    )
    
    # Performance patterns
    patterns = langfuse.analyze_patterns(
        timerange="7d",
        group_by=["day_of_week", "hour_of_day"]
    )
    
    report = f"""
    Mini-Agent Weekly Analysis - Week of {last_week.strftime('%Y-%m-%d')}
    
    📊 WEEK OVERVIEW
    - Total Sessions: {trends.total_sessions}
    - Week-over-Week Growth: {trends.wow_growth:.1%}
    - Success Rate: {trends.avg_success_rate:.1%}
    
    📈 KEY PATTERNS
    - Busiest Day: {patterns.busiest_day}
    - Peak Hour: {patterns.peak_hour}
    - Most Active Tool Category: {patterns.top_category}
    
    ⚡ PERFORMANCE INSIGHTS
    - Fastest Tool: {patterns.fastest_tool} ({patterns.fastest_time}s)
    - Slowest Tool: {patterns.slowest_tool} ({patterns.slowest_time}s)
    - Bottleneck Identified: {patterns.bottleneck}
    
    🎯 RECOMMENDATIONS
    {generate_recommendations(patterns)}
    """
    
    return report
```

### Anomaly Detection

**Purpose**: Automated issue identification  
**Method**: Statistical analysis + ML-based detection

```python
# anomaly_detection.py
from langfuse import Langfuse
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies():
    langfuse = Langfuse()
    
    # Get recent metrics
    metrics = langfuse.get_metrics(
        timerange="24h",
        granularity="5min"
    )
    
    # Prepare data
    X = np.array([
        metrics.session_count,
        metrics.error_rate,
        metrics.avg_duration
    ]).T
    
    # Train anomaly detector
    detector = IsolationForest(contamination=0.1)
    anomalies = detector.fit_predict(X)
    
    # Identify anomalous periods
    anomalous_periods = []
    for i, is_anomaly in enumerate(anomalies):
        if is_anomaly == -1:
            anomalous_periods.append({
                "timestamp": metrics.timestamps[i],
                "session_count": metrics.session_count[i],
                "error_rate": metrics.error_rate[i],
                "avg_duration": metrics.avg_duration[i]
            })
    
    # Send alerts
    if anomalous_periods:
        send_anomaly_alert(anomalous_periods)
    
    return anomalous_periods
```

---

## Integration with Mini-Agent

### Update Observability Client

Add Langfuse integration to existing client:

```python
# client.py - Add after existing code
from langfuse import Langfuse

class MiniAgentObservability:
    def __init__(self):
        # Existing initialization...
        
        # Add Langfuse
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
        )
    
    def log_tool_execution(self, tool_name, inputs, outputs, duration):
        # Existing Supabase logging...
        
        # Add Langfuse trace
        trace = self.langfuse.trace(
            name="mini_agent_session",
            metadata={"session_id": self.session_id}
        )
        
        span = trace.span(
            name=f"tool_execution_{tool_name}",
            input=inputs,
            output=outputs,
            metadata={
                "duration": duration,
                "tool_category": self._get_tool_category(tool_name)
            }
        )
        
        span.end()
```

---

## Testing Dashboard Configuration

Run validation test:

```bash
cd C:\Users\Jazeel-Home\.mini-agent\observability
python test_langfuse_integration.py
```

Expected output:
```
✅ Langfuse connection successful
✅ Trace creation working
✅ Dashboard data visible
✅ All metrics configured
```

---

## Next Steps

1. ✅ Complete Langfuse account setup
2. ✅ Copy API keys to environment
3. ✅ Run integration test
4. ✅ Configure custom dashboards
5. ✅ Set up automated reports
6. ✅ Enable anomaly detection

**Status**: Phase 5 configuration ready for deployment!
