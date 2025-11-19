-- Mini-Agent Observability Schema
-- Run this in Supabase Studio SQL Editor

-- Create dedicated schema for Mini-Agent observability
CREATE SCHEMA IF NOT EXISTS mini_agent_observability;

-- Agent sessions (root traces)
CREATE TABLE mini_agent_observability.traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    agent_version TEXT,
    user_context TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Individual tool executions
CREATE TABLE mini_agent_observability.tool_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id UUID REFERENCES mini_agent_observability.traces(id) ON DELETE CASCADE,
    tool_name TEXT NOT NULL,
    category TEXT, -- 'core', 'file', 'mcp', 'document', 'skill'
    input JSONB,
    output JSONB,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    duration_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Performance metrics
CREATE TABLE mini_agent_observability.performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id UUID REFERENCES mini_agent_observability.traces(id) ON DELETE CASCADE,
    metric_type TEXT NOT NULL, -- 'token_usage', 'latency', 'cost', 'memory'
    metric_value NUMERIC NOT NULL,
    unit TEXT, -- 'tokens', 'ms', 'usd', 'mb'
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent decisions (for transparency)
CREATE TABLE mini_agent_observability.decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id UUID REFERENCES mini_agent_observability.traces(id) ON DELETE CASCADE,
    decision_type TEXT NOT NULL, -- 'tool_selection', 'parameter_choice', 'error_handling'
    considered_options JSONB, -- Array of alternatives
    selected_option TEXT,
    reasoning TEXT,
    confidence_score NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_traces_session_id ON mini_agent_observability.traces(session_id);
CREATE INDEX idx_traces_started_at ON mini_agent_observability.traces(started_at DESC);
CREATE INDEX idx_tool_executions_trace_id ON mini_agent_observability.tool_executions(trace_id);
CREATE INDEX idx_tool_executions_tool_name ON mini_agent_observability.tool_executions(tool_name);
CREATE INDEX idx_tool_executions_category ON mini_agent_observability.tool_executions(category);
CREATE INDEX idx_tool_executions_start_time ON mini_agent_observability.tool_executions(start_time DESC);
CREATE INDEX idx_performance_metrics_trace_id ON mini_agent_observability.performance_metrics(trace_id);
CREATE INDEX idx_decisions_trace_id ON mini_agent_observability.decisions(trace_id);

-- Row Level Security (RLS)
ALTER TABLE mini_agent_observability.traces ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent_observability.tool_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent_observability.performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent_observability.decisions ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations for authenticated users
CREATE POLICY "Allow all for authenticated users" ON mini_agent_observability.traces
    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "Allow all for authenticated users" ON mini_agent_observability.tool_executions
    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "Allow all for authenticated users" ON mini_agent_observability.performance_metrics
    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "Allow all for authenticated users" ON mini_agent_observability.decisions
    FOR ALL USING (auth.role() = 'authenticated');

-- Comments for documentation
COMMENT ON SCHEMA mini_agent_observability IS 'Mini-Agent observability data - all tool executions, performance metrics, and agent decisions';
COMMENT ON TABLE mini_agent_observability.traces IS 'Root traces for agent sessions';
COMMENT ON TABLE mini_agent_observability.tool_executions IS 'Individual tool execution records with success/failure tracking';
COMMENT ON TABLE mini_agent_observability.performance_metrics IS 'Performance and resource usage metrics';
COMMENT ON TABLE mini_agent_observability.decisions IS 'Agent decision-making transparency logs';
