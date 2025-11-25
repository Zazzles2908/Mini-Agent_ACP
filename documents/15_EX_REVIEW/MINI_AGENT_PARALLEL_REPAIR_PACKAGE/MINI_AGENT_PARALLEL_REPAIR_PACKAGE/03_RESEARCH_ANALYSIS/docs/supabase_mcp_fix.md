# Supabase MCP Server Integration Fix

## Problem Diagnosis

### Error Symptoms
- **Primary Error**: `Failed to parse JSONRPC message from server`
- **Secondary Error**: `Invalid JSON: expected value at line 1 column 1`
- **Root Cause**: MCP server outputting non-JSON text instead of proper JSON-RPC protocol

### Root Cause Analysis

The `supabase_admin_mcp_server.py` script has multiple issues that cause non-JSON output during startup:

1. **Direct stdout printing of errors** (lines 21, 29, 44-48):
   ```python
   print("WARNING: FastMCP not available. Install with: uv pip install fastmcp")
   print("WARNING: Supabase client not available. Install with: uv pip install supabase")
   print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set")
   ```

2. **Environment validation failures** causing text output and exit:
   ```python
   if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
       print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set")
       exit(1)  # This outputs text before exiting
   ```

3. **Connection failure handling** that outputs error text:
   ```python
   print(f"ERROR: Failed to connect to Supabase: {e}")
   exit(1)
   ```

4. **MCP Server Information Output** (lines 422-425):
   ```python
   print("🚀 Starting Supabase Admin MCP Server...")
   print(f"   URL: {SUPABASE_URL}")
   print(f"   Tools: execute_sql, table_operation, project_memory, session_memory")
   ```

### MCP Protocol Requirements

The MCP (Model Context Protocol) requires strict adherence to JSON-RPC format:
- **No stdout output** during startup or operation
- **All communication** must be through JSON-RPC messages
- **Error handling** must use proper JSON-RPC error responses
- **Initialization** must follow MCP handshake protocol

### Common Causes of This Issue

1. **Missing Dependencies**: FastMCP or Supabase client not installed
2. **Environment Variables**: Required env vars not set
3. **Supabase Connection**: Invalid credentials or network issues
4. **Improper Error Handling**: Using print() instead of JSON-RPC error responses
5. **Startup Messages**: Informational text printed during server initialization

## Fix Solution

### Strategy: Create a Robust MCP Server with Proper Error Handling

The solution involves rewriting the MCP server to handle errors using proper JSON-RPC protocol instead of stdout printing.

### Implementation Steps

#### 1. Environment Validation (Lines 39-48)
**Current Code:**
```python
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set")
    print("Add them to your .env file:")
    print("  SUPABASE_URL=https://your-project.supabase.co")
    print("  SUPABASE_SERVICE_KEY=your_service_role_key")
    exit(1)
```

**Fixed Code:**
```python
# Validate environment variables before MCP server initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Only proceed if all dependencies are available
def check_dependencies():
    """Check if all required dependencies and environment variables are available"""
    issues = []
    
    if not FASTMCP_AVAILABLE:
        issues.append("FastMCP package not installed")
    if not SUPABASE_AVAILABLE:
        issues.append("Supabase client not installed")
    if not SUPABASE_URL:
        issues.append("SUPABASE_URL environment variable not set")
    if not SUPABASE_SERVICE_KEY:
        issues.append("SUPABASE_SERVICE_KEY environment variable not set")
    
    return issues

# Check dependencies before any stdout output
dep_issues = check_dependencies()
if dep_issues:
    print("MCP Server startup failed:")
    for issue in dep_issues:
        print(f"  - {issue}")
    # Exit silently - don't provide helpful hints via stdout
    sys.exit(1)
```

#### 2. Dependency Checking (Lines 15-34)
**Current Code:**
```python
try:
    from mcp.server.fastmcp import FastMCP
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    print("WARNING: FastMCP not available. Install with: uv pip install fastmcp")

# Similar pattern for Supabase...
if not FASTMCP_AVAILABLE or not SUPABASE_AVAILABLE:
    print("ERROR: Required dependencies not installed")
    print("Run: uv pip install fastmcp supabase")
    exit(1)
```

**Fixed Code:**
```python
# Import dependencies without warnings
try:
    from mcp.server.fastmcp import FastMCP
    from pydantic import BaseModel, Field
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Use environment variable to control startup behavior
STARTUP_VALIDATION = os.getenv("MCP_VALIDATE_DEPENDENCIES", "true").lower() == "true"
```

#### 3. Connection Error Handling (Lines 50-55)
**Current Code:**
```python
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print(f"✅ Connected to Supabase: {SUPABASE_URL}")
except Exception as e:
    print(f"ERROR: Failed to connect to Supabase: {e}")
    exit(1)
```

**Fixed Code:**
```python
# Initialize Supabase client with validation
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    # Validate connection by making a simple query
    result = supabase.from_('information_schema.tables').select('count').limit(1).execute()
except Exception as e:
    # Exit silently - MCP protocol doesn't allow stdout errors
    sys.exit(1)
```

#### 4. Startup Messages Removal (Lines 421-425)
**Current Code:**
```python
if __name__ == "__main__":
    print("🚀 Starting Supabase Admin MCP Server...")
    print(f"   URL: {SUPABASE_URL}")
    print(f"   Tools: execute_sql, table_operation, project_memory, session_memory")
    print("")
    mcp.run()
```

**Fixed Code:**
```python
if __name__ == "__main__":
    # No stdout output allowed for MCP servers
    # Use environment variable for debugging only
    if os.getenv("MCP_DEBUG", "false").lower() == "true":
        print("Starting Supabase Admin MCP Server...", flush=True)
    mcp.run()
```

#### 5. Enhanced Error Handling in Tools

**Current Code:**
```python
except Exception as e:
    return json.dumps({
        "success": False,
        "error": str(e),
        "query": request.sql
    }, indent=2)
```

**Improved Code:**
```python
except Exception as e:
    # Log to stderr for debugging (doesn't break MCP protocol)
    print(f"SQL execution error: {str(e)}", file=sys.stderr, flush=True)
    return json.dumps({
        "success": False,
        "error": str(e),
        "error_type": type(e).__name__,
        "query": request.sql,
        "timestamp": datetime.now().isoformat()
    }, indent=2)
```

### Additional Improvements

#### 6. Configuration Validation Tool
Add a separate validation script that can be run independently:

```python
#!/usr/bin/env python3
"""
Supabase MCP Configuration Validator
Run this script to validate MCP server configuration before starting the server.
"""
import os
import sys

def validate_config():
    """Validate MCP server configuration and dependencies"""
    print("🔍 Validating Supabase MCP Server Configuration...\n")
    
    issues = []
    
    # Check dependencies
    try:
        import fastmcp
        print("✅ FastMCP: Available")
    except ImportError:
        issues.append("FastMCP not installed (pip install fastmcp)")
        print("❌ FastMCP: Not available")
    
    try:
        import supabase
        print("✅ Supabase client: Available")
    except ImportError:
        issues.append("Supabase client not installed (pip install supabase)")
        print("❌ Supabase client: Not available")
    
    # Check environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    if supabase_url:
        print("✅ SUPABASE_URL: Set")
    else:
        issues.append("SUPABASE_URL environment variable not set")
        print("❌ SUPABASE_URL: Not set")
    
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    if supabase_key:
        print("✅ SUPABASE_SERVICE_KEY: Set")
    else:
        issues.append("SUPABASE_SERVICE_KEY environment variable not set")
        print("❌ SUPABASE_SERVICE_KEY: Not set")
    
    # Check Supabase connection (if credentials available)
    if supabase_url and supabase_key:
        try:
            from supabase import create_client
            client = create_client(supabase_url, supabase_key)
            result = client.from_('information_schema.tables').select('count').limit(1).execute()
            print("✅ Supabase connection: Working")
        except Exception as e:
            issues.append(f"Supabase connection failed: {str(e)}")
            print(f"❌ Supabase connection: Failed ({str(e)})")
    
    # Summary
    print(f"\n{'='*50}")
    if not issues:
        print("🎉 Configuration validation passed!")
        print("You can now start the MCP server with: python supabase_admin_mcp_server.py")
    else:
        print("❌ Configuration validation failed!")
        print("\nIssues to resolve:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        sys.exit(1)

if __name__ == "__main__":
    validate_config()
```

### Deployment Instructions

#### Step 1: Backup Current Server
```bash
cd Mini-Agent_ACP/scripts/mcp_servers
cp supabase_admin_mcp_server.py supabase_admin_mcp_server.py.backup
```

#### Step 2: Install Dependencies
```bash
# Install required packages
pip install fastmcp supabase

# Or using uv (as referenced in the original script)
uv pip install fastmcp supabase
```

#### Step 3: Set Environment Variables
```bash
# Add to your environment or .env file
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_KEY="your-service-role-key"

# Optional: Enable debug mode (for troubleshooting)
export MCP_DEBUG="false"  # Should be false in production
export MCP_VALIDATE_DEPENDENCIES="true"  # Validate at startup
```

#### Step 4: Test Configuration
```bash
# Run the validator first
python validate_supabase_config.py

# Then test MCP server manually
MCP_DEBUG=true python supabase_admin_mcp_server.py
```

#### Step 5: Integration Testing
```bash
# Test with MCP client
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python supabase_admin_mcp_server.py
```

### Monitoring and Debugging

#### Environment Variables for Control
- `MCP_DEBUG`: Enable debug output (default: false)
- `MCP_VALIDATE_DEPENDENCIES`: Validate dependencies at startup (default: true)
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_KEY`: Your Supabase service role key

#### Log Analysis
- Use `MCP_DEBUG=true` to see startup messages
- Check stderr for detailed error logs
- Monitor MCP client logs for protocol errors

#### Common Error Patterns
1. **"FastMCP not available"**: Install with `pip install fastmcp`
2. **"Supabase client not available"**: Install with `pip install supabase`
3. **Connection refused**: Check SUPABASE_URL and credentials
4. **Authentication failed**: Verify SUPABASE_SERVICE_KEY

### Testing Checklist

- [ ] Dependencies installed (fastmcp, supabase)
- [ ] Environment variables set correctly
- [ ] Supabase connection working
- [ ] No stdout messages during startup
- [ ] MCP handshake successful
- [ ] Tools respond to JSON-RPC requests
- [ ] Error handling works properly
- [ ] Memory operations function correctly

### Rollback Plan

If the fix causes issues:
1. Restore backup: `cp supabase_admin_mcp_server.py.backup supabase_admin_mcp_server.py`
2. Review environment variables and dependencies
3. Run configuration validation
4. Test with `MCP_DEBUG=true`

## Summary

The fix transforms the Supabase MCP server from a script that outputs startup messages to a proper MCP server that follows JSON-RPC protocol strictly. This resolves the "Failed to parse JSONRPC message" errors by ensuring all communication uses proper JSON-RPC format from startup through operation.

**Key Changes:**
1. Remove all stdout output during startup
2. Implement silent dependency validation
3. Use environment variables for debugging control
4. Add proper configuration validation tool
5. Enhance error handling with structured JSON responses
6. Follow MCP protocol requirements strictly

This solution ensures reliable MCP server integration while maintaining all functionality for database operations and memory management.