# 🔙 EMERGENCY ROLLBACK PROCEDURES
## Complete Guide to Reverting Mini-Agent Upgrade Implementation

**Created**: November 24, 2025  
**Purpose**: Emergency rollback procedures for Mini-Agent self-awareness upgrade implementation  
**Branch**: `self-awareness-upgrade-implementation`  
**Safe Point**: Main branch before implementation begins

---

## 🚨 **WHEN TO ROLLBACK**

### **Immediate Rollback Triggers:**
- ❌ **System crashes or critical failures**
- ❌ **Agent becomes unresponsive or loops indefinitely**
- ❌ **Configuration corruption prevents agent startup**
- ❌ **Database migration fails or corrupts data**
- ❌ **Performance degradation > 50%**
- ❌ **Security vulnerabilities introduced**
- ❌ **Agent tools stop working entirely**

### **Non-Critical Issues (Don't Rollback):**
- ⚠️ Minor performance impact (< 20%)
- ⚠️ New features not working as expected
- ⚠️ Configuration warnings (can fix incrementally)
- ⚠️ Documentation inconsistencies

---

## 🔙 **ROLLBACK PROCEDURES**

### **Method 1: Complete Branch Revert (RECOMMENDED)**
**When**: Any critical issue or when you want to return to pre-upgrade state

```bash
# 1. Navigate to main branch (safe state)
git checkout main
git pull origin main

# 2. Create emergency recovery branch
git checkout -b emergency-recovery-$(date +%Y%m%d-%H%M%S)

# 3. Force push to overwrite upgrade branch
git push origin main --force

# 4. Reset local repository
git reset --hard origin/main

# 5. Verify rollback
git status
git log --oneline -5
```

### **Method 2: Selective File Revert**
**When**: Specific files causing issues (configuration, specific modules)

```bash
# 1. Checkout specific files from main branch
git checkout main -- mini_agent/config/config.yaml
git checkout main -- mini_agent/cli.py
git checkout main -- mini_agent/agent.py

# 2. Check what changed
git status
git diff

# 3. Test agent startup
python -m mini_agent.cli

# 4. If successful, commit the revert
git add .
git commit -m "🔙 ROLLBACK: Reverted critical files to main branch state"
```

### **Method 3: Database Rollback**
**When**: Database migration caused issues

```sql
-- Execute in Supabase SQL Editor to rollback migration
-- WARNING: This will DELETE all data created by the upgrade

-- Drop upgrade tables (if they exist)
DROP TABLE IF EXISTS mini_agent_project_memory CASCADE;
DROP TABLE IF EXISTS mini_agent_pattern_learning CASCADE;
DROP TABLE IF EXISTS mini_agent_execution_insights CASCADE;
DROP TABLE IF EXISTS mini_agent_performance_analytics CASCADE;
DROP TABLE IF EXISTS mini_agent_web_intelligence CASCADE;
DROP TABLE IF EXISTS mini_agent_context_learnings CASCADE;

-- Drop custom RPC functions (if they exist)
DROP FUNCTION IF EXISTS exec_sql;
DROP FUNCTION IF EXISTS list_tables;
```

### **Method 4: Configuration Recovery**
**When**: Configuration files become corrupted

```bash
# 1. Restore config from backup (main branch)
git checkout main -- mini_agent/config/config.yaml
git checkout main -- mini_agent/config/.mcp.json
git checkout main -- mini_agent/config/system_prompt.md

# 2. Clear environment variables (if upgrade added new ones)
unset MINIMAX_MEMORY_ENHANCED
unset MINIMAX_WEB_INTELLIGENCE  
unset MINIMAX_SELF_AWARENESS

# 3. Test configuration
python -c "from mini_agent.config import get_config; print('Config OK')"
```

---

## 🧪 **VERIFICATION PROCEDURES**

### **After Any Rollback, Always Verify:**

```bash
# 1. Basic System Health
python -c "import mini_agent; print('✅ Package import OK')"

# 2. Configuration Loading
python -c "from mini_agent.config import get_config; print('✅ Config loading OK')"

# 3. Agent Initialization
python -c "
from mini_agent.agent import Agent
from mini_agent.llm import LLMClient
print('✅ Agent class import OK')
"

# 4. Tool Loading Test
python -c "
from mini_agent.tools.mcp_loader import load_mcp_tools_async
import asyncio
async def test():
    tools = await load_mcp_tools_async('mini_agent/config/.mcp.json')
    print(f'✅ MCP tools loaded: {len(tools)} tools')
asyncio.run(test())
"

# 5. CLI Startup Test (quick check)
timeout 10s python -m mini_agent.cli --help || echo "✅ CLI responds (with timeout)"
```

### **Database Verification:**
```sql
-- Check that original tables are intact
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'mini_agent%';
```

---

## 📋 **ROLLBACK CHECKLIST**

### **Immediate Actions (0-5 minutes):**
- [ ] Identify the specific issue
- [ ] Choose appropriate rollback method
- [ ] Execute rollback procedure
- [ ] Verify basic system functionality
- [ ] Test agent startup

### **Verification (5-15 minutes):**
- [ ] Run all verification procedures above
- [ ] Test existing functionality (web search, tools, MCP)
- [ ] Verify configuration loads correctly
- [ ] Check that no new environment variables remain
- [ ] Confirm database is in original state (if applicable)

### **Cleanup (15-30 minutes):**
- [ ] Remove any upgrade branch if problematic
- [ ] Archive upgrade work for future reference
- [ ] Update this rollback document with lessons learned
- [ ] Document any files that needed manual intervention
- [ ] Create incident report if issue was critical

---

## 🗂️ **FILE CHANGES SUMMARY**

### **Files that will be modified during upgrade:**
```
⚠️ CRITICAL FILES (Most likely to need rollback):
├── mini_agent/config/config.yaml          # New configuration sections
├── mini_agent/cli.py                      # Enhanced tool loading
├── mini_agent/agent.py                    # Agent class enhancements
├── mini_agent/config/__init__.py          # Config class extensions
├── mini_agent/tools/mcp_loader.py         # Enhanced MCP loading
└── mini_agent/tools/note_tool.py          # Enhanced session memory

📁 NEW FILES TO DELETE (if rollback needed):
├── scripts/mcp_servers/enhanced_memory_mcp_server.py
├── scripts/mcp_servers/web_intelligence_mcp_server.py
├── scripts/mcp_servers/self_awareness_mcp_server.py
├── scripts/upgrade_implementation/ (entire directory)
└── mini_agent/upgrade/ (entire directory)

🗄️ DATABASE CHANGES:
├── New tables in Supabase (see migration rollback above)
├── New RPC functions (drop via SQL above)
└── Updated configuration in Supabase settings
```

### **Safe Files (Generally don't need rollback):**
- `documents/` files (documentation only)
- `scripts/test_*.py` (testing scripts)
- `migrations/` (can be re-run)
- Configuration examples in `mini_agent/config/`

---

## 📞 **ESCALATION PROCEDURES**

### **If Rollback Fails:**
1. **Check git history**: `git log --oneline -20`
2. **Identify last working commit**: Look for commits before upgrade
3. **Hard reset**: `git reset --hard <last-working-commit>`
4. **Force push**: `git push origin main --force`

### **If Database Cannot Be Recovered:**
1. **Contact Supabase support** with database URL
2. **Request point-in-time restore** to before migration
3. **Export critical data** before attempting recovery
4. **Use backup if available** from before upgrade

### **If System Remains Corrupted:**
1. **Fork from main branch** in GitHub
2. **Clone fresh repository**: `git clone <main-branch-url>`
3. **Restore from backup**: Use backup from before upgrade
4. **Contact Mini-Agent community** for support

---

## 📚 **ROLLBACK HISTORY**

| Date | Issue | Rollback Method | Resolution |
|------|-------|----------------|------------|
| - | - | - | - |
| [Add rollback incidents here for tracking] |

---

## 🔧 **PREVENTION FOR FUTURE**

### **Before Each Implementation Phase:**
1. **Create tagged release**: `git tag pre-upgrade-phase1`
2. **Backup current state**: Copy critical files to backup directory
3. **Test rollback procedure**: Practice on non-critical changes first
4. **Document changes**: Keep detailed change log

### **During Implementation:**
1. **Commit frequently**: Small, testable changes
2. **Test after each commit**: Verify system still works
3. **Keep rollback ready**: Have commands prepared
4. **Monitor performance**: Watch for degradation

### **After Successful Implementation:**
1. **Tag release**: `git tag post-upgrade-phase1`
2. **Update rollback docs**: Add lessons learned
3. **Archive backup**: Store safely for future reference
4. **Test rollback again**: Verify you can still rollback

---

## ✅ **SUCCESS INDICATORS**

**Rollback was successful if:**
- ✅ Agent starts without errors
- ✅ All existing tools work (file operations, bash, web search)
- ✅ MCP servers load correctly
- ✅ Configuration loads without warnings
- ✅ Performance is at or near pre-upgrade levels
- ✅ No orphaned processes or memory leaks
- ✅ Database is in original state (if applicable)

---

**🎯 REMEMBER**: When in doubt, rollback! It's always safer to return to a working state and try again with a different approach than to continue with a broken system.

---

*Last Updated: November 24, 2025*  
*Version: 1.0*  
*Branch: self-awareness-upgrade-implementation*  
*Safe State: main (commit d5e1d2b)*