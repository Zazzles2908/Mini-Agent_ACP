#!/usr/bin/env python3
"""Fix agent file access issues and provide proper workspace configuration."""

import sys
import os
from pathlib import Path

def fix_agent_workspace_issues():
    """Fix the workspace directory and file path issues."""
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if documents directory exists and has files
    documents_dir = current_dir / "documents"
    print(f"Documents directory: {documents_dir}")
    print(f"Documents exists: {documents_dir.exists()}")
    
    if documents_dir.exists():
        print("Documents subdirectories:")
        for subdir in sorted(documents_dir.iterdir()):
            if subdir.is_dir():
                print(f"  📁 {subdir.name}/")
        
        print("Documents markdown files:")
        for md_file in documents_dir.rglob("*.md"):
            print(f"  📄 {md_file.relative_to(documents_dir)}")
    
    # Check for PROJECT_CONTEXT.md files
    context_files = list(current_dir.rglob("PROJECT_CONTEXT.md"))
    print(f"\nFound {len(context_files)} PROJECT_CONTEXT.md files:")
    for file in context_files:
        rel_path = file.relative_to(current_dir)
        print(f"  📄 {rel_path}")
    
    # Create a working solution
    print("\n=== WORKING SOLUTIONS ===")
    
    # 1. List documents directory contents
    if documents_dir.exists():
        print("1. To explore documents, use these paths:")
        for subdir in sorted(documents_dir.iterdir()):
            if subdir.is_dir():
                rel_path = subdir.relative_to(current_dir)
                print(f"   read_file: {rel_path}")
    
    # 2. Find specific files
    if context_files:
        print("\n2. PROJECT_CONTEXT.md files found at:")
        for file in context_files:
            rel_path = file.relative_to(current_dir)
            print(f"   read_file: {rel_path}")
    
    # 3. Test workspace resolution
    print("\n3. Workspace resolution test:")
    workspace_path = Path("./workspace").absolute()
    print(f"   Config workspace: {workspace_path}")
    print(f"   Workspace exists: {workspace_path.exists()}")
    
    # Check if files would be accessible from workspace
    print(f"\n4. File accessibility test:")
    test_files = ["README.md", "documents/01_OVERVIEW/PROJECT_CONTEXT.md"]
    for test_file in test_files:
        workspace_file = workspace_path / test_file
        print(f"   {test_file}: {'✅' if workspace_file.exists() else '❌'} (workspace lookup)")
        
        root_file = current_dir / test_file
        print(f"   {test_file}: {'✅' if root_file.exists() else '❌'} (root lookup)")

if __name__ == "__main__":
    fix_agent_workspace_issues()
