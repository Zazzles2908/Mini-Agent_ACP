-- SIMPLIFIED: Skip the problematic INSERT for now
-- Execute this first, then we'll add the state manually

-- Clean up any incorrectly placed tables in public schema
DO $$
DECLARE
    table_name TEXT;
BEGIN
    -- List of tables that should be in mini_agent schema, not public
    FOR table_name IN SELECT unnest(ARRAY[
        'mini_agent_projects',
        'mini_agent_sessions', 
        'mini_agent_knowledge',
        'mini_agent_tool_logs',
        'mini_agent_user_prefs',
        'mini_agent_system_state'
    ]) LOOP
        -- Drop table if it exists in public schema
        IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = table_name) THEN
            EXECUTE 'DROP TABLE IF EXISTS public.' || table_name || ' CASCADE';
            RAISE NOTICE 'Dropped table public.%', table_name;
        END IF;
    END LOOP;
END $$;

-- Create all tables in mini_agent schema
CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id TEXT UNIQUE NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    project_id TEXT REFERENCES mini_agent.mini_agent_projects(project_id) ON DELETE CASCADE,
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_knowledge (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    observations JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entity_type, entity_name)
);

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

CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_user_prefs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    preferences_schema JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mini_agent.mini_agent_system_state (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    state_key TEXT UNIQUE NOT NULL,
    state_value JSONB NOT NULL,
    state_type TEXT DEFAULT 'operational',
    health_score DECIMAL(3,2) DEFAULT 1.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_projects_project_id ON mini_agent.mini_agent_projects(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON mini_agent.mini_agent_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_entity_type ON mini_agent.mini_agent_knowledge(entity_type);
CREATE INDEX IF NOT EXISTS idx_tool_logs_tool_name ON mini_agent.mini_agent_tool_logs(tool_name);
CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id ON mini_agent.mini_agent_user_prefs(user_id);
CREATE INDEX IF NOT EXISTS idx_system_state_key ON mini_agent.mini_agent_system_state(state_key);

-- Create RPC functions
CREATE OR REPLACE FUNCTION mini_agent.exec_sql(query_text TEXT)
RETURNS TABLE(exec_result JSONB, affected_rows INTEGER, execution_time_ms INTEGER)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    start_time TIMESTAMPTZ;
    end_time TIMESTAMPTZ;
    exec_time INTEGER;
    result_data JSONB;
BEGIN
    start_time := clock_timestamp();
    EXECUTE 'SELECT to_jsonb((' || query_text || '))' INTO result_data;
    end_time := clock_timestamp();
    exec_time := EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
    
    RETURN QUERY SELECT result_data, 0, exec_time;
END;
$$;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mini_agent TO service_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mini_agent TO service_role;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA mini_agent TO service_role;

SELECT 'Tables and functions created successfully!' as status;