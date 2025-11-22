# Critical System Prompt Updates Needed

## **1. File Organization Rules (HIGHEST PRIORITY)**

### CRITICAL: Never Create Files in Root Directory
```
❌ NEVER create files directly in project root
✅ ALWAYS use proper subdirectories:
   - mini_agent/ for core functionality
   - documents/ for documentation
   - tests/ for test files
   - workspace/ for user projects
```

### Script Management Rules
```
❌ DO NOT create external scripts unless absolutely necessary
✅ PREFER integration: Add functionality to existing modules
✅ USE mini_agent/[feature]/ structure over scattered scripts
```

## **2. Code Quality Standards (CRITICAL)**

### Syntax & Import Validation
```
✅ AFTER ANY CODE CHANGES:
   1. Test basic imports: python -c "from mini_agent.cli import main"
   2. Verify syntax: python -m py_compile file.py
   3. Check main entry points still work: mini-agent --help

❌ NEVER commit code without syntax validation
```

### Error Prevention Protocol
```
✅ MAJOR CHANGES MUST INCLUDE:
   - Import testing after each change
   - Core functionality verification
   - Entry point testing (CLI commands)
```

## **3. Development Process Rules**

### Before Creating New Scripts
```
ASK YOURSELF:
1. Is this functionality already in an existing module?
2. Can this integrate into mini_agent/core/ or another module?
3. Does this really need to be a standalone script?

❌ DEFAULT: Create standalone scripts
✅ DEFAULT: Integrate into existing modules
```

### When Adding Features
```
MANDATORY CHECKLIST:
□ Step 1: Check existing modules first
□ Step 2: Integrate into appropriate location if possible
□ Step 3: Test existing functionality still works  
□ Step 4: Verify entry points work
□ Step 5: Test imports work: from mini_agent.core import [new_function]
```

## **4. Cleanup Prevention**

### Root Cause Prevention
```
The chaos occurred because:
❌ No guidelines about file organization
❌ Easy script creation without integration consideration
❌ No testing of core functionality after changes
❌ Multiple small changes compounded into chaos

PREVENTION STRATEGY:
✅ System prompt enforces proper organization from start
✅ Every file creation considers existing structure
✅ Major changes include verification of basic functionality
```

## **5. Emergency Response Protocol**

### When System Breaks
```
IMMEDIATE ACTIONS:
1. Check syntax errors: python -c "import module_name"
2. Verify entry points: mini-agent --help
3. Test core imports: from mini_agent.core import SystemMonitor
4. Check recent changes and rollback if needed
```

## **6. Documentation Updates**

### File Creation Guidelines
```
✅ ALWAYS update documentation when:
   - Adding new functionality
   - Moving files between directories
   - Creating new modules
   - Breaking changes to existing code

❌ NEVER leave documentation outdated
```

## **Priority Implementation:**

1. **IMMEDIATE**: Add file organization rules to system prompt
2. **HIGH**: Add syntax validation requirements
3. **MEDIUM**: Add development process checklists
4. **ONGOING**: Update documentation as system evolves

**Goal**: Never again create a situation where 150+ scripts accumulate or core functionality breaks due to improper file management.