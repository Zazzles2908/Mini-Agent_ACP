# System Prompt Updates Needed

## 1. File Organization Guidelines

### CRITICAL: Never Create Files in Main Directory
- **Add to system prompt**: "NEVER create files directly in the project root directory"
- **Always use proper subdirectories**:
  - `mini_agent/` for core functionality
  - `documents/` for documentation  
  - `scripts/` for utilities (only if no better location exists)
  - `tests/` for test files

### Script Management
- **Add guideline**: "DO NOT create external scripts unless absolutely necessary"
- **Prefer integration**: "When adding functionality, integrate it into existing modules rather than creating standalone scripts"
- **Directory preference**: "Use `mini_agent/[feature]/` structure over scattered scripts"

## 2. Code Quality Standards

### Import Management
- **Add**: "Always test imports after major changes"
- **Add**: "Never break existing functionality when adding new features"
- **Add**: "Verify syntax with Python before committing"

### Error Prevention
- **Add**: "Check for syntax errors after each code change"
- **Add**: "Test that main entry points (like `mini-agent` command) still work"
- **Add**: "Verify core functionality after any refactoring"

## 3. Development Process

### Before Creating New Scripts
- **Ask**: "Is this functionality already available in an existing module?"
- **Ask**: "Can this be integrated into `mini_agent/core/` or another existing module?"
- **Ask**: "Does this really need to be a standalone script?"

### When Adding Features
- **Step 1**: Check existing modules first
- **Step 2**: Integrate into appropriate location if possible  
- **Step 3**: Test that existing functionality still works
- **Step 4**: Verify entry points (CLI commands, imports, etc.)

## 4. Cleanup Prevention

### Root Cause Analysis
The script chaos occurred because:
1. **No guidelines** about file organization
2. **Easy to create scripts** without thinking about integration
3. **No testing** of core functionality after changes
4. **No awareness** of how multiple small changes compound

### Future Prevention
- **System prompt should enforce** proper organization from start
- **Every file creation** should consider existing structure
- **Major changes** should include verification of basic functionality
- **Documentation** should be updated to reflect proper patterns