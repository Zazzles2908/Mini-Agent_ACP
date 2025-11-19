# Mini-Agent Documentation Hub

## 🎯 **Quick Navigation**

### **For New Agents - Start Here** 🚀
1. **[Agent Best Practices](workflows/AGENT_BEST_PRACTICES.md)** - Mandatory first steps
2. **[Project Context](project/PROJECT_CONTEXT.md)** - System overview and status
3. **[Setup Guide](setup/SETUP_GUIDE.md)** - Installation and configuration
4. **[Universal Workflow Protocol](workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md)** - 5-phase mandatory process

### **Architecture & Design** 🏗️
- **[Architectural Mastery](architecture/MINI_AGENT_ARCHITECTURAL_MASTERY.md)** - System design patterns
- **[Codebase Organization](CODEBASE_ORGANIZATION_REFERENCE.md)** - File structure reference
- **[System Architecture](architecture/SYSTEM_ARCHITECTURE.md)** - Technical overview
- **[ACP Protocol Guide](architecture/ACP_PROTOCOL_INTEGRATION.md)** - Editor integration protocol
- **[VS Code Integration](architecture/VSCODE_INTEGRATION_GUIDE.md)** - Extension development guide

### **Development Resources** 🛠️
- **[Agent Handoff](project/AGENT_HANDOFF.md)** - Current status and next steps
- **[Configuration Guide](setup/CONFIGURATION_GUIDE.md)** - System configuration
- **[Usage Examples](examples/USAGE_EXAMPLES.md)** - Common patterns
- **[Troubleshooting](troubleshooting/TROUBLESHOOTING.md)** - Problem resolution

---

## 📁 **Documentation Structure**

This documentation follows a professional 7-category organizational system:

```
documents/
├── architecture/          # System design and architecture (9 files)
├── workflows/             # Procedures and protocols (2 files)
├── project/               # Management and context (4 files)
├── setup/                 # Installation and configuration (3 files)
├── examples/              # Usage patterns and templates (3 files)
├── testing/               # Validation and reports (15+ files)
├── troubleshooting/       # Problem resolution (2 files)
├── legacy/                # Historical documentation
├── vscode-extension/      # Extension integration guides
└── archive/               # Previous agent work
```

---

## 🔍 **Finding Information**

### By Task Type
- **Setting up Mini-Agent** → [Setup Guide](setup/SETUP_GUIDE.md)
- **Understanding architecture** → [Architectural Mastery](architecture/MINI_AGENT_ARCHITECTURAL_MASTERY.md)
- **Starting a new task** → [Universal Workflow](workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md)
- **Implementing features** → [Agent Best Practices](workflows/AGENT_BEST_PRACTICES.md)
- **Solving problems** → [Troubleshooting](troubleshooting/TROUBLESHOOTING.md)
- **Reviewing status** → [Project Context](project/PROJECT_CONTEXT.md)

### By Component
- **Skills System** → [Architectural Mastery](architecture/MINI_AGENT_ARCHITECTURAL_MASTERY.md)
- **Z.AI Integration** → [Project Context](project/PROJECT_CONTEXT.md)
- **Knowledge Graph** → [Codebase Organization](CODEBASE_ORGANIZATION_REFERENCE.md)
- **VS Code Extension** → [VS Code Integration Guide](architecture/VSCODE_INTEGRATION_GUIDE.md)
- **ACP Server** → [ACP Protocol Guide](architecture/ACP_PROTOCOL_INTEGRATION.md)

---

## 🚀 **Quick Start for Agents**

### Mandatory Agent Initialization
```bash
# 1. Query organizational knowledge
search_nodes("Mini-Agent Codebase Organization System")
search_nodes("Universal Workflow Protocol")
read_graph()

# 2. Load fact-checking skill
get_skill("fact-checking-self-assessment")

# 3. Validate workspace
python scripts/validation/pre_implementation_check.py

# 4. Review workflow protocol
read_file("documents/workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md")
```

### Essential Reading (5 minutes)
1. **[Agent Best Practices](workflows/AGENT_BEST_PRACTICES.md)** - How to work with Mini-Agent
2. **[Project Context](project/PROJECT_CONTEXT.md)** - What is Mini-Agent
3. **[Universal Workflow](workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md)** - How to complete tasks

---

## 🎯 **System Identity**

**Mini-Agent is a CLI/coder tool with protocol support**, serving as the foundation for a broader ecosystem:

### Three-Project Ecosystem
1. **Mini-Agent** (current): CLI/coder with agentic structure → **Foundation**
2. **exai-mcp-server**: Complex multi-tool system → **WIP**
3. **orchestrator**: Infrastructure framework integration → **WIP**

### Core Capabilities
- **Progressive Skill Loading**: 15+ specialized skills with 3-level disclosure
- **Z.AI Integration**: Direct REST API with GLM-4.5/4.6 models
- **Knowledge Graph**: Persistent context across agent sessions
- **VS Code Integration**: Native Chat API support
- **Organizational Intelligence**: Self-documenting, self-enforcing structure

### Production Status
- **Architecture Compliance**: 95% (80%+ required)
- **Dependencies**: 92/92 packages resolved ✅
- **Services**: 7 Docker services healthy ✅
- **Documentation**: 30+ files organized ✅
- **Quality**: Automated validation operational ✅

---

## 📊 **Documentation Quality Standards**

All documentation follows these principles:

### Clarity
- Clear language and structure
- Progressive disclosure of complexity
- Consistent terminology
- Well-organized sections

### Examples
- Code examples for key concepts
- Command-line examples for procedures
- Architecture diagrams where helpful
- Real-world usage patterns

### Currency
- Regular updates with system changes
- Version tracking and timestamps
- Deprecated content moved to legacy
- Active maintenance and review

### Organization
- 7-category structure for findability
- Cross-references between related docs
- Clear navigation and indexing
- Knowledge graph integration

### Actionable
- Step-by-step procedures
- Checklists for validation
- Troubleshooting guides
- Quick reference sections

---

## 🔄 **Keeping Documentation Current**

### Agent Responsibilities
- Update relevant docs when making changes
- Add new docs to correct categories
- Move outdated content to legacy
- Update this README when adding major docs

### Documentation Checklist
- [ ] Content accurate and tested
- [ ] Examples working and verified
- [ ] Cross-references updated
- [ ] Placed in correct category
- [ ] Timestamp updated
- [ ] Knowledge graph updated

---

## 🛠️ **Validation Tools**

### Pre-Implementation Check
```bash
python scripts/validation/pre_implementation_check.py
```
Validates workspace cleanliness and organizational compliance.

### Architecture Compliance
```bash
python scripts/validation/validate_architectural_compliance.py
```
Ensures implementation follows architectural patterns.

### Organization Validator
```bash
python scripts/assessment/organization_validator.py
```
Checks file placement in correct categories.

---

## 📝 **Contributing to Documentation**

### Adding New Documentation
1. **Determine category** (architecture, workflows, project, setup, examples, testing, troubleshooting)
2. **Follow naming conventions** (UPPERCASE_WITH_UNDERSCORES.md)
3. **Include metadata** (timestamp, version, status)
4. **Add cross-references** to related docs
5. **Update this README** if major addition
6. **Update knowledge graph** with new entities

### Documentation Template
```markdown
# Document Title

## Overview
Brief description of document purpose

## Contents
- Section 1
- Section 2

[Document content]

---

**Last Updated**: YYYY-MM-DD  
**Status**: [Production Ready | WIP | Deprecated]  
**Related Docs**: [Links to related documents]
```

---

## 🔍 **Knowledge Graph Integration**

All documentation is integrated into the knowledge graph system:

### Query Organizational Knowledge
```python
search_nodes("codebase organization")
search_nodes("Universal Workflow Protocol")
read_graph()  # Complete organizational context
```

### Key Entities Available
- **Mini-Agent Codebase Organization System**
- **Document Directory Structure**
- **Scripts Directory Structure**
- **Universal Workflow Protocol**

---

## 📞 **Getting Help**

### For Agents
1. Check [Troubleshooting Guide](troubleshooting/TROUBLESHOOTING.md)
2. Review [Agent Best Practices](workflows/AGENT_BEST_PRACTICES.md)
3. Query knowledge graph for context
4. Run validation tools for diagnostics

### For Users
1. Start with [Setup Guide](setup/SETUP_GUIDE.md)
2. Review [Usage Examples](examples/USAGE_EXAMPLES.md)
3. Check [Troubleshooting](troubleshooting/TROUBLESHOOTING.md)
4. See [Configuration Guide](setup/CONFIGURATION_GUIDE.md)

---

## 🏆 **Documentation Status**

- **Total Files**: 30+ organized documents
- **Categories**: 7 professional categories
- **Quality**: Comprehensive and current
- **Integration**: Knowledge graph enabled
- **Validation**: Automated tools operational
- **Compliance**: 95% architectural standards

---

**Last Updated**: 2025-11-20  
**Current Stage**: Production Ready with Professional Organizational Intelligence  
**System Version**: 0.1.0  
**Maintenance**: Active and regularly updated
