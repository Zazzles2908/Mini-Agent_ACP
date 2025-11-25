-- Mini-Agent Memory System Database Schema - FIXED VERSION
-- This migration creates all necessary tables for Mini-Agent's long-term memory
-- FIXED: Properly namespaced in mini_agent schema to avoid conflicts
--
-- Tables:
-- 1. mini_agent_projects - Project context and metadata
-- 2. mini_agent_sessions - Conversation history by session
-- 3. mini_agent_knowledge - Knowledge graph entities and relations
-- 4. mini_agent_tool_logs - Tool usage analytics
-- 5. mini_agent_user_prefs - User preferences and settings
-- 6. mini_agent_system_state - System health and state tracking
--
-- RPC Functions:
-- - exec_sql() - Execute arbitrary SQL (admin only)
-- - list_tables() - List all tables in mini_agent schema
--
-- ============================================================================
-- CREATE MINI_AGENT SCHEMA (if not exists)
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS mini_agent;

-- Grant permissions for service role access
GRANT USAGE ON SCHEMA mini_agent TO service_role;
GRANT ALL PRIVILEGES ON SCHEMA mini_agent TO service_role;

-- ============================================================================
-- MINI-AGENT PROJECTS TABLE
-- ============================================================================
-- Stores project-level context and metadata
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id TEXT UNIQUE NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projects_project_id ON mini_agent.mini_agent_projects(project_id);
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON mini_agent.mini_agent_projects(created_at DESC);

COMMENT ON TABLE mini_agent.mini_agent_projects IS 'Project-level memory for Mini-Agent';
COMMENT ON COLUMN mini_agent.mini_agent_projects.project_id IS 'Unique identifier for the project';
COMMENT ON COLUMN mini_agent.mini_agent_projects.context IS 'Project context data (goals, status, etc.)';
COMMENT ON COLUMN mini_agent.mini_agent_projects.metadata IS 'Additional project metadata';

-- ============================================================================
-- MINI-AGENT SESSIONS TABLE
-- ============================================================================
-- Stores conversation history and session context
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    project_id TEXT REFERENCES mini_agent.mini_agent_projects(project_id) ON DELETE CASCADE,
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON mini_agent.mini_agent_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project_id ON mini_agent.mini_agent_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON mini_agent.mini_agent_sessions(created_at DESC);

COMMENT ON TABLE mini_agent.mini_agent_sessions IS 'Session-level conversation history for Mini-Agent';
COMMENT ON COLUMN mini_agent.mini_agent_sessions.session_id IS 'Unique identifier for the session';
COMMENT ON COLUMN mini_agent.mini_agent_sessions.project_id IS 'Associated project identifier';
COMMENT ON COLUMN mini_agent.mini_agent_sessions.messages IS 'Conversation history as JSON array';

-- ============================================================================
-- MINI-AGENT KNOWLEDGE TABLE
-- ============================================================================
-- Stores knowledge graph entities and relationships
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_knowledge (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    observations JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Unique constraint on entity
    UNIQUE(entity_type, entity_name)
);

CREATE INDEX IF NOT EXISTS idx_knowledge_entity_type ON mini_agent.mini_agent_knowledge(entity_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_entity_name ON mini_agent.mini_agent_knowledge(entity_name);
CREATE INDEX IF NOT EXISTS idx_knowledge_created_at ON mini_agent.mini_agent_knowledge(created_at DESC);

COMMENT ON TABLE mini_agent.mini_agent_knowledge IS 'Knowledge graph entities for Mini-Agent memory';
COMMENT ON COLUMN mini_agent.mini_agent_knowledge.entity_type IS 'Type of entity (person, project, concept, etc.)';
COMMENT ON COLUMN mini_agent.mini_agent_knowledge.entity_name IS 'Name or identifier of the entity';
COMMENT ON COLUMN mini_agent.mini_agent_knowledge.observations IS 'Array of observations about this entity';

-- ============================================================================
-- MINI-AGENT TOOL LOGS TABLE
-- ============================================================================
-- Stores tool usage analytics and performance data
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_tool_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT,
    tool_name TEXT NOT NULL,
    tool_category TEXT,
    success BOOLEAN DEFAULT TRUE,
    execution_time_ms INTEGER,
    error_message TEXT,
    parameters JSONB,
    result_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tool_logs_session_id ON mini_agent.mini_agent_tool_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_tool_logs_tool_name ON mini_agent.mini_agent_tool_logs(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_logs_category ON mini_agent.mini_agent_tool_logs(tool_category);
CREATE INDEX IF NOT EXISTS idx_tool_logs_created_at ON mini_agent.mini_agent_tool_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tool_logs_success ON mini_agent.mini_agent_tool_logs(success);

COMMENT ON TABLE mini_agent.mini_agent_tool_logs IS 'Tool usage analytics for Mini-Agent performance monitoring';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.session_id IS 'Associated session identifier';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.tool_name IS 'Name of the tool that was used';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.tool_category IS 'Category of the tool (file, git, mcp, etc.)';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.success IS 'Whether the tool execution was successful';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.execution_time_ms IS 'Execution time in milliseconds';
COMMENT ON COLUMN mini_agent.mini_agent_tool_logs.error_message IS 'Error message if tool execution failed';

-- ============================================================================
-- MINI-AGENT USER PREFERENCES TABLE
-- ============================================================================
-- Stores user preferences and settings
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_user_prefs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    preferences_schema JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id ON mini_agent.mini_agent_user_prefs(user_id);
CREATE INDEX IF NOT EXISTS idx_user_prefs_updated_at ON mini_agent.mini_agent_user_prefs(updated_at DESC);

COMMENT ON TABLE mini_agent.mini_agent_user_prefs IS 'User preferences and configuration for Mini-Agent';
COMMENT ON COLUMN mini_agent.mini_agent_user_prefs.user_id IS 'Unique user identifier';
COMMENT ON COLUMN mini_agent.mini_agent_user_prefs.preferences IS 'User preference data as JSON';
COMMENT ON COLUMN mini_agent.mini_agent_user_prefs.preferences_schema IS 'Schema definition for validation';

-- ============================================================================
-- MINI-AGENT SYSTEM STATE TABLE
-- ============================================================================
-- Stores system health and state tracking
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_system_state (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    state_key TEXT UNIQUE NOT NULL,
    state_value JSONB NOT NULL,
    state_type TEXT DEFAULT 'operational',
    health_score DECIMAL(3,2) DEFAULT 1.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_state_key ON mini_agent.mini_agent_system_state(state_key);
CREATE INDEX IF NOT EXISTS idx_system_state_type ON mini_agent.mini_agent_system_state(state_type);
CREATE INDEX IF NOT EXISTS idx_system_state_updated_at ON mini_agent.mini_agent_system_state(updated_at DESC);

COMMENT ON TABLE mini_agent.mini_agent_system_state IS 'System health and state monitoring for Mini-Agent';
COMMENT ON COLUMN mini_agent.mini_agent_system_state.state_key IS 'Key identifying the state item';
COMMENT ON COLUMN mini_agent.mini_agent_system_state.state_value IS 'State data as JSON';
COMMENT ON COLUMN mini_agent.mini_agent_system_state.state_type IS 'Type of state (operational, warning, error)';
COMMENT ON COLUMN mini_agent.mini_agent_system_state.health_score IS 'Health score from 0.00 to 1.00';

-- ============================================================================
-- INITIALIZE SYSTEM STATE ENTRIES
-- ============================================================================
-- Create initial system state entries
INSERT INTO mini_agent.mini_agent_system_state (state_key, state_value, state_type, health_score) VALUES
('system_initialized', '{"timestamp": NOW(), "status": "initialization_complete"}', 'operational', 1.00),
('mcp_servers_loaded', '{"count": 0, "last_check": NOW()}', 'operational', 1.00),
('database_ready', '{"tables_created": 6, "migration_version": "001"}', 'operational', 1.00)
ON CONFLICT (state_key) DO NOTHING;

-- ============================================================================
-- RPC FUNCTIONS
-- ============================================================================
-- Function to execute arbitrary SQL (admin only)
CREATE OR REPLACE FUNCTION mini_agent.exec_sql(query_text TEXT)
RETURNS TABLE(exec_result JSONB, affected_rows INTEGER, execution_time_ms INTEGER)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    start_time TIMESTAMPTZ;
    end_time TIMESTAMPTZ;
    exec_time INTEGER;
    affected_count INTEGER;
    result_data JSONB;
BEGIN
    start_time := clock_timestamp();
    
    -- Execute the query and capture results
    EXECUTE 'SELECT to_jsonb((' || query_text || '))' INTO result_data;
    
    -- Get affected rows for INSERT/UPDATE/DELETE
    GET DIAGNOSTICS affected_count = ROW_COUNT;
    
    end_time := clock_timestamp();
    exec_time := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
    
    RETURN QUERY SELECT result_data, affected_count, exec_time;
END;
$$;

-- Function to list all tables in mini_agent schema
CREATE OR REPLACE FUNCTION mini_agent.list_tables()
RETURNS TABLE(table_name TEXT, table_type TEXT, row_count BIGINT)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.relname::TEXT as table_name,
        c.relkind::TEXT as table_type,
        CASE 
            WHEN c.relkind = 'r' THEN c.reltuples
            ELSE 0
        END::BIGINT as row_count
    FROM pg_class c
    JOIN pg_namespace n ON c.relnamespace = n.oid
    WHERE n.nspname = 'mini_agent' 
    AND c.relkind IN ('r', 'v', 'm')  -- regular tables, views, materialized views
    ORDER BY c.relname;
END;
$$;

-- ============================================================================
-- SECURITY AND PERMISSIONS
-- ============================================================================
-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mini_agent TO service_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mini_agent TO service_role;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA mini_agent TO service_role;

-- Enable RLS (Row Level Security) if needed
ALTER TABLE mini_agent.mini_agent_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent.mini_agent_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent.mini_agent_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent.mini_agent_tool_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent.mini_agent_user_prefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE mini_agent.mini_agent_system_state ENABLE ROW LEVEL SECURITY;

-- Create policies to allow service_role full access (adjust as needed)
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_projects FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_sessions FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_knowledge FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_tool_logs FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_user_prefs FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mini_agent.mini_agent_system_state FOR ALL USING (true);

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
-- Log successful migration
INSERT INTO mini_agent.mini_agent_system_state (state_key, state_value, state_type, health_score) VALUES
('migration_001_complete', '{"completed_at": NOW(), "tables_created": 6, "schema": "mini_agent"}', 'operational', 1.00)
ON CONFLICT (state_key) DO UPDATE SET
    state_value = EXCLUDED.state_value,
    updated_at = NOW();
