-- Mini-Agent Observability Public Views with RETURNING Clauses
-- Execute this in Supabase Dashboard SQL Editor AFTER deploying the main schema
-- URL: https://mxaazuhlqewmkweewyaz.supabase.co/sql

-- Drop existing views and rules if they exist
DROP VIEW IF EXISTS public.agent_traces CASCADE;
DROP VIEW IF EXISTS public.agent_tool_executions CASCADE;
DROP VIEW IF EXISTS public.agent_performance_metrics CASCADE;
DROP VIEW IF EXISTS public.agent_decisions CASCADE;

DROP RULE IF EXISTS agent_traces_insert ON public.agent_traces;
DROP RULE IF EXISTS agent_tool_executions_insert ON public.agent_tool_executions;
DROP RULE IF EXISTS agent_performance_metrics_insert ON public.agent_performance_metrics;
DROP RULE IF EXISTS agent_decisions_insert ON public.agent_decisions;

-- Create views in public schema that reference mini_agent_observability tables
-- This allows PostgREST to access them

CREATE VIEW public.agent_traces AS
SELECT * FROM mini_agent_observability.traces;

CREATE VIEW public.agent_tool_executions AS
SELECT * FROM mini_agent_observability.tool_executions;

CREATE VIEW public.agent_performance_metrics AS
SELECT * FROM mini_agent_observability.performance_metrics;

CREATE VIEW public.agent_decisions AS
SELECT * FROM mini_agent_observability.decisions;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_traces TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_tool_executions TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_performance_metrics TO authenticated, anon, service_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.agent_decisions TO authenticated, anon, service_role;

-- Create insert rules with RETURNING clauses to redirect to actual tables
CREATE OR REPLACE RULE agent_traces_insert AS
ON INSERT TO public.agent_traces
DO INSTEAD
INSERT INTO mini_agent_observability.traces VALUES (NEW.*)
RETURNING *;

CREATE OR REPLACE RULE agent_tool_executions_insert AS
ON INSERT TO public.agent_tool_executions
DO INSTEAD
INSERT INTO mini_agent_observability.tool_executions VALUES (NEW.*)
RETURNING *;

CREATE OR REPLACE RULE agent_performance_metrics_insert AS
ON INSERT TO public.agent_performance_metrics
DO INSTEAD
INSERT INTO mini_agent_observability.performance_metrics VALUES (NEW.*)
RETURNING *;

CREATE OR REPLACE RULE agent_decisions_insert AS
ON INSERT TO public.agent_decisions
DO INSTEAD
INSERT INTO mini_agent_observability.decisions VALUES (NEW.*)
RETURNING *;
