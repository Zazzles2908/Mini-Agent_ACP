# Updated Mini-Agent Technical Documentation Based on Current Sources

**Updated:** 2025-11-25  
**Sources:** MiniMax and Z.AI official documentation and repositories

## Summary of Updates

All existing markdown files have been updated to align with the current MiniMax and Z.AI capabilities as of November 2025. The following files were modified:

## Files Updated

### 1. `mini_agent_technical_audit_report.md`
**Key Updates:**
- Enhanced MCP integration section to include current Z.AI and MiniMax MCP servers
- Updated `zai-mcp-manager` issue analysis with specific endpoint information and quota details
- Added current authentication methods (Bearer token for Z.AI)
- Extended sources section with official MiniMax and Z.AI documentation

**Critical Addition:**
- Z.AI MCP servers information:
  - Web Search MCP: `https://api.z.ai/api/mcp/web_search_prime/mcp`
  - Web Reader MCP: `https://api.z.ai/api/mcp/web_reader/mcp`
  - Quota system: Lite (100), Pro (1,000), Max (4,000)
  - Bearer token authentication requirement

### 2. `research/current_mcp_best_practices.md`
**Key Updates:**
- Added current production examples section
- Included MiniMax-Coding-Plan-MCP specifications (GLM-4.6 model, stdio/SSE transport)
- Added Z.AI MCP server configuration examples
- Extended references with current official documentation

**Current Implementation Details:**
- MiniMax-Coding-Plan-MCP: Coding-specific tools (`web_search`, `understand_image`)
- Z.AI MCP Servers: HTTP-based remote services with Bearer authentication
- One-click installation commands for Claude Code and other MCP clients

### 3. `research/ai_self_validation_architectures.md`
**Key Updates:**
- Integrated current MCP server capabilities into self-awareness context
- Added MiniMax and Z.AI specifications as foundation for validation frameworks
- Extended references with current implementations

**Relevance to Self-Validation:**
- How current MCP integrations (MiniMax-Coding-Plan-MCP, Z.AI search/reader) provide research capabilities
- How these can be enhanced through self-validation frameworks
- Current quota and authentication systems impact on validation strategies

### 4. `research/parallel_research_execution.md`
**Key Updates:**
- Added Z.AI Web Search MCP Server as practical AI-native search implementation
- Updated conclusion to include current production implementations
- Enhanced references with current sources

**Production Implementation Details:**
- Z.AI Web Search MCP Server specifications and capabilities
- Integration methods and authentication requirements
- Real-time information retrieval features for agent research

## Current MiniMax & Z.AI Specifications (2025-11-25)

### MiniMax-Coding-Plan-MCP
- **Purpose**: Specialized MCP server for coding-plan users
- **Tools**: `web_search`, `understand_image`
- **Model**: GLM-4.6
- **Transports**: stdio, SSE
- **Image Support**: JPEG, PNG, WebP
- **GitHub**: https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP

### Z.AI MCP Servers
- **Web Search MCP**: `https://api.z.ai/api/mcp/web_search_prime/mcp`
- **Web Reader MCP**: `https://api.z.ai/api/mcp/web_reader/mcp`
- **Authentication**: Bearer token (`Authorization: Bearer your_api_key`)
- **Pricing**: Lite ($3/month), Pro ($15/month)
- **Quotas**: Lite (100 searches/readers), Pro (1,000), Max (4,000)
- **Reset**: 5-hour cycles
- **Data Location**: Singapore
- **Retention**: No user data storage

### Z.AI Coding Plan Features
- **Models**: GLM-4.6 (Lite), GLM-4.5-Air (Haiku equivalent)
- **Response Speed**: 55+ tokens/second
- **Usage**: ~120 prompts every 5 hours (Lite)
- **Integration**: Claude Code, Roo Code, Kilo Code, Cline, OpenCode, Crush, Goose
- **Additional Features**: Vision Understanding, Web Search MCP, Web Reader MCP

### MiniMax Text AI Coding Tools
- **Model**: MiniMax-M2
- **Capabilities**: Strong code understanding, multi-turn dialogue, reasoning
- **API Endpoints**: Multiple regional endpoints (International/China)
- **Compatibility**: Anthropic API and OpenAI API compatible
- **Black Friday Offer**: $2 Starter plan (ended Dec 1, 2024)

## Impact on Mini-Agent Upgrade Strategy

### Configuration Management
The zai-mcp-manager issue is now clearly understood:
- **Root Cause**: Incorrect path resolution in `config_consolidator.py`
- **Specific Problem**: Z.AI MCP endpoints and Bearer tokens being moved from config directory
- **Impact**: Breaks web search and web reading capabilities essential for research
- **Fix Required**: Centralized configuration management with proper Z.AI endpoint handling

### Self-Validation Integration
Current MCP servers provide excellent foundation for self-validation:
- **Web Research**: Z.AI MCP servers enable real-time information retrieval
- **Code Analysis**: MiniMax-Coding-Plan-MCP provides coding assistance
- **Validation Sources**: Multiple independent sources for cross-validation
- **Quota Management**: Proper rate limiting and quota tracking for research activities

### Parallel Research Capabilities
Current implementations support parallel research execution:
- **Z.AI MCP Servers**: HTTP-based, Bearer authenticated, quota-managed
- **Rate Limiting**: Built-in quota system per plan
- **Integration**: One-click installation for major MCP clients
- **Real-time Data**: Access to current information for validation

## Recommendations for Intermediate Developer

1. **Fix Configuration Path Issue**: Update `config_consolidator.py` to properly handle Z.AI MCP endpoints
2. **Implement Bearer Token Management**: Secure storage and handling of Z.AI API keys
3. **Add Quota Tracking**: Monitor usage against Z.AI plan limits
4. **Enhance Self-Validation**: Leverage current MCP servers for multi-source research validation
5. **Integrate Current Documentation**: Use official endpoints and authentication methods from sources above

## Next Steps

1. Review updated documentation files
2. Implement configuration fixes based on current Z.AI specifications
3. Test integration with current MCP servers
4. Develop self-validation framework using available research capabilities
5. Monitor quota usage and implement proper rate limiting

All documentation now reflects current production capabilities and provides accurate technical guidance for the Mini-Agent self-awareness upgrade implementation.
