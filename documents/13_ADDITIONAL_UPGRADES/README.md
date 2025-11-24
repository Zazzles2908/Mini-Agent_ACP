# 🚀 Mini-Agent Additional Upgrades

This directory contains comprehensive upgrade plans for Mini-Agent system enhancements organized into three strategic phases.

## 📋 Directory Structure

```
13_ADDITIONAL_UPGRADES/
├── README.md                           # This file - Overview of all upgrade phases
├── PHASE_1_WEB_SEARCH/                # Web search architecture optimization
│   ├── PHASE_1_IMPLEMENTATION_PLAN.md # Complete implementation guide
│   ├── ZAI_MCP_INTEGRATION.md        # Z.AI MCP server setup
│   └── MINIMAX_CODING_PLAN_MCP.md    # MiniMax Coding Plan MCP setup
├── PHASE_2_SUPABASE/                  # Supabase database integration
│   ├── PHASE_2_IMPLEMENTATION_PLAN.md # Complete implementation guide
│   ├── SUPABASE_MCP_SERVER.md        # Custom MCP server design
│   └── DATABASE_OPERATIONS.md         # All database operations reference
└── PHASE_3_OBSERVABILITY_ACP/         # Future: Langfuse + ACP integration
    ├── PHASE_3_IMPLEMENTATION_PLAN.md # Complete implementation guide
    ├── LANGFUSE_INTEGRATION.md        # LLM observability setup
    └── ACP_ZED_INTEGRATION.md         # Agent Client Protocol with Zed

```

## 🎯 Phase Overview

### **Phase 1: Web Search Architecture Optimization** 🔍
**Status**: Ready for Implementation  
**Priority**: High  
**Estimated Time**: 2-3 hours

**Goals:**
- Fix Z.AI MCP protocol implementation (SSE vs JSON-RPC)
- Integrate MiniMax Coding Plan MCP with web_search and understand_image tools
- Remove duplicate web search functionality
- Align with Mini-Agent's proven hybrid architecture pattern
- Establish single, reliable web search workflow

**Key Deliverables:**
- Properly configured Z.AI MCP servers (web-search-prime, web-reader)
- MiniMax Coding Plan MCP integration (web_search, understand_image)
- Unified web search tool with intelligent fallback
- Updated configuration files and documentation

**Why This Matters:**
Current architecture has redundant tools (MCP + Direct API fallback) due to protocol mismatch. This phase creates a clean, efficient web search system that uses FREE quotas properly and follows Mini-Agent's design patterns.

---

### **Phase 2: Supabase Database Integration** 🗄️
**Status**: Ready for Implementation  
**Priority**: High  
**Estimated Time**: 3-4 hours

**Goals:**
- Implement custom Supabase MCP server with admin-level access
- Provide comprehensive database operations (all CRUD + schema management)
- Create long-term storage system for project data
- Enable internal memory persistence across sessions
- Full transparency and visibility into all database operations

**Key Deliverables:**
- Custom Supabase MCP server with all operations
- Admin-level database control with service role key
- Project memory and storage system
- Database operation logging and monitoring
- Integration with existing Mini-Agent tools

**Why This Matters:**
Supabase will serve as Mini-Agent's long-term memory and project storage. This enables persistent context across sessions, project tracking, and knowledge accumulation. Full admin access ensures complete control and transparency.

---

### **Phase 3: Observability & Editor Integration** 📊 
**Status**: PAUSED - Future Implementation  
**Priority**: Medium  
**Estimated Time**: 5-6 hours

**Goals:**
- Integrate Langfuse for LLM observability and tracing
- Implement Agent Client Protocol (ACP) for Zed editor integration
- Create comprehensive monitoring and analytics system
- Enable multi-editor support through open protocols

**Key Deliverables:**
- Langfuse integration for all LLM calls
- ACP implementation for Zed editor
- Trace visualization and analytics
- Performance monitoring and cost tracking
- Multi-editor compatibility layer

**Why This Matters:**
Langfuse provides production-grade observability for LLM operations (cost tracking, performance monitoring, debugging). ACP enables Mini-Agent to work seamlessly with modern editors like Zed and JetBrains, expanding beyond VS Code.

**Why Paused:**
This phase requires stable foundation from Phases 1 & 2. Once web search and database systems are solid, observability and editor integration will provide significant value for production usage and multi-user scenarios.

---

## 🏗️ Implementation Strategy

### **Sequential Implementation (Recommended)**

```
Phase 1 (Web Search) → Phase 2 (Supabase) → Phase 3 (Observability/ACP)
     ↓                      ↓                         ↓
  Foundation          Long-term Memory        Production Ready
```

**Rationale:**
1. **Phase 1 First**: Fixes immediate architectural issues, establishes clean web search
2. **Phase 2 Second**: Builds on stable web search, adds persistence and memory
3. **Phase 3 Last**: Adds observability and editor integration to complete system

### **Parallel Implementation (Advanced)**

For experienced teams, Phases 1 and 2 can run in parallel:
- **Team A**: Web search architecture (Phase 1)
- **Team B**: Supabase MCP implementation (Phase 2)
- **Integration Point**: After both complete, merge and test

**Phase 3 always waits for 1 & 2 to complete.**

---

## 📊 Success Metrics

### **Phase 1 Success Criteria:**
- ✅ Zero web search tool failures
- ✅ MCP protocol working correctly (no fallback to direct API)
- ✅ MiniMax Coding Plan MCP operational (web_search, understand_image)
- ✅ Single, reliable web search workflow
- ✅ FREE quota usage tracking accurate

### **Phase 2 Success Criteria:**
- ✅ All database operations functional (CRUD, schema, admin)
- ✅ Service role key properly secured
- ✅ Project memory persisting across sessions
- ✅ Full operation transparency and logging
- ✅ Integration with web search workflow

### **Phase 3 Success Criteria:**
- ✅ Langfuse tracing all LLM calls
- ✅ ACP integration with Zed editor
- ✅ Cost and performance analytics available
- ✅ Multi-editor support working
- ✅ Production monitoring active

---

## 🔗 Dependencies

### **Phase 1 Dependencies:**
- Z.AI API key (ZAI_API_KEY)
- MiniMax API key (MINIMAX_API_KEY)
- MiniMax Coding Plan subscription
- Python packages: aiohttp, fastmcp

### **Phase 2 Dependencies:**
- Supabase project URL
- Supabase service role key
- Supabase admin access token
- Python packages: supabase-py, fastmcp

### **Phase 3 Dependencies:**
- Langfuse account (self-hosted or cloud)
- Langfuse API keys
- Zed editor (for ACP testing)
- Python packages: langfuse, acpex

---

## 📚 Additional Resources

### **Official Documentation:**
- [Z.AI MCP Documentation](https://docs.z.ai/devpack/mcp/search-mcp-server)
- [MiniMax Coding Plan MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Langfuse Documentation](https://langfuse.com/docs)
- [Agent Client Protocol (ACP)](https://zed.dev/acp)

### **Mini-Agent Architecture References:**
- `documents/03_ARCHITECTURE/SYSTEM_ARCHITECTURE.md`
- `documents/08_TOOLS_INTEGRATION/MCP_SERVERS_FINAL_REPORT.md`
- `documents/01_OVERVIEW/AGENT_HANDOFF.md`

---

## 🎯 Quick Start

### **For Phase 1:**
```bash
cd documents/13_ADDITIONAL_UPGRADES/PHASE_1_WEB_SEARCH
# Read PHASE_1_IMPLEMENTATION_PLAN.md for complete guide
```

### **For Phase 2:**
```bash
cd documents/13_ADDITIONAL_UPGRADES/PHASE_2_SUPABASE
# Read PHASE_2_IMPLEMENTATION_PLAN.md for complete guide
```

### **For Phase 3:**
```bash
cd documents/13_ADDITIONAL_UPGRADES/PHASE_3_OBSERVABILITY_ACP
# Read PHASE_3_IMPLEMENTATION_PLAN.md when ready (currently paused)
```

---

## ⚡ Current Status

**Last Updated**: November 24, 2025

| Phase | Status | Progress | Next Action |
|-------|--------|----------|-------------|
| Phase 1 | Ready | 0% | Begin implementation |
| Phase 2 | Ready | 0% | Wait for Phase 1 |
| Phase 3 | Paused | 0% | Wait for Phases 1 & 2 |

---

## 🤝 Contributing

When implementing these phases:
1. Follow Mini-Agent's architecture patterns (see `documents/03_ARCHITECTURE/`)
2. Update `documents/01_OVERVIEW/AGENT_HANDOFF.md` with progress
3. Document all changes in respective phase folders
4. Test thoroughly before marking phase complete

---

*For questions or clarifications, refer to the detailed implementation plans in each phase folder.*
