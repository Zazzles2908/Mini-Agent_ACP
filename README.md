# Mini-Agent: AI Agent Platform

## Overview

Mini-Agent is a sophisticated, enterprise-grade AI agent platform powered by MiniMax. It features a modular architecture with advanced memory systems, skills-based capabilities, and comprehensive tool integration through MCP (Model Context Protocol).

## Key Features

### 🧠 **Advanced Memory System**
- **Base Memory Engine**: AI-like memory with natural growth and decay
- **Organic Memory**: Tree-like memory structure that grows stronger with use
- **Intelligent Categorization**: Automatic memory classification (identity, project, knowledge, session)
- **Connection Building**: Memories automatically connect to related concepts

### 🔧 **Modular Architecture**
- **ComponentManager**: Coordinates all specialized components
- **ContextManager**: Advanced token management (200K token limits)
- **ValidationManager**: Enterprise input/output validation and security
- **ExecutionEngine**: Sophisticated LLM integration with tool execution
- **TaskManager**: Complex task orchestration and session management
- **MonitoringSystem**: Comprehensive health monitoring and alerting

### 🎯 **Skills System**
- **Progressive Disclosure**: Load skills on-demand with metadata-first approach
- **16+ Specialized Skills**: Document processing, algorithmic art, memory management, and more
- **Dynamic Loading**: Skills load based on context and requirements
- **Context-Aware**: Skills understand project context and requirements

### 🔗 **MCP Integration**
- **Full Protocol Support**: Complete Model Context Protocol implementation
- **Multiple Server Types**: Local stdio, HTTP, SSE, streamable-http
- **Connection Management**: Async context management with cleanup
- **Tool Validation**: Schema validation and error handling

### 🛡️ **Enterprise Features**
- **Security**: Input sanitization, forbidden pattern detection
- **Monitoring**: Real-time health checks, performance metrics, alerting
- **Error Recovery**: Comprehensive error handling and graceful degradation
- **Resource Management**: Connection pooling, cleanup protocols

### 🚀 **ACP Integration (Enterprise Protocol)**
- **Full ACP Support**: Complete Agent Context Protocol implementation
- **Dual Agent Types**: ACPAgent (advanced) and ModularAgent (basic) 
- **Protocol Compliance**: Standards-based communication and validation
- **Enterprise Session Management**: Workspace isolation and context persistence
- **Advanced Monitoring**: Component health monitoring and performance metrics
- **Flexible Configuration**: Easy switching between agent types via config.yaml
- **Zero Breaking Changes**: Backward compatible with existing code

## Architecture

The system is built on a sophisticated modular architecture:

```
mini_agent/
├── core/                  # Core system components
│   ├── agent.py          # Modular Agent implementation
│   ├── component_manager.py
│   ├── context_manager.py
│   ├── execution_engine.py
│   ├── task_manager.py
│   ├── validation_manager.py
│   ├── monitoring.py
│   └── acp_*.py          # ACP Protocol components
├── config/               # Configuration files
├── skills/               # Skills system
├── tools/                # Tool loaders and implementations
├── llm/                  # LLM client implementations
├── mcp_servers/          # MCP server implementations
└── utils/                # Utility functions
```

## Configuration

### Main Configuration
- `mini_agent/config/config.yaml` - Main agent configuration
- `mini_agent/config/.mcp.json` - MCP server configuration
- `mini_agent/config/system_prompt.md` - System behavior prompts

### ACP Integration Configuration
The system supports both advanced (ACPAgent) and basic (ModularAgent) agent types. See **[ACP_INTEGRATION_GUIDE.md](ACP_INTEGRATION_GUIDE.md)** for detailed configuration options and migration guide.

**Quick Start with ACPAgent (Recommended):**
```yaml
# config.yaml
agent:
  type: "acp"  # Default - enables enterprise features
  acp_config:
    enabled: true
    strict_mode: false
    timeout: 300
```

**Legacy Basic Mode:**
```yaml
# config.yaml  
agent:
  type: "basic"  # Use basic ModularAgent for compatibility
```

### Environment Variables
- `MINIMAX_API_KEY` - MiniMax API key for LLM access
- `ZAI_API_KEY` - Z.AI API key for web search capabilities

## Usage

### Basic Agent
```python
from mini_agent.core.agent import Agent
from mini_agent.llm.llm_wrapper import LLMClient

# Initialize the agent
agent = Agent()

# Process a message
response = await agent.process_message("Hello, how can you help me?")
```

### With Custom Configuration
```python
from mini_agent.core.agent import Agent
from mini_agent.config import load_config

config = load_config("mini_agent/config/config.yaml")
agent = Agent(config=config)
```

## Skills

The system includes 16+ specialized skills that can be loaded on-demand:

- **Document Processing**: PDF, DOCX, PPTX, XLSX handling
- **Algorithmic Art**: p5.js based generative art creation
- **Memory Management**: Organic memory system management
- **Context Management**: Advanced context optimization
- **MCP Builder**: MCP server development tools
- **Theme Factory**: Document and web theming
- **And more...**

Skills are loaded using progressive disclosure - metadata is shown first, full content loaded when needed.

## MCP Tools

The system integrates with multiple MCP servers for extended capabilities:

- **Z.AI Web Search**: Web search and reading (requires ZAI_API_KEY)
- **Supabase Admin**: Database management capabilities
- **Memory System**: Advanced memory management
- **Session Management**: Session lifecycle management

## Memory System

The memory system provides sophisticated AI-like capabilities:

### Memory Types
- **Identity**: User preferences and communication style
- **Project**: Project-specific context and information
- **Knowledge**: General learning and facts
- **Session**: Temporary conversation context
- **Conversation**: Current discussion thread

### Features
- Natural growth and decay based on usage
- Automatic connection building between related memories
- Project isolation with smart bridging
- Intelligent prompt analysis and categorization

## Development

### Setup
1. Clone the repository
2. Install dependencies: `uv sync`
3. Configure environment variables
4. Set up configuration files

### Testing
```bash
# Run basic functionality tests
python -m pytest tests/

# Test MCP integration
python scripts/test_mcp_tools.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Archive

Previous development work and documentation has been archived in `archive/cleanup_20251128_122451/` for reference.

---

**Built with MiniMax AI** - A sophisticated AI agent platform for enterprise applications.