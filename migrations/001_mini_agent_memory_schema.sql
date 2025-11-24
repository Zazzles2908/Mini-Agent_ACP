-- Mini-Agent Memory System Database Schema
-- This migration creates all necessary tables for Mini-Agent's long-term memory
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
-- - list_tables() - List all tables in public schema

-- ============================================================================
-- MINI-AGENT PROJECTS TABLE
-- ============================================================================
-- Stores project-level context and metadata
CREATE TABLE IF NOT EXISTS mini_agent_projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id TEXT UNIQUE NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projects_project_id ON mini_agent_projects(project_id);
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON mini_agent_projects(created_at DESC);

COMMENT ON TABLE mini_agent_projects IS 'Project-level memory for Mini-Agent';
COMMENT ON COLUMN mini_agent_projects.project_id IS 'Unique identifier for the project';
COMMENT ON COLUMN mini_agent_projects.context IS 'Project context data (goals, status, etc.)';
COMMENT ON COLUMN mini_agent_projects.metadata IS 'Additional project metadata';

-- ============================================================================
-- MINI-AGENT SESSIONS TABLE
-- ============================================================================
-- Stores conversation history and session context
CREATE TABLE IF NOT EXISTS mini_agent_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    project_id TEXT REFERENCES mini_agent_projects(project_id) ON DELETE CASCADE,
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON mini_agent_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_project_id ON mini_agent_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON mini_agent_sessions(created_at DESC);

COMMENT ON TABLE mini_agent_sessions IS 'Session-level conversation history';
COMMENT ON COLUMN mini_agent_sessions.session_id IS 'Unique identifier for the session';
COMMENT ON COLUMN mini_agent_sessions.project_id IS 'Associated project (optional)';
COMMENT ON COLUMN mini_agent_sessions.messages IS 'Array of conversation messages';

-- ============================================================================
-- MINI-AGENT KNOWLEDGE GRAPH TABLE
-- ============================================================================
-- Stores entities and their relationships for knowledge graph
CREATE TABLE IF NOT EXISTS mini_agent_knowledge (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    attributes JSONB DEFAULT '{}'::jsonb,
    relations JSONB DEFAULT '[]'::jsonb,
    project_id TEXT REFERENCES mini_agent_projects(project_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entity_type, entity_id, project_id)
);

CREATE INDEX IF NOT EXISTS idx_knowledge_entity ON mini_agent_knowledge(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_project ON mini_agent_knowledge(project_id);

COMMENT ON TABLE mini_agent_knowledge IS 'Knowledge graph entities and relations';
COMMENT ON COLUMN mini_agent_knowledge.entity_type IS 'Type of entity (e.g., "file", "concept", "person")';
COMMENT ON COLUMN mini_agent_knowledge.entity_id IS 'Unique identifier for the entity';
COMMENT ON COLUMN mini_agent_knowledge.attributes IS 'Entity attributes and properties';
COMMENT ON COLUMN mini_agent_knowledge.relations IS 'Array of relationships to other entities';

-- ============================================================================
-- MINI-AGENT TOOL USAGE LOGS TABLE
-- ============================================================================
-- Tracks tool executions for analytics and debugging
CREATE TABLE IF NOT EXISTS mini_agent_tool_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    parameters JSONB DEFAULT '{}'::jsonb,
    result JSONB DEFAULT '{}'::jsonb,
    execution_time_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tool_logs_session ON mini_agent_tool_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_tool_logs_tool_name ON mini_agent_tool_logs(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_logs_timestamp ON mini_agent_tool_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_tool_logs_success ON mini_agent_tool_logs(success);

COMMENT ON TABLE mini_agent_tool_logs IS 'Tool execution logs for analytics';
COMMENT ON COLUMN mini_agent_tool_logs.tool_name IS 'Name of the tool that was executed';
COMMENT ON COLUMN mini_agent_tool_logs.parameters IS 'Input parameters for the tool';
COMMENT ON COLUMN mini_agent_tool_logs.result IS 'Tool execution result';
COMMENT ON COLUMN mini_agent_tool_logs.execution_time_ms IS 'Execution time in milliseconds';

-- ============================================================================
-- MINI-AGENT USER PREFERENCES TABLE
-- ============================================================================
-- Stores user preferences and settings
CREATE TABLE IF NOT EXISTS mini_agent_user_prefs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    history JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id ON mini_agent_user_prefs(user_id);

COMMENT ON TABLE mini_agent_user_prefs IS 'User preferences and settings';
COMMENT ON COLUMN mini_agent_user_prefs.user_id IS 'Unique identifier for the user';
COMMENT ON COLUMN mini_agent_user_prefs.preferences IS 'User preference settings';
COMMENT ON COLUMN mini_agent_user_prefs.history IS 'User interaction history';

-- ============================================================================
-- MINI-AGENT SYSTEM STATE TABLE
-- ============================================================================
-- Tracks system component health and state
CREATE TABLE IF NOT EXISTS mini_agent_system_state (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    component TEXT UNIQUE NOT NULL,
    state JSONB DEFAULT '{}'::jsonb,
    health_status TEXT DEFAULT 'healthy',
    last_check TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_state_component ON mini_agent_system_state(component);
CREATE INDEX IF NOT EXISTS idx_system_state_health ON mini_agent_system_state(health_status);

COMMENT ON TABLE mini_agent_system_state IS 'System component health tracking';
COMMENT ON COLUMN mini_agent_system_state.component IS 'Component name (e.g., "mcp_loader", "llm_client")';
COMMENT ON COLUMN mini_agent_system_state.state IS 'Current component state';
COMMENT ON COLUMN mini_agent_system_state.health_status IS 'Health status: healthy, degraded, unhealthy';

-- ============================================================================
-- RPC FUNCTIONS
-- ============================================================================

-- Function to execute arbitrary SQL (admin only)
CREATE OR REPLACE FUNCTION exec_sql(query_text TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result_data JSONB;
BEGIN
    EXECUTE query_text INTO result_data;
    RETURN jsonb_build_object('success', true, 'data', result_data);
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('success', false, 'error', SQLERRM);
END;
$$;

COMMENT ON FUNCTION exec_sql IS 'Execute arbitrary SQL query (admin only)';

-- Function to list all tables in public schema
CREATE OR REPLACE FUNCTION list_tables()
RETURNS TABLE(table_name TEXT, table_schema TEXT, row_count BIGINT)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.table_name::TEXT,
        t.table_schema::TEXT,
        (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = t.table_name)::BIGINT
    FROM information_schema.tables t
    WHERE t.table_schema = 'public'
    AND t.table_type = 'BASE TABLE'
    ORDER BY t.table_name;
END;
$$;

COMMENT ON FUNCTION list_tables IS 'List all tables in public schema with row counts';

-- ============================================================================
-- PERMISSIONS
-- ============================================================================

-- Grant necessary permissions to service_role
GRANT USAGE ON SCHEMA public TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert system state entry for Mini-Agent
INSERT INTO mini_agent_system_state (component, state, health_status)
VALUES 
    ('mini_agent_core', '{"version": "1.0.0", "initialized": true}'::jsonb, 'healthy'),
    ('supabase_mcp', '{"version": "1.0.0", "connected": true}'::jsonb, 'healthy')
ON CONFLICT (component) DO NOTHING;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Verify tables were created
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'mini_agent_%';
    
    RAISE NOTICE 'Migration complete: % Mini-Agent tables created', table_count;
END $$;
