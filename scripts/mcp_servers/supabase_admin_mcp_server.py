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
try:
    from mcp.server.fastmcp import FastMCP
    from pydantic import BaseModel, Field
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    print("WARNING: FastMCP not available. Install with: uv pip install fastmcp")

# Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("WARNING: Supabase client not available. Install with: uv pip install supabase")

if not FASTMCP_AVAILABLE or not SUPABASE_AVAILABLE:
    print("ERROR: Required dependencies not installed")
    print("Run: uv pip install fastmcp supabase")
    exit(1)

# Initialize MCP server
mcp = FastMCP("supabase_admin")

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set")
    print("Add them to your .env file:")
    print("  SUPABASE_URL=https://your-project.supabase.co")
    print("  SUPABASE_SERVICE_KEY=your_service_role_key")
    exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print(f"✅ Connected to Supabase: {SUPABASE_URL}")
except Exception as e:
    print(f"ERROR: Failed to connect to Supabase: {e}")
    exit(1)

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
        
        # Execute query using Supabase postgrest
        # Note: For raw SQL, we use rpc if available or direct postgres connection
        result = supabase.rpc('exec_sql', {'query_text': request.sql}).execute()
        
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
                "project": result.data[0] if result.data else None
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
                "project": result.data[0] if result.data else None
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
                "session": result.data[0] if result.data else None
            }, indent=2)
        
        elif request.operation == "append":
            # Get existing session
            existing = table.select("messages").eq("session_id", request.session_id).execute()
            
            if existing.data:
                current_messages = existing.data[0]["messages"]
                updated_messages = current_messages + (request.messages or [])
                
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
    print("🚀 Starting Supabase Admin MCP Server...")
    print(f"   URL: {SUPABASE_URL}")
    print(f"   Tools: execute_sql, table_operation, project_memory, session_memory")
    print("")
    mcp.run()
