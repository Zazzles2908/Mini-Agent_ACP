#!/usr/bin/env python3
"""
Clean up and organize the scripts folder structure
"""

import os
import shutil
from pathlib import Path

def organize_scripts():
    """Organize scripts into logical subdirectories"""
    
    scripts_dir = Path("scripts")
    if not scripts_dir.exists():
        print("❌ Scripts directory not found")
        return
    
    # Create subdirectories
    subdirs = {
        "testing": "All test scripts",
        "setup": "Installation and setup scripts",
        "integration": "Integration and bridge scripts", 
        "utilities": "Utility and helper scripts",
        "maintenance": "Cleanup and maintenance scripts"
    }
    
    for subdir, description in subdirs.items():
        path = scripts_dir / subdir
        path.mkdir(exist_ok=True)
        print(f"✅ Created directory: {subdir}")
    
    # Move files to appropriate directories
    file_moves = {
        # Testing scripts
        "testing": [
            "test_acp_library.py",
            "test_acp_pattern.py", 
            "test_acp_stdio.py",
            "test_acp_stdio_detailed.py",
            "test_basic_server.py",
            "test_complete_integration.py",
            "test_enhanced_server.py",
            "test_extension_transport.py",
            "test_production_server.py",
            "test_simple_acp.py",
            "test_spawn_functions.py",
            "test_zai_coding_plan_functionality.py",
            "test_zai_comparison.py",
            "test_zai_fixes.py",
            "test_zai_reader.py",
            "test_zai_reader_fix.py",
            "test_zai_tools.py",
            "test_corrected_zai.py",
            "test_correct_models.py",
            "test_enhanced_acp.py",
            "test_authentication_fixes.py",
            "test_acp_integration.py",
            "test_acp_setup.py",
            "comprehensive_zai_test.py",
            "final_test_zai_reader.py",
            "simple_acp_test.py",
            "test_lite_plan_implementation.py",
            "test_coding_plan_functionality.py"
        ],
        
        # Setup scripts
        "setup": [
            "install_dependencies.py",
            "setup_mini_agent.py",
            "setup_acp_bridge.py",
            "launch_mini_agent.py"
        ],
        
        # Integration scripts
        "integration": [
            "acp_terminal_bridge.py",
            "agent_integration.py",
            "vscode_acp_bridge.py"
        ],
        
        # Utility scripts  
        "utilities": [
            "example_implementation.py",
            "fact_checker.py",
            "production_fact_checker.py",
            "quick_validator.py",
            "load_agent_context.py"
        ],
        
        # Maintenance scripts
        "maintenance": [
            "cleanup_and_organize.py",
            "cleanup_and_organize_fixed.py", 
            "simple_cleanup.py",
            "investigate_zai_reader.py"
        ]
    }
    
    # Move files
    moved_count = 0
    for subdir, files in file_moves.items():
        for filename in files:
            source = scripts_dir / filename
            if source.exists():
                target = scripts_dir / subdir / filename
                try:
                    shutil.move(str(source), str(target))
                    print(f"✅ Moved {filename} → {subdir}/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Failed to move {filename}: {e}")
            else:
                print(f"⚠️ File not found: {filename}")
    
    print(f"\n📊 Summary: {moved_count} files organized")
    
    # List remaining files in root scripts directory
    remaining_files = list(scripts_dir.glob("*.py"))
    if remaining_files:
        print(f"\n📋 Remaining files in scripts/ (need manual review):")
        for f in sorted(remaining_files):
            print(f"  - {f.name}")
    
    # Create README for the scripts folder
    readme_content = """# Scripts Directory

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
"""
    
    readme_path = scripts_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"\n📚 Created: {readme_path}")

if __name__ == "__main__":
    organize_scripts()