# Scripts Organization Guide

## 📁 **Organized Script Structure**

All scripts in the Mini-Agent project must follow this hierarchical organization:

```
scripts/
├── validation/           # Fact-checking and architectural compliance
│   ├── validate_architectural_compliance.py
│   ├── fact_check_my_failures.py
│   ├── vscode_integration_validation.txt
│   └── [other validation scripts]
├── cleanup/              # Workspace maintenance and organization
│   ├── workspace_validator.py
│   ├── file_organization_cleanup.py
│   └── [other cleanup utilities]
├── assessment/           # System analysis and reporting
│   ├── knowledge_graph_status.py
│   ├── system_assessment.py
│   └── [other assessment tools]
├── deployment/           # Production deployment utilities
├── testing/              # Test automation and fixtures
└── utilities/            # General-purpose helper scripts
```

## 📋 **Script Categorization Rules**

### 🔍 **validation/** Scripts
**Purpose**: Fact-checking, compliance validation, architectural assessment
**Criteria**: 
- Validates architectural compliance
- Performs fact-checking operations
- Assesses implementation quality
- Generates compliance reports

**Examples**:
- `validate_architectural_compliance.py`
- `fact_check_my_failures.py`
- `compliance_reporter.py`

### 🧹 **cleanup/** Scripts  
**Purpose**: Workspace maintenance and organization
**Criteria**:
- Cleans up temporary files
- Organizes directory structure
- Validates workspace cleanliness
- Maintains proper file organization

**Examples**:
- `workspace_validator.py`
- `file_organization_cleanup.py`
- `temp_file_remover.py`

### 📊 **assessment/** Scripts
**Purpose**: System analysis and comprehensive reporting
**Criteria**:
- Analyzes system state
- Generates detailed reports
- Measures performance metrics
- Assesses knowledge graph status

**Examples**:
- `knowledge_graph_status.py`
- `system_assessment.py`
- `performance_metrics.py`

### 🚀 **deployment/** Scripts
**Purpose**: Production deployment and configuration
**Criteria**:
- Handles production deployment
- Manages configuration
- Sets up production environment
- Handles deployment validation

### 🧪 **testing/** Scripts
**Purpose**: Test automation and test fixtures
**Criteria**:
- Automates test execution
- Provides test fixtures
- Manages test data
- Handles test reporting

### 🔧 **utilities/** Scripts
**Purpose**: General-purpose helper scripts
**Criteria**:
- Miscellaneous utility functions
- Helper scripts for development
- Common operations automation
- Integration utilities

## 🚨 **Script Placement Rules**

### ✅ **Correct Placement**
```bash
# Fact-checking script → validation/
scripts/validation/compliance_checker.py

# Workspace cleanup → cleanup/  
scripts/cleanup/workspace_organizer.py

# System analysis → assessment/
scripts/assessment/system_status.py
```

### ❌ **Incorrect Placement**
```bash
# Don't place in wrong category
scripts/validation/deployment_script.py    # Wrong!

# Don't place in main directory
compliance_check.py                       # Wrong!

# Don't create new top-level directories without approval
scripts/new_category/script.py            # Wrong!
```

## 📝 **Script Documentation Requirements**

### Header Requirements
Every script must include:
```python
#!/usr/bin/env python3
"""
Script Name - Brief Description

Purpose: What this script does
Category: validation|cleanup|assessment|deployment|testing|utilities
Architecture Compliance: Yes|No
Last Updated: YYYY-MM-DD
"""

import os
import sys
# ... rest of script
```

### File Naming Conventions
- **Use descriptive names**: `validate_architectural_compliance.py`
- **CamelCase or snake_case**: Choose one and be consistent
- **Action-oriented**: Start with verb (validate, cleanup, assess)
- **No spaces or special characters**: Use underscores

## 🔧 **Script Quality Standards**

### Code Quality
- **Clean, readable code**: Follow PEP 8
- **Proper error handling**: Handle edge cases gracefully
- **Logging and output**: Clear feedback to user
- **Documentation**: Comments explaining complex logic

### Functionality Standards
- **Single responsibility**: Each script does one thing well
- **Modularity**: Reusable functions when appropriate
- **Configuration**: Accept parameters for flexibility
- **Validation**: Validate inputs and outputs

### Integration Requirements
- **Workspace awareness**: Understand current directory structure
- **Architecture compliance**: Follow Mini-Agent patterns
- **Knowledge graph**: Update relevant entities when applicable
- **File organization**: Maintain proper directory structure

## 📋 **Script Review Checklist**

Before adding any script to the repository:

### Functionality ✅
- [ ] Script serves a clear purpose
- [ ] Functionality is well-defined
- [ ] Error handling is comprehensive
- [ ] Output is informative and helpful

### Organization ✅
- [ ] Placed in correct category directory
- [ ] Follows naming conventions
- [ ] Proper documentation header
- [ ] Comments explain complex logic

### Integration ✅
- [ ] Architecture compliant
- [ ] Works with existing system
- [ ] Updates knowledge graph if needed
- [ ] Validates workspace organization

### Quality ✅
- [ ] Code follows standards
- [ ] Handles edge cases
- [ ] Provides useful feedback
- [ ] Is maintainable and extensible

## 🚀 **Script Development Workflow**

### 1. **Planning Phase**
```bash
# Determine script category and purpose
# Plan integration with existing system
# Design interface and functionality
```

### 2. **Development Phase**
```bash
# Create in appropriate category directory
# Follow naming and documentation standards
# Implement with proper error handling
# Test with various inputs and edge cases
```

### 3. **Validation Phase**
```bash
# Run architectural compliance check
# Validate integration with existing system
# Test workspace organization impact
# Update knowledge graph if needed
```

### 4. **Integration Phase**
```bash
# Add to version control
# Update relevant documentation
# Create usage examples
# Document in appropriate guides
```

## 📊 **Script Metrics and Monitoring**

### Quality Metrics
- **Architecture Compliance**: All scripts must be compliant
- **Documentation Coverage**: 100% of scripts documented
- **Error Handling**: Graceful failure for all edge cases
- **Integration Score**: Seamless integration with existing system

### Usage Monitoring
- **Script Utilization**: Track which scripts are most used
- **Performance Impact**: Monitor execution time and resource usage
- **Error Rates**: Track failure rates and common issues
- **User Feedback**: Collect feedback for improvements

---

**CRITICAL**: All scripts must follow this organization structure. Scripts placed incorrectly or without proper categorization will be moved to appropriate locations during workspace maintenance.