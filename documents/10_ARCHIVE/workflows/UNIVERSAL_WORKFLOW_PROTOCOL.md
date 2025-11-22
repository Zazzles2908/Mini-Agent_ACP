# Mini-Agent Universal Workflow Protocol

## 🎯 **MANDATORY WORKFLOW FOR ALL TASKS**

Every task, regardless of complexity, must follow this exact sequence:

### **Phase 1: Pre-Implementation (Mandatory)**
```bash
# 1. Architecture Review
read_file("documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md")
read_file("documents/AGENT_BEST_PRACTICES.md")

# 2. State Assessment  
git_status(repo_path="Mini-Agent")
bash("Get-ChildItem -Path 'Mini-Agent' -Recurse -ErrorAction SilentlyContinue")

# 3. Fact-Checking Preparation
get_skill("fact-checking-self-assessment")

# 4. Compliance Validation
python scripts/validation/validate_architectural_compliance.py
```

### **Phase 2: Planning & Design (Mandatory)**
```bash
# 5. Task Decomposition
# Break down into implementation phases
# Identify required architecture patterns
# Map to existing skill system where possible

# 6. Implementation Strategy Selection
# - Native Skill Integration (preferred)
# - Tool Extension (if needed)  
# - External Integration (last resort)

# 7. Knowledge Graph Planning
# Plan entities, relations, observations needed
# Identify context persistence requirements
```

### **Phase 3: Implementation (Structured)**
```bash
# 8. Progressive Development
# Follow Level 1→2→3 skill loading patterns
# Use existing tool infrastructure
# Maintain knowledge graph integration

# 9. Validation at Each Step
# Fact-check after each major component
# Validate architectural compliance incrementally
# Maintain workspace organization
```

### **Phase 4: Testing & Validation (Mandatory)**
```bash
# 10. Functional Testing
# Test all major functionality
# Validate tool integration
# Check error handling

# 11. Architectural Compliance
# Run full compliance validation
# Ensure 80%+ score achieved
# Fix any violations

# 12. Documentation Update
# Update relevant documentation files
# Record implementation decisions
# Update agent handoff notes
```

### **Phase 5: Completion & Handoff (Mandatory)**
```bash
# 13. Final Workspace Validation
# Clean up any temporary files
# Ensure proper organization
# Verify no pollution

# 14. Knowledge Graph Completion
# Create entities for implemented components
# Add relations between components  
# Record observations about implementation

# 15. Handoff Documentation
# Update documents/AGENT_HANDOFF.md
# Record current status and next steps
# Document any architectural decisions made
```

---

## 📋 **WORKFLOW VALIDATION CHECKLIST**

### Pre-Implementation ✅
- [ ] Architectural documents reviewed
- [ ] Current state assessed  
- [ ] Fact-checking skill loaded
- [ ] Initial compliance validation passed

### Planning ✅
- [ ] Task decomposed into phases
- [ ] Architecture pattern selected
- [ ] Knowledge graph integration planned
- [ ] Implementation strategy defined

### Implementation ✅
- [ ] Progressive skill loading followed
- [ ] Native tool integration maintained
- [ ] Knowledge graph updates during development
- [ ] Incremental validation performed

### Testing ✅
- [ ] Functional testing completed
- [ ] Architectural compliance validated
- [ ] Error handling verified
- [ ] Documentation updated

### Completion ✅
- [ ] Workspace organization verified
- [ ] Knowledge graph finalized
- [ ] Handoff documentation complete
- [ ] Compliance score 80%+

---

## 🔧 **WORKFLOW ENFORCEMENT MECHANISMS**

### Phase Gates
**Each phase must complete before moving to next:**
- Phase 1 → Phase 2: All pre-implementation checks passed
- Phase 2 → Phase 3: Implementation plan approved
- Phase 3 → Phase 4: Implementation functional
- Phase 4 → Phase 5: Validation and testing passed

### Validation Requirements
- **Fact-check at major milestones**
- **Compliance check at phase transitions**
- **Workspace validation before completion**
- **Knowledge graph persistence throughout**

### Fail-Safe Procedures
**If any phase fails:**
1. **Stop immediately**
2. **Diagnose specific failure**
3. **Remediate before continuation**
4. **Re-validate before proceeding**

---

## 🎯 **TASK TYPE SPECIFIC ADAPTATIONS**

### For New Features
- Emphasize architectural pattern matching
- Validate against existing skill system
- Ensure progressive enhancement

### For Bug Fixes
- Minimal change principle
- Regression testing mandatory
- Documentation update required

### For Optimization
- Performance measurement baseline
- Architecture impact assessment
- Rollback plan required

### For Documentation
- Technical accuracy validation
- Architecture alignment check
- Cross-reference verification

---

## 📊 **WORKFLOW QUALITY METRICS**

### Completion Criteria
- **Compliance Score**: 80%+ required
- **Test Coverage**: All major paths tested
- **Documentation**: Complete and current
- **Architecture**: Aligned with intrinsic patterns

### Success Indicators
- Clean workspace organization
- Proper skill system integration
- Knowledge graph persistence
- Future agent handoff ready

### Red Flags (Stop Immediately)
- Compliance score below 80%
- Workspace pollution detected
- Architectural violations
- Missing validation steps

---

## 🚀 **AUTOMATED WORKFLOW ASSISTANCE**

### Script Tools Available
```bash
# Phase 1 Validation
python scripts/validation/pre_implementation_check.py

# Architecture Compliance  
python scripts/validation/validate_architectural_compliance.py

# Workspace Cleanup
python scripts/cleanup/workspace_validator.py

# Knowledge Graph Assessment
python scripts/assessment/knowledge_graph_status.py
```

### Reporting Requirements
**Each phase generates:**
- Phase completion report
- Validation scores
- Recommendations for next phase
- Risk assessment if issues found

---

## 📝 **WORKFLOW CUSTOMIZATION**

### For Different Complexity Levels
- **Simple Tasks (1-2 hours)**: Abbreviated but complete workflow
- **Complex Tasks (1+ days)**: Full detailed workflow with more validation
- **Multi-agent Tasks**: Enhanced handoff procedures

### For Different Task Types
- **Research Tasks**: Enhanced validation and fact-checking
- **Implementation Tasks**: Full architectural compliance
- **Documentation Tasks**: Accuracy and completeness validation

---

**CRITICAL**: This workflow is **mandatory, not optional**. Every task, regardless of size or complexity, must follow all phases. Non-compliance will result in poor architectural alignment and require extensive remediation.

**Success Standard**: Only complete tasks that pass all workflow validation gates with 80%+ compliance scores.