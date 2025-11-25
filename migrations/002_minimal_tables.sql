-- MINIMAL: Just create the essential tables
CREATE SCHEMA IF NOT EXISTS mini_agent;

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

-- Create the exec_sql function in mini_agent schema
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

SELECT 'Essential tables created!' as status;