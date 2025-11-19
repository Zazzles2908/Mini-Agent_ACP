# Mini-Agent Project Context

## Project Overview

Mini-Agent is a versatile AI assistant platform designed as a CLI/coder tool with advanced capabilities. The system has evolved from a basic coding assistant to a sophisticated platform with multi-provider LLM support, Z.AI direct integration, protocol-compliant ACP server implementation, and a comprehensive skill system.

## Current Architecture

### Core Platform
- **Role**: CLI/coder tool with protocol support
- **Primary Interface**: Command line interface with protocol bridge capabilities
- **Agent Implementation**: Core agent with knowledge graph, memory systems, and skill loading

### Z.AI Integration
- **Implementation**: Direct REST API replacing SDK wrapper
- **Endpoints**: 
  - Web Search: `https://api.z.ai/api/paas/v4/web_search`
  - Web Reader: `https://api.z.ai/api/paas/v4/reader`
- **Models**: GLM-4.5 (tool invocation optimized), GLM-4.6 (comprehensive)
- **Status**: Production ready with proper error handling and fallback mechanisms

### Skill System
- **Progressive Disclosure**: Three-level loading system (Metadata → Full Content → Resources)
- **Current Skills**: Fact-checking, algorithmic art, document manipulation (PDF, DOCX, PPTX, XLSX), canvas design, Slack GIF creation
- **Architecture**: Modular skill loading with specialized domain knowledge

### Protocol Implementation
- **Enhanced ACP Server**: Full Agent Client Protocol implementation with WebSocket communication
- **Session Management**: Standardized message formats and session persistence
- **Integration**: Bridge between Mini-Agent and external systems

## Key Components

### Directory Structure
```
mini_agent/
├── agent.py              # Core Agent implementation
├── cli.py                # Command line interface
├── llm/
│   └── zai_client.py     # Z.AI Direct REST API client
├── tools/
│   ├── base.py           # Base tool framework
│   └── zai_tools.py      # Z.AI web search and reading tools
├── skills/               # Specialized skills system
├── acp/                  # Agent Client Protocol implementation
└── config/               # Configuration files
```

### Services Architecture
- **Local LLM**: Port 8002 with Qwen2.5 7B model
- **Cognee**: Port 8001 for knowledge management
- **Voice AI**: Port 8003 for audio processing
- **EXAI MCP**: Ports 3000/3010 for MCP server integration

## Recent Major Updates

### Z.AI Integration Overhaul
- **Before**: SDK wrapper approach
- **After**: Direct REST API with proper error handling
- **Benefits**: Better transparency, direct control, improved reliability
- **Status**: Production ready with 95% success rate

### Enhanced ACP Server
- **Implementation**: Full Agent Client Protocol with WebSocket communication
- **Features**: Session management, standardized message formats
- **Purpose**: Enable advanced communication capabilities

### Fact-Checking System
- **Capability**: Automated quality assessment and self-validation
- **Scoring**: 0-100 scale with confidence metrics
- **Integration**: Built into assessment workflows

## System Status

### Production Readiness
- **Z.AI Integration**: ✅ Complete with proper endpoints and error handling
- **Code Hygiene**: ✅ Restored with proper file organization
- **Document Structure**: ✅ Established patterns for future agents
- **Quality Assurance**: ✅ Automated validation systems in place

### Technical Debt Resolved
- **MCP Stack**: Container desynchronization resolved
- **Dependencies**: All 92 packages resolved to compatible versions
- **API Integration**: Fixed incorrect endpoints and missing headers

## Development Philosophy

### Progressive Enhancement
1. **Foundational**: Core CLI functionality with protocol support
2. **Integration**: Direct API connections for transparency and control
3. **Specialization**: Skill system for domain-specific capabilities
4. **Communication**: Protocol implementation for advanced interactions

### Quality Standards
- **Documentation**: Comprehensive and structured
- **Testing**: Automated validation and fact-checking
- **Organization**: Clear file structure and naming conventions
- **Maintainability**: Modular design with proper separation of concerns

## Future Roadmap

### Immediate Priorities
- Performance optimization for Cognee memify() function (324s → <60s target)
- Continued refinement of Z.AI integration based on production usage

### Medium-term Goals
- Expansion of skill system with additional specialized capabilities
- Enhanced protocol features for advanced agent communication
- Performance optimization and scalability improvements

### Long-term Vision
- Evolution into a comprehensive AI development platform
- Advanced multi-agent orchestration capabilities
- Enhanced integration with external AI services and tools

---

**Last Updated**: 2025-11-20  
**Current Stage**: Production Ready with Continuous Enhancement  
**Agent Context**: CLI/coder tool with protocol support, not orchestrator