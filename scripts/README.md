# Scripts Directory

This directory contains all Mini-Agent utility scripts, organized by purpose.

## Directory Structure

### `/testing/` - Test Scripts
All test scripts for validating functionality:
- Z.AI functionality tests
- ACP integration tests  
- VS Code extension tests
- Model and client tests

### `/setup/` - Setup Scripts  
Installation and environment setup scripts:
- Dependency installation
- Mini-Agent initialization
- ACP bridge setup

### `/integration/` - Integration Scripts
Bridge and integration scripts:
- ACP terminal bridging
- Agent integration workflows
- VS Code extension integration

### `/utilities/` - Utility Scripts
Helper and utility functions:
- Example implementations
- Fact checking utilities
- Validation tools

### `/maintenance/` - Maintenance Scripts
Cleanup and maintenance scripts:
- Directory cleanup
- File organization
- Investigation tools

## Usage

Run scripts from the root directory:
```bash
python scripts/testing/test_zai_functionality.py
python scripts/setup/install_dependencies.py
```

## Guidelines

- Keep scripts focused and single-purpose
- Use descriptive names (verb_noun.py format)
- Add docstrings with purpose and usage
- Organize by functionality, not by technology
- Remove duplicates and outdated scripts
