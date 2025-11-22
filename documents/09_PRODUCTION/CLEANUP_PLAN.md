# 🧹 Mini-Agent Repository Cleanup Plan
**Status**: READY TO EXECUTE  
**Estimated Time**: 2-3 hours  
**Based on**: BRUTAL_CODE_AUDIT.md

---

## 🎯 OBJECTIVES

1. **Respect .gitignore** - Remove tracked files that should be ignored
2. **Preserve WIP** - Keep research/experimental work organized
3. **Follow own standards** - Use `documents/` for all documentation
4. **Clean root** - Reduce root directory clutter
5. **Maintain functionality** - Don't break anything that works

---

## 📦 WHAT WE'RE PRESERVING

### Research & WIP (Moving to documents/)
```
KEEP BUT ORGANIZE:
├── zed_research/          → documents/experiments/zed_acp/
│   └── (empty - placeholder for Zed ACP work)
├── vscode-extension/      → KEEP in root (active project)
├── mini-agent-*.vsix      → documents/builds/archive/ (failed attempts, keep for reference)
├── production/            → documents/production/ (deployment configs)
└── comprehensive_tool_audit* → documents/audits/ (historical value)
```

### Active Development
```
KEEP AS-IS:
├── mini_agent/            # Core package
├── tests/                 # Test suite  
├── scripts/               # Utility scripts
├── examples/              # Example usage
└── vscode-extension/      # VS Code integration (active)
```

---

## 🗑️ PHASE 1: GITIGNORE ENFORCEMENT (Critical)

### 1.1 Remove Cached Files That Should Be Ignored

```bash
# Remove Python cache
git rm -r --cached mini_agent/**/__pycache__
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Remove session memory
git rm --cached .agent_memory.json

# Remove VSCode settings (should be user-specific)
git rm -r --cached .vscode

# Remove workspace outputs (if any)
git ls-files workspace/ | xargs git rm --cached

# Remove any .log files
git ls-files "*.log" | xargs git rm --cached
```

### 1.2 Verify .gitignore is Correct

```bash
# Check current .gitignore
cat .gitignore

# Should include (already there, just not enforced):
# - __pycache__/
# - .vscode/
# - workspace/
# - *.log
# - .agent_memory.json
# - .venv (CRITICAL - check if .venv is tracked!)
```

### 1.3 Handle .venv (CRITICAL)

```bash
# Check if .venv is tracked
git ls-files .venv/

# If output shows files, REMOVE IMMEDIATELY:
git rm -r --cached .venv
# This removes from git but keeps local .venv intact
```

---

## 📁 PHASE 2: DIRECTORY REORGANIZATION

### 2.1 Create Organized Structure

```bash
# Create new organization
mkdir -p documents/experiments/zed_acp
mkdir -p documents/experiments/vscode_attempts
mkdir -p documents/builds/archive
mkdir -p documents/audits
mkdir -p documents/production
mkdir -p documents/minimax_original
mkdir -p documents/research
mkdir -p documents/archive
```

### 2.2 Move Research & Experiments

```bash
# Zed research (preserve for future work)
# It's empty, just create proper home
echo "# Zed Editor ACP Integration Research" > documents/experiments/zed_acp/README.md
echo "" >> documents/experiments/zed_acp/README.md
echo "## Goal" >> documents/experiments/zed_acp/README.md
echo "Implement Agent Client Protocol (ACP) integration with Zed editor" >> documents/experiments/zed_acp/README.md
echo "" >> documents/experiments/zed_acp/README.md
echo "## Status" >> documents/experiments/zed_acp/README.md
echo "📋 Planning phase - not yet started" >> documents/experiments/zed_acp/README.md
echo "" >> documents/experiments/zed_acp/README.md
echo "## Related" >> documents/experiments/zed_acp/README.md
echo "- VSCode extension: `/vscode-extension/`" >> documents/experiments/zed_acp/README.md
echo "- ACP server: `/mini_agent/acp/`" >> documents/experiments/zed_acp/README.md
rmdir zed_research

# VS Code build artifacts (failed attempts - keep for reference)
mv mini-agent-acp-1.0.0.vsix documents/builds/archive/
mv mini-agent-vscode-1.0.0.vsix documents/builds/archive/
echo "# VS Code Extension Build Archive" > documents/builds/archive/README.md
echo "" >> documents/builds/archive/README.md
echo "These are archived build attempts. Current development in /vscode-extension/" >> documents/builds/archive/README.md

# Tool audits (historical value)
mv comprehensive_tool_audit.py documents/audits/
mv comprehensive_tool_audit_results.json documents/audits/
mv COMPREHENSIVE_TOOL_AUDIT_SUMMARY.md documents/audits/

# Production configs
mv production/* documents/production/
rmdir production
```

### 2.3 Move Old Documentation

```bash
# Consolidate docs/ and documents/
if [ -d "docs" ]; then
    mv docs/* documents/minimax_original/ 2>/dev/null || true
    rmdir docs
fi

# Move output/research
if [ -d "output/research" ]; then
    mv output/research/* documents/research/ 2>/dev/null || true
fi

# Move output/test_results  
if [ -d "output/test_results" ]; then
    mv output/test_results/* documents/archive/test_results/ 2>/dev/null || true
fi

# Clean up empty output/
if [ -d "output" ]; then
    rm -rf output/logs  # Empty
    rmdir output 2>/dev/null || rm -rf output
fi
```

### 2.4 Archive Old Results

```bash
# Move archive/ to documents/archive/
if [ -d "archive" ]; then
    mv archive/* documents/archive/old_backups/ 2>/dev/null || true
    rmdir archive
fi
```

### 2.5 Handle Fixed Files

```bash
# mini_agent_fixed_files - document what these are
ls -la mini_agent_fixed_files/

# If they're backups from a fix, archive them:
mv mini_agent_fixed_files documents/archive/fixed_files_backup_$(date +%Y%m%d)/

# Or if they're obsolete, just delete:
# rm -rf mini_agent_fixed_files/
```

### 2.6 Clean Empty Directories

```bash
# Remove empty logs directory
rmdir logs 2>/dev/null || true
```

---

## ⚙️ PHASE 3: CONFIGURATION CLEANUP

### 3.1 Consolidate MCP Configuration

```bash
# Check both MCP configs
diff .mcp.json mini_agent/config/mcp.json

# If they're the same or .mcp.json is obsolete:
rm .mcp.json

# If they're different, document the difference:
echo "# MCP Configuration Files" > documents/CONFIG_NOTES.md
echo "" >> documents/CONFIG_NOTES.md
echo "## Consolidation Note" >> documents/CONFIG_NOTES.md
echo "Found duplicate MCP configs - review and consolidate" >> documents/CONFIG_NOTES.md
```

### 3.2 Document Configuration Hierarchy

```bash
cat > documents/CONFIGURATION.md << 'EOF'
# Configuration Guide

## Configuration Hierarchy

### 1. Main Configuration
**File**: `mini_agent/config/config.yaml`
- Tracked in git
- Default settings for all users
- Edit with caution - affects all installations

### 2. Local Overrides (Recommended)
**File**: `local_config.yaml` (root directory)
- Git-ignored (not tracked)
- User-specific settings
- Copy from `mini_agent/config/config-example.yaml`
- Override specific values only

### 3. Environment Variables
**File**: `.env` (root directory)
- Git-ignored (NEVER commit!)
- API keys and secrets
- Loaded automatically by agent

### 4. MCP Server Configuration
**File**: `mini_agent/config/mcp.json`
- MCP server connections
- Tool integrations

## Setup Instructions

```bash
# 1. Copy example config
cp mini_agent/config/config-example.yaml local_config.yaml

# 2. Create .env file
cat > .env << 'ENVFILE'
MINIMAX_API_KEY=your_minimax_key_here
ZAI_API_KEY=your_zai_key_here
OPENAI_API_KEY=your_openai_key_here
ENVFILE

# 3. Edit local_config.yaml with your preferences
# (e.g., default model, workspace path, etc.)
```

## Priority Order
When agent starts, it loads in this order:
1. `mini_agent/config/config.yaml` (base)
2. `local_config.yaml` (overrides)
3. `.env` (environment variables)

Later sources override earlier ones.
EOF
```

### 3.3 Update .gitignore

```bash
# Ensure local config is ignored
grep -q "local_config.yaml" .gitignore || echo "local_config.yaml" >> .gitignore

# Ensure build artifacts are ignored
grep -q "*.vsix" .gitignore || echo "*.vsix" >> .gitignore
```

---

## 📦 PHASE 4: DEPENDENCY CLEANUP

### 4.1 Remove Legacy Requirements File

```bash
# Check if requirements.txt is redundant
diff <(uv pip compile pyproject.toml) requirements.txt

# If pyproject.toml is source of truth, remove requirements.txt:
# (WAIT - let's verify this doesn't break anything first)
git mv requirements.txt documents/archive/requirements.txt.bak
```

### 4.2 Clean pyproject.toml

**Manual edit** - `pyproject.toml`:
```toml
# REMOVE these from dependencies:
# - "pip>=25.3"      # UV handles this
# - "pipx>=1.8.0"    # User-level tool, not project dependency

# KEEP only one dev dependencies section:
[project.optional-dependencies]
dev = [
    "pytest>=8.4.2",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=7.0.0",
    "pytest-xdist>=3.8.0",
]

# REMOVE duplicate:
# [dependency-groups]
# dev = [...]
```

---

## 📝 PHASE 5: DOCUMENTATION

### 5.1 Create Missing Standard Docs

```bash
# PROJECT_CONTEXT.md
cat > documents/PROJECT_CONTEXT.md << 'EOF'
# Mini-Agent Project Context

## Origin
**Created by**: MiniMax AI Team  
**Repository**: https://github.com/MiniMax-AI/agent-demo  
**Purpose**: Teaching-level agent demonstration with extensible architecture

## Architecture

### Core Components (by MiniMax)
- **Agent Loop**: `mini_agent/agent.py` - Execution loop with tool calling
- **LLM Clients**: `mini_agent/llm/` - Multi-provider support (MiniMax-M2, Anthropic, OpenAI, GLM)
- **Tools**: `mini_agent/tools/` - File operations, bash execution, MCP integration
- **Skills**: `mini_agent/skills/` - 20+ specialized capabilities (Claude skills)
- **Configuration**: `mini_agent/config/` - YAML-based configuration system

### Community Extensions (~10%)
- **Z.AI Integration**: GLM-4.5/4.6 models with web search capabilities
- **ACP Server**: `mini_agent/acp/` - Agent Client Protocol bridge
- **VS Code Extension**: `vscode-extension/` - Native Chat API integration
- **Zed Integration**: (Planned) - In research phase

## Project Structure
```
mini_agent/
├── agent.py              # Core agent execution loop
├── cli.py                # Command-line interface
├── config/               # Configuration files
├── llm/                  # LLM client wrappers
├── tools/                # Tool implementations
├── skills/               # Specialized skills (git submodule)
├── acp/                  # Agent Client Protocol server
└── schema/               # Data models

vscode-extension/         # VS Code integration (active development)
tests/                    # Test suite
scripts/                  # Utility scripts
examples/                 # Usage examples
documents/                # All project documentation
```

## Current Status (as of 2025-01-22)

### Stable
- ✅ Core agent execution
- ✅ Multi-LLM support
- ✅ File and bash tools
- ✅ Skills system
- ✅ CLI interface

### Active Development
- 🔄 VS Code ACP integration
- 🔄 Z.AI web search optimization
- 🔄 Test coverage improvements

### Planned
- 📋 Zed editor integration
- 📋 Agent class refactoring (separate concerns)
- 📋 CI/CD pipeline
- 📋 Pre-commit hooks

## Key Technologies
- **Language**: Python 3.10+
- **Package Manager**: uv (modern pip replacement)
- **LLM APIs**: Anthropic, OpenAI, MiniMax, Z.AI
- **Testing**: pytest with async support
- **Configuration**: YAML + environment variables
EOF

# AGENT_HANDOFF.md
cat > documents/AGENT_HANDOFF.md << 'EOF'
# Agent Handoff Notes

## Last Updated
2025-01-22 by Claude (Repository Cleanup Session)

## Current Status

### Just Completed
- ✅ Comprehensive code audit (see BRUTAL_CODE_AUDIT.md)
- ✅ Cleanup plan created (see CLEANUP_PLAN.md)
- 🔄 Executing cleanup phases

### In Progress
- Repository hygiene enforcement
- Directory reorganization
- Documentation consolidation

### Blocked
- None currently

## Next Steps

### Immediate (Today)
1. Complete Phase 1-5 of cleanup plan
2. Test that agent still runs after cleanup
3. Verify VS Code extension still works
4. Update README.md if paths changed

### This Week
1. Refactor Agent class (see audit recommendations)
2. Reorganize tests into unit/integration/e2e
3. Add test coverage reporting
4. Create VS Code extension README

### Future
1. Implement Zed editor ACP integration (see documents/experiments/zed_acp/)
2. Set up CI/CD pipeline
3. Add pre-commit hooks
4. Performance profiling

## Important Context

### Design Decisions
- **Gitignore violations**: Root cause was files committed before .gitignore rules added
- **Multiple LLM providers**: Intentional - allows user choice based on use case
- **Skills as submodule**: Shared resource, keep as submodule
- **VSIX files**: Archived failed VS Code build attempts, preserved for reference

### Known Issues
- Agent class is a god object (414 lines, multiple responsibilities)
- Test structure is flat (should be unit/integration/e2e)
- Configuration hierarchy not documented (now in documents/CONFIGURATION.md)

### Gotchas
- **Always use `uv`** for Python operations, not raw pip
- **Z.AI quota**: ~120 prompts per 5 hours, plan usage carefully
- **MCP tools**: Most are deprecated in favor of native tools
- **VS Code extension**: Has own node_modules, don't commit it

## For Next Agent

### Files to Review First
1. `documents/BRUTAL_CODE_AUDIT.md` - Comprehensive analysis
2. `documents/CLEANUP_PLAN.md` - This file
3. `documents/CONFIGURATION.md` - Config hierarchy
4. `documents/PROJECT_CONTEXT.md` - Project overview

### Commands to Run
```bash
# Verify environment
uv --version
python --version
ls -la .env  # Should exist with API keys

# Test agent
uv run mini-agent --version
uv run pytest tests/ -v

# Check git status
git status
git ls-files | wc -l  # Should be much smaller after cleanup
```

### Current Experiments
- **Zed ACP**: Placeholder in documents/experiments/zed_acp/ - not started
- **VS Code**: Active in vscode-extension/ - uses ACP server
- **Web Search**: Z.AI integration working, see mini_agent/tools/zai_*.py

### Questions to Investigate
1. Can we consolidate .mcp.json and mini_agent/config/mcp.json?
2. Is requirements.txt still needed or is pyproject.toml sufficient?
3. Should skills submodule be merged into main repo?
4. What's the test coverage percentage?
EOF
```

### 5.2 Update README (if needed)

```bash
# Check if README references moved files
grep -n "docs/" README.md
grep -n "output/" README.md
grep -n "archive/" README.md

# If found, update paths to documents/
```

---

## ✅ PHASE 6: COMMIT & VERIFY

### 6.1 Review Changes

```bash
# See what's been removed from git
git status

# See what's been moved
find documents/ -type f | head -20

# Verify .venv is NOT tracked
git ls-files .venv/  # Should be empty

# Verify cache is NOT tracked
git ls-files "**/__pycache__"  # Should be empty
```

### 6.2 Test Functionality

```bash
# Test agent still works
uv run mini-agent --help

# Run quick test
uv run pytest tests/test_agent.py -v

# Test VS Code extension (if possible)
cd vscode-extension
npm run compile  # Or whatever build command
```

### 6.3 Commit Changes

```bash
# Stage all changes
git add -A

# Commit with detailed message
git commit -m "fix: Repository cleanup - enforce gitignore, organize documentation

- Remove cached files that should be ignored (.venv, __pycache__, .agent_memory.json)
- Move research/experiments to documents/experiments/
- Archive old build artifacts to documents/builds/archive/
- Consolidate docs/ → documents/minimax_original/
- Move output/research → documents/research/
- Move production/ → documents/production/
- Create standard documentation (PROJECT_CONTEXT, AGENT_HANDOFF, CONFIGURATION)
- Remove empty directories (logs, zed_research)
- Preserve VS Code extension (active development)
- Preserve VSIX files for reference (Zed ACP research)

Ref: documents/BRUTAL_CODE_AUDIT.md, documents/CLEANUP_PLAN.md"

# Create tag for this milestone
git tag -a v0.1.1-cleanup -m "Repository cleanup and organization"
```

---

## 🎯 SUCCESS CRITERIA

After cleanup, verify:

- [ ] `git ls-files .venv/` returns nothing
- [ ] `git ls-files "**/__pycache__"` returns nothing  
- [ ] Root directory has <10 folders
- [ ] All docs are in `documents/`
- [ ] `uv run mini-agent --help` works
- [ ] `uv run pytest tests/ -k test_agent` passes
- [ ] No .log files tracked in git
- [ ] VS Code extension directory still intact
- [ ] .gitignore actually respected

---

## 📊 ESTIMATED IMPACT

### Before Cleanup
```
Repository size: ~XX MB (with .venv tracked)
Files tracked: ~XXXX files
Root directories: 15
Documentation locations: 3 (docs/, documents/, output/)
```

### After Cleanup  
```
Repository size: ~YY MB (much smaller)
Files tracked: ~XXX files (70% reduction)
Root directories: <10
Documentation locations: 1 (documents/)
```

---

## ⚠️ ROLLBACK PLAN

If anything breaks:

```bash
# Rollback commit
git reset --hard HEAD~1

# Or checkout specific files
git checkout HEAD~1 -- path/to/file

# Check reflog for safety
git reflog
```

**Safety**: All moves preserve files, nothing is deleted. Worst case, manually move files back.

---

## 🚀 READY TO EXECUTE

**Next Command**: Proceed to Phase 1 execution?

I'll run each phase step-by-step, verifying as we go.
