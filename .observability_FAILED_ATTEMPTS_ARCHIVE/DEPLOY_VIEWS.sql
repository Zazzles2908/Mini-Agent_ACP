-- Mini-Agent Observability Public Views Deployment Script
-- Execute this in Supabase Dashboard SQL Editor AFTER deploying the main schema
-- URL: https://mxaazuhlqewmkweewyaz.supabase.co/sql

-- Create views in public schema that reference mini_agent_observability tables
-- This allows PostgREST to access them

CREATE OR REPLACE VIEW public.agent_traces AS
SELECT * FROM mini_agent_observability.traces;

CREATE OR REPLACE VIEW public.agent_tool_executions AS
SELECT * FROM mini_agent_observability.tool_executions;

CREATE OR REPLACE VIEW public.agent_performance_metrics AS
SELECT * FROM mini_agent_observability.performance_metrics;

CREATE OR REPLACE VIEW public.agent_decisions AS
SELECT * FROM mini_agent_observability.decisions;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_traces TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_tool_executions TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_performance_metrics TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_decisions TO authenticated, anon, service_role;

-- Create insert rules to redirect to actual tables
CREATE OR REPLACE RULE agent_traces_insert AS
ON INSERT TO public.agent_traces
DO INSTEAD
INSERT INTO mini_agent_observability.traces VALUES (NEW.*);

CREATE OR REPLACE RULE agent_tool_executions_insert AS
ON INSERT TO public.agent_tool_executions
DO INSTEAD
INSERT INTO mini_agent_observability.tool_executions VALUES (NEW.*);

CREATE OR REPLACE RULE agent_performance_metrics_insert AS
ON INSERT TO public.agent_performance_metrics
DO INSTEAD
INSERT INTO mini_agent_observability.performance_metrics VALUES (NEW.*);

CREATE OR REPLACE RULE agent_decisions_insert AS
ON INSERT TO public.agent_decisions
DO INSTEAD
INSERT INTO mini_agent_observability.decisions VALUES (NEW.*);
