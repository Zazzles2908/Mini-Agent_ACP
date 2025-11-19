# 🎯 Mini-Agent - Clean & Working Setup

## ✅ WORKING METHOD (Use This)

```bash
# ONLY use this method - all others are deprecated
python launch_mini_agent.py --workspace .
```

## ❌ DEPRECATED METHODS (Don't Use)

- ~~`run-mini-agent.bat`~~ - Causes import failures
- ~~`start-mini-agent.bat`~~ - Causes import failures  
- ~~`python -m mini_agent.cli`~~ - Relative import errors
- ~~Any .bat files~~ - All deprecated

## 🔧 What Was Fixed

### 1. **.bat Files Neutralized**
- All .bat files now show deprecation warnings
- They no longer cause import failures
- Use `launch_mini_agent.py` instead

### 2. **MCP Configuration Cleaned**
- Removed deprecated `minimax_search` server
- Kept only essential MCP servers (memory, git, filesystem)
- No longer conflicting with Z.AI web search

### 3. **Project Structure**
- `.observability/` contains failed attempts - use with caution
- `build/` contains package build artifacts
- Focus on root-level files for current work

## 🚀 Current Status

### Working Features:
- ✅ File operations (read, write, edit)
- ✅ Knowledge graph memory
- ✅ Z.AI web search (native)
- ✅ Bash commands  
- ✅ Skills system
- ✅ Git operations

### Environment:
- ✅ Z.AI API key loaded (`.env`)
- ✅ Virtual environment ready (`.venv`)
- ✅ All dependencies installed

## 🎯 Quick Start

```bash
cd C:\Users\Jazeel-Home\Mini-Agent
python launch_mini_agent.py --workspace .
```

This will start Mini-Agent with all 39+ tools available and Z.AI integration working properly.

## 📁 Project Structure (Cleaned)

```
Mini-Agent/
├── launch_mini_agent.py          # ⭐ MAIN LAUNCHER
├── .env                          # Environment variables
├── .venv/                        # Virtual environment
├── mini_agent/                   # Core package
├── documents/                    # Documentation
├── tests/                        # Test suite
├── scripts/                      # Utility scripts
└── [other files]
```

## 🔍 What's Inside

### Core Agent Features:
- **39+ Tools**: File, bash, web search, MCP, skills
- **Z.AI Integration**: Native GLM models (4.5, 4.6, 4-air)
- **Web Search**: Z.AI Search Prime engine
- **Memory**: Knowledge graph with long-term storage
- **Skills**: 10+ specialized skills (docx, pdf, pptx, etc.)

### Configuration:
- **`.env`**: API keys and environment variables
- **`mini_agent/config/`**: Core configuration files
- **`pyproject.toml`**: Project dependencies

---

**Status**: ✅ Clean, working, and simplified setup
