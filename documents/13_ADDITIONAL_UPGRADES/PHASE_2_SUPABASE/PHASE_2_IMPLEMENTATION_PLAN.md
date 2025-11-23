# Phase 2: Supabase Database Integration - Implementation Plan

## 🎯 Executive Summary

**Goal**: Implement comprehensive Supabase MCP server with admin-level database control to serve as Mini-Agent's long-term memory and project storage system.

**Vision**: Supabase becomes Mini-Agent's **persistent brain** - storing project context, conversation history, learned knowledge, user preferences, and system state across all sessions.

**Architecture Pattern**: Custom local MCP server (following Mini-Agent's proven pattern) with full transparency and admin-level access.

---

## 📋 Phase 2 Overview

**Status**: Ready for Implementation (after Phase 1)  
**Priority**: High  
**Estimated Time**: 3-4 hours  
**Dependencies**: 
- ✅ Supabase project credentials (provided)
- ✅ Service role key for admin access (provided)
- ✅ Admin access token (provided)
- 🔄 Phase 1 completion (web search architecture stable)

---

## 🗄️ Supabase as Mini-Agent's Long-Term Memory

### **Memory Architecture Vision**

```
┌────────────────────────────────────────────────────────────┐
│                    Mini-Agent                              │
│                 (Session Context)                          │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│              Supabase MCP Server                           │
│           (Persistent Memory Layer)                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Projects    │  │  Sessions    │  │  Knowledge   │    │
│  │  Table       │  │  Table       │  │  Graph       │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ - id         │  │ - id         │  │ - entities   │    │
│  │ - name       │  │ - project_id │  │ - relations  │    │
│  │ - context    │  │ - messages   │  │ - attributes │    │
│  │ - metadata   │  │ - timestamp  │  │ - timestamps │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  User Prefs  │  │  Tool Usage  │  │  System      │    │
│  │  Table       │  │  Logs        │  │  State       │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ - user_id    │  │ - tool_name  │  │ - version    │    │
│  │ - settings   │  │ - params     │  │ - config     │    │
│  │ - history    │  │ - results    │  │ - health     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│         Supabase PostgreSQL Database                       │
│  URL: https://mxaazuhlqewmkweewyaz.supabase.co           │
└────────────────────────────────────────────────────────────┘
```

### **Why Supabase for Long-Term Memory?**

| Feature | Benefit for Mini-Agent |
|---------|------------------------|
| **PostgreSQL** | Robust, ACID-compliant storage |
| **Real-time Subscriptions** | Live updates across sessions |
| **Row Level Security** | Fine-grained access control |
| **RESTful API** | Easy integration with Python |
| **Admin SDK** | Full programmatic control |
| **Built-in Auth** | User management if needed |
| **Edge Functions** | Custom server-side logic |
| **Storage API** | File and artifact storage |

---

## 🔐 Credentials & Configuration

### **Provided Credentials**

```env
# Supabase Connection Details
SUPABASE_URL=https://mxaazuhlqewmkweewyaz.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_29Ok3p5WJ2qa_QHcZMY3wQ_y8naYtLV
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw
SUPABASE_ADMIN_TOKEN=sbp_af0f003e58dfcea9ad42d545e9f8d79102855f9f
```

### **Key Types Explained**

| Key Type | Purpose | Access Level | Use In MCP |
|----------|---------|--------------|------------|
| **Publishable Key** | Frontend/public use | Row-level security enforced | ❌ No |
| **Service Role Key** | Backend admin operations | Bypasses RLS, full access | ✅ Yes |
| **Admin Token** | Management API access | Project-level operations | ✅ Yes |

**For MCP Server**: Use **Service Role Key** for database operations and **Admin Token** for project management.

---

## 🛠️ Implementation Steps

### **Step 1: Create Supabase MCP Server** ⏱️ 60 minutes

**Task**: Build custom MCP server using FastMCP framework.

**File to Create**: `scripts/mcp_servers/supabase_admin_mcp_server.py`

**Full Implementation**:

```python
#!/usr/bin/env python3
"""
Supabase Admin MCP Server
Provides comprehensive database operations with full admin access for Mini-Agent's long-term memory.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

# MCP and Pydantic imports
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Supabase client
from supabase import create_client, Client

# Initialize MCP server
mcp = FastMCP("supabase_admin")

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# =============================================================================
# Input Models
# =============================================================================

class QueryRequest(BaseModel):
    """SQL query execution request"""
    sql: str = Field(..., description="SQL query to execute")
    params: Optional[Dict[str, Any]] = Field(None, description="Query parameters for safe interpolation")

class TableOperation(str, Enum):
    """Table operation types"""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    UPSERT = "upsert"

class TableRequest(BaseModel):
    """Table operation request"""
    table_name: str = Field(..., description="Name of the table")
    operation: TableOperation = Field(..., description="Operation to perform")
    data: Optional[Dict[str, Any]] = Field(None, description="Data for insert/update/upsert")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters for select/update/delete")
    columns: Optional[List[str]] = Field(None, description="Columns to select")
    order_by: Optional[str] = Field(None, description="Column to order by")
    limit: Optional[int] = Field(None, description="Limit number of results")

class SchemaRequest(BaseModel):
    """Schema management request"""
    action: str = Field(..., description="Action: 'create_table', 'alter_table', 'drop_table', 'list_tables'")
    table_name: Optional[str] = Field(None, description="Table name for create/alter/drop")
    schema_definition: Optional[Dict[str, Any]] = Field(None, description="Schema definition for create/alter")

class ProjectMemoryRequest(BaseModel):
    """Project memory management"""
    project_id: str = Field(..., description="Unique project identifier")
    operation: str = Field(..., description="Operation: 'create', 'read', 'update', 'delete', 'list'")
    context: Optional[Dict[str, Any]] = Field(None, description="Project context data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class SessionMemoryRequest(BaseModel):
    """Session memory management"""
    session_id: str = Field(..., description="Unique session identifier")
    project_id: Optional[str] = Field(None, description="Associated project ID")
    operation: str = Field(..., description="Operation: 'create', 'append', 'read', 'list'")
    messages: Optional[List[Dict[str, Any]]] = Field(None, description="Conversation messages")

# =============================================================================
# Database Operations Tools
# =============================================================================

@mcp.tool(
    annotations={
        "title": "Execute SQL Query",
        "description": "Execute raw SQL query with full admin access. Use for complex queries beyond CRUD operations.",
        "readOnlyHint": False
    }
)
def execute_sql(request: QueryRequest) -> str:
    """
    Execute raw SQL query with full transparency.
    
    Returns detailed execution results including affected rows, returned data, and execution time.
    """
    try:
        start_time = datetime.now()
        
        # Execute query using Supabase RPC
        result = supabase.rpc('exec_sql', {'query': request.sql}).execute()
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        return json.dumps({
            "success": True,
            "data": result.data,
            "execution_time_seconds": execution_time,
            "query": request.sql,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "query": request.sql
        }, indent=2)

@mcp.tool(
    annotations={
        "title": "Table Operations",
        "description": "Perform CRUD operations on database tables (select, insert, update, delete, upsert)",
        "readOnlyHint": False
    }
)
def table_operation(request: TableRequest) -> str:
    """
    Perform table operations with automatic query building.
    
    Supports: SELECT, INSERT, UPDATE, DELETE, UPSERT operations.
    """
    try:
        table = supabase.table(request.table_name)
        
        if request.operation == TableOperation.SELECT:
            query = table.select(*request.columns if request.columns else "*")
            
            # Apply filters
            if request.filters:
                for key, value in request.filters.items():
                    query = query.eq(key, value)
            
            # Apply ordering
            if request.order_by:
                query = query.order(request.order_by)
            
            # Apply limit
            if request.limit:
                query = query.limit(request.limit)
            
            result = query.execute()
            
            return json.dumps({
                "success": True,
                "operation": "select",
                "table": request.table_name,
                "count": len(result.data),
                "data": result.data
            }, indent=2)
        
        elif request.operation == TableOperation.INSERT:
            result = table.insert(request.data).execute()
            
            return json.dumps({
                "success": True,
                "operation": "insert",
                "table": request.table_name,
                "inserted": result.data
            }, indent=2)
        
        elif request.operation == TableOperation.UPDATE:
            query = table.update(request.data)
            
            # Apply filters
            if request.filters:
                for key, value in request.filters.items():
                    query = query.eq(key, value)
            
            result = query.execute()
            
            return json.dumps({
                "success": True,
                "operation": "update",
                "table": request.table_name,
                "updated_count": len(result.data),
                "updated": result.data
            }, indent=2)
        
        elif request.operation == TableOperation.DELETE:
            query = table.delete()
            
            # Apply filters
            if request.filters:
                for key, value in request.filters.items():
                    query = query.eq(key, value)
            
            result = query.execute()
            
            return json.dumps({
                "success": True,
                "operation": "delete",
                "table": request.table_name,
                "deleted_count": len(result.data)
            }, indent=2)
        
        elif request.operation == TableOperation.UPSERT:
            result = table.upsert(request.data).execute()
            
            return json.dumps({
                "success": True,
                "operation": "upsert",
                "table": request.table_name,
                "upserted": result.data
            }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "operation": request.operation.value,
            "table": request.table_name
        }, indent=2)

@mcp.tool(
    annotations={
        "title": "Schema Management",
        "description": "Manage database schema: create/alter/drop tables, list schema",
        "readOnlyHint": False
    }
)
def schema_management(request: SchemaRequest) -> str:
    """
    Manage database schema with DDL operations.
    
    Actions: create_table, alter_table, drop_table, list_tables
    """
    try:
        if request.action == "list_tables":
            # Query information_schema to list tables
            result = supabase.rpc('list_tables').execute()
            
            return json.dumps({
                "success": True,
                "action": "list_tables",
                "tables": result.data
            }, indent=2)
        
        elif request.action == "create_table":
            # Generate CREATE TABLE SQL
            columns_sql = []
            for col_name, col_def in request.schema_definition.items():
                columns_sql.append(f"{col_name} {col_def}")
            
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {request.table_name} (
                {', '.join(columns_sql)}
            );
            """
            
            result = supabase.rpc('exec_sql', {'query': create_sql}).execute()
            
            return json.dumps({
                "success": True,
                "action": "create_table",
                "table": request.table_name,
                "sql": create_sql
            }, indent=2)
        
        elif request.action == "drop_table":
            drop_sql = f"DROP TABLE IF EXISTS {request.table_name} CASCADE;"
            result = supabase.rpc('exec_sql', {'query': drop_sql}).execute()
            
            return json.dumps({
                "success": True,
                "action": "drop_table",
                "table": request.table_name
            }, indent=2)
        
        elif request.action == "alter_table":
            # TODO: Implement ALTER TABLE logic
            return json.dumps({
                "success": False,
                "error": "ALTER TABLE not yet implemented"
            }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "action": request.action
        }, indent=2)

# =============================================================================
# Mini-Agent Memory Tools
# =============================================================================

@mcp.tool(
    annotations={
        "title": "Project Memory",
        "description": "Manage project-level memory and context for Mini-Agent",
        "readOnlyHint": False
    }
)
def project_memory(request: ProjectMemoryRequest) -> str:
    """
    Manage long-term project memory.
    
    Operations: create, read, update, delete, list
    """
    try:
        table = supabase.table("mini_agent_projects")
        
        if request.operation == "create":
            data = {
                "project_id": request.project_id,
                "context": request.context or {},
                "metadata": request.metadata or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            result = table.insert(data).execute()
            
            return json.dumps({
                "success": True,
                "operation": "create",
                "project": result.data[0]
            }, indent=2)
        
        elif request.operation == "read":
            result = table.select("*").eq("project_id", request.project_id).execute()
            
            return json.dumps({
                "success": True,
                "operation": "read",
                "project": result.data[0] if result.data else None
            }, indent=2)
        
        elif request.operation == "update":
            data = {
                "context": request.context,
                "metadata": request.metadata,
                "updated_at": datetime.now().isoformat()
            }
            result = table.update(data).eq("project_id", request.project_id).execute()
            
            return json.dumps({
                "success": True,
                "operation": "update",
                "project": result.data[0]
            }, indent=2)
        
        elif request.operation == "delete":
            result = table.delete().eq("project_id", request.project_id).execute()
            
            return json.dumps({
                "success": True,
                "operation": "delete",
                "project_id": request.project_id
            }, indent=2)
        
        elif request.operation == "list":
            result = table.select("*").execute()
            
            return json.dumps({
                "success": True,
                "operation": "list",
                "projects": result.data,
                "count": len(result.data)
            }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "operation": request.operation
        }, indent=2)

@mcp.tool(
    annotations={
        "title": "Session Memory",
        "description": "Manage session-level conversation history and context",
        "readOnlyHint": False
    }
)
def session_memory(request: SessionMemoryRequest) -> str:
    """
    Manage session-level conversation memory.
    
    Operations: create, append, read, list
    """
    try:
        table = supabase.table("mini_agent_sessions")
        
        if request.operation == "create":
            data = {
                "session_id": request.session_id,
                "project_id": request.project_id,
                "messages": request.messages or [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            result = table.insert(data).execute()
            
            return json.dumps({
                "success": True,
                "operation": "create",
                "session": result.data[0]
            }, indent=2)
        
        elif request.operation == "append":
            # Get existing session
            existing = table.select("messages").eq("session_id", request.session_id).execute()
            
            if existing.data:
                current_messages = existing.data[0]["messages"]
                updated_messages = current_messages + request.messages
                
                result = table.update({
                    "messages": updated_messages,
                    "updated_at": datetime.now().isoformat()
                }).eq("session_id", request.session_id).execute()
                
                return json.dumps({
                    "success": True,
                    "operation": "append",
                    "session_id": request.session_id,
                    "message_count": len(updated_messages)
                }, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "error": f"Session {request.session_id} not found"
                }, indent=2)
        
        elif request.operation == "read":
            result = table.select("*").eq("session_id", request.session_id).execute()
            
            return json.dumps({
                "success": True,
                "operation": "read",
                "session": result.data[0] if result.data else None
            }, indent=2)
        
        elif request.operation == "list":
            query = table.select("*")
            if request.project_id:
                query = query.eq("project_id", request.project_id)
            
            result = query.execute()
            
            return json.dumps({
                "success": True,
                "operation": "list",
                "sessions": result.data,
                "count": len(result.data)
            }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "operation": request.operation
        }, indent=2)

# =============================================================================
# Run Server
# =============================================================================

if __name__ == "__main__":
    mcp.run()
```

**Dependencies to Install**:
```bash
uv pip install supabase fastmcp
```

---

### **Step 2: Create Database Schema** ⏱️ 30 minutes

**Task**: Initialize Mini-Agent memory tables in Supabase.

**SQL Migration** (`migrations/001_mini_agent_memory.sql`):

```sql
-- Mini-Agent Projects Table
CREATE TABLE IF NOT EXISTS mini_agent_projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id TEXT UNIQUE NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_project_id ON mini_agent_projects(project_id);
CREATE INDEX idx_projects_created_at ON mini_agent_projects(created_at DESC);

-- Mini-Agent Sessions Table
CREATE TABLE IF NOT EXISTS mini_agent_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    project_id TEXT REFERENCES mini_agent_projects(project_id) ON DELETE CASCADE,
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sessions_session_id ON mini_agent_sessions(session_id);
CREATE INDEX idx_sessions_project_id ON mini_agent_sessions(project_id);
CREATE INDEX idx_sessions_created_at ON mini_agent_sessions(created_at DESC);

-- Mini-Agent Knowledge Graph Table
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

CREATE INDEX idx_knowledge_entity ON mini_agent_knowledge(entity_type, entity_id);
CREATE INDEX idx_knowledge_project ON mini_agent_knowledge(project_id);

-- Mini-Agent Tool Usage Logs
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

CREATE INDEX idx_tool_logs_session ON mini_agent_tool_logs(session_id);
CREATE INDEX idx_tool_logs_tool_name ON mini_agent_tool_logs(tool_name);
CREATE INDEX idx_tool_logs_timestamp ON mini_agent_tool_logs(timestamp DESC);

-- Mini-Agent User Preferences
CREATE TABLE IF NOT EXISTS mini_agent_user_prefs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    history JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_user_prefs_user_id ON mini_agent_user_prefs(user_id);

-- Mini-Agent System State
CREATE TABLE IF NOT EXISTS mini_agent_system_state (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    component TEXT UNIQUE NOT NULL,
    state JSONB DEFAULT '{}'::jsonb,
    health_status TEXT DEFAULT 'healthy',
    last_check TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_system_state_component ON mini_agent_system_state(component);

-- Create RPC function for executing arbitrary SQL
CREATE OR REPLACE FUNCTION exec_sql(query TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    result JSONB;
BEGIN
    EXECUTE query INTO result;
    RETURN result;
EXCEPTION WHEN OTHERS THEN
    RETURN jsonb_build_object('error', SQLERRM);
END;
$$;

-- Create RPC function for listing tables
CREATE OR REPLACE FUNCTION list_tables()
RETURNS TABLE(table_name TEXT, table_schema TEXT)
LANGUAGE SQL
SECURITY DEFINER
AS $$
    SELECT table_name::TEXT, table_schema::TEXT
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
$$;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;
```

**Apply Migration**:
```bash
# Option 1: Via Supabase Dashboard SQL Editor
# Copy and paste the SQL above

# Option 2: Via supabase CLI
supabase db push
```

---

### **Step 3: Configure MCP Server** ⏱️ 15 minutes

**Task**: Add Supabase MCP to Mini-Agent configuration.

**File to Modify**: `mini_agent/config/.mcp.json`

**Add Configuration**:

```json
{
  "mcpServers": {
    "supabase-admin": {
      "description": "Supabase Admin MCP - Full database control for Mini-Agent's long-term memory and project storage",
      "command": "python",
      "args": ["scripts/mcp_servers/supabase_admin_mcp_server.py"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_SERVICE_KEY": "${SUPABASE_SERVICE_KEY}",
        "SUPABASE_ADMIN_TOKEN": "${SUPABASE_ADMIN_TOKEN}"
      },
      "disabled": false
    },
    
    "... existing MCP servers ..."
  }
}
```

**Update `.env` File**:

```bash
# Add to .env file
SUPABASE_URL=https://mxaazuhlqewmkweewyaz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14YWF6dWhscWV3bWt3ZWV3eWF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODE5MDUyNSwiZXhwIjoyMDczNzY2NTI1fQ.HpPi30g4NjpDRGYtc406X_TjIj70OoOYCzQYUltxfgw
SUPABASE_ADMIN_TOKEN=sbp_af0f003e58dfcea9ad42d545e9f8d79102855f9f
```

---

### **Step 4: Create Memory Integration Layer** ⏱️ 45 minutes

**Task**: Build high-level memory management interface for Mini-Agent.

**File to Create**: `mini_agent/memory/supabase_memory.py`

```python
"""
Supabase Memory Manager
High-level interface for Mini-Agent's persistent memory system.
"""

import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4

class SupabaseMemory:
    """
    Manage Mini-Agent's long-term memory using Supabase MCP.
    
    Provides high-level operations for:
    - Project context management
    - Session history tracking
    - Knowledge graph operations
    - Tool usage analytics
    """
    
    def __init__(self, mcp_tools):
        """Initialize with MCP tools loaded from MCP loader."""
        self.supabase_tool = next(
            (t for t in mcp_tools if "supabase" in t.name.lower()),
            None
        )
        
        if not self.supabase_tool:
            raise ValueError("Supabase MCP tool not found in loaded tools")
    
    # =========================================================================
    # Project Memory Operations
    # =========================================================================
    
    async def create_project(self, project_id: str, context: Dict[str, Any] = None,
                            metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create new project memory entry."""
        result = await self.supabase_tool.execute(
            tool_name="project_memory",
            project_id=project_id,
            operation="create",
            context=context or {},
            metadata=metadata or {}
        )
        return json.loads(result.content)
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve project context."""
        result = await self.supabase_tool.execute(
            tool_name="project_memory",
            project_id=project_id,
            operation="read"
        )
        data = json.loads(result.content)
        return data.get("project")
    
    async def update_project(self, project_id: str, context: Dict[str, Any],
                            metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update project context."""
        result = await self.supabase_tool.execute(
            tool_name="project_memory",
            project_id=project_id,
            operation="update",
            context=context,
            metadata=metadata or {}
        )
        return json.loads(result.content)
    
    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        result = await self.supabase_tool.execute(
            tool_name="project_memory",
            project_id="",  # Not used for list
            operation="list"
        )
        data = json.loads(result.content)
        return data.get("projects", [])
    
    # =========================================================================
    # Session Memory Operations
    # =========================================================================
    
    async def create_session(self, session_id: str, project_id: Optional[str] = None,
                            initial_messages: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create new session memory."""
        result = await self.supabase_tool.execute(
            tool_name="session_memory",
            session_id=session_id,
            project_id=project_id,
            operation="create",
            messages=initial_messages or []
        )
        return json.loads(result.content)
    
    async def append_to_session(self, session_id: str,
                                messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Append messages to session history."""
        result = await self.supabase_tool.execute(
            tool_name="session_memory",
            session_id=session_id,
            operation="append",
            messages=messages
        )
        return json.loads(result.content)
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session history."""
        result = await self.supabase_tool.execute(
            tool_name="session_memory",
            session_id=session_id,
            operation="read"
        )
        data = json.loads(result.content)
        return data.get("session")
    
    async def list_sessions(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List sessions, optionally filtered by project."""
        result = await self.supabase_tool.execute(
            tool_name="session_memory",
            session_id="",  # Not used for list
            project_id=project_id,
            operation="list"
        )
        data = json.loads(result.content)
        return data.get("sessions", [])
    
    # =========================================================================
    # Database Operations (Direct Access)
    # =========================================================================
    
    async def execute_sql(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute raw SQL query."""
        result = await self.supabase_tool.execute(
            tool_name="execute_sql",
            sql=sql,
            params=params or {}
        )
        return json.loads(result.content)
    
    async def table_select(self, table_name: str, filters: Optional[Dict[str, Any]] = None,
                          columns: Optional[List[str]] = None,
                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Select from table."""
        result = await self.supabase_tool.execute(
            tool_name="table_operation",
            table_name=table_name,
            operation="select",
            filters=filters or {},
            columns=columns,
            limit=limit
        )
        data = json.loads(result.content)
        return data.get("data", [])
    
    async def table_insert(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert into table."""
        result = await self.supabase_tool.execute(
            tool_name="table_operation",
            table_name=table_name,
            operation="insert",
            data=data
        )
        return json.loads(result.content)
    
    async def table_update(self, table_name: str, data: Dict[str, Any],
                          filters: Dict[str, Any]) -> Dict[str, Any]:
        """Update table rows."""
        result = await self.supabase_tool.execute(
            tool_name="table_operation",
            table_name=table_name,
            operation="update",
            data=data,
            filters=filters
        )
        return json.loads(result.content)
    
    async def table_delete(self, table_name: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Delete from table."""
        result = await self.supabase_tool.execute(
            tool_name="table_operation",
            table_name=table_name,
            operation="delete",
            filters=filters
        )
        return json.loads(result.content)
    
    # =========================================================================
    # Convenience Methods
    # =========================================================================
    
    def generate_session_id(self) -> str:
        """Generate unique session ID."""
        return f"session_{uuid4().hex[:16]}"
    
    def generate_project_id(self, name: str) -> str:
        """Generate project ID from name."""
        safe_name = name.lower().replace(" ", "_")
        return f"project_{safe_name}_{uuid4().hex[:8]}"
```

---

### **Step 5: Integration Testing** ⏱️ 30 minutes

**Test Script** (`tests/test_phase2_supabase.py`):

```python
"""Phase 2 Supabase Integration Tests"""

import asyncio
import pytest
from mini_agent.memory.supabase_memory import SupabaseMemory
from mini_agent.tools.mcp_loader import load_mcp_tools_async

@pytest.mark.asyncio
async def test_supabase_mcp_connection():
    """Test Supabase MCP server connection."""
    tools = await load_mcp_tools_async()
    supabase_tool = next((t for t in tools if "supabase" in t.name.lower()), None)
    
    assert supabase_tool is not None, "Supabase MCP tool not loaded"
    print("✅ Supabase MCP server connected")

@pytest.mark.asyncio
async def test_project_memory():
    """Test project memory operations."""
    tools = await load_mcp_tools_async()
    memory = SupabaseMemory(tools)
    
    # Create project
    project_id = memory.generate_project_id("Test Project")
    result = await memory.create_project(
        project_id=project_id,
        context={"goal": "Test Mini-Agent memory", "status": "active"},
        metadata={"created_by": "test_suite"}
    )
    assert result["success"] == True
    print(f"✅ Created project: {project_id}")
    
    # Read project
    project = await memory.get_project(project_id)
    assert project is not None
    assert project["context"]["goal"] == "Test Mini-Agent memory"
    print("✅ Retrieved project context")
    
    # Update project
    await memory.update_project(
        project_id=project_id,
        context={"goal": "Test Mini-Agent memory", "status": "completed"}
    )
    print("✅ Updated project context")
    
    # List projects
    projects = await memory.list_projects()
    assert len(projects) > 0
    print(f"✅ Listed {len(projects)} projects")

@pytest.mark.asyncio
async def test_session_memory():
    """Test session memory operations."""
    tools = await load_mcp_tools_async()
    memory = SupabaseMemory(tools)
    
    # Create session
    session_id = memory.generate_session_id()
    result = await memory.create_session(
        session_id=session_id,
        initial_messages=[
            {"role": "user", "content": "Hello Mini-Agent!"},
            {"role": "assistant", "content": "Hello! How can I help you today?"}
        ]
    )
    assert result["success"] == True
    print(f"✅ Created session: {session_id}")
    
    # Append to session
    await memory.append_to_session(
        session_id=session_id,
        messages=[
            {"role": "user", "content": "Tell me about Supabase integration"},
            {"role": "assistant", "content": "Supabase provides persistent storage..."}
        ]
    )
    print("✅ Appended messages to session")
    
    # Read session
    session = await memory.get_session(session_id)
    assert session is not None
    assert len(session["messages"]) == 4
    print(f"✅ Retrieved session with {len(session['messages'])} messages")

@pytest.mark.asyncio
async def test_table_operations():
    """Test direct table operations."""
    tools = await load_mcp_tools_async()
    memory = SupabaseMemory(tools)
    
    # Insert
    result = await memory.table_insert(
        table_name="mini_agent_tool_logs",
        data={
            "session_id": "test_session",
            "tool_name": "test_tool",
            "parameters": {"param1": "value1"},
            "result": {"success": True},
            "execution_time_ms": 150,
            "success": True
        }
    )
    assert result["success"] == True
    print("✅ Inserted into tool_logs table")
    
    # Select
    logs = await memory.table_select(
        table_name="mini_agent_tool_logs",
        filters={"session_id": "test_session"},
        limit=10
    )
    assert len(logs) > 0
    print(f"✅ Retrieved {len(logs)} log entries")

if __name__ == "__main__":
    asyncio.run(test_supabase_mcp_connection())
    asyncio.run(test_project_memory())
    asyncio.run(test_session_memory())
    asyncio.run(test_table_operations())
    print("\n🎉 All Phase 2 tests passed!")
```

---

### **Step 6: Update Agent to Use Memory** ⏱️ 30 minutes

**Task**: Integrate Supabase memory into Mini-Agent's agent logic.

**File to Modify**: `mini_agent/agent.py`

**Add Memory Initialization**:

```python
from mini_agent.memory.supabase_memory import SupabaseMemory

class Agent:
    def __init__(self, ...):
        # ... existing initialization ...
        
        # Initialize Supabase memory
        try:
            self.memory = SupabaseMemory(self.tools)
            self.memory_enabled = True
            logger.info("Supabase memory initialized")
        except Exception as e:
            logger.warning(f"Supabase memory not available: {e}")
            self.memory = None
            self.memory_enabled = False
        
        # Generate session ID
        if self.memory_enabled:
            self.session_id = self.memory.generate_session_id()
            asyncio.create_task(self._init_session())
    
    async def _init_session(self):
        """Initialize session memory."""
        try:
            await self.memory.create_session(
                session_id=self.session_id,
                initial_messages=[]
            )
            logger.info(f"Session memory created: {self.session_id}")
        except Exception as e:
            logger.error(f"Failed to initialize session memory: {e}")
    
    async def _store_message(self, role: str, content: str):
        """Store message in session memory."""
        if not self.memory_enabled:
            return
        
        try:
            await self.memory.append_to_session(
                session_id=self.session_id,
                messages=[{
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }]
            )
        except Exception as e:
            logger.error(f"Failed to store message: {e}")
    
    async def run(self, user_message: str):
        """Run agent with memory persistence."""
        # Store user message
        await self._store_message("user", user_message)
        
        # ... existing agent logic ...
        
        # Store assistant response
        await self._store_message("assistant", response)
        
        return response
```

---

## 📊 Success Criteria

### **Phase 2 Complete When:**

- ✅ Supabase MCP server running and connected
- ✅ All database tables created with proper schema
- ✅ Project memory operations functional
- ✅ Session memory operations functional
- ✅ Table CRUD operations working
- ✅ Memory integration layer complete
- ✅ Agent using memory for persistence
- ✅ All tests passing
- ✅ Documentation complete

### **Metrics to Track:**

| Metric | Target | Actual |
|--------|--------|--------|
| MCP Server Startup Time | <5s | ___ |
| Average Query Time | <200ms | ___ |
| Memory Persistence Success Rate | >99% | ___ |
| Session History Accuracy | 100% | ___ |
| Database Connection Uptime | >99.9% | ___ |

---

## 📚 Next Steps After Phase 2

1. Monitor memory usage and optimize queries
2. Implement knowledge graph functionality
3. Add data export/import capabilities
4. Begin Phase 3 (Langfuse + ACP) when ready

---

*Last Updated: November 24, 2025*
