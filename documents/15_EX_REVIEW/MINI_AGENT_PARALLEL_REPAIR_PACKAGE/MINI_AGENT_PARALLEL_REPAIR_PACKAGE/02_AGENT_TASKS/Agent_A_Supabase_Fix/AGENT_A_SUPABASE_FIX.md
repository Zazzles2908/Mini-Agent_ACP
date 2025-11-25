# Agent A: Supabase MCP Server Protocol Fix
*Priority: CRITICAL - Fix startup errors preventing system functionality*

## 🎯 Mission
Fix the "Failed to parse JSONRPC message from server" error that's preventing Supabase MCP integration during Mini-Agent startup.

## 📋 Current Problem
- **Error:** `Failed to parse JSONRPC message from server`
- **Cause:** MCP server outputs text instead of JSON-RPC protocol
- **Impact:** Supabase tools unavailable, startup errors
- **Location:** `scripts/mcp_servers/supabase_admin_mcp_server.py`

## 🛠️ Implementation Steps

### Step 1: Backup & Analysis
```bash
cd Mini-Agent_ACP/scripts/mcp_servers
cp supabase_admin_mcp_server.py supabase_admin_mcp_server.py.backup
```

### Step 2: Apply Protocol Fix
**Key Changes Required:**
1. **Remove all stdout output** during startup/initialization
2. **Redirect errors to stderr only** 
3. **Ensure pure JSON-RPC responses**
4. **Add environment control** for debugging

### Step 3: Deploy Fixed Version
```bash
# Install dependencies
pip install fastmcp supabase

# Test protocol compliance
python validate_supabase_config.py

# Restart Mini-Agent to verify fix
mini-agent
```

### Step 4: Validation
- ✅ No JSONRPC parsing errors in startup
- ✅ Supabase MCP server connects successfully
- ✅ Supabase tools become available
- ✅ Clean startup logs

## 📁 Resources
- **Fix Plan:** `/workspace/docs/supabase_mcp_fix.md`
- **Fixed Server:** `supabase_admin_mcp_server_fixed.py`
- **Validation Tool:** `validate_supabase_config.py`

## 🎯 Success Criteria
**Complete when:** Mini-Agent starts without Supabase MCP errors and Supabase tools are functional.

## ⏱️ Estimated Time
**Target:** 2-3 hours
**Max:** 4 hours
