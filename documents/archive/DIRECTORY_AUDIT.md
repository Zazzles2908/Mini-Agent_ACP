# Mini-Agent Directory Audit & Cleanup Plan

## 🚨 **Current State Assessment**

### **The Mess: Evidence of Multiple Agent Attempts**
```
32+ batch/cmd files created by different agents
10+ Python launcher scripts with conflicting approaches
Multiple "FINAL", "ULTIMATE", "WORKING" versions
Conflicting documentation with contradictory instructions
```

### **Root Issues Identified**

1. **ACP Type Annotation Error**
   - Line 88 in `mini_agent/acp/__init__.py`: `InitializeRequest` type issue
   - Likely caused by ACP library version mismatches
   - Pylance complaining about type expressions

2. **MCP Configuration Overlap**
   - Deprecated minimax_search server still present
   - Hardcoded API keys in mcp.json (security issue)
   - Multiple conflicting configurations

3. **Package Structure Problems**
   - Relative import issues in ACP module
   - Path resolution problems
   - Version conflicts

## 📋 **Systematic Cleanup Plan**

### **Phase 1: Identify Working Components**
- [ ] Test core mini-agent functionality
- [ ] Verify which Python interpreter works
- [ ] Check which launcher scripts actually work
- [ ] Document real working configuration

### **Phase 2: Remove Messy Files**
- [ ] Remove all "duplicate launcher" files
- [ ] Delete conflicting batch files
- [ ] Remove debugging scripts
- [ ] Consolidate documentation

### **Phase 3: Fix Core Issues**
- [ ] Fix ACP type annotations
- [ ] Clean up MCP configuration
- [ ] Ensure proper import paths
- [ ] Update configuration files

### **Phase 4: Create Single Working Setup**
- [ ] One working launcher
- [ ] Clean configuration
- [ ] Clear documentation
- [ ] Proper file organization

## 🎯 **Immediate Actions Required**

### 1. **Fix ACP Type Error**
The Pylance error suggests version mismatch in ACP library imports.

### 2. **Remove Duplicates**
Archive or delete the 32+ batch files and multiple Python launchers.

### 3. **Consolidate Configuration**
Clean up mcp.json and config.yaml to remove deprecated entries.

### 4. **Create Single Launch Method**
Replace all the "FINAL", "ULTIMATE", "WORKING" files with one clean solution.

## 📝 **Files to Remove (First Pass)**

### Batch Files (Redundant):
- `COMMAND-CLARIFICATION.bat`
- `COMPLETE-DEBUG.bat` 
- `CONSOLE-FIX.bat`
- `COPY-PASTE-FIX.bat`
- `COPY-PASTE-TROUBLESHOOTING.bat`
- `CORRECT-COMMAND.bat`
- `EMERGENCY-IMPORT-FIX.bat`
- `FINAL-DEMONSTRATION.bat`
- `FINAL-MINI-AGENT-LAUNCHER.bat`
- `FINAL-STATUS.bat`
- `FINAL-TEST.bat`
- `INTERACTIVE-SESSION-FIX.bat`
- `LAUNCH-MINI-AGENT.bat`
- `MINI-AGENT-FIXED.bat`
- `MINI-AGENT-LAUNCHER.bat`
- `MINI-AGENT-PACKAGE-FIX.bat`
- `MINI-AGENT-WORKING.bat`
- `ONE-CLICK-LAUNCHER.bat`
- `SIMPLE-START.bat`
- `SIMPLE-WORKING-LAUNCHER.bat`
- `START-COMMAND.bat`
- `START-MINI-AGENT-EASY.bat`
- `STARTUP-DIAGNOSTIC.bat`
- `STATUS-CHECK.bat`
- `STOP-RIGHT-NOW-COMMAND-FIX.bat`
- `STOP-USING-OLD-COMMANDS.bat`
- `ULTIMATE-MINI-AGENT-LAUNCHER.bat`
- `WORKING-SOLUTION.bat`

### Python Scripts (Redundant):
- `launch_mini_agent_ultimate.py`
- `launch-mini-agent-fixed.py`
- `START_MINI_AGENT_NO_ERRORS.py`
- `quick-test.py`

### Documentation (Redundant):
- `COMMAND-GUIDE.md`
- `COPY-PASTE-COMMAND.md`
- `DEFINITIVE-SOLUTION.md`
- `FINAL-MINI-AGENT-LAUNCHER.bat` (already listed above)
- `FINAL-SOLUTION-COMPLETE.md`
- `FINAL-WORKING-SOLUTION.md`
- `LAUNCH_INSTRUCTIONS.md`
- `MINI-AGENT-FIX-COMPLETE.md`
- `ONE-CLICK-SOLUTION.md`
- `ONE-LINE-COMMAND.txt`
- `ONE-LINE-START.txt`
- `READ-ME-FIRST.txt`
- `STOP_USING_MINI-AGENT_COMMAND.md`
- `STOP-USING-OLD-COMMANDS.md`
- `SUCCESS-FINAL-STATUS.md`
- `ULTIMATE-SOLUTION.md`

## 🎯 **Keep These Files**

### Essential:
- `pyproject.toml` - Project configuration
- `README.md` - Main documentation  
- `LICENSE` - License file
- `.env` - Environment variables
- `mini_agent/` - Core package directory
- `tests/` - Test directory
- `docs/` - Documentation directory
- `examples/` - Examples directory

### Working Launchers (Pick One):
- `start-mini-agent.bat` - Simple working launcher
- `run-mini-agent.bat` - Alternative launcher

### Documentation (Consolidate):
- `USAGE_EXAMPLES.md` - Keep as reference

## 🚀 **Next Steps**

1. **Test Current Functionality** - Verify what's actually working
2. **Create Clean Environment** - Remove all the duplicates
3. **Fix ACP Issues** - Resolve the Pylance errors
4. **Single Launch Method** - One clean way to start mini-agent
5. **Clear Documentation** - Updated README with working instructions

---
*This audit was created to systematically clean up the mess from multiple agent attempts and get mini-agent working properly.*