# 🤖 Mini-Agent by MiniMax

**Created by**: [MiniMax AI Team](https://github.com/MiniMax-AI/agent-demo)  
**System**: Teaching-level agent demonstration with community extensions  
**Primary LLM**: MiniMax-M2 (OpenAI-compatible API)  
**Original Docs**: [docs/](docs/) directory contains official MiniMax documentation

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](README.md)
[![MiniMax](https://img.shields.io/badge/created--by-MiniMax-red.svg)](https://github.com/MiniMax-AI)
[![Status](https://img.shields.io/badge/status-extended--system-green.svg)](documents/project/)

---

## 📖 **What is Mini-Agent?**

**Mini-Agent is a teaching-level agent demo created by MiniMax AI Team** that demonstrates core agent concepts including tool calling, LLM integration, and extensible architecture.

### 🎯 **System Components**

**From MiniMax (Core - 90%)**:
- ✅ Agent execution loop with tool calling
- ✅ Multi-provider: "openai"  # OpenAI SDK format)
- ✅ Tool framework (File, Bash, MCP integration)
- ✅ MiniMax-M2 Skills integration (20+ professional capabilities)
- ✅ Configuration system and retry mechanism
- ✅ Interactive CLI interface

**Community Extensions (10%)**:
- 🆕 Z.AI Integration - Web search using GLM-4.6 (FREE with Lite plan: 100 searches + 100 readers)
- 🆕 ACP Server - Protocol bridge for VS Code/Zed integration
- 🆕 Organizational System - Professional documentation structure
- 🆕 Fact-Checking Framework - Quality assurance tools
- 🆕 VS Code Extension - Native Chat API support

---

## 🚀 **Quick Start**

### **Fast Track Setup (5 minutes)**
```bash
# 1. Clone repository
git clone https://github.com/MiniMax-AI/agent-demo.git
cd agent-demo

# 2. Setup environment
uv venv && uv pip install -e .

# 3. Configure (get keys from https://platform.minimax.io)
echo "MINIMAX_API_KEY=your_minimax_key" > .env
echo "ZAI_API_KEY=your_zai_key" >> .env  # Web search: GLM-4.6 (FREE on Lite plan)

# 4. Initialize MiniMax-M2 Skills (recommended)
git submodule update --init --recursive

# 5. Start using
mini-agent
```

### **Configuration**
```yaml
# mini_agent/config/config.yaml
api_key: "${MINIMAX_API_KEY}"  # Required: MiniMax API key
api_base: "https://api.minimax.io"  # Global platform
model: "MiniMax-M2"  # Primary model
provider: "openai"  # OpenAI SDK format"  # Protocol format (OpenAI-compatible for MiniMax)

# Optional: Z.AI for web search
tools:
  enable_zai_search: true  # Requires ZAI_API_KEY
```

---

## 📚 **Documentation**

### **Official MiniMax Documentation**
- **[Development Guide](docs/DEVELOPMENT_GUIDE.md)** - Official development documentation
- **[Production Guide](docs/PRODUCTION_GUIDE.md)** - Deployment and scaling guide

### **Community Extensions Documentation**
- **[Setup Guide](documents/setup/SETUP_GUIDE.md)** - Enhanced installation guide
- **[Project Context](documents/project/PROJECT_CONTEXT.md)** - System overview and extensions
- **[Architecture Guide](documents/architecture/)** - Technical deep-dives
- **[Workflow Protocols](documents/workflows/)** - Development best practices

---

## 🏗️ **Architecture Overview**

### **MiniMax Core System**
```
mini_agent/
├── agent.py              # Core agent loop (MiniMax)
├── cli.py                # Interactive CLI (MiniMax)
├── config.py             # Configuration loader (MiniMax)
├── llm/
│   ├── anthropic_client.py  # Anthropic protocol (MiniMax)
│   ├── openai_client.py     # OpenAI protocol (MiniMax)
│   ├── llm_wrapper.py       # Multi-provider wrapper (MiniMax)
│   └── zai_client.py        # Z.AI integration (Community)
├── tools/
│   ├── base.py              # Tool framework (MiniMax)
│   ├── file_tools.py        # File operations (MiniMax)
│   ├── bash_tool.py         # Bash execution (MiniMax)
│   ├── mcp_loader.py        # MCP integration (MiniMax)
│   ├── skill_tool.py        # Skills system (MiniMax)
│   └── zai_tools.py         # Z.AI tools (Community)
└── acp/                     # ACP server (Community)
```

### **LLM Provider Hierarchy**
1. **MiniMax-M2** (Primary) - Core reasoning and execution
2. **Z.AI GLM-4.6** (Additional) - Web search and reading (FREE on Lite plan: 100 searches + 100 readers)
3. **Anthropic/OpenAI** (Fallback) - Alternative providers

---

## 🎯 **Core Features (MiniMax)**

### **Agent Loop**
- Async execution with configurable max_steps
- Tool calling with result processing
- Context management and token estimation
- Retry mechanism with exponential backoff

### **Tool System**
- **File Operations**: Read, Write, Edit files
- **Bash Execution**: Command execution with output capture
- **MCP Integration**: Memory (knowledge graph), Git, Web Search
- **Skills**: 20+ professional capabilities from MiniMax-M2 Skills

### **Multi-Provider LLM Support**
```python
# Supports multiple providers with same interface
providers = [
    "MiniMax-M2",     # Default - Primary reasoning model
    "minimax-opus-4",  # MiniMax-M2 (same model)
    "glm-4.6 (via Z.AI)"          # Z.AI GLM-4.6 for web search (FREE on Lite plan)
]
```

---

## 🆕 **Community Extensions**

### **Z.AI Integration**
**Purpose**: Add web search capabilities using GLM-4.6 (FREE on Lite plan)

```python
# Configuration
tools:
  enable_zai_search: true  # Enable Z.AI tools (uses FREE Lite plan quota)
  
# Available tools
- zai_web_search: Search the web using GLM-4.6 (100 searches on Lite plan)
- zai_web_reader: Extract and read web content using GLM-4.6 (100 readers on Lite plan)
```

### **ACP (Agent Client Protocol) Server**
**Purpose**: Connect Mini-Agent to external editors (VS Code, Zed)

```bash
# Run as ACP server
mini-agent-acp

# Configure in VS Code/Zed
{
  "agent_servers": {
    "mini-agent": {
      "command": "mini-agent-acp"
    }
  }
}
```

### **Organizational System**
**Purpose**: Professional workspace management for agents

- **7-Category Documentation**: architecture, workflows, project, setup, examples, testing, troubleshooting
- **6-Category Scripts**: validation, cleanup, assessment, deployment, testing, utilities
- **Knowledge Graph Integration**: Organizational wisdom persisted across sessions

---

## 🚀 **Usage Modes**

### **1. Interactive CLI (Original MiniMax Mode)**
```bash
# Start interactive session
mini-agent

# Available commands:
# /help - Show available commands
# /clear - Clear message history
# /stats - Show session statistics
# /exit - Exit agent
```

### **2. VS Code Integration (Community Extension)**
```bash
# Start ACP server
mini-agent-acp

# Access in VS Code:
# @mini-agent explain this code
# @mini-agent generate tests
# @mini-agent search web for [query]
```

---

## 🛠️ **Development**

### **Adding Custom Tools (MiniMax Framework)**
```python
# Follow MiniMax tool framework
from mini_agent.tools.base import Tool, ToolResult

class MyTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    async def execute(self, **kwargs) -> ToolResult:
        # Tool implementation
        return ToolResult(success=True, content="Result")
```

### **Adding MCP Servers (MiniMax Integration)**
```json
// Edit mcp.json
{
  "mcpServers": {
    "my_server": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": {"API_KEY": "your-key"}
    }
  }
}
```

### **For Agent Development (Community Protocols)**
```bash
# Follow 5-phase workflow
1. Pre-Implementation: Validation and compliance checks
2. Planning & Design: Architecture pattern selection
3. Implementation: Progressive development
4. Testing & Validation: Fact-checking and quality
5. Completion & Handoff: Documentation and cleanup

# Quality standards
- 80%+ compliance score required
- Knowledge graph updates throughout
- Fact-checking at milestones
```

---

## 📊 **System Status**

### **MiniMax Core**
- ✅ Agent loop operational
- ✅ Tool calling functional
- ✅ MCP integration working
- ✅ Skills system active (20+ skills)
- ✅ Multi-provider LLM support

### **Community Extensions**
- ✅ Z.AI integration complete
- 🔄 ACP server (stdio-based) functional
- ✅ Organizational system established
- ✅ Fact-checking framework active
- 🔄 VS Code extension in development

---

## 🔧 **System Requirements**

- **Python**: 3.10+ (required by MiniMax)
- **Package Manager**: `uv` (recommended) or pip
- **Node.js**: Required for MCP tools
- **API Keys**:
  - **MiniMax API Key**: Required (get from [platform.minimax.io](https://platform.minimax.io))
  - **Z.AI API Key**: Optional (for web search)

---

## 🚨 **Important Notes**

### **Attribution**
- **Mini-Agent core is created by MiniMax AI Team**
- Original repository: https://github.com/MiniMax-AI/Mini-Agent
- Official docs in `docs/` directory are authoritative
- Community extensions are additional, not replacements

### **LLM Providers**
- **PRIMARY**: MiniMax-M2 (default, created by MiniMax)
- **ADDITIONAL**: Z.AI GLM-4.5/4.6 (web search extension)
- **FALLBACK**: MiniMax-M2, OpenAI GPT (optional)

### **System Purpose**
- **Original**: Teaching-level agent demonstration (MiniMax)
- **Extended**: Production-capable system with additional tools (Community)
- **Design**: Build on MiniMax foundation, not replace it

---

## 📞 **Support & Resources**

### **MiniMax Resources**
- **Official Repo**: https://github.com/MiniMax-AI/agent-demo
- **Platform**: https://platform.minimax.io (Global) or https://platform.minimaxi.com (China)
- **Development Guide**: [docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)
- **Production Guide**: [docs/PRODUCTION_GUIDE.md](docs/PRODUCTION_GUIDE.md)

### **Community Resources**
- **Extended Documentation**: [documents/](documents/) directory
- **Troubleshooting**: [documents/troubleshooting/](documents/troubleshooting/)
- **Architecture Deep-Dives**: [documents/architecture/](documents/architecture/)
- **Workflow Protocols**: [documents/workflows/](documents/workflows/)

---

## 🏆 **Acknowledgments**

### **Created By**
**MiniMax AI Team** - Original system design, core implementation, and foundational architecture.

### **Extended By**
Community contributors - Z.AI integration, ACP server, organizational tools, and enhanced documentation.

### **Built On**
- **MiniMax-M2 Skills**: Professional capabilities from Anthropic
- **MCP Protocol**: Model Context Protocol standards
- **Agent Client Protocol**: Editor integration protocol

---

## 📄 **License**

MIT License - See LICENSE file

**Note**: This is an extended version of MiniMax's original Mini-Agent demo. The core system (90%) is created by MiniMax AI Team. Community extensions (10%) add additional capabilities while honoring the original design.

---

**🎯 Ready to Start?**
1. **New Users**: See [Setup Guide](documents/setup/SETUP_GUIDE.md)
2. **Developers**: See [Development Guide](docs/DEVELOPMENT_GUIDE.md)
3. **Agents**: See [Agent Best Practices](documents/workflows/AGENT_BEST_PRACTICES.md)

---

**Last Updated**: 2025-11-20  
**Mini-Agent Core**: v0.1.0 by MiniMax AI Team  
**Community Extensions**: Active development  
**Status**: Extended teaching-level system with production enhancements