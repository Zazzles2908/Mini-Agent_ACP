# Agent Best Practices - Mini-Agent Architectural Compliance

## 🚨 **MANDATORY FIRST STEPS FOR ALL NEW AGENTS**

When a new agent session is activated, they **MUST** follow these steps in this exact order:

### 1. **Organizational Knowledge Discovery**
```bash
# REQUIRED: Query organizational knowledge system
search_nodes("Mini-Agent Codebase Organization System")
search_nodes("Universal Workflow Protocol")

# REQUIRED: Get complete organizational context
read_graph()

# REQUIRED: Review organization reference guide
read_file("documents/CODEBASE_ORGANIZATION_REFERENCE.md")
```

### 2. **Fact-Checking Skill Preparation**
```bash
# REQUIRED: Load fact-checking skill for validation
get_skill("fact-checking-self-assessment")
```

### 3. **Current State Assessment**
```bash
# REQUIRED: Assess current workspace and organization
bash("Get-ChildItem -Path 'Mini-Agent' -Recurse")
git_status(repo_path="Mini-Agent")
```

### 4. **Workspace Validation**
```bash
# REQUIRED: Validate workspace cleanliness
- No Python files in main directory
- No directories in wrong locations (skills/, not /skills)
- All skills properly located in mini_agent/skills/
- Proper documentation structure
```

## 📋 **MANDATORY COMPLIANCE CHECKLIST**

### Before Starting ANY Task:
- [ ] Read architectural mastery document
- [ ] Load fact-checking skill  
- [ ] Assess current workspace state
- [ ] Validate clean organization

### During Implementation:
- [ ] Use fact-checking for validation
- [ ] Follow progressive skill loading (Level 1→2→3)
- [ ] Maintain knowledge graph integration
- [ ] Keep workspace organized (no pollution)
- [ ] Place all files in correct directories

### Before Completion:
- [ ] Run architectural compliance check
- [ ] Validate all files in proper locations
- [ ] Ensure progressive skill system integration
- [ ] Check knowledge graph persistence
- [ ] Clean up any polluting files

## 🏗️ **REQUIRED ARCHITECTURE PATTERNS**

### Progressive Skill Loading System
```python
# Level 1: Metadata Discovery
list_skills()  # Shows available skills

# Level 2: Full Content Loading  
get_skill("skill_name")  # Loads complete skill content

# Level 3: Resources Execution
execute_with_resources("skill_name", mode="execution")
```

### Skills Directory Structure
```
mini_agent/skills/{skill_name}/
├── SKILL.md              # REQUIRED: Skill documentation
├── README.md             # Optional: Additional docs
└── scripts/
    ├── {skill_name}.py   # REQUIRED: Implementation
    └── [other resources] # Optional: Additional files
```

### Workspace Organization
```
Mini-Agent/
├── documents/           # ALL documentation
├── scripts/             # Utility scripts
│   ├── validation/      # Fact-checking & tests
│   ├── cleanup/         # Maintenance scripts
│   └── [categorized]
├── mini_agent/skills/   # Skills ONLY (not /skills)
├── tests/               # Official test suite
└── [core files]         # Essential project files
```

### Knowledge Graph Integration
```python
# All skills MUST integrate with knowledge graph
- create_entities() - For system components
- create_relations() - For component connections  
- add_observations() - For context persistence
- read_graph() - For state retrieval
```

## ❌ **CRITICAL VIOLATIONS TO AVOID**

### Directory Pollution
- **NEVER** place Python files in main directory
- **NEVER** create `/skills` directory (use `/mini_agent/skills`)
- **NEVER** scatter test scripts in root
- **ALWAYS** use `scripts/` for utilities

### Architecture Bypass
- **NEVER** create standalone implementations
- **NEVER** skip progressive skill loading
- **NEVER** ignore knowledge graph integration
- **ALWAYS** follow native skill system patterns

### Fact-Checking Failures
- **NEVER** complete tasks without validation
- **NEVER** skip architectural compliance checks
- **ALWAYS** use fact-checking skill before completion

## 🛠️ **VALIDATION TOOLS**

### Architecture Compliance Check
```bash
# Create this validation script
fact_check_architecture.py:
- Check skills directory structure
- Validate progressive loading implementation  
- Ensure knowledge graph integration
- Verify workspace cleanliness
- Generate compliance score
```

### Workspace Cleanup Validation
```bash
# Required validation commands
1. No .py files in main directory
2. All skills in mini_agent/skills/ 
3. All validation scripts in scripts/validation/
4. All documentation in documents/
5. Proper directory hierarchy maintained
```

## 📊 **COMPLIANCE SCORING**

### Score Categories (0-100)
- **Architecture Alignment**: 25 points
- **Directory Organization**: 25 points  
- **Progressive Loading**: 25 points
- **Knowledge Graph Integration**: 15 points
- **Fact-Checking Validation**: 10 points

### Success Thresholds
- **90-100%**: ✅ Production Ready
- **80-89%**: ⚠️ Review Recommended  
- **70-79%**: 🔄 Significant Issues
- **Below 70%**: ❌ Critical Failures

## 🔄 **REMEDIATION PROCESS**

If Compliance Score < 80%:

1. **Immediate Actions**:
   - Stop current task
   - Run fact-checking validation
   - Identify specific violations
   - Create remediation plan

2. **Cleanup Sequence**:
   - Remove polluting files
   - Reorganize to proper structure  
   - Implement missing architecture patterns
   - Re-run compliance check

3. **Validation Loop**:
   - Re-run all compliance checks
   - Ensure 80%+ score achieved
   - Only then continue with task

## 🎯 **AGENT ACTIVATION PROTOCOL**

### New Agent Session Checklist:
1. **Read** `documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md`
2. **Load** `get_skill("fact-checking-self-assessment")`  
3. **Assess** workspace state with `git_status()` and directory listing
4. **Validate** architectural compliance with fact-checking
5. **Proceed** only if 80%+ compliance score achieved

### Handoff Documentation Requirements:
- Update `documents/AGENT_HANDOFF.md` with current status
- Record architectural decisions made
- Document any compliance issues found and resolved
- List remaining tasks with architectural considerations

## 📝 **IMPLEMENTATION TEMPLATE**

### For Any New Feature/Task:
```python
# Step 1: Architecture Review
read_file("documents/MINI_AGENT_ARCHITECTURAL_MASTERY.md")

# Step 2: Fact-Checking Preparation  
fact_check_request = """
Use fact-checking to validate this implementation:
- Task: [Describe task]
- Architecture requirements: [List requirements]
- Expected compliance: [80%+ target]
"""

# Step 3: Implementation Following Patterns
# - Progressive skill loading
# - Knowledge graph integration
# - Proper directory structure

# Step 4: Final Validation
# - Compliance check
# - Workspace cleanup
# - Documentation update
```

---

**CRITICAL REMINDER**: These practices are mandatory, not optional. Non-compliance will result in poor architectural alignment and require extensive remediation. Always prioritize architecture over speed of implementation.

**Success Metric**: Every task must achieve 80%+ architectural compliance score before completion.