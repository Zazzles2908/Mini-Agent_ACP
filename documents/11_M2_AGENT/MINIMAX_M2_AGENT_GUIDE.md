# MiniMax-M2 Agent Implementation Guide

## Overview

MiniMax-M2 is the **primary reasoning model** for this Mini-Agent system, providing 300 prompts every 5 hours for complex reasoning, extended thinking, and core agent execution.

## Core Architecture

### Primary Model Status
- **Model**: MiniMax-M2 (minimax-MiniMax-M2-4-20250514)
- **Quota**: 300 prompts every 5 hours
- **Role**: Primary reasoning and execution engine
- **Environment Variable**: `MINIMAX_API_KEY`

### Integration with Z.AI Web Intelligence
MiniMax-M2 works in conjunction with Z.AI GLM-4.6 for web capabilities:
- **MiniMax-M2**: Core reasoning (300 prompts/5hrs)
- **Z.AI GLM-4.6**: Web search and reading (100 searches + 100 readers FREE)

## Configuration

### Environment Setup
```bash
# Required for MiniMax-M2
setx MINIMAX_API_KEY your_minimax_api_key

# Optional: For web search capabilities
setx ZAI_API_KEY your_zai_api_key
```

### Configuration File
```yaml
# mini_agent/config/config.yaml
default_provider: "minimax"
default_model: "minimax-MiniMax-M2-4-20250514"
api_key: "${MINIMAX_API_KEY}"
api_base: "https://api.minimax.io"

# Web capabilities via Z.AI
tools:
  enable_zai_search: true
```

## Capabilities

### Core Reasoning Features
- **Extended Thinking**: Complex problem solving and analysis
- **Tool Calling**: Execute functions and integrate with external systems
- **Context Management**: Maintain conversation history and state
- **Error Handling**: Robust retry mechanisms with exponential backoff

### Integration Points
- **File Operations**: Read, write, edit files with full path support
- **Bash Execution**: Command execution (PowerShell on Windows, bash on Unix)
- **Session Management**: Persistent context across conversations
- **Knowledge Graph**: Entity management and relationship tracking

### Skills System
20+ specialized capabilities loaded via progressive disclosure:
- Document processing (PDF, DOCX, PPTX, XLSX)
- Algorithmic art generation
- Web application testing
- Internal communications
- Canvas design
- And more...

## Usage Patterns

### Interactive Mode
```bash
# Start interactive session
mini-agent

# Available commands:
# /help - Show available commands
# /clear - Clear message history
# /stats - Show session statistics
# /exit - Exit agent
```

### Single Command Mode
```bash
# Execute single task
mini-agent "Analyze the README and summarize it"

# With specific model
mini-agent --model minimax-MiniMax-M2-4-20250514 "Complex analysis task"
```

### ACP Server Mode
```bash
# Start ACP server for editor integration
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

## Best Practices

### Quota Management
- **Monitor Usage**: Track 300 prompts every 5 hours
- **Efficient Prompting**: Provide clear, specific requests
- **Context Optimization**: Use session management to avoid repetition
- **Fallback Planning**: Have alternative approaches ready

### Development Workflow
1. **Setup**: Configure `MINIMAX_API_KEY` environment variable
2. **Verify**: Run `mini-agent --help` to test connectivity
3. **Test**: Start with simple tasks to verify functionality
4. **Scale**: Build complex workflows incrementally

### Integration Guidelines
- Use MiniMax-M2 for primary reasoning tasks
- Leverage Z.AI for web search when needed (FREE quotas)
- Combine with specialized skills for domain expertise
- Maintain clear separation between reasoning and data gathering

## Troubleshooting

### Common Issues
1. **API Key Missing**: Ensure `MINIMAX_API_KEY` is set in environment
2. **Connection Errors**: Check internet connectivity and API endpoints
3. **Quota Exhaustion**: Monitor prompt usage and plan accordingly
4. **Model Errors**: Verify model name `minimax-MiniMax-M2-4-20250514`

### Debug Commands
```bash
# Test API connectivity
uv run python -c "import os; print('MINIMAX_API_KEY' in os.environ)"

# Verify agent functionality
mini-agent --help

# Check configuration
cat mini_agent/config/config.yaml
```

## System Architecture

### File Structure
```
mini_agent/
├── agent.py              # Core agent loop
├── cli.py                # Command-line interface
├── config.py             # Configuration loader
├── llm/
│   ├── anthropic_client.py  # MiniMax-M2 integration
│   ├── openai_client.py     # OpenAI-compatible format
│   ├── llm_wrapper.py       # Unified interface
│   └── zai_client.py        # Z.AI integration
├── tools/                # Tool implementations
│   ├── file_tools.py     # File operations
│   ├── bash_tool.py      # Command execution
│   ├── mcp_loader.py     # MCP integration
│   ├── skill_tool.py     # Skills system
│   └── zai_tools.py      # Z.AI tools
└── skills/               # Specialized capabilities
```

### Integration Flow
```
User Request → MiniMax-M2 → Tool Execution → Result Processing → Response
                      ↓
              Z.AI GLM-4.6 (when web search needed)
                      ↓
              Web Intelligence (100 searches + 100 readers FREE)
```

## Performance Optimization

### Efficient Usage
- **Clear Prompts**: Provide specific, actionable requests
- **Batch Operations**: Group related tasks together
- **Context Reuse**: Maintain conversation context for related queries
- **Tool Selection**: Choose appropriate tools for each task

### Monitoring
- **Quota Tracking**: Monitor prompt usage against 300/5hrs limit
- **Performance Metrics**: Track response times and success rates
- **Error Analysis**: Monitor and address recurring issues
- **Usage Patterns**: Identify optimal usage patterns

---

**Status**: Primary reasoning model fully integrated and operational
**Next Steps**: Monitor usage patterns and optimize workflows
**Support**: Refer to project documentation for detailed implementation guides
