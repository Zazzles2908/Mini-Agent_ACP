# Mini-Agent Master System Documentation
## Single Source of Truth for System Architecture

---

## 🚀 **System Architecture Overview**

### **Primary LLM: MiniMax-M2**
- **Purpose**: Main reasoning agent (NOT Claude SDK anymore)
- **Interface**: OpenAI-compatible SDK format
- **Configuration**: `mini_agent/llm/llm_wrapper.py`
- **Quota**: 300 prompts/5 hours (coding plan)
- **API**: `https://api.minimax.io`

### **Secondary: Z.AI Web Search/Reading**
- **Purpose**: Web intelligence via MCP servers
- **Interface**: MCP Protocol (Model Context Protocol)
- **Current Status**: Testing/development phase
- **Quota**: 100 web searches + 100 readers (Lite plan)
- **Endpoints**: 
  - Web Search: `https://api.z.ai/api/mcp/web_search_prime/mcp`
  - Web Reader: `https://api.z.ai/api/mcp/web_reader/mcp`

---

## 🔧 **Current Implementation Status**

### **✅ Working Components**
1. **MiniMax-M2 LLM**: Fully operational with OpenAI SDK compatibility
2. **Core Agent System**: 4 integrated modules in `mini_agent/core/`
3. **Skills Framework**: 15+ specialized skills functional
4. **Basic Tools**: File operations, bash execution, notes system

### **🔄 In Progress Components**
1. **MCP Integration**: Web search/reading via MCP servers
2. **Z.AI Configuration**: Testing Lite plan quota usage
3. **File Organization**: Cleanup of scattered documentation

### **⚠️ Known Issues**
1. **Credit Consumption**: Direct API calls vs MCP quota usage
2. **Documentation Overload**: 100+ scattered markdown files
3. **Mixed SDK References**: Some Claude SDK references still present

---

## 📁 **Documentation Structure (Consolidated)**

### **01_CRITICAL_SETUP**
- **MASTER_SYSTEM_DOCUMENTATION.md** (this file)
- **QUICK_START.md** (minimal setup guide)
- **ARCHITECTURE_DECISIONS.md** (why certain choices were made)

### **02_CURRENT_IMPLEMENTATION**
- **MINIMAX_M2_INTEGRATION.md** (primary LLM setup)
- **ZA_I_MCP_INTEGRATION.md** (web search/reading setup)
- **CONFIGURATION.yaml** (single configuration source)

### **03_TOOLS_AND_SKILLS**
- **CORE_TOOLS.md** (built-in capabilities)
- **SKILLS_CATALOG.md** (specialized abilities)
- **MCP_TOOLS.md** (web intelligence tools)

### **04_ARCHIVE**
- **DEPRECATED_DOCS/** (moved files for reference)
- **EXPERIMENTAL_RESEARCH/** (development notes)
- **OLD_BACKUPS/** (historical versions)

---

## 🎯 **Implementation Strategy**

### **Phase 1: Documentation Consolidation**
1. Move all scattered markdown files to proper structure
2. Consolidate overlapping content
3. Remove/backup outdated information
4. Create single source of truth documents

### **Phase 2: MCP Integration Completion**
1. Finalize MCP server configuration
2. Test Z.AI web search/reading quotas
3. Update Mini-Agent to use MCP tools instead of direct API
4. Implement credit protection via configuration

### **Phase 3: SDK Alignment**
1. Remove remaining Claude SDK references
2. Ensure consistent OpenAI SDK format throughout
3. Update system prompt for agent behavior
4. Test full workflow integration

---

## 📊 **Current File Count by Category**

| Category | Count | Status |
|----------|-------|--------|
| Core Documentation | 15 | ✅ Active |
| System Architecture | 25 | 🔄 Cleanup Needed |
| Deprecated/Archive | 85 | 🗂️ Move to Archive |
| Visual/Tools | 20 | 📁 Consolidate |
| Total | 145 | 🎯 Target: 30 |

---

## 🔧 **Configuration Files Reference**

### **Primary Configuration**
```yaml
# mini_agent/config/config.yaml
api_key: "${MINIMAX_API_KEY}"
api_base: "https://api.minimax.io"
model: "MiniMax-M2"
provider: "openai"  # OpenAI SDK format

tools:
  enable_zai_search: true  # MCP integration testing
  enable_zai_llm: false    # Credit protection
```

### **MCP Configuration**  
```json
# .mcp.json
{
  "mcpServers": {
    "zai-web-search": {
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {"Authorization": "Bearer YOUR_API_KEY"}
    }
  }
}
```

---

## 🚨 **Critical Action Items**

### **Immediate (Next 10 minutes)**
1. ✅ Create this master documentation
2. ⏳ Consolidate scattered markdown files
3. ⏳ Archive 100+ duplicate/deprecated files
4. ⏳ Update system prompt with file organization rules

### **Short-term (Next session)**
1. Complete MCP integration testing
2. Verify Z.AI quota usage ($0.72 remaining)
3. Remove direct API calls, implement MCP tools
4. Test full agent workflow

### **Medium-term**
1. Complete documentation consolidation
2. Archive all experimental/research files
3. Finalize agent behavior guidelines
4. Deploy clean, well-documented system

---

## 💡 **Key Architectural Decisions**

1. **MiniMax-M2 over Claude**: Cost-effective, better API access
2. **MCP over Direct API**: Proper quota usage, future-proof
3. **OpenAI SDK Format**: Broad compatibility, standard protocol
4. **Modular Design**: Skills-based architecture for extensibility

---

*Last Updated: [Current Session]*  
*Next Review: After documentation consolidation*