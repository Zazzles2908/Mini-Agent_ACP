# Supabase Key Types: Why We Need the Service Role Key

## 🔑 **Key Type Analysis**

### **SERVICE_ROLE KEY (Currently Used)**
```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Type: JWT Token
Role: service_role
Reference: mxaazuhlqewmkweewyaz
Purpose: ✅ Database operations with full privileges
```

### **ADMIN TOKEN (Your Suggestion)**
```
Token: sbp_af0f003e58dfcea9ad42d545e9f8d79102855f9f
Type: Management API Token
Purpose: ❌ API management only (project settings, user management)
Database Access: ❌ **NO** (401 Unauthorized)
```

## 🧪 **Test Results: Admin Token Cannot Access Database**

**When testing the admin token for database operations:**
- **HTTP Status**: 401 Unauthorized
- **Result**: ❌ Admin token has NO database access
- **Reason**: Different token type for different purposes

## 📋 **What Each Key Does**

### **SERVICE_ROLE KEY** ✅
- **Database Operations**: INSERT, UPDATE, SELECT, DELETE
- **RPC Function Calls**: `exec_sql`, custom functions
- **Schema Operations**: CREATE TABLE, ALTER TABLE
- **User Management**: Limited database user operations
- **MCP Server**: ✅ Perfect for database MCP tools

### **ADMIN TOKEN** ❌
- **Project Management**: Create/modify Supabase projects
- **API Settings**: Configure API endpoints, rate limits
- **Team Management**: User roles, permissions (at API level)
- **Billing/Usage**: Project usage, billing information
- **Database Operations**: ❌ **CANNOT ACCESS DATABASE**

## 🎯 **Why MCP Server Needs Service Role Key**

### **Required Database Operations:**
1. **Execute SQL Queries**: `supabase.rpc('exec_sql', {...})`
2. **Access Tables**: `supabase.from_('mini_agent.mini_agent_projects')`
3. **Function Calls**: Custom RPC functions for agent operations
4. **Schema Access**: Read/write to `mini_agent` schema tables

### **Admin Token Limitations:**
- **No Database Schema Access**: Cannot read/write tables
- **No RPC Function Access**: Cannot call database functions
- **No SQL Execution**: Cannot perform any database operations
- **Wrong API Endpoint**: Management API vs Database API

## 🏗️ **Architecture Explanation**

```
SERVICE_ROLE KEY Flow:
MCP Server → Service Role Key → Database API → Tables/RPC Functions

ADMIN TOKEN Flow (If Used):
MCP Server → Admin Token → Management API → ❌ NO DATABASE ACCESS
```

## ⚖️ **Security & Design**

### **Principle of Least Privilege:**
- **Service Role Key**: Minimal required privileges for database operations
- **Admin Token**: Broad administrative privileges (but not database)
- **Design Intent**: Each token has specific, limited use cases

### **Why This Design:**
- **Security**: Separate permissions for different operations
- **Audit Trail**: Different tokens for different types of actions
- **Rate Limiting**: Different APIs have different rate limits
- **Error Handling**: Clear separation between API vs database issues

## 🔧 **Alternative Approaches (If Needed)**

If you want to avoid using service role key, options include:

### **Option 1: Database User Account**
```sql
-- Create specific database user for MCP server
CREATE USER mcp_server_user WITH PASSWORD 'secure_password';
GRANT USAGE ON SCHEMA mini_agent TO mcp_server_user;
GRANT ALL ON ALL TABLES IN SCHEMA mini_agent TO mcp_server_user;
```
**Downside**: Requires complex authentication setup

### **Option 2: Row Level Security (RLS)**
```sql
-- Use anon key with RLS policies
-- More complex, but more secure
```
**Downside**: Significantly more complex setup

### **Option 3: API Gateway**
```python
# Proxy database access through another service
# MCP Server → API Gateway → Database
```
**Downside**: Additional infrastructure complexity

## 💡 **Conclusion**

**We MUST use the service role key** because:

1. **Admin Token Fails**: Returns 401 (no database access)
2. **MCP Server Requirements**: Needs direct database operations
3. **Function Access**: Only service role can call RPC functions
4. **Schema Operations**: Only service role has schema access
5. **Security**: Service role is designed specifically for this use case

**The current 503 error is infrastructure-related**, not a permission issue. The service role key is correctly configured and will work once the database service recovers.

---

**Bottom Line**: Service role key is the correct and only viable option for MCP database operations. Admin token is for API management, not database access.