# Mini-Agent Setup Guide

## Environment Setup

### Prerequisites
- **Python**: 3.8+ (recommended: 3.11+)
- **Package Manager**: `uv` (recommended) or pip
- **Operating System**: Windows (PowerShell), Linux/macOS (bash)
- **Hardware**: RTX 5070 Ti (configured in current setup)

### Virtual Environment Setup

#### Using `uv` (Recommended)
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv

# Install Mini-Agent in development mode
uv pip install -e .
```

#### Using pip
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -e .
```

## Configuration

### Environment Variables
Create or update `.env` file in the root directory:

```bash
# Z.AI API Configuration
ZAI_API_KEY=your_zai_api_key_here

# Optional: Additional API keys
OPENAI_API_KEY=your_openai_key  # For other LLM providers
```

### Configuration Files

#### Main Configuration (`mini_agent/config/config.yaml`)
```yaml
# Z.AI Integration
zai:
  enabled: true
  base_url: "https://api.z.ai/api/paas/v4"
  default_model: "glm-4.5"
  timeout: 60

# LLM Providers
llm:
  default: "zai"
  providers:
    zai:
      enabled: true
      priority: 1
    openai:
      enabled: false
      priority: 2

# Skills System
skills:
  loading_mode: "progressive"
  cache_enabled: true
  fact_checking: true

# File System Access
filesystem:
  workspace_root: "."
  temp_dir: "./temp"
  max_file_size_mb: 100
```

#### MCP Configuration (`mini_agent/config/mcp.json`)
```json
{
  "mcpServers": {
    "minimax_search": {
      "command": "minimax-search-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

## Dependencies Verification

### Core Dependencies
```bash
# Check all dependencies are properly installed
uv pip list

# Verify critical packages
python -c "import aiohttp; print('aiohttp available')"
python -c "from mini_agent.llm.zai_client import ZAIClient; print('ZAI client available')"
python -c "from mini_agent.tools.zai_tools import ZAIWebSearchTool; print('ZAI tools available')"
```

### Dependencies Status
- **Total Packages**: 92/92 resolved ✅
- **aiohttp**: For async HTTP requests ✅
- **click**: For CLI interface ✅
- **pyyaml**: For configuration ✅
- **websockets**: For ACP server ✅

## Installation Verification

### Basic Test
```bash
# Test CLI startup
mini-agent --help

# Should display help information with Z.AI tools
```

### Z.AI Integration Test
```bash
# Test Z.AI web search (requires valid API key)
export ZAI_API_KEY="your_key_here"
mini-agent

# In the agent session:
> test_zai_web_search
```

### System Components Test
```python
# Run comprehensive system check
python documents/testing/quick_status_check.py
```

## Service Architecture

### Docker Services Status
The system includes 7 Docker services (all healthy):
- **Local LLM**: Port 8002 (Qwen2.5 7B model)
- **Cognee**: Port 8001 (Knowledge management)
- **Voice AI**: Port 8003 (Audio processing)
- **EXAI MCP**: Ports 3000/3010 (MCP server integration)

### Protocol Implementation
- **Enhanced ACP Server**: Full Agent Client Protocol implementation
- **WebSocket Communication**: Real-time agent communication
- **Session Management**: Standardized message formats

## Usage Modes

### 1. Direct CLI (Recommended)
```bash
# Start Mini-Agent CLI
mini-agent

# The agent will:
# - Load all Z.AI tools automatically
# - Provide full file system access
# - Enable skill system progressively
# - Support protocol communication
```

### 2. ACP Server Mode
```bash
# Install and start ACP server
uv pip install -e .
mini-agent-acp

# Configure in editor (Zed, VS Code, etc.)
```

### 3. Development Mode
```bash
# Run from source for development
uv run mini-agent

# Or specific development commands
uv run python mini_agent/cli.py
```

## Troubleshooting

### Common Issues

#### 1. Z.AI API Errors
**Issue**: "API key not found" or authentication errors
**Solution**: 
- Verify `.env` file exists and has `ZAI_API_KEY`
- Check API key validity
- Ensure proper header configuration

#### 2. File Access Restrictions
**Issue**: Cannot access files outside workspace
**Solution**: 
- Use direct CLI mode instead of MCP mode
- Check working directory permissions
- Verify filesystem access configuration

#### 3. Import Errors
**Issue**: Module import failures
**Solution**:
- Ensure virtual environment is activated
- Reinstall with `uv pip install -e .`
- Check Python path configuration

#### 4. Service Connection Issues
**Issue**: Cannot connect to Docker services
**Solution**:
- Verify Docker is running
- Check port availability (8001, 8002, 8003, 3000, 3010)
- Review service configuration

### Debug Commands
```bash
# Check system status
python documents/testing/quick_status_check.py

# Validate Z.AI integration
python documents/testing/test_zai_integration.py

# Test file access
python -c "from mini_agent.tools.base import *; print('File tools available')"

# Check service health
curl http://localhost:8002/health  # Local LLM
curl http://localhost:8001/health  # Cognee
```

## Performance Optimization

### Known Performance Issues
- **Cognee memify()**: Currently ~324s, targeting <60s optimization
- **MCP Stack**: Previously resolved container desynchronization

### Optimization Recommendations
1. **Memory Management**: Monitor virtual memory usage
2. **Service Scaling**: Consider horizontal scaling for high-load scenarios
3. **Cache Configuration**: Enable skill caching for faster load times
4. **Network Optimization**: Ensure proper port allocation and traffic management

## Security Considerations

### File Access
- Default access limited to workspace directory
- No automatic system file access
- Configurable access restrictions per session

### API Key Management
- Environment variables for sensitive data
- `.env` file should be excluded from version control
- Consider key rotation for production use

### Network Security
- HTTPS for all external API communications
- WebSocket encryption for ACP server
- Configurable network access controls

---

## Quick Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] `.env` file configured with Z.AI API key
- [ ] Configuration files present and valid
- [ ] Z.AI tools accessible (test web search)
- [ ] File system access working
- [ ] No import errors when running basic commands
- [ ] Docker services accessible (if applicable)

**Setup Complete**: When all items are checked ✅

---

**Last Updated**: 2025-11-20  
**Current Status**: Production Ready  
**Support**: See `documents/guides/TROUBLESHOOTING.md` for detailed help