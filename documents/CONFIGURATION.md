# Configuration Guide

## Configuration Hierarchy

Mini-Agent uses a layered configuration system where later sources override earlier ones.

### 1. Main Configuration (Base Layer)
**File**: `mini_agent/config/config.yaml`
- Tracked in git
- Default settings for all users
- Includes:
  - Default LLM provider
  - Model names
  - Workspace paths
  - Tool settings
  - Logging configuration

**⚠️ Edit with caution** - Changes affect all installations

### 2. Local Overrides (User Layer)
**File**: `local_config.yaml` (root directory)
- **Git-ignored** (not tracked)
- User-specific settings
- Only override specific values you want to change
- Copy from example: `cp mini_agent/config/config-example.yaml local_config.yaml`

**Example**:
```yaml
# local_config.yaml - only override what you need
default_provider: "anthropic"  # Override default provider
workspace_dir: "~/my-workspace"  # Custom workspace
max_steps: 100  # Increase max steps
```

### 3. Environment Variables (Runtime Layer)
**File**: `.env` (root directory)
- **Git-ignored** (NEVER commit!)
- API keys and secrets
- Loaded automatically at runtime
- Highest priority for sensitive values

**Required**:
```bash
# .env
MINIMAX_API_KEY=your_minimax_key_here
ZAI_API_KEY=your_zai_key_here          # Optional: for web search
OPENAI_API_KEY=your_openai_key_here    # Optional: for GPT models
ANTHROPIC_API_KEY=your_anthropic_key   # Optional: for Claude
```

### 4. MCP Server Configuration
**File**: `mini_agent/config/mcp.json`
- MCP (Model Context Protocol) server connections
- Defines external tool integrations
- JSON format

**Example**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"],
      "disabled": true
    }
  }
}
```

**Note**: Most MCP servers are now disabled in favor of native tools.

## Priority Order

When agent starts, configuration is loaded in this order:

```
1. mini_agent/config/config.yaml    (base)
      ↓ (override)
2. local_config.yaml                (user overrides)
      ↓ (override)
3. .env                             (environment variables)
      ↓ (override)
4. Command-line arguments           (runtime overrides)
```

Later sources override earlier ones for the same key.

## Setup Instructions

### First-Time Setup

```bash
# 1. Create local config from example
cp mini_agent/config/config-example.yaml local_config.yaml

# 2. Create .env file
cat > .env << 'EOF'
MINIMAX_API_KEY=your_minimax_key_here
ZAI_API_KEY=your_zai_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF

# 3. Edit local_config.yaml with your preferences
# (e.g., default model, workspace path, etc.)
```

### Verify Configuration

```bash
# Check that API keys are loaded
uv run python -c "import os; print('MINIMAX_API_KEY' in os.environ)"

# Run agent in dry-run mode (if available)
uv run mini-agent --help
```

## Common Configuration Options

### LLM Provider Selection

**In config.yaml or local_config.yaml**:
```yaml
# Use MiniMax M2 (default, best for most tasks)
default_provider: "minimax"
default_model: "MiniMax-Text-01"

# Use Anthropic Claude (high quality, extended thinking)
default_provider: "anthropic"
default_model: "claude-sonnet-4-20250514"

# Use OpenAI GPT (widely compatible)
default_provider: "openai"
default_model: "gpt-4o"

# Use Z.AI GLM (web search, Coding Plan quota)
default_provider: "glm"
default_model: "glm-4.5"  # or glm-4.6 for higher quality
```

### Workspace Configuration

```yaml
workspace_dir: "./workspace"  # Default: ./workspace
max_steps: 50                 # Maximum agent steps per task
token_limit: 80000            # Token limit before summarization
```

### Logging

```yaml
logging:
  level: "INFO"              # DEBUG, INFO, WARNING, ERROR
  file: "logs/agent.log"     # Log file path
  console: true              # Print to console
```

### Tool Configuration

```yaml
tools:
  bash:
    timeout: 120             # Seconds
    background_timeout: 600  # For long-running commands
  file:
    max_file_size: 10485760  # 10MB
```

## Provider-Specific Notes

### MiniMax M2
- **Best for**: General tasks, Chinese language, cost-effective
- **API Key**: Get from https://platform.minimax.io
- **Models**: MiniMax-Text-01

### Anthropic Claude
- **Best for**: Complex reasoning, extended thinking
- **API Key**: Get from https://console.anthropic.com
- **Models**: claude-sonnet-4-20250514, claude-opus-4-20250514

### OpenAI GPT
- **Best for**: Wide compatibility, function calling
- **API Key**: Get from https://platform.openai.com
- **Models**: gpt-4o, gpt-4-turbo

### Z.AI GLM
- **Best for**: Web search, Coding Plan (120 prompts/5hrs)
- **API Key**: Get from Z.AI platform
- **Models**: glm-4.6 (best quality), glm-4.5 (efficient), glm-4.5-air (lightweight)
- **Features**: Built-in web search and web reader

## Troubleshooting

### "API key not found"
1. Check `.env` file exists in project root
2. Verify key name matches exactly (case-sensitive)
3. No spaces around `=` in `.env`
4. Restart terminal after creating `.env`

### "Configuration file not found"
1. Check file path in error message
2. Create `local_config.yaml` from example
3. Ensure file is in project root (not mini_agent/ subdirectory)

### "Invalid configuration"
1. Check YAML syntax (indentation must be spaces, not tabs)
2. Validate YAML: `python -c "import yaml; yaml.safe_load(open('local_config.yaml'))"`
3. Check for typos in key names

### Config Not Taking Effect
1. Check priority order - env vars override config files
2. Verify file name is exactly `local_config.yaml`
3. Check that values are not being overridden by command-line args

## Security Best Practices

### ✅ DO
- Keep `.env` and `local_config.yaml` in `.gitignore`
- Use environment variables for all secrets
- Rotate API keys regularly
- Use separate keys for development and production

### ❌ DON'T
- Commit `.env` to version control
- Hardcode API keys in source code
- Share your personal `local_config.yaml`
- Use production keys in development

## Example Configurations

### Development Setup
```yaml
# local_config.yaml
default_provider: "minimax"
workspace_dir: "./workspace"
max_steps: 30
logging:
  level: "DEBUG"
  console: true
```

### Production Setup
```yaml
# local_config.yaml
default_provider: "anthropic"
default_model: "claude-sonnet-4-20250514"
workspace_dir: "/var/mini-agent/workspace"
max_steps: 100
token_limit: 100000
logging:
  level: "INFO"
  file: "/var/log/mini-agent.log"
  console: false
```

### Web Search Focused
```yaml
# local_config.yaml
default_provider: "glm"
default_model: "glm-4.5"  # Efficient for quota management
tools:
  web_search:
    enabled: true
    max_results: 5
```

## Migration Guide

### From requirements.txt to pyproject.toml
Mini-Agent now uses `pyproject.toml` and `uv` for dependency management. If you have old `requirements.txt`:

```bash
# Requirements are now in pyproject.toml
# To regenerate requirements.txt (if needed):
uv pip compile pyproject.toml > requirements.txt
```

### From Old Config Format
If you have an old `config.yaml` in the root:

```bash
# Backup old config
cp config.yaml config.yaml.old

# Use new structure
cp mini_agent/config/config-example.yaml local_config.yaml
# Manually migrate your settings
```

## See Also
- `PROJECT_CONTEXT.md` - Project overview and architecture
- `AGENT_HANDOFF.md` - Current status and next steps
- `mini_agent/config/config-example.yaml` - Full configuration template
- `mini_agent/config/system_prompt.md` - Agent system prompt
