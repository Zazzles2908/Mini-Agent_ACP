# Mini-Agent Setup Guide

## 🚀 **Quick Start (5 minutes)**

### **Prerequisites**
- **Python**: 3.8+ (recommended: 3.11+)
- **Package Manager**: `uv` (recommended) or pip
- **Operating System**: Windows (PowerShell), Linux/macOS (bash)
- **Hardware**: 8GB+ RAM recommended
- **Z.AI API Key**: Required for web search/reading capabilities

### **Fast Track Setup**
```bash
# 1. Create and activate virtual environment
uv venv

# 2. Install Mini-Agent in development mode
uv pip install -e .

# 3. Configure Z.AI (create .env file)
echo "ZAI_API_KEY=your_zai_api_key_here" > .env

# 4. Validate installation
python scripts/validation/pre_implementation_check.py

# 5. Start using Mini-Agent
mini-agent
```

---

## 🏗️ **Professional Installation**

### **Step 1: Environment Setup**

#### Using `uv` (Recommended)
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
. .venv/Scripts/Activate.ps1  # Windows
# or
source .venv/bin/activate     # Linux/macOS

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

### **Step 2: Configuration**

#### Environment Variables
Create/update `.env` file in the root directory:

```bash
# Z.AI API Configuration (Required)
ZAI_API_KEY=your_zai_api_key_here

# Optional: Additional LLM providers
OPENAI_API_KEY=your_openai_key  # For fallback LLM
ANTHROPIC_API_KEY=your_key      # For Claude integration

# System Configuration
MINI_AGENT_ENVIRONMENT=development  # or production
DEBUG_MODE=true                    # Enable detailed logging
```

#### Main Configuration (`mini_agent/config/config.yaml`)
```yaml
# Z.AI Integration
zai:
  enabled: true
  base_url: "https://api.z.ai/api/paas/v4"
  default_model: "glm-4.5"        # Tool invocation optimized
  comprehensive_model: "glm-4.6"  # Comprehensive analysis
  timeout: 60
  max_retries: 3

# LLM Providers Configuration
llm:
  default: "zai"
  providers:
    zai:
      enabled: true
      priority: 1
      models: ["glm-4.5", "glm-4.6"]
    openai:
      enabled: false
      priority: 2
    anthropic:
      enabled: false
      priority: 3

# Progressive Skill System
skills:
  loading_mode: "progressive"      # Level 1→2→3 disclosure
  cache_enabled: true
  fact_checking: true              # Enable quality assessment
  auto_load_core: true

# Knowledge Graph Integration
knowledge_graph:
  enabled: true
  persistence: true
  auto_update: true
  entity_tracking: true

# File System Access
filesystem:
  workspace_root: "."
  temp_dir: "./temp"
  max_file_size_mb: 100
  allow_outside_workspace: false

# Organizational System
organization:
  strict_categorization: true      # Enforce 7+6 category system
  validation_required: true        # Pre-implementation checks
  compliance_scoring: true         # 80%+ requirement

# VS Code Extension
vscode_integration:
  enabled: true
  auto_start_acp: true
  chat_participant: "@mini-agent"
```

#### MCP Configuration (`mini_agent/config/mcp.json`)
```json
{
  "mcpServers": {
    "minimax-search": {
      "command": "minimax-search-mcp",
      "args": [],
      "env": {}
    },
    "mini-agent-acp": {
      "command": "python",
      "args": ["-m", "mini_agent.acp"],
      "env": {}
    }
  }
}
```

### **Step 3: Service Architecture**

#### Docker Services Status (Optional)
The system includes 7 Docker services for enhanced capabilities:

```bash
# All services should be healthy:
Local LLM (Port 8002):     Qwen2.5 7B model     ✅ Healthy
Cognee (Port 8001):        Knowledge management ✅ Healthy  
Voice AI (Port 8003):      Audio processing    ✅ Healthy
EXAI MCP (Ports 3000/3010): MCP server integration ✅ Healthy
```

#### Service Health Check
```bash
# Check service status
curl http://localhost:8002/health  # Local LLM
curl http://localhost:8001/health  # Cognee
curl http://localhost:8003/health  # Voice AI

# If services are down, restart Docker:
docker-compose up -d
```

---

## 🔧 **Advanced Configuration**

### **Z.AI Integration Setup**

#### API Configuration
```yaml
# Enhanced Z.AI configuration
zai:
  endpoints:
    web_search: "https://api.z.ai/api/paas/v4/web_search"
    web_reader: "https://api.z.ai/api/paas/v4/reader"
    chat: "https://api.z.ai/api/paas/v4/chat-completions"
  
  models:
    glm_4_5: "glm-4.5"      # Optimized for tool calls
    glm_4_6: "glm-4.6"      # Comprehensive analysis
  
  features:
    streaming: true          # Real-time responses
    fact_checking: true      # Quality validation
    knowledge_graph: true    # Context persistence
```

#### Z.AI Integration Test
```bash
# Test Z.AI connectivity (requires valid API key)
export ZAI_API_KEY="your_key_here"
mini-agent

# In the agent session:
> test_zai_web_search
> test_zai_web_reader
> status_report
```

### **Organizational System Configuration**

#### Validation Tools Setup
```bash
# Pre-implementation validation
python scripts/validation/pre_implementation_check.py

# Architecture compliance
python scripts/validation/validate_architectural_compliance.py

# Organizational assessment
python scripts/assessment/organization_validator.py
```

#### Knowledge Graph Integration
```python
# Test knowledge graph functionality
from mini_agent.knowledge import create_entities, search_nodes

# Test entity creation
create_entities([{
    "name": "Test Entity",
    "entityType": "test_type", 
    "observations": ["Test observation"]
}])

# Test entity search
search_nodes("Mini-Agent Codebase Organization System")
```

---

## 📊 **Installation Verification**

### **Core System Check**
```bash
# 1. Basic CLI test
mini-agent --help

# Should display help with Z.AI tools and organizational features

# 2. Pre-implementation validation
python scripts/validation/pre_implementation_check.py

# Expected output: 80%+ compliance score

# 3. Knowledge graph test
python -c "from mini_agent.knowledge import read_graph; print('Knowledge graph operational')"

# 4. Progressive skill system test
python -c "from mini_agent.skills import list_skills; print(f'Available skills: {len(list_skills())}')"
```

### **Integration Tests**
```bash
# Z.AI integration test
python -c "
from mini_agent.llm.zai_client import ZAIClient
client = ZAIClient()
print('Z.AI client available')
"

# Tool system test  
python -c "
from mini_agent.tools.base import list_tools
print(f'Tools available: {list_tools()}')
"

# VS Code extension test
python -c "
from mini_agent.skills.vscode_integration import VSCodeIntegrationSkill
skill = VSCodeIntegrationSkill()
print('VS Code integration ready')
"
```

### **System Components Verification**
- **Total Packages**: 92/92 resolved ✅
- **Z.AI Client**: Direct REST API integration ✅
- **Knowledge Graph**: Entities and relations operational ✅
- **Progressive Skills**: 15+ skills with 3-level loading ✅
- **Organizational System**: 7+6 category structure ✅
- **Validation Tools**: Pre-implementation, compliance, organization ✅

---

## 🚀 **Usage Modes**

### **1. Interactive CLI (Recommended)**
```bash
# Start Mini-Agent with full capabilities
mini-agent

# Features loaded:
# ✅ Progressive skill loading (Level 1→2→3)
# ✅ Z.AI web search and reading
# ✅ Knowledge graph integration
# ✅ Fact-checking framework
# ✅ Organizational validation
# ✅ Professional workflow support
```

### **2. VS Code Chat Integration**
```json
{
  "agent_servers": {
    "mini-agent": {
      "command": "mini-agent-acp"
    }
  }
}
```

**Chat Commands**:
- `@mini-agent explain this code` - Code explanation with context
- `@mini-agent generate test` - Test generation using skill system
- `@mini-agent use fact-checking` - Quality assessment
- `@mini-agent search web for pattern` - Web search integration

### **3. ACP Server Mode**
```bash
# Start as standalone ACP server
mini-agent-acp

# Configure in Zed, VS Code, or other ACP-compatible editors
```

### **4. Development Mode**
```bash
# Run from source for development
uv run mini-agent

# Or with specific development commands
uv run python mini_agent/cli.py --debug
uv run python -m mini_agent.acp --test
```

---

## 🛠️ **Agent Development Setup**

### **For Agents Working on Mini-Agent**
```bash
# 1. Organizational knowledge discovery (MANDATORY)
search_nodes("Mini-Agent Codebase Organization System")
search_nodes("Universal Workflow Protocol")
read_graph()

# 2. Pre-implementation validation (REQUIRED)
python scripts/validation/pre_implementation_check.py

# 3. Load fact-checking skill (QUALITY ASSURANCE)
get_skill("fact-checking-self-assessment")

# 4. Review best practices (RECOMMENDED)
read_file("documents/workflows/AGENT_BEST_PRACTICES.md")
```

### **Development Workflow**
1. **Phase 1**: Pre-Implementation (organizational validation)
2. **Phase 2**: Planning & Design (architecture pattern selection)
3. **Phase 3**: Implementation (progressive development)
4. **Phase 4**: Testing & Validation (fact-checking + compliance)
5. **Phase 5**: Completion & Handoff (documentation + knowledge graph)

### **Quality Standards for Development**
- **80%+ Compliance Score**: Required before task completion
- **Fact-Checking Validation**: Mandatory at implementation milestones
- **Organizational Compliance**: Files must be in correct 7+6 categories
- **Knowledge Graph Updates**: Context persistence required throughout

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### 1. Organizational Validation Failures
**Issue**: Pre-implementation check fails with low compliance score
**Solution**:
```bash
# Fix workspace pollution
python scripts/assessment/organization_validator.py
python scripts/validation/validate_architectural_compliance.py

# Recreate missing directories
python -c "
import os
os.makedirs('documents/architecture', exist_ok=True)
os.makedirs('documents/workflows', exist_ok=True)
os.makedirs('scripts/validation', exist_ok=True)
"
```

#### 2. Knowledge Graph Issues
**Issue**: Entity creation or search fails
**Solution**:
```bash
# Reset knowledge graph
python -c "from mini_agent.knowledge import reset_graph; reset_graph()"

# Test knowledge graph functionality
python scripts/testing/test_knowledge_graph.py
```

#### 3. Z.AI Integration Problems
**Issue**: API errors or authentication failures
**Solution**:
- Verify `.env` file exists with valid `ZAI_API_KEY`
- Check API key permissions and quota
- Test with: `python scripts/testing/test_zai_integration.py`

#### 4. Import Errors
**Issue**: Module import failures
**Solution**:
```bash
# Ensure virtual environment is activated
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/macOS

# Reinstall in development mode
uv pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 5. Service Connection Issues
**Issue**: Cannot connect to Docker services
**Solution**:
```bash
# Check Docker status
docker ps

# Restart services
docker-compose up -d

# Check port availability
netstat -an | grep 800
```

### **Debug Commands**
```bash
# Complete system validation
python scripts/validation/pre_implementation_check.py

# Z.AI integration test
python scripts/testing/test_zai_integration.py

# Knowledge graph status
python scripts/assessment/knowledge_graph_status.py

# Organizational compliance
python scripts/assessment/organization_validator.py

# Service health check
curl http://localhost:8002/health  # Local LLM
curl http://localhost:8001/health  # Cognee
curl http://localhost:8003/health  # Voice AI
```

---

## 📈 **Performance Optimization**

### **Known Performance Areas**
- **Cognee memify()**: Currently ~324s, targeting <60s optimization
- **Knowledge Graph**: Optimized for agent context persistence
- **Progressive Skills**: Cached loading for faster access
- **Z.AI Integration**: Direct API with proper timeout handling

### **Optimization Recommendations**
1. **Memory Management**: Monitor virtual memory usage during large operations
2. **Service Scaling**: Consider horizontal scaling for high-load scenarios  
3. **Cache Configuration**: Enable skill caching in configuration
4. **Network Optimization**: Ensure proper port allocation and traffic management

### **Monitoring Commands**
```bash
# System resource usage
htop  # Linux/macOS
Get-Process | Sort-Object CPU -Descending  # Windows

# Memory usage check
python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}% used')
print(f'Disk: {psutil.disk_usage(\'.\').percent}% used')
"

# Service resource monitoring
docker stats
```

---

## 🔒 **Security Considerations**

### **File Access Security**
- Default access limited to workspace directory
- No automatic system file access
- Configurable access restrictions per session
- Organizational validation prevents unauthorized file placement

### **API Key Management**
- Environment variables for sensitive data
- `.env` file excluded from version control
- Consider key rotation for production use
- Encrypted storage for long-term keys

### **Network Security**
- HTTPS for all external API communications
- WebSocket encryption for ACP server
- Configurable network access controls
- Organizational system prevents security violations

---

## ✅ **Setup Verification Checklist**

### **Installation Complete** ✅
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully (92/92)
- [ ] `.env` file configured with Z.AI API key
- [ ] Configuration files present and valid
- [ ] Z.AI tools accessible (test web search)
- [ ] Knowledge graph operational
- [ ] Organizational system validated (7+6 categories)
- [ ] Pre-implementation check passes (80%+ score)
- [ ] Progressive skill system functional
- [ ] Fact-checking framework active
- [ ] No import errors when running basic commands
- [ ] Docker services accessible (if applicable)

### **Agent Development Ready** ✅
- [ ] Organizational knowledge queryable (`search_nodes`)
- [ ] Knowledge graph accessible (`read_graph()`)
- [ ] Best practices documentation reviewed
- [ ] Universal workflow protocol understood
- [ ] Quality standards (80%+ compliance) achievable

---

**🎉 Setup Complete**: When all checklist items are verified ✅

**📚 Next Steps**:
1. Review [Agent Best Practices](documents/workflows/AGENT_BEST_PRACTICES.md)
2. Explore [Universal Workflow Protocol](documents/workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md)  
3. Understand [System Architecture](documents/architecture/MINI_AGENT_ARCHITECTURAL_MASTERY.md)

---

**Last Updated**: 2025-11-20  
**System Version**: 0.1.0  
**Current Status**: Production Ready with Professional Organizational Intelligence  
**Support**: See [Troubleshooting Guide](documents/troubleshooting/TROUBLESHOOTING.md) for detailed help