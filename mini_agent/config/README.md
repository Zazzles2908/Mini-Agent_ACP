# 🔧 PRODUCTION CONFIGURATION SYSTEM
## Single Source of Truth with Environment-Based Overrides

This is the **PRODUCTION-GRADE** configuration system that replaces the previous scattered approach.

### **Configuration Hierarchy (Priority Order)**
1. **Environment Variables** (Production override)
2. **`.env` file** (Development convenience)  
3. **`config.yaml`** (Application defaults)
4. **Hardcoded defaults** (Fallback safety)

---

## 📋 CONFIGURATION STRUCTURE

### **Core Application Config (`config.yaml`)**
```yaml
# Application defaults (safe for public repo)
app:
  name: "mini-agent"
  version: "1.0.0"
  debug: false
  log_level: "INFO"

# LLM Provider Configuration
llm:
  provider: "minimax"
  model: "MiniMax-M2"
  api_base: "https://api.minimax.io"
  max_tokens: 200000
  temperature: 0.7

# Tool Configuration  
tools:
  enable_zai_web_search: true
  enable_mcp_tools: true
  enable_skills: true
  max_concurrent_tools: 5

# MCP Server Configuration
mcp:
  config_file: "mini_agent/config/.mcp.json"
  timeout: 30
  retry_attempts: 3
  retry_delay: 1.0

# Workspace Configuration
workspace:
  directory: "./workspace"
  auto_cleanup: true
  max_history: 1000
```

### **Environment Variables (Production)**
```bash
# Required for Production
MINIMAX_API_KEY=your_minimax_api_key_here
ZAI_API_KEY=your_zai_api_key_here  # Optional for web search

# Optional Overrides
MINIMAX_API_BASE=https://api.minimax.io
MINIMAX_MODEL=MiniMax-M2
MINIMAX_DEBUG=false
MINIMAX_LOG_LEVEL=INFO
MINIMAX_MAX_TOKENS=200000
MINIMAX_TEMPERATURE=0.7
MINIMAX_WORKSPACE_DIR=./workspace
```

### **Development Environment (`.env`)**
```bash
# Copy from .env.example and fill in your keys
MINIMAX_API_KEY=your_minimax_key_here
ZAI_API_KEY=your_zai_key_here
MINIMAX_DEBUG=true
MINIMAX_LOG_LEVEL=DEBUG
```

---

## 🚀 USAGE

### **Loading Configuration (Production Way)**
```python
from mini_agent.config import Config

# Auto-loads from environment, .env, then config.yaml
config = Config()

# Access values with environment override support
api_key = config.get("MINIMAX_API_KEY", required=True)
provider = config.get("llm.provider", default="minimax")
debug_mode = config.get("app.debug", default=False)
```

### **CLI Usage (Production)**
```bash
# Production deployment
export MINIMAX_API_KEY=your_key_here
export ZAI_API_KEY=your_zai_key_here
export MINIMAX_DEBUG=false
export MINIMAX_LOG_LEVEL=INFO

# Start agent with production settings
mini-agent

# Development mode
export MINIMAX_DEBUG=true
export MINIMAX_LOG_LEVEL=DEBUG
mini-agent
```

---

## 🔒 SECURITY & BEST PRACTICES

### **Never Commit Secrets**
- ✅ `.env.example` with placeholder values
- ✅ `.env` in `.gitignore`  
- ✅ Real values only in environment or secrets management

### **Production Deployment**
```bash
# Docker/Cloud deployment
MINIMAX_API_KEY=${MINIMAX_API_KEY}
ZAI_API_KEY=${ZAI_API_KEY}
MINIMAX_DEBUG=false
MINIMAX_LOG_LEVEL=WARNING

# Kubernetes Secrets
env:
  - name: MINIMAX_API_KEY
    valueFrom:
      secretKeyRef:
        name: mini-agent-secrets
        key: minimax-api-key
```

---

## 🧪 VALIDATION

### **Configuration Validation**
```python
# Automatic validation on load
config = Config()
config.validate_required(["MINIMAX_API_KEY"])
config.validate_types({"MINIMAX_MAX_TOKENS": int})
config.validate_ranges({"MINIMAX_TEMPERATURE": (0.0, 2.0)})
```

### **Health Check**
```bash
# Validate configuration
python -c "from mini_agent.config import Config; Config().health_check()"
```

---

**This replaces**:  
❌ `local_config.yaml.example`  
❌ Multiple scattered config approaches  
❌ API keys in source control  
❌ Unclear precedence  

**Benefits**:  
✅ Single source of truth  
✅ Production-ready security  
✅ Environment-based overrides  
✅ Validation and health checks  
✅ Clear documentation
