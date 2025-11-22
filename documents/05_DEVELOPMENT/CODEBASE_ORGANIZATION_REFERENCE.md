# Codebase Organization Reference Guide

## 🎯 **ORGANIZATIONAL KNOWLEDGE FOR ALL AGENTS**

This guide is integrated into the knowledge graph system. All agents can query this information using:
- `search_nodes("codebase organization")` 
- `read_graph()` for full organizational context

---

## 📁 **COMPLETE DIRECTORY STRUCTURE**

### **Documents Organization (7 Categories)**
```
documents/
├── architecture/          # System design and architecture
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── VISUAL_ARCHITECTURE_GUIDE.md
│   ├── TECHNICAL_OVERVIEW.md
│   ├── ACP_BRIDGE_COMPLETE.md
│   ├── ACP_IMPLEMENTATION_COMPLETE.md
│   ├── ACP_INTEGRATION_GUIDE.md
│   ├── ACP_INTEGRATION_COMPLETE.md
│   ├── NATIVE_VSCODE_INTEGRATION.md
│   └── SYSTEM_OPTIMIZATION_COMPLETE.md
│
├── workflows/             # Procedures and protocols
│   ├── UNIVERSAL_WORKFLOW_PROTOCOL.md
│   └── AGENT_BEST_PRACTICES.md
│
├── project/               # Project management and context
│   ├── PROJECT_CONTEXT.md
│   ├── AGENT_HANDOFF.md
│   ├── SYSTEM_STATUS.md
│   ├── COMPREHENSIVE_SYSTEM_UPDATE.md
│   └── PROJECT_CLEANUP_SUMMARY.md
│
├── setup/                 # Installation and configuration
│   ├── SETUP_GUIDE.md
│   ├── CONFIGURATION_GUIDE.md
│   └── QUICK_START_GUIDE.md
│
├── examples/              # Usage examples and templates
│   ├── FACT_CHECKING_EXAMPLES.md
│   ├── USAGE_EXAMPLES.md
│   └── USER_SUMMARY.md
│
├── testing/               # Testing and validation reports
│   ├── COMPREHENSIVE_VERIFICATION_REPORT.md
│   ├── PRODUCTION_READINESS_REPORT.md
│   ├── FINAL_PRODUCTION_VERIFICATION.md
│   ├── STRATEGY_VALIDATION_ANALYSIS.md
│   ├── IMMEDIATE_ACTION_PLAN.md
│   ├── ZAI_*.md (all ZAI analysis files)
│   ├── FACT_CHECK_*.md (all fact-checking files)
│   └── VALIDATION_*.md (all validation files)
│
├── troubleshooting/       # Problem resolution
│   ├── TROUBLESHOOTING.md
│   └── ZAI_WEB_READER_ISSUE_RESOLUTION.md
│
├── legacy/               # Historical documentation
│   └── [moved from technical/ directory]
│
├── vscode-extension/     # VS Code extension specific docs
│   ├── 00_IMPLEMENTATION_PATHWAY_SUMMARY.md
│   ├── 01_ACP_VS_CODE_INTEGRATION_OVERVIEW.md
│   ├── 02_ACP_STDIO_SERVER_IMPLEMENTATION.md
│   ├── 03_VSCODE_EXTENSION_DEVELOPMENT.md
│   ├── QUICK_REFERENCE.md
│   └── README.md
│
├── archive/              # Previous agent work (historical)
│   └── [historical files from previous sessions]
│
├── workflows/
│   └── [already listed above]
│   └── SCRIPTS_ORGANIZATION_GUIDE.md
│   └── DOCUMENTS_ORGANIZATION_GUIDE.md
│
└── [main project README.md]  # Project overview
```

### **Scripts Organization (6 Categories)**
```
scripts/
├── validation/            # Fact-checking and compliance
│   ├── validate_architectural_compliance.py
│   ├── pre_implementation_check.py
│   ├── fact_check_my_failures.py
│   └── vscode_integration_validation.txt
│
├── cleanup/               # Workspace maintenance (ready for future)
│   └── [cleaning utilities]
│
├── assessment/            # System analysis and reporting
│   └── organization_validator.py
│
├── deployment/            # Production deployment (ready for future)
│   └── [deployment utilities]
│
├── testing/               # Test automation (ready for future)
│   └── [test utilities]
│
└── utilities/             # General helpers (ready for future)
    └── [helper scripts]
```

---

## 🚀 **AGENT QUICK REFERENCE**

### **Before Starting Any Task:**
```bash
# 1. Check organizational knowledge
search_nodes("codebase organization")
search_nodes("Universal Workflow Protocol")

# 2. Validate workspace
python scripts/validation/pre_implementation_check.py

# 3. Load fact-checking skill
get_skill("fact-checking-self-assessment")

# 4. Review workflow protocol
read_file("documents/workflows/UNIVERSAL_WORKFLOW_PROTOCOL.md")
```

### **Where to Put New Files:**
**Documents:**
- **Architecture docs** → `documents/architecture/`
- **Procedures/guides** → `documents/workflows/`
- **Project management** → `documents/project/`
- **Setup/installation** → `documents/setup/`
- **Usage examples** → `documents/examples/`
- **Testing/validation** → `documents/testing/`
- **Problem resolution** → `documents/troubleshooting/`
- **Historical/deprecated** → `documents/legacy/`

**Scripts:**
- **Validation/compliance** → `scripts/validation/`
- **Maintenance/cleanup** → `scripts/cleanup/`
- **Analysis/reporting** → `scripts/assessment/`
- **Deployment tools** → `scripts/deployment/`
- **Test automation** → `scripts/testing/`
- **General helpers** → `scripts/utilities/`

### **Workflow Integration:**
- **All tasks** must follow 5-phase protocol
- **80%+ compliance** score required for completion
- **Fact-checking** mandatory at milestones
- **Knowledge graph** updates required throughout
- **Documentation** updates in proper categories

---

## 🔍 **KNOWLEDGE GRAPH INTEGRATION**

**Available Entity Queries:**
- `search_nodes("Mini-Agent Codebase Organization System")`
- `search_nodes("Document Directory Structure")`
- `search_nodes("Scripts Directory Structure")`
- `search_nodes("Universal Workflow Protocol")`

**For Complete Context:**
- `read_graph()` - Get all organizational knowledge

**Updated Automatically:**
- New organizational changes persist across sessions
- Agents can build on previous organizational decisions
- Historical decisions preserved for future reference

---

## 📊 **ORGANIZATIONAL ENFORCEMENT**

### **Automated Validators:**
1. **Pre-Implementation Check** - Validates setup before starting
2. **Architecture Compliance** - Ensures architectural patterns followed
3. **Organization Validator** - Checks file placement in correct categories

### **Quality Gates:**
- **Phase Transitions** - Cannot proceed without validation
- **Compliance Scoring** - 80%+ required for completion
- **Knowledge Graph** - Must persist context throughout
- **Documentation** - Must update in proper locations

### **Fail-Safe Mechanisms:**
- **Violation Detection** - Automated checks catch issues
- **Task Blocking** - Cannot proceed with compliance failures
- **Remediation Required** - Must fix issues before continuation
- **Validation Loop** - Re-check until compliance achieved

---

## 🎯 **AGENT SUCCESS PATTERNS**

### **Successful Implementation Checklist:**
- [ ] Query organizational knowledge on startup
- [ ] Run pre-implementation validation
- [ ] Follow 5-phase workflow protocol
- [ ] Place files in correct categories
- [ ] Update knowledge graph throughout
- [ ] Achieve 80%+ compliance score
- [ ] Clean workspace on completion

### **Common Mistakes to Avoid:**
- [ ] **Don't** place files in wrong categories
- [ ] **Don't** skip validation phases
- [ ] **Don't** ignore compliance scoring
- [ ] **Don't** forget knowledge graph updates
- [ ] **Don't** pollute main directory
- [ ] **Don't** bypass architectural patterns

---

**🏆 RESULT**: Self-documenting, self-enforcing organizational system with comprehensive knowledge integration that guides all agents toward consistent, high-quality implementations.

**📖 ACCESS**: This knowledge is permanently stored in the knowledge graph and available to all future agents through entity queries.