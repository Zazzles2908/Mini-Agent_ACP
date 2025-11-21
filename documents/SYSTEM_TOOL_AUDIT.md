# 🛠️ Mini-Agent System Tool Audit & Optimization Guide

## 📋 Executive Summary

**System Type**: Extended Mini-Agent with multi-provider LLM integration and comprehensive tool ecosystem  
**Primary LLM**: MiniMax-M2 (via OpenAI-compatible API)  
**Secondary LLM**: Z.AI GLM-4.5/4.6 (web search + additional reasoning)  
**Platform**: Windows (PowerShell), Unix/Linux compatible  
**Total Tools Available**: 50+ specialized tools across 8 categories

---

## 🎯 Core Architecture Overview

### **Multi-Layer Tool Hierarchy**
```
┌─────────────────────────────────────┐
│  🧠 Primary LLM Layer (MiniMax-M2)  │
├─────────────────────────────────────┤
│  🔍 Secondary LLM (Z.AI GLM-4.5/4.6)│
├─────────────────────────────────────┤
│  🛠️ Native Tools (File, Bash, Notes) │
├─────────────────────────────────────┤
│  🎯 Specialized Skills (16 Skills)  │
├─────────────────────────────────────┤
│  📚 Knowledge Graph & Memory        │
└─────────────────────────────────────┘
```

### **Provider Strategy**
- **Primary Reasoning**: MiniMax-M2 (high-quality reasoning)
- **Web Intelligence**: Z.AI GLM-4.5/4.6 (search + analysis)
- **Fallback**: OpenAI GPT-4, Anthropic Claude
- **Efficiency**: GLM-4.5 for routine tasks, GLM-4.6 for complex analysis

---

## 🔧 Complete Tool Inventory

### **1. Native Core Tools** ✅ Available
**File Location**: `mini_agent/tools/`

| Tool | File | Purpose | Criticality |
|------|------|---------|-------------|
| `file_tools.py` | File Operations | Read/Write/Edit with full path support | ⭐⭐⭐ |
| `bash_tool.py` | Bash Execution | PowerShell/Unix commands, Git, packages | ⭐⭐⭐ |
| `note_tool.py` | Session Notes | Persistent context across conversations | ⭐⭐ |
| `base.py` | Tool Framework | Base classes for tool development | ⭐⭐ |

### **2. Z.AI Integration Tools** ⚡ Available
**Purpose**: Web search, reading, and additional reasoning

| Tool | File | Models | Quota Management |
|------|------|--------|------------------|
| `zai_tools.py` | Basic Z.AI | GLM-4.5/4.6/4.5-air | ~120 prompts/5hrs |
| `zai_web_search_with_citations.py` | Web Search | GLM-4.5 optimized | Integrated |
| `zai_anthropic_tools.py` | Extended Tools | GLM-4.6 analysis | Advanced features |
| `claude_zai_tools.py` | Claude Bridge | GLM-4.6 + Claude integration | Hybrid mode |
| `claude_zai_extended_tools.py` | Advanced Bridge | Full feature set | Complete |

### **3. Skills System** 🎯 16 Skills Available
**Location**: `mini_agent/skills/`

#### **Document Processing Skills**
| Skill | Directory | Capability | Python Environment Required |
|-------|-----------|------------|----------------------------|
| **docx** | `document-skills/docx/` | Word document creation/editing | ✅ Setup venv first |
| **pdf** | `document-skills/pdf/` | PDF manipulation, forms | ✅ Setup venv first |
| **pptx** | `document-skills/pptx/` | PowerPoint presentations | ✅ Setup venv first |
| **xlsx** | `document-skills/xlsx/` | Excel spreadsheets | ✅ Setup venv first |

#### **Creative & Design Skills**
| Skill | Directory | Capability |
|-------|-----------|------------|
| **canvas-design** | `canvas-design/` | Visual art creation with fonts |
| **algorithmic-art** | `algorithmic-art/` | p5.js generative art |
| **brand-guidelines** | `brand-guidelines/` | Anthropic brand styling |
| **theme-factory** | `theme-factory/` | 10 pre-set themes for artifacts |
| **artifacts-builder** | `artifacts-builder/` | Complex React artifacts |
| **slack-gif-creator** | `slack-gif-creator/` | Animated GIFs for Slack |

#### **Development & Integration Skills**
| Skill | Directory | Capability |
|-------|-----------|------------|
| **mcp-builder** | `mcp-builder/` | MCP server creation |
| **skill-creator** | `skill-creator/` | New skill development |
| **vscode_integration** | `vscode_integration/` | VS Code Chat API |
| **webapp-testing** | `webapp-testing/` | Playwright web testing |

#### **Communication & Assessment Skills**
| Skill | Directory | Capability |
|-------|-----------|------------|
| **internal-comms** | `internal-comms/` | Company communications |
| **fact-checking-self-assessment** | `fact-checking-self-assessment/` | Quality assurance |

#### **Template Skills**
| Skill | Directory | Capability |
|-------|-----------|------------|
| **template-skill** | `template-skill/` | Base template for new skills |

### **4. Knowledge Graph & Memory** 🧠 Available
**Integrated into native tools**

| Function | Purpose | Usage Pattern |
|----------|---------|---------------|
| `create_entities` | Structured knowledge storage | `create_entities([{name, entityType, observations}])` |
| `add_observations` | Extend existing entities | `add_observations([{entityName, contents}])` |
| `open_nodes` | Retrieve entities by name | `open_nodes([entity_names])` |
| `search_nodes` | Search knowledge graph | `search_nodes(query)` |
| `read_graph` | Get entire graph | `read_graph()` |
| `create_relations` | Link entities | `create_relations([{from, to, relationType}])` |
| `delete_entities` | Remove entities | `delete_entities([entity_names])` |
| `delete_relations` | Remove links | `delete_relations([{from, to, relationType}])` |
| `delete_observations` | Remove from entities | `delete_observations([{entityName, observations}])` |

### **5. LLM Client System** 🔌 Multiple Providers
**Location**: `mini_agent/llm/`

| Client | Provider | Protocol | Purpose |
|--------|----------|----------|---------|
| `zai_client.py` | Z.AI | Direct API | Web search & GLM models |
| `claude_zai_client.py` | Z.AI + Claude | Hybrid | Combined reasoning |
| `extended_claude_zai_client.py` | Z.AI + Claude | Extended | Advanced features |
| `coding_plan_zai_client.py` | Z.AI | Coding plan | Efficient usage |
| `anthropic_client.py` | Anthropic | OpenAI format | Claude models |
| `openai_client.py` | OpenAI | OpenAI API | GPT models |
| `glm_client.py` | Z.AI | GLM specific | GLM models |
| `llm_wrapper.py` | Multi-provider | Universal | Provider coordination |

### **6. Configuration System** ⚙️ Advanced
**Location**: `mini_agent/config/`

| File | Purpose | Key Settings |
|------|---------|--------------|
| `config.yaml` | Main configuration | Models, tools, retry logic |
| `system_prompt.md` | Agent behavior | Instructions & guidelines |
| `mcp.json` | MCP tool configuration | External server setup |
| `config-example.yaml` | Template | Reference configuration |

### **7. ACP (Agent Client Protocol)** 🔌 VS Code Integration
**Location**: `mini_agent/acp/`

| Component | Purpose | Status |
|-----------|---------|--------|
| `server.py` | Basic ACP server | Available |
| `enhanced_server.py` | Enhanced features | Available |
| `__init__.py` | Main interface | Active |

---

## 📊 Tool Utilization Strategy

### **Tier 1: Essential Tools (Use Always)**
```python
# File Operations - Every task
read_file(path)        # ✅ Native, no dependencies
write_file(path, content)  # ✅ Native
edit_file(path, old_str, new_str)  # ✅ Native

# Bash Commands - System operations
bash(command)          # ✅ Native, PowerShell/Unix aware

# Knowledge Management - Context preservation
record_note(content, category)  # ✅ Native session persistence
create_entities(entities)       # ✅ Knowledge graph
```

### **Tier 2: Specialized Tools (Use Judiciously)**
```python
# Z.AI Web Intelligence - When research needed
# ⚠️ Quota: ~120 prompts every 5 hours
zai_web_search(query, model="glm-4.5")  # Efficient search
zai_web_reader(url)              # Content extraction

# Document Skills - When file processing needed
# ⚠️ Requires: Python venv setup first
get_skill("docx")                # Word docs
get_skill("pdf")                 # PDF manipulation
get_skill("pptx")                # Presentations
get_skill("xlsx")                # Spreadsheets
```

### **Tier 3: Advanced Skills (Use for Complex Tasks)**
```python
# Creative Tasks
get_skill("algorithmic-art")     # p5.js generative art
get_skill("canvas-design")       # Visual design
get_skill("theme-factory")       # Styling artifacts

# Development Tasks
get_skill("webapp-testing")      # Playwright automation
get_skill("mcp-builder")         # MCP server creation
get_skill("skill-creator")       # Skill development

# Quality Assurance
get_skill("fact-checking-self-assessment")  # Validation
```

---

## ⚡ Efficiency Guidelines

### **Z.AI Coding Plan Optimization**
```python
# ✅ GOOD: Efficient usage patterns
# 1. Use GLM-4.5 for routine tasks (web search, basic analysis)
# 2. Reserve GLM-4.6 for complex analysis and debugging
# 3. Batch related operations together
# 4. Aim for <2000 tokens per prompt

# ❌ BAD: Inefficient usage
# - Using GLM-4.6 for simple web searches
# - Multiple small prompts instead of batched requests
# - No context reuse between related tasks
```

### **Tool Selection Matrix**
| Task Type | Recommended Tools | Model | Cost Efficiency |
|-----------|-------------------|-------|----------------|
| **File Operations** | Native tools | N/A | 🟢 Free |
| **System Commands** | Native bash | N/A | 🟢 Free |
| **Web Research** | Z.AI search | GLM-4.5 | 🟡 Limited quota |
| **Complex Analysis** | Z.AI extended | GLM-4.6 | 🔴 High quota use |
| **Document Creation** | Document skills | + Python env | 🟡 Setup required |
| **Creative Work** | Design skills | + Python env | 🟡 Setup required |
| **Code Testing** | Webapp-testing | + Python env | 🟡 Setup required |

---

## 🚨 Critical Setup Requirements

### **Python Environment (Required for Document/Creative Skills)**
```bash
# BEFORE using any Python-based skills
1. Check venv: if [ ! -d .venv ]; then uv venv; fi
2. Install: uv pip install <package>
3. Run: uv run python script.py
4. If uv missing: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### **Environment Variables**
```bash
# Required for full functionality
MINIMAX_API_KEY=your_minimax_key       # Primary LLM
ZAI_API_KEY=your_zai_key               # Web search + GLM
OPENAI_API_KEY=your_openai_key         # Fallback LLM
```

### **Platform-Specific Notes**
```bash
# Windows (Current Platform)
# - Use PowerShell commands (already detected)
# - Quote paths with spaces: "My Documents"
# - Backslash paths: C:\Users\...

# Unix/Linux/macOS
# - Use bash commands
# - Forward slash paths: /home/user/...
```

---

## 🎯 Automatic Tool Utilization Protocol

### **Phase 1: System Assessment** (First 30 seconds)
```python
# 1. Check workspace structure
bash("Get-Location; Get-ChildItem")  # Windows

# 2. Verify configuration
read_file("mini_agent/config/config.yaml")

# 3. Check project context
read_file("documents/AGENT_HANDOFF.md") if exists
read_file("documents/PROJECT_CONTEXT.md") if exists

# 4. Assess prerequisites
bash("if [ ! -d .venv ]; then echo 'No venv found'; fi")
```

### **Phase 2: Tool Strategy Selection** (First 60 seconds)
```python
# Determine task category and select tools
task_category = assess_task_type(user_request)

if task_category == "web_research":
    tools = ["zai_web_search", "zai_web_reader"]
    model = "glm-4.5"  # Efficient
elif task_category == "document_processing":
    tools = ["get_skill(docx/pdf/pptx/xlsx)"]
    model = "python_venv"  # Setup required
elif task_category == "file_operations":
    tools = ["read_file", "write_file", "edit_file"]
    model = "native"  # No quota
```

### **Phase 3: Knowledge Graph Integration** (Ongoing)
```python
# Always persist important context
record_note(f"Task: {user_request}", "task_context")
create_entities([
    {"name": "current_project", "entityType": "project", "observations": ["Active session", "User working on specific task"]}
])
```

---

## 📈 Success Metrics

### **Efficiency KPIs**
- **Tool Selection Accuracy**: 95%+ correct tool choice on first attempt
- **Quota Management**: Stay within 80% of Z.AI limits per 5-hour window
- **Context Preservation**: 100% important decisions logged to knowledge graph
- **Setup Optimization**: <2 minutes to prepare Python environment when needed

### **Quality KPIs**
- **File Operations**: 100% successful with proper error handling
- **Web Intelligence**: <3 seconds average response time for searches
- **Documentation**: All new work documented in `documents/` folder
- **Code Quality**: Python skills require venv setup before execution

---

## 🔄 Continuous Optimization

### **Weekly Review Process**
1. **Quota Analysis**: Review Z.AI usage patterns and optimize
2. **Tool Effectiveness**: Analyze success/failure rates by tool
3. **Knowledge Graph Growth**: Ensure session context is properly captured
4. **Skill Utilization**: Evaluate which skills are most valuable

### **Tool Evolution Tracking**
- Monitor new skills integration
- Track API changes affecting tools
- Document best practices for tool combinations
- Update efficiency guidelines based on usage patterns

---

**Last Updated**: 2025-11-22  
**System Version**: Mini-Agent v0.1.0 Extended  
**Next Review**: Weekly quota and performance analysis
