# Mini-Agent Project Context

## Origin
**Created by**: MiniMax AI Team  
**Repository**: https://github.com/MiniMax-AI/agent-demo  
**Purpose**: Teaching-level agent demonstration with extensible architecture

## Architecture

### Core Components (by MiniMax - ~90%)
- **Agent Loop**: `mini_agent/agent.py` - Execution loop with tool calling and message management
- **LLM Clients**: `mini_agent/llm/` - Multi-provider support
  - MiniMax-M2 (primary)
  - MiniMax-M2
  - OpenAI GPT
  - Z.AI GLM-4.5/4.6 (community extension)
- **Tools**: `mini_agent/tools/` - Extensible tool framework
  - File operations (read, write, edit)
  - Bash execution (PowerShell on Windows)
  - MCP server integration
  - Skills loader
  - Session notes
- **Skills**: `mini_agent/skills/` - 20+ specialized capabilities
  - Document processing (PDF, DOCX, PPTX, XLSX)
  - Algorithmic art generation
  - Web app testing
  - Internal communications
  - And more...
- **Configuration**: `mini_agent/config/` - YAML-based configuration system
- **Retry Logic**: Exponential backoff for LLM calls
- **Logging**: Structured logging for debugging

### Community Extensions (~10%)
- **Z.AI Integration**: GLM-4.5/4.6 models with web search capabilities
- **ACP Server**: `mini_agent/acp/` - Agent Client Protocol bridge for editor integration
- **VS Code Extension**: `vscode-extension/` - Native Chat API integration
- **Zed Integration**: (Planned) - See `documents/experiments/zed_acp/`
- **Organizational System**: Professional documentation structure

## Project Structure
```
mini_agent/
├── agent.py              # Core agent execution loop (414 lines)
├── cli.py                # Command-line interface
├── config.py             # Configuration loading
├── logger.py             # Structured logging
├── retry.py              # Retry logic with exponential backoff
├── config/               # Configuration files
│   ├── config.yaml       # Main configuration (tracked)
│   ├── config-example.yaml # Template for local configs
│   ├── mcp.json          # MCP server connections
│   └── system_prompt.md  # Agent system prompt
├── llm/                  # LLM client wrappers
│   ├── base.py           # Abstract base class
│   ├── anthropic_client.py
│   ├── openai_client.py
│   ├── glm_client.py     # Z.AI GLM models
│   ├── zai_client.py     # Z.AI web search
│   └── llm_wrapper.py    # Unified interface
├── tools/                # Tool implementations
│   ├── base.py           # Tool abstract base
│   ├── file_tools.py     # Read, write, edit
│   ├── bash_tool.py      # Command execution
│   ├── mcp_loader.py     # MCP server integration
│   ├── skill_tool.py     # Skills system
│   └── zai_tools.py      # Z.AI web search tools
├── skills/               # Specialized skills (git submodule)
│   ├── document-skills/  # PDF, DOCX, PPTX, XLSX
│   ├── algorithmic-art/  # p5.js art generation
│   ├── webapp-testing/   # Playwright testing
│   └── ...               # 20+ more skills
├── acp/                  # Agent Client Protocol server
│   ├── server.py         # Main ACP server
│   └── __main__.py       # Entry point
├── schema/               # Pydantic data models
│   └── schema.py         # Message, ToolCall, etc.
└── utils/                # Utility functions
    └── terminal_utils.py

vscode-extension/         # VS Code integration (active development)
├── extension.js          # VS Code Chat API integration
├── package.json          # Extension manifest
└── ...

tests/                    # Test suite (15 test files)
scripts/                  # Utility scripts
examples/                 # Usage examples
documents/                # ALL project documentation
├── BRUTAL_CODE_AUDIT.md  # Code quality assessment
├── CLEANUP_PLAN.md       # Repository cleanup plan
├── PROJECT_CONTEXT.md    # This file
├── AGENT_HANDOFF.md      # For next agent
├── CONFIGURATION.md      # Config hierarchy
├── experiments/          # Research and WIP
│   └── zed_acp/          # Zed editor integration
├── builds/archive/       # Archived build attempts
├── audits/               # Historical audits
├── research/             # Research outputs
├── production/           # Production configs
└── archive/              # Old backups
```

## Current Status (as of 2025-01-22)

### Stable ✅
- Core agent execution loop
- Multi-LLM support (4 providers)
- File and bash tools
- Skills system (20+ skills)
- CLI interface
- Message history management
- Token counting and summarization
- Retry logic

### Active Development 🔄
- VS Code ACP integration
- Z.AI web search optimization
- Repository cleanup and organization
- Test coverage improvements
- Documentation consolidation

### Planned 📋
- Zed editor integration (see experiments/)
- Agent class refactoring (separate concerns)
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks
- Test coverage reporting
- Performance profiling

### Known Issues ⚠️
- Agent class is a god object (414 lines, multiple responsibilities)
- Test structure is flat (should be unit/integration/e2e)
- Skills as git submodule (adds deployment complexity)

## Key Technologies
- **Language**: Python 3.10+
- **Package Manager**: uv (modern pip replacement)
- **LLM APIs**: Anthropic, MiniMax-M2, GLM-4.6
- **Testing**: pytest with async support
- **Configuration**: YAML + environment variables
- **Protocol**: Agent Client Protocol (ACP) for editor integration
- **Skills Framework**: Progressive disclosure pattern

## Design Patterns

### Progressive Disclosure (Skills)
1. **Level 1**: Metadata (name, description) loaded at startup
2. **Level 2**: Full content loaded on demand via `get_skill()`
3. **Level 3+**: Resources (scripts, templates) accessed as needed

### Multi-Provider LLM
- Abstract base class: `LLMClient`
- Concrete implementations for each provider
- Unified interface via `LLMWrapper`
- Automatic retry with exponential backoff

### Tool Framework
- Abstract base: `Tool`
- Schema generation for Anthropic/OpenAI formats
- Async execution
- Structured results: `ToolResult(success, content, error)`

## Configuration Philosophy

**Hierarchy** (see documents/CONFIGURATION.md):
1. `mini_agent/config/config.yaml` - Default settings
2. `local_config.yaml` - User overrides (git-ignored)
3. `.env` - API keys (git-ignored)
4. Environment variables - Runtime overrides

**Priority**: Later sources override earlier ones

## Development Workflow

### Setup
```bash
# Clone and setup
git clone https://github.com/MiniMax-AI/agent-demo.git
cd agent-demo
uv venv
uv pip install -e .

# Configure
cp mini_agent/config/config-example.yaml local_config.yaml
# Edit local_config.yaml and .env
```

### Testing
```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=mini_agent
```

### Running
```bash
# Interactive mode
uv run mini-agent

# Single command
uv run mini-agent "Analyze the README and summarize it"

# ACP server (for editors)
uv run mini-agent-acp
```

## Contributing

See original MiniMax documentation in `documents/minimax_original/`:
- DEVELOPMENT_GUIDE.md
- PRODUCTION_GUIDE.md

## License
MIT (see LICENSE file)
